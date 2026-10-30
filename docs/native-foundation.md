# Native foundation

## What exists

Version `0.1.0-dev.1` is a compiled and smoke-tested foundation, not a crop-harvesting release. The bundle is in `mixins/right-click-crops/` and has three ordinary, non-cancelling HEAD hooks:

1. Register an explicitly labeled foundation row in Horizon's native mod list.
2. Log foundation activation once per process when the mod is enabled.
3. Log the first observed block-use boundary once per process when enabled, then let the original action continue unchanged.

It does not inspect maturity, evaluate loot, consume seeds, change blocks, intercept client prediction, add packets, or perform harvesting. It has no custom settings or save data. Logs contain no player names, positions, inventory contents, or credentials. The row remains visible when disabled; logging checks Horizon's enablement state. Disabling across a full process restart was verified in the isolated default-integrated-server test; immediate live synchronization is not claimed.

The shared runtime is also a dependency-free standalone Cargo library. Its four Rust unit tests cover one-time observation, independent observation flags, concurrent observation, and explicit foundation identity. All four passed with the installed Rust 1.99.1 using locked, offline dependency resolution.

## Pins and limitations

`compatibility.json` and the bundle pin Horizon `64e298952d8bbb1188108bd4de68be2ab25d202b`. This is the user-approved initial source target, already installed as a Nightly game but not extracted as native source in the inspected cache.

Mixins `3f99a5c60dfa311cc365524c44ae2fd799bfa1de` is the explicit pin validated for this foundation build. The existing launcher tool is older `0d6b103...`; it rejects body macros that the newer pin documents preserving for HEAD hooks. After separate user approval, the exact newer tool source was downloaded and compiled with the existing Rust. It resolved all three hooks, staged the real pinned Horizon source, and the corrected foundation compiled successfully. Do not substitute the old tool or claim gameplay compatibility from compilation alone.

All hooks are non-cancelling, and the two observation adapters receive an immutable game reference. Registration only appends the mod's own row if absent. This is an implementation description, not a substitute for Rust checking or a security proof.

The package is not publishable through Cargo, and its own-code license remains undecided. There is no release `.hnmod` or install-ready claim.

## Checks available without building native code

From the repository root with Python 3.11 or later:

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
```

These standard-library-only tests validate JSON/TOML parsing, matching pins/identity/version, unique manifest identifiers, expected target names, payload paths, non-cancelling hook declarations, the shared runtime path, and dependency/lockfile structure. They do not resolve hooks against the real Horizon AST, compile Rust, execute the Rust tests, or prove gameplay.

The 15 structural Python tests, four standalone Rust tests, real Mixins target resolution, read-only AST audit, and actual native game compilation have passed. The audit's own four tests include rejection of an altered helper and unrelated body changes. The same four runtime tests passed inside the compiled Horizon test binary. The isolated foundation launch, mod row, actual survival block-use logging, and disabled/restart checks also passed. None is a harvest acceptance test. See [native-validation.md](native-validation.md) for exact scope and remaining checks.

The checked-in root lockfile describes only this dependency-free package. It was initially prepared manually and has now been validated by a successful locked, offline Cargo test run. The audit tool has its own separately locked development dependencies, not game/runtime dependencies.

## Next gate

Historical gate: the user subsequently accepted the foundation and authorized wheat implementation on 2026-10-30. Current work is documented in [wheat-validation.md](wheat-validation.md); the rest of this section records the earlier stop point.

The foundation launch was separately approved and completed with isolated test data. Native registration, startup/block-use logging on the default server-thread path, and disabling across process restart were checked; the game was then closed.

Stop for review before replacing observation with actual wheat harvesting. Product acceptance, client fall-through handling for a consuming harvest, inventory payment, growth, multiplayer, other platforms, and immediate live enablement synchronization are not proven by this foundation. Harvesting implementation and public release remain unapproved.
