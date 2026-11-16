"""Automatic Japanese client restart/PID reuse detection (no process writes)."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from practice.toolkit import Toolkit
from tests.test_japan_party_controller import Label


class Field:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value
    def set(self, value):
        self.value = value


def screen(*, connected=True, target='auto', birth=100):
    app = SimpleNamespace(
        active_version=SimpleNamespace(key='japan'),
        connection_target=Field(target),
        _connecting=False,
        _jp_reconnect_enabled=True,
        _jp_process_birth=birth,
        _jp_last_liveness_check=0.0,
        _jp_last_auto_attempt=0.0,
        jp_rdram=object() if connected else None,
        game_pid=321 if connected else None,
        pid_text=Field('321'),
        status=Label(),
        _clear_japan_base_choices=Mock(),
        _connect_japan_emulator=Mock(),
    )
    def disconnect():
        app.jp_rdram = None
        app.game_pid = None
    app._disconnect_for_version_change = Mock(side_effect=disconnect)
    return app


class JapanesePidRestartTests(unittest.TestCase):
    def test_same_verified_pid_creation_time_keeps_connected_handle(self):
        s = screen()
        with patch('psutil.Process') as process:
            process.return_value.create_time.return_value = 100
            Toolkit._watch_japan_process_restart(s, 25.0)
        process.assert_called_once_with(321)
        s._disconnect_for_version_change.assert_not_called()
        s._connect_japan_emulator.assert_not_called()
        self.assertIsNotNone(s.jp_rdram)

    def test_pid_restart_closes_old_session_and_rescans_without_old_pid(self):
        s = screen()
        with patch('psutil.Process') as process:
            process.return_value.create_time.return_value = 130
            Toolkit._watch_japan_process_restart(s, 25.0)
        s._disconnect_for_version_change.assert_called_once_with()
        s._clear_japan_base_choices.assert_called_once_with()
        s._connect_japan_emulator.assert_called_once_with()
        self.assertIsNone(s.game_pid)
        self.assertEqual(s.pid_text.get(), '')
        self.assertEqual(s._jp_last_auto_attempt, 25.0)
        self.assertIn('restarted', s.status.value)

    def test_missing_client_triggered_by_nosuchprocess(self):
        import psutil
        s = screen()
        with patch('psutil.Process', side_effect=psutil.NoSuchProcess(321)):
            Toolkit._watch_japan_process_restart(s, 25.0)
        s._disconnect_for_version_change.assert_called_once_with()
        s._connect_japan_emulator.assert_called_once_with()

    def test_retry_is_bounded_when_game_is_not_running(self):
        s = screen(connected=False)
        s._jp_last_auto_attempt = 10.0
        Toolkit._watch_japan_process_restart(s, 13.0)
        s._connect_japan_emulator.assert_not_called()
        Toolkit._watch_japan_process_restart(s, 25.0)
        s._connect_japan_emulator.assert_called_once_with()
        self.assertEqual(s.pid_text.get(), '')
        self.assertEqual(s._jp_last_auto_attempt, 25.0)

    def test_manual_backend_or_connection_in_progress_never_restarts(self):
        for state in (dict(target='recomp'), dict(target='auto', connecting=True)):
            with self.subTest(state=state):
                s = screen(target=state['target'])
                s._connecting = state.get('connecting', False)
                with patch('psutil.Process') as process:
                    Toolkit._watch_japan_process_restart(s, 25.0)
                process.assert_not_called()
                s._connect_japan_emulator.assert_not_called()


if __name__ == '__main__':
    unittest.main()
