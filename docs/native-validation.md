# Native foundation validation

Report date: 2026-10-30. Scope: the non-harvesting `0.1.0-dev.1` foundation only. The user separately approved a short isolated game launch after compilation passed. The foundation smoke test below completed; harvesting is not implemented or accepted.

## Inputs and isolation

- Horizon: `64e298952d8bbb1188108bd4de68be2ab25d202b`.
- Mixins: `3f99a5c60dfa311cc365524c44ae2fd799bfa1de`.
- Existing launcher-owned Rust/Cargo 1.99.1 and MinGW, not a fresh toolchain installation.
- Existing launcher-owned Cargo dependency cache is reused. Missing locked Windows dependencies were fetched after an offline check identified them. No account or world files are involved.
- Archives, extracted sources, staging, diagnostic data, and Cargo targets are under ignored `.local/`. The ordinary launcher/game installation and native game build are not replaced.
- The downloaded Horizon ZIP was 25,536,789 bytes with observed SHA-256 `6d278e460cfcb99352a21d2736c4974fa86a67d26b7116ad31776449c1bde366`.
- The downloaded Mixins ZIP was 265,352 bytes with observed SHA-256 `3ee2b62e16a3b8a46d0c2a25648bd5618dadb952812a6e2c78c41525669cbe0c`.
- These are recorded archive hashes, not a claim of independent signature verification. Sources were retrieved from commit-pinned GitHub codeload URLs. Extraction rejected unsafe paths and skipped one Horizon symlink, consistent with the launcher's source-isolation approach.

## Passed checks

1. **Standalone runtime:** `cargo test --locked --offline` passed all four runtime tests; zero doc tests were present. The root lockfile worked without changes.
2. **Mixins tool:** the exact candidate compiled offline in release mode using the existing dependency cache.
3. **Real target resolution:** Mixins `plan` resolved three injections and one module against the pinned full Horizon workspace, with no bridges or injected state.
4. **Staging:** Mixins `apply` completed. Exactly `crates/horizon-client/src/game.rs` and `crates/horizon-client/src/game/native_hooks.rs` differed from pristine inputs.
5. **Pristine input integrity:** SHA-256 comparison confirmed all 3,570 input files remained unchanged after planning/staging.
6. **AST audit:** the read-only audit removed exactly the three expected hook heads and one unchanged runtime module in memory, then compared canonical parsed Rust syntax with the pristine files. Both files matched. Canonical printing normalizes layout and insignificant trailing punctuation; the initial raw token comparison was too strict for the nested runtime's formatting and was corrected.
7. **Audit negative checks:** four audit-tool tests passed, covering correct removal, altered-helper rejection, preserving unrelated changes for comparison to reject, and missing-method detection.

## Native build result

The corrected staged game executable built successfully on Windows with the `fast` profile, normal default features (audio/controllers), and `horizon-client/mods`. The repeat build took 2m 14s after the hit-type correction; the test-binary compilation took 2m 22s. These are observed warm-cache retry times, not first-build or player-performance promises.

The embedded `game::right_click_crops::tests::` suite passed all four tests, with zero failures. The 159 other upstream binary tests were filtered out and were not run. No game window was opened by these Rust unit tests.

Local executable: `.local/build/game-target/fast/horizon-client.exe`, 108,095,802 bytes; observed SHA-256 `f400eea0dc7aa1a15afa17277b5b203e3265c99209ef861792a172f3758e1f02`. This is a local test artifact, not a published/install-ready release or a gameplay compatibility promise. The detailed local receipt is `.local/build/foundation-build-result.json`.

Post-build integrity verification again confirmed all 3,570 pristine source files unchanged and only the two intended Rust files modified in the generated stage. The later launch check is recorded separately below; binary compilation alone was not counted as game verification.

## Isolated game smoke test

The built executable ran offscreen at 960x540 with the default integrated-server path, render distance 2, and deterministic test terrain. Fresh game/launcher/XDG/scratch homes were created under `.local/runs/`; existing Nightly `64e2989` resources were passed by explicit path, without copying account files or real saves. The test used offline name `CropTest`, no external server or published LAN session, and the existing matching `horizon-ctl.exe` through a unique local control endpoint. Endpoint credentials were not printed.

Observed outcomes:

- The world became ready with `server.address=local`, `joined=true`, and `loaded=true`; this was not an in-frame-only launch.
- The Mods UI exposed `Right-Click Crops (foundation) 0.1.0-dev.1: ON`. A local screenshot and the full widget JSON were saved. The long label is visually clipped at the narrow standard button width, so the complete ON/OFF text was checked through UI state rather than inferred from the screenshot.
- The process log contained the single startup message.
- A mature wheat fixture at `[3,65,-8]` was prepared using permitted creative setup commands. The acting player then switched to survival, aimed at the crop, and performed a real `mouse right click` action.
- The log contained the single block-use observation message. The crop remained `minecraft:wheat[age=7]` and the inventory remained empty, as expected for a foundation with no harvesting implementation.
- Farmland remained farmland. Its moisture changed during ordinary unwatered world ticking; this run is not evidence of exact farmland-property preservation under a harvest operation.
- The mod was toggled OFF through its actual UI. The test game exited gracefully, then the same isolated world was reopened in a fresh process. The UI still showed OFF, the saved player was in survival, and the mature wheat state persisted.
- A further real right-click in the disabled process left the crop unchanged and produced zero foundation startup/block-use log lines. This verifies disabling across a full process restart, not immediate live synchronization with an already-running server thread.
- Both successful test processes and the initial harness-error process were closed through the control interface. No ordinary launcher/profile process was stopped.

Local evidence is in `.local/runs/foundation-smoke-436de0ce/`: UI JSON, ON/OFF screenshots, pre-click state, crop/inventory observations, enabled/disabled process logs, and quit acknowledgements. These files and all worlds/resources remain excluded from Git.

Harness corrections made before the successful run: an initial test name exceeded Horizon's 16-character limit and could not join the integrated server; the retry used `CropTest`. Windows PowerShell `Start-Process -Wait` waited for the launched game descendant as well as the control CLI; the helper was corrected to wait only for the control process using `WaitForExit`. Neither issue required changing the mod or game code.

### Issues found and corrected during validation

- The first native compilation rejected the observer's hit binding. The gameplay method accepts the private `crate::game::Hit` struct, not the distinct `horizon_client::first_person::Hit` enum. Both the helper and manifest now use the actual gameplay type, and the structural regression check asserts this path. This is why target resolution alone was not treated as proof of compilation.
- Mixins on Windows rejected replacing an existing stage with `E_ATOMIC_STAGE`; atomic replacement is Linux-only in this version. The failed first stage was preserved under `.local/build/horizon-foundation-first-attempt/`, and Mixins generated a fresh stage at the stable original build path. Hash-identical files retained their previous timestamps to avoid recompiling unchanged crates; no source text was manually patched. The corrected stage passed the read-only AST audit again before the retry.

## Commands

Run from the repository root in PowerShell. The environment setup changes only the current process and reuses installed tools; it does not start the game or launcher.

The `apply` command below records initial staging into a fresh directory. On Windows, do not rerun it against an existing output directory: preserve the old generated stage and use a fresh destination instead. Do not delete or modify an original source checkout to work around this limitation.

```powershell
. .\tools\Enter-NativeBuildEnvironment.ps1
cargo test --locked --offline

cargo build --locked --offline --release -p horizon-mixins-cli --manifest-path .local\sources\horizon-mixins-3f99a5c60dfa311cc365524c44ae2fd799bfa1de\Cargo.toml --target-dir .local\build\mixins-target

.\.local\build\mixins-target\release\horizon-mixins.exe plan --workspace .local\sources\horizon-64e298952d8bbb1188108bd4de68be2ab25d202b --mods mixins --out .local\build\foundation-plan.json
.\.local\build\mixins-target\release\horizon-mixins.exe apply --workspace .local\sources\horizon-64e298952d8bbb1188108bd4de68be2ab25d202b --mods mixins --out .local\build\horizon-foundation

cargo run --locked --offline --release --manifest-path tools\audit-foundation\Cargo.toml --target-dir .local\build\mixins-target -- .local\sources\horizon-64e298952d8bbb1188108bd4de68be2ab25d202b .local\build\horizon-foundation mixins\right-click-crops
cargo test --locked --offline --release --manifest-path tools\audit-foundation\Cargo.toml --target-dir .local\build\mixins-target

$env:CARGO_TARGET_DIR = Join-Path (Get-Location) '.local\build\game-target'
cargo build --locked --offline --profile fast -p horizon-client --bin horizon-client --features horizon-client/mods --manifest-path .local\build\horizon-foundation\Cargo.toml
cargo test --locked --offline --profile fast -p horizon-client --bin horizon-client --features horizon-client/mods --manifest-path .local\build\horizon-foundation\Cargo.toml 'game::right_click_crops::tests::'
```

The standalone AST audit is a development tool with its own locked dependencies. It does not rewrite source files or add dependencies to the game/mod runtime.

## Not performed

- No harvest acceptance scenario, actual harvest/replant operation, exact farmland-state assertion, or immediate live client/server enablement synchronization test.
- No harvesting, loot, inventory-payment, growth, cheats-disabled/non-OP, LAN/two-player, dedicated-server, in-frame comparison, or other-mod compatibility claim.
- No full Horizon parity suite, global formatter/linter installation, public release, or source/resource publication.
