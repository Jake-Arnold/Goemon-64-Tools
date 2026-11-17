"""Tk integration of the shared Items / Story Flags Unlocks views."""
import tkinter as tk
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
        self.root.withdraw()
        remember = patch('practice.toolkit.save_last_region')
        remember.start()
        self.addCleanup(remember.stop)
        cache = patch('practice.toolkit.load_remembered_rom', return_value=None)
        cache.start()
        self.addCleanup(cache.stop)
        self.app = Toolkit(self.root, parse_args([
            '--game-version', 'usa', '--enable-hex-edit']))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for callback in self.root.tk.call('after', 'info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def _select_japan(self):
        app = self.app
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key, 'japan')

    def test_two_pages_keep_all_old_item_controls(self):
        app = self.app
        self.assertEqual([
            app.unlock_sections.tab(item, 'text')
            for item in app.unlock_sections.tabs()],
            ['Items & equipment', 'Story & event flags'])
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertEqual(len(app.unlock_row_widgets), 34)
        self.assertGreater(len(app.unlock_flag_rows), 100)
        self.assertTrue(app.unlock_flag_tree.exists('benkei_encounter'))
        app.unlock_sections.select(app.unlock_flags_page)
        app.mem = FakeRAM()
        app.refresh_unlock_flags(force=True)
        app.unlock_flag_tree.selection_set('benkei_encounter')
        app.select_unlock_flag()
        self.assertNotIn('disabled', app.unlock_flag_set.state())

    def test_usa_flag_set_clear_preserves_other_bits(self):
        app = self.app
        app.mem = FakeRAM()
        app.mem.bytes[0x8015C60C] = 0x81
        app.unlock_sections.select(app.unlock_flags_page)
        app.refresh_unlock_flags(force=True)
        app.unlock_flag_tree.selection_set('benkei_encounter')
        app.select_unlock_flag()
        app.set_unlock_flag('Set')
        self.assertEqual(app.mem.bytes[0x8015C60C], 0xA1)
        app.set_unlock_flag('Clear')
        self.assertEqual(app.mem.bytes[0x8015C60C], 0x81)
        self.assertEqual(app.mem.writes[0][0], 0x8015C60C)
        self.assertEqual(app.mem.writes[1][0], 0x8015C60C)

    def test_usa_stale_and_read_only_refuse_writes(self):
        app = self.app
        ram = FakeRAM()
        app.mem = ram
        app.refresh_unlock_flags(force=True)
        app.unlock_flag_tree.selection_set('benkei_encounter')
        app.select_unlock_flag()
        ram.bytes[0x8015C60C] = 0x10
        app.set_unlock_flag('Set')
        self.assertEqual(ram.writes, [])
        self.assertIn('blocked', app.unlock_status.get())
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        app.select_unlock_flag()
        self.assertIn('disabled', app.unlock_flag_set.state())
        app.set_unlock_flag('Set')
        self.assertEqual(ram.writes, [])

    def test_japan_only_live_confirmed_benkei_can_be_toggled(self):
        app = self.app
        self._select_japan()
        ram = FakeRAM()
        ram.bytes[0x80161DFC] = 0x81
        app.jp_rdram = ram
        app.game_pid = 1234
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        app.unlock_sections.select(app.unlock_flags_page)
        app.refresh_unlock_flags(force=True)
        benkei = app.unlock_flag_rows['benkei_encounter']
        self.assertEqual(benkei.address, 0x80161DFC)
        self.assertTrue(benkei.editable)
        app.unlock_flag_tree.selection_set('benkei_encounter')
        app.select_unlock_flag()
        self.assertNotIn('disabled', app.unlock_flag_set.state())
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            app.set_unlock_flag('Set')
            writer.assert_called_once_with(
                0x80161DFC, b'\xA1', expected=b'\x81')
        candidate = app.unlock_flag_rows['oedo_old_man_dialogue_cycle']
        self.assertFalse(candidate.editable)
        app.unlock_flag_tree.selection_set(candidate.key)
        app.select_unlock_flag()
        self.assertIn('disabled', app.unlock_flag_set.state())
        with patch.object(app, 'write_japan_raw_bytes') as writer:
            app.set_unlock_flag('Set')
            writer.assert_not_called()

    def test_flag_filter_and_region_switch_remove_stale_rows(self):
        app = self.app
        app.unlock_flag_query.set('Benkei')
        self.assertLess(len(app.unlock_flag_tree.get_children()),
                        len(app.unlock_flag_rows))
        self.assertTrue(app.unlock_flag_tree.exists('benkei_encounter'))
        self._select_japan()
        self.assertNotIn('external_sasuke_recruited',
                         app.unlock_flag_rows)
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertIn('external_sasuke_recruited',
                      app.unlock_flag_rows)
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].address,
                         0x8015C60C)
        app.unlock_flag_query.set('')
        self.assertEqual(len(app.unlock_flag_tree.get_children()),
                         len(app.unlock_flag_rows))


if __name__ == '__main__':
    unittest.main()
