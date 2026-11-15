"""Synthetic Japan-0 original-menu category/stage and load verification."""
import struct
import unittest
from practice.japan_native_scene_warp import (
    JAPAN_MENU_CATEGORY, JAPAN_MENU_STAGE_INDEX,
    japan_warp_selection, read_japan_menu_selection,
    stage_japan_native_destination, is_japan_scene_loaded,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_LOADING,
)
from practice.japanese_position import JAPAN_PLAYER_XYZ_START
from tests.test_japanese_debug_warp import debugger


class JapanNativeSceneWarpTests(unittest.TestCase):
    def test_exact_japan_menu_offsets_and_usa_derived_scene_values(self):
        self.assertEqual(JAPAN_MENU_CATEGORY, 0x800CD294)
        self.assertEqual(JAPAN_MENU_STAGE_INDEX, 0x800CD2A4)
        oedo = japan_warp_selection(0x161)
        self.assertEqual((oedo.category_name, oedo.category_index, oedo.stage_index),
                         ('MACHI', 3, 3))
        house = japan_warp_selection(0x1D1)
        self.assertEqual((house.category_name, house.category_index, house.stage_index),
                         ('SHOP', 4, 65))

    def test_stage_only_category_and_stage_during_native_menu(self):
        for endian in ('wordswapped', 'big'):
            with self.subTest(endian=endian):
                p = debugger(endian, state=10, scene=0x161)
                p.writes.clear()
                ram = p.rdram()
                selection = stage_japan_native_destination(ram, 0x1D1)
                self.assertEqual(selection.category_index, 4)
                self.assertEqual(selection.stage_index, 65)
                self.assertEqual(read_japan_menu_selection(ram), (4, 65))
                self.assertEqual(ram.read_guest(JAPAN_DEBUG_SCENE, 2),
                                 bytes.fromhex('0161'))
                self.assertEqual(ram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0a')
                self.assertEqual(len(p.writes), 2)
                self.assertEqual(
                    sorted({addr for addr, _data in p.writes}),
                    sorted({JAPAN_MENU_CATEGORY, JAPAN_MENU_STAGE_INDEX}
                           if endian == 'big' else
                           {JAPAN_MENU_CATEGORY & ~3, JAPAN_MENU_STAGE_INDEX & ~3}))
                self.assertTrue(all(len(data) <= 4 for _, data in p.writes))

    def test_staging_rejected_if_debug_menu_is_closed(self):
        p = debugger(state=13)
        with self.assertRaisesRegex(RuntimeError, 'Debug menu'):
            stage_japan_native_destination(p.rdram(), 0x161)
        self.assertEqual(p.writes, [])

    def test_staged_values_can_be_read_again_before_input(self):
        p = debugger(state=10)
        ram = p.rdram()
        stage_japan_native_destination(ram, 0x1D1)
        self.assertEqual(read_japan_menu_selection(ram), (4, 65))
        p.set_guest(JAPAN_MENU_STAGE_INDEX, bytes.fromhex('0000'))
        self.assertNotEqual(read_japan_menu_selection(ram), (4, 65))

    def test_scene_id_alone_never_claims_loaded_gameplay(self):
        p = debugger(state=10, scene=0x1D1)
        p.set_guest(JAPAN_PLAYER_XYZ_START, struct.pack('>fff', 12, 0, 10))
        self.assertFalse(is_japan_scene_loaded(p.rdram(), 0x1D1))
        p.set_guest(JAPAN_DEBUG_ENGINE_MODE, b'\x0d')
        self.assertTrue(is_japan_scene_loaded(p.rdram(), 0x1D1))
        p.set_guest(JAPAN_DEBUG_LOADING, (1).to_bytes(4, 'big'))
        self.assertFalse(is_japan_scene_loaded(p.rdram(), 0x1D1))
        p.set_guest(JAPAN_DEBUG_LOADING, bytes(4))
        p.set_guest(JAPAN_DEBUG_SCENE, bytes.fromhex('0161'))
        self.assertFalse(is_japan_scene_loaded(p.rdram(), 0x1D1))


if __name__ == '__main__':
    unittest.main()
