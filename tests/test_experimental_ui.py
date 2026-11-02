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

    def test_reload_selected_character_native_swap_after_load(self):
        from practice.checkpoints import MAP_ADDR
        from autosplitter.memory import CHARACTER_ID_ADDR
        self.app.scene_character.current(2)
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        self.app.hex_advanced.set(True)
        with patch('practice.ui_extension.messagebox.askyesno',return_value=True):
            self.app.try_reload_warp()
        pending=self.app.pending_direct_warp
        self.assertEqual(pending['selected_character'],2)
        self.assertEqual(self.ram.u32(CHARACTER_ID_ADDR),0)
        self.ram.write_guest(MAP_ADDR,(353).to_bytes(2,'big'))
        self.ram.write_guest(STATE_ADDR,b'\x0d')
        self.ram.write_guest(self.ram.snapshot()['task_ptr']+0xCC,b'\x00')
        for dt in (1,1.2,1.4):
            self.app.poll_direct_warp(pending['start_at']+dt)
        self.assertEqual(pending['phase'],'character_switch')
        with patch('practice.ui_extension.press_native_c_down',return_value=lambda:None) as press:
            self.app.poll_direct_warp(pending['switch_started']+2.2)
            press.assert_called_once()
        self.assertEqual(self.ram.u32(CHARACTER_ID_ADDR),0)
        self.assertEqual(pending['attempts'],1)
        self.app._release_debug_key()
        self.ram.write_guest(CHARACTER_ID_ADDR,(2).to_bytes(4,'big'))
        self.ram.write_guest(self.ram.snapshot()['task_ptr']+0x60,b'\x02')
        for dt in (3,3.2,3.4):
            self.app.poll_direct_warp(pending['switch_started']+dt)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('selected character 2',self.app.scene_status.get())

    def test_locked_scene_character_never_writes_active_id(self):
        from practice.checkpoints import MAP_ADDR, GAMEDATA_ADDR
        from autosplitter.memory import CHARACTER_ID_ADDR
        self.app.scene_character.current(3)
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        self.app.hex_advanced.set(True)
        with patch('practice.ui_extension.messagebox.askyesno',return_value=True):
            self.app.try_reload_warp()
        pending=self.app.pending_direct_warp
        self.ram.write_guest(MAP_ADDR,(353).to_bytes(2,'big'))
        self.ram.write_guest(STATE_ADDR,b'\x0d')
        self.ram.write_guest(self.ram.snapshot()['task_ptr']+0xCC,b'\x00')
        self.ram.write_guest(GAMEDATA_ADDR+0x94+4*3,b'\x00'*4)
        for dt in (1,1.2,1.4):
            self.app.poll_direct_warp(pending['start_at']+dt)
        with patch('practice.ui_extension.press_native_c_down',side_effect=AssertionError('must not press')):
            self.app.poll_direct_warp(pending['switch_started']+2)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('not unlocked',self.app.scene_status.get())
        self.assertEqual(self.ram.u32(CHARACTER_ID_ADDR),0)

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
