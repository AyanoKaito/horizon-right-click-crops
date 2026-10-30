"""Compact survival checks that ordinary sweet and glow berry use is preserved."""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts


def sweet_berries(batch):
    state, inventory, ground = batch.script("sweet-setup", [
        "command gamemode creative", "command clear @s", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 0", "fill 0 64 -10 5 68 -6 minecraft:air --confirm",
        "setblock 0 64 -9 minecraft:stone --confirm", "setblock 3 64 -8 minecraft:dirt --confirm",
        "setblock 3 65 -8 minecraft:sweet_berry_bush[age=3] --confirm",
        "command kill @e[type=minecraft:item]", "command give @s minecraft:wheat_seeds 5", "select 9",
        "command tp @s 0.5 65 -8.5", "command gamemode survival", "wait 4",
        "look-at-block 3 65 -8", "state", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(state["gamemode"] == "survival" and state["looking_at"]["block"]["pos"] == [3, 65, -8],
          "sweet berries: survival aim")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5} and not ground["entities"],
          "sweet berries: clean fixture")

    bush, inventory, ground = batch.script("sweet-harvest", [
        "mouse right click", "wait 8", "block 3 65 -8", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    counts = ground_counts(ground)
    check(bush["state"] == "minecraft:sweet_berry_bush[age=1]", "sweet berries: ordinary harvested age")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5}
          and set(counts) == {"minecraft:sweet_berries"} and 2 <= counts["minecraft:sweet_berries"] <= 3,
          "sweet berries: one ordinary harvest and no payment")
    batch.passed.append("sweet berries: ordinary mature harvest, no payment or duplicate")

    before = ground_counts(ground)
    bush, inventory, ground = batch.script("sweet-repeat", [
        "look-at-block 3 65 -8", "mouse right click", "wait 6", "block 3 65 -8",
        "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(bush["state"] == "minecraft:sweet_berry_bush[age=1]"
          and inventory["counts"] == {"minecraft:wheat_seeds": 5}
          and ground_counts(ground) == before, "sweet berries: empty repeat")
    batch.passed.append("sweet berries: post-harvest repeat passthrough")

    bush, inventory, ground = batch.script("sweet-bone-meal", [
        "command gamemode creative", "command clear @s", "command kill @e[type=minecraft:item]",
        "command give @s minecraft:bone_meal 2", "wait 2", "select 1", "wait 2",
        "command gamemode survival", "look-at-block 3 65 -8", "mouse right click", "wait 8",
        "block 3 65 -8", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(bush["block"] == "minecraft:sweet_berry_bush" and "age=1" not in bush["state"],
          "sweet berries: ordinary bone meal growth")
    check(inventory["counts"] == {"minecraft:bone_meal": 1} and not ground["entities"],
          "sweet berries: exact bone meal use without harvest")
    batch.passed.append("sweet berries: ordinary bone meal interaction")


def glow_berries(batch):
    state, inventory, ground = batch.script("glow-setup", [
        "command gamemode creative", "command clear @s", "fill 0 64 -6 5 68 -2 minecraft:air --confirm",
        "setblock 0 64 -5 minecraft:stone --confirm", "setblock 3 66 -4 minecraft:stone --confirm",
        "setblock 3 65 -4 minecraft:cave_vines[age=0,berries=true] --confirm",
        "command kill @e[type=minecraft:item]", "command give @s minecraft:wheat_seeds 5", "select 9",
        "command tp @s 0.5 65 -4.5", "command gamemode survival", "wait 4",
        "look-at-block 3 65 -4", "state", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check(state["gamemode"] == "survival" and state["looking_at"]["block"]["pos"] == [3, 65, -4],
          "glow berries: survival aim")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5} and not ground["entities"],
          "glow berries: clean fixture")

    vine, inventory, ground = batch.script("glow-harvest", [
        "mouse right click", "wait 8", "block 3 65 -4", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check("berries=false" in vine["state"], "glow berries: ordinary harvested state")
    check(inventory["counts"] == {"minecraft:wheat_seeds": 5}
          and ground_counts(ground) == {"minecraft:glow_berries": 1},
          "glow berries: one ordinary harvest and no payment")
    batch.passed.append("glow berries: ordinary harvest, no payment or duplicate")

    before = ground_counts(ground)
    vine, inventory, ground = batch.script("glow-repeat", [
        "look-at-block 3 65 -4", "mouse right click", "wait 6", "block 3 65 -4",
        "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check("berries=false" in vine["state"] and inventory["counts"] == {"minecraft:wheat_seeds": 5}
          and ground_counts(ground) == before, "glow berries: empty repeat")
    batch.passed.append("glow berries: post-harvest repeat passthrough")

    vine, inventory, ground = batch.script("glow-bone-meal", [
        "command gamemode creative", "command clear @s", "command kill @e[type=minecraft:item]",
        "command give @s minecraft:bone_meal 2", "wait 2", "select 1", "wait 2",
        "command gamemode survival", "look-at-block 3 65 -4", "mouse right click", "wait 8",
        "block 3 65 -4", "inventory", "entities 20 minecraft:item",
    ])[-3:]
    check("berries=true" in vine["state"], "glow berries: ordinary bone meal berries")
    check(inventory["counts"] == {"minecraft:bone_meal": 1} and not ground["entities"],
          "glow berries: exact bone meal use without harvest")
    batch.passed.append("glow berries: ordinary bone meal interaction")


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    sweet_berries(batch)
    glow_berries(batch)
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
        (batch.run / "berry-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
