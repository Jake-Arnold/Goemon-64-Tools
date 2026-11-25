"""Startup access policy and read-only game action regressions."""
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.backends.memory import WindowsProcess
from practice.toolkit import Toolkit, parse_args, PRACTICE_OPTIONS
from practice.unlocks import UNLOCKS
from tests.test_checkpoint import TestCheckpoint


class TestAccessArguments(unittest.TestCase):
    def test_normal_launch_enables_existing_tools(self):
        args=parse_args([])
        self.assertTrue(all(getattr(args,key) for key in PRACTICE_OPTIONS))
        self.assertFalse(args.enable_scene_warp)
        self.assertFalse(args.read_only)

    def test_read_only_wins_in_both_argument_orders(self):
        legacy=['--'+key.replace('_','-') for key in (*PRACTICE_OPTIONS,'enable_scene_warp')]
        for argv in (['--read-only',*legacy],[*legacy,'--read-only']):
            args=parse_args(argv)
            self.assertFalse(any(getattr(args,key) for key in (*PRACTICE_OPTIONS,'enable_scene_warp')))

    def test_read_only_process_rejects_write_before_native_call(self):
        process=WindowsProcess.__new__(WindowsProcess)
        process.writable=False
        with self.assertRaises(PermissionError):
            process.write(123,b'\x01')


class TestAccessGUI(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()

    def tearDown(self):
        if hasattr(self,'root'):
            for callback in self.root.tk.call('after','info'):
                self.root.after_cancel(callback)
            self.root.destroy()

    def test_default_controls_enabled_without_startup_writes(self):
        with patch.object(WindowsProcess,'__init__',side_effect=AssertionError('Startup must not open a process')):
            app=Toolkit(self.root,parse_args([]))
        self.assertFalse(hasattr(app,'hex_advanced'))
        self.assertFalse(hasattr(app,'unsafe_check'))
        for button in (app.raw_write_btn,app.experimental_warp_btn,
                       app.native_debug_btn):
            self.assertNotIn('disabled',button.state())
        self.assertTrue(app.args.enable_state_restore)
        self.assertIsNone(app.mem)

    def test_read_only_disables_controls_and_blocks_action_handlers(self):
        args=parse_args(['--read-only'])
        # Even programmatic construction with conflicting opt-ins is normalized.
        args.enable_hex_edit=True
        app=Toolkit(self.root,args)
        self.assertFalse(hasattr(app,'hex_advanced'))
        self.assertFalse(hasattr(app,'unsafe_check'))
        for button in (app.raw_write_btn,app.experimental_warp_btn,
                       app.native_debug_btn):
            self.assertIn('disabled',button.state())
        self.assertFalse(app.args.enable_state_restore)
        for _label,controls in app.unlock_row_widgets.values():
            for button in controls.values():self.assertIn('disabled',button.state())
        process,app.mem=TestCheckpoint().sample()
        app.current=app.mem.snapshot()
        with (patch.object(process,'write',side_effect=AssertionError('No game writes')),
              patch('practice.toolkit.press_native_c_down',side_effect=AssertionError('No game input')),
              patch('practice.ui_extension.press_native_debug_accept',side_effect=AssertionError('No game input'))):
            app.write_raw_hex()
            app.set_unlock(UNLOCKS[0],1)
            app.restore_full_checkpoint()
            app.try_reload_warp()
            app._request_native_character_swap({},0)
            app.pending_native_warp={'deadline':100}
            app.poll_native_warp_menu(1)
            self.assertIsNone(app.pending_native_warp)
