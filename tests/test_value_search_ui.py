"""Value Search Tk smoke tests; no toolkit process or game required."""
from __future__ import annotations

import struct
import time
import tkinter as tk
from tkinter import ttk
import unittest
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

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
        self.added_watches = []
        self.build_value_search_tab(self.notebook)
        self.value_search_size = 64

    def add_custom_watch(self):
        self.added_watch = (self.user_watch_name.get(),
                            self.user_watch_address.get(),
                            self.user_watch_type.get())
        self.added_watches.append(self.added_watch)


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

    def test_root_destroy_cancels_periodic_search_callbacks(self):
        app = self.app
        initial = app._value_search_auto_after
        self.assertIsNotNone(initial)
        with patch.object(self.root, 'after_cancel',
                          wraps=self.root.after_cancel) as cancel:
            app._value_search_on_destroy(
                SimpleNamespace(widget=self.root))
            cancel.assert_any_call(initial)
        self.assertIsNone(app._value_search_auto_after)
        self.assertIsNone(app._value_search_poll_after)

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


    def test_continuous_unchanged_against_initial_and_stop(self):
        app = self.app
        app.value_repeat_interval.set('2000 ms')
        app._value_start('unknown')
        self.finish()
        initial_count = app.value_scanner.count
        app.value_search_filter.set('Unchanged')
        app.value_search_compare.set('Initial')
        app.toggle_continuous_value_filter()
        self.assertTrue(app._value_repeat_running)
        self.finish()
        self.assertEqual(app.value_scanner.count, initial_count)
        self.assertEqual(app._value_repeat_scans, 1)
        self.assertIn('Stop continuous filter', app.value_repeat_button.cget('text'))
        app.mem.put(8, 20)
        app._value_repeat_due = time.monotonic() - 1
        self.root.update()
        self.finish()
        self.assertEqual(app._value_repeat_scans, 2)
        self.assertLess(app.value_scanner.count, initial_count)
        app.toggle_continuous_value_filter()
        self.assertFalse(app._value_repeat_running)
        self.assertIn('Start continuous filter', app.value_repeat_button.cget('text'))
        self.assertIn('Stopped after 2', app.value_repeat_status.get())

    def test_continuous_exact_uses_filter_value_and_zero_stops(self):
        app = self.app
        app.mem.put(8, 950)
        app._value_start('exact')
        self.finish()
        app.mem.put(8, 900)
        app.value_search_filter.set('Exact')
        app._value_search_filter_changed()
        app.value_filter_value.set('900')
        app.toggle_continuous_value_filter()
        self.finish()
        self.assertEqual(app.value_scanner.count, 1)
        self.assertTrue(app._value_repeat_running)
        app.mem.put(8, 800)
        app._value_repeat_due = time.monotonic() - 1
        self.root.update()
        self.finish()
        self.assertFalse(app._value_repeat_running)
        self.assertEqual(app.value_scanner.count, 0)
        self.assertIn('zero candidates', app.value_repeat_status.get())

    def test_continuous_requires_scan_and_valid_filter_and_stops_on_clear(self):
        app = self.app
        app.toggle_continuous_value_filter()
        self.assertFalse(app._value_repeat_running)
        self.assertIn('Finish a scan', app.value_repeat_status.get())
        app._value_start('unknown')
        self.finish()
        app.value_search_filter.set('Exact')
        app._value_search_filter_changed()
        app.value_filter_value.set('')
        app.toggle_continuous_value_filter()
        self.assertFalse(app._value_repeat_running)
        self.assertIn('Invalid Exact', app.value_repeat_status.get())
        app.value_filter_value.set('0')
        app.toggle_continuous_value_filter()
        self.finish()
        self.assertTrue(app._value_repeat_running)
        app.clear_value_search()
        self.assertFalse(app._value_repeat_running)
        self.assertEqual(app.value_scanner.count, 0)

    def test_continuous_stops_on_connection_change(self):
        app = self.app
        app._value_start('unknown')
        self.finish()
        app.value_search_filter.set('Unchanged')
        app.toggle_continuous_value_filter()
        self.finish()
        app.invalidate_value_search_connection()
        self.assertFalse(app._value_repeat_running)
        self.assertEqual(app.value_scanner.count, 0)
        self.assertIn('connection changed', app.value_repeat_status.get())

    def test_multi_select_watches_saved_in_one_batch(self):
        from practice.custom_watches import load_watches
        app = self.app
        app.mem.put(8, 950)
        app.mem.put(24, 950)
        app._value_start('exact')
        self.finish()
        self.assertEqual(app.value_search_tree['selectmode'], 'extended')
        app.select_all_value_results()
        self.assertEqual(len(app.value_search_tree.selection()), 2)
        with TemporaryDirectory() as tmp, patch(
            'practice.ui_extension.CUSTOM_WATCHES_PATH',
            Path(tmp) / 'custom-watches.json'
        ) as user_path:
            app.custom_watches = []
            app.watch_value_search_candidate()
            saved = load_watches(user_path)
            self.assertEqual(len(saved), 2)
            self.assertEqual(
                {w.address for w in saved},
                {GUEST_BASE + 8, GUEST_BASE + 24})
            app.watch_value_search_candidate()
            self.assertEqual(len(load_watches(user_path)), 2)

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
