"""Headless Tk exercise of the shared discovery results controls."""
from __future__ import annotations

import struct
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from practice.custom_watches import load_watches
from practice.discovery_results import DiscoveryResultsPanel


class Ram:
    def __init__(self):
        self.data = bytearray(128)
        self.reads = []
        self.writes = 0

    def read_guest(self, address, width):
        start = address - 0x80000000
        self.reads.append((address, width))
        if not 0 <= start <= len(self.data) - width:
            raise OSError("Out of RAM")
        return bytes(self.data[start:start + width])


class ResultPanelsTest(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"No Tk display: {exc}")
        self.root.withdraw()
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.app = SimpleNamespace()
        self.app.root = self.root
        self.app.notebook = ttk.Notebook(self.root)
        self.app.notebook.pack(fill="both", expand=True)
        self.app.live_memory_tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.app.live_memory_tab, text="Live memory")
        self.app.discovery_tab = ttk.Frame(self.app.notebook)
        self.app.notebook.add(self.app.discovery_tab, text="Memory discovery")
        self.app.discovery_tabs = ttk.Notebook(self.app.discovery_tab)
        self.app.discovery_tabs.pack(fill="both", expand=True)
        self.app.active_version = SimpleNamespace(key="usa")
        self.app.game_pid = 9876
        self.app.mem = Ram()
        self.app.jp_rdram = Ram()
        self.app.custom_watches = []
        self.app.jp_custom_watches = []
        self.app.jp_watch_path = Path(self.folder.name) / "jp.json"
        self.app._jp_insert_custom_watch = Mock()
        self.app._jp_reset_comparison = Mock()
        self.app.refresh_japan_fields = Mock()
        self.app.refresh_inspector = Mock()
        self.app.current = {}
        self.app.last_inspect_at = 123.0
        self.panels = {}
        for title, value_type in (
            ("Find a value", "u16"),
            ("Compare memory changes", "f32 candidate"),
            ("Investigate flags", "u8"),
            ("Record damage", "u32"),
        ):
            tab = ttk.Frame(self.app.discovery_tabs)
            self.app.discovery_tabs.add(tab, text=title)
            status = tk.StringVar(value="Ready")
            report = tk.StringVar(value=title)
            # Treeview exists before the panel is built; lambda closes over
            # its own per-iteration reference using a default argument.
            tree = ttk.Treeview(
                tab, columns=("address", "type", "live", "raw"),
                show="headings", selectmode="extended")
            for col in ("address", "type", "live", "raw"):
                tree.heading(col, text=col)
            panel = DiscoveryResultsPanel(
                self.app, tab, tree=lambda t=tree: t, status=status,
                report_name=report, save=Mock(), label=title)
            tree.pack(fill="both", expand=True)
            self.panels[title] = (panel, tree, tab)

    def tearDown(self):
        try:
            if self.root.winfo_exists():
                self.root.destroy()
        except tk.TclError:
            pass

    def spin(self, condition, timeout=3.0):
        deadline = time.monotonic() + timeout
        while not condition() and time.monotonic() < deadline:
            self.root.update()
            time.sleep(0.01)
        self.assertTrue(condition())

    def test_all_four_modes_show_same_candidate_actions_and_live_values(self):
        values = {
            "Find a value": (8, "u16", (950).to_bytes(2, "big"), "950"),
            "Compare memory changes": (16, "f32 candidate",
                                       struct.pack(">f", 7.5), "7.5"),
            "Investigate flags": (24, "u8", b"\x20", "32"),
            "Record damage": (32, "u32", (123456).to_bytes(4, "big"), "123456"),
        }
        self.app.notebook.select(self.app.discovery_tab)
        for title, (offset, kind, data, expected) in values.items():
            with self.subTest(title=title):
                panel, tree, tab = self.panels[title]
                self.app.mem.data[offset:offset + len(data)] = data
                tree.insert("", "end", iid="0",
                            values=(f"0x800000{offset:02X}", kind, "—", "—"))
                self.app.discovery_tabs.select(tab)
                panel.refresh_now()
                self.spin(lambda: tree.set("0", "live") == expected)
                self.assertEqual(tree.set("0", "raw"),
                                 "0x" + data.hex().upper())
                self.assertTrue(panel.auto.get())
                self.assertEqual(panel.interval.get(), "250 ms")
                self.assertEqual(tree["selectmode"], "extended")
                self.assertEqual(panel.save_button.cget("text"), "Save report")
        self.assertEqual(self.app.mem.writes, 0)

    def test_batch_watches_and_japan_only_reader(self):
        panel, tree, tab = self.panels["Investigate flags"]
        self.app.notebook.select(self.app.discovery_tab)
        self.app.discovery_tabs.select(tab)
        self.app.active_version.key = "japan"
        self.app.mem.data[8] = 0x21  # USA deliberately differs.
        self.app.jp_rdram.data[8] = 0x53
        self.app.jp_rdram.data[16] = 0x40
        tree.insert("", "end", iid="0",
                    values=("0x80000008", "u8", "—", "—"))
        tree.insert("", "end", iid="1",
                    values=("0x80000010", "u8", "—", "—"))
        panel.refresh_now()
        self.spin(lambda: tree.set("0", "live") == "83")
        tree.selection_set(tree.get_children())
        panel.watch_selected()
        self.assertEqual(len(self.app.jp_custom_watches), 2)
        self.assertEqual(len(self.app.custom_watches), 0)
        self.assertEqual(len(load_watches(self.app.jp_watch_path)), 2)
        self.assertEqual(
            {w.address for w in self.app.jp_custom_watches},
            {0x80000008, 0x80000010})
        self.assertEqual(self.app.notebook.select(),
                         str(self.app.live_memory_tab))
        self.assertEqual(self.app.jp_rdram.writes, 0)
        self.assertEqual(self.app.mem.writes, 0)

    def test_live_updates_change_without_changing_original_candidates(self):
        panel, tree, tab = self.panels["Record damage"]
        self.app.notebook.select(self.app.discovery_tab)
        self.app.discovery_tabs.select(tab)
        self.app.mem.data[32:36] = (100).to_bytes(4, "big")
        tree.insert("", "end", iid="0",
                    values=("0x80000020", "u32", "—", "—"))
        panel.refresh_now()
        self.spin(lambda: tree.set("0", "live") == "100")
        self.app.mem.data[32:36] = (101).to_bytes(4, "big")
        panel.refresh_now()
        self.spin(lambda: tree.set("0", "live") == "101")
        self.assertEqual(len(tree.get_children()), 1)
        self.assertEqual(tree.set("0", "type"), "u32")

    def test_save_report_and_selected_address_controls(self):
        panel, tree, tab = self.panels["Compare memory changes"]
        tree.insert("", "end", iid="0",
                    values=("0x80000020", "u8", "—", "—"))
        tree.insert("", "end", iid="1",
                    values=("0x80000024", "u8", "—", "—"))
        panel.select_visible()
        self.assertEqual(len(tree.selection()), 2)
        panel.copy_address()
        self.assertIn(self.root.clipboard_get(),
                      ("0x80000020", "0x80000024"))
        panel.save_button.invoke()
        self.assertEqual(panel.save_action.call_count, 1)


if __name__ == "__main__":
    unittest.main()
