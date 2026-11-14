"""Schema and provenance checks for external, UNVERIFIED USA cheat/actor leads.

No runtime memory reads or writes are performed.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research" / "usa_external_memory_leads.json"


class ExternalUSAValueLeadsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_sources_are_region_scoped_and_unverified(self):
        self.assertEqual(self.data["region"], "usa-ng5e-rev0")
        self.assertIn("tcrf_notes", self.data["sources"])
        self.assertIn("tcrf_main", self.data["sources"])
        self.assertIn("gamehacking_usa", self.data["sources"])
        for entry in self.data["new_usa_address_leads"]:
            self.assertEqual(entry["status"], "EXTERNAL_UNVERIFIED")
            self.assertIn(entry["source"], self.data["sources"])

    def test_no_duplicate_or_previously_mapped_addresses(self):
        entries = self.data["new_usa_address_leads"]
        addresses = [x["address"] for x in entries]
        self.assertEqual(len(addresses), len(set(addresses)))
        self.assertFalse(set(addresses) & set(self.data["previously_known_usa_excluded"]))
        self.assertEqual(len(entries), 25)
        self.assertTrue(all(x.startswith(("0x80", "0xA0")) and len(x) == 10
                            for x in addresses))

    def test_actor_ids_unique_and_source_only(self):
        actors = self.data["external_actor_ids"]
        ids = [x["actor_id"] for x in actors]
        self.assertEqual(len(actors), 47)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(next(x["label"] for x in actors
                              if x["actor_id"] == "0x0193"), "Key")
        self.assertTrue(all(x["status"] == "EXTERNAL_UNVERIFIED" for x in actors))

    def test_tcrf_japanese_debug_offsets_not_global_translation(self):
        rows = self.data["regional_debug_codes"]
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(int(row["japan"], 16) - int(row["usa"], 16), 0x57F0)
            self.assertEqual(row["offset"], "0x57F0")
        self.assertTrue(rows[0]["already_mapped_in_usa"])
        self.assertFalse(rows[1]["already_mapped_in_usa"])

    def test_raw_codes_preserved_without_auto_enabling(self):
        by_address = {e["address"]: e for e in self.data["new_usa_address_leads"]}
        self.assertEqual(by_address["0x8015C8B7"]["raw_codes"],
                         ["50000B04 0000", "8015C8B7 0001"])
        self.assertIn("81204156 ????", by_address["0x80204156"]["raw_codes"])
        self.assertIn("D00C7D3B 0020", by_address["0x800C7D3B"]["raw_codes"])


if __name__ == "__main__":
    unittest.main()
