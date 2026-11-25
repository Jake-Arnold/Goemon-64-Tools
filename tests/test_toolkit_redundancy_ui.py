"""Regressions for removing duplicate JP diagnostics/ROM controls.

The hidden Japanese model continues supplying typed watches and guarded XYZ
controller state; users see only shared Live Memory and Scene Browser.
"""
from __future__ import annotations

from argparse import Namespace
import tkinter as tk
import unittest
from unittest.mock import patch
from pathlib import Path

from practice.toolkit import Toolkit


class RedundancyUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")
        self.root.withdraw()
        self.rom = patch("practice.toolkit.load_remembered_rom", return_value=None)
        self.rom.start()
        self.addCleanup(self.rom.stop)
        self.app = Toolkit(self.root, Namespace(
            pid=None, base=None, endian='auto', route=None,
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, game_version='usa', read_only=False))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for after in self.root.tk.call("after", "info"):
                self.root.after_cancel(after)
            if self.root.winfo_exists():
                self.root.destroy()
        except tk.TclError:
            pass

    def test_diagnostics_tab_hidden_but_shared_live_and_scene_remain(self):
        app = self.app
        self.assertFalse(hasattr(app, 'jp_fields_tab'))
        self.assertFalse(hasattr(app, "verify_rom_button"))
        app.game_version_choice.set("Japan - Ganbare Goemon")
        app.on_game_version_changed()
        self.assertFalse(hasattr(app, 'jp_fields_tab'))
        self.assertEqual(app.notebook.tab(app.live_memory_tab, "state"), "normal")
        self.assertEqual(app.notebook.tab(app.scene_tab, "state"), "normal")
        self.assertTrue(app.jp_scene_position_frame.winfo_manager())
        self.assertIn("Japan", app.jp_scene_position_frame.cget("text"))
        self.assertIn("Click Connect", app.status.get())
        app.game_version_choice.set("USA - Mystical Ninja")
        app.on_game_version_changed()
        self.assertFalse(app.jp_scene_position_frame.winfo_manager())
        self.assertFalse(hasattr(app, 'jp_fields_tab'))

    def test_initial_japan_connect_requests_rom_once_in_same_flow(self):
        app = self.app
        app.game_version_choice.set("Japan - Ganbare Goemon")
        app.on_game_version_changed()
        self.assertIsNone(app.verified_rom_path)
        with patch("practice.toolkit.filedialog.askopenfilename",
                   return_value="") as pick:
            app._connect_japan_emulator()
        pick.assert_called_once()
        self.assertIsNone(app.jp_rdram)
        self.assertFalse(app._connecting)
        self.assertIn("cancelled", app.status.get())

    def test_rom_matching_is_still_mandatory_and_path_remembered(self):
        app = self.app
        app.game_version_choice.set("Japan - Ganbare Goemon")
        app.on_game_version_changed()
        with patch("practice.toolkit.filedialog.askopenfilename",
                   return_value="/tmp/japan0.z64"), patch(
                   "practice.toolkit.verify_selected_rom") as verify, patch(
                   "practice.toolkit.remember_verified_rom",
                   return_value=Path("/tmp/japan0.z64")) as remembered:
            verify.return_value = app.active_version
            self.assertTrue(app.verify_rom_for_version())
        verify.assert_called_once_with("/tmp/japan0.z64", "japan")
        remembered.assert_called_once_with("/tmp/japan0.z64", "japan")
        self.assertEqual(app.verified_rom_path, Path("/tmp/japan0.z64"))

    def test_failed_rom_select_never_arms_game(self):
        app = self.app
        app.game_version_choice.set("Japan - Ganbare Goemon")
        app.on_game_version_changed()
        with patch("practice.toolkit.filedialog.askopenfilename",
                   return_value="/tmp/not-jp-rom.n64"), patch(
                   "practice.toolkit.verify_selected_rom",
                   side_effect=ValueError("wrong hash")):
            app._connect_japan_emulator()
        self.assertFalse(app._connecting)
        self.assertIsNone(app.jp_rdram)
        self.assertIn("wrong hash", app.status.get())


if __name__ == "__main__":
    unittest.main()
