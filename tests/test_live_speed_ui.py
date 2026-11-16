"""Verify rebuilt-recomp speed controls are no longer part of the toolkit UI.

Standalone speed research modules remain available without a live GUI entry.
"""
import tkinter as tk
import unittest
from practice.toolkit import Toolkit, parse_args

class LiveSpeedUITests(unittest.TestCase):
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
