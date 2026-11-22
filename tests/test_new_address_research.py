"""Imported research must not silently become writable gameplay metadata."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "practice" / "data"

class ImportedAddressResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = json.loads((ROOT / "address_catalogue_v1.json").read_text())
        cls.discoveries = json.loads((ROOT / "address_discoveries_v1.json").read_text())
        cls.audit = json.loads((ROOT / "address_catalogue_audit.json").read_text())
        cls.rows = {r["id"]: r for r in cls.catalogue["entries"]}
        cls.notes = {r["id"]: r for r in cls.discoveries["entries"]}

    def test_counts_and_audit(self):
        self.assertGreaterEqual(len(self.rows), 615)
        self.assertGreaterEqual(len(self.notes), 117)
        self.assertEqual(self.audit["total_records"], len(self.rows))
        self.assertGreater(self.audit["research_only"], 0)

    def test_new_research_has_no_authorised_writes(self):
        for key in ("research:jp_vm_lookup_table_native_20261121",
                    "research:glitch_pause_phase_byte_jp",
                    "research:dialogue_grant_chain_pipe_jp",
                    "research:dialogue_grant_chain_pipe_us"):
            with self.subTest(key=key):
                row = self.rows[key]
                self.assertEqual(row["confidence"], "research_observed")
                self.assertIsNone(row["control"])
                self.assertIs(row["live_readable"], False)
                self.assertTrue(row["source_revision"])
                self.assertTrue(row["sources"])

    def test_pause_stays_disputed(self):
        pause = self.rows["crosswalk:japan:static:pause_byte"]
        self.assertEqual(pause["confidence"], "disputed")
        self.assertIn("NOT verified", pause["name"])

    def test_conflict_stays_disputed(self):
        note = self.notes["decomp:conflict:research:vm_active_countdown:41dc7404e23a:801c77f8"]
        self.assertEqual(note["confidence"], "disputed")
        self.assertIsNone(note["control"])
        self.assertIs(note["live_readable"], False)

if __name__ == "__main__":
    unittest.main()
