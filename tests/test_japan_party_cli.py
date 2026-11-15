"""Japanese party write CLI cannot be enabled implicitly or under --read-only."""
import unittest
from practice.toolkit import parse_args


class JapanPartyCliTests(unittest.TestCase):
    def test_default_is_no_japan_writes(self):
        args = parse_args(["--game-version", "japan"])
        self.assertFalse(args.enable_japan_party_writes)
        self.assertFalse(args.enable_japan_position_writes)
        self.assertFalse(args.enable_japan_debug_menu_writes)

    def test_explicit_opt_in(self):
        args = parse_args(["--game-version", "japan",
                           "--enable-japan-party-writes"])
        self.assertTrue(args.enable_japan_party_writes)
        self.assertFalse(args.read_only)

    def test_debug_menu_and_position_are_independent_opt_ins(self):
        args = parse_args([
            "--game-version", "japan", "--enable-japan-debug-menu-writes"])
        self.assertTrue(args.enable_japan_debug_menu_writes)
        self.assertFalse(args.enable_japan_position_writes)
        self.assertFalse(args.enable_japan_party_writes)
        blocked = parse_args([
            "--game-version", "japan", "--enable-japan-debug-menu-writes",
            "--enable-japan-position-writes", "--read-only"])
        self.assertFalse(blocked.enable_japan_debug_menu_writes)
        self.assertFalse(blocked.enable_japan_position_writes)

    def test_read_only_overrides_opt_in(self):
        args = parse_args(["--game-version", "japan",
                           "--enable-japan-party-writes", "--read-only"])
        self.assertFalse(args.enable_japan_party_writes)
        self.assertTrue(args.read_only)


if __name__ == "__main__":
    unittest.main()
