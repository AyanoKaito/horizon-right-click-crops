# Wheat prototype integration contract

The user authorized wheat implementation after the foundation smoke test on 2026-10-30. Exact source/tool pins and isolation boundaries remain unchanged.

- Two support modules: a dependency-free payment core and typed game adapters. Cancellable HEAD hooks replace observation at `use_hand` and supply only a consumption hint at `remote_block_reacts`. No source-string edits or new network protocol.
- Scope: the integrated server's owner and the in-frame local player, survival only. External clients, LAN guests and dedicated hosting are deliberately not enabled before capability/compatibility work. Other modes pass through.
- Enablement is latched once per process from Horizon's native setting, shared by the window and its integrated server. Fully restart the game after changing it. No live-toggle claim.
- The authoritative hook runs after existing packet reach, spawn-protection and border checks, with the acting player's inventory installed by `as_guest`. It accepts main-hand mature wheat only. Bone meal in either hand passes through, as does secondary use with occupied hands.
- The client hint is limited to the window's own integrated server and a matching mature wheat target. It performs no loot, inventory or block changes and does not skip sending `UseItemOn`.
- Preflight resolves wheat age zero through the actual registry, checks loaded farmland, bounds, border and ordinary survival. One `block_loot_at` call produces local loot; `block_drops=false` produces none. No fixed loot table or second break operation.
- Payment is `Loot(index)`, `Inventory(slot)` or `None`, in that order. Inventory searches slots 0..36, then offhand 40; never armor, crafting, cursor, containers or nested stacks. Counts must be positive and the item exactly wheat seeds. Selection does not mutate anything.
- A successful ordinary `Behaviours::set_block(UPDATE_ALL)` is the commit point. Set wheat directly to age zero or air, without an intermediate break. Before that point failures consume/spawn nothing. The supported wheat-only transition has no block-entity removal side effects. Then debit exactly one selected stack and spawn remaining local loot with `pop_resource`; process ordinary level events. No added hunger, XP, tool cost or save schema.
- A failed preflight/write consumes the attempted interaction without falling through to an unrelated item action. No general transaction API or compatibility with later cancelling hooks is claimed. Other protection mods require separate ordering/integration testing.
- Rechecking maturity on the single authoritative thread prevents replay from harvesting a replanted immature target. Use the existing held-input loop, not a crop scan or custom repeat timer.

## Bounded tasks

- [x] Payment core and tests, including missing/wrong seeds and cancelled commit.
- [x] Typed authoritative adapter and integrated-client consumption hint.
- [x] Real Mixins staging, unchanged-source AST audit and Windows build/tests.
- [x] Isolated survival checks; record each acceptance scenario honestly, including pending growth/multiplayer work.
