"""Cross-area restore and nonblocking connect regression tests (synthetic RAM)."""
from __future__ import annotations
from argparse import Namespace
import threading
import time
import tkinter as tk
import unittest
from unittest.mock import patch
from practice.checkpoints import MAP_ADDR, LIVE_ADDR, STATE_ADDR, capture_checkpoint
from practice.toolkit import Toolkit
from tests.test_checkpoint import TestCheckpoint
from tests.test_tools import BASE, write_u8, write_u32


class CrossAreaRestoreTests(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk()
        self.root.withdraw()
        self.app=Toolkit(self.root,Namespace(pid=None,base=None,endian='auto',
            route=None,enable_teleport=True,enable_state_restore=True,
            enable_debug_menu=True,enable_scene_warp=False,enable_hex_edit=True))
        self.process,self.ram=TestCheckpoint().sample()
        self.app.mem=self.ram
        self.app.current=self.ram.snapshot()
        self.checkpoint=capture_checkpoint(self.ram,'Map 35')
        self.app.checkpoints=[self.checkpoint]
        self.app.checkpoints_box['values']=self.app.checkpoint_labels()
        self.app.checkpoints_box.current(0)
        write_u8(self.process,0x801B0000+0xCC,0)

    def tearDown(self):
        for callback_id in self.root.tk.call('after','info'):
            try:self.root.after_cancel(callback_id)
            except tk.TclError:pass
        self.root.destroy()

    def _begin(self):
        self.ram.write_guest(MAP_ADDR,(36).to_bytes(2,'big'))
        self.ram.write_f32(0x801A0008,987.0)
        with patch('tkinter.messagebox.askyesno',return_value=True):
            self.app.restore_full_checkpoint()
        self.assertEqual(self.ram.u8(STATE_ADDR),12)
        self.assertEqual(self.ram.read_guest(0x800C7CA0,2),b'\x00\x23')
        self.assertEqual(self.app.pending_restore['phase'],'warp')

    def test_warp_waits_for_correct_map_then_restores_saved_xyz(self):
        self._begin()
        self.ram.write_guest(LIVE_ADDR+16,(777).to_bytes(4,'big'))
        self.app.poll_pending_restore(None,self.app.pending_restore['started']+.2)
        self.assertAlmostEqual(self.ram.snapshot()['x'],987.)
        self.assertEqual(self.ram.u32(LIVE_ADDR+16),777)
        self.ram.write_guest(MAP_ADDR,(35).to_bytes(2,'big'))
        write_u8(self.process,STATE_ADDR,13)
        t=self.app.pending_restore['started']+1
        for i in range(4):self.app.poll_pending_restore(None,t+i*.2)
        self.assertIsNone(self.app.pending_restore)
        self.assertAlmostEqual(self.ram.snapshot()['x'],125.25)
        self.assertEqual(self.ram.u32(LIVE_ADDR+16),100)

    def test_no_restore_during_script_or_cutscene(self):
        self._begin()
        self.ram.write_guest(MAP_ADDR,(35).to_bytes(2,'big'))
        write_u8(self.process,STATE_ADDR,13)
        write_u8(self.process,0x800C7AE9,1)
        t=self.app.pending_restore['started']+1
        for i in range(4):self.app.poll_pending_restore(None,t+i*.2)
        self.assertIsNotNone(self.app.pending_restore)
        self.assertAlmostEqual(self.ram.snapshot()['x'],987.)

    def test_timeout_is_terminal(self):
        self._begin()
        self.app.poll_pending_restore(None,self.app.pending_restore['started']+31)
        self.assertIsNone(self.app.pending_restore)
        self.assertAlmostEqual(self.ram.snapshot()['x'],987.)

    def test_same_map_restore_is_immediate(self):
        self.ram.write_f32(0x801A0008,111.)
        with patch('tkinter.messagebox.askyesno',return_value=True):
            self.app.restore_full_checkpoint()
        self.assertIsNone(self.app.pending_restore)
        self.assertAlmostEqual(self.ram.snapshot()['x'],125.25)

    def test_connect_scan_does_not_block_tk(self):
        started=threading.Event()
        release=threading.Event()
        proc=TestCheckpoint().sample()[0]
        proc.close=lambda:None
        self.app.mem=None
        def slow_scan(_process,_endian):
            started.set()
            self.assertTrue(release.wait(2))
            return BASE,'wordswapped'
        with (patch('practice.toolkit.find_pid',return_value=1234),
              patch('practice.toolkit.WindowsProcess',return_value=proc),
              patch('practice.toolkit.discover_rdram',side_effect=slow_scan)):
            before=time.monotonic()
            self.app.connect()
            self.assertLess(time.monotonic()-before,.2)
            self.assertTrue(started.wait(2))
            self.root.update()
            release.set()
            deadline=time.monotonic()+3
            while self.app._connecting and time.monotonic()<deadline:
                self.root.update()
                time.sleep(.01)
            self.assertFalse(self.app._connecting)
            self.assertEqual(self.app.game_pid,1234)

    def test_connect_without_player_and_clear_stale_position(self):
        proc=TestCheckpoint().sample()[0];proc.close=lambda:None
        write_u32(proc,0x801FC60C,0);write_u32(proc,0x801FC604,0);write_u8(proc,STATE_ADDR,6)
        with (patch('practice.toolkit.find_pid',return_value=1234),
              patch('practice.toolkit.WindowsProcess',return_value=proc),
              patch('practice.toolkit.discover_rdram',return_value=(BASE,'wordswapped'))):
            self.app._connect_worker((None,None,'auto',False,'recomp'))
        result=self.app._connect_queue.get_nowait()
        self.assertEqual(result[0],'ok');self.assertIsNone(result[4]['x'])
        self.app._connecting=True;self.app._connect_queue.put(result);self.app._poll_connect_results()
        self.assertIn('player unavailable',self.app.status.get())
        self.app.pos_text.set('stale');self.app.tick()
        self.assertIn('—',self.app.pos_text.get());self.assertIsNone(self.app.current)
        self.assertIsNotNone(self.app.mem)

    def test_project64_target_passed_to_worker(self):
        proc=TestCheckpoint().sample()[0]
        proc.close=lambda:None
        with (patch('practice.toolkit.find_pid',return_value=1234) as select,
              patch('practice.toolkit.WindowsProcess',return_value=proc) as opened,
              patch('practice.toolkit.discover_rdram',return_value=(BASE,'wordswapped'))):
            self.app._connect_worker((None,None,'auto',False,'project64'))
        select.assert_called_once_with('project64')
        opened.assert_called_once_with(1234,writable=False)
        result=self.app._connect_queue.get_nowait()
        self.assertEqual(result[0],'ok')


if __name__=='__main__':
    unittest.main()
