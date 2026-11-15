"""Synthetic Japan-0 USA-style instant 0x0C reload tests; no emulator."""
import unittest
from practice.entrances import Spawn
from practice.japan_direct_scene_reload import (
    JAPAN_PENDING_MAP, JAPAN_DIRECT_RELOAD_MODE, stage_japan_direct_reload,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_EXIT,
    get_japan_debug_context,
)
from tests.test_japanese_debug_warp import debugger


class JapanDirectSceneReloadTests(unittest.TestCase):
    def test_same_sequence_as_usa_pending_then_0x0c_not_debug_menu(self):
        for endian in ('big','wordswapped'):
            with self.subTest(endian=endian):
                p = debugger(endian, state=13, scene=0x161)
                p.set_guest(JAPAN_PENDING_MAP, bytes.fromhex('0161'))
                p.writes.clear()
                ram=p.rdram()
                before=get_japan_debug_context(ram)
                original_exit=ram.read_guest(JAPAN_DEBUG_EXIT,1)
                result=stage_japan_direct_reload(
                    ram,0x1D1,expected_context=before)
                self.assertEqual(result.source_scene,0x161)
                self.assertEqual(result.destination,0x1D1)
                self.assertEqual(result.pending_width,2)
                self.assertEqual(result.state_after_write,12)
                self.assertEqual(ram.read_guest(JAPAN_PENDING_MAP,2),
                                 bytes.fromhex('01D1'))
                self.assertEqual(ram.read_guest(JAPAN_DEBUG_ENGINE_MODE,1),
                                 bytes([JAPAN_DIRECT_RELOAD_MODE]))
                self.assertNotEqual(
                    ram.read_guest(JAPAN_DEBUG_ENGINE_MODE,1),b'\x0a')
                self.assertEqual(ram.read_guest(JAPAN_DEBUG_SCENE,2),
                                 bytes.fromhex('0161'))
                self.assertEqual(ram.read_guest(JAPAN_DEBUG_EXIT,1),original_exit)
                self.assertEqual(len(p.writes),2)
                self.assertEqual(
                    p.writes[0][0],
                    (JAPAN_PENDING_MAP&0x1FFFFFFF)&(~3 if endian=='wordswapped' else ~0))
                self.assertEqual(
                    p.writes[1][0],
                    (JAPAN_DEBUG_ENGINE_MODE&0x1FFFFFFF)&(~3 if endian=='wordswapped' else ~0))

    def test_full_entrance_block_matches_usa_native_layout(self):
        p=debugger(state=13)
        ram=p.rdram()
        spawn=Spawn(
            0x161,(-289,0,-167),heading=0x400,mode=0x10,
            label='Oedo South',entrance_id='test:default')
        result=stage_japan_direct_reload(
            ram,0x161,expected_context=get_japan_debug_context(ram),
            spawn=spawn)
        self.assertEqual(result.pending_width,12)
        self.assertEqual(ram.read_guest(JAPAN_PENDING_MAP,12),
                         spawn.pending_bytes())
        self.assertEqual(
            ram.read_guest(JAPAN_DEBUG_ENGINE_MODE,1),b'\x0c')

    def test_changed_context_or_menu_refuses_without_pending_write(self):
        for state in (10,12):
            p=debugger(state=state)
            with self.assertRaises(RuntimeError):
                stage_japan_direct_reload(
                    p.rdram(),0x1D1,
                    expected_context=get_japan_debug_context(p.rdram()))
            self.assertEqual(p.writes,[])

        p=debugger(state=13)
        expected=get_japan_debug_context(p.rdram())
        p.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('0162'))
        with self.assertRaisesRegex(RuntimeError,'changed'):
            stage_japan_direct_reload(
                p.rdram(),0x1D1,expected_context=expected)
        self.assertEqual(p.writes,[])

    def test_state_write_failure_rolls_back_pending_only_while_safe(self):
        p=debugger(state=13)
        p.set_guest(JAPAN_PENDING_MAP,bytes.fromhex('0161'))
        ram=p.rdram()
        expected=get_japan_debug_context(ram)
        class FailEngine:
            def read_guest(self,addr,n):
                return ram.read_guest(addr,n)
            def write_guest(self,addr,data):
                if addr==JAPAN_DEBUG_ENGINE_MODE:
                    raise OSError('synthetic engine state write failed')
                return ram.write_guest(addr,data)
        with self.assertRaisesRegex(OSError,'synthetic engine'):
            stage_japan_direct_reload(
                FailEngine(),0x1D1,expected_context=expected)
        self.assertEqual(ram.read_guest(JAPAN_PENDING_MAP,2),
                         bytes.fromhex('0161'))
        self.assertEqual(ram.read_guest(JAPAN_DEBUG_ENGINE_MODE,1),b'\x0d')

    def test_readonly_handle_cannot_stage_scene(self):
        p=debugger(state=13)
        context=get_japan_debug_context(p.rdram())
        p.writable=False
        with self.assertRaises(PermissionError):
            stage_japan_direct_reload(
                p.rdram(),0x1D1,expected_context=context)
        self.assertEqual(p.writes,[])

    def test_unknown_scene_and_entrance_mismatch_are_no_writes(self):
        p=debugger(state=13)
        context=get_japan_debug_context(p.rdram())
        for dest in (True,-1,0xFFFF,'0x161'):
            with self.assertRaises(ValueError):
                stage_japan_direct_reload(
                    p.rdram(),dest,expected_context=context)
        with self.assertRaises(ValueError):
            stage_japan_direct_reload(
                p.rdram(),0x1D1,expected_context=context,
                spawn=Spawn(0x161,(-289,0,-167)))
        self.assertEqual(p.writes,[])


if __name__ == '__main__':
    unittest.main()
