"""ROM-free tests for canonical proof/inventory context (not retired G64 plans)."""
from __future__ import annotations

import copy
import io
import unittest
from contextlib import redirect_stdout

from decomp import skill_context as sc


class ProofContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sc.load()

    def test_stored_proof_and_inventory_consistent(self):
        self.assertEqual(sc.validate(self.data), [])

    def test_no_historical_task_packets_in_context(self):
        self.assertEqual(set(self.data), {"proof"})
        self.assertNotIn("tasks", self.data)

    def test_all_original_functions_accounted_for(self):
        p = self.data["proof"]
        self.assertEqual(p["c_total"] + p["asm_total"], p["identified"])
        self.assertEqual(p["new_c"] + p["baseline_c"], p["c_total"])

    def test_wrong_rom_size_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["proof"]["rom_size"] -= 1
        self.assertTrue(sc.validate(data))

    def test_mismatched_count_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["proof"]["claimed"] += 1
        self.assertTrue(sc.validate(data))

    def test_mismatched_rom_sha1_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["proof"]["inventory_sha1"] = "0" * 40
        self.assertTrue(sc.validate(data))

    def test_false_full_rom_proof_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["proof"]["full_rom_match"] = False
        self.assertTrue(sc.validate(data))

    def test_malformed_numeric_field_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["proof"]["new_c"] = "unknown"
        self.assertTrue(sc.validate(data))

    def test_status_is_canonical_not_g64_task_scheduler(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(sc.main(["--status", "--json"]), 0)
        self.assertIn("published_canonical_proof", out.getvalue())
        self.assertNotIn("first_planned", out.getvalue())

    def test_validate_cli(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(sc.main(["--validate"]), 0)
        self.assertIn("CONSISTENT_STORED_REPORTS", out.getvalue())


if __name__ == "__main__":
    unittest.main()
