"""Fail-closed, subprocess-mocked Linux keyboard tests; no real key injection."""
from __future__ import annotations
import os
import unittest
from unittest.mock import patch

from practice import linux_input


class LinuxInputTests(unittest.TestCase):
    def test_x11_target_focus_and_balanced_release(self):
        calls = []
        def fake(*args):
            calls.append(args)
            if args[0] == "search": return "123\n"
            if args[0] == "getwindowpid": return "55"
            if args[0] == "getwindowname": return "Goemon 64: Recompiled"
            if args[0] == "getwindowfocus": return "123"
            return ""
        with patch.object(linux_input.sys, "platform", "linux"), \
             patch.dict(os.environ, {"XDG_SESSION_TYPE": "x11", "DISPLAY": ":0"}), \
             patch.object(linux_input.shutil, "which", return_value="/usr/bin/xdotool"), \
             patch.object(linux_input, "_run", side_effect=fake):
            release = linux_input.press_key(55, "Down")
            release()
            release()
        self.assertEqual([x[0] for x in calls].count("keydown"), 1)
        self.assertEqual([x[0] for x in calls].count("keyup"), 1)

    def test_wrong_focused_pid_never_injects(self):
        calls = []
        def fake(*args):
            calls.append(args)
            if args[0] == "search": return "123"
            if args[0] == "getwindowpid": return "55" if args[1] == "123" else "99"
            if args[0] == "getwindowname": return "Goemon 64: Recompiled"
            if args[0] == "getwindowfocus": return "999"
            return ""
        with patch.object(linux_input.sys, "platform", "linux"), \
             patch.dict(os.environ, {"XDG_SESSION_TYPE": "x11", "DISPLAY": ":0"}), \
             patch.object(linux_input.shutil, "which", return_value="/usr/bin/xdotool"), \
             patch.object(linux_input, "_run", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "does not belong"):
                linux_input.press_key(55, "space")
        self.assertFalse(any(x[0] == "keydown" for x in calls))

    def test_wayland_and_missing_dependency_fail_without_injection(self):
        with patch.object(linux_input.sys, "platform", "linux"), \
             patch.dict(os.environ, {"XDG_SESSION_TYPE": "wayland", "DISPLAY": ":0"}), \
             patch.object(linux_input, "_run") as run:
            with self.assertRaisesRegex(OSError, "Wayland"):
                linux_input.press_key(55, "Down")
            run.assert_not_called()
        with patch.object(linux_input.sys, "platform", "linux"), \
             patch.dict(os.environ, {"XDG_SESSION_TYPE": "x11", "DISPLAY": ":0"}), \
             patch.object(linux_input.shutil, "which", return_value=None), \
             patch.object(linux_input, "_run") as run:
            with self.assertRaisesRegex(OSError, "xdotool"):
                linux_input.press_key(55, "Down")
            run.assert_not_called()

    def test_unknown_key_fails_before_focus_or_dispatch(self):
        with patch.object(linux_input, "_focused_game") as focused:
            with self.assertRaises(ValueError):
                linux_input.press_key(55, "Return")
            focused.assert_not_called()


if __name__ == "__main__":
    unittest.main()
