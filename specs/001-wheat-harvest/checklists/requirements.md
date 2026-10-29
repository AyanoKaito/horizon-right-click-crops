# Specification Quality Checklist: right-click wheat harvesting

**Purpose**: Review requirements quality before technical planning.

**Created**: 2026-10-29

**Feature**: [spec.md](../spec.md)

**Reviewer**: Agent, revised-draft review. Checked items indicate document quality, not completed gameplay tests, user approval of the whole revision, or permission to implement.

## Content Quality

- [x] CHK001 Describes required behavior without selecting a language, library, internal method, or implementation structure.
- [x] CHK002 Focuses on player value, world integrity, and honest item costs.
- [x] CHK003 Uses understandable player scenarios and expected outcomes.
- [x] CHK004 Completes the mandatory template sections.

## Requirement Completeness

- [x] CHK005 No unresolved clarification markers remain; held-click behavior is approved in FR-017 and AS-21.
- [x] CHK006 Requirements are testable and unambiguous within the survival prototype, including loot-first inventory fallback and no-material harvesting.
- [x] CHK007 Success criteria are measurable through item counts, crop state, and scenario outcomes.
- [x] CHK008 Success criteria do not depend on the selected implementation approach.
- [x] CHK009 Acceptance scenarios cover the functional requirements, including inventory payment, cancellation, and holding right-click.
- [x] CHK010 Edge cases include empty loot, both payment sources, incorrect items, two hands, denial, and a full inventory.
- [x] CHK011 Scope is bounded to survival wheat, with deferred source requirements preserved.
- [x] CHK012 Dependencies, setup privileges, natural-growth evidence, and unverified compatibility are explicit.

## Feature Readiness

- [x] CHK013 Every functional requirement has acceptance criteria; resolved FR-017 links to AS-02, AS-09, and AS-21.
- [x] CHK014 User paths cover loot-funded replanting, inventory fallback, no-material harvesting, ordinary interactions, persistence, and disabling.
- [x] CHK015 SC-001 through SC-007 define future outcomes without presenting them as existing test results.
- [x] CHK016 Product requirements do not select implementation details; inventory slot/access behavior and configuration mechanisms are reserved for technical inspection.

## Notes

- All 16 document-quality criteria pass the agent's revised-draft review. This is not a gameplay verification report.
- The user approved held-click behavior, inventory fallback, English-only GitHub content, creative preparation followed by survival execution, and the revised product specification as a whole on 2026-10-29. This is not approval to implement or run a native build.
- Creative/adventure harvesting, release crops, and settings format remain explicitly outside this survival prototype's unresolved implementation choices.
- Verify the exact seed source: generated loot first, inventory only when loot cannot pay, no seed from either source means successful harvesting without replanting. A denied/cancelled or losing multiplayer interaction must not charge inventory.
- Creative fixture setup and bone meal do not prove cheats-disabled/unprivileged operation or natural growth; report evidence separately.
- No gameplay code, native build, technical plan, implementation tasks, or executed gameplay scenarios exist yet. Do not automatically advance to another phase.
