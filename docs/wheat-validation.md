# Wheat prototype validation

Date: 2026-10-30. Version: `0.1.0-dev.2`. This is an implementation record, not a public release or full acceptance claim. The user authorized proceeding after the separately validated `dev.1` foundation.

## Boundaries

- Horizon source `64e298952d8bbb1188108bd4de68be2ab25d202b`; Mixins `3f99a5c60dfa311cc365524c44ae2fd799bfa1de`; existing launcher-owned Rust/Cargo 1.99.1 and MinGW on Windows.
- Ordinary installed resources and the dependency cache are reused read-only/as a build cache. Source exports, generated stages, targets, control endpoints and saves stay in ignored `.local/`. No account or real-world import.
- Four HEAD hooks and two support modules, only in three generated Rust files. No pristine-source edits, upstream patch, new protocol, runtime dependency or game save format.
- Survival wheat for the integrated server owner and in-frame local player only. No guest/dedicated activation or compatibility claim. Bone meal in either hand bypasses harvesting. The ordinary native setting is latched per process: fully restart after changing it.
- Payment searches ordinary slots 0..36 then offhand 40. Armor, crafting/cursor, containers, nested items and nearby ground items do not pay.

## Checks completed

- Nine standalone Rust payment/enablement tests passed with `cargo test --locked --offline`.
- Twenty-four Python tests passed: sixteen structural checks and eight synthetic checks of the paired ground-loot verifier. These are not compilation or gameplay proof.
- Five read-only AST audit tests passed, including rejection of a changed cancellation return. The real stage audit passed for `game.rs`, `game/native_hooks.rs` and `game/remote.rs`: removing exactly the declared additions preserves the canonical original syntax.

## Native build

The Windows native executable compiled successfully in 2m15s on the first complete pass. Nine embedded payment/enablement tests passed in the game test binary after a 2m23s test build; 159 unrelated upstream binary tests were filtered out. That build emitted four private-interface visibility warnings for the two adapter functions. The adapter visibility was then reduced to `pub(super)`, restaged through Mixins and rebuilt successfully in 1m18s without warnings; nine embedded tests passed again. No Clippy result is claimed.

Before that pass, the first plan rejected a helper's qualified result alias because the tool requires the exact syntactic target result; helpers now use the target's own `Result<bool>` and `DryUse` spelling. A build invocation reached its harness time limit while compiling dependencies; it was not counted as a pass. The next compile exposed a private upstream property accessor; the adapter now reads age from the actual public registry state without modifying upstream visibility. An attempted formatting command found no installed `rustfmt`; no formatter was downloaded and no successful fmt check is claimed.

Windows staging uses a fresh output: the previous generated stage is retained, Mixins creates `.local/build/horizon-wheat`, and only byte-identical files inherit their earlier modification times. No generated Rust is hand-patched. An explicit block around the gameplay closure keeps the payload's canonical syntax identical when nested by the formatter; the audit does not waive changed executable statements.

```powershell
. .\tools\Enter-NativeBuildEnvironment.ps1
$env:CARGO_TARGET_DIR = Join-Path $PWD '.local\build\game-target'
cargo build --locked --offline --profile fast -p horizon-client --bin horizon-client --features horizon-client/mods --manifest-path .local/build/horizon-wheat/Cargo.toml
cargo test --locked --offline --profile fast -p horizon-client --bin horizon-client --features horizon-client/mods --manifest-path .local/build/horizon-wheat/Cargo.toml 'game::right_click_crops::tests::'
```

## Gameplay: default integrated server

Run directory: `.local/runs/wheat-gameplay-8e42c682/`. The game's own `horizon-ctl` drove actual mouse interactions through its local control socket. Every scenario prepared its fixture with creative/commands and switched the acting player to survival before the right-click; pre/post block, inventory and nearby ground-item JSON is kept in the ignored run directory. The integrated server ran on its default separate thread. Processes exited gracefully between phases. The test name, world and all homes were isolated from normal user data.

Passed observations:

- Mature wheat with an empty hand and inventory: age 7 became age 0, exactly one wheat item and a stack of two wheat seeds appeared on the ground in the observed result after the mod's seed reservation. No items were granted directly to inventory. Farmland remained `minecraft:farmland[moisture=7]`. An immediate repeat left the young crop unchanged and did not create a new ground entity. The original roll's count was not independently measured in that first smoke fixture; later paired comparisons are recorded separately.
- With nine inventory seeds present, the same ordinary loot-funded harvest left all nine unchanged. With the ordinary game rule `minecraft:block_drops=false` as a **controlled empty-loot fixture**, two inventory seeds became one and wheat restarted at age 0. With no suitable item the crop became air over unchanged farmland and no loot was invented. Three beetroot seeds did not pay for wheat. An offhand-only single wheat seed paid exactly once in the empty-loot fixture.
- Bone meal on mature wheat did not harvest or consume bone meal; bone meal in the main or off hand on young wheat grew it through the ordinary item path with its ordinary one-item cost, not via harvest. A throwable offhand item was not used after a main-hand harvest.
- A held right-click successively harvested three aimed mature plants without releasing; an adjacent un-aimed mature plant stayed intact. Ordinary left-click removed wheat without replanting; ordinary seed planting still charged one seed. Mature carrots were unaffected.
- A world-border-denied click left the mature crop, fallback inventory seed and ground unchanged. A full inventory still yielded the wheat item on the ground without consuming the held stone stack or placing it. A paid replant retained its young wheat and one remaining inventory seed after a full save, process exit and reopen.
- The ordinary game had generated wheat seeds in the loot-funded fixture; remaining ground stacks showed counts two and three in two separate rolls after the one-seed payment. This is evidence for those rolls only, not a universal loot-count guarantee or a direct fixed-count replacement for Horizon's loot mechanism.
- The world was prepared with commands, then placed in survival. **Separately, Allow Commands was switched OFF through the actual World Options UI and applied before an empty-hand harvest.** The UI still displayed OFF afterward; survival harvest completed, wheat age became 0, farmland stayed moisture 7, ground wheat appeared and inventory remained empty. This tests a cheats-disabled world *after preparation*, not a new world created with commands disabled or an independent non-OP LAN guest.
- Version `dev.2` was toggled OFF in the actual native Mods UI with a mature wheat fixture prepared, survival mode and world commands OFF. After a full game-process restart, the UI still showed OFF and a real right-click left mature wheat, farmland and the empty inventory unchanged with zero new ground items and zero mod activation log lines. This verifies restart-based disabling, not immediate live client/server synchronization or a clean removal of the mod from the build.
- The same isolated saved world was reopened with the **installed unmodified matching Nightly executable**, referenced read-only rather than copying or editing it. The native mod row was absent; mature wheat and farmland loaded normally, and a survival right-click left both intact with no mod activation log. This is a clean remove-mod check on the matching local Nightly, not a promise for other revisions or dedicated deployments.

## In-frame comparison

An additional isolated world under `.local/runs/wheat-in-frame-cfc329ef/` ran with `--in-frame`. Actual survival right-click replanted mature wheat using generated loot and spawned wheat on the ground without inventory charge. In a controlled zero-loot/zero-seed fixture it removed the mature wheat and left the farmland empty. These two scenarios passed on the comparison path; no general parity claim follows from them. An attempt to wait 1,200 in-frame game ticks for random growth hit the control helper's 40-second timeout, and that growth case was **not** counted as passed. The test game exited gracefully. A subsequent in-frame retry passed both harvest slices.

## Paired ordinary-game loot comparison

Four separate, closed test saves were prepared with four mature wheat plants each, fixed seed 42 and `random_tick_speed=0` to keep the loot fixture stable. Each save was copied into two fresh isolated homes; every copied save file was checked byte-for-byte with SHA-256. One branch used the installed unmodified matching Nightly to break the plants normally, and the other used this mod to right-click harvest them. Both branches used survival and the same held item. Navigation teleports and tool preparation were harness setup, not part of the harvest operation.

The paired observations were checked after **each** plant, not just against the final total. All ground item counts matched the ordinary branch minus one wheat seed per replanted plant; no other item type/count changed, and the player inventory received no loot. Results for four plants per row:

| Actual held item | Ordinary wheat | Mod wheat | Ordinary seeds | Ground seeds after mod replants | Reserved seeds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Empty hand | 4 | 4 | 14 | 10 | 4 |
| Diamond hoe | 4 | 4 | 14 | 10 | 4 |
| Diamond hoe, Fortune III | 4 | 4 | 22 | 18 | 4 |
| Diamond hoe, Silk Touch I | 4 | 4 | 14 | 10 | 4 |

These are observed seeded rolls, not custom fixed loot counts implemented by the mod. The actual Fortune III and Silk Touch components were asserted after reload and immediately before each action. An initial Fortune-labelled run was rejected as enchantment evidence: the control CLI's shortcut `enchant` changed only the window's inventory, so the authoritative player reloaded without Fortune. A client-local teleport also failed to place a later branch reliably. The corrected harness used server commands `enchant @s ...` and `tp @s ...`, allowed synchronization ticks, asserted the held enchantment in the action snapshot, and repeated all four pairs successfully. No mod or upstream gameplay code was changed to correct those harness issues.

Ignored receipts: `.local/build/loot-parity-results.json`, per-branch `loot-parity-branch.json`, per-clone hash receipts and the pre-action state/inventory plus post-action crop/ground JSON. The reusable development-only verifier is [tools/compare_loot.py](../tools/compare_loot.py); it reads two branch JSON files and rejects lost/extra unrelated loot, free replants or extra seed payment. Its eight synthetic tests are not substitutes for the actual paired game runs.

```powershell
python tools/compare_loot.py PATH_TO_ORDINARY_BRANCH_JSON PATH_TO_HARVEST_BRANCH_JSON
```

## Ground seeds and saved ground loot

Run `.local/runs/wheat-ground-seeds-8f3130f3/` used a controlled empty-loot wheat fixture. Three seeds were dropped using the real Ctrl+Q input path, the server inventory was allowed to synchronize, and the harvest ran with no inventory seed. Wheat was removed without replanting; the existing ground seed entity kept its id and all three seeds. A separate normal loot-funded harvest in that world yielded one wheat and two ground seeds; after graceful exit and full reopen, the young crop persisted and the same item counts remained on the ground without inventory awards or replay.

The earlier ground-only attempt was rejected: the CLI's `drop all` shortcut directly changed client state rather than sending the server's drop action. Its ghost seed entity coexisted with an unchanged server inventory, from which one seed was then correctly paid. The physical key path and synchronized inventory precondition corrected the test; this was not a mod consuming nearby ground items.

## Nonempty seedless loot (test-only resource fixture)

Ordinary mature wheat's pinned loot table always has a positive wheat-seed base count, so a nonempty seedless result cannot be honestly presented as a naturally occurring ordinary roll. The additional run `.local/runs/wheat-nonempty-seedless-46f58e70/` instead used a separately authored **test-only** loot table yielding one wheat and no seeds. The ordinary `block_drops` rule remained true.

The fixture had its own ignored resource root: root files and the `data/` directory were copied locally, other resource directories were referenced with junctions, and only the copied wheat table was replaced with the authored fixture. No installed table or mod gameplay code was changed; the installed wheat table's SHA-256 was checked before and after the run. This fixture is not part of the mod bundle or ordinary-game compatibility claims.

Actual survival clicks passed all three cases:

- One inventory seed: exactly that seed was consumed, wheat replanted at age 0, and the **entire** generated one-wheat loot result remained on the ground.
- No inventory seed: mature wheat was removed, unchanged farmland stayed empty, and the full one-wheat loot dropped without any planting item being invented.
- Border-denied action with one inventory seed: mature crop and seed stayed unchanged and no wheat item appeared. This is a genuine upstream border denial, not an empty-loot success being mislabelled cancellation.

## Unsupported plants

Run `.local/runs/wheat-other-plants-6bb69f72/` confirmed ordinary survival interactions with the mod enabled: a mature sweet berry bush reset to age 1 and dropped sweet berries without wheat/seeds or an inventory cost; a berry-bearing cave vine kept the vine, cleared its berry flag and dropped exactly one glow berry without a second loot result or planting charge. Mature-carrot passthrough was checked earlier. This covers those plants, not generic compatibility with all modded crops.

## Disabled ordinary-action comparisons

In `.local/runs/wheat-disabled-setup-a746079c/`, the native mod was turned OFF through its UI and the entire process restarted before testing. With the effective process setting OFF, mature and explicitly aimed age-zero wheat produced no right-click harvest. Bone meal grew young wheat at a one-item cost, ordinary left-click removed mature wheat, ordinary planting spent one wheat seed, and a mature sweet berry bush kept its age-one reset and berry drops. No mod activation log appeared in the disabled process. These observed action results match the corresponding enabled passthrough cases; not every possible item/plant combination was exhaustively compared.

## Natural random-tick growth (accelerated fixture)

In a separate fresh default-integrated-server world `.local/runs/wheat-natural-growth-c73dbc11/`, wheat began at age 0 on irrigated farmland. After creative fixture preparation, the game's `minecraft:random_tick_speed` rule was increased from 3 to 250, the player returned to survival, and 1,200 world ticks ran **without bone meal, forced block-age changes or a harvest action**. The crop reached `minecraft:wheat[age=7]`. The rule was restored to 3 and the game exited normally. This verifies the ordinary random-tick growth mechanism at accelerated test speed; it does **not** establish elapsed growth time under the default speed.

The same isolated world was then reopened with the mod: its naturally matured wheat was harvested through a real survival click, yielding an actual mod-replanted age-zero crop. The random-tick rule was again accelerated to 250 only after that harvest; the player returned to survival and the replanted wheat reached age 7 after another 1,200 ticks without bone meal or age-setting commands. The ordinary tick rule was restored to 3 before a graceful exit. Thus **mod-replanted** wheat also grows normally under accelerated random ticks; default-speed elapsed time remains unmeasured.

The inspection harness twice failed to aim at a very short age-0 crop because natural grass blocked its camera ray; clearing nearby view obstruction in the isolated fixture fixed the harness. This was not counted as a gameplay defect. An initial attempt to open a nonexistent `options world` control page was corrected to pause-screen > World Options; the save/persistence assertions had already passed.

An explicitly aimed age-zero wheat retest first found an already-present ground seed after the click. Inspection of the **pre-click** item JSON showed the same entity id and count before the click: clearing the fixture terrain after the harness's earlier cleanup had dropped it. The fixture cleanup was moved after block preparation. The corrected run `.local/runs/wheat-passthrough-d4499b3a/` confirmed the crosshair was on age-zero wheat and the click changed neither the crop, inventory nor pre/post ground-item ids. A mature-wheat click with bone meal only in the offhand also left the crop, meal count and ground loot unchanged.

## Still unverified / not promised

- Full natural growth timing at ordinary random-tick speed; the accelerated mechanism check above is a separate, narrower result, not evidence of default-speed timing.
- Other-mod protection hooks and cancellation ordering, non-OP LAN guests, two-player concurrent use, dedicated server installation and compatibility, other crops/modes, all revision/platform combinations, and live enablement synchronization. No universal multiplayer claim.
- Arbitrary tool/enchantment combinations beyond the four paired cases above, every edge case in AS-01 through AS-24 and no-partial-side-effect behavior if an unexpected upstream level update fails after loot RNG is rolled.

## Product scenario ledger

These are **scenario-level judgments for the observed fixtures**, not a claim of version-independent compatibility. A partial mark means an important variant of the scenario remains unrun.

| Product scenario | Observed status | Missing variant, if any |
| --- | --- | --- |
| AS-01, AS-02, AS-04, AS-05, AS-06, AS-08, AS-09, AS-10, AS-11, AS-21, AS-22, AS-23 | Passed | AS-06/23 used controlled zero-loot fixtures or border denial where relevant. AS-02/08 had an explicitly aimed age-zero retest. AS-09 checked both hands on young wheat and both hands' mature-wheat passthrough variants across fixtures. |
| AS-03 | Partial | Accelerated natural ticks verified on an actual mod-replanted crop; default-speed timing still pending. |
| AS-07 | Passed in controlled fixtures | Exact one inventory seed paid with both empty loot and an authored nonempty seedless loot result. Neither seedless case is claimed as an ordinary natural wheat roll. |
| AS-12 | Passed for tested plants | Mature carrots, sweet berry bushes and glow-berry vines retain ordinary behavior; arbitrary other or modded plants untested. |
| AS-13 | Partial | World-border denial passed; other reach and protection-mod denials pending. |
| AS-14 | Passed for tested tools | Four crops each with empty hand, plain diamond hoe, Fortune III hoe and Silk Touch I hoe matched ordinary loot exactly minus replant seeds. Arbitrary other tools remain untested. |
| AS-15 | Partial | Repeated click and projectile offhand passed; not all two-hand/tool combinations. |
| AS-16 | Passed for tested results | Young crop, inventory payment and ground-loot counts persisted across full process restarts without replay. Other save outcomes are separate variants. |
| AS-17 | Passed for observed actions | Restart-disabled mature/young wheat, bone meal, ordinary breaking/planting and berry bush checks passed. No universal item/plant parity claim. |
| AS-18 | Passed | Saved world opened with the installed unmodified matching Nightly executable; crops/soil persisted and right-click stayed ordinary. Other revisions untested. |
| AS-19 | Partial | Border denial and core payment-selection cancellation passed; unexpected upstream failure and third-party cancellations untested. |
| AS-20 | Not run (P2) | Two players and both multiplayer environments untested. |
| AS-24 | Passed for tested exclusions | Wrong crop seeds and nearby ground seeds did not pay; the latter used real drop input with a synchronized empty inventory. |

Use the [product scenarios](../specs/001-wheat-harvest/spec.md) as the acceptance checklist; passing the slices above is **partial gameplay verification**, not complete prototype acceptance.

The validation work included no public release, new crop support or upstream message. The user subsequently authorized a source-only checkpoint push to the existing private repository; local game resources, builds, test saves and raw run evidence remain excluded.
