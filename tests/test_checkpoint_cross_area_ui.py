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
from tests.test_checkpoint import BASE, write_u8, write_u32


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
        self.app.logical_checkpoint_selection = 0
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

    def test_capture_uses_plain_state_and_persists_checkpoint(self):
        app = self.app
        with patch('practice.toolkit.save_checkpoint_file') as save:
            app.capture_full_checkpoint('Plain state capture')
        self.assertEqual(app.logical_checkpoint_selection, 1)
        self.assertEqual(app.checkpoints[1]['payload']['name'], 'Plain state capture')
        save.assert_called_once()
        self.assertEqual(save.call_args.args[1], app.checkpoints)
        self.assertIn('Captured logical checkpoint', app.status.get())
        self.assertFalse(hasattr(app, 'checkpoints_box'))

    def test_combined_selector_legacy_restores_only_xyz(self):
        app=self.app
        app.legacy_bookmarks=[dict(name='Old position',x=222.5,y=12.5,z=-77.5,
                                   character=self.ram.snapshot()['character'],map_id=35)]
        app.logical_checkpoint_selection = 1
        original_progress=self.ram.read_guest(0x8015C608,0x304)
        original_hp=self.ram.u32(LIVE_ADDR+12)
        original_rotation=self.ram.read_guest(0x801A0014,6)
        with patch('tkinter.messagebox.askyesno',return_value=True) as confirm:
            app.restore_full_checkpoint()
        confirm.assert_called_once()
        self.assertAlmostEqual(self.ram.snapshot()['x'],222.5)
        self.assertEqual(self.ram.read_guest(0x8015C608,0x304),original_progress)
        self.assertEqual(self.ram.u32(LIVE_ADDR+12),original_hp)
        self.assertEqual(self.ram.read_guest(0x801A0014,6),original_rotation)
        self.assertIn('XYZ only',app.status.get())

    def test_legacy_with_no_map_does_not_write(self):
        app=self.app
        app.legacy_bookmarks=[dict(name='Old legacy',x=5,y=6,z=7,character=0)]
        app.logical_checkpoint_selection = 1
        original=self.ram.read_guest(0x801A0008,12)
        with patch('tkinter.messagebox.showerror') as err, \
             patch('tkinter.messagebox.askyesno') as ask:
            app.restore_full_checkpoint()
        err.assert_called_once();ask.assert_not_called()
        self.assertEqual(self.ram.read_guest(0x801A0008,12),original)

    def test_legacy_rejects_cross_map_and_read_only(self):
        app=self.app
        app.legacy_bookmarks=[dict(name='Elsewhere',x=5,y=6,z=7,character=0,map_id=45)]
        app.logical_checkpoint_selection = 1
        with patch('tkinter.messagebox.showerror') as err:
            app.restore_full_checkpoint()
        err.assert_called_once()
        app.args.read_only=True
        app.args.enable_teleport=False
        with patch('tkinter.messagebox.askyesno') as ask:
            app.restore_full_checkpoint()
        ask.assert_not_called()

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
              patch('practice.toolkit.HostProcess',return_value=proc),
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
              patch('practice.toolkit.HostProcess',return_value=proc),
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
              patch('practice.toolkit.HostProcess',return_value=proc) as opened,
              patch('practice.toolkit.discover_rdram',return_value=(BASE,'wordswapped'))):
            self.app._connect_worker((None,None,'auto',False,'project64'))
        select.assert_called_once_with('project64')
        opened.assert_called_once_with(1234,writable=False)
        result=self.app._connect_queue.get_nowait()
        self.assertEqual(result[0],'ok')


if __name__=='__main__':
    unittest.main()
