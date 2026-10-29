# Feature Specification: right-click wheat harvesting

**Feature Branch**: `main` - no separate documentation branch was created.

**Created**: 2026-10-29

**Status**: Product specification approved by the user on 2026-10-29. Technical planning, implementation, native builds, and public releases remain separate approval gates.

**Input**: Harvest mature wheat with right-click in survival. Drop loot on the ground. Replant using one wheat seed from generated loot first, otherwise from the player's inventory. If neither source can pay, harvest without replanting. Preserve bone meal behavior. Holding right-click may harvest successive targeted mature plants. Creative preparation of isolated test fields and supplies is allowed; exercise harvesting in survival.

**Sources**: [full requirements R01-R28](../../docs/requirements.md), [decisions](../../docs/decisions.md), and [draft principles](../../.specify/memory/constitution.md). This specification selects the first prototype, not a replacement for the full requirements. Disagreements require review, not silent changes to the sources.

## User Scenarios & Testing *(mandatory)*

All scenarios below are future checks, not completed gameplay tests. Use isolated test data, never real saves. P1 is mandatory for prototype acceptance. P2 is mandatory before advertising the corresponding multiplayer support.

### Test setup and execution

Creative mode and commands may supply farmland, crops, tools, seeds, and bone meal. Bone meal may mature crops quickly for harvest checks. Switch the acting player to survival before checking the mechanic and record starting inventory counts; no OP action or cheat command may be part of harvesting itself. Reset and record each fixture so automatic item pickup or seeds left from another case do not hide payment errors.

Preparation privileges do not prove runtime privileges. Record whether the actual check used a cheats-disabled world or an unprivileged player before making that claim. Creative/adventure harvest behavior is not decided by allowing creative preparation.

Natural growth must be verified separately from bone meal use. If it has not been observed, report it as untested rather than treating a bone-meal-grown fixture as evidence. If ordinary wheat always drops seeds in the selected version, use controlled tests for absent-seed loot; do not change ordinary gameplay loot or claim a controlled case occurred naturally.

### User Story 1 - harvest mature wheat and keep it planted (Priority: P1)

The player wants to harvest mature wheat with an ordinary right-click, without manually replanting it.

**Why this priority**: This is the mod's core benefit.

**Independent Test**: Inspect the crop, inventory, and ground drops after one click, then verify subsequent normal growth separately.

**Acceptance Scenarios**:

1. **AS-01 - Given** mature wheat and generated loot containing wheat seeds, **When** the player right-clicks without using bone meal, **Then** the crop returns to its initial stage on the same farmland, exactly one generated seed pays for replanting, and the remaining ordinary loot drops once on the ground. No inventory seed is charged.
2. **AS-02 - Given** the replanted immature wheat, **When** the player immediately right-clicks again or keeps holding right-click on it, **Then** no new loot appears, no seed is consumed from either source, and the mod does not reset growth.
3. **AS-03 - Given** replanted wheat and ordinary suitable growth conditions, **When** enough game time passes without bone meal or forced growth, **Then** it follows normal growth stages and reaches maturity again.
4. **AS-04 - Given** mature wheat, an empty used hand, and no inventory seeds, **When** the standing player right-clicks without crouching, **Then** AS-01 works if the loot contains a seed; neither a hoe nor an existing seed supply is required.
5. **AS-05 - Given** mature wheat and a full inventory, **When** harvesting succeeds, **Then** loot can still drop on the ground and replanting can use a seed from loot. Ordinary subsequent automatic pickup is not direct inventory delivery by the mod.
6. **AS-21 - Given** a row of mature wheat, **When** the player holds right-click and aims at successive plants while moving along the row, **Then** each targeted mature plant may be harvested through normal repeated interactions without releasing the button. Untargeted plants are not harvested, immature targets are not harvested again, and bone meal interactions remain ordinary.
7. **AS-22 - Given** both generated wheat seeds and wheat seeds in the player's inventory, **When** harvesting succeeds, **Then** exactly one seed from loot pays for replanting; inventory seed count is unchanged before any ordinary pickup.

### User Story 2 - use inventory seeds when the loot has none (Priority: P1)

The player wants an available suitable inventory seed to pay for replanting when the harvested crop produces none. Lack of planting material in both sources still must not cancel harvesting.

**Why this priority**: This is the approved fallback, without free seeds or a hidden double cost.

**Independent Test**: Use controlled loot without wheat seeds, first with a suitable inventory seed and then without one. Compare starting and ending inventory, the whole loot result, and the crop/farmland state.

**Acceptance Scenarios**:

1. **AS-06 - Given** mature wheat and no wheat seeds in either generated loot or inventory, **When** the player right-clicks, **Then** the crop is removed, the unchanged farmland is empty, and all generated loot drops on the ground. No seed is created. The same rule applies to an empty loot result.
2. **AS-07 - Given** generated loot with no wheat seeds but at least one wheat seed in inventory, **When** harvesting succeeds, **Then** exactly one inventory wheat seed is consumed, wheat is replanted at its initial stage, and all generated loot drops unchanged. This also applies to an otherwise empty loot result.
3. **AS-23 - Given** loot without a seed, an inventory seed, and an interaction that is actually denied or cancelled, **When** the interaction ends, **Then** no inventory seed is consumed, no loot drops, and the crop/farmland remain unchanged.
4. **AS-24 - Given** loot without wheat seeds and inventory or nearby ground items that are not an available inventory wheat seed, **When** the player harvests wheat, **Then** those items are not used. For example, beetroot seeds do not pay for wheat; absent a suitable inventory seed, AS-06 applies.

### User Story 3 - preserve ordinary actions and restrictions (Priority: P1)

The player continues using bone meal, planting, and breaking normally. The mod must not bypass game restrictions.

**Why this priority**: Convenience must not break existing actions, loot rules, or permissions.

**Independent Test**: Compare the same interactions with the mod enabled and disabled; run harvest assertions in survival even if the fixtures were prepared in creative.

**Acceptance Scenarios**:

1. **AS-08 - Given** immature wheat, **When** the player right-clicks, **Then** the mod does not harvest it or suppress available ordinary interactions.
2. **AS-09 - Given** mature or immature wheat, **When** the player uses bone meal, **Then** no mod harvest occurs; the game determines the ordinary result and bone meal cost.
3. **AS-10 - Given** mature or immature wheat, **When** the player breaks it with left-click, **Then** ordinary breaking occurs without mod replanting or a second loot result.
4. **AS-11 - Given** suitable empty farmland, **When** the player plants seeds normally, **Then** planting works as it does with the mod disabled.
5. **AS-12 - Given** a berry bush, glow berries, or any plant other than wheat, **When** the player interacts, **Then** this prototype adds no harvesting/replanting and does not change ordinary results, including existing berry harvesting.
6. **AS-13 - Given** an interaction outside permitted reach or denied by available area protection, **When** harvesting is attempted, **Then** the mod does not bypass the restriction: crop, farmland, and inventory remain unchanged and no loot is produced.
7. **AS-14 - Given** a tool or enchantment that affects ordinary loot in the selected version, **When** permitted harvesting occurs, **Then** the original loot rules apply, minus one suitable seed only when paid from loot. Inventory fallback does not reduce generated loot or add a bonus.

### User Story 4 - preserve the world and prevent duplicates (Priority: P1)

The player can save the world and disable the mod without damaging crops or creating extra items.

**Why this priority**: World integrity and honest item costs are mandatory even in the first prototype.

**Independent Test**: Check both hands, repeated processing, saving/reopening the test world, and disabling/removing the mod. Cover both replanting payment sources and the no-replant result.

**Acceptance Scenarios**:

1. **AS-15 - Given** one mature wheat plant, **When** one interaction is processed repeatedly or both hands participate, **Then** at most one successful harvest and one loot result occur, with at most one seed charged from one source. Legitimate held-click interactions with different mature targets remain allowed.
2. **AS-16 - Given** a completed harvest with a replanted crop or empty farmland, **When** the world is saved and reopened, **Then** the result persists without restoring the old mature crop, repeating loot, or repeating inventory payment.
3. **AS-17 - Given** the mod is disabled, **When** the player performs AS-01 or AS-08 through AS-12, **Then** the ordinary game behavior applies without the mod intervening.
4. **AS-18 - Given** a saved test world previously used with the mod, **When** it is opened with the mod disabled or removed in a compatible game version, **Then** crops and farmland remain available without world damage or mod-specific planting data requirements.
5. **AS-19 - Given** a harvest is genuinely cancelled by a permission check or an expected failure before completion, **When** the action ends, **Then** there is no partial crop, farmland, inventory, or drop result and no game crash. AS-06 is a successful no-replant harvest, not cancellation.

### User Story 5 - one harvest for two players (Priority: P2)

In multiplayer, simultaneous interactions must not produce two harvests from one mature crop.

**Why this priority**: This is mandatory before claiming LAN or dedicated-server support, which remains unverified.

**Independent Test**: Two players try to harvest one mature plant simultaneously, separately in each multiplayer environment to be advertised.

**Acceptance Scenarios**:

1. **AS-20 - Given** two players beside one mature wheat plant, **When** both right-click almost simultaneously, **Then** there is one loot result, at most one planting-item payment, and one consistent final crop state. A player whose harvest did not succeed is not charged an inventory seed. Subsequent messages must not trigger extra ordinary actions from a handled/cancelled interaction.

### Edge Cases

- Exactly one generated seed: it entirely pays for replanting; zero ground seeds is correct.
- Generated seeds and inventory seeds both present: generated loot pays, inventory does not.
- No generated seeds and exactly one inventory seed: consume it, replant, and drop the entire original loot.
- No suitable seed in either source, including zero generated loot: harvest without replanting; do not invent items.
- Seeds of another crop or items lying nearby do not pay for wheat. Future supported crops must use their own planting item under source R14, never poisonous potatoes.
- Ordinary automatic pickup may change later inventory counts; inspect payment and ground drops before pickup masks the result.
- Repeated or held clicks on immature replanted wheat do not reset growth or charge inventory seeds.
- Check bone meal on mature and immature wheat with ordinary hand-use ordering; using bone meal must not become a harvest.
- The harvest itself does not change farmland type or state. Later changes caused by ordinary world rules are not attributed to the mod.
- Creative/adventure harvest behavior remains undecided. Using creative to prepare a survival test does not approve or verify it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Provide wheat-only right-click harvesting in survival without cheats/administrative rights, crouching, or a required hoe. Acceptance: AS-01, AS-04. Sources: R01, R03, R05, R24.
- **FR-002**: Harvest only mature wheat; replanted wheat starts at the initial stage and grows normally. Acceptance: AS-01 through AS-03, AS-08. Sources: R06 through R08.
- **FR-003**: Use one ordinary loot result per successful harvest, including supported tool/enchantment effects, without invented fixed item counts. Acceptance: AS-01, AS-14, AS-15. Sources: R12, R17.
- **FR-004**: Pay exactly one wheat seed from generated loot first; only if it contains none, consume one available wheat seed from the player's inventory. Do not charge both sources, use the wrong crop item, or take nearby ground items. Acceptance: AS-01, AS-04, AS-07, AS-22 through AS-24. Sources: R06, R13, R14, R16.
- **FR-005**: If neither source has a suitable seed, complete harvesting without replanting: empty farmland, full generated loot, no free seed. Acceptance: AS-06, AS-24. Source: R15.
- **FR-006**: Drop remaining loot on the ground, not directly in inventory. Inventory-funded replanting leaves all generated loot intact and does not wait for pickup. Acceptance: AS-01, AS-05 through AS-07. Sources: R06, R13.
- **FR-007**: Preserve ordinary planting, left-click, and bone meal use; do not harvest immature plants. Acceptance: AS-08 through AS-11. Sources: R07 through R10.
- **FR-008**: Harvesting itself must not change farmland or its state, regardless of planting-item availability. Acceptance: AS-01, AS-06, AS-07, AS-16. Source: R11.
- **FR-009**: Do not change unsupported plants, including berries with existing harvesting. Acceptance: AS-12. Sources: R20 through R23.
- **FR-010**: Repeated processing, both hands, and rapid repetitions must not duplicate loot, double-charge planting items, or trigger an extra ordinary action. Acceptance: AS-02, AS-15, AS-23; multiplayer also AS-20. Sources: R16 through R18.
- **FR-011**: Respect reach, game mode, and available area-protection/permission checks, without requiring extra player rights. Survival acceptance: AS-04, AS-13, AS-23. Other-mode behavior requires separate agreement before implementation. Sources: R03, R18.
- **FR-012**: A cancelled or expected failed harvest has no partial world, drop, or inventory result and does not crash the game. Acceptance: AS-13, AS-19, AS-23. Source: R16.
- **FR-013**: Save/reopen preserves the completed crop, loot, and inventory result without replaying the harvest or seed payment. Acceptance: AS-16. Source: R19.
- **FR-014**: The mod must be disableable; disabled behavior does not interfere with the game. Disabling/removing it must not damage the test world. Acceptance: AS-17, AS-18. Sources: R24 through R27. The disabling mechanism and restart requirements must be documented when the technical approach is selected, not guessed here.
- **FR-015**: Do not add area harvesting, bonus loot, hunger/experience costs, or unrelated mechanics. Acceptance: AS-01, AS-14, AS-15, AS-21, also checking that those effects are absent. Sources: R01, R28.
- **FR-016**: Report single-player, LAN, and dedicated-server validation separately; one environment does not prove another. Multiplayer acceptance includes AS-20. Sources: R02, R16, R18.
- **FR-017**: Holding right-click and aiming at successive mature wheat plants may harvest each through normal repeated interactions without a fresh press, one targeted plant at a time. An immature target or a bone meal interaction must not be converted into a harvest. Acceptance: AS-02, AS-09, AS-21. Sources: R05, R07, R10, R28.

### Key Entities *(include if feature involves data)*

- **Crop**: mature wheat before harvesting; initial-stage wheat or no plant afterward.
- **Farmland**: the crop's supporting ground, unchanged by the harvest itself.
- **Generated loot**: one ordinary harvest result with applicable game modifiers, not a fixed custom item list.
- **Planting payment**: one suitable item from exactly one source, generated loot first or the player's inventory as fallback; none if replanting is impossible.
- **Player inventory**: an alternate planting-item source, whose available matching items and exact one-item consumption must be respected without taking unrelated items.
- **Player interaction**: target, used item, hand, and game permissions; held input can produce legitimate interactions with different targets but one interaction cannot create duplicate harvests.
- **Enabled state**: enabled behavior follows this specification; disabled behavior does not intervene. Its storage mechanism is not selected here.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For every loot-funded replant check, the crop starts at its initial stage, ground loot equals ordinary loot minus exactly one wheat seed, and no inventory seed is charged. Other item counts match the original result. Checks: AS-01, AS-04, AS-05, AS-14, AS-22.
- **SC-002**: For every inventory-funded replant check, the crop starts at its initial stage, inventory decreases by exactly one wheat seed, and ground loot equals the complete ordinary result. Wrong items and cancelled/losing interactions consume zero inventory items. Checks: AS-07, AS-23, AS-24; multiplayer also AS-20.
- **SC-003**: When neither source can pay, including zero generated loot, the crop is removed, farmland is unchanged and empty, all original loot drops, and no free planting item is created. Checks: AS-06, AS-24.
- **SC-004**: A full ordinary growth cycle after replanting is confirmed separately; immediate repeated/held interactions with an immature plant produce zero additional items or costs. Checks: AS-02, AS-03, AS-15. Bone meal is not substituted for the natural-growth evidence.
- **SC-005**: All ordinary planting, left-click, bone meal, and unsupported-plant scenarios match the game with the mod disabled. Held-click harvesting affects only successive targeted mature wheat, not an area. Checks: AS-08 through AS-12, AS-17, AS-21.
- **SC-006**: Saving/reopening and disabling/removing preserve test crops without duplicate loot, repeated seed payment, or world damage. No tested denial, cancellation, or duplicate processing causes partial effects or a crash. Checks: AS-13, AS-15, AS-16, AS-18, AS-19, AS-23; multiplayer also AS-20.
- **SC-007**: Prototype acceptance requires all P1 scenarios and a report distinguishing preparation from survival execution, natural growth from bone meal, and completed checks from unperformed checks. Do not count unperformed tests as passes. P2 is required before claiming the corresponding multiplayer support.

## Assumptions

- The current gameplay proof covers wheat in survival. LAN, dedicated servers, and more crops remain project goals, not discarded requirements or verified capabilities.
- Ordinary loot randomness belongs to the selected game version. Do not assume seeds can be absent naturally without checking it; controlled absent-seed fixtures may cover both inventory fallback and no-material cases.
- Using creative/commands to prepare isolated data is explicitly allowed; those privileges are not an input to the harvesting mechanic. Runtime survival, permission, and cheat-dependency assertions must reflect the conditions actually tested.
- Source requirements R01-R28 remain authoritative. License, compatible revisions, environment setup, and integration details require later review, not an invented choice inside this product specification.
- Inventory access, eligible ordinary inventory slots, and safe exact one-item consumption must be checked against the selected game version during technical planning. Do not extend the fallback to chests, nearby entities, or nested container contents without approval.
- Settings format and restart requirements will be selected after inspection; an in-game settings page is not promised.

### Source coverage and deferred scope

- **R01-R03**: prototype boundaries, FR-001, FR-015, FR-016, and test setup/execution distinction.
- **R04**: carrots, potatoes, and beetroot are not in this prototype; the first public release crop list is still pending.
- **R05-R11**: FR-001, FR-002, FR-004 through FR-008, FR-017.
- **R12-R19**: FR-003 through FR-006, FR-010 through FR-013, FR-016; creative/adventure behavior remains undecided.
- **R20-R23**: FR-009; special crops, nether wart, cocoa, and generic modded-plant support are not added here.
- **R24-R27**: FR-001, FR-014; disabling is checked in the prototype, while settings format, per-crop switches, and a possible in-game page remain later work, not deleted requirements.
- **R28**: FR-015, FR-017.

### Remaining review gates

1. Agree on the technical plan and separately review the draft principles. This product specification is approved; the earlier held-click question is resolved, and no product choices remain unresolved inside the described survival interaction.
2. Before implementing other game modes, agree on creative/adventure behavior without bypassing game restrictions.
3. Before expanding the prototype, choose release crops, corresponding settings, and each planting item under source R14.
4. Before native builds or compatibility claims, choose compatible revisions, inspect inventory and interaction behavior, obtain explicit native-build trust, and prepare distinct single-player/LAN/dedicated checks.

No technical plan, implementation tasks, or gameplay code are generated automatically by this specification.
