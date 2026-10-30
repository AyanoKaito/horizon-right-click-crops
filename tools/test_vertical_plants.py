"""Compact survival checks for retained-base sugar cane, cactus and bamboo."""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts


PLANTS = (
    ("sugar_cane", "sand", -8, 3),
    ("cactus", "sand", -4, 3),
    ("bamboo", "dirt", 0, 4),
)


def setup(batch, label, plant, support, z, height, drops=True, neighbour=True):
    commands = [
        "command gamemode creative", "command clear @s",
        f"command gamerule minecraft:block_drops {str(drops).lower()}",
        "command gamerule minecraft:random_tick_speed 0",
        f"fill 0 64 {z-2} 8 70 {z+2} minecraft:air --confirm",
        f"setblock 0 64 {z-1} minecraft:stone --confirm",
        f"setblock 3 64 {z} minecraft:{support} --confirm",
    ]
    if plant == "sugar_cane":
        commands.append(f"setblock 2 64 {z} minecraft:water --confirm")
    for y in range(65, 65 + height):
        commands.append(f"setblock 3 {y} {z} minecraft:{plant} --confirm")
    if neighbour:
        commands.append(f"setblock 6 64 {z} minecraft:{support} --confirm")
        if plant == "sugar_cane":
            commands.append(f"setblock 5 64 {z} minecraft:water --confirm")
        for y in range(65, 65 + height):
            commands.append(f"setblock 6 {y} {z} minecraft:{plant} --confirm")
    commands += [
        "command kill @e[type=minecraft:item]", "command give @s minecraft:wheat_seeds 5",
        f"command tp @s 0.5 65 {z-0.5}", "select 9", "command gamemode survival",
        "wait 3", f"look-at-block 3 {65 + height - 1} {z}", "state", "inventory",
        "entities 20 minecraft:item",
    ]
    state, inventory, ground = batch.script(label + "-setup", commands)[-3:]
    check(state["gamemode"] == "survival" and
          state["looking_at"]["block"]["pos"] == [3, 65 + height - 1, z], label + ": aim")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5} and not ground["entities"], label + ": clean fixture")


def inspect(batch, label, plant, support, z, height, neighbour=True):
    commands = [f"block 3 {y} {z}" for y in range(64, 65 + height)]
    if neighbour:
        commands += [f"block 6 {y} {z}" for y in range(65, 65 + height)]
    commands += ["inventory", "entities 20 minecraft:item"]
    replies = batch.script(label, commands)
    own = replies[:height + 1]
    other = replies[height + 1:height * 2 + 1] if neighbour else []
    inventory, ground = replies[-2:]
    check(own[0]["block"] == f"minecraft:{support}", label + ": support")
    check(own[1]["block"] == f"minecraft:{plant}", label + ": retained base")
    check(all(block["block"] == "minecraft:air" for block in own[2:]), label + ": upper growth removed")
    if neighbour:
        check(all(block["block"] == f"minecraft:{plant}" for block in other), label + ": neighbour untouched")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5}, label + ": no planting payment")
    return ground


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    for plant, support, z, height in PLANTS:
        setup(batch, plant + "-loot", plant, support, z, height)
        batch.script(plant + "-click", ["mouse right click", "wait 8"])
        ground = inspect(batch, plant + "-after", plant, support, z, height)
        check(ground_counts(ground) == {f"minecraft:{plant}": height - 1}, plant + ": one loot per removed block")
        batch.passed.append(plant + ": retained base, ground loot, no payment, no neighbour harvest")

        batch.script(plant + "-base-click", [
            "command kill @e[type=minecraft:item]", f"look-at-block 3 65 {z}",
            "mouse right click", "wait 6",
        ])
        again = inspect(batch, plant + "-base-after", plant, support, z, height)
        check(not again["entities"], plant + ": single base click has no effects")
        batch.passed.append(plant + ": single retained base passthrough")

        setup(batch, plant + "-no-drops", plant, support, z, height, drops=False, neighbour=False)
        batch.script(plant + "-middle-click", [f"look-at-block 3 66 {z}", "mouse right click", "wait 8"])
        ground = inspect(batch, plant + "-no-drops-after", plant, support, z, height, neighbour=False)
        check(not ground["entities"], plant + ": block-drops-off creates no loot")
        batch.passed.append(plant + ": connected-column harvest with drops disabled")

        setup(batch, plant + "-growth", plant, support, z, 1, neighbour=False)

    replies = batch.script("shared-growth", [
        "command gamemode creative", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 1000", "command clear @s",
        "command gamemode survival", "wait 1200",
        *[f"block 3 66 {z}" for _, _, z, _ in PLANTS],
        "command gamerule minecraft:random_tick_speed 3",
    ], timeout=150)
    for (plant, _, _, _), block in zip(PLANTS, replies[-4:-1]):
        check(block["block"] == f"minecraft:{plant}", plant + ": retained base regrew")
        batch.passed.append(plant + ": accelerated random-tick regrowth")

    batch.fixture("wheat-regression", "wheat", 7, "wheat_seeds", 3, -8)
    crop, inventory, ground = batch.click("wheat-regression", -8)
    check(crop["state"] == "minecraft:wheat[age=0]" and inventory == {"minecraft:wheat_seeds": 3}
          and ground_counts(ground)["minecraft:wheat"] == 1, "wheat regression")
    batch.passed.append("wheat regression")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, required=True)
    args = parser.parse_args()
    batch = Batch(json.loads(args.session.read_text(encoding="utf-8-sig")))
    result = {"status": "failed", "passed": batch.passed}
    try:
        run(batch)
        result["status"] = "passed"
    except Exception as error:
        result["failure"] = str(error)
        raise
    finally:
        result["control_processes"] = batch.calls
        (batch.run / "vertical-plant-results.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
