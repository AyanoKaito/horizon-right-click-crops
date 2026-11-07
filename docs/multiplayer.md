# Multiplayer compatibility

Right-Click Crops performs world and inventory changes on Horizon's authoritative server path. The same gameplay code receives single-player, LAN-host and LAN-guest interactions.

## Current release status

- Single-player on the `1.0.1` pin: passed.
- LAN host: passed.
- LAN guest: passed.
- Dedicated server: not advertised for `1.0.1`.

Horizon documents that native mods are not yet built by its dedicated-server pipeline. The hook call sites exist and a locally built modded game can be started with `--dedicated`, but that is not a player-ready installation path. This project will not claim dedicated support until Horizon provides a distributable path and the mod passes a dedicated gameplay check.

The exact machine-readable status is in [`compatibility.json`](../compatibility.json), and observed checks are in [`VALIDATION.md`](../VALIDATION.md).
