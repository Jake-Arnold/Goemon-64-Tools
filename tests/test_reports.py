"""Portable report writer/index regression tests, without ROM or GUI."""
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from practice import reports


class ReportTests(unittest.TestCase):
    def test_safe_names_and_platform_documents(self):
        self.assertEqual(reports.safe_slug("Sasuke: Position? / JP"),
                         "sasuke-position-jp")
        self.assertEqual(reports.safe_slug("../\\<>"), "research")
        with TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(
                reports.documents_dir(platform_name="linux", home=home,
                                      environ={"XDG_DOCUMENTS_DIR": "$HOME/Notes"}),
                home / "Notes")
            self.assertEqual(
                reports.documents_dir(platform_name="win32", home=home,
                                      environ={"USERPROFILE": tmp}),
                home / "Documents")

    def test_save_index_and_export_with_truncation(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Reports"
            folder = reports.create_value_search_report(
                region="japan", title="Sasuke movement",
                rows=[{"address": "0x80151B10", "kind": "f32",
                       "value": "10.25", "hex": "41240000"}],
                total_count=500, value_type="f32", sample_count=3,
                timestamp=datetime(2026, 11, 16, 18, 15,
                                   tzinfo=timezone.utc), root=root)
            self.assertEqual(folder.parent.name, "JP")
            self.assertRegex(
                folder.name,
                r"^2026-11-16_181500Z__sasuke-movement__[a-f0-9]{8}$")
            data = json.loads((folder / "manifest.json").read_text())
            self.assertTrue(data["candidate_truncated"])
            self.assertEqual(data["candidate_exported"], 1)
            self.assertFalse(data["instruction_access_tracing"])
            self.assertIn("Only the displayed candidate",
                          (folder / "summary.md").read_text())
            entries = reports.list_reports(root=root,
                                           legacy_dir=Path(tmp) / "missing")
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].path, folder)
            with ZipFile(reports.export_report_zip(folder)) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {folder.name + "/" + name for name in (
                        "manifest.json", "summary.md",
                        "session.json", "candidates.csv")})

    def test_unique_names_region_isolation_and_bad_input(self):
        with TemporaryDirectory() as tmp:
            args = dict(title="Health changes", rows=[], total_count=0,
                        value_type="u8", sample_count=1, root=tmp)
            a = reports.create_value_search_report(region="usa", **args)
            b = reports.create_value_search_report(region="usa", **args)
            c = reports.create_value_search_report(region="japan", **args)
            self.assertNotEqual(a, b)
            self.assertEqual(a.parent.name, "USA")
            self.assertEqual(c.parent.name, "JP")
            with self.assertRaises(ValueError):
                reports.create_value_search_report(region="../../etc", **args)
            with self.assertRaises(ValueError):
                reports.create_value_search_report(
                    region="usa", **{**args, "rows": [{}]})

    def test_legacy_read_only_and_ignore_incomplete(self):
        with TemporaryDirectory() as tmp:
            legacy = Path(tmp) / "old"
            legacy.mkdir()
            original = legacy / "inspect_20261115.json"
            original.write_text('{"original": 1}')
            incomplete = Path(tmp) / "new" / "USA" / "missing-manifest"
            incomplete.mkdir(parents=True)
            (incomplete / "session.json").write_text("{}")
            entries = reports.list_reports(
                root=Path(tmp) / "new", legacy_dir=legacy)
            self.assertEqual(len(entries), 1)
            self.assertTrue(entries[0].legacy)
            self.assertEqual(original.read_text(), '{"original": 1}')

    def test_linux_file_manager_launch(self):
        with TemporaryDirectory() as tmp:
            with patch.object(reports.sys, "platform", "linux"), \
                 patch.object(reports.subprocess, "Popen") as popen:
                reports.open_in_file_manager(tmp)
            popen.assert_called_once_with(["xdg-open", tmp],
                                          start_new_session=True)


if __name__ == "__main__":
    unittest.main()
