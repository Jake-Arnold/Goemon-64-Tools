"""Presentation smoke tests; do not depend on a running game process."""
from __future__ import annotations

import tkinter as tk
import unittest
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import patch

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

    def test_dashboard_only_has_connection_and_checkpoints(self):
        app = self.toolkit
        self.assertEqual(app.notebook.tab(app.notebook.tabs()[0], 'text'), 'Dashboard')
        self.assertFalse(hasattr(app, 'quick_scene_tree'))
        self.assertFalse(hasattr(app, 'quick_watch_tree'))
        self.assertFalse(hasattr(app, 'speed_launch_button'))
        self.assertTrue(app.connect_button.winfo_exists())
        self.assertTrue(app.restore_state_btn.winfo_exists())
        self.assertTrue(app.cancel_restore_btn.winfo_exists())
        self.assertTrue(app.capture_state_btn.winfo_exists())
        self.assertTrue(app.checkpoint_name.winfo_exists())
        self.assertFalse(hasattr(app,'bookmarks_box'))
        self.assertFalse(hasattr(app,'teleport_btn'))
        self.assertFalse(hasattr(app,'bookmark_name'))
        app.open_full_scene_tab()
        self.assertEqual(app.notebook.select(), str(app.scene_tab))
        app.open_live_memory_tab()
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))

    def test_dashboard_scrollable_at_compact_window_size(self):
        app = self.toolkit
        self.root.geometry('960x640')
        self.root.update_idletasks()
        self.assertEqual(app.notebook.tab(app.notebook.tabs()[0], 'text'),'Dashboard')
        self.assertTrue(app.checkpoints_box.winfo_exists())

    def test_combined_selector_labels_full_and_legacy_position_without_misrepresentation(self):
        from tests.test_checkpoint import TestCheckpoint
        from practice.checkpoints import capture_checkpoint
        app=self.toolkit
        _,ram=TestCheckpoint().sample()
        full=capture_checkpoint(ram,'Complete snapshot')
        app.checkpoints=[full]
        app.legacy_bookmarks=[dict(name='Old room',x=1.5,y=2.5,z=3.5,character=0,map_id=35),
                              dict(name='No map',x=1,y=2,z=3,character=0)]
        labels=app.checkpoint_labels()
        self.assertEqual(app.checkpoint_choices(),[('logical',0),('position',0),('position',1)])
        self.assertIn('logical',labels[0]);self.assertIn('XYZ saved',labels[0])
        self.assertIn('POSITION ONLY',labels[1]);self.assertIn('no inventory',labels[1])
        self.assertIn('map unknown',labels[2])
        self.assertFalse(hasattr(app,'save_bookmark'))

    def test_dark_theme_and_no_unsafe_warp_activation(self):
        self.assertEqual(self.root.cget('background'), PALETTE['background'])
        self.assertFalse(self.toolkit.direct_warp_confirmed)
        self.assertFalse(self.toolkit.pending_direct_warp)


if __name__ == '__main__':
    unittest.main()
