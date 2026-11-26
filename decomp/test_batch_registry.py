"""ROM-free tests and fail-closed negative controls for decomp.batch_registry."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from decomp import batch_registry as regmod


class BatchRegistryTests(unittest.TestCase):
    def test_live_registry_validates_cleanly(self):
        reg = regmod.load_registry()
        self.assertEqual(reg["format"], regmod.FORMAT)
        self.assertEqual(reg["base_stage"], "promo36_promotion")
        usa_c, usa_b, usa_rem = regmod.expected_totals("usa")
        jp_c, jp_b, jp_rem = regmod.expected_totals("japan_0")
        self.assertGreaterEqual(usa_c, 3087)
        self.assertGreaterEqual(usa_b, 212412)
        self.assertEqual(usa_c + 13 + usa_rem, 7376)
        self.assertGreaterEqual(jp_c, 3019)
        self.assertGreaterEqual(jp_b, 202176)
        self.assertEqual(jp_c + jp_rem, 7376)
        self.assertEqual(regmod.validate_jp()["status"], "PASS")

    def test_duplicate_batch_id_or_namespace_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "batches").mkdir()
            reg = regmod.load_registry()
            bad = copy.deepcopy(reg)
            bad["batches"] = [
                {"id": "dup_batch", "namespace": "ns1", "usa": {}},
                {"id": "dup_batch", "namespace": "ns2", "usa": {}},
            ]
            (root / "batches/registry.json").write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                regmod.load_registry(root)

            bad2 = copy.deepcopy(reg)
            bad2["batches"] = [
                {"id": "batch_a", "namespace": "same_ns", "usa": {}},
                {"id": "batch_b", "namespace": "same_ns", "usa": {}},
            ]
            (root / "batches/registry.json").write_text(json.dumps(bad2))
            with self.assertRaises(ValueError):
                regmod.load_registry(root)

    def test_base_count_drift_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "batches").mkdir()
            bad = copy.deepcopy(regmod.load_registry())
            bad["base_usa"]["accepted_C"] = 9999
            (root / "batches/registry.json").write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                regmod.load_registry(root)


if __name__ == "__main__":
    unittest.main()
