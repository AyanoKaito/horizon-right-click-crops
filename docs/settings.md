# Plant settings

Open `Options > Mods > Right-Click Crops > Settings` to see one alphabetical list of sixteen `Plant: ON/OFF` buttons.

All plants default to `ON`. A button changes the corresponding plant immediately for the running process. The global native-mod switch still requires a full game restart.

Settings are stored in:

```text
horizon-mods/.horizon-mod-data/right_click_crops/plants.conf
```

Supported keys:

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

Each value is `true` or `false`. Unknown keys and malformed values are ignored. Manual edits load on the next game start.

If you used a development build with the former `right-click-crops` ID, copy its `plants.conf` into the new `right_click_crops` directory before starting `1.0.0`; otherwise the defaults apply.

Sweet berries and glow berries have no setting because the mod does not replace their ordinary Horizon interactions.
