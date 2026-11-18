//! Right-Click Crops: a right click harvests a mature supported plant and replants it.
//!
//! One hook does the work: `right_click_block`, which the game asks on the clicking client and on
//! the server. The server harvests; the client makes the same choice from what it can see, so it
//! does not go on to use the off-hand item for the same click.

mod core;
mod harvest;

use mod_api::{
    self, Flow, Hooks, HostSide, InteractionResult, Registrar, RegistrationContext,
    RightClickBlockEvent,
};

#[derive(Default)]
struct Mod;

#[mod_api::horizon_mod]
impl Hooks for Mod {
    /// One on/off setting per plant family, on the mod's page in Options > Mods.
    fn register(&self, registrar: &mut dyn Registrar, _: &RegistrationContext) {
        for plant in core::Plant::ALL {
            if let Err(error) = registrar.register_setting(harvest::setting(plant)) {
                eprintln!("[{}] Setting {} not registered: {error:?}", core::MOD_ID, plant.key());
            }
        }
    }

    fn right_click_block(&self, host: HostSide<'_>, event: &mut RightClickBlockEvent<'_>) -> Flow {
        let click = *event.click;
        let handled = match host {
            HostSide::Server(host) => harvest::on_server(host, &click),
            HostSide::Client(host) => harvest::on_client(host, &click),
        };
        if handled {
            // A consuming result ends the click: no block use, no item use, no off-hand try.
            *event.cancellation_result = InteractionResult::Success;
            Flow::Cancel
        } else {
            Flow::Continue
        }
    }
}
