# Installation

## Release package

Download `right_click_crops-1.0.0.hnmod` from the [official 1.0.0 release](https://github.com/AyanoKaito/horizon-right-click-crops/releases/tag/v1.0.0), and compare its SHA-256 with the value listed in that release. Version `1.0.0` targets Horizon revision `9d979caa48a3bb58203319b9ea044db58c38e0d8`; compatibility with newer Nightlies is not claimed.

Official repository: <https://github.com/AyanoKaito/horizon-right-click-crops>

## Horizon launcher

Horizon native mods run as native code with the player's privileges. Read the source and accept Horizon's trust warning only if you trust this project.

Use the launcher's Mods page and **Add from GitHub** with the official repository URL. Horizon resolves a release to an exact `.hnmod`, verifies its GitHub digest, and builds a separate native-mod game instance after the player explicitly approves the build. A GitHub release is separate from a listing in Horizon's reviewed mod registry.

The first native build may download Horizon's Rust toolchain and take substantially longer than later builds.

## Updates and removal

Use Horizon's normal GitHub-mod update and removal controls. Worlds keep ordinary Minecraft plant states and do not require this mod to load. Back up important worlds before changing any native mod build.
