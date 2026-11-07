# Harvesting guide

Right-Click Crops changes how you harvest, not the game's loot tables. The notes below describe version `1.0.1` on its [tested Horizon revision](../VALIDATION.md).

## The short version

- Right-click a mature supported plant in **survival**. One interaction handles one targeted plant or connected vertical column, not a whole field.
- Replanting costs **one matching planting item**: generated loot pays first, then your inventory (including the offhand). Never both.
- If neither source has that item, you still receive the ordinary harvest, but the crop is **not replanted**.
- Vertical plants keep their base; pumpkins and melons keep their attached stem. These do not need a planting item.
- Loot remains ordinary Horizon loot. A harvest is not a promise of a fixed number of items or a guaranteed drop.

## What pays for replanting?

| Plant | One item needed | Important detail |
|---|---|---|
| Wheat | Wheat seeds | Wheat itself is not a seed. |
| Carrots | Carrot | One carrot is reserved for planting. |
| Potatoes | Potato | Poisonous potatoes cannot pay. |
| Beetroot | Beetroot seeds | If the loot rolls no seeds, inventory supplies one; beetroot itself cannot pay. |
| Nether wart | Nether wart | One wart is reserved for planting. |
| Cocoa | Cocoa beans | One bean is reserved for planting; support and facing are retained. |
| Torchflower | Torchflower seeds | The mature flower does not provide replacement seeds. Keep spare seeds in your inventory. |
| Pitcher crop | Pitcher pod | The mature pitcher plant is not a pod. Keep spare pods in your inventory. |

Planting items do not need to be selected in your hand. Items lying on the ground are not used as payment. A successful replant starts at the ordinary initial growth stage.

For a mature pitcher crop, clicking either half performs one harvest and at most one planting payment, not one per half. A decorative torchflower away from farmland is not managed by the mod.

## What stays in the world?

| Plants | Retained part |
|---|---|
| Sugar cane, cactus, bamboo, kelp, twisting vines | The lowest connected base; growth above it is harvested. |
| Weeping vines (the red hanging vines) | The top connected anchor; hanging growth below it is harvested. |
| Pumpkin, melon | The attached stem. The fruit must have a matching attached stem beside it. |

A lone base has no extra growth to harvest. Removing growth does not consume seeds or planting material. Holding right-click can handle successive targets through normal repeated interactions, but does not harvest neighbouring columns as an area action.

## Why did my Nether vines drop nothing?

Both **twisting vines** and **weeping vines** use the same ordinary drop chances for each removed block:

| Main-hand tool or enchantment | Chance per removed block |
|---|---|
| Empty hand / ordinary tool without a relevant enchantment | 33% |
| Fortune I | 55% |
| Fortune II | 77% |
| Fortune III | 100% |
| Shears or a tool satisfying the game's Silk Touch condition | 100% |

These are per-block chances, not a guarantee that every click gives an item. Removing two blocks with an empty hand can give zero, one or two vines. The retained base does not drop an item because it was not removed.

The numbers come from the tested game's loot tables, not custom mod probabilities. [Focused gameplay checks](../VALIDATION.md#follow-up-nether-vine-loot) verified both vines with empty hands and plain shears. Enchantment cases were not retested in that follow-up.

## When does the mod leave the click alone?

- The actor is not in survival, the plant is immature, or its setting is OFF.
- Bone meal is held in either hand: normal fertilising takes priority.
- You are crouching with an item in either hand: normal item use takes priority.
- You use shears on a pumpkin: normal carving takes priority.
- The plant is unsupported. Sweet berries and glow berries are deliberately left to Horizon and have no mod settings.

World restrictions and the game's reach still apply. If the world disables block drops (`minecraft:block_drops = false`), the mod does not invent loot to compensate. This setting is separate from the random chance of a Nether vine drop.

## Quick troubleshooting

**The flower disappeared instead of being replanted.** Check for torchflower seeds or pitcher pods in your inventory, not the harvested flower or pitcher plant.

**Only the vine's base remained and nothing dropped.** That is possible with an empty hand. Try shears in your main hand. If a shears harvest still gives nothing, check the world's block-drop rule and report the plant, tool, Horizon revision and what happened.

**Right-click did not harvest.** Check survival mode, maturity, the plant's [setting](settings.md), bone meal in either hand, reach and any world restrictions. The mod does not force an action the game disallows.
