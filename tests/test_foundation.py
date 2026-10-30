"""Structural source checks only; these do not compile Rust or resolve real hooks."""

import json
from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "mixins" / "right-click-crops"
HORIZON_REVISION = "64e298952d8bbb1188108bd4de68be2ab25d202b"
MIXINS_REVISION = "3f99a5c60dfa311cc365524c44ae2fd799bfa1de"


def read_toml(path):
    with path.open("rb") as source:
        return tomllib.load(source)


class FoundationSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cargo = read_toml(ROOT / "Cargo.toml")
        cls.lock = read_toml(ROOT / "Cargo.lock")
        cls.manifest = read_toml(BUNDLE / "horizon-mixin.toml")
        cls.compatibility = json.loads((ROOT / "compatibility.json").read_text())
        cls.runtime = (BUNDLE / "runtime.rs").read_text()

    def test_game_revision_is_the_approved_exact_pin(self):
        self.assertEqual(self.compatibility["horizon_revision"], HORIZON_REVISION)
        self.assertEqual(
            self.manifest["compatibility"]["horizon_revision"], HORIZON_REVISION
        )
        self.assertEqual(
            self.compatibility["horizon_source_tag"],
            "nightly-source/2026-10-29-64e2989",
        )

    def test_mixins_pin_and_validation_status_are_explicit(self):
        self.assertEqual(self.compatibility["horizon_mixins_revision"], MIXINS_REVISION)
        self.assertIn(
            self.compatibility["status"],
            {"wheat-implementation-in-progress", "wheat-compiled-gameplay-pending", "wheat-partially-gameplay-tested", "field-crops-compiled-gameplay-pending", "field-crops-partially-gameplay-tested", "wart-cocoa-implementation-in-progress", "wart-cocoa-compiled-gameplay-pending", "wart-cocoa-partially-gameplay-tested", "flower-crops-implementation-in-progress", "flower-crops-partially-gameplay-tested", "vertical-plants-implementation-in-progress", "vertical-plants-partially-gameplay-tested", "kelp-vines-implementation-in-progress", "kelp-vines-partially-gameplay-tested", "stem-fruits-implementation-in-progress", "stem-fruits-partially-gameplay-tested"},
        )
        self.assertIn(self.compatibility["validation"]["gameplay"], {"not-run", "partial", "not-run-dev3;wheat-partial-dev2", "partial-dev3", "not-run-dev4;field-crops-partial-dev3", "partial-dev4", "not-run-dev5;wart-cocoa-partial-dev4", "partial-dev5", "not-run-dev6;flower-crops-partial-dev5", "partial-dev6", "not-run-dev7;vertical-plants-partial-dev6", "partial-dev7", "not-run-dev8;kelp-vines-partial-dev7", "partial-dev8"})
        if self.compatibility["status"] in {"wheat-compiled-gameplay-pending", "wheat-partially-gameplay-tested"}:
            self.assertTrue(self.compatibility["validation"]["native_build"].startswith("passed"))
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed")
            self.assertEqual(self.compatibility["validation"]["native_runtime_tests"], "9-passed-159-upstream-filtered")
        if self.compatibility["status"] == "wheat-partially-gameplay-tested":
            self.assertEqual(self.compatibility["validation"]["game_launch"], "passed")
            self.assertEqual(self.compatibility["validation"]["disabled_after_process_restart"], "passed-foundation-and-wheat-dev2")
        if self.compatibility["status"].startswith("field-crops-"):
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "11-passed-dev3")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev3-four-field-crop-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev3-offline")
        if self.compatibility["status"] in {"wart-cocoa-compiled-gameplay-pending", "wart-cocoa-partially-gameplay-tested"}:
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "11-passed-dev4")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev4-six-crop-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev4-offline")
        if self.compatibility["status"] == "flower-crops-partially-gameplay-tested":
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "11-passed-dev5")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev5-eight-crop-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev5-offline-final-fix")
        if self.compatibility["status"] == "vertical-plants-partially-gameplay-tested":
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "12-passed-dev6")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev6-eleven-family-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev6-offline")
        if self.compatibility["status"] == "kelp-vines-partially-gameplay-tested":
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "12-passed-dev7")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev7-fourteen-family-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev7-offline")
        if self.compatibility["status"] == "stem-fruits-partially-gameplay-tested":
            self.assertEqual(self.compatibility["validation"]["standalone_rust_tests"], "13-passed-dev8")
            self.assertEqual(self.compatibility["validation"]["wheat_ast_audit"], "passed-dev8-sixteen-family-stage")
            self.assertEqual(self.compatibility["validation"]["native_build"], "passed-dev8-offline")
        self.assertEqual(self.compatibility["mixin_schema"], 5)
        self.assertEqual(self.compatibility["hook_policy"], "direct-revision-pinned")

    def test_package_and_bundle_versions_agree(self):
        self.assertEqual(
            self.cargo["package"]["version"], self.manifest["mod"]["version"]
        )
        version = re.search(r'pub const MOD_VERSION: &str = "([^"]+)";', self.runtime)
        self.assertIsNotNone(version)
        self.assertEqual(version.group(1), self.manifest["mod"]["version"])

    def test_runtime_identity_matches_the_bundle(self):
        self.assertEqual(self.manifest["mod"]["id"], "right-click-crops")
        self.assertIn('pub const MOD_ID: &str = "right-click-crops";', self.runtime)

    def test_the_library_and_injected_module_share_one_runtime(self):
        modules = self.manifest["module"]
        self.assertEqual(len(modules), 2)
        module = modules[0]
        self.assertEqual(module["file"], "crates/horizon-client/src/game.rs")
        self.assertEqual(module["name"], "right_click_crops")
        self.assertEqual(
            (ROOT / self.cargo["lib"]["path"]).resolve(),
            (BUNDLE / module["source"]).resolve(),
        )

    def test_every_payload_stays_inside_the_bundle(self):
        names = [m["source"] for m in self.manifest["module"]]
        names += [hook["helper"] for hook in self.manifest["injection"]]
        for name in names:
            with self.subTest(name=name):
                path = (BUNDLE / name).resolve()
                self.assertTrue(path.is_relative_to(BUNDLE.resolve()))
                self.assertTrue(path.is_file())

    def test_all_manifest_identifiers_are_unique(self):
        identifiers = [m["id"] for m in self.manifest["module"]]
        identifiers += [hook["id"] for hook in self.manifest["injection"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_only_four_bounded_head_hooks_are_declared(self):
        hooks = self.manifest["injection"]
        self.assertEqual(len(hooks), 4)
        for hook in hooks:
            self.assertEqual(hook["kind"], "HEAD")
            self.assertEqual(hook.get("cancellable", False), hook["id"] in {"harvest-wheat", "consume-local-wheat-click"})

    def test_hook_targets_match_the_researched_declaring_modules(self):
        targets = {hook["id"]: hook["target"] for hook in self.manifest["injection"]}
        self.assertEqual(
            targets,
            {
                "register-foundation": "horizon_client::game::native_hooks::Game<'_>::native_mods",
                "report-foundation-start": "horizon_client::game::native_hooks::Game<'_>::native_tick",
                "harvest-wheat": "horizon_client::game::Game<'_>::use_hand",
                "consume-local-wheat-click": "horizon_client::game::remote::Game<'_>::remote_block_reacts",
            },
        )

    def test_bindings_do_not_evaluate_game_calls(self):
        for hook in self.manifest["injection"]:
            for binding in hook["bindings"]:
                self.assertIn(binding["value"], {"mods", "&*self", "&mut *self", "block_hit", "hit"})
                if binding["name"] == "game":
                    self.assertIn(binding["ty"], {"&crate::game::Game<'_>", "&mut crate::game::Game<'_>"})
                if binding["name"] == "block_hit":
                    self.assertEqual(binding["ty"], "Option<&crate::game::Hit>")

    def test_the_standalone_library_needs_no_external_dependencies_or_build_script(self):
        self.assertFalse(self.cargo["package"]["publish"])
        for section in ("dependencies", "dev-dependencies", "build-dependencies", "target"):
            self.assertNotIn(section, self.cargo)
        self.assertFalse((ROOT / "build.rs").exists())
        self.assertEqual(self.cargo["lints"]["rust"]["unsafe_code"], "forbid")

    def test_the_lockfile_contains_only_this_package(self):
        self.assertEqual(self.lock["version"], 4)
        self.assertEqual(
            self.lock["package"],
            [{"name": self.cargo["package"]["name"], "version": self.cargo["package"]["version"]}],
        )

    def test_runtime_payload_has_no_unsupported_file_level_constructs(self):
        self.assertNotIn("#![", self.runtime)
        self.assertNotIn("//!", self.runtime)
        self.assertNotRegex(self.runtime, r"\binclude(?:_str|_bytes)?!|#\s*\[path\s*=")
        self.assertNotRegex(self.runtime, r"(?m)^\s*(?:pub\s+)?mod\s+\w+\s*;")

    def test_no_break_hook_or_client_world_mutation_is_added(self):
        for hook in self.manifest["injection"]:
            self.assertNotIn("break_block", hook["target"])
        client = (BUNDLE / "client_reacts.rs").read_text()
        self.assertNotRegex(client, r"block_loot_at|pop_resource|set_block|consume_held")
        self.assertIn("full game restart", self.runtime)

    def test_gameplay_uses_one_ordinary_loot_path_per_harvest_adapter(self):
        gameplay = (BUNDLE / "gameplay.rs").read_text()
        self.assertEqual(gameplay.count("game.block_loot_at("), 3)
        self.assertEqual(gameplay.count("b.set_block("), 7)
        self.assertNotRegex(gameplay, r"\.break_block\(|\.native_give\(|\.consume_held\(")
        self.assertIn("game.integrated.is_some()", gameplay)
        self.assertIn("game.lan_acting_uuid == Some(server.owner)", gameplay)
        self.assertIn("(0..36).chain", gameplay)
        self.assertIn("if !written", gameplay)
        self.assertIn("if let Some((upper_pos, upper_state)) = upper", gameplay)
        self.assertIn("let _ = b.set_block(level, ticks, upper_at, upper_state, UPDATE_ALL)", gameplay)
        self.assertIn("UPDATE_CLIENTS | UPDATE_KNOWN_SHAPE | UPDATE_SUPPRESS_DROPS", gameplay)

    def test_gameplay_uses_the_same_explicit_profile_for_maturity_and_payment(self):
        gameplay = (BUNDLE / "gameplay.rs").read_text()
        self.assertIn("core::crop_profile(&game.res.facts().get(state).name)?", gameplay)
        self.assertIn("crop.mature_age.is_some_and", gameplay)
        self.assertIn("core::select_payment(crop.planting_item,", gameplay)
        self.assertIn("core::spend_one(game.stack_in_mut(slot), crop.planting_item)", gameplay)
        self.assertIn("crop.support_below.is_some_and", gameplay)
        self.assertIn("b.can_survive(level, ticks, at, young)", gameplay)

    def test_bundle_source_and_metadata_use_english_text(self):
        paths = list(BUNDLE.glob("*.rs")) + [ROOT / "compatibility.json"]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(), r"[\u0400-\u04ff]")


if __name__ == "__main__":
    unittest.main()
