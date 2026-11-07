# Installation

## Release package

Download `right_click_crops-1.0.1.hnmod` from the [official 1.0.1 release](https://github.com/AyanoKaito/horizon-right-click-crops/releases/tag/v1.0.1), and compare its SHA-256 with the digest GitHub shows for that file on the release page. Version `1.0.1` targets Horizon revision `66f3981f522b24c250b21523a70080965b940424`; compatibility with newer Nightlies is not claimed.

Official repository: <https://github.com/AyanoKaito/horizon-right-click-crops>

### Verify the signature

The release also provides `right_click_crops-1.0.1.hnmod.minisig`. Download it beside the `.hnmod` and verify with [Minisign](https://jedisct1.github.io/minisign/) and the project's public key:

```powershell
minisign -V -P RWRwbuaByP5mM4VUm4kZEQVPiuw+3IEVJ7CZcEHIjY5fPKf9lhQKUZRy -m right_click_crops-1.0.1.hnmod
```

The expected success message is `Signature and comment signature verified`. The public key above (ID `3366FEC881E66E70`) is the same key stored in the project's entry in Horizon's reviewed mod registry, which requires every version to be signed with it. A valid signature proves the package was signed by the matching key, not that its code is harmless.

## Horizon launcher

Horizon native mods run as native code with the player's privileges. Read the source and accept Horizon's trust warning only if you trust this project.

Use the launcher's Mods page and **Add from GitHub** with the official repository URL. Horizon resolves a release to an exact `.hnmod`, verifies its GitHub digest, and builds a separate native-mod game instance after the player explicitly approves the build. A GitHub release is separate from a listing in Horizon's reviewed mod registry.

The first native build may download Horizon's Rust toolchain and take substantially longer than later builds.

## Updates and removal

Use Horizon's normal GitHub-mod update and removal controls. Worlds keep ordinary Minecraft plant states and do not require this mod to load. Back up important worlds before changing any native mod build.
