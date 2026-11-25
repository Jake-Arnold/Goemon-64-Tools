import unittest
from unittest.mock import patch
from tests.test_checkpoint import TestCheckpoint
from practice.scene_controls import (request_scene_warp, assess_scene_warp,
                                     open_native_debug_menu, PENDING_MAP_ADDR, EXIT_REQUEST_ADDR)
from practice.checkpoints import MAP_ADDR, SUBMODE_ADDR


class TestWarp(unittest.TestCase):
    def make(self):
        p, ram = TestCheckpoint().sample()
        ram.write_guest(MAP_ADDR, (353).to_bytes(2, 'big'))
        ram.write_guest(PENDING_MAP_ADDR, (353).to_bytes(2, 'big'))
        ram.write_guest(EXIT_REQUEST_ADDR, b'\x00')
        return ram

    def test_direct_scene_request_is_disabled(self):
        ram=self.make()
        before=(ram.u16(PENDING_MAP_ADDR),ram.u8(EXIT_REQUEST_ADDR),ram.u16(MAP_ADDR))
        with patch.object(ram, 'write_guest', wraps=ram.write_guest) as write_guest:
            for destination in (465,353,9999,-1):
                with self.assertRaisesRegex(RuntimeError,'Direct warp disabled'):
                    request_scene_warp(ram,destination,{353:'Oedo',465:'House'})
            write_guest.assert_not_called()
        self.assertEqual(before,(ram.u16(PENDING_MAP_ADDR),ram.u8(EXIT_REQUEST_ADDR),ram.u16(MAP_ADDR)))

    def test_normal_indoor_submode_3_can_enter_debug(self):
        ram=self.make()
        ram.write_guest(SUBMODE_ADDR,b'\x03')
        self.assertEqual(open_native_debug_menu(ram),10)
        self.assertEqual(ram.u8(0x800C7A94),10)
        self.assertEqual(ram.u16(MAP_ADDR),353)

    def test_impact_submode_missing_player_and_non_gameplay_state_enter_debug(self):
        from practice.backends.memory import PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR
        from practice.checkpoints import STATE_ADDR
        proc, ram = TestCheckpoint().sample()
        ram.write_guest(SUBMODE_ADDR, b'\x04')  # Impact battle
        ram.write_guest(PLAYER_OBJECT_PTR_ADDR, bytes(4))
        ram.write_guest(PLAYER_TASK_PTR_ADDR, bytes(4))
        ram.write_guest(STATE_ADDR, b'\x06')
        source_scene = ram.u16(MAP_ADDR)
        with patch.object(proc, 'write', wraps=proc.write) as write:
            self.assertEqual(open_native_debug_menu(ram), 10)
            self.assertEqual(write.call_count, 1)
            self.assertEqual(write.call_args.args[1], b'\x0a')
            # Already in debug: absolutely no second write.
            self.assertEqual(open_native_debug_menu(ram), 10)
            self.assertEqual(write.call_count, 1)
        self.assertEqual(ram.u16(MAP_ADDR), source_scene)
        self.assertEqual(ram.u8(EXIT_REQUEST_ADDR), 0)

if __name__=='__main__':unittest.main()
