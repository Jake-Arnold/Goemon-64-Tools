"""No-ROM Japanese scene-loading versus playable-actor evidence tests."""
import unittest
import struct

from practice.japan_native_scene_warp import (
    japan_scene_readiness, is_japan_scene_loaded,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_LOADING,
    JAPAN_DEBUG_SCENE, JAPAN_DEBUG_EXIT,
)
from practice.japanese_position import JAPAN_PLAYER_XYZ_START
from tests.test_japanese_debug_warp import debugger


class JapanSceneReadinessTests(unittest.TestCase):
    def test_all_four_playable_character_ids_are_distinguished(self):
        for character in range(4):
            with self.subTest(character=character):
                proc = debugger(scene=0x161, character=character)
                # This vector is Goemon-specific; it must never be consulted
                # when the active character is Ebisumaru/Sasuke/Yae.
                if character == 0:
                    proc.set_guest(
                        JAPAN_PLAYER_XYZ_START, struct.pack('>fff', 4, 0, -6))
                else:
                    proc.set_guest(JAPAN_PLAYER_XYZ_START, b'\xff' * 12)
                reading = japan_scene_readiness(proc.rdram(), 0x161)
                self.assertTrue(reading.scene_loaded)
                self.assertEqual(reading.character, character)
                self.assertEqual(reading.goemon_position_plausible,
                                 character == 0)
                self.assertIn('not verified', reading.note)
                self.assertTrue(is_japan_scene_loaded(proc.rdram(), 0x161))

    def test_scene_id_does_not_prove_loading_finished(self):
        for issue in (
            dict(state=12), dict(state=10), dict(loading=1),
            dict(exit_flag=1), dict(scene=0x162), dict(character=17),
        ):
            with self.subTest(issue=issue):
                proc = debugger(**issue)
                reading = japan_scene_readiness(proc.rdram(), 0x161)
                self.assertFalse(reading.scene_loaded)
                self.assertFalse(is_japan_scene_loaded(proc.rdram(), 0x161))

    def test_uninitialized_goemon_xyz_blocks_ready_without_writes(self):
        proc = debugger(scene=0x161, character=0)
        proc.set_guest(JAPAN_PLAYER_XYZ_START, b'\xff' * 12)
        proc.writes.clear()
        out = japan_scene_readiness(proc.rdram(), 0x161)
        self.assertFalse(out.scene_loaded)
        self.assertIn('not initialized', out.note)
        self.assertEqual(proc.writes, [])

    def test_wrong_destination_never_reads_actor_position(self):
        proc = debugger(scene=0x161)
        proc.set_guest(JAPAN_PLAYER_XYZ_START, b'\xff' * 12)
        proc.writes.clear()
        result = japan_scene_readiness(proc.rdram(), 0x1D1)
        self.assertFalse(result.scene_loaded)
        self.assertIn('current scene', result.note)
        self.assertEqual(proc.writes, [])


if __name__ == '__main__':
    unittest.main()
