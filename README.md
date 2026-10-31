# Horizon Right-Click Crops

A small native Horizon mod that harvests mature plants with right-click, replants when appropriate, and lets every mod-managed plant be disabled separately.

> **Pre-release preview.** The current source targets Horizon Nightly `2026-10-29` (`64e2989`) and Minecraft: Java Edition 26.3. No public `.hnmod` package or stable release is available yet.

## Features

- Right-click one mature plant to harvest it.
- Use Horizon's ordinary loot, including supported tool and Fortune effects.
- Replant with exactly one matching item from the generated loot, or from the player's inventory when the loot has none.
- Harvest without replanting when no matching item is available; never create a free seed.
- Keep a viable base for vertical plants and the attached stem for pumpkins and melons.
- Toggle each of the sixteen mod-managed plant families independently in `Options > Mods > Right-Click Crops > Settings`.
- Preserve ordinary left-click breaking, immature crops, bone meal and unrelated interactions.

The mod handles one targeted plant at a time. It does not add area harvesting, bonus loot, hunger costs or experience costs.

## Supported plants

| Behavior | Plants |
|---|---|
| Harvest and replant | Wheat, carrots, potatoes, beetroot, nether wart, cocoa, torchflower, pitcher crop |
| Harvest upper growth and retain a living base | Sugar cane, cactus, bamboo, kelp, twisting vines, weeping vines |
| Harvest fruit and retain the associated stem | Pumpkin, melon |
| Ordinary Horizon behavior, not modified by this mod | Sweet berries, glow berries |

Plants outside this explicit list are passed through unchanged. Generic compatibility with crops from other mods is not claimed.

## Settings

The in-game page is one alphabetical scrolling list of `Plant: ON/OFF` buttons. Changes apply immediately to the client and its integrated server.

The same choices are stored in:

```text
horizon-mods/.horizon-mod-data/right-click-crops/plants.conf
```

Manual file edits load on the next game start. The standard global native-mod switch still controls the whole mod and requires a full process restart. See [Plant settings](docs/settings.md) for the exact keys and defaults.

## Current compatibility

- **Verified:** isolated survival single-player with Horizon's default integrated-server path.
- **Also exercised during development:** Horizon's in-frame single-player comparison path.
- **Not yet supported or claimed:** external multiplayer clients, LAN guests, dedicated servers, creative/adventure harvesting, other Horizon revisions, or arbitrary modded crops.

Native Horizon mods are revision-pinned and compiled into a dedicated game build. This source will need a compatibility update for a different Horizon Nightly.

## Installation status

This repository currently provides a source preview, not a player-ready release. A reviewed `.hnmod` package and launcher/catalog instructions will be added after the remaining compatibility, packaging and licensing work is complete.

For the native-mod model itself, see Horizon's [native mod documentation](https://github.com/horizon-rust/horizon/blob/main/docs/native-mods.md).

## Original implementation and AI assistance

Right-Click Crops is an original implementation for Horizon. It is **not a port of another crop-harvest mod**, and no gameplay source code was copied from one. Published behavior of similar mods was reviewed only to understand common expectations and define this project's scope.

Development was AI-assisted under human direction. AI tooling contributed to implementation, test harnesses and documentation. Claims in this README are limited to checks that were actually run; AI output is not treated as evidence by itself.

The current `dev.9` stage passed:

- 16 standalone Rust tests;
- 26 Python structural and observation tests;
- a real six-hook `horizon-mixins` plan and generated-source AST audit;
- an offline native Horizon build against the pinned revision;
- isolated in-game batches for all agreed plant families;
- live per-plant toggle and restart-persistence checks in the real settings UI.

Exact completed and pending checks are recorded in [Development](docs/development.md), [Compatibility](compatibility.json) and the group validation documents under [`docs/`](docs/).

## Project status

This is work in progress, not an official Horizon or Minecraft project, and is not affiliated with or endorsed by Mojang or Microsoft. The project's own license is still pending, so no public release should be redistributed yet. Third-party development materials retain their own notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
