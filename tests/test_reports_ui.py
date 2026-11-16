"""Report browser smoke tests; do not require a connected game."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from practice.reports import ReportEntry
from practice.reports_ui import ReportsMixin


class ReportBrowserShell(ReportsMixin):
    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)


class ReportBrowserTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")
        self.root.withdraw()
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / "JP" / "sample"
        self.folder.mkdir(parents=True)
        (self.folder / "summary.md").write_text("Test report")
        self.record = ReportEntry(self.folder, "Sasuke position", "JP",
                                  "2026-11-16T18:15:00Z", "value-search")
        self.shell = ReportBrowserShell(self.root)
        with patch("practice.reports_ui.list_reports",
                   return_value=[self.record]), \
             patch("practice.reports_ui.reports_root",
                   return_value=Path(self.tmp.name)):
            self.shell.build_reports_tab(self.shell.notebook)

    def tearDown(self):
        if hasattr(self, "root"):
            self.root.destroy()

    def test_report_tab_and_selection(self):
        app = self.shell
        self.assertEqual(app.notebook.tab(app.reports_tab, "text"), "Reports")
        self.assertEqual(len(app.reports_tree.get_children()), 1)
        self.assertEqual(app.reports_tree.item("0", "text"), "Sasuke position")
        app.reports_tree.selection_set("0")
        with patch("practice.reports_ui.open_in_file_manager") as opener:
            app.open_selected_report()
        opener.assert_called_once_with(self.folder / "summary.md")

    def test_open_folder_and_copy_path(self):
        app = self.shell
        app.reports_tree.selection_set("0")
        with patch("practice.reports_ui.open_in_file_manager") as opener:
            app.open_selected_report_folder()
        opener.assert_called_once_with(self.folder)
        app.copy_selected_report_path()
        self.assertEqual(self.root.clipboard_get(), str(self.folder))

    def test_missing_selection_is_explained(self):
        app = self.shell
        app.open_selected_report()
        self.assertIn("Select a report", app.report_status.get())


if __name__ == "__main__":
    unittest.main()
