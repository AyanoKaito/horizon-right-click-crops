"""Synthetic checks of the observation verifier, not gameplay acceptance."""

import copy
import importlib.util
from pathlib import Path
import unittest


MODULE = Path(__file__).resolve().parents[1] / "tools" / "compare_loot.py"
SPEC = importlib.util.spec_from_file_location("compare_loot", MODULE)
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


def records():
    ordinary = {
        "tool": "fortune3",
        "branch": "ordinary",
        "steps": [
            {"z": -8, "crop": "minecraft:air", "counts": {"minecraft:wheat": 1, VERIFIER.SEED: 3}},
            {"z": -5, "crop": "minecraft:air", "counts": {"minecraft:wheat": 2, VERIFIER.SEED: 7}},
        ],
    }
    harvest = copy.deepcopy(ordinary)
    harvest["branch"] = "harvest"
    for index, step in enumerate(harvest["steps"], 1):
        step["crop"] = "minecraft:wheat[age=0]"
        step["counts"][VERIFIER.SEED] -= index
    return ordinary, harvest


class LootComparisonTests(unittest.TestCase):
    def test_exact_one_seed_per_replant_is_accepted(self):
        ordinary, harvest = records()
        self.assertEqual(VERIFIER.compare_records(ordinary, harvest)["reserved_seeds"], 2)

    def test_free_replant_is_rejected(self):
        ordinary, harvest = records()
        harvest["steps"][0]["counts"][VERIFIER.SEED] += 1
        with self.assertRaises(ValueError):
            VERIFIER.compare_records(ordinary, harvest)

    def test_double_payment_is_rejected(self):
        ordinary, harvest = records()
        harvest["steps"][0]["counts"][VERIFIER.SEED] -= 1
        with self.assertRaises(ValueError):
            VERIFIER.compare_records(ordinary, harvest)

    def test_missing_or_bonus_unrelated_loot_is_rejected(self):
        for count in (0, 2):
            ordinary, harvest = records()
            harvest["steps"][0]["counts"]["minecraft:wheat"] = count
            with self.assertRaises(ValueError):
                VERIFIER.compare_records(ordinary, harvest)

    def test_extra_item_is_rejected(self):
        ordinary, harvest = records()
        harvest["steps"][0]["counts"]["minecraft:diamond"] = 1
        with self.assertRaises(ValueError):
            VERIFIER.compare_records(ordinary, harvest)

    def test_empty_or_mismatched_observations_are_rejected(self):
        for mutation in ("empty", "short", "tool", "target", "mature"):
            ordinary, harvest = records()
            if mutation == "empty":
                ordinary["steps"] = []
            elif mutation == "short":
                harvest["steps"].pop()
            elif mutation == "tool":
                harvest["tool"] = "empty"
            elif mutation == "target":
                harvest["steps"][0]["z"] = -99
            else:
                harvest["steps"][0]["crop"] = "minecraft:wheat[age=7]"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                VERIFIER.compare_records(ordinary, harvest)

        for invalid in (None, [], "record"):
            with self.subTest(record=invalid), self.assertRaises(ValueError):
                VERIFIER.compare_records(invalid, records()[1])
        ordinary, harvest = records()
        harvest["steps"][0] = None
        with self.assertRaises(ValueError):
            VERIFIER.compare_records(ordinary, harvest)

    def test_zero_remaining_seed_is_valid_when_one_was_reserved(self):
        ordinary, harvest = records()
        ordinary["steps"] = ordinary["steps"][:1]
        harvest["steps"] = harvest["steps"][:1]
        ordinary["steps"][0]["counts"][VERIFIER.SEED] = 1
        harvest["steps"][0]["counts"][VERIFIER.SEED] = 0
        self.assertEqual(VERIFIER.compare_records(ordinary, harvest)["crops"], 1)

    def test_invalid_counts_are_rejected(self):
        for count in (-1, True, "2", 1.5):
            ordinary, harvest = records()
            harvest["steps"][0]["counts"][VERIFIER.SEED] = count
            with self.subTest(count=count), self.assertRaises(ValueError):
                VERIFIER.compare_records(ordinary, harvest)


if __name__ == "__main__":
    unittest.main()
