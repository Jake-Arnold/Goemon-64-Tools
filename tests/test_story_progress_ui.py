import tkinter as tk
import unittest
from unittest.mock import patch
from practice.toolkit import Toolkit,parse_args
from practice.story_progress import FLAGS,EXTERNAL_FLAGS,SAVED_BASE
from tests.test_unlocks import FakeRAM


class StoryProgressUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw();self.app=Toolkit(self.root,parse_args(['--read-only','--game-version','usa']))
        self.assertEqual(self.app.active_version.key, 'usa')

    def tearDown(self):
        if hasattr(self,'root'):self.root.destroy()

    def test_live_stage_advisory_and_no_write_in_read_only_mode(self):
        app=self.app;ram=FakeRAM();app.mem=ram
        ram.bytes[0x8015C60D]=0x7F;ram.bytes[0x8015C60E]=2
        with patch.object(ram,'write_guest',side_effect=AssertionError('No writes')):
            app.refresh_unlocks(force=True)
        self.assertEqual(app.notebook.tab(app.story_progress_tab,'text'),'Story progress')
        self.assertEqual(len(app.story_table.get_children()),len(FLAGS)+6)
        self.assertIn('Training passed',app.ushiwaka_story.get())
        self.assertIn('reward branch may be skipped',app.story_notes.get())
        self.assertEqual(app.story_table.item('training_passed','values')[2],'0x40')
        self.assertEqual(app.story_table.item('mini','values')[3],'Absent')
        app.story_table.selection_set('training_passed')
        ram.bytes[0x8015C60D]=0x38;app.refresh_unlocks(force=True)
        self.assertEqual(app.story_table.selection(),('training_passed',))
        self.assertFalse(hasattr(app, 'ushiwaka_status'))
        self.assertIn('Five yellow',app.ushiwaka_story.get())
        self.assertIn('disabled',app.raw_write_btn.state())

    def test_disconnected_tick_without_legacy_ushiwaka_widget(self):
        # Regression: an old Unlocks label was removed, but the periodic
        # disconnected refresh path still attempted to update it.
        app = self.app
        self.assertFalse(hasattr(app, 'ushiwaka_status'))
        app.mem = None
        with patch.object(self.root, 'after', return_value=None):
            app.tick()
        self.assertIn('Unavailable', app.ushiwaka_story.get())

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

    def test_source_filter_refreshes_hidden_rows_and_restores_full_list(self):
        app=self.app;app.mem=FakeRAM();app.refresh_unlocks(force=True)
        app.story_filter.set('external')
        visible=app.story_table.get_children()
        self.assertEqual(set(visible),{f.key for f in EXTERNAL_FLAGS})
        self.assertEqual(len(visible),37)
        self.assertTrue(app.story_table.exists('ushi_intro'))  # Detached, not destroyed.
        app.mem.bytes[0x8015C60A]=0x10
        app.refresh_unlocks(force=True)
        self.assertEqual(app.story_table.item('external_koryuta_freed','values')[3],'Set')
        self.assertEqual(set(app.story_table.get_children()),set(visible))
        app.story_filter.set('0x8015C614')
        self.assertEqual(len(app.story_table.get_children()),sum(f.address==0x8015C614 for f in FLAGS))
        app.story_filter.set('')
        self.assertEqual(len(app.story_table.get_children()),len(FLAGS)+6)

    def test_fortune_doll_tab_groups_pickups_and_counters(self):
        app=self.app;app.mem=FakeRAM();app.refresh_story_progress()
        sections={app.story_sections.tab(i,'text') for i in app.story_sections.tabs()}
        self.assertIn('Fortune Dolls',sections)
        self.assertIn('Benkei & Kihachi',sections)
        self.assertIn('Keys & Locks',sections)
        dolls=app.story_tables['Fortune Dolls']
        for key in ('silver_doll_356','placed_gold_doll_0f2',
                    'fortune_doll_quarters','fortune_doll_total'):
            self.assertTrue(dolls.exists(key),key)
        self.assertFalse(dolls.exists('training_passed'))
        tab=next(i for i in app.story_sections.tabs()
                 if app.story_sections.tab(i,'text')=='Fortune Dolls')
        app.story_sections.select(tab)
        app.story_filter.set('silver')
        self.assertTrue(dolls.get_children())
        self.assertNotIn('fortune_doll_total',dolls.get_children())
        app.story_filter.set('')
        self.assertIn('fortune_doll_total',dolls.get_children())

    def test_story_dropdown_applies_selected_flag_and_keeps_other_bits(self):
        app=self.app; app.args.read_only=False; app.args.enable_hex_edit=True
        app.mem=FakeRAM(); app.mem.bytes[0x8015C60D]=0x85; app.refresh_story_progress()
        app.story_table.selection_set('ushi_intro'); app.select_story_edit()
        self.assertEqual(app.story_edit_choice.get(),'Clear')
        self.assertEqual(tuple(app.story_edit_combo['values']),('Clear','Set'))
        app.story_edit_choice.set('Set'); app.apply_story_edit()
        self.assertEqual(app.mem.bytes[0x8015C60D],0xA5)
        self.assertIn('verified',app.story_edit_status.get())
        app.story_table.selection_set('mini'); app.select_story_edit()
        self.assertEqual(tuple(app.story_edit_combo['values']),('Absent','Present'))
        app.story_edit_choice.set('Present'); app.apply_story_edit()
        self.assertEqual(app.mem.read_guest(0x8015C6F0,4),b'\x00\x00\x00\x01')
        app.story_table.selection_set('bank_a'); app.select_story_edit()
        self.assertIn('disabled',app.story_edit_button.state())

    def test_story_dropdown_refuses_read_only_and_stale_values(self):
        app=self.app; app.mem=FakeRAM(); app.refresh_story_progress()
        app.story_table.selection_set('ushi_intro'); app.select_story_edit()
        self.assertIn('disabled',app.story_edit_button.state())
        app.story_edit_choice.set('Set'); app.apply_story_edit()
        self.assertEqual(app.mem.writes,[])
        app.args.read_only=False; app.args.enable_hex_edit=True; app.select_story_edit()
        app.story_edit_choice.set('Set'); app.mem.bytes[0x8015C60D]=0x80
        app.apply_story_edit(); self.assertEqual(app.mem.writes,[])
        self.assertIn('changed',app.story_edit_status.get())
