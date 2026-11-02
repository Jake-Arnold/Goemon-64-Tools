import tempfile
import threading
import time
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from practice.toolkit import Toolkit,parse_args
from practice.event_sessions import EVENT_START,EVENT_SIZE,rank_bits
from tests import test_checkpoint


class EventSessionUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()
        self.app=Toolkit(self.root,parse_args(['--read-only']))
        self.process,self.app.mem=test_checkpoint.TestCheckpoint().sample()
        self.app.mem.write_guest(EVENT_START,bytes(EVENT_SIZE))
        self.app._event_connection=lambda: ((123,456),'project64')
        self.folder=tempfile.TemporaryDirectory()
        self.storage=patch('practice.event_sessions_ui.diagnostics_dir',return_value=Path(self.folder.name))
        self.storage.start()

    def tearDown(self):
        if hasattr(self,'root'):
            for callback in self.root.tk.call('after','info'):self.root.after_cancel(callback)
            self.root.destroy();self.storage.stop();self.folder.cleanup()

    def wait_rank(self):
        deadline=time.monotonic()+4
        while 'Analysing' in self.app.event_trial_summary.get() and time.monotonic()<deadline:
            self.root.update();time.sleep(.01)
        self.assertNotIn('Analysing',self.app.event_trial_summary.get())

    def test_save_reopen_rank_and_no_game_writes(self):
        app=self.app;app.new_event_session();app.capture_event_stage('A')
        app.mem.write_guest(EVENT_START,b'\x20')
        with patch.object(self.process,'write',side_effect=AssertionError('No writes')):
            app.capture_event_stage('B');app.record_event_trial();self.wait_rank()
        self.assertEqual(len(app.event_session['trials']),1)
        self.assertEqual(app.event_rows[0]['mask'],'20')
        app.event_table.selection_set('0');app.show_event_evidence()
        self.assertIn(app.event_session['trials'][0]['id'],app.event_evidence.get('1.0','end'))
        path=next(Path(self.folder.name).glob('*.json'))
        with patch('practice.event_sessions_ui.filedialog.askopenfilename',return_value=str(path)):
            app.open_event_session();self.wait_rank()
        self.assertEqual(len(app.event_session['trials']),1);self.assertEqual(app.event_pending,{})

    def test_disconnect_capture_failure_and_failed_save_leave_no_phantom_trial(self):
        app=self.app;app.new_event_session();app.capture_event_stage('A')
        app._event_connection=lambda: ((999,456),'project64')
        app.capture_event_stage('B')
        self.assertEqual(app.event_pending,{})
        self.assertIn('discarded',app.event_status.get())
        app.capture_event_stage('A');app.capture_event_stage('B')
        with patch('practice.event_sessions_ui.save_session',side_effect=OSError('disk full')):
            app.record_event_trial()
        self.assertEqual(app.event_session['trials'],[])
        self.assertIn('not recorded',app.event_status.get())
        app.discard_event_captures();self.assertEqual(app.event_pending,{})

    def test_slow_analysis_does_not_block_tk_and_stale_result_is_ignored(self):
        app=self.app;entered=threading.Event();release=threading.Event()
        def slow(session):
            entered.set();release.wait(3);return rank_bits(session)
        with patch('practice.event_sessions_ui.rank_bits',side_effect=slow):
            started=time.monotonic();app.new_event_session()
            self.assertLess(time.monotonic()-started,.3)
            self.assertTrue(entered.wait(1))
            heartbeat=[];self.root.after(0,lambda:heartbeat.append(True));self.root.update()
            self.assertTrue(heartbeat)
            app.event_generation+=1
            release.set();self.root.update()
        self.assertEqual(app.event_rows,[])
