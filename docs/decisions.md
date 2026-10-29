# Decisions

## Approved

- 2026-10-29: Repository name: `horizon-right-click-crops`, not the broader `horizon-harvest`.
- 2026-10-29: Use a native mod through `horizon-mixins`, following levzzz's recommendation to "use mixins" in a Discord screenshot provided by the user. This chooses a direction, not verified gameplay or platform compatibility.
- 2026-10-29: Set up local Git and a private personal GitHub repository. Making it public and publishing releases require separate approval.
- 2026-10-29: Use the approved GitHub author name and noreply address only in this repository; do not change global Git identity.
- 2026-10-29: Use the core GitHub Spec Kit workflow for OpenCode, without additional extensions or automatic runtime events. Planning does not authorize automatic implementation.
- 2026-10-29: Loot falls on the ground. Reserve one suitable planting item from generated loot before spawning the rest; picking it up is not required for replanting.
- 2026-10-29: Do not cancel harvesting merely because planting material is unavailable. When neither loot nor inventory can pay, remove the plant, drop all loot, and leave empty farmland. The earlier proposal to cancel harvesting was rejected.
- 2026-10-29: Inventory fallback is now approved. Pay from generated loot first; if it has no suitable item, consume exactly one from the player's inventory. This supersedes the earlier no-inventory-search restriction. Never charge both sources.
- 2026-10-29: Do not intercept bone meal interactions, including on mature crops.
- 2026-10-29: Holding right-click while aiming at successive mature plants may harvest each through normal repeated interactions, one targeted plant at a time, not an area action. No fresh press per plant is required.
- 2026-10-29: Creative mode, commands, and bone meal may prepare an isolated test field and supplies. Switch to survival for harvest checks. The mechanic itself must work without cheats/OP; preparation does not decide creative-mode harvest behavior. Verify natural growth separately rather than treating bone meal as proof of it.
- 2026-10-29: All Git-tracked and GitHub-facing material, including code and comments, must be English. Conversation and ignored local review files may be Russian. Preserve Russian originals locally; do not rewrite existing Git history without separate approval.
- 2026-10-29: The user approved the revised wheat specification and explicitly authorized replacing the initial Git history with an English-only root commit on the private repository's `main` branch. Preserve the previous history locally and use an exact force-with-lease guard. This does not authorize future history rewrites or gameplay implementation. GitHub may retain unreachable old objects or cached views after the branch is rewritten.
- Work in small steps, discuss architecture, and explain technical decisions in plain Russian to the user.

## Pending

- Exact Horizon/Mixins revisions and whether to use stable native hook points or direct revision-pinned hooks.
- The project's own code license, public presentation, and the date for opening the repository.
- Open product choices in `requirements.md`, the release crop list, and settings format.
- Specific external Rust skills: mentioning one does not mean it is installed.
- Separate acceptance of the draft project principles and agreement on the technical plan. The approved product specification does not by itself authorize implementation.

## Why not extend the WASM API first?

The inspected server API 0.3 lacks the full right-click/ordinary-loot path. However, Horizon already provides native mods, `.hnmod` catalog entries, and launcher builds. After research and the Discord recommendation, the user chose that direction. The earlier assumption that a new WASM API is required is not the current decision.
