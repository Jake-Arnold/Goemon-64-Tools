"""Tk smoke tests for verified Japanese Story Progress controls and stale values."""
import tkinter as tk
import unittest
from argparse import Namespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.game_versions import VERSIONS
from practice.japan_story_progress import JAPAN_PROGRESS_ITEMS
from tests.test_japanese_fields import FakeRam


class JapanStoryProgressUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root=tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk unavailable: {exc}')
        self.root.withdraw()
        store = patch('practice.toolkit.save_last_region')
        store.start(); self.addCleanup(store.stop)
        patcher=patch('practice.toolkit.load_remembered_rom',return_value=None)
        patcher.start()
        self.addCleanup(patcher.stop)
        metadata=patch('practice.toolkit.load_named_checkpoints',return_value=[])
        metadata.start()
        self.addCleanup(metadata.stop)
        self.app=Toolkit(self.root,Namespace(
            pid=None, base=None, endian='auto', route=None,
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, read_only=False))
        self.addCleanup(self._close)
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.jp_rdram=FakeRam({
            (0x8016204B,1):b'\x01',
            (0x80161EF7,1):b'\x04',
        })
        self.app.game_pid=1234
        self.app.jp_backend='project64'
        self.app.connection_target.set('project64')
        self.app.refresh_story_progress()

    def _close(self):
        try:
            for callback in self.root.tk.call('after','info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def test_verified_japan_progress_rows_grouped_and_battery_not_reinterpreted(self):
        app=self.app
        self.assertEqual(app._story_display_region,'japan')
        self.assertTrue(app.story_tables['Fortune Dolls'].exists(
            'jp_unlock_silver_fortune_doll_progress'))
        self.assertTrue(app.story_tables['Collectibles & Miracles'].exists(
            'jp_unlock_star'))
        self.assertEqual(app.story_tables['All'].item(
            'jp_unlock_star','values')[3],'0x01')
        self.assertFalse(app.story_tables['All'].exists(
            'jp_unlock_sasuke_battery_1_collected'))
        self.assertIn('user-verified',app.story_notes.get())

    def test_select_and_edit_japan_story_progress_routes_mapped_write(self):
        app=self.app
        app.story_sections.select(0)
        row='jp_unlock_star'
        app.story_tables['All'].selection_set(row)
        app.select_story_edit()
        self.assertNotIn('disabled',app.story_edit_button.state())
        self.assertEqual(tuple(app.story_edit_combo['values']),
                         ('0x00','0x01'))
        app.story_edit_choice.set('0x00')
        with patch.object(app,'apply_japan_unlocks',return_value=(1,1)) as write:
            app.apply_story_edit()
        write.assert_called_once_with(((JAPAN_PROGRESS_ITEMS['star'],0),))
        self.assertIn('Star: 0x00',app.story_edit_status.get())

    def test_stale_japan_progress_byte_rejected_before_write(self):
        app=self.app
        app.story_sections.select(0)
        app.story_tables['All'].selection_set('jp_unlock_star')
        app.select_story_edit()
        app.story_edit_choice.set('0x00')
        app.jp_rdram.values[(0x8016204B,1)]=b'\x00'
        with patch.object(app,'apply_japan_unlocks') as write:
            app.apply_story_edit()
        write.assert_not_called()
        self.assertIn('changed',app.story_edit_status.get())

    def test_usa_region_still_uses_original_story_model(self):
        app=self.app
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key,'usa')
        app.refresh_story_progress()
        self.assertEqual(app._story_display_region,'usa')
        self.assertFalse(app.story_tables['All'].exists('jp_unlock_star'))


if __name__=='__main__':
    unittest.main()
