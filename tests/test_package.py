"""Checks for the deterministic Horizon native package builder."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("right_click_crops_package", ROOT / "tools" / "package.py")
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PackageTests(unittest.TestCase):
    def test_manifest_matches_the_release_identity(self):
        _, _, manifest = PACKAGE.metadata(ROOT)
        self.assertEqual(manifest["schema"], 1)
        self.assertEqual(manifest["id"], "right_click_crops")
        self.assertEqual(manifest["version"], "1.0.1")
        self.assertEqual(manifest["game"], "26.3")
        self.assertNotIn("hooks", manifest)

    def test_package_is_reproducible_and_source_only(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.hnmod"
            second = Path(directory) / "second.hnmod"
            first_result = PACKAGE.build(ROOT, first)
            second_result = PACKAGE.build(ROOT, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first_result["sha256"], second_result["sha256"])

            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
                self.assertEqual(names, sorted(names))
                self.assertEqual(names[0], "horizon-native.json")
                self.assertTrue(all("\\" not in name for name in names))
                self.assertTrue(
                    all(
                        name == "horizon-native.json"
                        or name.startswith("mixins/right_click_crops/")
                        for name in names
                    )
                )
                manifest = json.loads(archive.read("horizon-native.json"))
                self.assertEqual(manifest, first_result["manifest"])


if __name__ == "__main__":
    unittest.main()
