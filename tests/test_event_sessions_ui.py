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

    def test_flag_report_contains_full_trials_and_ranked_bits(self):
        import json
        app = self.app
        app.new_event_session()
        app.capture_event_stage('A')
        app.mem.write_guest(EVENT_START, b'\x20')
        app.capture_event_stage('B')
        app.record_event_trial()
        self.wait_rank()
        with patch('practice.reports.reports_root',
                   return_value=Path(self.folder.name) / 'reports'):
            app.save_event_investigation_report()
        found = list((Path(self.folder.name) / 'reports').glob(
            'USA/*/*/manifest.json'))
        self.assertEqual(len(found), 1)
        session = json.loads((found[0].parent / 'session.json').read_text())
        self.assertEqual(session['manifest']['kind'], 'flag-investigation')
        self.assertEqual(len(session['evidence']['working_investigation']['trials']), 1)
        self.assertEqual(session['evidence']['working_investigation']
                         ['trials'][0]['captures']['B']['bytes_hex'][:2], '20')
        self.assertTrue(session['candidates'])
        self.assertIn('Saved', app.event_status.get())

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

    def test_event_sessions_consolidates_advanced_memory_and_removes_shadow(self):
        app=self.app
        tabs={app.notebook.tab(tab,'text') for tab in app.notebook.tabs()}
        self.assertIn('Memory discovery',tabs)
        nested_discovery = {
            app.discovery_tabs.tab(t, 'text')
            for t in app.discovery_tabs.tabs()
        }
        self.assertEqual(nested_discovery, {
            'Start here', 'Find a value', 'Compare memory changes',
            'Investigate flags', 'Record damage'
        })
        self.assertNotIn('Saved / shadow',tabs)
        self.assertNotIn('State discovery',tabs)
        self.assertIs(app.event_sections, app.discovery_tabs)
        self.assertEqual(
            app.event_sections.tab(app.state_discovery_tab,'text'),
            'Compare memory changes')
        self.assertFalse(hasattr(app,'save_buffers_tree'))
        self.assertFalse(hasattr(app,'save_buffers_tab'))
        app.refresh_checkpoint_options();app.refresh_checkpoint_diff(force=True)
        app.refresh_native_watch(time.monotonic())

    def test_monitor_advances_without_removed_shadow_panel(self):
        app=self.app
        with patch.object(self.process,'write',side_effect=AssertionError('No writes')):
            app.poll_event_monitor()
            self.assertIn('Game-loop counter:',app.event_live.get())
            with patch.object(app.mem,'read_guest',side_effect=OSError('lost connection')):
                app.poll_event_monitor()
            self.assertIn('Read unavailable',app.event_live.get())
            app.mem=None
            with patch('practice.event_sessions_ui.time.monotonic',return_value=app.event_monitor_started+12.5):
                app.poll_event_monitor()
            self.assertIn('12.5s',app.event_live.get())
            self.assertIn('Disconnected',app.event_live.get())

    def test_raw_pending_comparison_including_control_and_zero_changes(self):
        app=self.app;app.new_event_session();app.capture_event_stage('A');app.capture_event_stage('B')
        self.assertIn('0 changed bytes',app.event_comparison.get())
        app.event_role.set('control')
        app.mem.write_guest(EVENT_START,b'\x20')
        app.capture_event_stage('B')
        self.assertIn('1 changed bytes, 1 changed bits',app.event_comparison.get())
        self.assertIn('0x8015C608: 00->20',app.event_comparison.get())
        app.record_event_trial();self.wait_rank()
        self.assertEqual(app.event_rows,[])
        self.assertIn('Capture A',app.event_comparison.get())

    def test_cross_room_capture_record_and_evidence_preserve_context(self):
        from practice.checkpoints import MAP_ADDR
        app=self.app;app.new_event_session();app.capture_event_stage('A')
        original=app.mem.snapshot
        app.mem.write_guest(MAP_ADDR,(99).to_bytes(2,'big'))
        app.mem.write_guest(EVENT_START,b'\x10')
        state=original();state.update(character=1,player_ptr=0x801B0000,task_ptr=0x801B0100)
        with patch.object(app.mem,'snapshot',return_value=state),patch.object(self.process,'write',side_effect=AssertionError('No writes')):
            app.capture_event_stage('B');app.record_event_trial();self.wait_rank()
        self.assertEqual(len(app.event_session['trials']),1)
        self.assertIn('Context-changing trials: 1',app.event_trial_summary.get())
        app.event_table.selection_set('0');app.show_event_evidence()
        text=app.event_evidence.get('1.0','end')
        self.assertIn('B: map 99, character 1',text)
        self.assertIn('player 0x801B0000',text)
        self.assertIn('task 0x801B0100',text)
