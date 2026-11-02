"""Tk smoke tests for deliberately separated experimental buttons."""
import unittest
import tkinter as tk
from argparse import Namespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.checkpoints import STATE_ADDR
from practice.scene_controls import PENDING_MAP_ADDR
from tests.test_checkpoint import TestCheckpoint

class TestExperimentalGUI(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()
        self.app=Toolkit(self.root,Namespace(pid=None,base=None,endian='auto',route=None,
            enable_teleport=True,enable_state_restore=True,enable_debug_menu=True,
            enable_hex_edit=True,enable_scene_warp=False))
        _,self.ram=TestCheckpoint().sample()
        self.app.mem=self.ram
        self.ram.write_guest(PENDING_MAP_ADDR,(35).to_bytes(2,'big'))

    def tearDown(self):
        if hasattr(self,'root'):self.root.destroy()

    def test_f1_opens_memory_and_retires_ineffective_motion_controls(self):
        self.assertFalse(hasattr(self.app,'try_motion_pulse'))
        self.app.notebook.select(self.app.scene_tab)
        self.assertEqual(self.app._on_f1_open_memory(),'break')
        self.assertEqual(self.app.notebook.select(),str(self.app.live_memory_tab))
        self.assertTrue(self.root.bind_all('<F1>'))

    def test_warp_only_explicit_button_and_confirmation(self):
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        self.app.request_direct_scene(353,'Test destination')
        self.assertEqual(self.ram.u8(STATE_ADDR),13)
        self.app.hex_advanced.set(True)
        with patch('practice.ui_extension.messagebox.askyesno',return_value=False):
            self.app.try_reload_warp()
        self.assertEqual(self.ram.u8(STATE_ADDR),13)
        with patch('practice.ui_extension.messagebox.askyesno',return_value=True):
            self.app.try_reload_warp()
        self.assertEqual(self.ram.u8(STATE_ADDR),12)
        self.assertEqual(self.ram.u16(PENDING_MAP_ADDR),353)
        self.assertIsNotNone(self.app.pending_direct_warp)

if __name__=='__main__':unittest.main()
