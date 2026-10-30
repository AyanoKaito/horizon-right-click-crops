"""Compact survival checks for retained-anchor kelp and Nether vines."""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts, ground_items


PLANTS = (
    ("kelp", "kelp_plant", "up", -8),
    ("twisting_vines", "twisting_vines_plant", "up", -4),
    ("weeping_vines", "weeping_vines_plant", "down", 0),
)


def positions(direction):
    return [65, 66, 67] if direction == "up" else [67, 66, 65]


def setup(batch, label, head, body, direction, z, drops=True, neighbour=True):
    ys = positions(direction)
    commands = [
        "command gamemode creative", "command clear @s",
        f"command gamerule minecraft:block_drops {str(drops).lower()}",
        "command gamerule minecraft:random_tick_speed 0",
        f"fill 0 63 {z-2} 8 72 {z+2} minecraft:air --confirm",
        f"setblock 0 63 {z-1} minecraft:stone --confirm",
    ]
    columns = [3, 6] if neighbour else [3]
    for x in columns:
        if head == "kelp":
            commands += [
                f"setblock {x} 64 {z} minecraft:stone --confirm",
                f"fill {x-1} 65 {z} {x+1} 69 {z} minecraft:water --confirm",
            ]
        elif direction == "up":
            commands.append(f"setblock {x} 64 {z} minecraft:netherrack --confirm")
        else:
            commands.append(f"setblock {x} 68 {z} minecraft:netherrack --confirm")
        commands += [
            f"setblock {x} {ys[0]} {z} minecraft:{body} --confirm",
            f"setblock {x} {ys[1]} {z} minecraft:{body} --confirm",
            f"setblock {x} {ys[2]} {z} minecraft:{head}[age=0] --confirm",
        ]
    commands += [
        "command kill @e[type=minecraft:item]", "command give @s minecraft:shears 1",
        f"command tp @s 0.5 64 {z-0.5}", "select 1", "command gamemode survival",
        "wait 4", f"look-at-block 3 {ys[2]} {z}", "state", "inventory",
        "entities 20 minecraft:item",
    ]
    state, inventory, ground = batch.script(label + "-setup", commands)[-3:]
    check(state["gamemode"] == "survival" and
          state["looking_at"]["block"]["pos"] == [3, ys[2], z], label + ": survival aim")
    check(inventory["counts"] == {"minecraft:shears": 1}, label + ": held shears")
    check(not ground["entities"], label + ": clean ground")


def inspect(batch, label, head, body, direction, z, neighbour=True):
    ys = positions(direction)
    commands = [f"block 3 {y} {z}" for y in ys]
    if neighbour:
        commands += [f"block 6 {y} {z}" for y in ys]
    commands += ["inventory", "entities 20 minecraft:item", "state"]
    replies = batch.script(label, commands)
    own = replies[:3]
    other = replies[3:6] if neighbour else []
    inventory, ground, state = replies[-3:]
    check(own[0]["block"] == f"minecraft:{head}", label + ": retained anchor became live head")
    empty = "minecraft:water" if head == "kelp" else "minecraft:air"
    check(all(block["block"] == empty for block in own[1:]), label + ": outward growth removed")
    if neighbour:
        family = {f"minecraft:{head}", f"minecraft:{body}"}
        check(all(block["block"] in family for block in other), label + ": neighbour untouched")
    check(inventory["counts"] == {"minecraft:shears": 1}, label + ": no payment or tool loss")
    check(state["gamemode"] == "survival", label + ": survival after action")
    return ground


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    for head, body, direction, z in PLANTS:
        setup(batch, head + "-loot", head, body, direction, z)
        batch.script(head + "-click", ["mouse right click", "wait 10"])
        ground = inspect(batch, head + "-after", head, body, direction, z)
        check(ground_counts(ground) == {f"minecraft:{head}": 2}, head + ": shears-aware ordinary loot")
        batch.passed.append(head + ": retained live anchor, exact tool-aware loot, no neighbour harvest")

        anchor_y = positions(direction)[0]
        before = ground_items(ground)
        batch.script(head + "-anchor-click", [f"look-at-block 3 {anchor_y} {z}", "mouse right click", "wait 6"])
        again = inspect(batch, head + "-anchor-after", head, body, direction, z)
        check(ground_items(again) == before, head + ": lone anchor has no effects")
        batch.passed.append(head + ": single retained anchor passthrough")

        setup(batch, head + "-no-drops", head, body, direction, z, drops=False, neighbour=False)
        middle_y = positions(direction)[1]
        batch.script(head + "-middle-click", [f"look-at-block 3 {middle_y} {z}", "mouse right click", "wait 10"])
        ground = inspect(batch, head + "-no-drops-after", head, body, direction, z, neighbour=False)
        check(not ground["entities"], head + ": drops-disabled harvest creates no loot")
        batch.passed.append(head + ": connected directed harvest with drops disabled")

    replies = batch.script("shared-growth", [
        "command gamemode creative", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 1000", "command clear @s",
        "command gamemode survival", "wait 1200",
        "block 3 66 -8", "block 3 66 -4", "block 3 66 0",
        "command gamerule minecraft:random_tick_speed 3",
    ], timeout=150)
    for (head, _, _, _), block in zip(PLANTS, replies[-4:-1]):
        family = {f"minecraft:{head}", f"minecraft:{head}_plant"}
        check(block["block"] in family, head + ": retained anchor regrew outward")
        batch.passed.append(head + ": accelerated directed random-tick regrowth")

    batch.script("wheat-regression-cleanup", [
        "command gamemode creative", "fill 0 65 -10 4 72 -6 minecraft:air --confirm", "wait 4",
    ])
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
        (batch.run / "kelp-vine-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
