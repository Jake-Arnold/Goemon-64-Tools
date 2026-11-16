"""Japanese right-click Freeze/Unfreeze Tk smoke tests; no emulator process."""
import tkinter as tk
import unittest
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import patch

from practice.game_versions import VERSIONS
from practice.inspector import Watch
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
)
from practice.toolkit import Toolkit
from tests.test_japanese_fields import FakeRam


class JapanRawFreezeUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root=tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        store = patch('practice.toolkit.save_last_region')
        store.start(); self.addCleanup(store.stop)
        patches=[
            patch('practice.toolkit.load_remembered_rom', return_value=None),
            patch('practice.toolkit.load_named_checkpoints', return_value=[]),
        ]
        for handle in patches:
            handle.start()
            self.addCleanup(handle.stop)
        self.app=Toolkit(self.root, Namespace(
            pid=None, base=None, endian='auto', route=None,
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, read_only=False))
        self.addCleanup(self._close)
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.jp_rdram=FakeRam({
            (JAPAN_DEBUG_ENGINE_MODE,1):b'\x0d',
            (JAPAN_DEBUG_SCENE,2):bytes.fromhex('0161'),
            (JAPAN_DEBUG_CHARACTER,4):bytes(4),
            (JAPAN_DEBUG_LOADING,4):bytes(4),
            (0x80161EEF,1):b'\x01',
        })
        self.app.game_pid=1234
        self.app.jp_backend='project64'
        self.app.connection_target.set('project64')
        self.watch=Watch('Triton Test',0x80161EEF,'On','01','OK','Japan-test')
        self.app.watch_rows=[self.watch]
        self.app.draw_watches()

    def _close(self):
        try:
            for handle in self.root.tk.call('after','info'):
                self.root.after_cancel(handle)
            self.root.destroy()
        except tk.TclError:
            pass

    def _right_click(self):
        app=self.app
        with patch.object(app.watch_tree, 'identify_row',
                          return_value=self.watch.name), \
             patch.object(app.watch_context_menu,'tk_popup'):
            app.open_live_watch_menu(
                SimpleNamespace(y=5,x_root=100,y_root=100))

    def test_japanese_right_click_freeze_and_unfreeze_are_enabled(self):
        app=self.app
        self._right_click()
        self.assertEqual(app.watch_context_menu.entrycget(2,'label'),
                         'Freeze value')
        self.assertEqual(app.watch_context_menu.entrycget(2,'state'),'normal')
        with patch.object(app,'_ensure_freeze_worker'):
            app.watch_context_menu.invoke(2)
        self.assertEqual(app.value_freezes.get(0x80161EEF).value,b'\x01')
        self._right_click()
        self.assertEqual(app.watch_context_menu.entrycget(2,'label'),
                         'Unfreeze value')
        app.watch_context_menu.invoke(2)
        self.assertIsNone(app.value_freezes.get(0x80161EEF))

    def test_japan_freeze_refused_in_readonly_and_stops_on_region_switch(self):
        app=self.app
        self._right_click()
        with patch.object(app,'_ensure_freeze_worker'):
            app.watch_context_menu.invoke(2)
        self.assertTrue(app.value_freezes.active())
        app.args.read_only=True
        self._right_click()
        self.assertEqual(app.watch_context_menu.entrycget(2,'state'),'disabled')
        app.args.read_only=False
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertFalse(app.value_freezes.active())


if __name__=='__main__':
    unittest.main()
