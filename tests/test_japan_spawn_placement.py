"""No-ROM guarded post-load Japanese XYZ write using identical USA entrance."""
import struct
import unittest

from practice.entrances import Spawn
from practice.japan_spawn_placement import place_japan_spawn_once
from practice.japanese_position import JAPAN_PLAYER_XYZ_START
from tests.test_japanese_debug_warp import debugger


class JapanSpawnPlacementTests(unittest.TestCase):
    def test_exact_selected_usa_xyz_applied_once_both_ram_endians(self):
        spawn = Spawn(0x1D1, (120, 4, -210), heading=500, mode=0x10)
        for endian in ('big', 'wordswapped'):
            with self.subTest(endian=endian):
                proc = debugger(endian=endian, scene=0x1D1)
                proc.set_guest(
                    JAPAN_PLAYER_XYZ_START,
                    struct.pack('>fff', 5.0, 0.0, 10.0))
                proc.writes.clear()
                ram = proc.rdram()
                original = ram.read_guest(JAPAN_PLAYER_XYZ_START, 12)
                actual = place_japan_spawn_once(
                    ram, spawn, expected_before=original)
                self.assertEqual(actual, (120.0, 4.0, -210.0))
                self.assertEqual(
                    ram.read_guest(JAPAN_PLAYER_XYZ_START, 12),
                    struct.pack('>fff', 120.0, 4.0, -210.0))
                self.assertEqual(len(proc.writes), 1)
                self.assertEqual(
                    place_japan_spawn_once(
                        ram, spawn,
                        expected_before=ram.read_guest(JAPAN_PLAYER_XYZ_START, 12)),
                    (120.0, 4.0, -210.0))
                self.assertEqual(len(proc.writes), 1)

    def test_invalid_character_map_loading_and_stale_vector_do_not_write(self):
        spawn = Spawn(0x1D1, (120, 4, -210))
        for opts in (
            dict(scene=0x161), dict(character=3),
            dict(state=12), dict(loading=1)):
            with self.subTest(opts=opts):
                proc = debugger(**opts)
                proc.set_guest(
                    JAPAN_PLAYER_XYZ_START,
                    struct.pack('>fff', 0, 0, 0))
                proc.writes.clear()
                with self.assertRaises(RuntimeError):
                    place_japan_spawn_once(
                        proc.rdram(), spawn,
                        expected_before=struct.pack('>fff', 0, 0, 0))
                self.assertEqual(proc.writes, [])
        proc = debugger(scene=0x1D1)
        proc.set_guest(
            JAPAN_PLAYER_XYZ_START,
            struct.pack('>fff', 5, 0, 10))
        proc.writes.clear()
        with self.assertRaisesRegex(RuntimeError, 'moved'):
            place_japan_spawn_once(
                proc.rdram(), spawn,
                expected_before=struct.pack('>fff', 0, 0, 0))
        self.assertEqual(proc.writes, [])

    def test_write_is_exact_guest_float32_and_not_a_direct_map_edit(self):
        proc = debugger(scene=0x1D1)
        proc.set_guest(JAPAN_PLAYER_XYZ_START, struct.pack('>fff', 0, 0, 0))
        proc.writes.clear()
        spawn = Spawn(0x1D1, (9.25, -3.5, 17.75))
        ram = proc.rdram()
        place_japan_spawn_once(
            ram, spawn,
            expected_before=ram.read_guest(JAPAN_PLAYER_XYZ_START, 12))
        self.assertEqual(
            ram.read_guest(JAPAN_PLAYER_XYZ_START, 12),
            struct.pack('>fff', 9.25, -3.5, 17.75))
        self.assertEqual(len(proc.writes), 1)


if __name__ == '__main__':
    unittest.main()
