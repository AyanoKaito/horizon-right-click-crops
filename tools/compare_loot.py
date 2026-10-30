"""Compare cumulative ground loot from paired, identically saved game fixtures.

Development-only verifier. Does not launch a game or inspect player files.
Input records are produced by the isolated game harness; identical initial
saves and ordinary survival execution must be established by that harness.
"""

import argparse
import json
from pathlib import Path


SEED = "minecraft:wheat_seeds"


def positive_counts(value):
    if not isinstance(value, dict):
        raise ValueError("Ground counts must be an item-to-count object")
    result = {}
    for item, count in value.items():
        if not isinstance(item, str) or not item:
            raise ValueError("An item id must be a nonempty string")
        if type(count) is not int or count < 0:
            raise ValueError(f"Invalid ground count for {item}")
        if count:
            result[item] = count
    return result


def compare_records(ordinary, harvest):
    if not isinstance(ordinary, dict) or not isinstance(harvest, dict):
        raise ValueError("Each branch record must be a JSON object")
    if ordinary.get("branch") != "ordinary" or harvest.get("branch") != "harvest":
        raise ValueError("Expected an ordinary record and a harvest record")
    if ordinary.get("tool") != harvest.get("tool") or not ordinary.get("tool"):
        raise ValueError("The two fixtures must use the same tool")
    normal_steps = ordinary.get("steps")
    harvest_steps = harvest.get("steps")
    if not isinstance(normal_steps, list) or not normal_steps:
        raise ValueError("At least one ordinary harvest observation is required")
    if not isinstance(harvest_steps, list) or len(normal_steps) != len(harvest_steps):
        raise ValueError("The fixtures must observe the same number of crops")
    for paid, (normal, replanted) in enumerate(zip(normal_steps, harvest_steps), 1):
        if not isinstance(normal, dict) or not isinstance(replanted, dict):
            raise ValueError(f"Crop {paid} observations must be JSON objects")
        if "z" not in normal or normal["z"] != replanted.get("z"):
            raise ValueError(f"Target order differs at crop {paid}")
        if normal.get("crop") != "minecraft:air":
            raise ValueError(f"Ordinary breaking did not remove crop {paid}")
        if replanted.get("crop") != "minecraft:wheat[age=0]":
            raise ValueError(f"Harvest did not replant crop {paid}")
        expected = positive_counts(normal.get("counts"))
        actual = positive_counts(replanted.get("counts"))
        if expected.get(SEED, 0) < paid:
            raise ValueError(f"Ordinary loot cannot fund {paid} replants")
        expected[SEED] -= paid
        expected = {item: count for item, count in expected.items() if count}
        if expected != actual:
            raise ValueError(
                f"Loot mismatch at crop {paid}: expected {expected}, observed {actual}"
            )
    return {
        "status": "passed",
        "tool": ordinary["tool"],
        "crops": len(normal_steps),
        "reserved_seeds": len(normal_steps),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ordinary", type=Path)
    parser.add_argument("harvest", type=Path)
    args = parser.parse_args()
    try:
        ordinary = json.loads(args.ordinary.read_text(encoding="utf-8-sig"))
        harvest = json.loads(args.harvest.read_text(encoding="utf-8-sig"))
        result = compare_records(ordinary, harvest)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"Comparison failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
