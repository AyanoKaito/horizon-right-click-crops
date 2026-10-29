# Technical research references

This is a portable summary without local secrets, account details, or player data. Earlier detailed research remains outside the repository; development-relevant findings and sources are recorded here.

## Versions and sources

- Horizon targets Minecraft Java 26.3, but no Horizon revision has been selected for this native mod.
- Native guide: https://github.com/horizon-rust/horizon/blob/main/docs/native-mods.md . Read it at the selected pinned revision before building.
- Framework: https://github.com/horizon-rust/horizon-mixins .
- Template: https://github.com/horizon-rust/horizon-native-mod-template . Its initially inspected setup targeted Linux and older pinned revisions; do not assume Windows readiness.
- Historical research snapshots: `6d3489d30b8cd6220917943fde8d63624fd7a0de`, then `8993772de0bf4b0f92c9f76be64f7a1e6b21cf37`. These are not the selected compatibility targets for a release.

## Code map for further inspection

At snapshot `6d3489d30`:
- `crates/horizon-client/src/game.rs`: `use_item_as_player`, `use_hand`, `block_loot_at`, `pop_resource`, `break_block_as_player`.
- `crates/horizon-client/src/game/lan_actions.rs`: server-side `UseItemOn`, hand/guest context, and protection checks.
- `crates/horizon-world/src/level/tick.rs`: `crop_random_tick`, `crop_growth_speed`, `farmland_random_tick`.
- `crates/horizon-world/src/level/bonemeal.rs`: `crop_max_age`, `crop_state_for_age`, and crop-specific behavior.
- `crates/horizon-items/src/items.rs`: ordinary loot and enchantment modifiers.
- `crates/horizon-client/src/game/native_hooks.rs`: inspect current stable hook points before choosing to intercept an internal method directly.

Names and paths may have changed after refactoring. Inspect the selected source; do not invent API calls from this map. Inventory fallback also requires inspecting actual inventory access, item matching, and safe consumption before selecting an implementation.

## Native compatibility

A `.hnmod` may pin a commit or require a native-hook version. Mods compiled into one build must be mutually compatible; installing every latest version does not guarantee this.

The mechanic must run on the world-simulation side. A single-player launch does not prove correct LAN/dedicated behavior or server-only operation.

## Licensing and provenance

- Catalog policy: https://playhorizon.dev/mods/policy ; a port requires permission from the original license or written authorization, preserving attribution/notices and linking to the original.
- RightClickHarvest has an MIT LICENSE at `9ec801b799b4add3cdde30995ee45852c81f3a27`. It is a behavior reference; no gameplay code was ported.
- Harvest with ease uses the restrictive Crystal Nest Community License v1 at `ac76de6fd46bac09522f6dfc690ce62eb59a9eb4`; do not base a public port on it without suitable permission.
- The native template and horizon-mixins use MIT; retain notices when copying or adapting them.
- Moving from Java to Rust does not remove obligations for borrowed materials. An independently implemented gameplay idea is not automatically a port of a particular project.

Documentation and source interfaces were inspected. This mod has not been built; crop loot against actual game resources and the gameplay cycle have not been tested.
