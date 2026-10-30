"""Compact survival checks against an already running, isolated Horizon instance.

Uses horizon-ctl's script command to batch requests. No builds, downloads or
game launches. Detailed commands/replies stay beside the isolated test world.
"""

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
CROPS = (
    ("carrots", 7, "carrot", "beetroot_seeds", -8),
    ("potatoes", 7, "potato", "poisonous_potato", -4),
    ("beetroots", 3, "beetroot_seeds", "beetroot", 0),
)


class Batch:
    def __init__(self, session):
        self.run = Path(session["run"]).resolve()
        if not self.run.is_relative_to(ROOT / ".local" / "runs"):
            raise ValueError("Only project-local isolated runs are accepted")
        self.home = Path(session["gameHome"]).resolve()
        if not self.home.is_relative_to(self.run):
            raise ValueError("Game home must be inside the isolated run")
        self.ctl = session["ctl"]
        self.socket = session["socket"]
        self.env = os.environ.copy()
        for key, child in {
            "HORIZON_HOME": "game", "HORIZON_LAUNCHER_HOME": "launcher",
            "XDG_DATA_HOME": "xdg-data", "XDG_CONFIG_HOME": "xdg-config",
            "XDG_RUNTIME_DIR": "runtime", "HORIZON_LAUNCHER_TRASH": "trash",
            "HORIZON_LAUNCHER_DESKTOP": "desktop",
        }.items():
            self.env[key] = str(self.run / child)
        self.env.update(HORIZON_LAUNCHER_NO_SELF_UPDATE="1", HORIZON_NO_AUDIO="1",
                        HORIZON_LAUNCHER_CLIPBOARD=str(self.run / "clipboard.txt"))
        self.calls = 0
        self.passed = []

    def script(self, label, commands, timeout=60):
        path = self.run / f"batch-{label}.ctl"
        path.write_text("\n".join(commands) + "\n", encoding="utf-8")
        result = subprocess.run(
            [self.ctl, "--socket", self.socket, "script", str(path)],
            cwd=self.home, env=self.env, capture_output=True, text=True,
            encoding="utf-8", timeout=timeout,
        )
        self.calls += 1
        (self.run / f"batch-{label}.jsonl").write_text(result.stdout, encoding="utf-8")
        (self.run / f"batch-{label}.err.txt").write_text(result.stderr, encoding="utf-8")
        replies = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        if result.returncode or len(replies) != len(commands) or any("error" in r for r in replies):
            raise AssertionError(f"Control batch failed: {label}; inspect local receipts")
        return replies

    def fixture(self, label, crop, age, item, count, z, drops=True):
        commands = [
            "command gamemode creative", "command clear @s",
            f"command gamerule minecraft:block_drops {str(drops).lower()}",
            "command gamerule minecraft:random_tick_speed 0",
            f"fill 0 65 {z-2} 4 67 {z+2} minecraft:air --confirm",
            f"setblock 3 64 {z+2} minecraft:water --confirm",
            f"setblock 3 64 {z} minecraft:farmland[moisture=7] --confirm",
            f"setblock 3 65 {z} minecraft:{crop}[age={age}] --confirm",
            "command kill @e[type=minecraft:item]",
        ]
        if count:
            commands.append(f"command give @s minecraft:{item} {count}")
        commands += [
            f"command tp @s 0.5 65 {z-0.5}", "select 9",
            "command gamemode survival", "wait 3",
            f"look-at 3.5 65.06 {z+0.5}", "state", "inventory",
            "entities 16 minecraft:item",
        ]
        state, inventory, ground = self.script(label + "-setup", commands)[-3:]
        check(state["gamemode"] == "survival", label + ": survival precondition")
        check(state["looking_at"]["block"]["pos"] == [3, 65, z], label + ": aim")
        check(state["looking_at"]["block"]["state"] == f"minecraft:{crop}[age={age}]", label + ": starting age")
        check(inventory["counts"] == ({f"minecraft:{item}": count} if count else {}), label + ": starting inventory")
        check(not ground["entities"], label + ": clean ground")
        return inventory

    def click(self, label, z):
        replies = self.script(label + "-action", [
            "mouse right click", "wait 6", f"block 3 65 {z}",
            f"block 3 64 {z}", "inventory", "entities 16 minecraft:item", "state",
        ])
        crop, soil, inventory, ground, state = replies[-5:]
        check(soil["state"] == "minecraft:farmland[moisture=7]", label + ": soil")
        check(state["gamemode"] == "survival", label + ": survival after action")
        return crop, inventory["counts"], ground

    def cases(self, smoke=False):
        self.script("initial-options", ["options-set pauseOnLostFocus false", "time 6000"])
        for crop, mature, item, wrong, z in CROPS:
            self.fixture(crop + "-loot", crop, mature, item, 9, z)
            block, inventory, ground = self.click(crop + "-loot", z)
            check(block["state"] == f"minecraft:{crop}[age=0]", crop + ": normal replant")
            # Beetroot can naturally roll no planting seeds. Fallback then costs one.
            remaining = inventory.get(f"minecraft:{item}", 0)
            check(remaining in ({8, 9} if crop == "beetroots" else {9}), crop + ": loot priority")
            check(set(inventory) <= {f"minecraft:{item}"}, crop + ": no inventory loot")
            counts = ground_counts(ground)
            allowed = {f"minecraft:{item}", "minecraft:poisonous_potato"} if crop == "potatoes" else {f"minecraft:{item}"}
            if crop == "beetroots":
                allowed.add("minecraft:beetroot")
                check(counts["minecraft:beetroot"] == 1, "one ordinary beetroot")
                if remaining == 8:
                    check(counts["minecraft:beetroot_seeds"] == 0, "seedless beetroot fallback")
            check(set(counts) <= allowed, crop + ": no unrelated drops")
            if crop != "beetroots":
                check(counts[f"minecraft:{item}"] >= 1, crop + ": ground harvest")
            self.passed.append(crop + ": ordinary loot, replant, payment priority, ground drops")
            # Explicitly aim at the short age-zero plant before the repeat.
            self.script(crop + "-repeat-aim", [f"look-at 3.5 65.06 {z+0.5}", "state"])
            again, inv2, ground2 = self.click(crop + "-repeat", z)
            check(again["state"] == block["state"] and inv2 == inventory and
                  ground_items(ground2) == ground_items(ground), crop + ": repeat has no effects")
            self.passed.append(crop + ": repeated click on young replant")
            if smoke:
                continue
            for label, age, supply, count, drops, expected_age, expected_count in [
                ("immature", mature-1, item, 2, True, mature-1, 2),
                ("fallback", mature, item, 2, False, 0, 1),
                ("missing", mature, item, 0, False, None, 0),
                ("wrong", mature, wrong, 2, False, None, 2),
            ]:
                name = crop + "-" + label
                self.fixture(name, crop, age, supply, count, z, drops)
                after, inv, entities = self.click(name, z)
                expected = "minecraft:air" if expected_age is None else f"minecraft:{crop}[age={expected_age}]"
                check(after["state"] == expected, name + ": resulting block")
                check(inv == ({f"minecraft:{supply}": expected_count} if expected_count else {}), name + ": exact inventory")
                check(not entities["entities"], name + ": no invented loot")
                self.passed.append(name)
            # Leave a real paid replant for the shared random-growth observation.
            self.fixture(crop + "-regrow", crop, mature, item, 2, z, drops=False)
            after, inv, _ = self.click(crop + "-regrow", z)
            check(after["state"] == f"minecraft:{crop}[age=0]" and inv.get(f"minecraft:{item}") == 1, crop + ": regrowth starts from actual paid replant")

        if not smoke:
            grown = self.script("shared-growth", [
                "command gamemode creative",
                "command gamerule minecraft:block_drops true",
                "command gamerule minecraft:random_tick_speed 1000",
                "command gamemode survival", "wait 1200",
                *[f"block 3 65 {z}" for _, _, _, _, z in CROPS],
                "command gamerule minecraft:random_tick_speed 3",
            ], timeout=150)[-4:-1]
            for (crop, mature, _, _, _), block in zip(CROPS, grown):
                check(block["state"] == f"minecraft:{crop}[age={mature}]", crop + ": accelerated natural regrowth")
                self.passed.append(crop + ": accelerated natural regrowth (not default-speed timing)")

        self.fixture("wheat-regression", "wheat", 7, "wheat_seeds", 3, -8)
        crop, inv, ground = self.click("wheat-regression", -8)
        check(crop["state"] == "minecraft:wheat[age=0]" and inv == {"minecraft:wheat_seeds": 3}
              and ground_counts(ground)["minecraft:wheat"] == 1, "wheat regression")
        self.passed.append("wheat regression")

        if not smoke:
            for name, support, plant, target in [
                ("berry-bush", "setblock 3 64 -8 minecraft:dirt --confirm",
                 "minecraft:sweet_berry_bush[age=3]", "minecraft:sweet_berries"),
                ("glow-vine", "setblock 3 66 -8 minecraft:stone --confirm",
                 "minecraft:cave_vines[age=0,berries=true]", "minecraft:glow_berries"),
            ]:
                state = self.script(name + "-setup", [
                    "command gamemode creative", "command clear @s",
                    "setblock 3 65 -8 minecraft:air --confirm", support,
                    f"setblock 3 65 -8 {plant} --confirm",
                    "command kill @e[type=minecraft:item]",
                    "command tp @s 0.5 65 -8.5", "select 9",
                    "command gamemode survival", "wait 3",
                    "look-at-block 3 65 -8", "state",
                ])[-1]
                check(state["gamemode"] == "survival" and
                      state["looking_at"]["block"]["pos"] == [3, 65, -8], name + ": survival aim")
                block, inv, ground = self.script(name + "-action", [
                    "mouse right click", "wait 6", "block 3 65 -8", "inventory",
                    "entities 16 minecraft:item",
                ])[-3:]
                check(not inv["counts"], name + ": no inventory charge")
                counts = ground_counts(ground)
                check(set(counts) == {target} and counts[target] > 0, name + ": ordinary drops only")
                check(block["state"] == "minecraft:sweet_berry_bush[age=1]" if name == "berry-bush"
                      else "berries=false" in block["state"] and counts[target] == 1,
                      name + ": ordinary harvested state")
                self.passed.append(name + " regression")


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def ground_counts(ground):
    counts = Counter()
    for entity in ground["entities"]:
        counts[entity["item"]["item"]] += entity["item"]["count"]
    return counts


def ground_items(ground):
    return sorted((e["id"], e["item"]["item"], e["item"]["count"]) for e in ground["entities"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, required=True, help="Isolated control session JSON")
    parser.add_argument("--smoke", action="store_true", help="Only new crop/repeat cases and wheat regression")
    args = parser.parse_args()
    batch = Batch(json.loads(args.session.read_text(encoding="utf-8-sig")))
    result = {"status": "failed", "passed": batch.passed, "smoke": args.smoke}
    try:
        batch.cases(args.smoke)
        result["status"] = "passed"
    except Exception as error:
        result["failure"] = str(error)
        raise
    finally:
        result["control_processes"] = batch.calls
        (batch.run / "field-crop-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "passed": len(batch.passed), "control_processes": batch.calls}))


if __name__ == "__main__":
    main()
