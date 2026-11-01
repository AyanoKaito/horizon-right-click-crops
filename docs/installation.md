# Installation

## Release package

Version `1.0.0` is still undergoing release validation. Install only the `.hnmod` attached to the official GitHub Release once it is published, and compare its SHA-256 with the value listed in that release.

Official repository: <https://github.com/AyanoKaito/horizon-right-click-crops>

## Horizon launcher

Horizon native mods run as native code with the player's privileges. Read the source and accept Horizon's trust warning only if you trust this project.

After release, use the launcher's Mods page and **Add from GitHub** with the official repository URL. Horizon resolves a release to an exact `.hnmod`, verifies its GitHub digest, and builds a separate native-mod game instance after the player explicitly approves the build.

The first native build may download Horizon's Rust toolchain and take substantially longer than later builds.

## Updates and removal

Use Horizon's normal GitHub-mod update and removal controls. Worlds keep ordinary Minecraft plant states and do not require this mod to load. Back up important worlds before changing any native mod build.
