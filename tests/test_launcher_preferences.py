"""Unified USA/Japan launcher selection and default write-access tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from practice.launcher_preferences import load_last_region, save_last_region
from practice.toolkit import parse_args


class LauncherPreferencesTests(unittest.TestCase):
    def test_region_defaults_to_usa_without_settings(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "prefs.json"
            self.assertEqual(load_last_region(store=path), "usa")

    def test_last_selected_japanese_region_survives_relaunch(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "prefs.json"
            save_last_region("japan", store=path)
            self.assertEqual(load_last_region(store=path), "japan")
            save_last_region("usa", store=path)
            self.assertEqual(load_last_region(store=path), "usa")

    def test_corrupt_oversize_and_unknown_preferences_fail_closed(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "prefs.json"
            for data in ('junk', '{"format":"unknown","region":"japan"}',
                         '{"format":"goemon-toolkit-launcher-v1","region":"nonsense"}',
                         'x' * 4097):
                path.write_text(data, encoding="utf-8")
                self.assertEqual(load_last_region(store=path), "usa")
            with self.assertRaises(ValueError):
                save_last_region("nonsense", store=path)

    def test_unified_cli_defaults_to_write_enabled_gui_selected_region(self):
        args = parse_args([])
        self.assertIsNone(args.game_version)
        self.assertFalse(args.read_only)
        self.assertTrue(args.enable_japan_scene_writes)
        self.assertTrue(args.enable_japan_position_writes)
        self.assertTrue(args.enable_hex_edit)
        # Explicit old CLI override stays compatible but is no longer required.
        self.assertEqual(parse_args(["--game-version", "japan"]).game_version,
                         "japan")

    def test_legacy_read_only_mode_remains_explicit_opt_in(self):
        args = parse_args(["--read-only"])
        self.assertTrue(args.read_only)
        self.assertFalse(args.enable_hex_edit)
        self.assertFalse(args.enable_japan_scene_writes)


if __name__ == "__main__":
    unittest.main()
