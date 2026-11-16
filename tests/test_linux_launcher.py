"""ROM-free tests for Ubuntu dock identity and the unified Linux launcher."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import os
import shutil
import subprocess
import sys
import tkinter as tk

from scripts.install_linux_launcher import APP_ID, WINDOW_CLASS, install


class LinuxLauncherTests(unittest.TestCase):
    def test_installs_actual_png_and_stable_gnome_desktop_entry(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Goemon Tools with spaces"
            (root / "assets").mkdir(parents=True)
            (root / "Run-Linux.sh").write_text("#!/bin/sh\n", encoding="utf-8")
            icon = bytes.fromhex("89504e470d0a1a0a") + b"PNG-IMAGE"
            (root / "assets" / "goemon_tools_logo.png").write_bytes(icon)
            data = Path(tmp) / "xdg-user-data"
            desktop = install(repo_root=root, data_home=data)
            self.assertEqual(desktop, data / "applications" / f"{APP_ID}.desktop")
            contents = desktop.read_text(encoding="utf-8")
            self.assertIn("Name=Goemon Practice Toolkit", contents)
            self.assertIn(f"StartupWMClass={WINDOW_CLASS}", contents)
            self.assertEqual(APP_ID, WINDOW_CLASS)
            self.assertIn(f"Icon={data / 'icons' / (APP_ID + '.png')}", contents)
            self.assertIn('Exec=/usr/bin/env bash "', contents)
            self.assertIn(str(root / "Run-Linux.sh"), contents)
            self.assertNotIn("--game-version", contents)
            self.assertNotIn("--read-only", contents)
            self.assertEqual((data / "icons" / (APP_ID + ".png")).read_bytes(),
                             icon)
            self.assertEqual(desktop.stat().st_mode & 0o777, 0o644)
            # Re-running the installer is idempotent, and does not multiply apps.
            self.assertEqual(install(repo_root=root, data_home=data), desktop)

    def test_rejects_missing_logo_or_launcher(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(FileNotFoundError):
                install(repo_root=root, data_home=root / "xdg")
            (root / "Run-Linux.sh").write_text("echo toolkit\n")
            (root / "assets").mkdir()
            (root / "assets" / "goemon_tools_logo.png").write_bytes(b"bad")
            with self.assertRaisesRegex(ValueError, "PNG"):
                install(repo_root=root, data_home=root / "xdg")

    def test_native_tk_class_matches_desktop_launcher(self):
        source = (Path(__file__).resolve().parents[1] /
                  "practice" / "toolkit.py").read_text(encoding="utf-8")
        self.assertIn(f"tk.Tk(className='{WINDOW_CLASS}')", source)


    @unittest.skipUnless(sys.platform == "linux" and os.environ.get("DISPLAY")
                         and shutil.which("xprop"), "Requires Linux X11 and xprop")
    def test_real_tk_x11_window_instance_matches_installed_desktop_id(self):
        """Verify actual Tk WM_CLASS through X11 rather than assuming case."""
        try:
            root = tk.Tk(className=WINDOW_CLASS)
        except tk.TclError as exc:
            self.skipTest(str(exc))
        try:
            root.title("Goemon Practice Toolkit Dock Identity Smoke Test")
            root.update()
            result = subprocess.run(
                ["xprop", "-name", "Goemon Practice Toolkit Dock Identity Smoke Test",
                 "WM_CLASS"], capture_output=True, text=True, timeout=5, check=True)
            self.assertIn('"' + APP_ID + '"', result.stdout, result.stdout)
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
