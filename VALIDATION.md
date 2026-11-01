# Validation

This file records checks that were actually run. Compilation and structural checks are not presented as gameplay proof.

## Published 1.0.0 release

Target: Minecraft 26.3 on Horizon Nightly `2026-10-31` (`9d979ca`).

| Check | Result |
|---|---|
| Standalone Rust tests | Passed: 16 |
| Python structural and observation tests | Passed: 28 |
| horizon-mixins 0.6.0 plan/apply | Passed: 7 hooks, 2 modules |
| Generated-source AST preservation audit | Passed for `game.rs` and `game/native_hooks.rs` |
| Native Horizon build | Passed: approved isolated `cargo build --locked --offline --profile fast` |
| Single-player gameplay on the release pin | Passed: wheat payment and 8 interaction checks; 97 plant-group checks covering all 16 managed families and ordinary sweet/glow berries |
| LAN host and guest gameplay | Passed: 10 wheat cases (5 per actor), checked from both clients |
| Dedicated server | Not claimed: player-ready native installation is not provided by Horizon yet |
| `.hnmod` contents and SHA-256 | Passed: Horizon's official `native::Bundle::read` accepts `right_click_crops-1.0.0.hnmod` (11 files); reproducible build; SHA-256 published with the release |

The current code enters gameplay through `native_use_item_on` for held-item clicks and `native_right_click_block` for empty-main-hand clicks. A third hook, `native_use_item`, stops the second-hand item action from the same harvested click. The old owner-only `Game::use_hand` and client prediction hooks are no longer used.

The offhand regression uses a snowball as a measurable used item, not as a new mod feature: in survival, right-click mature wheat with an empty main hand and four snowballs in the off hand. The crop becomes `wheat[age=0]`; the snowball stack remains **4**. The first attempt exposed an unintended `4 -> 3` throw; the corrected candidate passed in single-player and separately for the LAN host and LAN guest. The LAN checks also covered empty-hand harvest, a held stick, bone meal in either hand, and matching crop states on both clients. Test fixtures used creative commands and disabled block drops; each harvest assertion ran in survival. This does not prove a no-cheats or non-operator LAN session.

## Follow-up: Nether vine loot

On the same `9d979ca` release build, `tools/test_nether_vine_loot.py` passed 32 isolated survival harvests: eight per vine/tool combination. Each fixture had three connected blocks; harvest retained one live anchor and removed two blocks. Creative commands prepared fixtures; block drops were enabled, random ticks were disabled, and both the action and assertions ran in survival. Neighbouring vines, inventory and the retained anchor were checked each time.

| Vine | Main hand | Harvests | Items from 16 removed blocks | Harvests with no drops |
|---|---|---|---|---|
| Twisting vines | Empty | 8 | 8 | 2 |
| Twisting vines | Shears | 8 | 16 | 0 |
| Weeping vines | Empty | 8 | 7 | 4 |
| Weeping vines | Shears | 8 | 16 | 0 |

The prepared resource loot tables for both vine heads and bodies specify a 0.33 chance without an applicable tool/enchantment, or guaranteed drops with shears/Silk Touch. Fortune I/II/III specify 0.55/0.77/1.0. This follow-up tested only empty hand and plain shears; enchantments were not retested. The small random sample is not a statistical verification of the table's probability. No gameplay code was changed.

## Earlier gameplay evidence

The previous development pin (`64e2989`) was tested in isolated single-player worlds. Those runs covered all sixteen managed plant families, ordinary sweet/glow berry preservation, settings UI and persistence, loot-funded and inventory-funded replanting, no-material harvest, held clicks, bone meal passthrough, save/reopen behaviour, removal/disable behaviour and selected ordinary-loot comparisons.

That evidence supported development; the release-pin checks above were run separately. Detailed historical reports remain available through Git history.

## Test rules

- Game runs use isolated homes and test worlds, never normal player saves.
- Creative mode, commands and bone meal may prepare fixtures; harvest assertions run in survival.
- Bone-meal growth is not reported as natural growth.
- A claim is marked passed only after the corresponding action was observed.
