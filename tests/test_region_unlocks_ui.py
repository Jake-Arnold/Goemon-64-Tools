"""Shared USA/Japan Unlocks Tk presentation and guarded button routing."""
import tkinter as tk
import unittest
from argparse import Namespace
from types import SimpleNamespace
from practice.inspector import Watch
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

    def test_all_mapped_japanese_fields_write_without_opt_in_or_consent(self):
        app = self.app
        self._select_japan()
        app.jp_rdram = FakeRam({
            (0x80161E97, 1): bytes((0,)),
            (0x80161E9B, 1): bytes((0,)),
            (0x80161EEF, 1): bytes((0,)),
            (0x80161F07, 1): bytes((0,)),
            (0x80161F13, 1): bytes((2,)),
        })
        app.game_pid = 1234
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        app.refresh_unlocks(force=True)
        sasuke = next(x for x in UNLOCKS if x.label == 'Sasuke in party')
        yae = next(x for x in UNLOCKS if x.label == 'Yae in party')
        triton = next(x for x in UNLOCKS if x.label == 'Triton Shell')
        cucumber = next(x for x in UNLOCKS if x.label == 'Cucumber')
        fish = next(x for x in UNLOCKS if x.label == 'Blue fish count')
        goemon = next(x for x in UNLOCKS if x.label == 'Goemon in party')
        for item in (sasuke, yae, triton, cucumber):
            for button in app.unlock_row_widgets[item.address][1].values():
                self.assertNotIn('disabled', button.state())
        self.assertNotIn('disabled', app.unlock_count_buttons[fish.address].state())
        self.assertNotIn('disabled', app.unlock_all_button.state())
        self.assertIn('disabled', app.unlock_row_widgets[goemon.address][1][1].state())
        with patch.object(app, 'apply_japan_unlocks', return_value=(1, 1)) as write:
            app.set_unlock(sasuke, 0)
            write.assert_called_with(((sasuke, 0),))
            app.set_unlock(yae, 1)
            write.assert_called_with(((yae, 1),))
            app.set_unlock(triton, 1)
            write.assert_called_with(((triton, 1),))
            app.set_unlock(cucumber, 0)
            write.assert_called_with(((cucumber, 0),))
            app.set_unlock_hex(fish, '03')
            write.assert_called_with(((fish, 3),))
            write.reset_mock()
            app.set_unlock(goemon, 1)
            write.assert_not_called()
        self.assertIn('unknown', app.unlock_status.get())
        with patch.object(app, 'apply_japan_unlocks', return_value=(9, 9)) as write:
            app.unlock_all_items()
            self.assertEqual(len(write.call_args.args[0]), 9)
        app.args.read_only = True
        app.refresh_unlocks(force=True)
        self.assertIn('disabled', app.unlock_row_widgets[yae.address][1][1].state())
        self.assertIn('disabled', app.unlock_count_buttons[fish.address].state())
        self.assertIn('disabled', app.unlock_all_button.state())

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


    def test_unlock_mouse_wheel_bound_to_cards_and_buttons(self):
        app = self.app
        self.assertTrue(app.unlock_canvas.bind('<MouseWheel>'))
        self.assertTrue(app.unlock_canvas.bind('<Button-4>'))
        button = app.unlock_row_widgets[0x8015C6A7][1][1]
        self.assertTrue(button.bind('<MouseWheel>'))
        self.assertEqual(
            app._unlock_wheel(SimpleNamespace(delta=-120, num=None)), 'break')
        self._select_japan()
        self.assertTrue(button.bind('<MouseWheel>'))

    def test_japanese_live_memory_context_menu_and_hex_edit(self):
        app = self.app
        self._select_japan()
        app.jp_rdram = FakeRam({(0x80161EEF, 1): bytes((0,))})
        app.game_pid = 1234
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        row_name = 'Items: Triton Shell'
        app.watch_rows = [Watch(
            row_name, 0x80161EEF, 'No (0)', '00', 'External lead',
            'Japanese sourced item')]
        app.draw_watches()
        self.assertTrue(app.watch_tree.exists(row_name))
        mouse = SimpleNamespace(y=6, x_root=100, y_root=100)
        with patch.object(app.watch_tree, 'identify_row', return_value=row_name), \
             patch.object(app.watch_context_menu, 'tk_popup'):
            app.open_live_watch_menu(mouse)
        self.assertIn('Edit value', app.watch_context_menu.entrycget(0, 'label'))
        self.assertEqual(app.watch_context_menu.entrycget(0, 'state'), 'normal')
        with patch('practice.ui_extension.simpledialog.askstring',
                   return_value='0x01') as dialog, \
             patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer, \
             patch.object(app, 'refresh_inspector'):
            app.edit_live_watch_value(row_name)
        writer.assert_called_once_with(
            0x80161EEF, bytes((1,)), expected=bytes((0,)))
        self.assertEqual(dialog.call_count, 1)
        self.assertIn('Verified write', app.inspector_status.get())

        app.args.read_only = True
        with patch.object(app.watch_tree, 'identify_row', return_value=row_name), \
             patch.object(app.watch_context_menu, 'tk_popup'):
            app.open_live_watch_menu(mouse)
        self.assertEqual(app.watch_context_menu.entrycget(0, 'state'),
                         'disabled')


if __name__ == '__main__':
    unittest.main()
