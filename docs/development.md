# Development

Right-Click Crops is a dependency-free Rust core plus a native `horizon-mixins` bundle under `mixins/right_click_crops/`.

## Release pins

- Horizon: `66f3981f522b24c250b21523a70080965b940424`
- Horizon source tag: `nightly-source/2026-11-05-66f3981`
- horizon-mixins: `4342a0bfbe71d4d14185528d64e496d6022f16a1`
- Rust used by Horizon: 1.99.1, `x86_64-pc-windows-gnu`

## Checks

These checks use a normal Rust toolchain and Python 3.11 or newer. Python tests and packaging use only the standard library; no Spec Kit or AI tooling is required.

```powershell
cargo test --locked
python -m unittest discover -s tests
cargo test --locked --manifest-path tools\audit-bundle\Cargo.toml
python tools\package.py
```

The mixin plan and AST audit use pristine source in ignored `.local/` folders. A native Horizon build is a separate trust-gated step and must never be run without explicit approval.

On Windows, `tools/Enter-NativeBuildEnvironment.ps1` can optionally reuse the toolchain installed by Horizon's launcher. Dot-source it before the checks if that toolchain is not already on `PATH`. It changes only the current shell's environment; it is not needed by players installing the release.

## Source and tools

- `mixins/right_click_crops/`: native hooks, harvest logic, settings and standalone Rust tests.
- `tests/`: Python checks for bundle structure, packaging and recorded-loot comparisons.
- `tools/package.py`: deterministic `.hnmod` and SHA-256 builder; writes to ignored `dist/`.
- `tools/audit-bundle/`: compares pristine and generated Rust syntax trees to detect unrelated changes.
- `tools/compare_loot.py`: compares recorded ordinary and modded loot observations.
- `tools/test_*.py`: gameplay checks driven by `horizon-ctl` against an already running isolated test session. Run a script with `--help` for its arguments; these scripts do not launch a game or prepare Minecraft resources.

Some launch/setup and focused regression harnesses used for the release remain local. The published scripts alone do not reproduce the complete validation campaign; see [Validation](../VALIDATION.md) for the scope of the recorded evidence.

Product behaviour is defined in [Requirements](requirements.md), with rationale in [Decisions](decisions.md). Player-facing guides cover [harvest rules and drop chances](harvesting.md), [installation](installation.md), [settings](settings.md) and [multiplayer compatibility](multiplayer.md).

## Boundaries

- Do not edit a player's Horizon installation or normal saves.
- Do not commit game resources, prepared Horizon source, build output or credentials.
- Use Horizon's ordinary loot, growth and world-update paths.
- Keep gameplay claims separate from compilation and structural checks.
- Public releases, repository visibility changes and public announcements require separate approval.
