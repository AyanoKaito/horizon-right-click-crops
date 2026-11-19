# Development

Right-Click Crops is a Horizon mod SDK project (`horizon-mod.toml`, `Cargo.toml`, `src/`) built to `mod.wasm` and packed as a `.hmod`.

## Pins

- Horizon mod SDK: `f00125f61f794aaa3d4e950d301f353b35b6ee3d` (`[package.metadata.horizon] sdk` in `Cargo.toml`), mod API 0.2
- Rust used by Horizon: 1.99.1

## Build

The release package is built by `.github/workflows/build.yml` on Ubuntu: SDK `0b14f8a` refused WebAssembly built on Windows, so the build stays on Linux. The workflow builds `cargo-horizon-mod` from the Horizon repository at the SDK commit, then runs:

```sh
cargo horizon-mod build --wasm
cargo test
cargo horizon-mod check target/horizon-mod/right_click_crops.hmod
```

It uploads the `.hmod` as the `right_click_crops-hmod` artifact and writes its SHA-256 to the run summary. `cargo horizon-mod` places the SDK under ignored `.horizon/` and writes `mod.wasm` and the `[wasm]` table itself; do not edit `[wasm]` by hand.

On any platform, `cargo test` runs the unit tests in `src/core.rs` once the SDK is present under `.horizon/sdk/`. `python -m unittest discover -s tests` (Python 3.11 or newer) checks the loot comparison tool.

## Source and tools

- `src/lib.rs`: settings registration and the `right_click_block` hook.
- `src/harvest.rs`: target choice, harvest and replant through Horizon's block, loot and inventory calls.
- `src/core.rs`: plant table, payment choice and unit tests; no game calls.
- `assets/right_click_crops/lang/en_us.json`: setting labels.
- `tools/compare_loot.py`: compares recorded ordinary and modded loot observations.
- `tools/test_*.py`: gameplay checks driven by `horizon-ctl` against an already running isolated test session. Run a script with `--help` for its arguments; these scripts do not launch a game or prepare Minecraft resources.

Product behaviour is defined in [Requirements](requirements.md), with rationale in [Decisions](decisions.md). Player-facing guides cover [harvest rules and drop chances](harvesting.md), [installation](installation.md), [settings](settings.md) and [multiplayer compatibility](multiplayer.md).

## Boundaries

- Do not edit a player's Horizon installation or normal saves.
- Do not commit game resources, the downloaded SDK, build output or credentials.
- Use Horizon's ordinary loot, growth and world-update paths.
- Keep gameplay claims separate from compilation and structural checks.
- Public releases, repository visibility changes and public announcements require separate approval.
