# Kelp and Nether vine validation

Version: `0.1.0-dev.7`. Adds kelp, twisting vines and weeping vines to the retained-anchor adapter. This is implementation-in-progress evidence, not a release or final compatibility promise.

## Behavior

- Kelp and twisting vines grow upward, while weeping vines grow downward. Clicking either the head or body resolves the connected directed plant, retains the block nearest its support and harvests all growth outward from that anchor. Neighboring plants are not included.
- The retained body uses Horizon's ordinary shape update to become a new live head. The adapter does not manufacture a head state, planting item or free vine. Kelp's surrounding water is left to Horizon's ordinary fluid updates.
- Head and body blocks both use Horizon's actual loot calculation with the held tool. No planting item is charged. Removal runs from the far tip back toward the retained anchor with automatic drops suppressed, so explicit ordinary loot is the only source.
- The existing 32-block scan bound applies in both directions. Natural head age limits these plants to shorter growth; the bound prevents malformed fixture columns from turning one click into unbounded work.

## Compact batch

`tools/test_kelp_vines.py` prepares valid isolated columns and exercises them in survival. For each family it checks a live retained head, exact shears-aware loot for two removed blocks, unchanged shears/inventory, an untouched neighboring plant, no effect from clicking the lone anchor, a drops-disabled middle-body harvest and accelerated outward regrowth. The kelp checks additionally require water in the removed positions. A short wheat regression guards the paid-crop path.

## Results

The offline native build completed without reported warnings. Twelve standalone Rust tests, 25 Python tests and the read-only AST audit passed.

One final fresh default integrated-server run under `.local/runs/kelp-vines-final-*` passed **13 recorded checks** and exited normally. For each family, clicking a three-block plant retained the support-side block as a live head, removed the two outward blocks, left the shears unchanged and produced exactly two ordinary shears-aware items on the ground. A separate neighboring plant remained intact. Clicking the lone retained head had no effect, and a drops-disabled middle-body click harvested outward without inventing loot.

Kelp removal positions returned to water. Kelp and twisting vines regrew upward, while weeping vines regrew downward, using random tick speed `1000` during 1,200 fixture ticks; the rule was restored to `3`. This verifies directed growth, not default-speed elapsed timing. A wheat regression passed after explicitly clearing the fixture's upper water volume.

The first attempted batch stopped before survival action because the test selected hotbar slot `0` although the control API uses `1..9`. A later partial run showed that the player needed a fixture floor for the downward-vine wait, and another passed all 12 new scenarios before leftover upper water invalidated only the wheat sightline. These were harness defects; no mod source or native rebuild changed after the successful build. Detailed receipts and `kelp-vine-results.json` remain in ignored isolated data. The final driver used 29 control processes, and all 3,570 pristine upstream source files remained unchanged.

## Still unverified

Unenchanted probabilistic vine loot, Fortune and Silk Touch variants, default-speed elapsed growth, every head age, malformed columns at the scan bound, save/reopen, disable/removal, multiplayer/dedicated operation and third-party cancellation.
