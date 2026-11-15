"""ROM-free Japan native debug-menu entry tests; no emulators involved."""
import unittest

from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING, JAPAN_DEBUG_SUBMODE,
    JAPAN_DEBUG_EXIT, get_japan_debug_context,
    debug_menu_selection_hint, enter_japan_native_debug_menu,
)
from tests.test_japanese_party_unlock import Process


def debugger(endian='wordswapped', *, state=13, scene=0x161,
             character=0, loading=0, submode=2, exit_flag=0):
    p = Process(endian)
    p.set_guest(JAPAN_DEBUG_ENGINE_MODE, bytes([state]))
    p.set_guest(JAPAN_DEBUG_SCENE, scene.to_bytes(2, 'big'))
    p.set_guest(JAPAN_DEBUG_CHARACTER, character.to_bytes(4, 'big'))
    p.set_guest(JAPAN_DEBUG_LOADING, loading.to_bytes(4, 'big'))
    p.set_guest(JAPAN_DEBUG_SUBMODE, bytes([submode]))
    p.set_guest(JAPAN_DEBUG_EXIT, bytes([exit_flag]))
    p.writes.clear()
    return p


class JapaneseDebugMenuCoreTests(unittest.TestCase):
    def test_known_debug_engine_address_and_source_selection_hint(self):
        self.assertEqual(JAPAN_DEBUG_ENGINE_MODE, 0x800CD284)
        self.assertEqual(debug_menu_selection_hint(0x161), ('MACHI', 3))
        self.assertEqual(debug_menu_selection_hint(0x1D1), ('SHOP', 0x41))
        for bad in (True, -1, 0xFFFF, '0x161'):
            with self.assertRaises(ValueError):
                debug_menu_selection_hint(bad)

    def test_single_native_debug_state_write_both_endians(self):
        for endian in ('big', 'wordswapped'):
            with self.subTest(endian=endian):
                p = debugger(endian)
                before = get_japan_debug_context(p.rdram())
                result = enter_japan_native_debug_menu(
                    p.rdram(), 0x161, expected_context=before)
                self.assertTrue(result.changed)
                self.assertEqual((result.before_state, result.observed_state),
                                 (13, 10))
                self.assertEqual((result.category_hint, result.menu_index_hint),
                                 ('MACHI', 3))
                self.assertEqual(p.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1),
                                 bytes([10]))
                self.assertEqual(p.rdram().read_guest(JAPAN_DEBUG_SCENE, 2),
                                 bytes.fromhex('0161'))
                self.assertEqual(len(p.writes), 1)
                self.assertEqual(len(p.writes[0][1]), 1 if endian == 'big' else 4)
                self.assertEqual(
                    p.writes[0][0],
                    0xCD284 if endian == 'big' else (0xCD284 & ~3))
                self.assertEqual(
                    result.suggested_destination, 0x161)

    def test_reject_non_gameplay_and_changed_context_with_no_write(self):
        cases = [
            dict(state=10), dict(state=12), dict(scene=0),
            dict(character=4), dict(loading=1), dict(submode=4),
            dict(exit_flag=1),
        ]
        for case in cases:
            with self.subTest(case=case):
                p = debugger(**case)
                with self.assertRaisesRegex(RuntimeError, 'refused'):
                    enter_japan_native_debug_menu(
                        p.rdram(), 0x161,
                        expected_context=get_japan_debug_context(p.rdram()))
                self.assertEqual(p.writes, [])

        p = debugger()
        before = get_japan_debug_context(p.rdram())
        p.set_guest(JAPAN_DEBUG_SCENE, (0x162).to_bytes(2, 'big'))
        with self.assertRaisesRegex(RuntimeError, 'changed'):
            enter_japan_native_debug_menu(
                p.rdram(), 0x161, expected_context=before)
        self.assertEqual(p.writes, [])

    def test_all_four_characters_can_enter_native_reload_gameplay(self):
        for character in range(4):
            with self.subTest(character=character):
                p = debugger(character=character, scene=0x00F, submode=0)
                context = get_japan_debug_context(p.rdram())
                self.assertEqual(context[2], character)
                result = enter_japan_native_debug_menu(
                    p.rdram(), 0x161, expected_context=context)
                self.assertTrue(result.changed)

    def test_readonly_ram_prevents_native_debug_write(self):
        p = debugger()
        snapshot = get_japan_debug_context(p.rdram())
        p.writable = False
        with self.assertRaises(PermissionError):
            enter_japan_native_debug_menu(
                p.rdram(), 0x161, expected_context=snapshot)
        self.assertEqual(p.writes, [])


if __name__ == '__main__':
    unittest.main()
