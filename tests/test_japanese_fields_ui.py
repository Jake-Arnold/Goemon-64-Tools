"""Actual Tk UI smoke tests, designed to run under xvfb-run."""
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from practice.japanese_fields_ui import JapaneseFieldsUi
from practice.japanese_fields import JAPAN_FIELDS
from practice.japanese_scene_probes import JAPAN_SCENE_PROBES
from tests.test_japanese_fields import FakeRam


class Host(JapaneseFieldsUi):
    def __init__(self, root):
        self.active_version = SimpleNamespace(key='japan')
        self.jp_rdram = None
        # JP Live's manual fallback uses the shared Scene Browser selection,
        # which is intentionally not built by this isolated Tk smoke host.
        self.scene_selected = 0x161
        self.scene_list = SimpleNamespace(curselection=lambda: ())
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.scene_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.scene_tab, text="Scene Browser")
        self.initialize_japanese_controls()

    # This minimal UI host deliberately has no Toolkit memory-write backend.
    # The real app binds these callbacks to Toolkit methods; smoke tests
    # must supply inert callbacks to construct the full Japanese tab.
    def move_japan_oedo_xyz(self):
        raise AssertionError('UI smoke host must never issue a position write')

    def open_japan_debug_for_selected_scene(self):
        raise AssertionError('UI smoke host must never enter debug mode')

    def open_full_scene_tab(self):
        # In the real Toolkit this selects the shared Scene Browser; this
        # lightweight test host deliberately does not build USA tabs.
        return None


class JapanTkSmokeTest(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'No Tk display: {exc}')
        self.root.withdraw()
        # A developer's Japan watch profile must never change smoke-test counts.
        self.custom_watch_temp = TemporaryDirectory()
        self.addCleanup(self.custom_watch_temp.cleanup)
        with patch('practice.japanese_fields_ui.practice_data_dir',
                   return_value=Path(self.custom_watch_temp.name)):
            self.host = Host(self.root)

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_all_japan_fields_are_present(self):
        host = self.host
        for attr in ('jp_fields_tab', 'jp_fields_tree', 'jp_research_tabs',
                     'jp_position_apply_button', 'jp_debug_menu_button'):
            self.assertFalse(hasattr(host, attr), attr)
        host.jp_rdram = FakeRam()
        host.refresh_japan_fields(force=True)
        self.assertEqual(set(host._jp_last_readings),
                         {f.key for f in JAPAN_FIELDS + JAPAN_SCENE_PROBES})

    def test_refresh_and_disconnect_clears_without_writer(self):
        host = self.host
        host.jp_rdram = FakeRam({(0x80161DDA, 2): bytes.fromhex('04D2')})
        host.refresh_japan_fields(force=True)
        self.assertEqual(host._jp_last_readings['ryo'].value, '1234')
        self.assertIn('58 Japanese', host.jp_fields_caption.get())
        host.clear_japan_field_values()
        self.assertEqual(host._jp_last_readings, {})

    def test_usa_selection_cannot_read_japan_fields(self):
        host = self.host
        ram = FakeRam()
        host.jp_rdram = ram
        host.active_version.key = 'usa'
        host.refresh_japan_fields(force=True)
        self.assertEqual(ram.reads, [])


if __name__ == '__main__':
    unittest.main()
