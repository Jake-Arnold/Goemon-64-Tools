"""The same virtual flag editor is used for USA and Japan gameplay."""
import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.game_versions import VERSIONS
from tests.test_unlocks import FakeRAM


class UnlockFlagsUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.geometry('1080x760+0+0')
        for target, value in (
                ('practice.toolkit.save_last_region', None),
                ('practice.toolkit.load_remembered_rom', None)):
            patcher = (patch(target) if value is None and 'save' in target
                       else patch(target, return_value=None))
            patcher.start()
            self.addCleanup(patcher.stop)
        self.app = Toolkit(
            self.root, parse_args(['--game-version', 'usa', '--enable-hex-edit']))
        self.addCleanup(self._close)
        self.root.update_idletasks()

    def _close(self):
        try:
            for callback in self.root.tk.call('after', 'info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def _open_flags(self):
        app = self.app
        app.notebook.select(app.unlock_tab)
        app.unlock_sections.select(app.unlock_flags_page)
        app.on_unlock_section_changed()
        app.refresh_unlock_flags(force=True)
        self.root.update_idletasks()

    def _expand_to(self, key):
        app = self.app
        flag = app.unlock_flag_rows[key]
        section = (flag.group, flag.subtype)
        app._set_unlock_flag_section_expanded(section, True)
        self.root.update_idletasks()
        self.assertTrue(app.unlock_flag_view.scroll_to_key(key))
        self.root.update_idletasks()
        self.assertIn(key, app.unlock_flag_widgets)
        return app.unlock_flag_widgets[key]

    def _japan(self):
        app = self.app
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key, 'japan')

    def _connected_japan(self):
        self._japan()
        self.app.jp_rdram = FakeRAM()
        self.app.game_pid = 1234
        self.app.jp_backend = 'project64'
        self.app.connection_target.set('project64')

    def test_one_notebook_one_virtual_editor_for_both_releases(self):
        app = self.app
        self.assertEqual(
            [app.unlock_sections.tab(index, 'text')
             for index in app.unlock_sections.tabs()],
            ['Items & equipment', 'Story & event flags'])
        view = app.unlock_flag_view
        self.assertGreater(len(app.unlock_flag_rows), 100)
        self._open_flags()
        self.assertIs(app.unlock_flag_view, view)
        self._japan()
        self.assertIs(app.unlock_flag_view, view)
        self.assertIs(app.unlock_flag_canvas, view.canvas)
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].address, 0x80161DFC)
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertIs(app.unlock_flag_view, view)
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].address, 0x8015C60C)

    def test_large_folder_is_virtual_with_one_scrollbar_and_real_buttons(self):
        app = self.app
        app.mem = FakeRAM()
        self._open_flags()
        key = next(f.key for f in app.unlock_flag_section_rows[
            ('Fortune Dolls', 'Unsorted')])
        row = self._expand_to(key)
        self.assertEqual(len(app.unlock_flag_section_rows[
            ('Fortune Dolls', 'Unsorted')]), 45)
        self.assertLess(app.unlock_flag_view.widget_count, 36)
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        items = list(descendants(app.unlock_flag_shell))
        self.assertEqual(sum(isinstance(w, ttk.Scrollbar) for w in items), 1)
        self.assertFalse(any(isinstance(w, ttk.Treeview) for w in items))
        self.assertEqual((row['off'].cget('text'), row['on'].cget('text')),
                         ('Off', 'On'))
        last = app.unlock_flag_section_rows[('Fortune Dolls', 'Unsorted')][-1]
        self.assertTrue(app.unlock_flag_view.scroll_to_key(last.key))
        self.assertIn(last.key, app.unlock_flag_widgets)
        self.assertLess(app.unlock_flag_view.widget_count, 36)

    def test_usa_masked_flag_write_preserves_other_bits(self):
        app = self.app
        app.mem = FakeRAM()
        app.mem.bytes[0x8015C60C] = 0x81
        self._open_flags()
        row = self._expand_to('benkei_encounter')
        self.assertEqual(row['state'].get(), 'Off')
        row['on'].invoke()
        self.assertEqual(app.mem.bytes[0x8015C60C], 0xA1)
        self.assertEqual(row['state'].get(), 'On')
        row['off'].invoke()
        self.assertEqual(app.mem.bytes[0x8015C60C], 0x81)

    def test_usa_stale_snapshot_blocks_write(self):
        app = self.app
        ram = FakeRAM()
        app.mem = ram
        self._open_flags()
        row = self._expand_to('benkei_encounter')
        ram.bytes[0x8015C60C] = 0x10
        row['on'].invoke()
        self.assertEqual(ram.writes, [])
        self.assertIn('changed', app.unlock_flag_feedback.get())

    def test_japan_uses_same_buttons_and_correct_candidate_address(self):
        app = self.app
        self._connected_japan()
        self._open_flags()
        row = self._expand_to('benkei_encounter')
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            row['on'].invoke()
            writer.assert_called_once_with(
                0x80161DFC, b'\x20', expected=b'\x00')
        candidate = app.unlock_flag_rows['oedo_old_man_dialogue_cycle']
        self.assertEqual(candidate.source, 'JP offset candidate')
        row = self._expand_to(candidate.key)
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            row['on'].invoke()
            writer.assert_called_once_with(
                candidate.address, bytes((candidate.mask,)),
                expected=b'\x00')

    def test_japan_external_flag_changes_only_one_bit(self):
        app = self.app
        self._connected_japan()
        app.jp_rdram.bytes[0x80161DF8] = 0x04
        app.jp_rdram.bytes[0x80161EF3] = 0x01
        self._open_flags()
        row = self._expand_to('external_super_pass')
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            row['on'].invoke()
            writer.assert_called_once_with(
                0x80161DF8, b'\x05', expected=b'\x04')
        self.assertEqual(app.jp_rdram.bytes[0x80161EF3], 0x01)

    def test_readonly_disconnect_and_region_change_disable_stale_actions(self):
        app = self.app
        app.mem = FakeRAM()
        self._open_flags()
        row = self._expand_to('benkei_encounter')
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        self.assertIn('disabled', row['off'].state())
        self.assertIn('disabled', row['on'].state())
        with patch.object(app, 'set_unlock_flag') as writer:
            row['on'].invoke()
            writer.assert_not_called()
        app.args.read_only = False
        app.mem = None
        app.refresh_unlock_flags(force=True)
        self.assertIn('disabled', row['on'].state())
        self._japan()
        self.assertNotIn('benkei_encounter', app.unlock_flag_widgets)

    def test_filters_only_change_logical_rows_and_reuse_pool(self):
        app = self.app
        self._open_flags()
        view = app.unlock_flag_view
        app.unlock_flag_query.set('benkei')
        self.assertLess(
            int(app.unlock_flag_counter.get().split(' / ')[0]),
            len(app.unlock_flag_rows))
        self.assertIn('benkei_encounter', [
            item[1].key for item in view.rows if item[0] == 'flag'])
        pool = view.widget_count
        app.unlock_flag_query.set('')
        self.assertIs(view, app.unlock_flag_view)
        self.assertGreaterEqual(view.widget_count, pool)
        app.unlock_flag_type.set('Benkei & Kihachi')
        app.on_unlock_flag_type_changed()
        self.assertIn('Unsorted', app.unlock_flag_subtype_box['values'])

    def test_collapsed_folders_have_no_flag_widget_allocations(self):
        app = self.app
        self._open_flags()
        self.assertEqual(app.unlock_flag_expanded, set())
        self.assertEqual(app.unlock_flag_view.widget_count,
                         len(app.unlock_flag_view._header_pool))
        section = ('Fortune Dolls', 'Unsorted')
        app.toggle_unlock_flag_section(section)
        self.assertIn(section, app.unlock_flag_expanded)
        app.toggle_unlock_flag_section(section)
        self.assertNotIn(section, app.unlock_flag_expanded)

    def test_idle_tick_does_not_refresh_disconnected_hidden_unlocks(self):
        app = self.app
        self.assertIsNone(app.mem)
        self.assertIsNone(app.jp_rdram)
        with (patch.object(app, '_watch_japan_process_restart'),
              patch.object(app, '_refresh_unlocks_on_reader_change') as poll,
              patch.object(app, 'refresh_unlocks') as refresh,
              patch.object(self.root, 'after')):
            app.tick()
            poll.assert_called_once_with()
            refresh.assert_not_called()


if __name__ == '__main__':
    unittest.main()
