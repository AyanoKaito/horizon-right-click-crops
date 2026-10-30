# Pumpkin and melon validation

Version: `0.1.0-dev.8`. Adds stem-associated pumpkin and melon fruit. This is implementation-in-progress evidence, not a release or final compatibility promise.

## Behavior

- A pumpkin or melon is a harvest target only when one horizontal neighbor is the matching attached-stem block and its facing property points to that fruit. Arbitrary decorative fruit is left to ordinary interaction.
- Successful right-click removes only the fruit, runs Horizon's ordinary loot once and leaves the attached stem to Horizon's ordinary shape update. The stem becomes its mature unattached age-seven state. No seed or inventory item is charged.
- A pumpkin is not intercepted when either hand holds shears. Horizon's existing pumpkin interaction remains responsible for carving direction, carved state, seed loot, sound, tool damage, statistics and game events.
- Automatic break drops are suppressed on the explicit fruit write, preventing duplication beside the manually spawned ordinary loot. Loot is spawned only after the write succeeds.

## Compact batch

`tools/test_stem_fruits.py` checks linked pumpkin and melon harvest with ordinary ground loot, preserved mature stems and unchanged unrelated seeds; unassociated decorative fruit; drops-disabled linked harvest; ordinary pumpkin carving with shears; accelerated fruit regrowth and stem reattachment; and a wheat regression. Fixture growth leaves only the harvested fruit position with valid supporting ground so the random mature stem can attach only to the expected replacement fruit.

## Results

The offline native build completed without reported warnings. Thirteen standalone Rust tests, 25 Python tests and the read-only AST audit passed.

One final fresh default integrated-server run under `.local/runs/stem-fruits-fixture-floor-*` passed **10 recorded checks** and exited normally. A linked pumpkin produced one ordinary pumpkin item; a linked melon produced an ordinary random roll of melon slices. Both fruits were removed, their attached stems became mature age-seven stems, and five unrelated seeds remained unchanged. Unassociated decorative pumpkin and melon blocks passed through without loot or mutation. Drops-disabled linked fruit still disappeared while preserving its stem and created no items.

With shears held, an ordinary pumpkin bypassed the mod, became a carved pumpkin and produced pumpkin seeds through Horizon's existing carving path. The shears stack remained present. The harvested mature pumpkin and melon stems later generated replacement fruit and returned to their matching attached-stem states using random tick speed `1000` during 1,600 fixture ticks; the rule was restored to `3`. This verifies the growth path, not default-speed elapsed timing. A wheat regression passed.

The first four partial runs each passed the two linked-fruit scenarios and progressively corrected only fixture sightlines around the carving/decorative fields: a stem or uncleared terrain blocked the control camera. No mod source or native rebuild changed after the successful build. Detailed receipts and `stem-fruit-results.json` remain in ignored isolated data. The final driver used 18 control processes, and all 3,570 pristine upstream source files remained unchanged.

## Still unverified

All four stem directions, pumpkin shears in the offhand, melon Silk Touch/Fortune variants, default-speed elapsed fruit growth, competing valid fruit positions, save/reopen, disable/removal, multiplayer/dedicated operation and third-party cancellation.
