"""No-ROM Japanese warp-point capture/persistence and mismatch regressions."""
from pathlib import Path
import struct
import tempfile
import unittest

from practice.entrances import Spawn
from practice.japan_direct_scene_reload import JAPAN_PENDING_MAP
from practice.japanese_position import JAPAN_PLAYER_XYZ_START
from practice.japan_warp_spawns import (
    capture_current_japan_spawn, destination_spawn, load_japan_spawns,
    position_difference, save_japan_spawn,
)
from tests.test_japanese_debug_warp import debugger


class JapanWarpSpawnsTests(unittest.TestCase):
    def test_unknown_destination_is_never_filled_from_usa_atlas(self):
        self.assertIsNone(destination_spawn({}, 0x1D1))
        oedo = destination_spawn({}, 0x161)
        self.assertEqual(oedo.position, (-289.0, 0.0, -167.0))
        self.assertIn('unverified', oedo.label)

    def test_json_store_roundtrips_user_observed_japanese_xyz(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'my-japan-spawns.json'
            self.assertEqual(load_japan_spawns(store=path), {})
            one = Spawn(0x1D1, (10, 20, -30), heading=512, mode=0x10,
                        entrance_id='jp:capture:1D1')
            save_japan_spawn(one, basis='native-pending', store=path)
            observed = load_japan_spawns(store=path)
            self.assertEqual(observed[0x1D1].pending_bytes(),
                             one.pending_bytes())
            two = Spawn(0x161, (-289, 0, -167), heading=0, mode=0x10,
                        entrance_id='jp:capture:161')
            save_japan_spawn(two, basis='xyz-only', store=path)
            observed = load_japan_spawns(store=path)
            self.assertEqual(set(observed), {0x161, 0x1D1})
            self.assertEqual(destination_spawn(observed, 0x161).position,
                             (-289, 0, -167))
            self.assertIn('native-pending', observed[0x1D1].label)

    def test_invalid_or_corrupt_registry_is_not_trusted(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'japan-spawns.json'
            for bad in (b'not-json', b'x' * 160001, b'{}',
                        b'{"format":"goemon-japan-warp-spawns-v1",'
                        b'"spawns":{"123":{"scene":456}}}'):
                path.write_bytes(bad)
                self.assertEqual(load_japan_spawns(store=path), {})

    def test_capture_japanese_native_pending_when_position_agrees(self):
        p = debugger(scene=0x161)
        ram = p.rdram()
        p.set_guest(JAPAN_PLAYER_XYZ_START,
                    struct.pack('>fff', -289.0, 0.0, -167.0))
        exact = Spawn(0x161, (-289, 0, -167), heading=1200, mode=0x20)
        p.set_guest(JAPAN_PENDING_MAP, exact.pending_bytes())
        p.writes.clear()
        recorded, basis = capture_current_japan_spawn(ram)
        self.assertEqual(basis, 'native-pending')
        self.assertEqual(recorded.pending_bytes(), exact.pending_bytes())
        self.assertEqual(p.writes, [])

    def test_capture_outdated_pending_uses_clearly_unverified_header(self):
        p = debugger(scene=0x161)
        ram = p.rdram()
        p.set_guest(JAPAN_PLAYER_XYZ_START,
                    struct.pack('>fff', -289.5, 0.0, -167.0))
        p.set_guest(JAPAN_PENDING_MAP,
                    Spawn(0x1D1, (500, 0, 300)).pending_bytes())
        observed, basis = capture_current_japan_spawn(ram)
        self.assertEqual(basis, 'xyz-only')
        self.assertEqual(observed.position, (-289.5, 0.0, -167.0))
        self.assertIn('unverified', observed.label)
        self.assertEqual(observed.pending_bytes()[4:10],
                         struct.pack('>hhh', -290, 0, -167))

    def test_capture_refuses_unverified_character_and_loading(self):
        for opts in (dict(character=1), dict(loading=1), dict(state=12)):
            p = debugger(**opts)
            p.set_guest(JAPAN_PLAYER_XYZ_START,
                        struct.pack('>fff', -289, 0, -167))
            with self.subTest(opts=opts), self.assertRaises(
                    (RuntimeError, ValueError)):
                capture_current_japan_spawn(p.rdram())

    def test_actual_postload_coordinates_can_disagree_with_requested(self):
        self.assertAlmostEqual(
            position_difference((100, 0, 200), (5, 0, -10)),
            (95 ** 2 + 210 ** 2) ** .5)
        self.assertEqual(position_difference((1, 2, 3), (1, 2, 3)), 0)


if __name__ == "__main__":
    unittest.main()
