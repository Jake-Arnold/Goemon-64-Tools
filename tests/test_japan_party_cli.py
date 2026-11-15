"""Japanese experimental operations are enabled unless --read-only."""
import unittest

from practice.toolkit import parse_args


class JapanPartyCliTests(unittest.TestCase):
    def test_default_enables_japanese_experimental_writes(self):
        args = parse_args(["--game-version", "japan"])
        self.assertTrue(args.enable_japan_party_writes)
        self.assertTrue(args.enable_japan_position_writes)
        self.assertTrue(args.enable_japan_debug_menu_writes)
        self.assertTrue(args.enable_japan_scene_writes)
        self.assertTrue(args.enable_hex_edit)
        self.assertFalse(args.read_only)

    def test_legacy_japan_party_optin_does_not_change_defaults(self):
        normal = parse_args(["--game-version", "japan"])
        legacy = parse_args(["--game-version", "japan",
                             "--enable-japan-party-writes"])
        self.assertEqual(normal.enable_japan_party_writes,
                         legacy.enable_japan_party_writes)

    def test_default_debug_position_and_scene_independent_of_party_switch(self):
        args = parse_args(["--game-version", "japan",
                           "--enable-japan-debug-menu-writes"])
        self.assertTrue(args.enable_japan_debug_menu_writes)
        self.assertTrue(args.enable_japan_position_writes)
        self.assertTrue(args.enable_japan_scene_writes)
        self.assertTrue(args.enable_japan_party_writes)

    def test_read_only_overrides_all_japanese_write_defaults(self):
        args = parse_args(["--game-version", "japan", "--read-only",
                           "--enable-japan-party-writes",
                           "--enable-japan-scene-writes",
                           "--enable-japan-debug-menu-writes",
                           "--enable-japan-position-writes"])
        self.assertTrue(args.read_only)
        for key in ("enable_japan_party_writes", "enable_japan_scene_writes",
                    "enable_japan_debug_menu_writes", "enable_japan_position_writes",
                    "enable_hex_edit", "enable_teleport"):
            self.assertFalse(getattr(args, key), key)


if __name__ == "__main__":
    unittest.main()
