# Changelog

All notable changes to Right-Click Crops are documented here.

## 2.0.0 - 2026-11-19

- Rewrote the mod for the Horizon mod SDK as a WebAssembly mod (`.hmod`, mod API 0.2, SDK `0b14f8a`). Horizon retired `.hnmod` native packages and horizon-mixins.
- No native build or native-code trust prompt is needed; install by copying the `.hmod` into `horizon-mods/`.
- One `right_click_block` hook replaces the four native hooks. The clicking player's game makes the same choice, so a harvested click still never uses the off-hand item.
- Plant settings use Horizon's settings service on the mod's Config page. 1.x `plants.conf` values are not migrated; all plants start `ON`.
- Crouching is now read from the clicking player on the server, so a LAN guest's crouch counts correctly.
- Bumped the version to `2.0.0`.

## 1.0.1 - 2026-11-07

- Fixed compilation on Horizon Nightly `2026-11-05` (`66f3981`): Horizon's block loot helper now takes the broken block's entity data. Managed plants have no block entity, so harvest passes none and loot is unchanged.
- Updated the compatibility pin to Horizon Nightly `2026-11-05` (`66f3981`, native hooks API 411).
- Bumped the version to `1.0.1`.
- Updated the project icon with author-approved Gemini-generated artwork and documented its provenance.
- Added focused empty-hand and shears loot checks for twisting and weeping vines, and clarified ordinary vine drops and flower replanting requirements.

## 1.0.0 - 2026-11-01

- Added right-click harvesting for sixteen explicit plant families.
- Added ordinary-loot replanting with inventory fallback and no free planting items.
- Added base-retaining harvest for vertical plants and stem-retaining harvest for pumpkins and melons.
- Added independent in-game settings for every managed plant family.
- Moved gameplay to Horizon's authoritative server hook path for single-player and LAN actors.
- Updated the compatibility pin to Horizon Nightly `2026-10-31` (`9d979ca`).
- Licensed the project's original work under MIT.
- Standardized the internal Horizon package ID as `right_click_crops`.
