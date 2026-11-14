"""Source-only Japanese scene hypotheses, no emulator memory writes."""
import unittest

from practice.japanese_fields import JAPAN_FIELDS, JapanFieldReading
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES, compare_guest_readings, read_japan_scene_probes,
)


class Ram:
    def __init__(self, values=None, bad=None):
        self.values = values or {}
        self.bad = bad
        self.reads = []

    def read_guest(self, address, width):
        self.reads.append((address, width))
        if self.bad == address:
            raise OSError("denied")
        return self.values.get((address, width), bytes(width))


class JapaneseSceneProbeTests(unittest.TestCase):
    def test_ten_individually_documented_offset_hypotheses(self):
        self.assertEqual(len(JAPAN_SCENE_PROBES), 10)
        self.assertTrue(all(x.address - x.usa_reference == 0x57F0
                            for x in JAPAN_SCENE_PROBES))
        self.assertEqual({x.key for x in JAPAN_SCENE_PROBES}.__len__(), 10)
        self.assertFalse({x.address for x in JAPAN_SCENE_PROBES} &
                         {x.address for x in JAPAN_FIELDS})

    def test_scene_and_character_candidates(self):
        v = {
            (0x800CD2A2, 2): bytes.fromhex("012C"),  # candidate scene 300
            (0x80161DCC, 4): bytes.fromhex("00000003"),
        }
        ram = Ram(v)
        out = read_japan_scene_probes(ram)
        self.assertEqual(out["scene_map"].raw, "012C")
        self.assertEqual(out["scene_map"].value, "300 / 0x12C")
        self.assertEqual(out["scene_character"].value, "Yae (3)")
        self.assertTrue(out["scene_map"].status.startswith("UNVERIFIED"))
        self.assertEqual(len(ram.reads), 10)
        self.assertFalse(hasattr(ram, "write_guest"))

    def test_unusual_scene_or_character_values_not_hidden(self):
        ram = Ram({
            (0x800CD2A2, 2): bytes.fromhex("F000"),
            (0x80161DCC, 4): bytes.fromhex("DEADBEEF"),
        })
        out = read_japan_scene_probes(ram)
        self.assertTrue(out["scene_map"].status.startswith("CHECK"))
        self.assertTrue(out["scene_character"].status.startswith("CHECK"))
        self.assertEqual(out["scene_character"].raw, "DEADBEEF")

    def test_probe_read_errors_are_isolated(self):
        ram = Ram(bad=0x800CD2A2)
        out = read_japan_scene_probes(ram)
        self.assertEqual(out["scene_map"].value, "—")
        self.assertIn("READ ERROR", out["scene_map"].status)
        self.assertFalse(out["scene_phase"].status.startswith("READ ERROR"))

    def test_compare_uses_raw_bytes_and_skips_read_errors(self):
        b = {
            "map": JapanFieldReading("Old", "0002", "UNVERIFIED"),
            "ryo": JapanFieldReading("12", "000C", "External lead"),
            "bad": JapanFieldReading("—", "—", "READ ERROR"),
        }
        a = {
            "map": JapanFieldReading("Scene 300", "012C", "UNVERIFIED"),
            "ryo": JapanFieldReading("12 displayed differently", "000C", "External lead"),
            "bad": JapanFieldReading("3", "03", "UNVERIFIED"),
        }
        self.assertEqual(compare_guest_readings(b, a, ("map", "ryo", "bad")),
                         (("map", "0002", "012C"),))


if __name__ == "__main__":
    unittest.main()
