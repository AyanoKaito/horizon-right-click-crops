// Shared by the standalone library and the injected game module.
use std::sync::{OnceLock, atomic::{AtomicBool, Ordering}};

pub const MOD_ID: &str = "right-click-crops";
pub const MOD_NAME: &str = "Right-Click Crops";
pub const MOD_VERSION: &str = "0.1.0-dev.4";
pub const MOD_DESCRIPTION: &str = "Survival field crops, nether wart and cocoa. Restart after toggling.";
pub const STARTUP_MESSAGE: &str = "[right-click-crops] Six crops active; toggles require a full game restart.";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Crop {
    pub mature_age: &'static str,
    pub planting_item: &'static str,
    // Cocoa uses the game's direction-sensitive survival check instead.
    pub support_below: Option<&'static str>,
}

// Explicit profiles, not every block with an age property.
pub fn crop_profile(block: &str) -> Option<Crop> {
    let (mature_age, planting_item, support_below) = match block {
        "minecraft:wheat" => ("7", "minecraft:wheat_seeds", Some("minecraft:farmland")),
        "minecraft:carrots" => ("7", "minecraft:carrot", Some("minecraft:farmland")),
        "minecraft:potatoes" => ("7", "minecraft:potato", Some("minecraft:farmland")),
        "minecraft:beetroots" => ("3", "minecraft:beetroot_seeds", Some("minecraft:farmland")),
        "minecraft:nether_wart" => ("3", "minecraft:nether_wart", Some("minecraft:soul_sand")),
        "minecraft:cocoa" => ("2", "minecraft:cocoa_beans", None),
        _ => return None,
    };
    Some(Crop { mature_age, planting_item, support_below })
}

static ENABLED: OnceLock<bool> = OnceLock::new();
static STARTUP_REPORTED: AtomicBool = AtomicBool::new(false);

pub fn enabled(requested: bool) -> bool {
    *ENABLED.get_or_init(|| requested)
}

pub fn report_startup_once() {
    if !STARTUP_REPORTED.swap(true, Ordering::Relaxed) {
        eprintln!("{STARTUP_MESSAGE}");
    }
}

pub trait SeedStack {
    fn item(&self) -> &str;
    fn count(&self) -> u32;
    fn count_mut(&mut self) -> &mut u32;
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Payment {
    Loot(usize),
    Inventory(usize),
    None,
}

pub fn is_seed(stack: &impl SeedStack, planting_item: &str) -> bool {
    stack.item() == planting_item && stack.count() > 0
}

pub fn select_payment<'a, S: SeedStack + 'a>(
    planting_item: &str,
    loot: &[S],
    inventory: impl IntoIterator<Item = (usize, &'a S)>,
) -> Payment {
    if let Some(index) = loot.iter().position(|s| is_seed(s, planting_item)) {
        Payment::Loot(index)
    } else if let Some((slot, _)) = inventory.into_iter().find(|(_, stack)| is_seed(*stack, planting_item)) {
        Payment::Inventory(slot)
    } else {
        Payment::None
    }
}

// Called only after the world transition succeeds. Selection guarantees a seed.
pub fn spend_one<S: SeedStack>(slot: &mut Option<S>, planting_item: &str) {
    if let Some(stack) = slot.as_mut().filter(|s| is_seed(*s, planting_item)) {
        *stack.count_mut() -= 1;
        if stack.count() == 0 {
            *slot = None;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const SEED: &str = "minecraft:wheat_seeds";

    #[derive(Clone, Debug, PartialEq)]
    struct Stack(&'static str, u32);
    impl SeedStack for Stack {
        fn item(&self) -> &str { self.0 }
        fn count(&self) -> u32 { self.1 }
        fn count_mut(&mut self) -> &mut u32 { &mut self.1 }
    }

    fn seeds(count: u32) -> Stack { Stack(SEED, count) }

    #[test]
    fn loot_precedes_inventory_and_charges_exactly_one() {
        let loot = vec![Stack("minecraft:wheat", 1), seeds(3), seeds(2)];
        let inventory = [seeds(10)];
        assert_eq!(select_payment(SEED, &loot, inventory.iter().enumerate()), Payment::Loot(1));
        let mut paid = Some(loot[1].clone());
        spend_one(&mut paid, SEED);
        assert_eq!(paid, Some(seeds(2)));
        assert_eq!(inventory[0], seeds(10));
    }

    #[test]
    fn one_loot_seed_leaves_no_ground_seed() {
        let mut slot = Some(seeds(1));
        spend_one(&mut slot, SEED);
        assert_eq!(slot, None);
    }

    #[test]
    fn inventory_fallback_keeps_all_loot() {
        let loot = [Stack("minecraft:wheat", 1)];
        let mut inventory = [Some(seeds(2))];
        assert_eq!(select_payment(SEED, &loot, inventory.iter().enumerate().filter_map(|(i,s)| s.as_ref().map(|s| (i,s)))), Payment::Inventory(0));
        spend_one(&mut inventory[0], SEED);
        assert_eq!(inventory, [Some(seeds(1))]);
        assert_eq!(loot, [Stack("minecraft:wheat", 1)]);
    }

    #[test]
    fn empty_loot_can_use_the_last_offhand_seed() {
        let mut offhand = Some(seeds(1));
        assert_eq!(select_payment(SEED, &[], [(40, offhand.as_ref().unwrap())]), Payment::Inventory(40));
        spend_one(&mut offhand, SEED);
        assert_eq!(offhand, None);
    }

    #[test]
    fn wrong_items_and_zero_counts_do_not_pay() {
        let loot = [Stack("minecraft:beetroot_seeds", 8), seeds(0)];
        let inventory = [Stack("minecraft:wheat", 1), seeds(0)];
        assert_eq!(select_payment(SEED, &loot, inventory.iter().enumerate()), Payment::None);
        assert_eq!(select_payment::<Stack>(SEED, &[], []), Payment::None);
    }

    #[test]
    fn selection_and_cancelled_commit_have_no_item_effects() {
        let loot = [Stack("minecraft:wheat", 1)];
        let inventory = [seeds(1)];
        let before = (loot.clone(), inventory.clone());
        let _planned = select_payment(SEED, &loot, inventory.iter().enumerate());
        // An adapter that cannot commit must not call spend_one or spawn loot.
        assert_eq!((loot, inventory), before);
    }

    #[test]
    fn deterministic_first_positive_seed_stack() {
        let inventory = [(8, seeds(0)), (12, seeds(2)), (40, seeds(5))];
        assert_eq!(select_payment(SEED, &[], inventory.iter().map(|(i,s)| (*i,s))), Payment::Inventory(12));
    }

    #[test]
    fn spending_never_underflows_or_charges_wrong_items() {
        for stack in [seeds(0), Stack("minecraft:beetroot_seeds", 1)] {
            let mut slot = Some(stack.clone());
            spend_one(&mut slot, SEED);
            assert_eq!(slot, Some(stack));
        }
    }

    #[test]
    fn enablement_latch_keeps_both_sides_consistent_until_restart() {
        for first in [false, true] {
            let setting = OnceLock::new();
            assert_eq!(*setting.get_or_init(|| first), first);
            assert_eq!(*setting.get_or_init(|| !first), first);
        }
    }

    #[test]
    fn field_profiles_have_exact_maturity_and_planting_items() {
        for (block, age, item, support) in [
            ("minecraft:wheat", "7", SEED, Some("minecraft:farmland")),
            ("minecraft:carrots", "7", "minecraft:carrot", Some("minecraft:farmland")),
            ("minecraft:potatoes", "7", "minecraft:potato", Some("minecraft:farmland")),
            ("minecraft:beetroots", "3", "minecraft:beetroot_seeds", Some("minecraft:farmland")),
            ("minecraft:nether_wart", "3", "minecraft:nether_wart", Some("minecraft:soul_sand")),
            ("minecraft:cocoa", "2", "minecraft:cocoa_beans", None),
        ] {
            assert_eq!(crop_profile(block), Some(Crop { mature_age: age, planting_item: item, support_below: support }));
        }
        for block in ["minecraft:torchflower", "minecraft:sweet_berry_bush", "minecraft:air"] {
            assert_eq!(crop_profile(block), None);
        }
    }

    #[test]
    fn every_profile_pays_only_its_own_item_and_prefers_loot() {
        let items = [SEED, "minecraft:carrot", "minecraft:potato", "minecraft:beetroot_seeds", "minecraft:nether_wart", "minecraft:cocoa_beans"];
        for item in items {
            let loot = [Stack(item, 2)];
            let inventory = [Stack(item, 4)];
            assert_eq!(select_payment(item, &loot, inventory.iter().enumerate()), Payment::Loot(0));
            assert_eq!(select_payment(item, &[], inventory.iter().enumerate()), Payment::Inventory(0));
            let mut last = Some(Stack(item, 1));
            spend_one(&mut last, item);
            assert_eq!(last, None);
            for wrong in items.into_iter().chain(["minecraft:poisonous_potato", "minecraft:beetroot"]) {
                if wrong == item { continue; }
                let wrong_loot = [Stack(wrong, 3), Stack(item, 0)];
                assert_eq!(select_payment(item, &wrong_loot, [(40, &wrong_loot[0])]), Payment::None);
                let mut slot = Some(Stack(wrong, 3));
                spend_one(&mut slot, item);
                assert_eq!(slot, Some(Stack(wrong, 3)));
            }
        }
    }
}
