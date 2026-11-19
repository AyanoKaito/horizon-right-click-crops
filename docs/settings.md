# Plant settings

Open the **Mods** screen (title screen or `Options > Mods`), select Right-Click Crops and press **Config**. The page lists sixteen on/off settings, one per managed plant.

All plants default to `ON`. A change applies to the next right-click; no restart is needed. Horizon's on/off line in `horizon-mods.txt` remains the whole-mod switch and needs a restart.

Horizon stores the settings in:

```text
horizon-mods/.horizon-mod-data/right_click_crops/
```

There is one file per setting. Setting keys:

```text
bamboo
beetroot
cactus
carrots
cocoa
kelp
melon
nether_wart
pitcher_crop
potatoes
pumpkin
sugar_cane
torchflower
twisting_vines
weeping_vines
wheat
```

The 1.x `plants.conf` file is no longer read. After upgrading, all plants start `ON`.

In a LAN game, the host's settings decide what the host's world harvests, for every player. A guest's own settings only affect what the guest's game predicts before the host answers.

Sweet berries and glow berries have no setting because the mod does not replace their ordinary Horizon interactions.
