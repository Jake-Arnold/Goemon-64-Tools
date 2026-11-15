"""Shared USA/Japan Unlocks Tk presentation and guarded button routing."""
import tkinter as tk
import unittest
from argparse import Namespace
from unittest.mock import patch

from practice.game_versions import VERSIONS
from practice.toolkit import Toolkit
from practice.unlocks import UNLOCKS
from tests.test_japanese_fields import FakeRam


class RegionUnlockUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk display required: {exc}')
        self.root.withdraw()
        cache = patch('practice.toolkit.load_remembered_rom', return_value=None)
        cache.start()
        self.addCleanup(cache.stop)
        self.app = Toolkit(self.root, Namespace(
            pid=None, base=None, endian='auto', route=None,
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, read_only=False,
            enable_japan_party_writes=False))
        self.addCleanup(self._close_root)

    def _close_root(self):
        try:
            for callback in self.root.tk.call('after', 'info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def _select_japan(self):
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.assertEqual(self.app.active_version.key, 'japan')

    def test_all_34_rows_keep_controls_and_unknown_addresses(self):
        app = self.app
        usa_labels = {
            item.address: app.unlock_address_labels[item.address].cget('text')
            for item in UNLOCKS
        }
        self.assertEqual(len(app.unlock_row_widgets), 34)
        self.assertEqual(
            usa_labels[0x8015C6A7], '8015C6A7')
        self._select_japan()
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertEqual(len(app.unlock_row_widgets), 34)
        self.assertEqual(
            app.unlock_address_labels[0x8015C69F].cget('text'), 'unknown')
        self.assertEqual(
            app.unlock_address_labels[0x8015C6A7].cget('text'), '80161E97')
        self.assertEqual(
            app.unlock_row_widgets[0x8015C69F][0].cget('text'), 'unknown')
        self.assertIn('disabled', app.unlock_all_button.state())
        for item in UNLOCKS:
            _state, buttons = app.unlock_row_widgets[item.address]
            self.assertEqual(set(buttons), set(item.values))
        self.assertFalse(hasattr(app, 'jp_unlock_panel'))
        self.assertFalse(hasattr(app, 'jp_unlock_table'))
        self.assertFalse(hasattr(app, 'jp_unlock_buttons'))
        self.assertFalse(hasattr(app, 'jp_party_buttons'))
        self.assertEqual(
            [app.jp_research_tabs.tab(x, 'text')
             for x in app.jp_research_tabs.tabs()], ['Goemon XYZ', 'Scene warp'])

    def test_only_verified_japanese_party_on_routes_to_existing_writer(self):
        app = self.app
        self._select_japan()
        app.args.enable_japan_party_writes = True
        app.jp_rdram = FakeRam({
            (0x80161E97, 1): bytes((0,)),
            (0x80161E9B, 1): bytes((0,)),
        })
        app.game_pid = 1234
        app.verified_rom_path = 'verified-japan-rom.n64'
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        app.refresh_unlocks(force=True)
        sasuke = next(row for row in UNLOCKS if row.label == 'Sasuke in party')
        yae = next(row for row in UNLOCKS if row.label == 'Yae in party')
        goemon = next(row for row in UNLOCKS if row.label == 'Goemon in party')
        self.assertNotIn('disabled', app.unlock_row_widgets[sasuke.address][1][1].state())
        self.assertIn('disabled', app.unlock_row_widgets[sasuke.address][1][0].state())
        self.assertNotIn('disabled', app.unlock_row_widgets[yae.address][1][1].state())
        self.assertIn('disabled', app.unlock_row_widgets[goemon.address][1][1].state())
        with patch.object(app, 'enable_japan_party') as guarded:
            app.set_unlock(sasuke, 1)
            guarded.assert_called_once_with(2)
            guarded.reset_mock()
            app.set_unlock(yae, 1)
            guarded.assert_called_once_with(3)
            guarded.reset_mock()
            app.set_unlock(sasuke, 0)
            app.set_unlock(goemon, 1)
            guarded.assert_not_called()
        self.assertIn('unknown', app.unlock_status.get())
        app.args.read_only = True
        app.refresh_unlocks(force=True)
        self.assertIn('disabled', app.unlock_row_widgets[yae.address][1][1].state())

    def test_switch_back_to_usa_restores_addresses_and_enabled_controls(self):
        app = self.app
        self._select_japan()
        self.assertEqual(
            app.unlock_address_labels[0x8015C69F].cget('text'), 'unknown')
        self.assertIn('disabled', app.unlock_count_buttons[0x8015C71B].state())
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key, 'usa')
        self.assertEqual(
            app.unlock_address_labels[0x8015C69F].cget('text'), '8015C69F')
        self.assertEqual(
            app.unlock_address_labels[0x8015C6A7].cget('text'), '8015C6A7')
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertNotIn('disabled', app.unlock_row_widgets[0x8015C6A7][1][0].state())
        self.assertNotIn('disabled', app.unlock_count_buttons[0x8015C71B].state())
        self.assertNotIn('disabled', app.unlock_all_button.state())


if __name__ == '__main__':
    unittest.main()
