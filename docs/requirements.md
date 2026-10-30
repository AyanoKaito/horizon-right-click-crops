# Horizon Right-Click Crops requirements

This is the canonical source of product requirements. `original-brief.md` is an English translation of the historical input; `decisions.md` records later decisions. Spec Kit artifacts must preserve these requirements. Changing agreed behavior requires approval.

## Purpose and scope

- R01: A small independent mod with one mechanic, not a farming pack; an original implementation, not an announced Java-mod port.
- R02: A public release for other players is the goal, including single-player, LAN, and dedicated servers. Advertise support only after testing each environment.
- R03: The first gameplay proof covers wheat only, with the mechanic working in survival without cheats or administrative rights. Creative mode, commands, and bone meal may prepare isolated test fields and supplies; switch to survival before exercising the harvest mechanic. Preparation privileges must not become runtime requirements.
- R04: The approved implementation scope has 18 plant families: wheat, carrots, potatoes, beetroot, nether wart, cocoa, torchflower, pitcher crop, sugar cane, cactus, bamboo, kelp, twisting vines, weeping vines, pumpkin, melon, sweet berries and glow berries. Approval is not evidence of implemented or tested support; the first public release list remains a later decision.

## Harvesting and normal interactions

- R05: Ordinary right-click on a mature supported crop harvests it without requiring crouching. Holding right-click and aiming at successive mature plants harvests through the game's normal repeated interactions, one targeted plant at a time. Do not require a fresh button press for each plant or introduce area harvesting.
- R06: Loot drops on the ground, not directly into the inventory. For paid-replant crops, if the generated loot contains a suitable planting item, reserve exactly one before spawning the remaining loot and leave the crop at its initial growth stage on the same support. Otherwise use the inventory fallback in R13, or R15 when neither source can pay. Retained living bases and stems follow R21 instead of incurring a planting cost.
- R07: A replanted crop grows normally. Immediate repeated clicks on an immature crop produce no items, consume no planting material, and do not reset growth.
- R08: Right-click does not harvest immature crops; ordinary interactions remain available.
- R09: Left-click continues to remove the plant through normal breaking behavior.
- R10: Ordinary planting and bone meal continue to work. The mod does not intercept bone meal use on either mature or immature crops; the game determines the result.
- R11: Harvesting itself does not change the underlying farmland or its state.

## Loot and operation integrity

- R12: Use Horizon's actual loot mechanism, including supported tool and Fortune effects; do not recreate loot tables from memory.
- R13: Pay for replanting with exactly one suitable item: first from generated loot, or, only when it contains none, from the player's inventory. Inventory fallback leaves the entire generated loot available to drop. Never charge both sources, take a different crop's planting item, use nearby ground items, or create free seeds. Replanting does not wait for dropped items to be picked up.
- R14: Wheat uses wheat seeds; beetroot uses beetroot seeds; carrots use carrots; potatoes use ordinary potatoes, never poisonous potatoes; nether wart uses nether wart; cocoa uses cocoa beans; torchflower uses torchflower seeds; pitcher crop uses a pitcher pod. Flower items are not substitutes for seeds or pods.
- R15: For paid-replant crops, if neither generated loot nor the player's inventory contains a suitable planting item, harvest anyway: drop all generated loot, remove the mature plant, and leave its support unchanged. This is a successful harvest without replanting, not an error or cancellation.
- R16: A cancelled harvest must not partially spawn loot, change the plant, or consume an inventory item. Successful harvesting without replanting under R15 is not cancellation. Prevent duplicate client/server or two-hand processing, and simultaneous double harvesting by two players when multiplayer is supported.
- R17: Use one source of loot; do not combine ordinary break drops with a second manual copy of the same items.
- R18: Respect game mode, interaction reach, and available permission/area-protection checks. Client prediction and subsequent messages must not trigger extra ordinary actions after a handled or cancelled interaction.
- R19: Save and reopen the world with the correct resulting state, without restored crops or repeated loot.

## Other plants

- R20: Preserve existing harvesting for berry bushes and glow berries, without an extra seed cost or second harvest.
- R21: Sugar cane, cactus, bamboo, kelp, twisting vines and weeping vines harvest one targeted connected column/vine while retaining a viable base or attachment, water where applicable, and ordinary head/body updates. Do not harvest neighboring plants or charge a planting item when retaining living growth. Pumpkin and melon harvesting removes the fruit, preserves its growing stem, and charges no seed; require an associated stem rather than harvesting arbitrary decorative blocks. Preserve pumpkin carving with shears. Do not use a generic age reset for these families.
- R22: Nether wart preserves soul sand; cocoa preserves attachment direction and support. Mature torchflower harvesting applies on farmland, not decorative flowers on other supports, and resets to the crop block only with real seed payment. Pitcher crop harvesting resolves either clicked half into one operation, one loot calculation and at most one planting payment; remove the upper half correctly and do not intercept decorative pitcher plants.
- R23: Do not promise compatibility with every plant from other mods.

Chorus, sea pickles, mushrooms, fungi, trees and other decorative flora are deferred for later consideration. Preserve their ordinary behavior; do not design or implement new harvesting mechanics for them in this expansion.

## Settings

- R24: The mod/convenience behavior must be disableable. Proposed settings are: mod enabled; hoe requirement disabled; individual supported crops enabled.
- R25: Choose the exact format, field names, and application behavior after checking the native template and Horizon conventions.
- R26: An in-game settings page is desirable but not promised until validated; document when a world reload or game restart is required.
- R27: A disabled mod does not interfere with ordinary behavior. Verify disabling/removing it without world damage.
- R28: Do not add area harvesting, hunger/experience costs, bonus loot, or unrelated improvements without approval.

## Prototype acceptance

Actual checks must cover mature wheat, payment from loot, inventory fallback with an exact one-item cost, no payment from either source, crop age and subsequent growth, held and repeated clicks, immature crops, bone meal on mature/immature crops, ordinary left-click, disabling, two-hand/repeated-processing duplicates, saving/reopening, and survival operation without runtime cheat/OP dependencies. Compilation alone does not establish any of these outcomes.

Prepare the test field and supplies in creative if convenient, optionally accelerating fixture growth with bone meal. Then switch to survival for harvest assertions and record starting inventory counts. Bone-meal-assisted maturation is not evidence of natural growth: verify ordinary growth separately. A command-enabled preparation world is not by itself evidence that a cheats-disabled world or an unprivileged multiplayer player has been tested.

If normal wheat loot always includes a seed in the selected game version, use controlled tests for inventory fallback and missing-material cases; do not claim those cases occurred naturally or alter ordinary gameplay drops to force them.

## Language and review policy

All Git-tracked documents, code, comments, commit messages, and GitHub-facing text must be English. Conversation and ignored `.local/review/` documents may be Russian. Keep the original Russian brief locally without publishing it again. Previously pushed history is not rewritten without separate approval.

## Open product decisions

- Which crops belong in the first public release?
- How should harvesting behave in creative/adventure while respecting game restrictions? Creative test preparation does not decide this behavior.

Resolve these before their implementation rather than silently accepting template defaults.
