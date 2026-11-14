"""Actual Tk UI smoke tests, designed to run under xvfb-run."""
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
import unittest

from practice.japanese_fields_ui import JapaneseFieldsUi
from practice.japanese_fields import JAPAN_FIELDS
from tests.test_japanese_fields import FakeRam


class Host(JapaneseFieldsUi):
    def __init__(self, root):
        self.active_version = SimpleNamespace(key='japan')
        self.jp_rdram = None
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.build_japanese_fields_tab(self.notebook)


class JapanTkSmokeTest(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'No Tk display: {exc}')
        self.root.withdraw()
        self.host = Host(self.root)

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_all_japan_fields_are_present(self):
        tree = self.host.jp_fields_tree
        self.assertEqual(sum(len(tree.get_children(x)) for x in tree.get_children('')),
                         len(JAPAN_FIELDS))
        self.assertEqual(tree.set('jp_field_ryo', 'value'), '—')
        self.assertIn('Japan Live', self.host.notebook.tab(self.host.jp_fields_tab, 'text'))

    def test_refresh_and_disconnect_clears_without_writer(self):
        host = self.host
        host.jp_rdram = FakeRam({(0x80161DDA, 2): bytes.fromhex('04D2')})
        host.refresh_japan_fields(force=True)
        self.assertEqual(host.jp_fields_tree.set('jp_field_ryo', 'value'), '1234')
        self.assertIn('58 Japanese', host.jp_fields_caption.get())
        host.clear_japan_field_values()
        self.assertEqual(host.jp_fields_tree.set('jp_field_ryo', 'value'), '—')

    def test_usa_selection_cannot_read_japan_fields(self):
        host = self.host
        ram = FakeRam()
        host.jp_rdram = ram
        host.active_version.key = 'usa'
        host.refresh_japan_fields(force=True)
        self.assertEqual(ram.reads, [])


if __name__ == '__main__':
    unittest.main()
