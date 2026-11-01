# Development

Right-Click Crops is a dependency-free Rust core plus a native `horizon-mixins` bundle under `mixins/right_click_crops/`.

## Release pins

- Horizon: `9d979caa48a3bb58203319b9ea044db58c38e0d8`
- Horizon source tag: `nightly-source/2026-10-31-9d979ca`
- horizon-mixins: `4342a0bfbe71d4d14185528d64e496d6022f16a1`
- Rust used by Horizon: 1.99.1, `x86_64-pc-windows-gnu`

## Checks

```powershell
. .\tools\Enter-NativeBuildEnvironment.ps1
cargo test --locked
python -m unittest discover -s tests
cargo test --locked --manifest-path tools\audit-bundle\Cargo.toml
python tools\package.py
```

The mixin plan and AST audit use pristine source in ignored `.local/` folders. A native Horizon build is a separate trust-gated step and must never be run without explicit approval.

## Boundaries

- Do not edit a player's Horizon installation or normal saves.
- Do not commit game resources, prepared Horizon source, build output or credentials.
- Use Horizon's ordinary loot, growth and world-update paths.
- Keep gameplay claims separate from compilation and structural checks.
- Public releases, repository visibility changes and public announcements require separate approval.
