"""Prove the debug-menu shortcut cannot accidentally use the unsafe warp path."""
import unittest
from tests.test_scene_warp import TestWarp
from practice.checkpoints import MAP_ADDR, STATE_ADDR
from practice.scene_controls import (
    open_native_debug_for_scene, native_debug_selection,
    PENDING_MAP_ADDR, EXIT_REQUEST_ADDR,
)

SCENES = {
    0: "Oedo Castle 1F Tile Room",
    300: "Kai Highway",
    353: "Oedo Town (South)",
    465: "South Oedo - Goemon's House",
}


class TestNativeDebugShortcut(unittest.TestCase):
    def test_native_codes_do_not_truncate_ids_above_255(self):
        self.assertEqual(native_debug_selection(0, SCENES)['label'], 'SIRO 0')
        self.assertEqual(native_debug_selection(300, SCENES)['label'], 'DOUCHU 0')
        self.assertEqual(native_debug_selection(353, SCENES)['label'], 'MACHI 3')
        self.assertEqual(native_debug_selection(465, SCENES)['label'], 'SHOP 65')

    def test_rejects_unknown_or_boolean_ids(self):
        for value in (466, -1, True, 353.0):
            with self.assertRaises(ValueError):
                native_debug_selection(value, SCENES)

    def test_uses_debug_state_not_pending_map_or_exit_flag(self):
        ram = TestWarp().make()
        pre_pending=ram.read_guest(PENDING_MAP_ADDR,2)
        pre_exit=ram.read_guest(EXIT_REQUEST_ADDR,1)
        result=open_native_debug_for_scene(ram,465,SCENES)
        self.assertEqual(result['status'],'menu_opened_selection_manual')
        self.assertEqual(result['label'],'SHOP 65')
        self.assertEqual(ram.u8(STATE_ADDR),10)
        self.assertEqual(ram.u16(MAP_ADDR),353)
        self.assertEqual(ram.read_guest(PENDING_MAP_ADDR,2),pre_pending)
        self.assertEqual(ram.read_guest(EXIT_REQUEST_ADDR,1),pre_exit)

    def test_bad_target_does_not_open_debug_menu(self):
        ram = TestWarp().make()
        with self.assertRaises(ValueError):
            open_native_debug_for_scene(ram,466,SCENES)
        self.assertEqual(ram.u8(STATE_ADDR),13)


if __name__ == '__main__':
    unittest.main()
