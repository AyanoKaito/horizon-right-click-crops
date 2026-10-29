# Horizon: right-click crop harvesting - historical brief

English translation of the original Russian brief dated October 28, 2026. Its working title was "Horizon Harvest" and was not yet approved. The byte-identical Russian original is preserved only in ignored local review storage.

**Historical material, not current instructions:** [requirements.md](requirements.md) and [decisions.md](decisions.md) govern the project. Later decisions supersede the cancellation proposal, the inventory-search restriction, and the initial WASM/API assumptions below. The current native direction, inventory fallback, held-click behavior, and creative test preparation are recorded in those documents. Do not execute this archived brief as an implementation authorization.

## 1. Goal

Create a small independent quality-of-life mod for Horizon, a Minecraft implementation in Rust. It should harvest mature crops by right-click while leaving the farmland planted, without manually breaking and replanting each crop.

The result should be a complete tool with a clear feature set, not an unrelated convenience pack, a new farming system, or continually expanding content.

## 2. Agreed behavior at the time

- Ordinary right-click on a mature supported crop: produce harvest loot, pay one suitable seed/item for replanting, and leave the plant at its initial growth stage.
- Right-click on an immature crop: no mod harvest; preserve existing ordinary interactions.
- Left-click: ordinary destruction, allowing the player to clear the farmland.

Harvesting does not require crouching. Earlier "harvest only with Shift" and "replant only with Shift" ideas were misunderstandings and are not requirements.

After harvesting, a young plant should follow the ordinary growth stages again. The mature crop must not immediately produce another harvest. The internal implementation may reset growth instead of physically removing and replacing a block.

## 3. Seeds and loot

- Use ordinary crop loot with supported tool effects, including Fortune. Inspect Horizon's actual mechanism instead of manually recreating loot tables.
- Reserve exactly one suitable planting item from generated loot for replanting.
- Wheat uses wheat seeds; beetroot uses beetroot seeds; carrots use carrots; potatoes use ordinary potatoes, not poisonous potatoes.
- Do not create free seeds or duplicate loot.
- Harvesting must not change the soil/farmland or its state.

The original brief proposed cancelling the entire convenience harvest and keeping the mature plant when loot could not pay for replanting. It explicitly described this as an implementation proposal, not a separate user request. It also warned against silently adding a complex whole-inventory seed search. Both points have since been superseded by explicit user decisions; see the current requirements.

## 4. Scope

### First technical prototype

Wheat only: one right-click, ordinary loot, one-seed payment, growth reset, and subsequent maturation. First prove the cycle in survival without cheats.

### Proposed small first-release set

- Wheat: wheat seeds.
- Carrots: carrots.
- Potatoes: potatoes.
- Beetroot: beetroot seeds.

Nether wart and cocoa are the nearest optional candidates after the basic four. Preserve cocoa's attachment direction. The user had not approved an exact final crop list; not every plant is mandatory for the first release.

### Other growth patterns

Do not apply one replanting algorithm to every plant:

- Berry bushes and glow berries already have ordinary harvesting that preserves the plant. Preserve it without extra seed costs or duplicate loot.
- Possible future sugar cane, cactus, and bamboo support should harvest upper parts while preserving the base.
- Melons and pumpkins require harvesting the fruit while retaining the stem.
- Torchflowers and pitcher plants have special growth behavior and are not required for the first prototype.

These describe boundaries, not mandatory support for vertical plants, pumpkins, or melons.

## 5. Settings

The user wants conveniences to be enableable/disableable. A minimal configuration is sufficient. Proposed defaults:

- Mod enabled: yes.
- Hoe required for convenience harvesting: no.
- Each supported crop enabled: yes.

Choose format and field names according to existing Horizon conventions rather than layering a new system over a suitable existing one.

An in-game toggle/settings page is desirable if supported by the available API. Inspect capabilities first. Do not claim hot toggling before validating it in a working prototype. Document which settings apply immediately and which require a world/game reload.

Do not add area harvesting, experience costs, bonus loot, or hunger costs by default. These are ideas from other mods, not the approved scope.

## 6. Horizon checks proposed before implementation

Earlier research identified Minecraft Java 26.3 as Horizon's target. The feature was not found in official settings or the six-entry mod catalog inspected then. No gameplay launch had confirmed its absence. Versions and capabilities change quickly; inspect the selected commit again.

1. Read upstream `AGENTS.md` and repository instructions. Pin the Horizon revision and target game version.
2. Locate block right-click handling, crops, growth stages, loot, and tool-item logic.
3. Check whether equivalent harvesting already exists; missing documentation does not prove missing code.
4. Inspect real mod interfaces. The inspected reference exposed server block-break/place events and block reads/writes, but generic server right-click interception, complete tool access, and loot spawning were not confirmed then.
5. The brief initially proposed finding a minimal independent `.hmod` implementation, separating any required API patch from mod code. Do not present an engine-built-in feature as an independent mod. The later approved direction is native `.hnmod`, not this initial assumption.

Do not invent unavailable APIs. Do not implement the mechanic through creative item grants, OP commands, or a requirement to enable cheats. Single-player world changes must pass through the side simulating the world. Later permission to use creative for test preparation does not change this runtime constraint.

## 7. Interaction correctness

- Process one interaction once, accounting for both hands and client/server behavior.
- A repeated click on a just-harvested crop must not produce more loot.
- Inspect and document bone meal and other ordinary interaction priorities; do not intercept every right-click unconditionally.
- Respect reach, game mode, and existing permission/area-protection checks when present.
- Cancelled operations produce no loot and leave the planting unchanged.
- Do not use two loot sources, such as ordinary break drops plus a manual copy.
- Ordinary planting and breaking continue to work.
- Ordinary crops are enough for a first release; do not promise compatibility with every future modded plant.

## 8. Original prototype acceptance criteria

1. In survival, right-clicking mature wheat produces ordinary loot minus one seed.
2. The same farmland holds initial-stage wheat that subsequently grows normally.
3. Repeated clicks on immature plants produce no items and consume no extra seeds.
4. Immature wheat survives; bone meal works as intended.
5. Left-click can remove the plant completely.
6. Disabled mod behavior is absent.
7. No duplicate loot from a second hand or repeated processing.
8. Harvesting works without cheats/administrative rights; saving/reopening preserves the correct planting state.

Run appropriate repository checks and a short manual gameplay check. Prioritize seed payment, duplicate prevention, and correct world state. Compilation is not gameplay verification. Explicitly list checks not performed.

## 9. References and sources

- Horizon: https://playhorizon.dev/ and https://github.com/horizon-rust/horizon
- Mod API: https://playhorizon.dev/docs/api/mods
- API reference: https://playhorizon.dev/docs/api/mods-reference
- Horizon settings: https://playhorizon.dev/docs/settings
- Horizon mod catalog: https://playhorizon.dev/mods
- RightClickHarvest: https://modrinth.com/mod/rightclickharvest
- RightClickHarvest source: https://github.com/JamCoreModding/right-click-harvest
- Harvest With Ease: https://modrinth.com/mod/harvest-with-ease
- Harvest Rules: https://www.curseforge.com/minecraft/mc-mods/harvest-rules

References illustrate existing gameplay. Java mods do not run directly in Horizon. Respect each project's license when borrowing code/materials. Reproducing every reference feature is not required.

## 10. Original suggested agent starting point

The brief asked an OpenChamber agent to read it and repository instructions, inspect current Horizon for an existing equivalent feature and sufficient APIs, explain a concrete integration path, then build and test a small wheat prototype if that path was confirmed. It excluded expansion into a large farming pack and expected sources, reproducible build/install commands, a usable package format, and an honest verification/limitations report.

This archived starting suggestion is superseded by the current explicit review gates. It is not permission to begin implementation now.
