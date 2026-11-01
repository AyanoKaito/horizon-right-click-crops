"""Structural source checks only; these do not compile Rust or resolve real hooks."""

import json
from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "mixins" / "right_click_crops"
HORIZON_REVISION = "9d979caa48a3bb58203319b9ea044db58c38e0d8"
MIXINS_REVISION = "4342a0bfbe71d4d14185528d64e496d6022f16a1"


def read_toml(path):
    with path.open("rb") as source:
        return tomllib.load(source)


class BundleSourceTests(unittest.TestCase):
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
            "nightly-source/2026-10-31-9d979ca",
        )

    def test_mixins_pin_and_validation_status_are_explicit(self):
        self.assertEqual(self.compatibility["horizon_mixins_revision"], MIXINS_REVISION)
        self.assertEqual(self.compatibility["status"], "release-validation-in-progress")
        self.assertEqual(self.compatibility["horizon_hooks_api"], 40)
        self.assertEqual(self.compatibility["mixin_schema"], 6)
        self.assertEqual(
            self.compatibility["hook_policy"],
            "server-hook-entrypoints-with-exact-nightly-pin",
        )
        self.assertEqual(
            self.compatibility["validation"]["native_build"],
            "passed-approved-isolated-offline-fast",
        )

    def test_package_and_bundle_versions_agree(self):
        self.assertEqual(
            self.cargo["package"]["version"], self.manifest["mod"]["version"]
        )
        version = re.search(r'pub const MOD_VERSION: &str = "([^"]+)";', self.runtime)
        self.assertIsNotNone(version)
        self.assertEqual(version.group(1), self.manifest["mod"]["version"])

    def test_runtime_identity_matches_the_bundle(self):
        self.assertEqual(self.manifest["mod"]["id"], "right_click_crops")
        self.assertIn('pub const MOD_ID: &str = "right_click_crops";', self.runtime)
        self.assertRegex(self.manifest["mod"]["id"], r"^[a-z0-9_]+$")

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

    def test_only_seven_bounded_head_hooks_are_declared(self):
        hooks = self.manifest["injection"]
        self.assertEqual(len(hooks), 7)
        for hook in hooks:
            self.assertEqual(hook["kind"], "HEAD")
            self.assertFalse(hook.get("cancellable", False))

    def test_hook_targets_match_the_researched_declaring_modules(self):
        targets = {hook["id"]: hook["target"] for hook in self.manifest["injection"]}
        self.assertEqual(
            targets,
            {
                "register-mod": "horizon_client::game::native_hooks::Game<'_>::native_mods",
                "report-mod-start": "horizon_client::game::native_hooks::Game<'_>::native_tick",
                "list-plant-settings": "horizon_client::game::native_hooks::Game<'_>::native_settings",
                "toggle-plant-setting": "horizon_client::game::native_hooks::Game<'_>::native_settings_click",
                "harvest-held-item": "horizon_client::game::native_hooks::Game<'_>::native_use_item_on",
                "stop-offhand-followup": "horizon_client::game::native_hooks::Game<'_>::native_use_item",
                "harvest-empty-hand": "horizon_client::game::native_hooks::Game<'_>::native_right_click_block",
            },
        )

    def test_bindings_do_not_evaluate_game_calls(self):
        for hook in self.manifest["injection"]:
            for binding in hook["bindings"]:
                self.assertIn(binding["value"], {"mods", "&*self", "&mut *self", "mod_id", "buttons", "button", "pos", "claimed", "canceled"})
                if binding["name"] == "game":
                    self.assertIn(binding["ty"], {"&crate::game::Game<'_>", "&mut crate::game::Game<'_>"})
                if binding["name"] in {"claimed", "canceled"}:
                    self.assertEqual(binding["ty"], "&mut bool")

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

    def test_gameplay_enters_through_server_native_hooks(self):
        for hook in self.manifest["injection"]:
            self.assertNotIn("break_block", hook["target"])
        targets = [hook["target"] for hook in self.manifest["injection"]]
        self.assertNotIn("horizon_client::game::Game<'_>::use_hand", targets)
        self.assertFalse(any("remote_block_reacts" in target for target in targets))
        self.assertIn("horizon_client::game::native_hooks::Game<'_>::native_use_item_on", targets)
        self.assertIn("horizon_client::game::native_hooks::Game<'_>::native_right_click_block", targets)
        self.assertIn("full game restart", self.runtime)

    def test_gameplay_uses_one_ordinary_loot_path_per_harvest_adapter(self):
        gameplay = (BUNDLE / "gameplay.rs").read_text()
        self.assertEqual(gameplay.count("game.block_loot_at("), 3)
        self.assertEqual(gameplay.count("b.set_block("), 7)
        self.assertNotRegex(gameplay, r"\.break_block\(|\.native_give\(|\.consume_held\(")
        self.assertNotIn("game.integrated.is_some()", gameplay)
        self.assertNotIn("let local_actor", gameplay)
        self.assertIn("game.lan_acting_uuid.or_else", gameplay)
        self.assertIn("game.remote.is_some()", gameplay)
        self.assertIn("game.hand != Hand::Main", gameplay)
        self.assertIn("game.hand != Hand::Off", gameplay)
        self.assertIn("game.ticks.checked_sub(click.tick).is_some_and(|elapsed| elapsed <= 2)", gameplay)
        self.assertIn("if pos.is_none() || !matches { clicks.remove(&actor); }", gameplay)
        self.assertIn("claim_offhand_followup(game, Some(pos))", (BUNDLE / "use_item_on.rs").read_text())
        self.assertIn("claim_offhand_followup(game, None)", (BUNDLE / "use_item.rs").read_text())
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

    def test_settings_are_flat_persistent_and_limited_to_mod_targets(self):
        listed = (BUNDLE / "settings_list.rs").read_text()
        clicked = (BUNDLE / "settings_click.rs").read_text()
        gameplay = (BUNDLE / "gameplay.rs").read_text()
        self.assertIn('pub const CONFIG_FILE: &str = "plants.conf";', self.runtime)
        self.assertIn("buttons.extend(runtime::Plant::ALL.map", listed)
        self.assertIn("runtime::Plant::ALL.get(button)", clicked)
        self.assertIn("game.native_set_setting(runtime::MOD_ID, runtime::CONFIG_FILE", clicked)
        self.assertIn("core::Plant::from_block(&clicked_name)?", gameplay)
        self.assertIn("if !core::plant_enabled(plant) { return None; }", gameplay)
        self.assertNotRegex(listed + clicked, r"berry|category|group")

    def test_bundle_source_and_metadata_use_english_text(self):
        paths = list(BUNDLE.glob("*.rs")) + [ROOT / "compatibility.json"]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(), r"[\u0400-\u04ff]")


if __name__ == "__main__":
    unittest.main()
