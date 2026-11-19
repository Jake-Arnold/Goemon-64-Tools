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
        self.assertIn('numeric',self.app.dialogue_status.get())
        self.assertIn('disabled',self.app.dialogue_wrap_button.state())
        self.assertEqual(self.app.dialogue_layout_mode.get(),'Measure only')

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
