use super::{Game, Hit, right_click_crops as core};
use horizon_client::{command::args::GameMode, first_person::Hand, items::ItemStack};
use horizon_core::position::BlockPos;
use horizon_world::{level::flags::{UPDATE_ALL, UPDATE_CLIENTS, UPDATE_KNOWN_SHAPE, UPDATE_SUPPRESS_DROPS}, registry::BlockStateId};
use winit::keyboard::KeyCode;

impl core::SeedStack for ItemStack {
    fn item(&self) -> &str { &self.item }
    fn count(&self) -> u32 { self.count }
    fn count_mut(&mut self) -> &mut u32 { &mut self.count }
}

fn enabled(game: &Game<'_>) -> bool {
    core::enabled(game.native_on(core::MOD_ID))
}

struct CropTarget {
    pos: [i32; 3],
    state: BlockStateId,
    crop: core::Crop,
    upper: Option<([i32; 3], BlockStateId)>,
}

struct ColumnTarget {
    blocks: Vec<([i32; 3], BlockStateId)>,
}

enum Target {
    Crop(CropTarget),
    Column(ColumnTarget),
}

fn target(game: &Game<'_>, hit: &Hit) -> Option<Target> {
    let bone_meal = |s: &ItemStack| s.count > 0 && &*s.item == "minecraft:bone_meal";
    let main = game.stack_in(game.selected);
    if game.mode != GameMode::Survival
        || main.is_some_and(bone_meal)
        || game.offhand.as_ref().is_some_and(bone_meal)
        || (game.keys.contains(&KeyCode::ShiftLeft) && (main.is_some() || game.offhand.is_some()))
        || !game.world.loaded(hit.pos[0], hit.pos[2])
    {
        return None;
    }
    let clicked_state = game.world.block(hit.pos[0], hit.pos[1], hit.pos[2]);
    let clicked_name = game.res.facts().get(clicked_state).name.clone();
    if core::column_item(&clicked_name).is_some() {
        let mut base_y = hit.pos[1];
        while base_y > hit.pos[1] - 32 {
            let below = game.world.block(hit.pos[0], base_y - 1, hit.pos[2]);
            if game.res.facts().get(below).name != clicked_name { break; }
            base_y -= 1;
        }
        let mut blocks = Vec::new();
        for y in base_y + 1..=base_y + 32 {
            let state = game.world.block(hit.pos[0], y, hit.pos[2]);
            if game.res.facts().get(state).name != clicked_name { break; }
            blocks.push(([hit.pos[0], y, hit.pos[2]], state));
        }
        if !blocks.is_empty() { return Some(Target::Column(ColumnTarget { blocks })); }
        return None;
    }
    let mut pos = hit.pos;
    let mut state = game.world.block(pos[0], pos[1], pos[2]);
    let clicked = game.pack.assets.registry.state(state)?;
    if &*game.res.facts().get(state).name == "minecraft:pitcher_crop"
        && clicked.properties.get("half").map(String::as_str) == Some("upper")
    {
        pos[1] -= 1;
        state = game.world.block(pos[0], pos[1], pos[2]);
    }
    let crop = core::crop_profile(&game.res.facts().get(state).name)?;
    let properties = &game.pack.assets.registry.state(state)?.properties;
    if crop.mature_age.is_some_and(|age| properties.get("age").map(String::as_str) != Some(age)) {
        return None;
    }
    let upper = if crop.two_blocks {
        if properties.get("half").map(String::as_str) != Some("lower") { return None; }
        let upper_pos = [pos[0], pos[1] + 1, pos[2]];
        let upper_state = game.world.block(upper_pos[0], upper_pos[1], upper_pos[2]);
        let upper_props = &game.pack.assets.registry.state(upper_state)?.properties;
        if &*game.res.facts().get(upper_state).name != "minecraft:pitcher_crop"
            || upper_props.get("age").map(String::as_str) != crop.mature_age
            || upper_props.get("half").map(String::as_str) != Some("upper")
        { return None; }
        Some((upper_pos, upper_state))
    } else { None };
    Some(Target::Crop(CropTarget { pos, state, crop, upper }))
}

// No prediction and no packets here: the original caller still sends UseItemOn.
pub(super) fn client_takes(game: &Game<'_>, hit: &Hit) -> bool {
    game.integrated.is_some() && enabled(game) && target(game, hit).is_some()
}

pub(super) fn harvest(game: &mut Game<'_>, hit: Option<&Hit>) -> horizon_client::Result<bool> {
    if !enabled(game) || game.remote.is_some() || game.hand != Hand::Main {
        return Ok(false);
    }
    // No capability handshake exists for external players in this prototype.
    let local_actor = match game.serving.as_ref() {
        Some(server) => game.lan_acting_uuid == Some(server.owner),
        None => game.options.dedicated.is_none() && game.lan_acting.is_none(),
    };
    if !local_actor { return Ok(false); }
    let Some(hit) = hit else { return Ok(false); };
    let Some(target) = target(game, hit) else { return Ok(false); };
    let crop_target = match target {
        Target::Column(column) => {
            let held = game.held().cloned();
            let mut loot = Vec::new();
            if game.ui.rules.bool("block_drops") {
                for (pos, state) in &column.blocks {
                    loot.extend(game.block_loot_at(*pos, *state, held.as_ref()));
                }
            }
            let written = game.with_level(|b, level, ticks| {
                let mut changed: Vec<([i32; 3], BlockStateId)> = Vec::new();
                for (pos, state) in column.blocks.iter().rev() {
                    let at = BlockPos::new(pos[0], pos[1], pos[2]);
                    if !b.set_block(level, ticks, at, BlockStateId(0), UPDATE_ALL | UPDATE_SUPPRESS_DROPS) {
                        for (restore_pos, restore_state) in changed.iter().rev() {
                            let restore_at = BlockPos::new(restore_pos[0], restore_pos[1], restore_pos[2]);
                            let _ = b.set_block(level, ticks, restore_at, *restore_state, UPDATE_ALL);
                        }
                        return false;
                    }
                    changed.push((*pos, *state));
                }
                true
            });
            if !written { return Ok(true); }
            for stack in loot {
                if stack.count > 0 && &*stack.item != "minecraft:air" {
                    game.pop_resource(hit.pos, stack);
                }
            }
            game.process_level_events()?;
            game.swing_arm();
            return Ok(true);
        }
        Target::Crop(crop) => crop,
    };
    let CropTarget { pos, state, crop, upper } = crop_target;
    let at = BlockPos::new(pos[0], pos[1], pos[2]);
    let young = if let Some(name) = crop.initial_block {
        let Some(default) = game.pack.assets.registry.default_state(name) else { return Ok(true); };
        default
    } else {
        let Some(young) = game.with_props(state, &[("age", "0")]) else { return Ok(true); };
        young
    };
    // Reject unsupported ground before loot/RNG, inventory or world effects.
    if !game.border.contains(f64::from(pos[0]), f64::from(pos[2]))
        || crop.support_below.is_some_and(|support| &*game.res.facts().get(game.world.block(pos[0], pos[1] - 1, pos[2])).name != support)
        || !game.with_level(|b, level, ticks| b.can_survive(level, ticks, at, young))
    {
        return Ok(true);
    }
    let held = game.held().cloned();
    let mut loot = if game.ui.rules.bool("block_drops") {
        game.block_loot_at(pos, state, held.as_ref())
    } else {
        Vec::new()
    };
    let slots = (0..36).chain(std::iter::once(super::shield::OFFHAND_SLOT));
    let payment = core::select_payment(crop.planting_item, &loot, slots.filter_map(|slot| game.stack_in(slot).map(|s| (slot, s))));
    let after = if payment == core::Payment::None { BlockStateId(0) } else { young };
    // These crop plants have no block entity or pre-remove effects.
    // On this thread no other player can alter the target between check and write.
    let written = game.with_level(|b, level, ticks| {
        if let Some((upper_pos, upper_state)) = upper {
            let upper_at = BlockPos::new(upper_pos[0], upper_pos[1], upper_pos[2]);
            let quiet_remove = UPDATE_CLIENTS | UPDATE_KNOWN_SHAPE | UPDATE_SUPPRESS_DROPS;
            if !b.set_block(level, ticks, upper_at, BlockStateId(0), quiet_remove) { return false; }
            if b.set_block(level, ticks, at, after, UPDATE_ALL) { return true; }
            let _ = b.set_block(level, ticks, upper_at, upper_state, UPDATE_ALL);
            return false;
        }
        b.set_block(level, ticks, at, after, UPDATE_ALL)
    });
    if !written { return Ok(true); }
    match payment {
        core::Payment::Loot(index) => {
            loot[index].count -= 1;
        }
        core::Payment::Inventory(slot) => core::spend_one(game.stack_in_mut(slot), crop.planting_item),
        core::Payment::None => {}
    }
    for stack in loot {
        if stack.count > 0 && &*stack.item != "minecraft:air" {
            game.pop_resource(pos, stack);
        }
    }
    game.process_level_events()?;
    game.swing_arm();
    Ok(true)
}
