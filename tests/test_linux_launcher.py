"""ROM-free tests for Ubuntu dock identity and the unified Linux launcher."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

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


if __name__ == "__main__":
    unittest.main()
