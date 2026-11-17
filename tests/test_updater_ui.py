"""Tk Dashboard updater UI uses the main thread and never checks Git at boot."""
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.updater import UpdateStatus


class UpdaterUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        rom = patch('practice.toolkit.load_remembered_rom', return_value=None)
        rom.start()
        self.addCleanup(rom.stop)
        save = patch('practice.toolkit.save_last_region')
        save.start()
        self.addCleanup(save.stop)
        self.app = Toolkit(self.root, parse_args(['--game-version', 'usa']))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for callback in self.root.tk.call('after', 'info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def test_dashboard_has_check_button_without_network_at_startup(self):
        app = self.app
        self.assertEqual(app.update_button.cget('text'), 'Check for updates')
        self.assertTrue(app.update_card.winfo_exists())
        self.assertFalse(app._update_busy)
        self.assertIsNone(app._update_ready)
        self.assertFalse(app._restart_after_update)

    def test_available_update_changes_same_button_to_install(self):
        app = self.app
        status = UpdateStatus('available', 'a' * 40, 'b' * 40)
        app._handle_update_result(False, status, None)
        self.assertEqual(app._update_ready, status)
        self.assertEqual(
            app.update_button.cget('text'), 'Install update and restart')
        self.assertIn('Update available', app.update_status.get())
        app._handle_update_result(False, None, 'Non-main development branch')
        self.assertIsNone(app._update_ready)
        self.assertEqual(app.update_button.cget('text'), 'Check for updates')
        self.assertIn('Non-main', app.update_status.get())

    def test_up_to_date_does_not_offer_install(self):
        app = self.app
        app._handle_update_result(
            False, UpdateStatus('current', 'a' * 40, 'a' * 40), None)
        self.assertIsNone(app._update_ready)
        self.assertIn('Up to date', app.update_status.get())

    def test_success_schedules_close_for_cleanup_then_relaunch(self):
        app = self.app
        with patch.object(self.root, 'after') as after:
            app._handle_update_result(True, 'a' * 40, None)
        self.assertTrue(app._restart_after_update)
        self.assertIn('restarting toolkit', app.update_status.get())
        self.assertIn('disabled', app.update_button.state())
        after.assert_called_once_with(100, self.root.destroy)


if __name__ == '__main__':
    unittest.main()
