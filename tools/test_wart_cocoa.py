"""Grouped survival harvest checks for nether wart and attached cocoa.

Start an isolated game with the project's existing helper first. Each control
phase uses a single scripted connection and writes receipts inside that run.
"""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts, ground_items


CROPS = (
    ("nether_wart", 3, "nether_wart", "wheat_seeds", -8, "minecraft:soul_sand"),
    ("cocoa", 2, "cocoa_beans", "beetroot_seeds", -4, "minecraft:stone"),
)


def crop_state(block, crop, age):
    state = block["state"]
    check(block["block"] == f"minecraft:{crop}" and f"age={age}" in state,
          f"{crop}: expected age {age}, got {state}")
    if crop == "cocoa":
        check("facing=east" in state, "cocoa: attachment direction was changed")


def fixture(batch, name, crop, age, item, count, z, support, drops=True):
    commands = [
        "command gamemode creative", "command clear @s",
        f"command gamerule minecraft:block_drops {str(drops).lower()}",
        "command gamerule minecraft:random_tick_speed 0",
        f"fill 0 65 {z-2} 4 67 {z+2} minecraft:air --confirm",
        f"setblock 3 64 {z} {support} --confirm",
    ]
    if crop == "cocoa":
        commands.append(f"setblock 4 65 {z} minecraft:jungle_log --confirm")
    plant = f"minecraft:{crop}[age={age}" + (",facing=east]" if crop == "cocoa" else "]")
    commands += [f"setblock 3 65 {z} {plant} --confirm", "command kill @e[type=minecraft:item]"]
    if count:
        commands.append(f"command give @s minecraft:{item} {count}")
    commands += [
        f"command tp @s 0.5 65 {z-0.5}", "select 9", "command gamemode survival",
        "wait 3", f"look-at-block 3 65 {z}", "state", "inventory", "entities 16 minecraft:item",
    ]
    state, inventory, ground = batch.script(name + "-setup", commands)[-3:]
    check(state["gamemode"] == "survival" and
          state["looking_at"]["block"]["pos"] == [3, 65, z], name + ": survival aim")
    crop_state(state["looking_at"]["block"], crop, age)
    check(inventory["counts"] == ({f"minecraft:{item}": count} if count else {}), name + ": clean inventory")
    check(not ground["entities"], name + ": clean ground")


def click(batch, name, z, support, cocoa=False):
    results = batch.script(name + "-action", [
        "mouse right click", "wait 6", f"block 3 65 {z}", f"block 3 64 {z}",
        *( [f"block 4 65 {z}"] if cocoa else [] ),
        "inventory", "entities 16 minecraft:item", "state",
    ])
    plant, beneath, *rest = results[-(6 if cocoa else 5):]
    attachment = rest.pop(0) if cocoa else None
    inventory, ground, state = rest
    check(beneath["block"] == support, name + ": soil preserved")
    if cocoa:
        check(attachment["block"] == "minecraft:jungle_log", name + ": cocoa attachment preserved")
    check(state["gamemode"] == "survival", name + ": survival after click")
    return plant, inventory["counts"], ground


def run(batch):
    batch.script("options", ["options-set pauseOnLostFocus false", "time 6000"])
    for crop, mature, item, wrong, z, support in CROPS:
        cocoa = crop == "cocoa"
        name = crop + "-loot"
        fixture(batch, name, crop, mature, item, 9, z, support)
        plant, inv, ground = click(batch, name, z, support, cocoa)
        crop_state(plant, crop, 0)
        check(inv == {f"minecraft:{item}": 9}, name + ": generated loot pays before inventory")
        count = ground_counts(ground)
        check(set(count) == {f"minecraft:{item}"}, name + ": only ordinary ground loot")
        check((count[f"minecraft:{item}"] == 2 if cocoa else 1 <= count[f"minecraft:{item}"] <= 3),
              name + ": exactly one reserved planting item")
        batch.passed.append(name + ": loot pays and required support state is preserved")

        # A young crop is not a new harvest even when clicked immediately again.
        aimed = batch.script(crop + "-repeat-aim", [f"look-at-block 3 65 {z}", "state"])[-1]
        check(aimed["looking_at"]["block"]["pos"] == [3, 65, z], crop + ": young crop aimed")
        again, remaining, items = click(batch, crop + "-repeat", z, support, cocoa)
        crop_state(again, crop, 0)
        check(remaining == inv and ground_items(items) == ground_items(ground), crop + ": repeat had no effect")
        batch.passed.append(crop + ": immature repeat")

        for label, age, supply, amount, drops, expected_age, expected_amount in [
            ("immature", mature-1, item, 2, True, mature-1, 2),
            ("fallback", mature, item, 2, False, 0, 1),
            ("missing", mature, item, 0, False, None, 0),
            ("wrong", mature, wrong, 2, False, None, 2),
        ]:
            case = crop + "-" + label
            fixture(batch, case, crop, age, supply, amount, z, support, drops)
            after, inventory, entities = click(batch, case, z, support, cocoa)
            if expected_age is None:
                check(after["block"] == "minecraft:air", case + ": harvest without replant")
            else:
                crop_state(after, crop, expected_age)
            check(inventory == ({f"minecraft:{supply}": expected_amount} if expected_amount else {}),
                  case + ": exact payment")
            check(not entities["entities"], case + ": controlled loot remains empty")
            batch.passed.append(case)

        fixture(batch, crop + "-growth", crop, mature, item, 2, z, support, drops=False)
        replanted, inventory, _ = click(batch, crop + "-growth", z, support, cocoa)
        crop_state(replanted, crop, 0)
        check(inventory == {f"minecraft:{item}": 1}, crop + ": paid replant for growth")

    grown = batch.script("shared-growth", [
        "command gamemode creative", "command gamerule minecraft:block_drops true",
        "command gamerule minecraft:random_tick_speed 250", "command gamemode survival",
        "wait 1200", "block 3 65 -8", "block 3 65 -4",
        "command gamerule minecraft:random_tick_speed 3",
    ], timeout=150)
    for (crop, age, _, _, _, _), block in zip(CROPS, grown[-3:-1]):
        crop_state(block, crop, age)
        batch.passed.append(crop + ": accelerated random-tick regrowth, not default timing")

    batch.fixture("wheat-regression", "wheat", 7, "wheat_seeds", 3, -8)
    plant, inventory, ground = batch.click("wheat-regression", -8)
    check(plant["state"] == "minecraft:wheat[age=0]" and inventory == {"minecraft:wheat_seeds": 3}
          and ground_counts(ground)["minecraft:wheat"] == 1, "wheat regression")
    batch.passed.append("wheat regression")

    state = batch.script("berry-setup", [
        "command gamemode creative", "command clear @s", "setblock 3 65 -8 minecraft:air --confirm",
        "setblock 3 64 -8 minecraft:dirt --confirm",
        "setblock 3 65 -8 minecraft:sweet_berry_bush[age=3] --confirm",
        "command kill @e[type=minecraft:item]", "command gamemode survival",
        "look-at-block 3 65 -8", "state",
    ])[-1]
    check(state["gamemode"] == "survival" and state["looking_at"]["block"]["pos"] == [3, 65, -8],
          "berry: survival aim")
    berry, inv, ground = batch.script("berry-action", [
        "mouse right click", "wait 6", "block 3 65 -8", "inventory", "entities 16 minecraft:item",
    ])[-3:]
    check(berry["state"] == "minecraft:sweet_berry_bush[age=1]" and not inv["counts"]
          and set(ground_counts(ground)) == {"minecraft:sweet_berries"}, "ordinary berry harvest")
    batch.passed.append("berry regression")


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
        (batch.run / "wart-cocoa-results.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed),
                          "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
