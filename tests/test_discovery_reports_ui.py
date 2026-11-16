"""Unified discovery report from the automatic damage workflow, synthetic RAM."""
from argparse import Namespace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.damage_event_capture import DamageRecorder
from tests.test_damage_event_capture import FakeMemory, take_hit


class DiscoveryReportUiTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")
        self.root.withdraw()
        self.app = Toolkit(self.root, Namespace(
            pid=None, base=None, endian='auto', route=None,
            enable_teleport=True, enable_state_restore=True,
            enable_debug_menu=True, enable_hex_edit=True,
            enable_scene_warp=False, read_only=True, game_version='usa'))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for item in self.root.tk.call("after", "info"):
                self.root.after_cancel(item)
            self.root.destroy()
        except tk.TclError:
            pass

    def test_damage_capture_writes_standard_evidence_files(self):
        app = self.app
        ram = FakeMemory()
        recorder = DamageRecorder(ram)
        take_hit(recorder, ram, 0)
        recorder.stop()
        app.damage_recorder = recorder
        app.damage_capture_worker = None
        app.damage_report_name.set("Damage after hitting Goemon")
        with TemporaryDirectory() as tmp:
            with patch("practice.reports.reports_root",
                       return_value=Path(tmp)):
                app.export_damage_capture()
            paths = list(Path(tmp).glob("USA/*/*/manifest.json"))
            self.assertEqual(len(paths), 1)
            folder = paths[0].parent
            self.assertEqual({p.name for p in folder.iterdir()},
                             {"summary.md", "candidates.csv",
                              "session.json", "manifest.json"})
            manifest = json.loads((folder / "manifest.json").read_text())
            evidence = json.loads((folder / "session.json").read_text())
            self.assertEqual(manifest["kind"], "damage-events")
            self.assertEqual(manifest["region"], "USA")
            self.assertEqual(manifest["candidate_exported"],
                             len(evidence["candidates"]))
            self.assertEqual(evidence["evidence"]["source_report"]["event_count"], 1)
            self.assertTrue(evidence["evidence"]["source_report"]["candidates"])
            self.assertIn("Saved", app.damage_capture_status.get())


if __name__ == "__main__":
    unittest.main()
