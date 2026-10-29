# Horizon Right-Click Crops project principles

**Status:** Draft documenting discussed principles; this document has not been separately ratified. It does not authorize implementation, new product decisions, or publication.

## Core principles

### I. One mechanic, a small first proof

Build mature-crop harvesting by right-click with paid replanting. Do not turn the project into a pack of unrelated conveniences. The first gameplay prototype covers wheat only. Full requirements are in `docs/requirements.md`.

### II. Native integration, not a gameplay bypass

The approved direction is `horizon-mixins`. Use Horizon's existing growth, loot, world-state, and player-permission mechanisms. Do not invent APIs, substitute fixed loot counts, or require cheats/OP for the mechanic. Do not promise compatibility before selecting and validating pinned revisions.

### III. World integrity and honest item costs

One interaction must not duplicate loot or create a free seed. Pay for replanting with one suitable item from generated loot first, then from the player's inventory only if needed. If neither can pay, harvest without replanting; this is not cancellation. A cancelled operation has no partial crop, inventory, or drop changes. Preserve immature crops, farmland, planting, and ordinary interactions. Never develop against real player saves.

### IV. Verified behavior over compilation

Check logic, integration, and actual gameplay separately. Derive scenarios from requirements and honestly list failed or unperformed checks. Creative mode, commands, and bone meal may prepare isolated fixtures, but exercise harvesting in survival. Preparation must not become a runtime dependency. Bone meal does not prove natural growth. Claim Windows, LAN, dedicated-server, or other-mod support only after corresponding validation.

### V. Understandable decisions and lawful publication

Explain decisions to the user in plain Russian; use English for all Git-tracked and GitHub-facing content, code, comments, and commit messages. Russian review material stays local and ignored. Agree on architecture, scope, and disputed behavior before implementation. Preserve sources and licenses for borrowed material. Public releases require a rights review and explicit user approval. Keep secrets and Mojang files out of Git.

## Review gates

Requirements -> approved technical plan -> testable tasks -> implementation -> verification report. Spec Kit stores artifacts but replaces neither approval nor testing. Do not execute every phase automatically. First validate a native foundation with isolated data, then wheat; expand only after acceptance.

## Governance

Do not silently change requirements or approval status. Record decisions and reasons in `docs/decisions.md`, working commands in `docs/development.md`, and concise agent rules in `AGENTS.md`. These principles do not override the user's constraints or upstream instructions. Do not rewrite published Git history without separate approval.

**Draft version:** 0.1.1 | **Prepared:** 2026-10-29 | **Last amended:** 2026-10-29
