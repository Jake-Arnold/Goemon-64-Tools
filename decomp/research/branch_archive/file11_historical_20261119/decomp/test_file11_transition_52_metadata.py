"""ROM-free identity/claim-guard tests for file_11 two-callback scratch evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "research" / "file11_transition_pair.c"
EVIDENCE = ROOT / "results" / "file11_transition_52_scratch_proof_20261116.json"

class File11Transition52EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(EVIDENCE.read_text())

    def test_original_source_digest_is_pinned(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(),self.data["new_source_sha256"])

    def test_cross_region_entrypoints_are_distinct(self):
        c=SOURCE.read_text()
        for value in self.data["new_usa_function_names"]+self.data["new_japan_function_names"]:
            self.assertIn(value,c)
        self.assertIn("#ifdef GOEMON_USA",c)

    def test_52_consists_of_50_plus_two(self):
        self.assertEqual(self.data["existing_50_functions"]+self.data["additional_new_functions"],52)
        self.assertEqual(self.data["file11_c_code_bytes"],1120)
        self.assertEqual(self.data["file11_mixed_link_chunks"],14)
        self.assertEqual(self.data["identified_func_entries_before_and_after"],7376)

    def test_relocation_order_exception_is_not_hidden(self):
        self.assertEqual(self.data["file11_relocation_tuples_matching"],8825)
        self.assertIs(self.data["raw_relocation_order_identical"],False)
        self.assertEqual(self.data["known_three_record_cycle_starts"],[2506,6131])

    def test_no_new_formal_promotion_is_claimed(self):
        self.assertEqual(self.data["central_212_g2"],"not_run")
        self.assertIs(self.data["canonical_manifest_modified"],False)
        self.assertEqual(self.data["central_210_existing_g2"],"passed_on_pr20_branch_d394efe7")

if __name__ == "__main__":
    unittest.main()
