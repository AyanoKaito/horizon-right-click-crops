use super::{Game, Hit, right_click_crops as core};
use horizon_client::{command::args::GameMode, first_person::Hand, items::ItemStack};
use horizon_core::position::BlockPos;
use horizon_world::{level::flags::UPDATE_ALL, registry::BlockStateId};
use winit::keyboard::KeyCode;

impl core::SeedStack for ItemStack {
    fn item(&self) -> &str { &self.item }
    fn count(&self) -> u32 { self.count }
    fn count_mut(&mut self) -> &mut u32 { &mut self.count }
}

fn enabled(game: &Game<'_>) -> bool {
    core::enabled(game.native_on(core::MOD_ID))
}

fn target(game: &Game<'_>, hit: &Hit) -> Option<(BlockStateId, core::Crop)> {
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
    let state = game.world.block(hit.pos[0], hit.pos[1], hit.pos[2]);
    let crop = core::crop_profile(&game.res.facts().get(state).name)?;
    if game.pack.assets.registry.state(state)?.properties.get("age").map(String::as_str) == Some(crop.mature_age)
    {
        Some((state, crop))
    } else {
        None
    }
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
    let Some((state, crop)) = target(game, hit) else { return Ok(false); };
    let pos = hit.pos;
    let at = BlockPos::new(pos[0], pos[1], pos[2]);
    let Some(young) = game.with_props(state, &[("age", "0")]) else { return Ok(true); };
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
    // These six plants have no block entity or pre-remove effects.
    // On this thread no other player can alter the target between check and write.
    let written = game.with_level(|b, level, ticks| {
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
