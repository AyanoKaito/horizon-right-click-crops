# Sweet and glow berry validation

Version: `0.1.0-dev.8`. Sweet berry bushes and glow-bearing cave vines intentionally remain outside the mod's target profiles because Horizon already provides their right-click harvest interactions. This record verifies preservation on the final 18-family implementation stage; it does not add a second berry mechanic.

## Behavior

- A mature sweet berry bush uses Horizon's ordinary interaction, returns to age one and drops its ordinary berry roll. A repeat at age one does nothing.
- A cave-vine head with berries uses Horizon's ordinary interaction, clears its berries property and drops one glow berry. A repeat without berries does nothing.
- Bone meal remains an ordinary game interaction for both plants. The mod does not harvest, charge a planting item or duplicate loot while bone meal is held.

## Compact batch

`tools/test_berries.py` prepares both families in isolated creative setup, switches to survival and checks ordinary harvest state, ground loot, unchanged unrelated inventory, immediate empty repeat, and exact one-item bone-meal use. A wheat regression confirms that the paid-crop path remains active in the same final native build.

## Results

One final fresh default integrated-server run under `.local/runs/berries-final-retry-*` passed **7 recorded checks** and exited normally. Sweet berries produced one ordinary mature harvest, remained unchanged on the age-one repeat and grew after consuming exactly one bone meal. Glow berries produced one ordinary berry, remained absent on repeat and returned after consuming exactly one bone meal. Neither plant consumed the five unrelated seeds or produced a second harvest. The wheat regression passed.

The first run passed the initial sweet-berry harvest, then exposed an overly strict harness comparison: two ground item entities merged into one entity with the same total count during the repeat wait. The assertion now compares item totals, not transient entity IDs. No mod source, native stage or game binary changed. The final driver used 11 control processes. Detailed receipts and `berry-results.json` remain in ignored isolated data.

## Still unverified

Every berry age and Cave Vines body/head placement, external loot changes, default-speed growth timing, save/reopen, disable/removal on this version, multiplayer/dedicated operation and third-party cancellation.
