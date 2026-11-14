"""No-emulator tests: process and focused-window dispatch use mocks."""
import os
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from practice import emulator_savestates as state

class EmulatorStateTests(unittest.TestCase):
    def test_names(self):
        self.assertEqual(state.emulator_kind("Project64.exe"), "project64")
        self.assertEqual(state.emulator_kind("mupen64plus"), "mupen64plus")
        self.assertIsNone(state.emulator_kind("Goemon64Recompiled"))

    def test_ambiguous_processes(self):
        p = SimpleNamespace(process_iter=lambda names: iter([
            SimpleNamespace(info={"pid": 11, "name": "Project64.exe"}),
            SimpleNamespace(info={"pid": 22, "name": "mupen64plus"})]))
        with patch.object(state, "_psutil", return_value=p):
            with self.assertRaisesRegex(RuntimeError, "Multiple"):
                state.find_emulator_pid("auto")
            self.assertEqual(state.find_emulator_pid("mupen64plus"), (22, "mupen64plus"))

    def test_other_process_rejected(self):
        p = SimpleNamespace(Process=lambda pid: SimpleNamespace(name=lambda: "Goemon64Recompiled"),
                            NoSuchProcess=RuntimeError, AccessDenied=PermissionError)
        with patch.object(state, "_psutil", return_value=p):
            with self.assertRaises(ValueError):
                state.verified_emulator_pid(11, "project64")

    def test_wrong_x11_focus_never_types(self):
        calls = []
        def fake(*args):
            calls.append(args)
            return {"search": "123", "getwindowpid": "11" if args[1] == "123" else "99",
                    "getwindowname": "Mystical Ninja", "getwindowfocus": "999"}.get(args[0], "")
        with patch.dict(os.environ, {"XDG_SESSION_TYPE": "x11", "DISPLAY": ":0"}), \
             patch.object(state.shutil, "which", return_value="xdotool"), \
             patch.object(state, "_run_x11", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "Focused"):
                state._send_x11(11, ("0", "F7"))
        self.assertFalse(any(x[0] == "key" for x in calls))

    def test_x11_slot_and_hotkey(self):
        calls = []
        def fake(*args):
            calls.append(args)
            return {"search": "123", "getwindowpid": "11", "getwindowname": "Mystical Ninja",
                    "getwindowfocus": "123"}.get(args[0], "")
        with patch.dict(os.environ, {"XDG_SESSION_TYPE": "x11", "DISPLAY": ":0"}), \
             patch.object(state.shutil, "which", return_value="xdotool"), \
             patch.object(state, "_run_x11", side_effect=fake):
            state._send_x11(11, ("2", "F5"))
        self.assertEqual([x for x in calls if x[0] == "key"],
                         [("key", "--clearmodifiers", "2"), ("key", "--clearmodifiers", "F5")])

    def test_wayland_fail_closed(self):
        with patch.dict(os.environ, {"XDG_SESSION_TYPE": "wayland", "DISPLAY": ":0"}), \
             patch.object(state, "_run_x11") as send:
            with self.assertRaisesRegex(OSError, "Wayland"):
                state._send_x11(11, ("0", "F5"))
            send.assert_not_called()

    def test_bad_action_and_slot(self):
        with patch.object(state, "verified_emulator_pid", return_value=(11, "project64")), \
             patch.object(state, "_send_x11") as dispatch:
            with self.assertRaises(ValueError):
                state.send_state_command(11, "project64", "load", 11)
            with self.assertRaises(ValueError):
                state.send_state_command(11, "project64", "reset", 0)
            dispatch.assert_not_called()

if __name__ == "__main__":
    unittest.main()
