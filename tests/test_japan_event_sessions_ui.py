"""Shared Tk Event Sessions performs Japanese A/B/C without USA pointers."""
import tempfile
import time
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
from practice.toolkit import Toolkit, parse_args
from practice.event_sessions import JAPAN_CANDIDATE_START, JAPAN_BATTERY_RESEARCH_START
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
)
from tests.test_japan_party_controller import Writer


class JapanEventSessionsUiTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root=tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'No Tk display: {exc}')
        self.root.withdraw()
        cache=patch('practice.toolkit.load_remembered_rom',return_value=None)
        cache.start()
        self.addCleanup(cache.stop)
        self.app=Toolkit(self.root,parse_args([
            '--game-version','japan','--read-only']))
        self.writer=Writer()
        self.writer.set_guest(JAPAN_DEBUG_ENGINE_MODE,b'\x0d')
        self.writer.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('0161'))
        self.writer.set_guest(JAPAN_DEBUG_CHARACTER,bytes(4))
        self.writer.set_guest(JAPAN_DEBUG_LOADING,bytes(4))
        self.writer.set_guest(JAPAN_CANDIDATE_START,bytes(100))
        self.writer.writes.clear()
        self.app.jp_rdram=self.writer.rdram()
        self.app.game_pid=5599
        self.app.jp_backend='project64'
        self.folder=tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        storage=patch('practice.event_sessions_ui.diagnostics_dir',
                      return_value=Path(self.folder.name))
        storage.start()
        self.addCleanup(storage.stop)

    def tearDown(self):
        if hasattr(self,'root'):
            for callback in self.root.tk.call('after','info'):
                self.root.after_cancel(callback)
            self.root.destroy()

    def _wait_ranking(self):
        deadline=time.monotonic()+4
        while 'Analysing' in self.app.event_trial_summary.get() and time.monotonic()<deadline:
            self.root.update()
            time.sleep(0.01)
        self.assertNotIn('Analysing',self.app.event_trial_summary.get())

    def test_japan_event_session_uses_same_tab_and_correct_guest_base(self):
        app=self.app
        self.assertEqual(
            app.event_sections.tab(app.event_sections.tabs()[0],'state'),
            'normal')
        self.assertNotIn('disabled',app.event_region_entry.state())
        self.assertIn('NOT a verified saved-event bank',
                      app.event_region_note.get())
        app.new_event_session()
        self.assertEqual(app.event_session['region'],'japan')
        self.assertEqual(app.event_session['event_start'],JAPAN_CANDIDATE_START)
        app.capture_event_stage('A')
        self.writer.set_guest(JAPAN_CANDIDATE_START,b'\x20')
        app.capture_event_stage('B')
        self.assertIn('0x80161D80: 00->20',app.event_comparison.get())
        app.record_event_trial()
        self._wait_ranking()
        self.assertEqual(len(app.event_session['trials']),1)
        self.assertEqual(app.event_rows[0]['address'],'0x80161D80')
        self.assertEqual(self.writer.writes,[])

    def test_sasuke_battery_preset_covers_unverified_bit_without_game_writes(self):
        app=self.app
        self.assertNotIn('disabled', app.event_battery_preset_button.state())
        self.writer.set_guest(JAPAN_BATTERY_RESEARCH_START, bytes(100))
        app.prepare_sasuke_battery_session()
        self.assertEqual(app.event_region_start.get(), '0x80161DC0')
        self.assertIn('battery', app.event_label.get().lower())
        self.assertIsNone(app.event_session)
        self.assertIn('UNVERIFIED', app.event_status.get())
        app.new_event_session()
        self.assertEqual(app.event_session['event_start'],
                         JAPAN_BATTERY_RESEARCH_START)
        app.capture_event_stage('A')
        self.writer.set_guest(0x80161DF9, bytes((0x20,)))
        app.capture_event_stage('B')
        self.assertIn('0x80161DF9: 00->20', app.event_comparison.get())
        self.assertEqual(self.writer.writes, [])

    def test_region_change_clears_event_session_without_cross_link(self):
        app=self.app
        app.new_event_session()
        self.assertEqual(app.event_session['region'],'japan')
        app.game_version_choice.set('Mystical Ninja USA (rev 0)')
        # Avoid guessing a display label: activate the known USA Version.
        from practice.game_versions import VERSIONS
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertIsNone(app.event_session)
        self.assertEqual(app.event_region_start.get(),'0x8015C608')
        self.assertIn('disabled',app.event_region_entry.state())
        self.assertIn('disabled',app.event_battery_preset_button.state())
        self.assertEqual(self.writer.writes,[])


if __name__=='__main__':
    unittest.main()
