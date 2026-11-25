"""Japanese Mupen read-only search and watch parity regression tests.

No emulator, ROM, or writable process handles. Tk tests run under Xvfb.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import time
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.test_japanese_fields_ui import Host
from tests.test_japanese_fields import FakeRam
from tests.test_value_search_ui import FakeToolkit, BossMemory


class JapanCustomWatchesTest(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Tk needs an X11 display: {exc}')
        self.root.withdraw()
        self.temp = TemporaryDirectory()
        self.mock_path = patch('practice.japanese_fields_ui.practice_data_dir',
                               return_value=Path(self.temp.name))
        self.mock_path.start()
        self.addCleanup(self.mock_path.stop)
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.root.destroy)
        self.host = Host(self.root)

    def test_region_scoped_persistent_watch_and_live_refresh(self):
        host = self.host
        self.assertEqual(host.jp_watch_path.name, 'japan_0_custom_watches.json')
        self.assertNotEqual(host.jp_watch_path.name, 'custom_watches.json')
        ram = FakeRam({(0x80161DCC, 4): bytes.fromhex('00000002')})
        ram.base, ram.endian = 0x10000000, 'wordswapped'
        host.game_pid, host.jp_rdram = 101, ram
        self.assertTrue(host.add_japan_custom_watch('Active character candidate', '0x80161DCC', 'u32'))
        key = 'custom:active character candidate'
        self.assertEqual(host._jp_last_readings[key].value, '2')
        self.assertEqual(host._jp_last_readings[key].raw, '0x00000002')
        self.assertEqual(len(host.jp_custom_watches), 1)
        self.assertIn('read-only', host.jp_custom_watch_status.get())
        self.assertTrue(host.jp_watch_path.exists())
        self.assertFalse(hasattr(ram, 'write_guest'))

        host.capture_japan_baseline()
        ram.values[(0x80161DCC, 4)] = bytes.fromhex('00000003')
        host.compare_japan_baseline()
        self.assertIn('custom:active character candidate',
                      {change[0] for change in host._jp_last_changes})
        self.assertIn((key, '0x00000002', '0x00000003'), host._jp_last_changes)
        self.assertTrue(host.remove_japan_custom_watch('Active character candidate'))
        self.assertNotIn(key, host._jp_last_readings)
        self.assertEqual(host.jp_custom_watches, [])
        self.assertIsNone(host._jp_baseline)

    def test_disallow_duplicate_bad_bounds_and_usa_mode_mutation(self):
        host = self.host
        self.assertFalse(host.add_japan_custom_watch('Candidate', '0x807FFFFF', 'u32'))
        self.assertEqual(len(host.jp_custom_watches), 0)
        self.assertTrue(host.add_japan_custom_watch('Candidate', '0x80161DCC', 'u32'))
        self.assertFalse(host.add_japan_custom_watch('Candidate', '0x80161DCC', 'u32'))
        self.assertEqual(len(host.jp_custom_watches), 1)

        original = host.jp_watch_path.read_bytes()
        host.active_version.key = 'usa'
        self.assertFalse(host.add_japan_custom_watch('Should not be saved', '0x80161DCC', 'u32'))
        self.assertEqual(host.jp_watch_path.read_bytes(), original)
        self.assertFalse(host.remove_japan_custom_watch("Candidate"))


class JapanValueSearchUiTest(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Tk needs an X11 display: {exc}')
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.app = FakeToolkit(self.root)
        self.app.active_version = SimpleNamespace(key='japan')
        self.app.jp_rdram = BossMemory()
        self.app.jp_custom_watch_status = tk.StringVar(value='')
        self.app.promoted = []
        def add_japan_watch(addr, kind):
            self.app.promoted.append((addr, kind))
            return True
        self.app.add_japan_custom_watch_from_search = add_japan_watch

    def finish(self):
        deadline = time.monotonic() + 5
        while self.app.value_scan_busy and time.monotonic() < deadline:
            self.root.update()
            time.sleep(0.01)
        self.root.update()
        self.assertFalse(self.app.value_scan_busy, self.app.value_search_status.get())

    def test_jp_search_uses_jp_ram_not_usa_ram_and_promotes_only_to_jp(self):
        app = self.app
        app.mem.put(8, 950)
        app.jp_rdram.put(24, 950)
        app.value_search_type.set('u16')
        app.value_search_value.set('950')
        app.value_search_size = 64
        app._value_start('exact')
        self.finish()
        self.assertEqual(app.value_search_tree.get_children(), ('0x80000018',))
        self.assertEqual(app.value_scanner.count, 1)
        app.value_search_tree.selection_set('0x80000018')
        app.watch_value_search_candidate()
        self.assertEqual(app.promoted, [('0x80000018', 'u16')])
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))
        self.assertIsNone(app.added_watch)
        self.assertFalse(hasattr(app.jp_rdram, 'write_guest'))

    def test_jp_multi_select_promotes_all_and_does_not_use_usa_memory(self):
        app = self.app
        app.value_search_size = 64
        app.mem.put(16, 950)  # Must not be included in Japanese results.
        app.jp_rdram.put(8, 950)
        app.jp_rdram.put(24, 950)
        app._value_start('exact')
        self.finish()
        app.select_all_value_results()
        app.watch_value_search_candidate()
        self.assertEqual(
            app.promoted,
            [('0x80000008', 'u16'), ('0x80000018', 'u16')])
        self.assertIsNone(app.added_watch)
        self.assertFalse(hasattr(app.jp_rdram, 'write_guest'))

    def test_disconnect_discards_results_and_does_not_fall_back_to_usa(self):
        app = self.app
        app.value_search_size = 64
        app.jp_rdram.put(8, 950)
        app._value_start('exact')
        self.finish()
        self.assertEqual(app.value_scanner.count, 1)
        app.jp_rdram = None
        app.invalidate_value_search_connection()
        self.assertEqual(app.value_scanner.count, 0)
        self.assertEqual(app.value_search_tree.get_children(), ())
        app._value_start('exact')
        self.assertIn('Connect to a running game first', app.value_search_status.get())


if __name__ == '__main__':
    unittest.main()
