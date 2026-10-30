# Crop coverage: reference survey and proposed inventory

Date: 2026-10-30. Status: research and scope proposal, not implemented support or a final release list.

Update after review: the user approved the proposed 18-family scope and special handling. [Requirements](requirements.md) now define the agreed behavior; candidate labels below describe implementation/evidence status, not a remaining scope gate. Additional flora is deferred for later consideration. Testing follows the grouped, risk-based policy in [development.md](development.md#efficient-test-batches-approved-2026-10-30), rather than repeating the full wheat campaign for each plant.

The user corrected the proposed sequencing: wheat is a prototype, not the whole intended product. Inventory the plants, compare the documented behavior of similar mods, implement the agreed plant groups and test them before release planning. This document does not silently replace the approved payment, safety or no-area-harvest rules.

## Method and limits

- Read public project descriptions, user documentation and the Minecraft crop index. No third-party gameplay implementation was inspected, copied, translated or ported.
- A reference project's broad statement such as "all vanilla crops" is not a verified per-plant support list. Named examples are distinguished from broad claims below.
- Minecraft Java reference-mod compatibility is not Horizon compatibility. Current native evidence covers wheat and the three additional field crops in separate validation records; wart/cocoa game checks are pending and other rows still need implementation or explicit ordinary-behavior tests.
- The proposed main list has **18 plant families**, not 18 block ids. Upper/lower halves, heads/bodies and fruit/stem pairs can need several ids for one family. More unusual flora is inventoried separately instead of hidden behind an "all plants" promise.

## What comparable projects document

| Reference | Explicit public description | Useful distinction, not a feature to copy automatically |
| --- | --- | --- |
| [RightClickHarvest](https://modrinth.com/mod/rightclickharvest) | Harvest/replant crops; broad vanilla-crop coverage, explicitly cocoa, cactus and sugar cane; Fortune; modded-crop claims. Its [tag documentation](https://docs.jamalam.tech/right-click-harvest/tags/) also names nether wart and cocoa. | Extends beyond the four ordinary field crops. Its radius, hunger/XP and broad modded support are not our approved requirements. |
| [Harvest with Ease](https://modrinth.com/mod/harvest-with-ease) | Mature-crop harvesting/replanting, explicitly nether wart and cocoa; consumes a crop item for planting; Fortune. | Public integration notes describe crop classes/age properties, not a complete verified species list. Its [configuration wiki](https://github.com/Crystal-Nest/harvest-with-ease/wiki/End-user-configuration) has optional multi-harvest and balancing settings that we must not import. |
| [The Right Click Harvest](https://modrinth.com/mod/the-right-click-harvest) | Harvest/replant grown crops using inventory or drops, plus crouch-to-harvest-without-replanting. | The description does not enumerate individual plants or establish our loot-first priority. Its crouch mode is not adopted. |
| [Harvest](https://modrinth.com/mod/harvest) | Right-click breaks fully grown crops and nether wart. | Right-click breaking is not necessarily paid replanting; do not treat it as equivalent to our mechanic. |
| [Actually Harvest](https://modrinth.com/mod/actually-harvest) | Broad modded crops/trees, named Java-mod integrations, optional radius/durability/XP. | Demonstrates that tree/modpack scope is a separate design choice, not proof that native Horizon can support those Java mods. |

RightClickHarvest's current project description and its configuration page disagree about some defaults (for example hoe/hunger settings). They are not used to define our defaults. Broad marketing percentages are not carried into this project.

## Proposed main plant list

All behavior in this table is **proposed**, except the explicitly labelled existing wheat/berry evidence. The six vertical-growth rows and fruit rows need product-rule approval before implementation; their age values must not be mistaken for maturity.

| Plant family | Proposed operation | Planting resource / structure to preserve | Current evidence |
| --- | --- | --- | --- |
| Wheat | Mature crop to initial growth stage | One wheat seed; same farmland | Implemented and partially accepted in the wheat validation record |
| Carrots | Mature crop to initial growth stage | One carrot; same farmland | Implemented; partial dev.3 group validation |
| Potatoes | Mature crop to initial growth stage | One normal potato, never a poisonous potato | Implemented; partial dev.3 group validation |
| Beetroot | Mature crop to initial growth stage | One beetroot seed, not beetroot | Implemented; partial dev.3 group validation |
| Nether wart | Mature wart to initial stage | One nether wart; preserve soul sand | Implemented; partial dev.4 group validation |
| Cocoa | Mature pod to initial stage | One cocoa bean; preserve facing and supporting jungle log | Implemented; partial dev.4 group validation |
| Torchflower | Mature field-grown flower to initial crop block | One torchflower seed; never invent a seed from the flower item | Implemented; partial dev.5 group validation |
| Pitcher crop | Mature two-block crop to one initial crop | One pitcher pod; recognize either clicked half, no duplicate upper-half loot | Implemented; partial dev.5 group validation |
| Sugar cane | Harvest growth above a retained base in one targeted column | Keep the living base/support and water; no planting debit if no replant occurs | Implemented; partial dev.6 group validation |
| Cactus | Harvest growth above a retained base in one targeted column | Keep base and sand; handle any cactus flower through ordinary updates | Implemented; partial dev.6 group validation; flower pending |
| Bamboo | Harvest growth above a retained base in one targeted column | Keep viable base; distinguish shoot/stalk; no age-based fake maturity | Implemented; partial dev.6 group validation |
| Kelp | Harvest one connected plant while retaining its base | Preserve water and a viable kelp growth state | Implemented; partial dev.7 group validation |
| Twisting vines | Harvest one connected vine while retaining its rooted portion | Preserve the correct grounded end and head/body transitions | Implemented; partial dev.7 group validation |
| Weeping vines | Harvest one connected hanging vine while retaining its attachment | Preserve the ceiling-side anchor, not an arbitrary lowest block | Implemented; partial dev.7 group validation |
| Pumpkin | Harvest the actual fruit while retaining its growing stem | No seed debit if the stem remains; preserve ordinary shears/carving | Implemented; partial dev.8 group validation |
| Melon | Harvest the actual fruit while retaining its growing stem | No seed debit if the stem remains; preserve ordinary tool/Fortune/Silk Touch loot | Implemented; partial dev.8 group validation |
| Sweet berries | Leave the ordinary right-click harvest in control | No extra seed payment, no second loot calculation | Preserved; partial dev.8 final-stage validation |
| Glow berries | Leave the ordinary right-click harvest in control | Keep vine and ordinary berry flag changes; no extra payment/drop | Preserved; partial dev.8 final-stage validation |

For the first eight paid-replant rows, the approved rule remains: reserve exactly one correct planting item from generated loot first, otherwise from the acting player's ordinary inventory, otherwise harvest without replanting. Preserving an already-living base/stem is **not** a free replant and must not charge a fictitious planting item. That distinction is a proposal to review, not an unnoticed change to the current wheat implementation.

## Additional flora: explicitly decide, do not silently generalize

| Plant group | Why it is not an ordinary maturity reset | Proposed review treatment |
| --- | --- | --- |
| Chorus plant / chorus flower | Branched structure, fruit is not a planting item, viable flower/regrowth and collapse behavior differ | Decide separately whether to add a custom one-plant harvest; no confirmed exact behavior from the reference descriptions |
| Sea pickles | Cluster count/spreading is not crop maturity | Decide whether harvesting a cluster while retaining one is desirable; do not create items from a generic age reset |
| Brown/red mushrooms | Spreading plants; huge mushrooms are structures, not ripe versions of a one-block crop | Preserve ordinary behavior unless a separate harvest rule is requested |
| Crimson/warped fungi | Huge fungus growth is not a normal crop harvest/replant cycle | Preserve ordinary behavior unless separately designed |
| Saplings, trees and propagules | Tree harvesting/felling is another mechanic with structural and tool rules | Do not add tree felling to this small crop mod by inference |
| Decorative flowers (including cactus flowers), grass, moss, lichen and ordinary non-fruiting vines | Most have no harvestable maturity; a one-item drop reserved for replanting can yield nothing or interfere with ordinary use | Explicit passthrough by default; no flower duplication or generic collection feature |
| Crops from other mods | Java reference-mod integrations do not map automatically to Horizon ids/behaviors | Add named native plant profiles only after their own compatibility tests; no blanket percentage claim |

"All plants" therefore needs a concrete inventory and behavior for each family, not a test for the existence of an `age` property. The unusual rows remain visible for the user's scope decision rather than being silently declared supported or excluded forever.

## Pinned Horizon checks relevant to the proposal

Read-only inspection used the existing `64e298952d8bbb1188108bd4de68be2ab25d202b` export and matching prepared 26.3 data. No game resources are included in this document.

- The ordinary `minecraft:crops` tag includes the four field crops, pumpkin/melon stems, torchflower crop and pitcher crop. It is not a complete list of right-click-harvest candidates: cocoa, wart, vertical plants and berries require their own handling.
- `horizon-world/src/level/bonemeal.rs::crop_state_for_age` turns mature torchflower growth into the distinct flower block. Resetting a property on that mature flower is insufficient.
- The same module's pitcher helpers resolve a lower half and allow growth up to age 4. Harvesting both halves as independent crops would be wrong.
- The mature torchflower's actual loot table drops the flower, not a planting seed; pitcher crop loot similarly needs a real planting-item check, not a flower-to-seed conversion. Inventory fallback/no-replant outcomes are important product cases for these two plants.
- `horizon-world/src/level/tick.rs` has distinct crop, stem, cocoa, wart, cactus, cane, bamboo and growing-plant paths. A shared payment core can be retained without forcing a single world-mutation adapter onto all of them.

## Implementation and test order after scope review

1. Agree on the inventory and special-plant rules. Preserve the native approach, source pins unless separately changed, survival-first scope and no area harvesting.
2. Implement carrots/potatoes/beetroot with individual planting items, maturity limits and profiles; rerun wheat to catch regressions.
3. Add wart/cocoa and then torchflower/pitcher; test supporting blocks, direction, mature/crop identity and two-block integrity.
4. Implement the agreed vertical-plant and fruit rules as separate adapters. One connected targeted plant is not a radius/neighbor harvest; retain ordinary bone meal and item-specific interactions.
5. Verify ordinary berries and every explicitly excluded flora group remain unchanged. Do not add a new berry harvest on top of the existing one.
6. Run a per-family matrix: mature/immature behavior, ordinary loot versus control (including applicable enchantments), correct paid item, loot priority, fallback/no material, held click, both hands, protection, support preservation, persistence, disabling/removal and natural regrowth. Mark genuinely inapplicable cases as such, not passed.

All game tests must use isolated homes/saves; preparation may use creative and commands, but harvest assertions run in survival. Controlled missing-material fixtures stay separate from ordinary gameplay loot. Record each family as planned, implemented, tested or blocked. Multiplayer capability work and publishing remain later gates, not evidence inferred from single-player crop coverage.

## Sources

- https://modrinth.com/mod/rightclickharvest
- https://docs.jamalam.tech/right-click-harvest/about/
- https://docs.jamalam.tech/right-click-harvest/tags/
- https://docs.jamalam.tech/right-click-harvest/configuration/
- https://modrinth.com/mod/harvest-with-ease
- https://github.com/Crystal-Nest/harvest-with-ease/wiki/End-user-configuration
- https://modrinth.com/mod/the-right-click-harvest
- https://modrinth.com/mod/harvest
- https://modrinth.com/mod/actually-harvest
- https://minecraft.wiki/w/Crops (plant inventory/reference only, not our compatibility list)

Direct CurseForge fetches were unavailable (HTTP 403); unsupported search snippets were not elevated to confirmed per-plant behavior. Public descriptions were not verified by running the Java mods. Existing reference licenses and the original-code boundary in `docs/research.md` remain applicable.
