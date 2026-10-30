"""Compact survival checks for torchflower and two-block pitcher crops."""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts, ground_items


def setup(batch, label, kind, mature=True, supply=None, count=0, drops=True, click_upper=False):
    z = -8 if kind == "torchflower" else -4
    commands = [
        "command gamemode creative", "command clear @s",
        f"command gamerule minecraft:block_drops {str(drops).lower()}",
        "command gamerule minecraft:random_tick_speed 0",
        f"fill 0 65 {z-2} 4 67 {z+2} minecraft:air --confirm",
        f"setblock 3 64 {z} minecraft:farmland[moisture=7] --confirm",
    ]
    if kind == "torchflower":
        block = "minecraft:torchflower" if mature else "minecraft:torchflower_crop[age=1]"
        commands.append(f"setblock 3 65 {z} {block} --confirm")
        target_y = 65
    else:
        age = 4 if mature else 3
        commands += [
            f"setblock 3 65 {z} minecraft:pitcher_crop[age={age},half=lower] --confirm",
            f"setblock 3 66 {z} minecraft:pitcher_crop[age={age},half=upper] --confirm",
        ]
        target_y = 66 if click_upper else 65
    commands.append("command kill @e[type=minecraft:item]")
    if count:
        commands.append(f"command give @s minecraft:{supply} {count}")
    commands += [
        f"command tp @s 0.5 65 {z-0.5}", "select 9", "command gamemode survival",
        "wait 3", f"look-at-block 3 {target_y} {z}", "state", "inventory",
        "entities 16 minecraft:item",
    ]
    state, inventory, ground = batch.script(label + "-setup", commands)[-3:]
    check(state["gamemode"] == "survival" and
          state["looking_at"]["block"]["pos"] == [3, target_y, z], label + ": survival aim")
    check(inventory["counts"] == ({f"minecraft:{supply}": count} if count else {}), label + ": inventory")
    check(not ground["entities"], label + ": clean ground")
    return z


def action(batch, label, z):
    replies = batch.script(label + "-action", [
        "mouse right click", "wait 6", f"block 3 65 {z}", f"block 3 66 {z}",
        f"block 3 64 {z}", "inventory", "entities 16 minecraft:item", "state",
    ])
    lower, upper, soil, inventory, ground, state = replies[-6:]
    check(soil["state"] == "minecraft:farmland[moisture=7]", label + ": farmland")
    check(state["gamemode"] == "survival", label + ": survival after action")
    return lower, upper, inventory["counts"], ground


def young(kind, lower, upper):
    if kind == "torchflower":
        check(lower["state"] == "minecraft:torchflower_crop[age=0]", "torchflower: initial crop")
    else:
        check(lower["block"] == "minecraft:pitcher_crop" and "age=0" in lower["state"]
              and "half=lower" in lower["state"], "pitcher: initial lower crop")
    check(upper["block"] == "minecraft:air", kind + ": no stale upper half")


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    for kind, planting, product in [
        ("torchflower", "torchflower_seeds", "torchflower"),
        ("pitcher", "pitcher_pod", "pitcher_plant"),
    ]:
        label = kind + "-inventory"
        z = setup(batch, label, kind, supply=planting, count=2)
        lower, upper, inventory, ground = action(batch, label, z)
        young(kind, lower, upper)
        check(inventory == {f"minecraft:{planting}": 1}, label + ": exact inventory payment")
        check(ground_counts(ground) == {f"minecraft:{product}": 1}, label + ": ordinary product loot")
        batch.passed.append(label + ": ordinary loot and exact inventory replant")

        # The paid young plant must not immediately harvest again.
        batch.script(kind + "-repeat-aim", [f"look-at-block 3 65 {z}"])
        again_l, again_u, inv2, ground2 = action(batch, kind + "-repeat", z)
        young(kind, again_l, again_u)
        check(inv2 == inventory and ground_items(ground2) == ground_items(ground), kind + ": repeat")
        batch.passed.append(kind + ": immature repeat")

        label = kind + "-immature"
        z = setup(batch, label, kind, mature=False, supply=planting, count=2,
                  click_upper=(kind == "pitcher"))
        lower, upper, inventory, ground = action(batch, label, z)
        if kind == "torchflower":
            check(lower["state"] == "minecraft:torchflower_crop[age=1]", label + ": unchanged crop")
        else:
            check("age=3" in lower["state"] and "half=lower" in lower["state"]
                  and "age=3" in upper["state"] and "half=upper" in upper["state"],
                  label + ": both halves unchanged")
        check(inventory == {f"minecraft:{planting}": 2} and not ground["entities"], label + ": no effects")
        batch.passed.append(label)

        label = kind + "-missing"
        z = setup(batch, label, kind)
        lower, upper, inventory, ground = action(batch, label, z)
        check(lower["block"] == "minecraft:air" and upper["block"] == "minecraft:air", label + ": removed")
        check(not inventory and ground_counts(ground) == {f"minecraft:{product}": 1}, label + ": full product loot")
        batch.passed.append(label + ": harvest without planting material")

        label = kind + "-wrong"
        wrong = "beetroot_seeds" if kind == "torchflower" else "torchflower_seeds"
        z = setup(batch, label, kind, supply=wrong, count=2, drops=False,
                  click_upper=(kind == "pitcher"))
        lower, upper, inventory, ground = action(batch, label, z)
        check(lower["block"] == "minecraft:air" and upper["block"] == "minecraft:air", label + ": no replant")
        check(inventory == {f"minecraft:{wrong}": 2} and not ground["entities"], label + ": wrong item untouched")
        batch.passed.append(label)

        if kind == "pitcher":
            label = "pitcher-upper-paid"
            z = setup(batch, label, kind, supply=planting, count=2, click_upper=True)
            lower, upper, inventory, ground = action(batch, label, z)
            young(kind, lower, upper)
            check(inventory == {"minecraft:pitcher_pod": 1}
                  and ground_counts(ground) == {"minecraft:pitcher_plant": 1},
                  label + ": one operation from upper half")
            batch.passed.append(label + ": one loot and one payment")

        label = kind + "-growth"
        z = setup(batch, label, kind, supply=planting, count=2)
        lower, upper, inventory, _ = action(batch, label, z)
        young(kind, lower, upper)
        check(inventory == {f"minecraft:{planting}": 1}, label + ": paid replant")

    grown = batch.script("shared-growth", [
        "command gamemode creative", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 1000", "command gamemode survival",
        "wait 1200", "block 3 65 -8", "block 3 65 -4", "block 3 66 -4",
        "command gamerule minecraft:random_tick_speed 3",
    ], timeout=150)
    torch, lower, upper = grown[-4:-1]
    check(torch["block"] == "minecraft:torchflower", "torchflower: accelerated mature flower")
    check("age=4" in lower["state"] and "half=lower" in lower["state"]
          and "age=4" in upper["state"] and "half=upper" in upper["state"],
          "pitcher: accelerated mature two-block crop")
    batch.passed += ["torchflower accelerated random-tick regrowth", "pitcher accelerated two-half regrowth"]

    batch.fixture("wheat-regression", "wheat", 7, "wheat_seeds", 3, -8)
    plant, inventory, ground = batch.click("wheat-regression", -8)
    check(plant["state"] == "minecraft:wheat[age=0]" and inventory == {"minecraft:wheat_seeds": 3}
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
        (batch.run / "flower-crop-results.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
