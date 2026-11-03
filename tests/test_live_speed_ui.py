import tkinter as tk
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from practice.toolkit import Toolkit, parse_args
from speed.live_control import SpeedStatus, SpeedUnavailable


class LiveSpeedUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw();self.app=Toolkit(self.root,parse_args([]))
    def tearDown(self):self.root.destroy()

    def test_dashboard_has_one_speed_control(self):
        def walk(widget):
            yield widget
            for child in widget.winfo_children():yield from walk(child)
        matches=[w for w in walk(self.root) if w.winfo_class()=='TLabelframe' and w.cget('text')==' Game speed (recomp) ']
        self.assertEqual(len(matches),1)

    def test_toggle_and_factor_change_use_selected_process_and_ack(self):
        app=self.app;app.game_pid=123
        with patch('practice.live_speed_ui.read_speed',return_value=SpeedStatus(1,1,20)):
            app.poll_live_speed()
        self.assertNotIn('disabled',app.live_speed_button.state())
        app.live_speed_enabled.set(True)
        with patch('practice.live_speed_ui.request_speed') as request:
            app.toggle_live_speed();request.assert_called_once_with(123,2)
        with patch('practice.live_speed_ui.read_speed',return_value=SpeedStatus(2,2,40)):
            app.poll_live_speed()
        self.assertTrue(app.live_speed_enabled.get());self.assertIn('2×',app.live_speed_status.get())
        app.live_speed_factor.set('3×')
        with patch('practice.live_speed_ui.request_speed') as request:
            app.change_live_speed_factor();request.assert_called_once_with(123,3)
        app.live_speed_enabled.set(False)
        with patch('practice.live_speed_ui.request_speed') as request:
            app.toggle_live_speed();request.assert_called_once_with(123,1)

    def test_stock_host_and_read_only_cannot_request_changes(self):
        app=self.app;app.game_pid=123
        with patch('practice.live_speed_ui.read_speed',side_effect=SpeedUnavailable('no channel')):
            app.poll_live_speed()
        self.assertIn('disabled',app.live_speed_button.state())
        app.args.read_only=True;app.live_speed_enabled.set(True)
        with patch('practice.live_speed_ui.request_speed') as request:
            app.toggle_live_speed();request.assert_not_called()
        self.assertFalse(app.live_speed_enabled.get())

    def test_launch_fills_explicit_pid_without_replacing_connection(self):
        app=self.app;app.game_pid=10;app.speed_executable.set('test.exe')
        with patch('practice.live_speed_ui.launch',return_value=SimpleNamespace(pid=456)) as start:
            app.launch_speed_game()
        self.assertEqual(start.call_args.args[1],1)
        self.assertEqual(app.pid_text.get(),'456');self.assertEqual(app.game_pid,10)
        self.assertEqual(app.connection_target.get(),'recomp')

    def test_invalid_pid_is_rejected_before_disconnect(self):
        app=self.app;app.pid_text.set('invalid');app.game_pid=77
        with patch.object(app,'stop_all_freezes') as stop:
            app.connect();stop.assert_not_called()
        self.assertEqual(app.game_pid,77);self.assertIn('valid positive PID',app.status.get())

    def test_pending_and_timeout_status(self):
        app=self.app;app.game_pid=123;app._speed_last_target=123;app._speed_requested=2;app._speed_requested_at=0
        with patch('practice.live_speed_ui.read_speed',return_value=SpeedStatus(2,1,20)), patch('practice.live_speed_ui.time.monotonic',return_value=4):
            app.poll_live_speed()
        self.assertIsNone(app._speed_requested);self.assertFalse(app.live_speed_enabled.get())
        self.assertIn('no speed acknowledgement',app.live_speed_status.get())
