# Installation

## Release package

Download `right_click_crops-2.0.0.hmod` from the [official 2.0.0 release](https://github.com/AyanoKaito/horizon-right-click-crops/releases/tag/v2.0.0), and compare its SHA-256 with the digest GitHub shows for that file on the release page. Version `2.0.0` is a WebAssembly mod built with Horizon mod SDK `0b14f8acfd97fa2c750e42795249dcc981178ca4` (mod API 0.2). It needs a Horizon game that loads WebAssembly mods with that API.

Official repository: <https://github.com/AyanoKaito/horizon-right-click-crops>

### Verify the signature

The release also provides `right_click_crops-2.0.0.hmod.minisig`. Download it beside the `.hmod` and verify with [Minisign](https://jedisct1.github.io/minisign/) and the project's public key:

```powershell
minisign -V -P RWRwbuaByP5mM4VUm4kZEQVPiuw+3IEVJ7CZcEHIjY5fPKf9lhQKUZRy -m right_click_crops-2.0.0.hmod
```

The expected success message is `Signature and comment signature verified`. The public key above (ID `3366FEC881E66E70`) is the same key used for every earlier release. A valid signature proves the package was signed by the matching key, not that its code is harmless.

## Install

1. In the Horizon launcher, open the instance's folder (**Open folder** in its ⋮ menu). This is the folder that holds `options.txt`.
2. Copy `right_click_crops-2.0.0.hmod` into `horizon-mods/` there. Create the folder if it is missing.
3. Turn the mod on: add the line `mod.right_click_crops:true` to `horizon-mods.txt` beside `options.txt`.
4. Start the game. The mod appears on the **Mods** screen; its **Config** button opens the plant settings.

The mod runs in Horizon's WebAssembly sandbox. There is no native build step and no native-code trust prompt. For LAN play, install it on every player's game; see [Multiplayer](multiplayer.md).

## Upgrading from 1.x

Versions 1.0.0 and 1.0.1 were native `.hnmod` packages for older Horizon Nightlies. Remove the old native mod from the launcher's Mods page before installing 2.0.0. Plant settings from `plants.conf` are not carried over: all plants start `ON`, and you can change them again on the settings page.

## Updates and removal

Replace the `.hmod` in `horizon-mods/` to update. Delete it, or set its line to `mod.right_click_crops:false`, to remove it. Worlds keep ordinary Minecraft plant states and do not require this mod to load. Back up important worlds before changing mods.
