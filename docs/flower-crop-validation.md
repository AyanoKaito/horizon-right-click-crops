# Torchflower and pitcher crop validation

Version: `0.1.0-dev.5`. Adds the two unusual cultivated flower families to the paid-replant core. This is work-in-progress grouped validation, not a public release.

## Behavior

- A mature torchflower is a different block from its growing crop. The mod handles it only over farmland, obtains ordinary flower loot once, and creates an age-zero `torchflower_crop` only after paying one real torchflower seed from loot or inventory. Decorative torchflowers on other support remain ordinary interactions.
- A mature pitcher crop has synchronized lower and upper age-four halves. Clicking either half resolves to the lower half, evaluates loot once, pays at most one pitcher pod and removes the upper half before leaving one age-zero lower crop. Decorative `pitcher_plant` blocks are not crop targets.
- Both families preserve farmland. Missing planting material still harvests the mature plant and drops the complete ordinary flower/plant product. Immature crop blocks pass through unchanged.
- The two-block write is checked before payment or loot spawning. It removes the upper half first with client notification but suppressed drops and intermediate shape updates, then changes the lower half with ordinary full updates. If changing the lower half unexpectedly fails, the adapter attempts to restore the original upper state and produces no payment or manual drops. This is a best-effort rollback around Horizon's non-transactional block API, not a claim of a general world transaction.

## Compact batch

`tools/test_flower_crops.py` uses one isolated running game. For both families it checks ordinary non-seed loot with exact inventory payment, immediate young-plant repeat, immature passthrough, no-material harvest, wrong-item rejection and accelerated natural regrowth from an actual paid replant. Pitcher additionally checks an upper-half click for one loot calculation, one payment and no stale upper half. Wheat receives a short regression. Raw control receipts remain in the ignored run directory.

## Results

The first game batch passed eight recorded scenarios, then exposed a real two-block ordering defect in the pitcher no-material case: changing the lower half first made Horizon remove the upper half automatically, so the subsequent explicit upper write reported no change and triggered the adapter's rollback. No payment or loot escaped, but the lower mature half remained. Reordering the writes fixed that outcome, but the next fresh batch found two pitcher-plant drops in the normal paid case: removing the upper half with ordinary full updates generated an additional shape-removal drop besides the one explicit lower-half loot calculation. Upper removal now suppresses that technical drop as described above. A later fresh batch passed all 11 harvest/payment/structure scenarios and fully grew pitcher, but torchflower reached only age 1 of 2 during the fixed random observation.

The final fresh default integrated-server run under `.local/runs/flower-crops-pass-*` passed **14 recorded checks** and exited normally. Torchflower and pitcher each passed ordinary product loot with exact inventory replanting, immediate young-crop repeat, immature passthrough, no-material harvest and wrong-item rejection. Clicking the pitcher upper half produced exactly one pitcher plant, consumed one pod and left one age-zero lower crop with no stale upper half. A wheat regression passed.

Both actual paid replants grew through random ticks: torchflower became the mature flower block and pitcher became synchronized age-four lower/upper halves. This final fixture used random tick speed `1000` for 1,200 game ticks and restored `3`; it proves the growth path, not default-speed elapsed time. Detailed scripted replies and `flower-crop-results.json` remain in the ignored isolated run. The driver used 30 control processes.

The offline build completed without reported warnings. Eleven standalone Rust tests, 25 Python tests and the read-only AST audit passed. The partial earlier batches are retained as defect evidence, not counted as the final pass. All 3,570 pristine upstream source files remained unchanged, and no installed resource or ordinary save was modified.

## Still unverified

Default-speed elapsed growth, paired control-game loot/tool comparisons, every hand/permission combination, save/reopen and disabled/removal on this version, unexpected second-write failure injection, multiplayer/dedicated operation, third-party cancellation and other Horizon revisions.
