# Horizon Right-Click Crops

An independent, work-in-progress Horizon mod for harvesting mature crops with right-click and replanting when a suitable planting item is available in the drops or the player's inventory.

**Preparation stage only. No playable mod or release is available yet.**

## Intended behavior

- Harvest a mature supported crop with right-click, without requiring crouching.
- Use the game's normal drops: reserve one suitable planting item from the loot first; if none drops, consume one from the player's inventory when available.
- Drop the remaining loot on the ground. If neither source provides a planting item, harvest without replanting and leave the farmland empty.
- Hold right-click and aim at successive mature plants to harvest them through normal repeated interactions, one plant at a time, not in an area.
- Leave bone meal interactions to the game's normal behavior.
- Preserve normal growth, the farmland below, left-click removal, and unrelated interactions.
- Start with a wheat-only prototype in survival without cheats.

Creative mode and bone meal may be used to prepare isolated test fields and supplies. Harvest behavior is then tested in survival; setup permissions are not a requirement of the mod itself. Natural growth is verified separately from bone-meal-assisted preparation.

## Technical direction

The agreed approach is a native Rust mod using `horizon-mixins`, packaged separately from Horizon. Native mods are compiled into a dedicated game build and run with the player's account permissions; they are not sandboxed.

Horizon revision, native hook compatibility, Windows build behavior and dedicated-server support must be validated before compatibility is advertised. Single-player, LAN and dedicated-server support are goals, not verified capabilities of this project.

Not an official Horizon or Minecraft project. Not affiliated with or endorsed by Mojang or Microsoft. This is not an announced port of another harvest mod.

## Project documentation

- [Requirements](docs/requirements.md) — agreed behavior, limits, and unresolved choices.
- [Wheat prototype specification](specs/001-wheat-harvest/spec.md) — approved product behavior and future acceptance scenarios.
- [Decisions](docs/decisions.md) — approved choices and pending decisions.
- [Research](docs/research.md) — versioned technical findings and licensing references.
- [Development](docs/development.md) — tooling, test preparation, and preparation status.
- [Original brief](docs/original-brief.md) — English translation of the historical input, not the current specification.

All Git-tracked content and GitHub-facing material is in English. Discussion and ignored local review documents may be in Russian. A complete player-facing guide will be prepared before public release.

## License and releases

The project's own code license has not been selected. Do not publish a release until licensing, attribution, tests and package contents have been reviewed. Third-party tooling retains its own license; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
