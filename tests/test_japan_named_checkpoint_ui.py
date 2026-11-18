"""Japanese named native state slots dispatch only to verified matching emulator."""
import tkinter as tk
import unittest
from argparse import Namespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.game_versions import VERSIONS
from tests.test_japanese_fields import FakeRam
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
)


class JapanNamedCheckpointUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root=tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk unavailable: {exc}')
        self.root.withdraw()
        store = patch('practice.toolkit.save_last_region')
        store.start(); self.addCleanup(store.stop)
        for name, val in (
            ('practice.toolkit.load_remembered_rom', None),
            ('practice.toolkit.load_named_checkpoints', []),
        ):
            mock=patch(name,return_value=val)
            mock.start()
            self.addCleanup(mock.stop)
        self.app=Toolkit(self.root,Namespace(
            pid=None, base=None, endian='auto', route=None,
            game_version='usa',
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, read_only=False))
        self.addCleanup(self._close)
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.connection_target.set('project64')
        self.app.jp_backend='project64'
        self.app.game_pid=1234
        self.app.jp_rdram=FakeRam({
            (JAPAN_DEBUG_ENGINE_MODE,1):b'\x0d',
            (JAPAN_DEBUG_SCENE,2):bytes.fromhex('0161'),
            (JAPAN_DEBUG_CHARACTER,4):bytes(4),
            (JAPAN_DEBUG_LOADING,4):bytes(4),
        })

    def _close(self):
        try:
            for job in self.root.tk.call('after','info'):
                self.root.after_cancel(job)
            self.root.destroy()
        except tk.TclError:
            pass

    def test_save_named_slot_then_load_uses_native_emulator_input(self):
        app=self.app
        self.assertEqual(app.named_native_frame.winfo_manager(),'pack')
        app.named_native_name.set('Oedo checkpoint')
        app.savestate_slot.set('3')
        with patch('practice.toolkit.verified_emulator_pid',
                   return_value=(1234,'project64')), \
             patch('practice.toolkit.send_state_command') as command, \
             patch('practice.toolkit.save_named_checkpoints') as save:
            app.save_named_native_checkpoint()
            command.assert_called_once_with(1234,'project64','save',3)
            save.assert_called_once()
        self.assertEqual(len(app.named_native_checkpoints),1)
        record=app.named_native_checkpoints[0]
        self.assertEqual((record['name'],record['slot'],record['scene']),
                         ('Oedo checkpoint',3,0x161))
        self.assertEqual(app.named_native_selector.current(),0)
        self.assertIn('Confirm the actual save',app.status.get())
        with patch('practice.toolkit.verified_emulator_pid',
                   return_value=(1234,'project64')), \
             patch('practice.toolkit.send_state_command') as command:
            app.load_named_native_checkpoint()
            command.assert_called_once_with(1234,'project64','load',3)
        self.assertIn('Requested native project64 load',app.status.get())
        self.assertIsNone(app.jp_rdram)

    def test_named_load_requires_current_matching_japanese_attachment(self):
        app=self.app
        app.named_native_checkpoints=[{
            'name':'Oedo','region':'japan','backend':'project64',
            'slot':2,'scene':None,'character':None,'xyz':None,
            'requested_utc':'2026-11-15T00:00:00+00:00',
        }]
        app.refresh_named_native_checkpoints()
        app.jp_rdram=None
        with patch('practice.toolkit.send_state_command') as command:
            app.load_named_native_checkpoint()
        command.assert_not_called()
        self.assertIn('Connect to the matching Japan-0 emulator',app.status.get())

    def test_usa_switch_preserves_named_slot_layout_but_disables_actions(self):
        app=self.app
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertEqual(app.named_native_frame.winfo_manager(),'pack')
        self.assertIn('disabled', app.named_native_save_btn.state())
        self.assertIn('disabled', app.named_native_load_btn.state())
        self.assertTrue(app.native_save_btn.winfo_exists())
        self.assertTrue(app.native_load_btn.winfo_exists())


if __name__=='__main__':
    unittest.main()
