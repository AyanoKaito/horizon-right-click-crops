# Nether wart and cocoa validation

Version: `0.1.0-dev.4`. Adds two plant profiles to the existing paid-replant core without changing Horizon or Mixins revisions, adding hooks, enabling multiplayer, or modifying ordinary game resources. This is grouped partial validation, not a public release.

## Behavior

- Nether wart matures at age 3, pays with one nether wart and retains soul sand. Cocoa matures at age 2, pays with one cocoa bean and retains its attached log and direction.
- The existing `with_props` adapter clones the actual state and replaces only `age`; cocoa's `facing` is not reset. The world's direction-sensitive `can_survive` checks the attachment before loot, payment or world writes. The wart profile explicitly requires soul sand. Unripe plants pass through unchanged.
- Generated loot is used once, before inventory fallback. Missing material means a real harvest without replanting. Offhand bone meal remains untouched by the mod; the first four field crops continue to use farmland.

## Compact batch

`tools/test_wart_cocoa.py` uses the existing `Batch` transport from `tools/test_field_crops.py`, with a running isolated test session and scripted control phases. For each new plant: normal loot-first harvest and ground drops, immediate immature repeat, last immature stage, controlled empty-loot inventory payment, no material, wrong item, retained support and cocoa facing, and accelerated random-tick regrowth from a paid replant. Wheat and ordinary sweet-berry harvesting receive a short regression. Detailed JSONL replies and an outcome summary remain under the ignored `.local/runs/` fixture.

An ordinary loot roll for cocoa should yield three beans, of which one is reserved for replanting; mature wart ordinarily yields two to four and reserves one. These are expectations from the pinned resource tables, **not** hard-coded gameplay loot. Empty-loot cases use a clearly separate test rule; accelerated growth is not evidence of ordinary elapsed growth time.

## Results

The offline native build completed without reported warnings. Eleven standalone Rust tests, 25 Python structural/verifier tests and the read-only AST audit passed. The audit preserved the same three original generated files around four declared hooks and two support modules; all 3,570 pristine source files remained unchanged.

One fresh default integrated-server run under `.local/runs/wart-cocoa-*` passed **16 recorded checks** and exited normally. Both plants used generated loot before the unchanged inventory: the observed wart roll left one nether wart on the ground after reserving one, and cocoa left two beans after reserving one. Soul sand, jungle-log attachment and cocoa's east-facing state remained intact. Immediate young-plant repeats, the last immature stages, exact one-item inventory fallback, no-material removal, wrong-item rejection, and accelerated random-tick regrowth from actual paid replants passed. The test restored random tick speed from `250` to `3`. Wheat and ordinary sweet-berry regressions passed.

Detailed scripted replies and `wart-cocoa-results.json` remain in the ignored isolated run. The grouped driver used 34 control processes rather than one for every individual command. No installed resource, ordinary save or upstream source was modified.

## Still unverified

Individual paired control-game loot/enchantment runs for these plants, all hand/permission variants, default-speed elapsed growth, save/reopen and disable/remove on this version, non-OP multiplayer, dedicated server, third-party cancellation, and compatibility with other revisions. Earlier [wheat](wheat-validation.md) and [field-crop](field-crop-validation.md) evidence remains tied to its recorded version and inputs.
