# Right-Click Crops requirements

This is the current product contract for version `2.0.1`. Behaviour changes require approval.

## Scope

- The project is a small independent Horizon WebAssembly mod with one mechanic, built with the Horizon mod SDK.
- It is an original implementation, not a port, and does not use gameplay code from other harvest mods.
- Version `2.0.1` targets Horizon mod SDK `f00125f` (mod API 0.2) and Minecraft 26.3.
- Support is advertised only for environments that pass actual gameplay validation.

## Managed plants

The mod explicitly manages wheat, carrots, potatoes, beetroot, nether wart, cocoa, torchflower, pitcher crop, sugar cane, cactus, bamboo, kelp, twisting vines, weeping vines, pumpkin and melon.

Sweet berries and glow berries retain ordinary Horizon behaviour and have no mod setting. Unlisted and modded plants pass through unchanged.

## Harvest behaviour

- A survival right-click harvests one targeted mature managed plant.
- Immature plants, creative/adventure/spectator actors, bone meal and unrelated interactions pass through.
- Holding right-click may harvest successive targeted mature plants through Horizon's ordinary repeated interactions; this is not area harvesting.
- Ordinary left-click breaking and planting remain available.
- The underlying farmland, soul sand, attachment support, water and unrelated block properties remain unchanged.
- A replanted crop starts at its ordinary initial growth state and can grow through Horizon's normal mechanics.
- Vertical plants retain their lowest connected base and remove only the connected growth above it.
- Pumpkin and melon harvest removes the fruit and retains its attached stem.
- Pumpkin carving with shears remains an ordinary interaction.
- Nether wart keeps soul sand; cocoa keeps its support and facing.
- Torchflower handling applies to the crop on farmland, not a decorative torchflower elsewhere.
- Clicking either half of a mature pitcher crop performs one harvest, one loot calculation and at most one planting payment.
- Save and reopen must preserve the resulting blocks and items without restoring crops or repeating loot.

## Loot and replanting

- Use Horizon's ordinary loot calculation exactly once with the acting player's held item.
- Preserve applicable ordinary tool and Fortune effects rather than recreating loot tables.
- Reserve one suitable planting item from generated loot first.
- If loot has none, take exactly one suitable plain item from the acting player's normal inventory or off hand.
- If neither source can pay, harvest without replanting.
- Never charge both sources, create free items, duplicate drops or use nearby ground items as payment.
- Wheat uses wheat seeds; beetroot uses beetroot seeds; carrots use carrots; potatoes use ordinary potatoes; nether wart uses nether wart; cocoa uses cocoa beans; torchflower uses torchflower seeds; pitcher crop uses a pitcher pod.
- Poisonous potatoes, flowers and another crop's planting items are never substitutes.
- Retained vertical bases and attached stems require no planting payment.
- A failed or cancelled harvest leaves the plant and inventory unchanged.
- Client prediction, repeated packets, two hands and simultaneous players must not duplicate a harvest or trigger an extra ordinary item action after a handled click.

## Settings

- Every managed plant has an independent setting, enabled by default.
- Settings are registered with Horizon's settings service and appear on the mod's Config page; Horizon stores them.
- The page lists one on/off setting per plant, without categories, counts or a second global action.
- Changes apply to the next click without a restart. Missing values use the enabled default.
- In a LAN game the host's settings decide harvesting for every player.
- Horizon's per-mod line in `horizon-mods.txt` remains the whole-mod control and requires a restart.
- Sweet berries and glow berries do not appear in the list.
- Disabling or removing the mod must leave ordinary interactions and existing worlds usable.

## Integrity and boundaries

- The mechanic must work in survival without cheats, operator status, creative-only grants, hunger costs or experience costs.
- Commands, creative mode and bone meal may prepare isolated fixtures, but assertions must switch the acting player to survival.
- Test setup with bone meal is not evidence of natural growth; accelerated random ticks must be labelled accurately.
- Respect Horizon's reach, world border, game mode and available interaction restrictions.
- Unlisted plants pass through unchanged. Chorus, sea pickles, mushrooms, fungi, trees and arbitrary crops from other mods are not claimed as supported.
- The mod does not add area harvesting, bonus loot or unrelated farming conveniences.

## Validation and release

- Required release checks: unit tests, WebAssembly build and `cargo horizon-mod check` on Linux CI, isolated single-player gameplay, LAN host/guest gameplay, package inspection and SHA-256.
- Gameplay checks cover empty and held main-hand clicks, offhand follow-up, mature and immature targets, bone meal in either hand, loot-funded and inventory-funded replanting, missing material, repeated use, ordinary breaking and planting, settings, persistence and save/reopen behaviour.
- Compilation alone is not gameplay evidence. Skipped checks and platform limitations must be reported.
- Dedicated support is not claimed until a dedicated gameplay check passes.
- Public release, repository visibility and public announcements happen only after separate approval.
