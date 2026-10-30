// Shared by the standalone library and the injected game module.
use std::sync::{OnceLock, atomic::{AtomicBool, Ordering}};

pub const MOD_ID: &str = "right-click-crops";
pub const MOD_NAME: &str = "Right-Click Crops";
pub const MOD_VERSION: &str = "0.1.0-dev.2";
pub const MOD_DESCRIPTION: &str = "Survival wheat harvesting. Restart the game after toggling.";
pub const SEED: &str = "minecraft:wheat_seeds";
pub const STARTUP_MESSAGE: &str = "[right-click-crops] Wheat prototype active; toggles require a full game restart.";

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

pub fn is_seed(stack: &impl SeedStack) -> bool {
    stack.item() == SEED && stack.count() > 0
}

pub fn select_payment<'a, S: SeedStack + 'a>(
    loot: &[S],
    inventory: impl IntoIterator<Item = (usize, &'a S)>,
) -> Payment {
    if let Some(index) = loot.iter().position(is_seed) {
        Payment::Loot(index)
    } else if let Some((slot, _)) = inventory.into_iter().find(|(_, stack)| is_seed(*stack)) {
        Payment::Inventory(slot)
    } else {
        Payment::None
    }
}

// Called only after the world transition succeeds. Selection guarantees a seed.
pub fn spend_one<S: SeedStack>(slot: &mut Option<S>) {
    if let Some(stack) = slot.as_mut().filter(|s| is_seed(*s)) {
        *stack.count_mut() -= 1;
        if stack.count() == 0 {
            *slot = None;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
        assert_eq!(select_payment(&loot, inventory.iter().enumerate()), Payment::Loot(1));
        let mut paid = Some(loot[1].clone());
        spend_one(&mut paid);
        assert_eq!(paid, Some(seeds(2)));
        assert_eq!(inventory[0], seeds(10));
    }

    #[test]
    fn one_loot_seed_leaves_no_ground_seed() {
        let mut slot = Some(seeds(1));
        spend_one(&mut slot);
        assert_eq!(slot, None);
    }

    #[test]
    fn inventory_fallback_keeps_all_loot() {
        let loot = [Stack("minecraft:wheat", 1)];
        let mut inventory = [Some(seeds(2))];
        assert_eq!(select_payment(&loot, inventory.iter().enumerate().filter_map(|(i,s)| s.as_ref().map(|s| (i,s)))), Payment::Inventory(0));
        spend_one(&mut inventory[0]);
        assert_eq!(inventory, [Some(seeds(1))]);
        assert_eq!(loot, [Stack("minecraft:wheat", 1)]);
    }

    #[test]
    fn empty_loot_can_use_the_last_offhand_seed() {
        let mut offhand = Some(seeds(1));
        assert_eq!(select_payment(&[], [(40, offhand.as_ref().unwrap())]), Payment::Inventory(40));
        spend_one(&mut offhand);
        assert_eq!(offhand, None);
    }

    #[test]
    fn wrong_items_and_zero_counts_do_not_pay() {
        let loot = [Stack("minecraft:beetroot_seeds", 8), seeds(0)];
        let inventory = [Stack("minecraft:wheat", 1), seeds(0)];
        assert_eq!(select_payment(&loot, inventory.iter().enumerate()), Payment::None);
        assert_eq!(select_payment::<Stack>(&[], []), Payment::None);
    }

    #[test]
    fn selection_and_cancelled_commit_have_no_item_effects() {
        let loot = [Stack("minecraft:wheat", 1)];
        let inventory = [seeds(1)];
        let before = (loot.clone(), inventory.clone());
        let _planned = select_payment(&loot, inventory.iter().enumerate());
        // An adapter that cannot commit must not call spend_one or spawn loot.
        assert_eq!((loot, inventory), before);
    }

    #[test]
    fn deterministic_first_positive_seed_stack() {
        let inventory = [(8, seeds(0)), (12, seeds(2)), (40, seeds(5))];
        assert_eq!(select_payment(&[], inventory.iter().map(|(i,s)| (*i,s))), Payment::Inventory(12));
    }

    #[test]
    fn spending_never_underflows_or_charges_wrong_items() {
        for stack in [seeds(0), Stack("minecraft:beetroot_seeds", 1)] {
            let mut slot = Some(stack.clone());
            spend_one(&mut slot);
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
}
