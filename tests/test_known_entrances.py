"""ROM-free checks for permanent scene-keyed entrance coordinate records."""
import unittest

from practice.known_entrances import known_entrances, known_entrance_count
from practice.entrances import Spawn, spawn_from_entry


class KnownEntrancesTests(unittest.TestCase):
    def test_oedo_south_is_available_without_loading_a_rom(self):
        self.assertGreaterEqual(known_entrance_count(), 1)
        records = known_entrances(0x161)
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["destination"], 0x161)
        self.assertEqual(record["position"], [-289.0, 0.0, -167.0])
        self.assertEqual(record["heading"], 256)
        self.assertEqual(record["mode"], 16)
        self.assertEqual(record["provenance"],
                         "observed-japan-oedo-south-goemon-xyz")
        self.assertTrue(record["heading_mode_verified"])
        spawn = spawn_from_entry(record)
        self.assertEqual(spawn.position, (-289.0, 0.0, -167.0))
        self.assertEqual(Spawn(0x161, spawn.position, spawn.heading,
                               spawn.mode).pending_bytes(),
                         spawn.pending_bytes())

    def test_unknown_scenes_not_given_guessed_coordinates(self):
        self.assertEqual(known_entrances(0x1D1), [])
        self.assertEqual(known_entrances(-1), [])
        self.assertEqual(known_entrances(True), [])

    def test_returned_points_are_fresh_not_shared_mutable_constants(self):
        row = known_entrances(0x161)[0]
        row["position"][0] = 9000
        row["heading"] = 123
        new = known_entrances(0x161)[0]
        self.assertEqual(new["position"][0], -289.0)
        self.assertEqual(new["heading"], 256)


if __name__ == "__main__":
    unittest.main()
