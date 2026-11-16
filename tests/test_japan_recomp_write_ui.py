"""Japanese native recomp must expose the same mapped write controls as JP emulators.

GUI tests exercise the actual Tk button states. No game is launched or modified.
"""
from __future__ import annotations

import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.game_versions import VERSIONS
from practice.unlocks import UNLOCKS
from practice.japan_story_progress import JAPAN_PROGRESS_ITEMS
from tests.test_japanese_fields import FakeRam


class JapanRecompWriteUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display not available: {exc}")
        self.root.withdraw()
        with patch('practice.toolkit.load_last_region', return_value='usa'), \
             patch('practice.toolkit.load_remembered_rom', return_value=None), \
             patch('practice.toolkit.save_last_region'):
            self.app = Toolkit(self.root, parse_args([]))
            self.app.game_version_choice.set(VERSIONS['japan'].label)
            self.app.on_game_version_changed()
        self.app.jp_rdram = FakeRam({
            (0x80161E97, 1): bytes((0,)),
            (0x80161E9B, 1): bytes((0,)),
        })
        self.app.game_pid = 86420
        self.app.jp_backend = 'recomp'
        self.app.connection_target.set('recomp')
        self.app.verified_rom_path = 'verified-japan-0.rom'

    def tearDown(self):
        try:
            if self.root.winfo_exists():
                self.root.destroy()
        except tk.TclError:
            pass

    def test_native_recomp_unblocks_japan_unlock_xyz_debug_and_raw_controls(self):
        app = self.app
        app.refresh_unlocks(force=True)
        app.refresh_japan_party_controls()
        self.assertTrue(app._japan_unlock_controls_ready())
        self.assertNotIn('disabled', app.unlock_all_button.state())
        sasuke = next(item for item in UNLOCKS if item.label == 'Sasuke in party')
        self.assertNotIn(
            'disabled', app.unlock_row_widgets[sasuke.address][1][1].state())
        self.assertNotIn('disabled', app.jp_position_apply_button.state())
        self.assertNotIn('disabled', app.jp_debug_menu_button.state())
        self.assertNotIn('disabled', app.raw_write_btn.state())
        self.assertNotIn('disabled', app.freeze_raw_button.state())
        self.assertTrue(app._freeze_worker_connection()[2])

    def test_native_recomp_raw_editor_uses_checked_japan_write_backend(self):
        app = self.app
        app.raw_address.set('80161E97')
        app.raw_width.set('1')
        app.raw_value.set('01')
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as write, \
             patch('practice.ui_extension.checked_write') as usa:
            app.write_raw_hex()
        write.assert_called_once_with(0x80161E97, bytes((1,)), expected=bytes((0,)))
        usa.assert_not_called()

    def test_disconnect_or_readonly_disables_recomp_mapped_writes(self):
        app = self.app
        app.args.read_only = True
        app.refresh_unlocks(force=True)
        app.refresh_japan_party_controls()
        self.assertFalse(app._japan_unlock_controls_ready())
        self.assertIn('disabled', app.unlock_all_button.state())
        self.assertIn('disabled', app.jp_position_apply_button.state())
        self.assertIn('disabled', app.jp_debug_menu_button.state())
        self.assertFalse(app._freeze_worker_connection()[2])
        app.args.read_only = False
        app.connection_target.set('mupen64plus')
        app.refresh_unlocks(force=True)
        app.refresh_japan_party_controls()
        self.assertIn('disabled', app.unlock_all_button.state())
        self.assertIn('disabled', app.jp_position_apply_button.state())
        self.assertIn('disabled', app.jp_debug_menu_button.state())

    def test_native_recomp_story_progress_inventory_editor_enabled(self):
        app = self.app
        app.jp_rdram.values[(0x8016204B, 1)] = bytes((1,))
        app.refresh_story_progress()
        app.story_sections.select(0)
        app.story_tables['All'].selection_set('jp_unlock_star')
        app.select_story_edit()
        self.assertNotIn('disabled', app.story_edit_button.state())
        self.assertEqual(tuple(app.story_edit_combo['values']),
                         ('0x00', '0x01'))
        self.assertEqual(JAPAN_PROGRESS_ITEMS['star'].label, 'Star')

    def test_native_recomp_freeze_permission_accepts_valid_gameplay(self):
        app = self.app
        with patch('practice.value_freezes_ui.stable_japan_gameplay',
                   return_value=(13, 0x161, 0, 0)):
            app.require_freeze_access(raw=True)
            app.args.read_only = True
            with self.assertRaises(PermissionError):
                app.require_freeze_access(raw=True)

    def test_unmapped_japanese_fields_stay_distinct_from_usa_writers(self):
        app = self.app
        app.refresh_unlocks(force=True)
        self.assertIn('disabled', app.freeze_health_button.state())
        self.assertIn('disabled', app.god_mode_button.state())
        self.assertIn('disabled', app.enemy_pass_through_button.state())


if __name__ == '__main__':
    unittest.main()
