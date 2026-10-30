# Retained-base vertical plant validation

Version: `0.1.0-dev.6`. Adds sugar cane, cactus and bamboo as one-column retained-base plants. This is implementation-in-progress evidence, not a release or final compatibility promise.

## Behavior

- Right-clicking any block in a connected supported column finds its lowest contiguous block, retains that base and harvests every block above it. A one-block plant passes through unchanged. Neighboring columns are not included.
- No planting item is consumed: the living base is already present. Each removed block uses Horizon's ordinary loot once with the held item; remaining items drop on the ground.
- Column writes run from top to bottom with ordinary neighbor/client updates and suppressed automatic plant drops, preventing a second copy beside the explicit loot. If a write unexpectedly fails, already changed plant blocks are restored before manual loot is spawned. This is best-effort rollback over the available non-transactional block API.
- The scan is explicitly limited to 32 contiguous blocks around the target. Natural bamboo is shorter and ordinary cane/cactus are much shorter; this bound prevents an unbounded malformed test column from turning one interaction into broad world work.

## Compact batch

`tools/test_vertical_plants.py` checks each family as one grouped survival fixture: retained base, one ordinary ground item per removed upper block, unchanged inventory, untouched neighboring column, no effect on the single retained base, a controlled drops-disabled column harvest, and accelerated regrowth. A short wheat regression guards the paid-crop path. Detailed receipts remain under ignored `.local/runs/` data.

## Results

The offline native build completed without reported warnings after one compile-only type annotation correction. Twelve standalone Rust tests, 25 Python tests and the read-only AST audit passed.

One fresh default integrated-server run under `.local/runs/vertical-plants-*` passed **13 recorded checks** and exited normally. For each family, clicking the top of a prepared column retained the lowest block, removed every block above it, produced exactly one ordinary ground item per removed block, left five unrelated inventory seeds unchanged and did not touch a separate neighboring column. Clicking the lone retained base produced no new items or state change. A drops-disabled middle-block click still harvested the connected upper column without inventing loot.

Each retained base grew a new block using random ticks at fixture speed `1000` during 1,200 game ticks; the rule was restored to `3`. This verifies regrowth mechanics, not default-speed elapsed growth. A wheat regression passed. Detailed JSONL receipts and `vertical-plant-results.json` remain in ignored isolated data; the driver used 31 control processes. All 3,570 pristine upstream source files remained unchanged.

## Still unverified

Cactus flowers attached to harvested growth, every bamboo leaf/stage combination, pathological columns above the scan bound, paired tool/control comparisons, default-speed elapsed regrowth, save/reopen, disable/removal, multiplayer/dedicated operation and third-party cancellation.
