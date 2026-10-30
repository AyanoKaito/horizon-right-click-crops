# Foundation-only tasks

Scope approved by the user: prepare the harmless native foundation files and structural checks, without downloads, compilation, or game launch. This is not the complete wheat implementation task list.

- [x] F001 Create the dependency-free Cargo library metadata and shared runtime source.
- [x] F002 Declare the exact Horizon pin, explicit Mixins candidate, and non-cancelling registration/observation hooks.
- [x] F003 Write four Rust unit tests without running a native compilation.
- [x] F004 Run structural Python checks and document their actual result.
- [x] F005 Resolve the bundle against the exact game source and inspect the generated diff after acquisition is approved.
- [x] F006 Compile and run Rust/native checks only after explicit build approval.
- [x] F007 Verify registration, logging, unchanged interactions, and disabling in an isolated game after launch approval.

F005-F007 are approval/verification gates, not authorizations. No loot, inventory payment, crop mutation, client capability exchange, or gameplay implementation is included in this slice.

The user approved missing source/tool downloads, compilation, and Rust tests, then separately approved the game smoke test. F005 passed against the real pin: three hooks, one support module, exactly two changed source files, all 3,570 pristine files unchanged, and canonical parsed Rust syntax preserved after removing only the declared additions. F006 passed after correcting the observer to use the actual `crate::game::Hit`: four standalone runtime tests, four audit-tool tests, the native game build, and the four embedded runtime tests passed. The other 159 upstream binary tests were filtered out.

F007 passed for the harmless foundation on the default integrated server: native row ON, startup log, an actual survival right-click on mature wheat with the plant and empty inventory unchanged, then UI OFF, full process restart, and another click with zero foundation log lines. The saved crop persisted, and test processes exited gracefully. This does not prove harvesting, exact farmland-state preservation, immediate live toggling, no-cheat/non-OP operation, in-frame parity, or multiplayer. See [the validation record](../../docs/native-validation.md).
