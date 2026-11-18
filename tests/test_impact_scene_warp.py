"""Synthetic original-ROM Impact/no-player scene-warp regression cases.

The tests do not prove that a live Impact boss-fight will tear down safely.
"""
import unittest

from autosplitter.memory import (
    PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR, CHARACTER_ID_ADDR,
    LOADING_FLAG_ADDR,
)
from practice.checkpoints import MAP_ADDR, STATE_ADDR, SUBMODE_ADDR
from practice.scene_controls import PENDING_MAP_ADDR, EXIT_REQUEST_ADDR
from practice.entrances import Spawn
from practice.experimental_controls import stage_reload_trial
from practice.japan_direct_scene_reload import (
    stage_japan_direct_reload, JAPAN_PENDING_MAP,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_SCENE,
    get_japan_debug_context,
)
from practice.scene_placement import SpawnPlacement
from tests.test_checkpoint import TestCheckpoint
from tests.test_japanese_debug_warp import debugger


class ImpactSceneReloadTests(unittest.TestCase):
    def usa(self):
        _process, ram = TestCheckpoint().sample()
        ram.write_guest(PENDING_MAP_ADDR, bytes.fromhex('0023'))
        ram.write_guest(SUBMODE_ADDR, bytes([4]))
        ram.write_guest(PLAYER_OBJECT_PTR_ADDR, bytes(4))
        ram.write_guest(PLAYER_TASK_PTR_ADDR, bytes(4))
        return ram

    def test_usa_impact_no_pointer_stages_entrance_then_loader(self):
        ram = self.usa()
        spawn = Spawn(353, (95, 0, -350), 0x300, 0x10)
        original_scene = ram.u16(MAP_ADDR)
        exit_byte = ram.read_guest(EXIT_REQUEST_ADDR, 1)
        result = stage_reload_trial(
            ram, 353, {353: 'Destination'}, spawn=spawn)
        self.assertTrue(result['source_player_unavailable'])
        self.assertIsNone(result['player_ptr'])
        self.assertIsNone(result['task_ptr'])
        self.assertEqual(result['source_position'], [None, None, None])
        self.assertEqual(ram.read_guest(PENDING_MAP_ADDR, 12),
                         spawn.pending_bytes())
        self.assertEqual(ram.read_guest(STATE_ADDR, 1), b'\x0c')
        self.assertEqual(ram.u16(MAP_ADDR), original_scene)
        self.assertEqual(ram.read_guest(EXIT_REQUEST_ADDR, 1), exit_byte)

    def test_usa_impact_reacquires_destination_player_for_placement(self):
        ram = self.usa()
        spawn = Spawn(353, (95, 0, -350), 0x300, 0x10)
        result = stage_reload_trial(
            ram, 353, {353: 'Destination'}, spawn=spawn)
        placement = SpawnPlacement(
            ram, spawn, result['requested_character'],
            result['source_map'], result['player_ptr'], result['task_ptr'],
            0, seen_transition=True)
        ram.write_guest(MAP_ADDR, (353).to_bytes(2, 'big'))
        ram.write_guest(STATE_ADDR, bytes([13]))
        ram.write_guest(SUBMODE_ADDR, bytes([1]))
        ram.write_guest(PLAYER_OBJECT_PTR_ADDR,
                        (0x801A0000).to_bytes(4, 'big'))
        ram.write_guest(PLAYER_TASK_PTR_ADDR,
                        (0x801B0000).to_bytes(4, 'big'))
        self.assertEqual(placement.poll(ram, 0.2)['status'], 'waiting')
        self.assertEqual(placement.poll(ram, 0.4)['status'], 'placed')
        self.assertEqual(
            tuple(ram.snapshot()[key] for key in ('x', 'y', 'z')),
            (95, 0, -350))

    def test_usa_unknown_character_requires_explicit_target(self):
        ram = self.usa()
        ram.write_guest(CHARACTER_ID_ADDR, bytes.fromhex('ffffffff'))
        with self.assertRaisesRegex(RuntimeError, 'choose Goemon'):
            stage_reload_trial(ram, 353, {353: 'Destination'})
        self.assertEqual(ram.u8(STATE_ADDR), 13)
        self.assertEqual(ram.u16(PENDING_MAP_ADDR), 35)
        result = stage_reload_trial(
            ram, 353, {353: 'Destination'}, spawn_character=0)
        self.assertTrue(result['character_staged'])
        self.assertEqual(result['requested_character'], 0)
        self.assertEqual(ram.u32(CHARACTER_ID_ADDR), 0)

    def test_usa_pointerless_never_bypasses_active_loader_exit_or_debug(self):
        for address, data in (
            (STATE_ADDR, bytes([10])),
            (STATE_ADDR, bytes([6])),
            (LOADING_FLAG_ADDR, bytes([1])),
            (EXIT_REQUEST_ADDR, bytes([1])),
        ):
            with self.subTest(address=address, data=data):
                ram = self.usa()
                ram.write_guest(address, data)
                with self.assertRaises((ValueError, RuntimeError)):
                    stage_reload_trial(ram, 353, {353: 'Destination'})
                self.assertEqual(ram.u16(PENDING_MAP_ADDR), 35)

    def test_japan_impact_no_pointer_required_and_native_entrance_used(self):
        for endian in ('wordswapped', 'big'):
            with self.subTest(endian=endian):
                game = debugger(
                    endian, state=13, scene=0x161, character=1, submode=4)
                rdram = game.rdram()
                spawn = Spawn(0x1D1, (95, 0, -350), 0x300, 0x10)
                original_scene = rdram.read_guest(JAPAN_DEBUG_SCENE, 2)
                outcome = stage_japan_direct_reload(
                    rdram, 0x1D1,
                    expected_context=get_japan_debug_context(rdram),
                    spawn=spawn)
                self.assertEqual(outcome.source_scene, 0x161)
                self.assertEqual(rdram.read_guest(JAPAN_PENDING_MAP, 12),
                                 spawn.pending_bytes())
                self.assertEqual(rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1),
                                 bytes([12]))
                self.assertEqual(rdram.read_guest(JAPAN_DEBUG_SCENE, 2),
                                 original_scene)

    def test_japan_unknown_character_requires_explicit_target(self):
        game = debugger(state=13, scene=0x161,
                        character=255, submode=4)
        rdram = game.rdram()
        context = get_japan_debug_context(rdram)
        with self.assertRaisesRegex(RuntimeError, 'choose Goemon'):
            stage_japan_direct_reload(
                rdram, 0x1D1, expected_context=context)
        self.assertEqual(game.writes, [])
        outcome = stage_japan_direct_reload(
            rdram, 0x1D1, expected_context=context,
            target_character=0)
        self.assertTrue(outcome.character_staged)
        self.assertEqual(rdram.read_guest(JAPAN_DEBUG_CHARACTER, 4),
                         bytes(4))


if __name__ == '__main__':
    unittest.main()
