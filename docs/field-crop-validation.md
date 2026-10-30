# Field-crop expansion validation

Version: `0.1.0-dev.3`. Adds carrots, potatoes and beetroot to the existing wheat adapter. This record covers one compact test batch, not full acceptance or a public release.

## Implementation

- Exact existing Horizon/Mixins pins, hooks, actor/mode gates and world-write path remain unchanged.
- Explicit profiles select maturity and planting item together: wheat 7 / wheat seeds, carrots 7 / carrot, potatoes 7 / normal potato, beetroot 3 / beetroot seeds.
- The shared payment core now receives that planting item. Poisonous potatoes, beetroot roots and other crops' items cannot pay. Ordinary loot is still evaluated once; world mutation must succeed before inventory payment and ground spawning.
- Other proposed plant families are not implemented by this change. Enablement still requires a full restart; guests, dedicated servers and non-survival harvesting remain gated off.

## Compact batch

`python tools/test_field_crops.py --session .local/build/active-wheat-run.json` uses an already running isolated test instance. It does not build, download or launch a game. `--smoke` selects only normal harvest/repeat cases plus wheat regression for the in-frame comparison. The driver rejects session homes outside this project's ignored `.local/runs/` tree.

Creative commands prepare each clean fixture; state and inventory are checked before actual survival mouse clicks. `horizon-ctl script` batches commands on a single control connection per phase. Raw `.ctl` and `.jsonl` files and `field-crop-results.json` remain beside the isolated save; only concise results are reported in chat.

For each new crop: ordinary ground harvest and payment priority, immediate repeat on the short replanted crop, the last immature stage, exact inventory payment, no material, wrong material, unchanged farmland and accelerated random growth from an actual paid replant. `block_drops=false` is an explicitly controlled empty-loot fixture, not a claim that ordinary carrots/potatoes naturally drop nothing. Beetroot may naturally generate no seed; its normal-loot case allows the exact one-seed inventory fallback instead of asserting guaranteed seed loot.

Shared checks: wheat harvesting and ordinary sweet/glow berry harvesting. Fast Rust tests cover all cross-crop planting-item combinations, positive counts, loot priority, offhand selection and no-underflow/no-wrong-item spending.

## Results

The first run stopped after 12 passed checks because the beetroot fixture had a natural terrain block in the camera ray. Its setup was corrected by clearing the test-only sightline from the player to the target. No gameplay source or native executable was changed for this harness correction.

The complete rerun used a fresh isolated world under `.local/runs/field-crops-retry-*` on the normal separate integrated-server thread. It passed **24 recorded checks** for the three crops, one wheat regression and both ordinary berry interactions; the test game exited normally. Results and detailed per-phase receipts are in the ignored `field-crop-results.json` and `batch-*.jsonl` files beside that world. The driver opened 50 short control processes rather than one per individual command.

All three mature crops replanted using actual ordinary generated loot in the observed rolls; inventory remained at nine planting items each. The ground held three carrots, three potatoes, and one beetroot plus one beetroot seed respectively, after each crop reserved one planting item. Beetroot's normal-loot test permits inventory fallback if a future roll has no seed, but this particular roll did not exercise that path. Immediate clicks on the young plants had no new payment or ground entities. Each crop also passed its last immature stage, exactly one-item inventory payment in a controlled empty-loot fixture, no-material removal, wrong-item rejection (including poisonous potato and beetroot root), unchanged farmland, and regrowth from an actual paid replant with accelerated random ticks (`250`, restored to `3`). This proves the random-growth path in that fixture, not default-speed elapsed growth. A wheat harvest and ordinary sweet/glow berry harvest passed as regressions.

The existing native build passed offline without reported warnings. Standalone Rust tests: **11 passed**; Python structural/verifier tests: **25 passed**; the read-only stage audit passed for the same three generated files and four declared hooks. The baseline check confirmed all **3,570** pristine source files unchanged. No game assets or isolated worlds were staged in Git.

## Not covered by this batch

Default-speed growth timing, new per-crop paired Fortune/Silk Touch loot comparisons, exhaustive hand/tool/protection variants, save/reopen and disabled/removal retests for the new version, third-party cancellation, LAN and dedicated compatibility. Earlier wheat evidence remains scoped to `dev.2` in [wheat-validation.md](wheat-validation.md), not relabelled as freshly run `dev.3` evidence. The grouped testing policy is in [development.md](development.md#efficient-test-batches-approved-2026-10-30).
