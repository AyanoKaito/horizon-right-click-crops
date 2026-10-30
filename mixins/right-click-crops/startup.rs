fn startup(game: &crate::game::Game<'_>) {
    use crate::game::right_click_crops as runtime;

    if runtime::enabled(game.native_on(runtime::MOD_ID)) {
        runtime::report_startup_once();
    }
}
