"""Focused empty-hand/shears survival checks for both Nether vines.

Each fixture has three connected blocks. Harvest must keep one live anchor
and remove two blocks. Bare-hand loot may be 0, 1 or 2; shears must give 2.
Observed samples are not a statistical proof of the configured drop chance.
"""

import argparse
import json
from pathlib import Path

from test_field_crops import Batch, check, ground_counts
from test_kelp_vines import inspect, setup


def run(batch, trials):
    samples = []
    batch.script("vine-loot-options", ["options-set pauseOnLostFocus false", "time 6000"])
    for head, body, direction, z in (
        ("twisting_vines", "twisting_vines_plant", "up", -4),
        ("weeping_vines", "weeping_vines_plant", "down", 0),
    ):
        for tool in ("empty", "shears"):
            counts = []
            for trial in range(trials):
                label = f"{head}-{tool}-{trial + 1:02d}"
                # Creative commands prepare the isolated fixture; setup switches
                # to survival before any action. The unused shears stay in the bag.
                setup(batch, label, head, body, direction, z)
                inventory = batch.script(label + "-hand", [
                    "select " + ("9" if tool == "empty" else "1"), "inventory",
                ])[-1]
                held = inventory["held"]
                check(held is None if tool == "empty" else
                      held and held["item"] == "minecraft:shears", label + ": actual hand")
                check(not inventory["offhand"].get("item"), label + ": empty offhand")
                batch.script(label + "-click", ["mouse right click", "wait 10"])
                ground = inspect(batch, label + "-after", head, body, direction, z)
                drops = ground_counts(ground)
                count = drops.get(f"minecraft:{head}", 0)
                check(set(drops) <= {f"minecraft:{head}"}, label + ": no unrelated loot")
                check(count == 2 if tool == "shears" else 0 <= count <= 2,
                      label + ": ordinary drop bounds")
                counts.append(count)
                batch.passed.append(label)
            samples.append({"plant": head, "hand": tool, "harvests": trials,
                            "removed_blocks_per_harvest": 2, "drops": counts,
                            "total_drops": sum(counts), "zero_drop_harvests": counts.count(0)})
    return samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.trials <= 100:
        parser.error("--trials must be between 1 and 100")
    batch = Batch(json.loads(args.session.read_text(encoding="utf-8-sig")))
    result = {"status": "failed", "passed": batch.passed}
    try:
        result["samples"] = run(batch, args.trials)
        result["status"] = "passed"
    except Exception as error:
        result["failure"] = str(error)
        raise
    finally:
        result["control_processes"] = batch.calls
        (batch.run / "nether-vine-loot-results.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result))


if __name__ == "__main__":
    main()
