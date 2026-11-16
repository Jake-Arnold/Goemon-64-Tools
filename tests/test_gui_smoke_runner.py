"""Headless regression coverage for the automated Tk dialog guard."""
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import unittest
from unittest.mock import patch
from tests.gui_smoke_runner import reject_unexpected_modals

class GUISmokeRunnerTests(unittest.TestCase):
    def test_unexpected_dialogs_fail_instead_of_blocking(self):
        previous = messagebox.askyesno
        with reject_unexpected_modals():
            with self.assertRaisesRegex(AssertionError, "messagebox.askyesno"):
                messagebox.askyesno("Confirm", "Would block")
            with self.assertRaisesRegex(AssertionError, "filedialog.askopenfilename"):
                filedialog.askopenfilename()
            with self.assertRaisesRegex(AssertionError, "simpledialog.askinteger"):
                simpledialog.askinteger("Prompt", "Would block")
        self.assertIs(messagebox.askyesno, previous)

    def test_explicit_dialog_mock_is_allowed(self):
        with reject_unexpected_modals():
            with patch("tkinter.messagebox.askyesno", return_value=True):
                self.assertTrue(messagebox.askyesno("Confirm", "Test"))
            with self.assertRaisesRegex(AssertionError, "messagebox.askyesno"):
                messagebox.askyesno("Confirm", "Test")

if __name__ == "__main__":
    unittest.main()
