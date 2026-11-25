"""Verify rebuilt-recomp speed controls are no longer part of the toolkit UI.

Historical standalone speed modules are preserved in Git history.
"""
from pathlib import Path
import tkinter as tk
import unittest
from practice.toolkit import Toolkit, parse_args

class LiveSpeedUITests(unittest.TestCase):
    def test_retired_speed_sources_not_in_active_tree(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / "speed").exists())
        self.assertFalse((root / "practice" / "live_speed_ui.py").exists())

    def test_speed_ui_removed_without_disabling_pid_connection(self):
        try:
            root=tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        try:
            root.withdraw()
            app=Toolkit(root,parse_args([]))
            self.assertFalse(hasattr(app,'speed_launch_button'))
            self.assertFalse(hasattr(app,'live_speed_button'))
            self.assertTrue(app.connect_button.winfo_exists())
            self.assertTrue(hasattr(app,'enable_linux_external_pid'))
        finally:
            root.destroy()

if __name__=='__main__': unittest.main()
