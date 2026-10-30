# Implementation Plan: wheat prototype foundation

**Branch**: `main` | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Current status (2026-10-30)**: The user accepted the foundation and authorized proceeding with wheat implementation. Exact pins, native compilation and an isolated foundation game launch were approved and completed. The bounded [integration contract and tasks](contracts.md) now govern gameplay implementation. See [wheat validation](../../docs/wheat-validation.md) for current checks. The proposal text below is retained as planning history; its earlier pending gates must not be mistaken for current results.

**Progress**: The user approved the staged order and starting isolated environment preparation. Launcher CLI version 0.2.26 is confirmed and an empty isolated `wheat-prototype` instance exists; see [environment checks](../../docs/test-environment.md). Milestone 1 is not complete: the exact candidate pins, downloads, and native execution trust still require agreement. No later milestone has started.

**Existing-cache correction**: Read-only inspection subsequently confirmed the ordinary installation already contains Rust/Cargo 1.99.1, MinGW, Mixins `0d6b103...`, dependency/build caches, a native game build, and the candidate Nightly game/resource directory. The isolated empty cache must not be mistaken for a missing host installation. Propose safe reuse and download only missing components; do not duplicate the full launcher environment by default. No existing-cache links/copies or build-path changes have been made.

**Foundation preparation update**: The user approved writing the harmless foundation source for installed Nightly `64e2989`, with no downloads, compilation, or game launch. The files and [foundation-only task record](foundation-tasks.md) now exist; [foundation documentation](../../docs/native-foundation.md) records 15 passing structural Python checks and four unexecuted Rust tests. Milestone 2's actual compile/launch proof remains incomplete. No harvesting or complete gameplay task list has been implemented.

**Input**: Approved wheat product specification, full requirements R01-R28, and [pinned-source research](research.md).

## Summary

Propose a small revision-pinned native Mixins bundle, a game-independent payment-selection core, and typed adapters for authoritative block interaction and client click consumption. Preserve normal loot, inventory payment rules, bone meal, farmland, and held-click behavior. First prove a harmless native foundation in an isolated Windows instance; do not start by implementing the entire mechanic or importing the Linux template tooling unchanged.

## Technical Context

**Language/Version**: Rust for all player-executed code. Candidate native build toolchain: the launcher's isolated Rust 1.99.1/Windows GNU setup, not a new global installation. Confirm the installed launcher before choosing actual commands.

**Primary Dependencies**: Proposed Horizon `64e298952d8bbb1188108bd4de68be2ab25d202b` (`nightly-source/2026-10-29-64e2989`) and Mixins `3f99a5c60dfa311cc365524c44ae2fd799bfa1de`. These are candidates for review and a compile spike, not approved compatibility targets. No new third-party runtime dependency is proposed.

**Storage**: No custom crop/save format. Use ordinary world and player inventory state. Propose existing Horizon mod enablement with a documented world restart until synchronized behavior is proven. No new configuration framework or guaranteed live toggle.

**Testing**: Pure payment/core tests; minimal source-transform/compile proof; integration checks of both authoritative actions and client consumption; isolated gameplay acceptance AS-01 through AS-24. Controlled absent-seed fixtures remain tests, not altered runtime loot.

**Target Platform**: First proof on Windows, default single-player integrated server. LAN and dedicated support remain separate goals. At the proposed pin, upstream also requests in-frame comparison checks; these do not replace default server-thread proof. The launcher does not yet build dedicated native servers.

**Project Type**: Independent native source-mixin bundle with a small testable Rust library, not a WASM mod and not an upstream built-in harvesting feature.

**Performance Goals**: No per-frame world scans, area harvest, or custom held-input loop. Work only on a relevant target interaction; generated loot is evaluated once and inventory fallback is bounded by ordinary player slots. No unmeasured latency/FPS claim.

**Constraints**: English-only tracked/GitHub content; Russian local review only; isolated homes and saves; explicit native-code trust; exact source/tool pins; pending own-code license; no borrowed harvest-mod gameplay or Minecraft resources; no cheats/OP in the harvesting path.

**Scale/Scope**: Wheat only, survival harvest, ground loot, one paid replant, no-material harvest without replanting, ordinary bone meal and left-click, held input across separate targeted plants.

## Constitution Check

The principles document is still a draft, not separately ratified. The user's explicit requirements apply regardless.

- Scope and item-accounting rules: proposal follows the approved specification; no feature expansion.
- Native direction: retained; exact pin and hooks are presented for approval rather than adopted silently.
- Safety and trust: read-only research performed; no native build, global installation, or real-save access.
- Honest validation: source evidence is distinct from compile/gameplay proof; dedicated support is not promised.
- Language/licensing/publication: tracked artifacts are English; local review is ignored; license and publication gates are preserved.
- **Gate status**: passes for a research/proposal artifact only. Implementation is blocked pending plan approval, revision/tool selection, inspection of the safe world-update path, enablement/capability agreement, and explicit build trust. Do not describe the full Spec Kit plan workflow or Phase 1 as completed.

## Project Structure

### Documentation (this feature)

```text
specs/001-wheat-harvest/
  spec.md                   approved product behavior
  plan.md                   this proposal
  research.md               pinned evidence and unresolved proof gates
  checklists/requirements.md product-specification quality review
```

`data-model.md`, `contracts/`, `quickstart.md`, and `tasks.md` are deliberately deferred. A runnable guide must not invent commands or claim a working integration before the spike gates are settled.

### Proposed source layout (not created)

```text
Cargo.toml
Cargo.lock
compatibility.json
mixins/right-click-crops/
  horizon-mixin.toml
  runtime.rs
  use_hand.rs
  client_reacts.rs
```

**Structure proposal**: Keep item-payment selection in a small standalone-testable portion of `runtime.rs`, shared with the injected support module. Keep typed game bindings in thin adapters. Inject no unrelated Cargo dependencies and avoid game/mod dependency cycles. Retain third-party MIT notices if template material is later adapted. The project's own license remains undecided.

## Proposed milestones and review gates

### 1. Confirm the isolated baseline

Obtain the installed launcher version and confirm how an isolated instance/home will be selected. Check available disk/toolchain status without installing or building. Ask the user to approve the proposed retained Nightly and Mixins pair, or inspect their working Nightly instead. Initially use only this mod, not an untested mixture of other pinned mods.

**Exit**: Agreed source/tool pins, instance/data paths, expected downloads and native-build trust boundary. No modification to the user's ordinary installation or saves.

### 2. Prove a harmless native foundation

After approval, introduce only a no-op/logging hook at the proposed boundary and a tiny standalone core fixture. Validate target resolution, module privacy/borrowing, supported macros, deterministic staging, and an untouched original source export. A successful Mixins plan alone does not establish compilation.

Before native code is executed, obtain explicit trust for the exact build step. Use the launcher's isolated toolchain or an approved equivalent; do not silently execute the Linux template's staging script on Windows. Confirm baseline launch and mod registration/disable behavior on isolated data.

**Exit**: Reproducible successful compile and safe launch, with no crop mutation and a clear report. Stop for review before adding gameplay logic.

### 3. Finalize the small wheat integration design

Resolve the spike questions from research before implementing the mechanic: ordinary block-state/neighbor update path, inventory matching and safe one-item consumption, bone meal/two-hand ordering, client/server enablement agreement, cancellation and duplicate handling. Draft data-model and interaction contracts at that point.

Candidate integration: authoritative cancellable HEAD at `Game::use_hand`; client-side consumption hint at `remote_block_reacts` only for a known matching enabled world. The latter must not suppress the original block-use packet or run world/inventory/loot effects. Do not use `native_give` or ordinary breaking plus a second loot spawn.

Proposed inventory policy for approval: 36 regular slots including hotbar, then offhand; deterministic first suitable stack, no armor/crafting/cursor/container/nested search. Charge inventory only when generated loot has no suitable seed. Finalize this in the technical contract before code.

**Exit**: Approved technical contracts and final implementation tasks. No assumption that a general transaction API exists or that an unmodified remote client can safely omit the mod.

### 4. Implement and accept wheat in small slices

Only after the previous review: core item accounting/tests, authoritative adapter, client consumption handling, then actual isolated gameplay. Build controlled no-seed cases for inventory fallback and no-material harvesting. Check unchanged tool/loot rules, bone meal, both hands, held clicks, world restart, and disabling/removal. Prepare fixtures in creative, perform harvest checks in survival, and verify natural growth separately.

**Exit**: Honest AS-01 through AS-24 report with actual versions, passed/failed/unperformed checks, and user acceptance of the single-player proof. LAN/two-player and dedicated proof remain separate before compatibility is advertised. No automatic public release or crop expansion.

## Stop conditions

- Missing/ambiguous hook targets, unsupported transforms, borrow/privacy failures, or an unproven world mutation path: stop and revise the design rather than patching Rust source by string replacement.
- Unknown external-server capability or mismatched enablement: do not apply the client consumption hint indiscriminately.
- Partial item/world changes, duplicated drops, or cancellation charging a seed: block gameplay acceptance.
- Exact candidate pair fails on Windows: report failure; do not silently change pins or promise another platform is equivalent.
- Need for new upstream hooks, network capability exchange, or a separate dedicated build: propose that work explicitly instead of hiding it inside the small mod.

## Complexity Tracking

No source-level complexity exemption is requested. The second interaction adapter is proposed only to prevent ordinary client fall-through; its necessity and safe activation must be demonstrated. A standalone server distribution, protocol extension, settings framework, and generic crop framework are not part of the initial foundation.
