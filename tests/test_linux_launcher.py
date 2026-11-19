"""ROM-free tests for Ubuntu dock identity and the unified Linux launcher."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import os
import re
import shutil
import subprocess
import sys
import tkinter as tk

from scripts.install_linux_launcher import APP_ID, WINDOW_CLASS, install


def matches_toolkit_wm_class(output: str) -> bool:
    """Tk's instance may gain ' #N'; its second WM_CLASS token is stable."""
    match = re.fullmatch(
        r'WM_CLASS\(STRING\)\s*=\s*"([^"]+)",\s*"([^"]+)"\s*',
        output.strip(),
    )
    if match is None:
        return False
    instance, app_class = match.groups()
    return (app_class == WINDOW_CLASS and
            (instance == APP_ID or
             re.fullmatch(re.escape(APP_ID) + r" #\d+", instance) is not None))


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
            self.assertEqual(WINDOW_CLASS, 'Goemon-practice-toolkit')
            self.assertNotEqual(APP_ID, WINDOW_CLASS)
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
        # Root creation now lives in the optional TkDND factory: checking
        # for a direct tk.Tk call in toolkit.py is obsolete.
        root_dir = Path(__file__).resolve().parents[1] / "practice"
        source = (root_dir / "toolkit.py").read_text(encoding="utf-8")
        dnd_source = (root_dir / "dialogue_dnd.py").read_text(encoding="utf-8")
        self.assertIn(f"make_toolkit_root(class_name='{APP_ID}')", source)
        self.assertIn("return tk.Tk(className=class_name)", dnd_source)
        self.assertIn("TkinterDnD.Tk(className=class_name)", dnd_source)

        # Assert the actual fallback factory forwards our desktop class.
        from unittest.mock import patch
        from practice.dialogue_dnd import make_toolkit_root
        with patch.dict(sys.modules, {'tkinterdnd2': None}):
            with patch('practice.dialogue_dnd.tk.Tk') as root_factory:
                self.assertIs(make_toolkit_root(class_name=APP_ID),
                              root_factory.return_value)
                root_factory.assert_called_once_with(className=APP_ID)
 
    def test_tk_class_accepts_numbered_instances_but_not_window_manager_frame(self):
        self.assertTrue(matches_toolkit_wm_class(
            'WM_CLASS(STRING) = "goemon-practice-toolkit", "Goemon-practice-toolkit"'))
        self.assertTrue(matches_toolkit_wm_class(
            'WM_CLASS(STRING) = "goemon-practice-toolkit #2", "Goemon-practice-toolkit"'))
        self.assertFalse(matches_toolkit_wm_class(
            'WM_CLASS(STRING) = "mutter-x11-frames", "mutter-x11-frames"'))
        self.assertFalse(matches_toolkit_wm_class(
            'WM_CLASS(STRING) = "other #2", "Goemon-practice-toolkit"'))
        self.assertFalse(matches_toolkit_wm_class(
            'WM_CLASS(STRING) = "goemon-practice-toolkit #2", "Wrong"'))

    @unittest.skipUnless(sys.platform == "linux" and os.environ.get("DISPLAY")
                         and shutil.which("xprop") and shutil.which("xwininfo"),
                         "Requires Linux X11, xprop and xwininfo")
    def test_real_tk_x11_window_instance_matches_installed_desktop_id(self):
        """Query the actual X11 Tk client, not a GNOME/Mutter title-matched frame.

        xprop -name can match mutter-x11-frames on GNOME, even when Tk's
        WM_CLASS is correct. Use a per-test unique window title to select
        the matching X window from the X11 hierarchy, then query its ID.
        """
        try:
            root = tk.Tk(className=APP_ID)
        except tk.TclError as exc:
            self.skipTest(str(exc))
        try:
            title = (f"Goemon Toolkit Dock Identity {os.getpid()}-"
                     f"{root.winfo_id():x}")
            root.title(title)
            root.update()
            tree = subprocess.run(
                ["xwininfo", "-root", "-tree"],
                capture_output=True, text=True, timeout=5, check=True)
            matches = []
            for line in tree.stdout.splitlines():
                if f'"{title}"' not in line:
                    continue
                window_id = re.match(r"\s*(0x[0-9a-fA-F]+)\b", line)
                if window_id is None:
                    continue
                result = subprocess.run(
                    ["xprop", "-id", window_id.group(1), "WM_CLASS"],
                    capture_output=True, text=True, timeout=5, check=True)
                matches.append(result.stdout)
            self.assertTrue(
                any(matches_toolkit_wm_class(output) for output in matches),
                "No toolkit X11 client had the expected WM_CLASS. "
                f"Title: {title!r}. Candidates: {matches!r}. "
                f"X11 tree: {tree.stdout[-3000:]}")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
