# Isolated test environment

## Current state - 2026-10-29

- The installed launcher reports `horizon-launcher 0.2.26` through its CLI. Windows file metadata reports `0.2.0`; use the CLI result, not that resource field, for the version observed here.
- Diagnostic launcher commands ran with separate process-scoped home variables and self-update disabled. No game or native build was started.
- A new Horizon instance with ID `wheat-prototype` was created inside an ignored project-local environment, without `--copy` and without importing an existing profile.
- The instance has no selected game version, play history, worlds, mod bundle, or authenticated account configured by this task. Its normal profile-selection state was not changed: it remains unselected even inside the isolated environment.
- `rust status` in this isolated environment reports pin `1.99.1`, host `x86_64-pc-windows-gnu`, and no installed Rust/linker there. This does not establish whether a toolchain exists in the user's ordinary launcher home.
- Available disk space was checked and is sufficient for the next preparation step; no capacity/size estimate is a promise about the eventual complete build.

## Existing installation inspection - 2026-10-29

After the user clarified that the launcher had just completed setup, the ordinary launcher's tool/cache/version directories were inspected without changing them. Account files and world contents were not read. The earlier empty-cache result applies only to the newly isolated launcher home, not to the computer's existing installation.

Confirmed under the ordinary launcher's data directory:

- Existing `rustc` and Cargo both report version 1.99.1 through direct `--version` calls. Those checks used isolated process homes and wrote diagnostic output only under the project's ignored test directory.
- MinGW's `gcc.exe` and `dlltool.exe` are present. Their existence was checked; no native compilation was run.
- A built `horizon-mixins.exe` exists for revision `0d6b103c70633d8fd9443d8d0acd3aadaacedb06`.
- The Cargo registry cache contains 337 crate archives, and `native/target/release` exists. This is evidence of cached dependencies/build output, not a guarantee that every future dependency or changed revision is cached.
- Source for Horizon `142388e1c136e622652ec7505af15d8ad195e041` is already extracted.
- Installed native version `native-142388e-bef82611e1c9` records Rust 1.99.1, that Horizon revision, Mixins `0d6b103...`, Mouse Tricks 0.2.0, and TreeFall 0.3.0. Its game executable is present. No game was launched during this inspection.
- The proposed Nightly `nightly-2026-10-29-64e2989` is also already installed, with a game executable and a prepared-resource directory. Resource completeness and launch behavior have not been verified. Its source is not among the currently extracted native-source directories inspected.

**Correction to the initial preparation recommendation:** Do not redownload the compiler, MinGW, or installed game merely because the fresh test launcher home has an empty cache. Prefer existing trusted tools/resources, keeping test worlds and generated mod/source outputs isolated. A safe reuse mechanism must be selected before changing launch/build paths; no links, cache copies, normal-profile edits, new downloads, or builds were performed here. The proposed newer Mixins revision and any uncached selected source/dependencies are separate possible additions, not a reason to reinstall the whole environment. Changing revisions can also require recompilation even when the compiler and dependencies are already available.

## Directory boundary

All test state is under the repository-relative ignored directory:

```text
.local/wheat-test-environment/
  game/
    instances/wheat-prototype/
  launcher/
  diagnostics/
  xdg-data/
  xdg-config/
  desktop/
  trash/
```

The ordinary launcher/game data locations are not test homes. No real saves, account files, options, or game resources were copied from them. The user's already-running ordinary launcher was not stopped or reconfigured.

## Required process environment for future commands

Set these only in the PowerShell process that starts a diagnostic/test launcher, never with persistent user/system environment settings:

- `HORIZON_HOME`: the test root's `game` directory.
- `HORIZON_LAUNCHER_HOME`: its `launcher` directory.
- `XDG_DATA_HOME` and `XDG_CONFIG_HOME`: its `xdg-data` and `xdg-config` directories.
- `HORIZON_LAUNCHER_TRASH`, `HORIZON_LAUNCHER_CLIPBOARD`, and `HORIZON_LAUNCHER_DESKTOP`: local scratch paths under the same test root.
- `HORIZON_LAUNCHER_NO_SELF_UPDATE=1` and `HORIZON_NO_AUDIO=1`.

Do not assume running the ordinary desktop shortcut uses these paths. For GUI executables from Windows PowerShell, wait for command completion explicitly before reading exit codes/output. Diagnostic stdout/stderr belong under ignored local storage, not in GitHub documentation.

## Checks actually run

With the isolated environment active:

```text
horizon-launcher --version
horizon-launcher instance create --help
horizon-launcher --json rust status
horizon-launcher --json instance list
horizon-launcher --json instance create wheat-prototype
horizon-launcher --json instance list
```

All completed successfully. The final list showed the isolated default instance and `wheat-prototype`; its home matched the expected test root. The environment setup file was syntax-checked, and local test paths are covered by `.gitignore`.

## Not performed or authorized by this preparation

- No game/toolchain download or installation.
- No account login, credential import, existing-world import, or resource preparation.
- No native mod source, compilation, game launch, or gameplay check.
- No global Rust/PATH/Visual Studio setup.
- No update of the ordinary launcher or modification of ordinary profiles.

Next review: approve the exact retained Nightly/Mixins pair and a safe way to reuse the existing tool/resource cache before preparing a harmless native foundation. Download only actual missing components after checking them; do not assume a full fresh installation is necessary. Trust to execute the concrete native build remains a separate explicit decision. The [technical plan](../specs/001-wheat-harvest/plan.md) and [source research](../specs/001-wheat-harvest/research.md) record candidates and remaining gates, not validated compatibility.
