fn client_reacts(
    game: &crate::game::Game<'_>,
    hit: &crate::game::Hit,
) -> core::ops::ControlFlow<(bool, DryUse)> {
    if crate::game::right_click_crops_gameplay::client_takes(game, hit) {
        core::ops::ControlFlow::Break((true, Default::default()))
    } else {
        core::ops::ControlFlow::Continue(())
    }
}
