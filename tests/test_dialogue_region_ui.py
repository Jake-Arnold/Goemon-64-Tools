"""Headless Tk smoke checks for cross-region Dialogue controls and file-manager button."""
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import patch

from practice.dialogue_region_ui import DialogueRegionMixin


class FakeBase:
    def build_dialogue_tab(self, notebook):
        self.dialogue_tab=ttk.Frame(notebook)
        notebook.add(self.dialogue_tab,text='Dialogue')
        self.dialogue_path=None
        self.dialogue_retail_path=None
        self.dialogue_build_running=False
        self.dialogue_staged={}
        self.dialogue_line_break_approved=set()
        self.dialogue_records=[]
        self.dialogue_by_key={}
        self.dialogue_selected_key=None
        self.dialogue_window_context=None
        self.dialogue_original_image=None
        self.dialogue_font_widths=None
        self.dialogue_status=tk.StringVar(value='Initial')
        self.dialogue_layout_summary=tk.StringVar(value='Initial layout')
        self.dialogue_query=tk.StringVar()
        self.dialogue_layout_mode=tk.StringVar(value='Native (auto when traced)')
        self.dialogue_width_limit=tk.StringVar()
        self.dialogue_line_limit=tk.StringVar()
        self.dialogue_build_queue=__import__('queue').SimpleQueue()
        original_top=ttk.Frame(self.dialogue_tab)
        original_top.pack()
        ttk.Label(self.dialogue_tab,textvariable=self.dialogue_status).pack()
        self.dialogue_editor=tk.Text(self.dialogue_tab,height=2)
        self.dialogue_editor.pack()
        self.dialogue_wrap_button=ttk.Button(self.dialogue_tab)
        self.dialogue_mode_selector=ttk.Combobox(self.dialogue_tab)
        self.dialogue_width_entry=ttk.Entry(self.dialogue_tab)
        self.dialogue_line_entry=ttk.Entry(self.dialogue_tab)
        self.dialogue_retail_build_button=ttk.Button(self.dialogue_tab)
    def _dialogue_filter(self):
        pass
    def _dialogue_mode_changed(self):
        pass
    def _dialogue_analyze(self):
        pass
    def _dialogue_select(self,event=None):
        pass


class FakeApp(DialogueRegionMixin,FakeBase):
    pass


class RegionUIIntegration(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk()
        self.root.withdraw()
        self.notebook=ttk.Notebook(self.root)
        self.notebook.pack()
        self.app=FakeApp()
        self.app.root=self.root
        self.app.notebook=self.notebook
        self.app.active_version=type('Version',(),{'key':'usa'})()
        self.app.build_dialogue_tab(self.notebook)
        self.root.update()
    def tearDown(self):
        self.root.destroy()

    def test_initial_usa_fallback_and_button(self):
        self.assertIn('drop',self.app.dialogue_drop_text.get().lower())
        self.assertEqual(self.app.dialogue_region_choice.get(),'usa')
        self.assertIn('No verified USA',self.app.dialogue_status.get())
        self.assertTrue(self.app.dialogue_tab.winfo_exists())

    def test_region_switch_reset_without_rom(self):
        self.app.dialogue_staged={'97:0x4':'test'}
        self.app.dialogue_region_choice.set('japan')
        self.app._dialogue_region_changed()
        self.assertEqual(self.app.dialogue_staged,{})
        self.assertIn('No verified JAPAN',self.app.dialogue_status.get())

    def test_japan_restores_stored_verified_tokens(self):
        jp=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not jp:self.skipTest('JP image unavailable')
        self.app.dialogue_region_choice.set('japan')
        with patch('practice.dialogue_region_ui.verify_stored',side_effect=lambda region,kind:Path(jp) if region=='japan' and kind=='decompressed' else None):
            self.app._dialogue_region_changed()
        self.assertEqual(len(self.app.dialogue_records),5039)
        self.assertIsNone(self.app.dialogue_font_widths)
        self.assertIn('Unicode',self.app.dialogue_status.get())
        self.assertIn('disabled',self.app.dialogue_wrap_button.state())
        self.assertEqual(self.app.dialogue_layout_mode.get(),'Measure only')

    def test_hypothesis_preview_stays_readonly_and_japan_only(self):
        from practice.dialogue_japan import JapanDialogueRecord
        record=JapanDialogueRecord(82,0x18,0x742358,(14,19,15,78,16),(0x64,))
        self.app.dialogue_region_choice.set('japan')
        self.app._dialogue_region_changed()
        self.app.dialogue_records=[record]
        self.app.dialogue_by_key={record.key:record}
        self.app.dialogue_selected_key=record.key
        self.app.dialogue_editor.insert('1.0',record.text)
        self.assertFalse(self.app.dialogue_kana_hypothesis_enabled.get())
        self.assertIn('108 screenshot-confirmed glyph IDs',self.app.dialogue_kana_note.get())
        self.assertIn('76/160 kana positions verified',self.app.dialogue_kana_note.get())
        self.app.dialogue_kana_hypothesis_enabled.set(True)
        self.app._dialogue_toggle_kana_hypothesis()
        self.assertEqual(self.app.dialogue_kana_text.get('1.0','end-1c'),'あかいどう')
        self.assertEqual(self.app.dialogue_kana_text.cget('state'),'disabled')
        self.assertEqual(self.app.dialogue_editor.get('1.0','end-1c'),record.text)
        self.app.dialogue_region_choice.set('usa')
        self.app._dialogue_region_changed()
        self.assertFalse(self.app.dialogue_kana_panel.winfo_manager())

    def test_hypothesis_search_and_list_are_explicitly_opt_in(self):
        from practice.dialogue_japan import JapanDialogueRecord
        rec=JapanDialogueRecord(81,0,0x742000,(25,44,27,59),(0x30,))
        self.app.dialogue_region_choice.set('japan')
        self.app._dialogue_region_changed()
        self.app.dialogue_records=[rec]
        self.app.dialogue_by_key={rec.key:rec}
        self.app.dialogue_tree=ttk.Treeview(self.app.dialogue_tab,
            columns=('resource','offset','references','text'),show='headings')
        self.app.dialogue_query.set('しません')
        self.app._dialogue_filter()
        self.assertEqual(self.app.dialogue_tree.get_children(),())
        self.app.dialogue_kana_hypothesis_enabled.set(True)
        self.app._dialogue_toggle_kana_hypothesis()
        self.assertEqual(self.app.dialogue_tree.get_children(),(rec.key,))
        self.assertIn('しません',str(self.app.dialogue_tree.item(rec.key,'values')))
        self.assertIn('HYPOTHETICAL',self.app.dialogue_status.get())

    def test_open_build_directory(self):
        with patch('practice.dialogue_region_ui.open_directory') as opener, patch('practice.dialogue_region_ui.build_directory',return_value=Path('/tmp/builds')):
            self.app._dialogue_open_built_dir()
            opener.assert_called_once_with(Path('/tmp/builds'))
        self.app.dialogue_last_build_dir=Path('/tmp/custom-output')
        with patch('practice.dialogue_region_ui.open_directory') as opener:
            self.app._dialogue_open_built_dir()
            opener.assert_called_once_with(Path('/tmp/custom-output'))

if __name__=='__main__':unittest.main()

class OptionalDnDTests(unittest.TestCase):
    def test_no_tkdnd_falls_back_to_real_tk(self):
        from practice.dialogue_dnd import make_toolkit_root
        root=make_toolkit_root()
        try:
            self.assertTrue(root.winfo_exists())
        finally:root.destroy()


class RomajiUIIntegration(RegionUIIntegration):
    def test_romanized_search_and_exact_resource_filter(self):
        from practice.dialogue_japan import JapanDialogueRecord
        target=JapanDialogueRecord(112,0xC,0x777000,(166,13,132,13,151,13,124,89,212,212),(0x70,))
        neighbor=JapanDialogueRecord(112,0x60,0x777100,(14,25),(0x90,))
        unrelated=JapanDialogueRecord(1112,0x10,0x788000,(166,132),(0x20,))
        self.app.dialogue_region_choice.set('japan')
        self.app._dialogue_region_changed()
        self.app.dialogue_records=[target,neighbor,unrelated]
        self.app.dialogue_by_key={r.key:r for r in self.app.dialogue_records}
        self.app.dialogue_tree=ttk.Treeview(self.app.dialogue_tab,
            columns=('resource','offset','references','text'),show='headings')
        self.app.dialogue_kana_hypothesis_enabled.set(True)
        self.app.dialogue_query.set('PU')
        self.app._dialogue_filter()
        self.assertEqual(len(self.app.dialogue_tree.get_children()),2)
        self.app.dialogue_query.set('purazuma')
        self.app._dialogue_filter()
        self.assertEqual(self.app.dialogue_tree.get_children(),(target.key,))
        self.app.dialogue_query.set('resource:112 pu')
        self.app._dialogue_filter()
        self.assertEqual(self.app.dialogue_tree.get_children(),(target.key,))
        self.app.dialogue_selected_key=target.key
        self.app._dialogue_show_selected_resource()
        self.assertEqual(self.app.dialogue_query.get(),'resource:112')
        self.assertEqual(set(self.app.dialogue_tree.get_children()),{target.key,neighbor.key})
        self.assertEqual(tuple(self.app.dialogue_tree.selection()),(target.key,))


class FullDialogueListUI(RegionUIIntegration):
    def test_inferred_japan_list_shows_all_805_rows(self):
        from practice.dialogue_japan import JapanDialogueRecord
        self.app.dialogue_region_choice.set('japan')
        self.app._dialogue_region_changed()
        records=[JapanDialogueRecord(112,n*4,0x730000+n*4,(14,25,20),(n*8,))
                 for n in range(805)]
        self.app.dialogue_records=records
        self.app.dialogue_by_key={r.key:r for r in records}
        self.app.dialogue_tree=ttk.Treeview(self.app.dialogue_tab,
            columns=('resource','offset','references','text'),show='headings')
        self.app.dialogue_kana_hypothesis_enabled.set(True)
        self.app._dialogue_toggle_kana_hypothesis()
        self.assertEqual(len(self.app.dialogue_tree.get_children()),805)
        self.assertTrue(self.app.dialogue_tree.exists(records[-1].key))
        self.assertIn('all 805 displayed',self.app.dialogue_status.get())

    def test_plain_filter_can_extend_legacy_800_results(self):
        from practice.dialogue_japan import JapanDialogueRecord
        records=[JapanDialogueRecord(112,n*4,0x730000+n*4,(14,25,20),(n*8,))
                 for n in range(805)]
        self.app.dialogue_region_choice.set('usa')
        self.app.dialogue_records=records
        self.app.dialogue_filtered=records
        self.app.dialogue_tree=ttk.Treeview(self.app.dialogue_tab,
            columns=('resource','offset','references','text'),show='headings')
        for r in records[:800]:
            self.app.dialogue_tree.insert('','end',iid=r.key,values=(r.resource_id,
                    f'0x{r.text_offset:X}',1,r.text))
        self.app.dialogue_status.set('805 matching records (first 800 shown); 0 staged')
        self.app._dialogue_complete_base_results()
        self.assertEqual(len(self.app.dialogue_tree.get_children()),805)
        self.assertIn('all 805 shown',self.app.dialogue_status.get())
