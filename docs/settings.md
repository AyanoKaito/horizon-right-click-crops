# Plant settings

Version `0.1.0-dev.9` adds individual settings for the sixteen plant families whose right-click behavior this mod changes. Sweet berry bushes and glow berries remain ordinary Horizon interactions and have no setting.

## In-game page

Open `Options > Mods > Right-Click Crops > Settings`. Horizon draws one scrolling, alphabetical list of full-width buttons:

1. Bamboo
2. Beetroot
3. Cactus
4. Carrots
5. Cocoa
6. Kelp
7. Melon
8. Nether wart
9. Pitcher crop
10. Potatoes
11. Pumpkin
12. Sugar cane
13. Torchflower
14. Twisting vines
15. Weeping vines
16. Wheat

Each label is `Plant: ON` or `Plant: OFF`. A click applies immediately to the client and its integrated server and saves the complete configuration. Turning a family off makes the mod pass that interaction through without changing the block, inventory or ordinary Horizon behavior.

The standard `Options > Mods` toggle controls the whole native mod and retains its full-process-restart behavior. There is no second disable-all button inside the plant page.

## Configuration file

Horizon keeps the file at:

```text
horizon-mods/.horizon-mod-data/right-click-crops/plants.conf
```

It contains one exact `true` or `false` value per managed family:

```ini
bamboo=true
beetroot=true
cactus=true
carrots=true
cocoa=true
kelp=true
melon=true
nether_wart=true
pitcher_crop=true
potatoes=true
pumpkin=true
sugar_cane=true
torchflower=true
twisting_vines=true
weeping_vines=true
wheat=true
```

Missing files, missing keys, unknown keys and invalid values leave the corresponding known family enabled. Empty lines and lines beginning with `#` are ignored. Manual file edits are loaded on the next game process start; in-game clicks apply immediately and rewrite the file in canonical alphabetical order.

## Validation scope

The `dev.9` settings change passed 16 standalone Rust tests, 26 Python structural/observation tests, a real six-hook Mixins plan and an offline fast native build against the pinned Horizon revision. An isolated Superflat test world confirmed the real Mods row, the top and bottom of the scrolling list, file creation, immediate disabled and re-enabled Bamboo behavior in survival, and Cactus persistence across a full process restart. The fixture and settings were restored afterward.

This focused pass did not repeat all earlier per-family gameplay batches, LAN or dedicated-server checks. It does not turn their existing partial evidence into release acceptance.
