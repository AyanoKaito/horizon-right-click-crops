# Wheat prototype: technical planning research

**Date:** 2026-10-29

**Status:** Read-only source research. Recommendations below are proposals for approval, not selected release compatibility, compilation results, or a completed implementation plan.

## Source snapshots

- Initially inspected Horizon `c7065027b15eee8e61a2bef653ea9c8f38a578c6`, then compared the relevant methods against published Nightly source `64e298952d8bbb1188108bd4de68be2ab25d202b`.
- The proposed reproducible baseline is the latter, retained by tag `nightly-source/2026-10-29-64e2989`. The moving `nightly` tag is not a dependency pin. This is not necessarily the user's installed build.
- Inspected horizon-mixins `3f99a5c60dfa311cc365524c44ae2fd799bfa1de`, the launcher's default `0d6b103c70633d8fd9443d8d0acd3aadaacedb06`, and native template `c8bfba72fb3c1f495d491d580e72cca7ae81de68`.
- Read the repositories' root agent instructions and Horizon's contribution rules. On the proposed Nightly, instructions still request both default server-thread and in-frame comparison checks; the initially inspected newer main snapshot instead deprecates in-frame. Follow the instructions at the revision actually selected, not a mixture of revisions.

## 1. Native integration requires a revision pin

**Evidence:** [native guide](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/docs/native-mods.md) and [native_hooks.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/native_hooks.rs).

`NATIVE_HOOKS_API` is 2. Its stable functions cover tick/frame/input, HUD, settings, and recipe panels; the inspected API has no authoritative block-use/crop-loot operation for this mechanic. `native_give` is creative-only and is not an acceptable substitute.

**Proposed decision:** Use direct, narrowly scoped mixin hooks and an exact Horizon revision for the first proof. Do not label the package as relying only on stable hook API 2 or promise compatibility with later Nightlies.

**Alternatives:** Request a new stable gameplay hook upstream (separate work and approval), or wait for one. Extending the WASM API first is not the approved project direction.

## 2. Authoritative interaction entry point exists

**Evidence:** [game.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game.rs) and [lan_actions.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/lan_actions.rs).

- `Game::use_hand` begins at line 4349 of the proposed baseline; `use_item_as_player` selects the relevant hand(s).
- `UseItemOn` handling starts at line 1178 of `lan_actions.rs`. Reach/hit validation, spawn protection, and world-border checks precede the acting player's `use_item` call.
- `as_guest`/`enter_guest` swap the acting player's inventory, offhand, selected slot, and game mode into `Game`; the hook must operate on this context rather than a cached owner inventory.
- The integrated server uses this network-style path even in ordinary single-player. A mouse-only implementation or an in-frame-only demonstration is insufficient.

**Proposed decision:** Evaluate a cancellable HEAD hook on `Game::use_hand`, restricted to actual block-use context and a mature supported crop. Continue the original function for disabled behavior, unsupported targets, immature wheat, bone meal, and modes not approved for mod harvesting. Return a handled outcome only for the mod's actual harvest path. Do not intercept the packet handler before its existing permission checks.

**Remaining proof:** Rust borrowing/privacy, exact context guards, block-state updates, and the interaction's complete effect sequence require a small staged compile/test proof. Reading source is not that proof.

## 3. A client-side consumption hint may also be necessary

**Evidence:** [remote.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/remote.rs): `remote_use_item_on` at line 4862, `remote_block_reacts` at line 5037, and `remote_use_item` at line 5161.

The client sends `UseItemOn` and, when its ordinary prediction says the block did not handle the click, can send item-use and offhand actions. Merely changing the server crop can therefore leave unwanted client fall-through, including held-item use. This affects default single-player, not only external multiplayer.

**Proposed decision:** Evaluate a second narrowly scoped hook in `remote_block_reacts` to classify a supported mature harvest target as a handled block interaction, with no predicted crop change, loot generation, or inventory payment. The original sender must still send the authoritative `UseItemOn` packet. Do not cancel `remote_use_item_on` before it sends the packet.

**Boundary:** Enable this hint only when the client knows the matching integrated server has the mechanic enabled. Do not suppress ordinary interactions on unrelated external servers. Capability/enablement agreement, two-hand bone meal priority, and disabled-state consistency are explicit spike gates, not assumed solved. Do not advertise server-only installation without testing an unmodified client.

## 4. Loot and inventory can use real game state

**Evidence:** [game.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game.rs), [shield.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/shield.rs), and [lan_actions.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/lan_actions.rs).

- `block_loot_at` at line 2635 evaluates actual player/tool-aware block loot and uses Horizon's loot random sequence; call it once, not once for preview and again for output.
- `pop_resource` at line 2660 provides normal ground item spawning. Do not also invoke ordinary crop breaking with drops.
- The inventory has 36 regular slots; offhand is separate. `stack_in`/`stack_in_mut` access a regular slot or offhand. `consume_held` only consumes the acting hand and skips creative; it is not a generic arbitrary-slot fallback operation.
- The crop helpers `crop_max_age` and `crop_state_for_age` in [bonemeal.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-world/src/level/bonemeal.rs) are `pub(crate)` inside `horizon-world`. A helper injected into `horizon-client` cannot directly call them as public APIs.

**Proposed decision:** Keep a testable payment-selection core independent of game resources, with one typed game adapter. Select exactly one payment source: generated wheat seed, inventory wheat seed, or no replant. Preserve all original stack metadata when returning remaining loot. Do not manually reconstruct loot tables or copy another harvest mod's code.

**Proposed inventory boundary for review:** Regular inventory/hotbar plus offhand, with deterministic selection; exclude armor, crafting grids, cursor stacks, open containers, and nested container contents. Confirm ordinary usable seed semantics and exact slot ordering before implementation.

**Remaining proof:** Inspect and test the public block-state/property and normal world-update path at the selected pin; do not invent an accessor for the private crop helpers. Validate/revalidate the target and inventory payment before publishing effects, then keep commit effects in the authoritative action without a yield. Demonstrate that cancellation cannot consume a seed or produce partial loot; do not assume a general transaction API exists.

## 5. Mixins/tooling pins cannot be copied blindly

**Evidence:** [launcher native_mods.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/launcher/src/native_mods.rs), [current Mixins boundary support](https://github.com/horizon-rust/horizon-mixins/blob/3f99a5c60dfa311cc365524c44ae2fd799bfa1de/docs/boundary-head-and-modules.md), [launcher-default boundary support](https://github.com/horizon-rust/horizon-mixins/blob/0d6b103c70633d8fd9443d8d0acd3aadaacedb06/docs/boundary-head-and-modules.md), and [template compatibility](https://github.com/horizon-rust/horizon-native-mod-template/blob/c8bfba72fb3c1f495d491d580e72cca7ae81de68/compatibility.json).

- The launcher defaults to Mixins `0d6b103...`, version 0.5.0. Its inspected boundary guide rejects source macros. The inspected newer `3f99a5c...` documents HEAD-only preservation of body macros, including cancellable HEAD, which matters for macro-bearing gameplay methods.
- Propose explicitly pinning `3f99a5c60dfa311cc365524c44ae2fd799bfa1de` rather than relying on the launcher's older default. This is a source-based candidate, not verified Windows compatibility of this exact pair.
- The template pins Horizon `028f608...` and Mixins `0500ff2...`, and its staging scripts are Linux-oriented. Use its small shared-runtime/adapters pattern as a reference, not as proof that unchanged scripts work on Windows or on the proposed Nightly.
- The inspected launcher documents its own isolated Rust 1.99.1/MinGW toolchain on Windows. Do not install a global Rust toolchain or Visual Studio as an unexamined prerequisite.

## 6. Disabling and multiplayer have separate gates

**Evidence:** [native hooks](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/native_hooks.rs) expose `native_mods` and `native_on`; [integrated.rs](https://github.com/horizon-rust/horizon/blob/64e298952d8bbb1188108bd4de68be2ab25d202b/crates/horizon-client/src/game/integrated.rs) clones settings when starting the server thread.

Propose using Horizon's mod listing/disable state, initially with a documented world restart rather than promising live synchronization. Prove both authoritative behavior and the client's consumption hint agree after disabling. Do not build a new settings framework or silently claim a client toggle changes server state immediately.

The native guide explicitly says the launcher does not yet build dedicated native servers. Dedicated support remains a goal with a separate pipeline/test gate, not an advertised capability of the first spike.

## Validation actually performed

- Read public source and documentation at immutable commits; checked availability of the retained Nightly source tag.
- Compared relevant methods from the initial main snapshot with the proposed Nightly. The key interaction/loot/client methods matched; instructions and some surrounding code differed and were checked at the candidate pin.
- No toolchain installation, source checkout, mixin planning/application, Rust compilation, game launch, player-data access, gameplay test, upstream patch, or public message was performed.

## Approval and completion boundary

Research supports proposing the staged approach in [plan.md](plan.md), but does not establish a completed Phase 1 design. Final pins, capability/disable agreement, safe world mutation, inventory slot policy, and Windows compilation remain gates. Do not generate a supposedly runnable quickstart or implementation task list until those gates are addressed and the user approves the next step.
