"""Compact survival checks for stem-associated pumpkin and melon fruit."""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts


FRUITS = (
    ("pumpkin", "pumpkin_stem", "attached_pumpkin_stem", -8, "west"),
    ("melon", "melon_stem", "attached_melon_stem", -4, "north"),
)


def linked_setup(batch, label, fruit, stem, attached, z, side, drops=True, shears=False):
    if side == "west":
        stem_pos = (2, z)
        facing = "east"
    elif side == "east":
        stem_pos = (4, z)
        facing = "west"
    else:
        stem_pos = (3, z - 1)
        facing = "south"
    sx, sz = stem_pos
    commands = [
        "command gamemode creative", "command clear @s",
        f"command gamerule minecraft:block_drops {str(drops).lower()}",
        "command gamerule minecraft:random_tick_speed 0",
        f"fill 0 64 {z-2} 5 68 {z+2} minecraft:air --confirm",
        f"setblock 0 64 {z-1} minecraft:stone --confirm",
        f"setblock {sx} 64 {sz} minecraft:farmland[moisture=7] --confirm",
        f"setblock 3 64 {z} minecraft:dirt --confirm",
        f"setblock 3 65 {z} minecraft:{fruit} --confirm",
        f"setblock {sx} 65 {sz} minecraft:{attached}[facing={facing}] --confirm",
        "command kill @e[type=minecraft:item]",
    ]
    if shears:
        commands += ["command give @s minecraft:shears 1", "wait 2", "select 1", "wait 2"]
    else:
        commands += ["command give @s minecraft:wheat_seeds 5", "select 9"]
    commands += [
        f"command tp @s 0.5 65 {z-0.5}", "command gamemode survival", "wait 4",
        f"look-at-block 3 65 {z}", "state", "inventory", "entities 20 minecraft:item",
    ]
    state, inventory, ground = batch.script(label + "-setup", commands)[-3:]
    check(state["gamemode"] == "survival" and
          state["looking_at"]["block"]["pos"] == [3, 65, z], label + ": survival fruit aim")
    expected = {"minecraft:shears": 1} if shears else {"minecraft:wheat_seeds": 5}
    check(inventory["counts"] == expected and not ground["entities"], label + ": clean inventory and ground")
    return stem_pos


def action(batch, label, z, stem_pos):
    sx, sz = stem_pos
    fruit_block, stem_block, inventory, ground, state = batch.script(label + "-action", [
        "mouse right click", "wait 8", f"block 3 65 {z}", f"block {sx} 65 {sz}",
        "inventory", "entities 20 minecraft:item", "state",
    ])[-5:]
    check(state["gamemode"] == "survival", label + ": survival after action")
    return fruit_block, stem_block, inventory["counts"], ground


def decorative_case(batch, fruit, z):
    replies = batch.script(fruit + "-decorative-setup", [
        "command gamemode creative", "command clear @s",
        "command gamerule minecraft:block_drops true",
        f"fill 0 64 {z-2} 5 68 {z+2} minecraft:air --confirm",
        f"setblock 0 64 {z-1} minecraft:stone --confirm",
        f"setblock 3 64 {z} minecraft:dirt --confirm", f"setblock 3 65 {z} minecraft:{fruit} --confirm",
        "command kill @e[type=minecraft:item]", f"command tp @s 0.5 65 {z-0.5}",
        "select 9", "command gamemode survival", "wait 4", f"look-at-block 3 65 {z}", "state",
    ])
    check(replies[-1]["looking_at"]["block"]["pos"] == [3, 65, z], fruit + ": decorative aim")
    block, inventory, ground = batch.script(fruit + "-decorative-action", [
        "mouse right click", "wait 8", f"block 3 65 {z}", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(block["block"] == f"minecraft:{fruit}" and not inventory["counts"] and not ground["entities"],
          fruit + ": unassociated decoration untouched")
    batch.passed.append(fruit + ": unassociated decorative fruit passthrough")


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    growth_sites = []
    for fruit, stem, attached, z, side in FRUITS:
        stem_pos = linked_setup(batch, fruit + "-linked", fruit, stem, attached, z, side)
        fruit_block, stem_block, inventory, ground = action(batch, fruit + "-linked", z, stem_pos)
        check(fruit_block["block"] == "minecraft:air", fruit + ": linked fruit removed")
        check(stem_block["state"] == f"minecraft:{stem}[age=7]", fruit + ": mature stem preserved")
        check(inventory == {"minecraft:wheat_seeds": 5}, fruit + ": no seed payment")
        counts = ground_counts(ground)
        if fruit == "pumpkin":
            check(counts == {"minecraft:pumpkin": 1}, "pumpkin: ordinary block loot")
        else:
            check(set(counts) == {"minecraft:melon_slice"} and 3 <= counts["minecraft:melon_slice"] <= 7,
                  "melon: ordinary slice loot")
        batch.passed.append(fruit + ": associated harvest, stem retained, ordinary loot, no payment")
        growth_sites.append((fruit, attached, z, stem_pos))

    state, inventory, ground = batch.script("pumpkin-carve-setup", [
        "command gamemode creative", "command clear @s", "command gamerule minecraft:block_drops true",
        "fill 0 64 -2 5 68 2 minecraft:air --confirm", "setblock 0 64 0 minecraft:stone --confirm",
        "setblock 3 64 0 minecraft:dirt --confirm",
        "setblock 3 65 0 minecraft:pumpkin --confirm", "command kill @e[type=minecraft:item]",
        "command give @s minecraft:shears 1", "wait 2", "select 1", "wait 2",
        "command tp @s 0.5 65 0.5", "command gamemode survival", "wait 4",
        "look-at 3.5 65.5 0.5", "state", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(state["looking_at"]["block"]["pos"] == [3, 65, 0] and
          inventory["counts"] == {"minecraft:shears": 1} and not ground["entities"],
          "pumpkin carving: clean survival aim")
    fruit_block, inventory, ground = batch.script("pumpkin-carve-action", [
        "mouse right click", "wait 8", "block 3 65 0", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(fruit_block["block"] == "minecraft:carved_pumpkin", "pumpkin carving: carved block")
    check(inventory["counts"] == {"minecraft:shears": 1} and ground_counts(ground)["minecraft:pumpkin_seeds"] > 0,
          "pumpkin carving: ordinary shears and seed result")
    batch.passed.append("pumpkin carving with shears remains ordinary interaction")

    decorative_case(batch, "pumpkin", 4)
    decorative_case(batch, "melon", 8)

    for fruit, stem, attached, z, side in [
        ("pumpkin", "pumpkin_stem", "attached_pumpkin_stem", 12, "west"),
        ("melon", "melon_stem", "attached_melon_stem", 16, "north"),
    ]:
        stem_pos = linked_setup(batch, fruit + "-no-drops", fruit, stem, attached, z, side, drops=False)
        fruit_block, stem_block, inventory, ground = action(batch, fruit + "-no-drops", z, stem_pos)
        check(fruit_block["block"] == "minecraft:air" and stem_block["state"] == f"minecraft:{stem}[age=7]",
              fruit + ": drops-off stem result")
        check(inventory == {"minecraft:wheat_seeds": 5} and not ground["entities"], fruit + ": no invented loot")
        batch.passed.append(fruit + ": associated harvest with drops disabled")

    commands = [
        "command gamemode creative", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 1000", "command clear @s",
        "command gamemode survival", "wait 1600",
    ]
    for fruit, attached, z, (sx, sz) in growth_sites:
        commands += [f"block 3 65 {z}", f"block {sx} 65 {sz}"]
    commands.append("command gamerule minecraft:random_tick_speed 3")
    replies = batch.script("shared-growth", commands, timeout=180)
    observed = replies[-5:-1]
    for index, (fruit, attached, _, _) in enumerate(growth_sites):
        fruit_block, stem_block = observed[index * 2:index * 2 + 2]
        check(fruit_block["block"] == f"minecraft:{fruit}", fruit + ": fruit regrew")
        check(stem_block["block"] == f"minecraft:{attached}", fruit + ": stem reattached")
        batch.passed.append(fruit + ": accelerated fruit regrowth and stem reattachment")

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
        (batch.run / "stem-fruit-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
