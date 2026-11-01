"""Presentation smoke tests; do not depend on a running game process."""
from __future__ import annotations

import tkinter as tk
import unittest
from argparse import Namespace

from practice.inspector import Watch
from practice.theme import PALETTE
from practice.toolkit import Toolkit


class DashboardSmokeTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk display unavailable: {exc}')
        self.root.withdraw()
        opts = dict(pid=None, base=None, endian='auto', route=None,
                    enable_teleport=True, enable_state_restore=True,
                    enable_debug_menu=True, enable_hex_edit=True,
                    enable_scene_warp=False)
        self.toolkit = Toolkit(self.root, Namespace(**opts))

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_dashboard_scene_search_and_tab_navigation(self):
        app = self.toolkit
        self.assertEqual(app.notebook.tab(app.notebook.tabs()[0], 'text'), 'Dashboard')
        app.quick_scene_filter.set('Festival Temple')
        scene_ids = app.quick_scene_tree.get_children()
        self.assertTrue(scene_ids)
        scene_id = scene_ids[0]
        app.quick_scene_tree.selection_set(scene_id)
        app.choose_quick_scene()
        self.assertEqual(app.scene_selected, int(scene_id))
        self.assertIsNone(app.pending_direct_warp)
        self.assertIsNone(app.pending_native_warp)
        app.open_full_scene_tab()
        self.assertEqual(app.notebook.select(), str(app.scene_tab))
        app.open_live_memory_tab()
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))

    def test_disconnected_memory_preview_remains_empty(self):
        app = self.toolkit
        app.watch_rows = [Watch('Map ID', 0x800C7AB2, '90', '005A', 'OK', 'mapped')]
        app.refresh_quick_watch()
        self.assertEqual(app.quick_watch_tree.get_children(), ())
        app.mem = object()  # Preview only; no game-memory calls required.
        app.refresh_quick_watch()
        self.assertEqual(app.quick_watch_tree.item('Map ID', 'values')[2], '005A')
        app.watch_rows = [Watch('Map ID', 0x800C7AB2, '96', '0060', 'OK', 'mapped')]
        app.refresh_quick_watch()
        self.assertIn('changed', app.quick_watch_tree.item('Map ID', 'tags'))
        app.mem = None
        app.refresh_quick_watch()
        self.assertEqual(app.quick_watch_tree.get_children(), ())

    def test_dark_theme_and_no_unsafe_warp_activation(self):
        self.assertEqual(self.root.cget('background'), PALETTE['background'])
        self.assertFalse(self.toolkit.direct_warp_confirmed)
        self.assertFalse(self.toolkit.pending_direct_warp)


if __name__ == '__main__':
    unittest.main()
