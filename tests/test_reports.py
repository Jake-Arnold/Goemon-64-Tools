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
        self.assertEqual(reports.readable_report_name(
            "First Memory Test - Ryo Known"), "First Memory Test - Ryo Known")
        self.assertEqual(reports.readable_report_name("Sasuke: XYZ/health?"),
                         "Sasuke - XYZ - health")
        self.assertEqual(reports.readable_report_name("CON"), "Report - CON")
        self.assertEqual(reports.readable_report_name("../"), "Untitled investigation")
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
            self.assertEqual(folder.parent.parent.name, "JP")
            self.assertEqual(folder.parent.name, "Sasuke movement")
            self.assertEqual(folder.name, "2026-11-16 18-15-00 UTC")
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
            self.assertEqual(a.parent.parent.name, "USA")
            self.assertEqual(c.parent.parent.name, "JP")
            self.assertEqual(a.parent.name, "Health changes")
            self.assertEqual(a.parent, b.parent)
            with self.assertRaises(ValueError):
                reports.create_value_search_report(region="../../etc", **args)
            with self.assertRaises(ValueError):
                reports.create_value_search_report(
                    region="usa", **{**args, "rows": [{}]})


    def test_same_timestamp_gets_a_readable_collision_suffix(self):
        with TemporaryDirectory() as tmp:
            when = datetime(2026, 11, 16, 18, 30, 43,
                            tzinfo=timezone.utc)
            kwargs = dict(region="japan", title="First Memory Test - Ryo Known",
                          rows=[], total_count=0, value_type="u16",
                          sample_count=11, timestamp=when, root=tmp)
            a = reports.create_value_search_report(**kwargs)
            b = reports.create_value_search_report(**kwargs)
            self.assertEqual(a.name, "2026-11-16 18-30-43 UTC")
            self.assertEqual(b.name, "2026-11-16 18-30-43 UTC (2)")
            self.assertEqual(a.parent.name, "First Memory Test - Ryo Known")
            self.assertEqual(len(reports.list_reports(
                root=tmp, legacy_dir=Path(tmp) / "unused")), 2)

    def test_previous_flat_reports_stay_visible_and_can_be_tided_explicitly(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "Reports"
            original = root / "JP" / "2026-11-16_183043Z__ryo__fe026609"
            original.mkdir(parents=True)
            content = "# This existing report must remain unchanged\n"
            (original / "summary.md").write_text(content)
            (original / "manifest.json").write_text(json.dumps({
                "schema": reports.SCHEMA, "region": "JP",
                "kind": "value-search",
                "title": "First Memory Test - Ryo Known",
                "candidate_total": 1,
                "created_utc": "2026-11-16T18:30:43.975041Z"}))
            first_index = reports.list_reports(root=root,
                        legacy_dir=root / "unknown")
            self.assertEqual(first_index[0].path, original)
            self.assertTrue(original.exists())  # Listing never modifies files.
            moved = reports.organise_report_folder(original, root=root)
            self.assertFalse(original.exists())
            self.assertEqual(moved.parent.name,
                             "First Memory Test - Ryo Known")
            self.assertEqual(moved.name, "2026-11-16 18-30-43 UTC")
            self.assertEqual((moved / "summary.md").read_text(), content)
            self.assertEqual(
                reports.organise_report_folder(moved, root=root), moved)
            items = reports.list_reports(root=root, legacy_dir=root / "unknown")
            self.assertEqual([item.path for item in items], [moved])

    def test_folder_organiser_rejects_outside_region_and_bad_manifest(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "reports"
            other = Path(tmp) / "other"
            other.mkdir()
            (other / "manifest.json").write_text(json.dumps({
                "schema": reports.SCHEMA, "region": "JP",
                "title": "Test", "created_utc": "2026-11-16T18:30:43Z"}))
            with self.assertRaises(ValueError):
                reports.organise_report_folder(other, root=root)

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
