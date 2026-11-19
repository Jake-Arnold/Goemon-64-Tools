"""Tests for source-only USA camera 136-byte scratch proof (ROM optional)."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT/"decomp/results/camera_reset_136_scratch_proof_20261117.json"
SOURCE = ROOT/"decomp/research/camera_reset_usa_5b56e4.c"

class CameraResetScratchProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof = json.loads(PROOF.read_text(encoding="utf-8"))

    def test_source_hash_and_stable_function(self):
        function = self.proof["function"]
        self.assertEqual(function["name"], "func_801F97D4_5B56E4")
        self.assertEqual(function["size"], 0x88)
        self.assertEqual(function["rom_start"], "0x5B56E4")
        self.assertEqual(function["rom_end"], "0x5B576C")
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), function["source_sha256"])

    def test_scratch_gate_metadata_and_no_false_production_claim(self):
        d = self.proof
        self.assertEqual(d["status"], "PASS_SCRATCH_NOT_CENTRAL_G2")
        self.assertEqual(d["canonical_343_candidate_g2"], "NOT_RUN")
        self.assertEqual(d["production_baseline_verified_C"], 342)
        self.assertEqual(d["full_rom_bytes_equal"], 33554432)
        self.assertEqual((d["file11_original_relocations"],d["file11_candidate_relocations"]), (8825,8825))
        self.assertTrue(d["relocation_multiset_equal"])
        self.assertEqual((d["original_function_entries"],d["candidate_function_entries"]), (7376,7376))
        self.assertTrue(d["all_original_function_names_vmas_sizes_preserved"])
        self.assertEqual(sum(d["scratch_objects_original_sizes"].values()), 0x5B8500-0x587370)

    def test_optional_original_usa_slice(self):
        rom_path = os.environ.get("GOEMON_USA_DECOMPRESSED_ROM")
        if not rom_path:
            self.skipTest("Set GOEMON_USA_DECOMPRESSED_ROM to authenticate original bytes")
        raw = Path(rom_path).read_bytes()
        self.assertEqual(len(raw),33554432)
        self.assertEqual(hashlib.sha1(raw).hexdigest(),self.proof["decompressed_usa_rom_sha1"])
        fn=self.proof["function"]
        self.assertEqual(hashlib.sha256(raw[int(fn["rom_start"],16):int(fn["rom_end"],16)]).hexdigest(),fn["original_and_compiled_bytes_sha256"])

if __name__ == "__main__":
    unittest.main()
