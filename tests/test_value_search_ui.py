"""Value Search Tk smoke tests; no toolkit process or game required."""
from __future__ import annotations

import struct
import time
import tkinter as tk
from tkinter import ttk
import unittest

from practice.value_search_ui import ValueSearchMixin
from practice.value_search import GUEST_BASE


class BossMemory:
    def __init__(self):
        self.data = bytearray(64)

    def read_guest(self, addr, width):
        off = addr - GUEST_BASE
        if not 0 <= off <= len(self.data) - width:
            raise OSError('invalid game RAM read')
        return bytes(self.data[off:off + width])

    def put(self, offset, amount):
        self.data[offset:offset + 2] = struct.pack('>H', amount)

    def snapshot(self):
        raise ValueError('Invalid player object pointer 0xA4600014')


class FakeToolkit(ValueSearchMixin):
    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.live_memory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.live_memory_tab, text='Live memory')
        self.mem = BossMemory()
        self.user_watch_name = tk.StringVar()
        self.user_watch_address = tk.StringVar()
        self.user_watch_type = tk.StringVar()
        self.added_watch = None
        self.build_value_search_tab(self.notebook)
        self.value_search_size = 64

    def add_custom_watch(self):
        self.added_watch = (self.user_watch_name.get(),
                            self.user_watch_address.get(),
                            self.user_watch_type.get())


class ValueSearchUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk display unavailable: {exc}')
        self.root.withdraw()
        self.app = FakeToolkit(self.root)

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def finish(self):
        deadline = time.monotonic() + 5
        while self.app.value_scan_busy and time.monotonic() < deadline:
            self.root.update()
            time.sleep(0.01)
        self.root.update()
        self.assertFalse(self.app.value_scan_busy, self.app.value_search_status.get())

    def test_find_oil_and_narrow_without_player_object(self):
        app = self.app
        app.mem.put(8, 950)
        app.mem.put(24, 950)
        app.value_search_type.set('u16')
        app.value_search_value.set('950')
        app._value_start('exact')
        self.finish()
        self.assertEqual(app.value_scanner.count, 2)
        app.mem.put(8, 920)
        app.value_search_filter.set('Decreased')
        app._value_start('filter')
        self.finish()
        self.assertEqual(app.value_scanner.count, 1)
        self.assertEqual(app.value_search_tree.get_children(), ('0x80000008',))
        app.value_search_tree.selection_set('0x80000008')
        app.watch_value_search_candidate()
        self.assertEqual(app.added_watch[1:], ('0x80000008', 'u16'))
        self.assertIn('No game memory was modified', app.value_search_status.get())

    def test_unknown_and_clear_resets_candidates(self):
        app = self.app
        app._value_start('unknown')
        self.finish()
        self.assertGreater(app.value_scanner.count, 0)
        app.clear_value_search()
        self.assertEqual(app.value_scanner.count, 0)
        self.assertFalse(app.value_search_tree.get_children())


if __name__ == '__main__':
    unittest.main()
