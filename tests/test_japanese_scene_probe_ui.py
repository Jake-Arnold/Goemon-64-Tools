"""Tk regression: Japanese scene baseline comparison never enables game writes."""
import unittest

from tests.test_japanese_fields_ui import Host, JapanTkSmokeTest
from tests.test_japanese_fields import FakeRam


class JapaneseSceneUiTest(JapanTkSmokeTest):
    def test_capture_compare_and_disconnect(self):
        host = self.host
        ram = FakeRam({
            (0x80161DDA, 2): bytes.fromhex("0010"),
            (0x800CD2A2, 2): bytes.fromhex("012C"),
        })
        ram.base = 0x7AA843EC0000
        ram.endian = "wordswapped"
        host.jp_rdram = ram
        host.game_pid = 959604
        host.capture_japan_baseline()
        self.assertEqual(host._jp_baseline["scene_map"].raw, "012C")
        ram.values[(0x800CD2A2, 2)] = bytes.fromhex("012D")
        ram.values[(0x80161DDA, 2)] = bytes.fromhex("000F")
        host.compare_japan_baseline()
        keys = {x[0] for x in host._jp_last_changes}
        self.assertEqual(keys, {"scene_map", "ryo"})
        self.assertIn("CHANGED:", host.jp_fields_tree.set("jp_field_scene_map", "status"))
        self.assertEqual(host.jp_fields_tree.set("jp_field_scene_map", "value"),
                         "301 / 0x12D")
        self.assertFalse(hasattr(ram, "write_guest"))
        host.clear_japan_field_values()
        self.assertIsNone(host._jp_baseline)
        self.assertEqual(host.jp_fields_tree.set("jp_field_scene_map", "value"), "—")

    def test_change_of_pid_or_ram_base_invalidates_baseline(self):
        host = self.host
        ram = FakeRam()
        ram.base, ram.endian = 0x10000000, "big"
        host.jp_rdram = ram
        host.game_pid = 111
        host.capture_japan_baseline()
        host.game_pid = 222
        host.compare_japan_baseline()
        self.assertIsNone(host._jp_baseline)
        self.assertIn("changed", host.jp_fields_caption.get())


if __name__ == "__main__":
    unittest.main()
