"""Metadata-only decomp bridge must preserve conflicting evidence."""
import json
import unittest

from practice.address_catalogue import DISCOVERIES
from scripts.import_decomp_address_manifest import import_upstream


class DecompMetadataSyncTests(unittest.TestCase):
    def setUp(self):
        self.local = json.loads(DISCOVERIES.read_text(encoding="utf-8"))
        self.example = next(
            r for r in self.local["entries"]
            if r["id"] == "research:vm_text_stream_cursor")

    def envelope(self, entries):
        return {
            "format": "goemon-address-discoveries-v1",
            "version": 1,
            "entries": entries,
        }

    def test_same_address_evidence_merges_without_upgrading_confidence(self):
        observed = dict(self.example)
        observed["source"] = "decomp/VM_RUNTIME_CURSOR_FIELD_REPORT.md"
        observed["confidence"] = "user-confirmed"
        observed["evidence"] = "Additional reader trace, still research"
        result, change = import_upstream(
            self.local, self.envelope([observed]),
            upstream_revision="abcde1234567")
        old = next(
            r for r in result["entries"] if r["id"] == observed["id"])
        self.assertEqual(old["confidence"], self.example["confidence"])
        self.assertIn("Additional reader trace", old["evidence"])
        self.assertEqual(change["updated"], 1)
        self.assertEqual(change["added"], 0)

    def test_disputed_location_keeps_both_records(self):
        contradiction = dict(self.example)
        contradiction["source"] = "decomp/VM_RUNTIME_CURSOR_FIELD_REPORT.md"
        contradiction["address"] = "0x801C77EC"
        result, stats = import_upstream(
            self.local, self.envelope([contradiction]),
            upstream_revision="abcd1234")
        primary = next(
            r for r in result["entries"] if r["id"] == self.example["id"])
        self.assertEqual(primary["address"], self.example["address"])
        disputes = [r for r in result["entries"]
                    if r["id"].startswith("decomp:conflict:")]
        self.assertEqual(len(disputes), 1)
        self.assertEqual(disputes[0]["confidence"], "disputed")
        self.assertFalse(disputes[0]["live_readable"])
        self.assertEqual(stats["disputed"], 1)

    def test_decomp_may_not_override_builtin_unlock_ids(self):
        bad = dict(self.example)
        bad["id"] = "unlock:usa:mini_ebisumaru"
        bad["source"] = "decomp/VM_RUNTIME_CURSOR_FIELD_REPORT.md"
        with self.assertRaisesRegex(ValueError, "only decomp:/research:"):
            import_upstream(
                self.local, self.envelope([bad]),
                upstream_revision="abcde1234")

    def test_decomp_manifest_requires_decomp_source(self):
        bad = dict(self.example)
        bad["source"] = "practice/unauthorised.py"
        with self.assertRaisesRegex(ValueError, "decomp/ source"):
            import_upstream(
                self.local, self.envelope([bad]),
                upstream_revision="abcde1234")


if __name__ == "__main__":
    unittest.main()
