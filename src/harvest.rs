//! The harvest itself: which click is a harvest, and the world and inventory changes it makes.
//!
//! The client and the server run the same `target` choice. Only the server changes anything:
//! it rolls the block's own loot, writes the blocks, pays for replanting and drops the rest.

use crate::core::{self, Crop, Payment, Plant, SeedStack};
use mod_api::{
    BlockClick, BlockState, BlockUpdateFlags, ClientHost, EntityRef, EquipmentSlot, GameMode,
    GameRuleValue, Hand, Host, HostBlockStates, ItemStack, LevelRef, PlayerRef, ServerHost,
    SettingSpec, SettingValue,
};

/// The on/off setting for one plant family, enabled by default.
pub fn setting(plant: Plant) -> SettingSpec {
    SettingSpec::toggle(plant.key(), plant.label_key(), true)
}

fn plant_enabled(host: &dyn Host, plant: Plant) -> bool {
    let stored = host.setting(core::MOD_ID, plant.key());
    !matches!(setting(plant).read(stored.as_deref()), SettingValue::Toggle(false))
}

struct CropTarget {
    pos: [i32; 3],
    state: BlockState,
    name: String,
    crop: Crop,
    upper: Option<([i32; 3], BlockState)>,
}

enum Target {
    Crop(CropTarget),
    Column(Vec<([i32; 3], BlockState)>),
    Fruit([i32; 3]),
}

/// Reads of one level through a host of either side.
struct World<'a> {
    host: &'a dyn Host,
    level: LevelRef,
}

impl World<'_> {
    fn state(&self, pos: [i32; 3]) -> Option<BlockState> {
        self.level.block_state(self.host, pos)
    }

    fn name(&self, pos: [i32; 3]) -> Option<String> {
        self.state(pos).map(|state| state.block().id(self.host))
    }

    fn property(&self, pos: [i32; 3], property: &str) -> Option<String> {
        self.level.block_property(self.host, pos, property)
    }
}

fn holds(host: &dyn Host, stack: Option<&ItemStack>, item: &str) -> bool {
    stack.is_some_and(|stack| stack.count() > 0 && stack.item().id(host) == item)
}

/// The plant this click harvests, or None to leave the click to the game.
fn target(host: &dyn Host, player: PlayerRef, level: LevelRef, click: &BlockClick<'_>) -> Option<Target> {
    if player.game_mode(host) != Some(GameMode::Survival) {
        return None;
    }
    let main = click.stack;
    let off = host
        .living(player.entity())
        .and_then(|living| living.equipment(host, EquipmentSlot::OffHand));
    let off = off.as_ref().filter(|stack| stack.count() > 0);
    // Bone meal always stays an ordinary game interaction.
    if holds(host, main, "minecraft:bone_meal") || holds(host, off, "minecraft:bone_meal") {
        return None;
    }
    // Sneaking with something in either hand keeps the game's own use (placing, for example).
    let sneaking = player.entity().is_shift_key_down(host) == Some(true);
    if sneaking && (main.is_some() || off.is_some()) {
        return None;
    }

    let world = World { host, level };
    let hit = click.pos;
    let clicked = world.state(hit)?;
    let clicked_name = clicked.block().id(host);
    let plant = Plant::from_block(&clicked_name)?;
    if !plant_enabled(host, plant) {
        return None;
    }

    if let Some(profile) = core::vertical_profile(&clicked_name) {
        // Keep the connected base: harvest everything above (or, for weeping vines, below) it.
        let mut anchor_y = hit[1];
        for _ in 0..32 {
            let support_y = anchor_y - profile.growth_y;
            let Some(name) = world.name([hit[0], support_y, hit[2]]) else { break };
            if !core::same_vertical_plant(&name, profile) {
                break;
            }
            anchor_y = support_y;
        }
        let mut blocks = Vec::new();
        for distance in 1..=32 {
            let pos = [hit[0], anchor_y + profile.growth_y * distance, hit[2]];
            let Some(state) = world.state(pos) else { break };
            if !core::same_vertical_plant(&state.block().id(host), profile) {
                break;
            }
            blocks.push((pos, state));
        }
        return (!blocks.is_empty()).then_some(Target::Column(blocks));
    }

    if let Some(fruit) = core::stem_fruit_profile(&clicked_name) {
        // Shears on a pumpkin carve it.
        let shears = |stack: Option<&ItemStack>| holds(host, stack, "minecraft:shears");
        if fruit.fruit == "minecraft:pumpkin" && (shears(main) || shears(off)) {
            return None;
        }
        // Only a fruit an attached stem points at; a placed pumpkin or melon block is decoration.
        for (dx, dz, facing) in [(-1, 0, "east"), (1, 0, "west"), (0, -1, "south"), (0, 1, "north")] {
            let stem = [hit[0] + dx, hit[1], hit[2] + dz];
            if world.name(stem).as_deref() == Some(fruit.attached_stem)
                && world.property(stem, "facing").as_deref() == Some(facing)
            {
                return Some(Target::Fruit(hit));
            }
        }
        return None;
    }

    // A pitcher crop is harvested from its lower half.
    let mut pos = hit;
    if clicked_name == "minecraft:pitcher_crop" && world.property(pos, "half").as_deref() == Some("upper") {
        pos[1] -= 1;
    }
    let state = world.state(pos)?;
    let name = state.block().id(host);
    let crop = core::crop_profile(&name)?;
    if crop.mature_age.is_some_and(|age| world.property(pos, "age").as_deref() != Some(age)) {
        return None;
    }
    let upper = if crop.two_blocks {
        if world.property(pos, "half").as_deref() != Some("lower") {
            return None;
        }
        let upper_pos = [pos[0], pos[1] + 1, pos[2]];
        let upper_state = world.state(upper_pos)?;
        if upper_state.block().id(host) != "minecraft:pitcher_crop"
            || world.property(upper_pos, "age").as_deref() != crop.mature_age
            || world.property(upper_pos, "half").as_deref() != Some("upper")
        {
            return None;
        }
        Some((upper_pos, upper_state))
    } else {
        None
    };
    Some(Target::Crop(CropTarget { pos, state, name, crop, upper }))
}

/// The client's side of a click: true when the server will treat it as a harvest, so the client
/// stops here as well instead of trying the item or the other hand.
pub fn on_client(host: &mut dyn ClientHost, click: &BlockClick<'_>) -> bool {
    let host: &dyn Host = host;
    if click.hand != Hand::Main {
        return false;
    }
    let Some(player) = host.player(click.player) else { return false };
    let Some(level) = player.level(host) else { return false };
    target(host, player, level, click).is_some()
}

/// The server's side of a click: harvest, and answer whether the click was used.
pub fn on_server(host: &mut dyn ServerHost, click: &BlockClick<'_>) -> bool {
    if click.hand != Hand::Main {
        return false;
    }
    let read: &dyn Host = host;
    let Some(player) = read.player(click.player) else { return false };
    let Some(level) = player.level(read) else { return false };
    let Some(target) = target(read, player, level, click) else { return false };
    let tool = click.stack.cloned();
    let breaker = Some(player.entity());
    match target {
        Target::Column(blocks) => harvest_column(host, level, tool.as_ref(), breaker, click.pos, &blocks),
        Target::Fruit(pos) => harvest_fruit(host, level, tool.as_ref(), breaker, pos),
        Target::Crop(crop) => harvest_crop(host, level, player, tool.as_ref(), breaker, crop),
    }
    // The click is used even when an ordinary failure left everything unchanged.
    true
}

fn drops_enabled(host: &dyn Host, level: LevelRef) -> bool {
    !matches!(level.game_rule(host, "block_drops"), Ok(Some(GameRuleValue::Bool(false))))
}

/// The block's own loot with the held tool, as breaking it would roll it; empty with drops off.
fn loot(
    host: &mut dyn ServerHost,
    level: LevelRef,
    pos: [i32; 3],
    tool: Option<&ItemStack>,
    breaker: Option<EntityRef>,
) -> Vec<ItemStack> {
    if !drops_enabled(host, level) {
        return Vec::new();
    }
    match level.block_drops(host, pos, tool, breaker) {
        Ok(Some(stacks)) => stacks,
        Ok(None) => Vec::new(),
        Err(error) => {
            log(&format!("loot at {pos:?} failed: {error:?}"));
            Vec::new()
        }
    }
}

fn drop_all(host: &mut dyn ServerHost, level: LevelRef, pos: [i32; 3], stacks: Vec<ItemStack>) {
    for stack in stacks.into_iter().filter(|stack| stack.count() > 0) {
        if let Err(error) = level.pop_resource(host, pos, stack) {
            log(&format!("drop at {pos:?} failed: {error:?}"));
        }
    }
}

fn air(host: &dyn Host) -> Option<BlockState> {
    host.block_state_id("minecraft:air")
}

fn write(host: &mut dyn ServerHost, level: LevelRef, pos: [i32; 3], state: BlockState, flags: BlockUpdateFlags) -> bool {
    matches!(level.set_block(host, pos, state, flags), Ok(true))
}

fn update_all() -> BlockUpdateFlags {
    BlockUpdateFlags::NEIGHBORS | BlockUpdateFlags::CLIENTS
}

/// Sugar cane, cactus, bamboo, kelp and the nether vines: everything past the base goes.
fn harvest_column(
    host: &mut dyn ServerHost,
    level: LevelRef,
    tool: Option<&ItemStack>,
    breaker: Option<EntityRef>,
    hit: [i32; 3],
    blocks: &[([i32; 3], BlockState)],
) {
    let Some(air) = air(host) else { return };
    let mut stacks = Vec::new();
    for (pos, _) in blocks {
        stacks.extend(loot(host, level, *pos, tool, breaker));
    }
    // From the far end back to the base, so no block is left floating mid-way.
    let mut removed: Vec<([i32; 3], BlockState)> = Vec::new();
    for (pos, state) in blocks.iter().rev() {
        if !write(host, level, *pos, air, update_all() | BlockUpdateFlags::SUPPRESS_DROPS) {
            for (pos, state) in removed.iter().rev() {
                write(host, level, *pos, *state, update_all());
            }
            return;
        }
        removed.push((*pos, *state));
    }
    drop_all(host, level, hit, stacks);
}

/// A pumpkin or melon beside its attached stem; the stem stays.
fn harvest_fruit(host: &mut dyn ServerHost, level: LevelRef, tool: Option<&ItemStack>, breaker: Option<EntityRef>, pos: [i32; 3]) {
    let Some(air) = air(host) else { return };
    let stacks = loot(host, level, pos, tool, breaker);
    if write(host, level, pos, air, update_all() | BlockUpdateFlags::SUPPRESS_DROPS) {
        drop_all(host, level, pos, stacks);
    }
}

/// A seen stack, by item id, for choosing what pays for replanting.
struct Seen {
    item: String,
    count: u32,
}

impl SeedStack for Seen {
    fn item(&self) -> &str {
        &self.item
    }
    fn count(&self) -> u32 {
        self.count
    }
    fn count_mut(&mut self) -> &mut u32 {
        &mut self.count
    }
}

fn seen(host: &dyn Host, stack: &ItemStack) -> Seen {
    Seen { item: stack.item().id(host), count: stack.count() }
}

/// The main inventory (0 to 35) and the off hand (40), in that order.
const OFF_HAND_SLOT: u32 = 40;

/// Field crops, nether wart, cocoa, torchflower and pitcher crop: harvest and replant at age 0.
fn harvest_crop(
    host: &mut dyn ServerHost,
    level: LevelRef,
    player: PlayerRef,
    tool: Option<&ItemStack>,
    breaker: Option<EntityRef>,
    target: CropTarget,
) {
    let CropTarget { pos, state, name, crop, upper } = target;
    let young = {
        let read: &dyn Host = host;
        match crop.initial_block {
            Some(initial) => read.block_state_id(initial),
            None => state.with(&read.block_states(), "age", "0").ok(),
        }
    };
    let Some(young) = young else {
        log(&format!("no young state for {name}"));
        return;
    };
    // Reject unsupported ground before loot, inventory or world effects. The young plant has the
    // same survival rule as the mature one already standing here, so its support is what counts.
    {
        let read: &dyn Host = host;
        let world = World { host: read, level };
        let inside = level.world_border(read).is_none_or(|[min_x, min_z, max_x, max_z]| {
            let (x, z) = (f64::from(pos[0]), f64::from(pos[2]));
            x >= min_x && x < max_x && z >= min_z && z < max_z
        });
        let supported = crop
            .support_below
            .is_none_or(|support| world.name([pos[0], pos[1] - 1, pos[2]]).as_deref() == Some(support));
        if !inside || !supported {
            return;
        }
    }
    let Some(air) = air(host) else { return };
    let mut stacks = loot(host, level, pos, tool, breaker);

    let (loot_seen, slots) = {
        let read: &dyn Host = host;
        let loot_seen: Vec<Seen> = stacks.iter().map(|stack| seen(read, stack)).collect();
        let slots: Vec<(u32, ItemStack)> = player
            .inventory_slots(read)
            .unwrap_or_default()
            .into_iter()
            .filter(|(slot, _)| *slot < 36 || *slot == OFF_HAND_SLOT)
            .collect();
        (loot_seen, slots)
    };
    let inventory_seen: Vec<(usize, Seen)> = {
        let read: &dyn Host = host;
        slots.iter().map(|(slot, stack)| (*slot as usize, seen(read, stack))).collect()
    };
    let payment = core::select_payment(
        crop.planting_item,
        &loot_seen,
        inventory_seen.iter().map(|(slot, stack)| (*slot, stack)),
    );

    // Charge the inventory first, so a failed charge never replants for free; a failed world
    // write below gives the item back.
    let mut charged: Option<(u32, ItemStack)> = None;
    if let Payment::Inventory(slot) = payment {
        let slot = slot as u32;
        let Some((_, original)) = slots.iter().find(|(s, _)| *s == slot) else { return };
        let left = original.clone().shrink(1);
        if let Err(error) = player.set_inventory_slot(host, slot, left) {
            log(&format!("paying from slot {slot} failed: {error:?}"));
            return;
        }
        charged = Some((slot, original.clone()));
    }

    let after = if payment == Payment::None { air } else { young };
    let written = match upper {
        Some((upper_pos, upper_state)) => {
            let quiet = BlockUpdateFlags::CLIENTS | BlockUpdateFlags::KNOWN_SHAPE | BlockUpdateFlags::SUPPRESS_DROPS;
            if !write(host, level, upper_pos, air, quiet) {
                false
            } else if write(host, level, pos, after, update_all()) {
                true
            } else {
                write(host, level, upper_pos, upper_state, update_all());
                false
            }
        }
        None => write(host, level, pos, after, update_all()),
    };
    if !written {
        if let Some((slot, original)) = charged {
            if let Err(error) = player.set_inventory_slot(host, slot, Some(original)) {
                log(&format!("refund to slot {slot} failed: {error:?}"));
            }
        }
        return;
    }

    if let Payment::Loot(index) = payment {
        let paid = stacks.remove(index);
        if let Some(left) = paid.shrink(1) {
            stacks.insert(index, left);
        }
    }
    drop_all(host, level, pos, stacks);
}

fn log(message: &str) {
    eprintln!("[{}] Harvest failed: {message}", core::MOD_ID);
}
