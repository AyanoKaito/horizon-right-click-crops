# Horizon Right-Click Crops

An independent, work-in-progress Horizon mod for harvesting mature crops with right-click and replanting when a suitable planting item is available in the drops or the player's inventory.

**Compiled survival wheat prototype with partial game verification. Not a public release or fully accepted build.**

The earlier [native foundation](docs/native-foundation.md) compiled and passed an isolated smoke test. Version `0.1.0-dev.2` adds the survival wheat implementation: ground loot, one seed from loot first or inventory second, and no replant when neither can pay. See the [integration contract](specs/001-wheat-harvest/contracts.md) and [wheat validation record](docs/wheat-validation.md) for actual progress and limitations. Foundation results alone do not validate harvesting.

The initial implementation is limited to the single-player owner (default integrated server and the in-frame comparison path). External clients, LAN guests and dedicated servers are not enabled or supported yet. Fully restart the game after toggling the native mod; live toggling is not implemented. Other game modes and crops remain unchanged.

Additional isolated checks compare four tool cases, including Fortune III, against the ordinary game; all 16 paired crops preserved ordinary loot minus exactly one seed per replant. Nonempty seedless loot was checked with a separately authored test-only resource fixture, not by changing ordinary installed loot or the mod's runtime tables. See the validation record for scope, raw-evidence locations and remaining acceptance work.

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
