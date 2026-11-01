<p align="center">
  <img src="assets/crop.png" width="160" alt="Right-Click Crops logo by AyanoKaito">
</p>

<h1 align="center">Right-Click Crops</h1>

<p align="center">
  <strong>Harvest with a right-click. Keep your garden growing.</strong><br>
  A native Horizon mod with sixteen plant families and individual settings.
</p>

<p align="center">
  <a href="https://github.com/AyanoKaito/horizon-right-click-crops/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-4c8c4a" alt="Release v1.0.0"></a>
  <a href="docs/multiplayer.md"><img src="https://img.shields.io/badge/Minecraft-26.3-6b7280" alt="Minecraft Java Edition 26.3"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4c8c4a" alt="MIT License"></a>
</p>

<p align="center">
  <a href="https://github.com/AyanoKaito/horizon-right-click-crops/releases/tag/v1.0.0"><strong>Download</strong></a> &middot;
  <a href="docs/installation.md">Installation</a> &middot;
  <a href="docs/settings.md">Settings</a> &middot;
  <a href="https://github.com/AyanoKaito/horizon-right-click-crops/releases/download/v1.0.0/Right-Click-Crops-Demo.mp4">Watch demo</a>
</p>

<p align="center">
  Built for Horizon Nightly <code>2026-10-31</code> (<code>9d979ca</code>).<br>
  Validated in single-player and LAN host/guest sessions.
</p>

---

## Features

- Harvest one targeted mature plant with right-click.
- Use Horizon's ordinary loot calculation, including applicable tool and Fortune effects.
- Replant with exactly one matching item from generated loot, then fall back to the player's inventory.
- Harvest without replanting when no matching item exists; never create a free seed.
- Retain the base of vertical plants and the attached stem of pumpkins and melons.
- Toggle all sixteen managed plant families separately under `Options > Mods > Right-Click Crops > Settings`.
- Leave immature plants, bone meal, ordinary left-click breaking, sweet berries, glow berries and unrelated interactions to Horizon.

The mod handles one targeted plant at a time. It does not add area harvesting, bonus loot, hunger costs or experience costs.

## Supported plants

| Behaviour | Plants |
|---|---|
| Harvest and replant | Wheat, carrots, potatoes, beetroot, nether wart, cocoa, torchflower, pitcher crop |
| Harvest upper growth and retain the base | Sugar cane, cactus, bamboo, kelp, twisting vines, weeping vines |
| Harvest fruit and retain the stem | Pumpkin, melon |
| Ordinary Horizon behaviour | Sweet berries, glow berries |

Plants outside this list pass through unchanged. Compatibility with arbitrary crops from other mods is not claimed.

## Installation

Download `right_click_crops-1.0.0.hnmod` from the official GitHub Release, or use the launcher's **Add from GitHub** with this repository. Horizon native mods run with the player's privileges and are compiled into a separate game build only after the player accepts Horizon's native-code warning.

See [Installation](docs/installation.md), [Settings](docs/settings.md) and [Compatibility](docs/multiplayer.md) for the current details.

## Compatibility

- Exact target: Horizon Nightly `2026-10-31` (`9d979ca`), Minecraft 26.3.
- The gameplay entrypoints run on the authoritative server path used by single-player, LAN hosts and LAN guests.
- Single-player and LAN host/guest checks passed on this pin; see [Validation](VALIDATION.md).
- Horizon does not yet build native mods through its player-ready dedicated-server pipeline. Dedicated support is therefore not advertised.

Native mods are revision-pinned. A future incompatible Horizon Nightly may require a Right-Click Crops patch release.

## Project integrity

The official repository is <https://github.com/AyanoKaito/horizon-right-click-crops>. Third-party forks cannot change this repository or its releases. Verify release downloads against the SHA-256 value published with the official GitHub Release.

Right-Click Crops is an original Horizon implementation, not a port. No gameplay code from other harvest mods was used. Similar projects were reviewed only to understand common player expectations and define scope.

Development was AI-assisted under human direction. AI tooling contributed to implementation, test harnesses and documentation; only checks that were actually run are reported as evidence.

## License

Original project code and documentation are available under the [MIT License](LICENSE). Third-party materials retain their own notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Right-Click Crops is not an official Horizon or Minecraft project and is not affiliated with or endorsed by Mojang or Microsoft.
