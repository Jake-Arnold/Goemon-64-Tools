"""Regression tests for the bundled original-USA numeric entrance atlas.

These load the checked-in JSON, not the ROM or an individual user's cache.
"""
from pathlib import Path
import unittest

from practice.entrance_ui import repository_entrance_atlas_path
from practice.entrances import load_atlas, incoming, spawn_from_entry
from practice.known_entrances import known_entrances


class BundledEntranceAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = repository_entrance_atlas_path()
        cls.atlas = load_atlas(cls.path)

    def test_checked_in_complete_numeric_atlas_loads_without_rom(self):
        self.assertIsNotNone(self.atlas, f"Missing bundled atlas: {self.path}")
        self.assertEqual(self.path.name, "entrance-coordinates.json")
        self.assertEqual(self.atlas["payload"]["format"],
                         "goemon-usa-entrance-atlas-v1")
        self.assertEqual(self.atlas["payload"]["rom_sha1"],
                         "df8083a54296b8c151917c5333e1c85f014a2a66")
        self.assertEqual(len(self.atlas["payload"]["rooms"]), 333)
        self.assertEqual(len(self.atlas["payload"]["entries"]), 888)
        self.assertEqual(len({entry["destination"] for entry in
                              self.atlas["payload"]["entries"]}), 266)

    def test_oedo_source_and_default_spawn_match_verified_xyz_heading_mode(self):
        oedo = incoming(self.atlas, 0x161)
        self.assertEqual(len(oedo), 10)
        self.assertEqual(
            [(entry["position"], entry["heading"], entry["mode"])
             for entry in oedo if entry["id"] in ("default:353", "15F:006")],
            [([-289, 0, -167], 256, 16)] * 2)
        observed_fallback = spawn_from_entry(known_entrances(0x161)[0])
        original_default = spawn_from_entry(
            next(entry for entry in oedo if entry["id"] == "default:353"))
        self.assertEqual(
            observed_fallback.pending_bytes(),
            original_default.pending_bytes())

    def test_multiple_distinct_entrances_to_one_scene_are_not_collapsed(self):
        oedo = incoming(self.atlas, 0x161)
        self.assertIn(("15F:006", (-289, 0, -167)),
                      [(entry["id"], tuple(entry["position"]))
                       for entry in oedo])
        self.assertIn(("160:004", (228, 0, -222)),
                      [(entry["id"], tuple(entry["position"]))
                       for entry in oedo])
        self.assertGreater(len({tuple(entry["position"]) for entry in oedo}), 1)

    def test_atlas_contains_only_numeric_functional_entrance_metadata(self):
        allowed = {"id", "kind", "source_map", "source_file",
                   "definition", "exit_id", "destination", "position",
                   "heading", "mode"}
        for entry in self.atlas["payload"]["entries"]:
            self.assertEqual(set(entry), allowed)
            self.assertEqual(len(entry["position"]), 3)
        self.assertLess(self.path.stat().st_size, 4 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
