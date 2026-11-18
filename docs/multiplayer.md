# Multiplayer compatibility

Right-Click Crops performs world and inventory changes on Horizon's authoritative server path. The same gameplay code receives single-player, LAN-host and LAN-guest clicks. The clicking player's game makes the same decision from what it can see, so it does not also use the off-hand item for a harvested click.

Install the mod on every player's game. The host's settings decide what is harvested.

## Status for 2.0.0

- Single-player: not yet checked in game.
- LAN host: not yet checked in game.
- LAN guest: not yet checked in game.
- Dedicated server: not advertised.

Version 1.0.1, a native mod for an older Horizon Nightly, passed single-player and LAN host/guest checks; that evidence does not carry over to the WebAssembly rewrite. Dedicated support will not be claimed until the mod passes a dedicated gameplay check.

The exact machine-readable status is in [`compatibility.json`](../compatibility.json), and observed checks are in [`VALIDATION.md`](../VALIDATION.md).
