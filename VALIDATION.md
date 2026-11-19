# Validation

This file records checks that were actually run. Compilation and structural checks are not presented as gameplay proof.

## Published 2.0.1 release (SDK f00125f)

Target: Minecraft 26.3, Horizon mod SDK `f00125f61f794aaa3d4e950d301f353b35b6ee3d` (mod API 0.2). Checked on 2026-11-19.

From Nightly `2026-11-19` (`f00125f`), WebAssembly mods link their game calls by name (horizon-rust/horizon#18357), and the game refuses mods built on older SDKs, including 2.0.0. Version 2.0.1 is the same source rebuilt on the new SDK; `cargo horizon-mod update` reported that none of the 233 items the mod uses changed. Game runs used Nightly `nightly-2026-11-19-f00125f` through the official `horizon-ctl`, set up as for 2.0.0.

| Check | Result |
|---|---|
| GitHub Actions on Ubuntu 24.04, commit `b901521` | Passed: `cargo-horizon-mod` built at the SDK commit, `cargo horizon-mod build --wasm`, 14 unit tests, `cargo horizon-mod check` |
| Package | `right_click_crops.hmod`, SHA-256 `ad0e2660dcd499b0e8bae1ee3570e58a557361611206d27643d0463f0cb3d892` (CI artifact, not a release) |
| Single-player plant groups | Passed: 97 checks (field crops 24, wart/cocoa 16, flower crops 14, vertical plants 13, kelp/vines 13, stem fruits 10, berries 7). In the first all-groups session, cactus did not regrow within the test's wait, and the leftover items then failed the melon setup check; both groups passed when rerun in their own sessions |
| Single-player wheat | Passed: 6 payment and loot slices and 8 interaction checks |
| Off-hand snowball | Passed: crop `wheat[age=0]`, snowballs stay at 4 |
| Settings | Passed: OFF on the Config page, OFF survives a restart, ON again without a restart |
| Installed package | Passed: player install path loads (`wasm mods loaded (1)`) and harvests |
| LAN host and guest gameplay | Passed: 10 wheat cases, crop states matching on both clients |
| Dedicated server | Not claimed |

This Nightly refuses to start a launcher-managed installation directly until the launcher's Play has registered its cache folders. The test runs used a copy of the installed version outside the launcher data folder. No mod errors appeared in the game logs. The release package `right_click_crops-2.0.1.hmod` comes from CI run 44577647751 on commit `7e8c72d` (SHA-256 `e6b741f6d45f0d498eaf8fddbef5a517955befbedacca0093a4a5b3e64d8b1a1`). Its `mod.wasm` is byte-identical to the tested one (same `[wasm] sha512`); only packed documentation changed. It passed the installed-package run again. The author's Minisign signature verifies with the project key.

## Published 2.0.0 release (WebAssembly)

Target: Minecraft 26.3, Horizon mod SDK `0b14f8acfd97fa2c750e42795249dcc981178ca4` (mod API 0.2). Checked on 2026-11-19.

Version 2 is a rewrite for the mod SDK. The 1.x evidence below was gathered on native builds and does not cover it. Game runs used Horizon Nightly `nightly-2026-11-18-0b14f8a` (the SDK commit) through the official `horizon-ctl`, with 26.3 resources prepared from a local Minecraft install, isolated homes and new test worlds (seed 42, Horizon test terrain).

| Check | Result |
|---|---|
| `cargo check` on Windows (Rust 1.99.1) | Passed, no warnings |
| GitHub Actions on Ubuntu 24.04, commit `365f55a` | Passed: `cargo-horizon-mod` built at the SDK commit, `cargo horizon-mod build --wasm`, 14 unit tests, `cargo horizon-mod check` (the registry's checks) |
| Package | `right_click_crops.hmod`, SHA-256 `7b294f74e738f234dfe13799474830d678f777345b4e5bc0281d99c1ba48652e` (CI artifact, not a release) |
| Single-player plant groups | Passed: 97 checks across all 16 managed families and ordinary sweet/glow berries (field crops 24, wart/cocoa 16, flower crops 14, vertical plants 13, kelp/vines 13, stem fruits 10, berries 7), all in one session |
| Single-player wheat | Passed: 6 payment and loot slices and 8 interaction checks (off-hand payment, bone meal in either hand, two hands harvest once, held right-click on successive targets without area harvest, ordinary breaking and planting) |
| Off-hand snowball | Passed: empty main hand, four snowballs in the off hand; crop `wheat[age=0]`, snowballs stay at 4 |
| Settings | Passed: wheat toggled OFF on the Config page leaves mature wheat and drops nothing; OFF survives a restart (stored as `wheat` = `false`); ON again harvests and replants without a restart |
| Installed package | Passed: the `.hmod` copied into `horizon-mods/` with `mod.right_click_crops:true` loads (`wasm mods loaded (1)`) and harvests |
| LAN host and guest gameplay | Passed: 10 wheat cases (5 per actor: empty hand, held stick, bone meal in either hand, off-hand snowball), crop states matching on both clients |
| Dedicated server | Not claimed |

The plant, wheat, snowball and settings runs loaded the package with `--dev-mod`; the installed-package run used the player install path. Fixtures were prepared with creative commands; every harvest assertion ran in survival. LAN fixtures used an operator-enabled LAN world, so this does not prove a no-cheats LAN session. No mod errors appeared in the game logs. The release package `right_click_crops-2.0.0.hmod` comes from CI run 44427597179 on commit `433f4de` (SHA-256 `c7cb17b53d017fb12f5bfa951e78a17ba574d911ddb10676388978a0618dc16e`). Its `mod.wasm` is byte-identical to the tested one (same `[wasm] sha512`); only packed documentation changed. It passed the installed-package run again. The author's Minisign signature verifies with the project key.

## Published 1.0.1 release

Target: Minecraft 26.3 on Horizon Nightly `2026-11-05` (`66f3981`, native hooks API 411). Checked on 2026-11-07.

Horizon `66f3981` added a block-entity argument to the internal block loot helper, which broke compilation of `1.0.0` (`E0061`). The patch passes no block entity: the managed plants have none. No other gameplay code changed.

| Check | Result |
|---|---|
| Standalone Rust tests | Passed: 16 |
| Python structural and observation tests | Passed: 28 |
| horizon-mixins 0.6.0 plan/apply (`4342a0b`) | Passed: 7 hooks, 2 modules |
| Generated-source AST preservation audit | `native_hooks.rs` passed. In `game.rs`, both bundle modules match the bundle source; the remaining tree differs from pristine source only in `unstuck_orb`, where the transformer's reprint wraps one upstream closure body in braces (`|s| s.moved(..)` became `|s| { s.moved(..) }`). Semantics are unchanged; the audit tool reports this file as not preserved. |
| Native Horizon build | Passed: approved isolated build matching the launcher's Dev build (`cargo build --locked --offline --profile fast --config profile.fast.package.horizon-client.opt-level=0 -p horizon-client --bin horizon-client`). Horizon `66f3981` no longer has the `horizon-client/mods` feature, so it was not passed. |
| Single-player wheat | Passed: 6 payment and loot slices, 8 interaction checks, and the offhand snowball regression (crop `wheat[age=0]`, snowballs stay at 4) |
| Single-player plant groups | Passed: 97 checks across all 16 managed families and ordinary sweet/glow berries (field crops 24, wart/cocoa 16, flower crops 14, vertical plants 13, kelp/vines 13, stem fruits 10, berries 7) |
| LAN host and guest gameplay | Passed: 10 wheat cases (5 per actor) |
| Dedicated server | Not claimed |

Game runs used the official `horizon-ctl` and prepared 26.3 resources of the installed `66f3981` Nightly read-only, with isolated homes and test worlds.

Harness notes: in three full plant-sequence sessions, three checks failed for reasons outside the mod, and each was rerun.

- `melon-linked: clean inventory and ground` (once): two `twisting_vines` items from the preceding vine test landed during fixture setup, before any click.
- `pitcher: repeat` (twice): the first harvest's `pitcher_plant` item rolled to within pickup range of the test player (x 1.25 and 1.65; player at x 0.5) and was picked up before the repeat assertion compared ground and inventory. Both times the crop stayed `pitcher_crop[age=0,half=lower]` and no pod was charged.

The stem-fruit script then passed alone, and the flower-crop script passed alone twice. The 97-check total combines a full session in which the other six scripts passed with those standalone flower-crop passes.

`tools/package.py` produced `right_click_crops-1.0.1.hnmod` (11 files, the same entry names as `1.0.0`) with SHA-256 `e369d9cb34320144d805d02f162a3ed357b9cf8bbeee457e409cedc0b7e63d0a`. A second build was byte-identical. Its bundle sources are byte-identical to the sources validated above. The manifest was checked against the field rules of Horizon `66f3981`'s native `Manifest`. Horizon's own bundle reader was not run for this candidate. The author's Minisign signature verifies against `right-click-crops.pub`.

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

## Registry preparation: newest Nightly compilation check

The newest Nightly source tag checked on 2026-11-01 was `nightly-source/2026-10-31-d91cab6`, commit `d91cab68ded29bd2b004f7050c468fb98c41a00b` (native hooks API 42).

In an isolated copy of the release bundle, only `compatibility.horizon_revision` was changed to that commit. All other bundle files were byte-identical to the release sources. With the release-pinned horizon-mixins revision:

- Apply passed: seven hooks, two modules.
- AST preservation audit passed for `game.rs` and `game/native_hooks.rs`.
- `cargo check --locked --offline -p horizon-client --bin horizon-client` passed using Rust 1.99.1 on `x86_64-pc-windows-gnu`.

The first compilation command timed out before completion; the cached retry finished successfully. This is a compilation check, not a linked executable build or gameplay validation on `d91cab6`. No gameplay changes were required. The published `1.0.0` bundle, SHA-256 and exact `9d979ca` installation pin remain unchanged; this experiment does not broaden their compatibility contract.

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
