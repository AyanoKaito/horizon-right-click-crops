fn use_hand(
    game: &mut crate::game::Game<'_>,
    block_hit: Option<&crate::game::Hit>,
) -> core::ops::ControlFlow<Result<bool>> {
    match crate::game::right_click_crops_gameplay::harvest(game, block_hit) {
        Ok(false) => core::ops::ControlFlow::Continue(()),
        result => core::ops::ControlFlow::Break(result),
    }
}
