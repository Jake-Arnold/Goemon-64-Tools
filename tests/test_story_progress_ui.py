import tkinter as tk
import unittest
from unittest.mock import patch
from practice.toolkit import Toolkit,parse_args
from practice.story_progress import FLAGS,SAVED_BASE
from tests.test_unlocks import FakeRAM


class StoryProgressUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw();self.app=Toolkit(self.root,parse_args(['--read-only']))

    def tearDown(self):
        if hasattr(self,'root'):self.root.destroy()

    def test_live_stage_advisory_and_no_write_in_read_only_mode(self):
        app=self.app;ram=FakeRAM();app.mem=ram
        ram.bytes[0x8015C60D]=0x7F;ram.bytes[0x8015C60E]=2
        with patch.object(ram,'write_guest',side_effect=AssertionError('No writes')):
            app.refresh_unlocks(force=True)
        self.assertEqual(app.notebook.tab(app.story_progress_tab,'text'),'Story progress')
        self.assertEqual(len(app.story_table.get_children()),len(FLAGS)+4)
        self.assertIn('Training passed',app.ushiwaka_story.get())
        self.assertIn('reward branch may be skipped',app.story_notes.get())
        self.assertEqual(app.story_table.item('training_passed','values')[2],'0x40')
        self.assertEqual(app.story_table.item('mini','values')[3],'Absent')
        app.story_table.selection_set('training_passed')
        ram.bytes[0x8015C60D]=0x38;app.refresh_unlocks(force=True)
        self.assertEqual(app.story_table.selection(),('training_passed',))
        self.assertIn('Five yellow',app.ushiwaka_status.get())
        self.assertIn('disabled',app.raw_write_btn.state())

    def test_disconnect_clears_previous_story_values(self):
        app=self.app;app.mem=FakeRAM();app.mem.bytes[0x8015C60C]=0x28
        app.refresh_unlocks(force=True);self.assertIn('referral',app.benkei_story.get())
        app.mem=None;app.refresh_unlocks(force=True)
        self.assertIn('Unavailable',app.benkei_story.get())
        self.assertIn('Disconnected',app.story_notes.get())
        self.assertEqual(app.story_table.item('kihachi_referral','values')[3],'Unavailable')
        self.assertEqual(app.story_table.item('kihachi_referral','values')[4],'—')

    def test_read_error_is_displayed_and_other_rows_remain_available(self):
        app=self.app;ram=FakeRAM();app.mem=ram;read=ram.read_guest
        def failed(addr,size):
            if addr==SAVED_BASE:raise OSError('Unavailable')
            return read(addr,size)
        with patch.object(ram,'read_guest',side_effect=failed):app.refresh_unlocks(force=True)
        self.assertIn('saved',app.story_notes.get())
        self.assertEqual(app.story_table.item('ushi_intro','values')[3],'Unavailable')
        self.assertEqual(app.story_table.item('mini','values')[3],'Absent')
