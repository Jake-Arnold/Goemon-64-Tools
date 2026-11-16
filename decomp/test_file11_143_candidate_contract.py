"""ROM-free validation of the pinned 143-function USA file_11 research snapshot.

The snapshot is only a source/ROM contract. This test never promotes C claims
and does not substitute for the original native compiler + central whole-ROM G2.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "research/file11_143_candidate/file11_143_source_fixture.json"
WAVE1 = ROOT / "results/file11_expansion_native_20261116.json"
PROOF = ROOT / "research/file11_143_candidate/reproduction_proof.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_UPSTREAM = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"


class File11143CandidateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.wave1 = json.loads(WAVE1.read_text(encoding="utf-8"))
        cls.proof = json.loads(PROOF.read_text(encoding="utf-8"))

    def test_snapshot_is_pinned_and_not_promoted(self):
        f = self.fixture
        self.assertEqual(f["format"], "goemon-file11-143-exact-staging-candidate-v1")
        self.assertEqual(f["upstream_commit"], EXPECTED_UPSTREAM)
        self.assertEqual(f["original_rom_sha1"], "6ea0ed71032ce08fc2745f412d84936382197494")
        self.assertEqual(f["original_elf_sha256"], "83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038")
        self.assertEqual(f["original_asm_sha256"], "e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b")
        self.assertEqual(f["file11_relocations"], 8825)
        self.assertEqual(f["rom_length"], 33554432)
        self.assertEqual(f["original_file11_stage_c_functions"], 50)
        self.assertEqual(f["wave1_research_functions_covered"], 77)
        self.assertEqual(f["wave45_additional_functions_beyond_wave1"], 16)
        self.assertEqual(f["total_represented_functions"], 143)
        self.assertEqual(f["new_covered_functions_beyond_existing_50"], 93)
        self.assertEqual(f["all_C_text_bytes"], 3908)
        self.assertIs(f["full_210_plus_research_g2_verified"], False)
        self.assertEqual(f["production_promotion_count"], 0)

    def test_complete_overlay_chunks_preserve_original_asm_gaps(self):
        f = self.fixture
        chunks = f["chunks"]
        self.assertEqual(len(chunks), 88)
        offset = f["overlay_text_start"]
        self.assertEqual(offset, 0x587370)
        counts = {"asm": 0, "c": 0}
        covered = {"asm": 0, "c": 0}
        for c in chunks:
            self.assertEqual(c["rom_start"], offset)
            self.assertEqual(c["rom_end"] - offset, c["size"])
            self.assertGreater(c["size"], 0)
            self.assertLessEqual(c["rom_end"], 0x5B8500)
            self.assertRegex(c["original_sha256"], HEX64)
            self.assertRegex(c["trimmed_obj_sha256"], HEX64)
            self.assertIn(c["kind"], counts)
            counts[c["kind"]] += 1
            covered[c["kind"]] += c["size"]
            if c["kind"] == "asm":
                self.assertIsNone(c["name"])
            else:
                self.assertIsInstance(c["name"], str)
                self.assertRegex(c["source_sha256"], HEX64)
            offset = c["rom_end"]
        self.assertEqual(offset, f["overlay_text_end"])
        self.assertEqual(offset, 0x5B8500)
        self.assertEqual(counts, {"asm": 44, "c": 44})
        self.assertEqual(covered["c"], 3908)

    def test_all_original_function_identities_are_disjoint(self):
        names, offsets = set(), set()
        count, size = 0, 0
        for chunk in self.fixture["chunks"]:
            if chunk["kind"] != "c":
                continue
            source = chunk["source"]
            self.assertNotIn("GLOBAL_ASM", source)
            self.assertNotIn("#include", source)
            self.assertEqual(hashlib.sha256(source.encode("utf-8")).hexdigest(), chunk["source_sha256"])
            off = chunk["rom_start"]
            for fn in chunk["functions"]:
                self.assertEqual(fn["off"], off)
                self.assertEqual(fn["vma"], 0x801CB460 + off - 0x587370)
                self.assertIn(fn["name"], source)
                self.assertGreater(fn["size"], 0)
                self.assertNotIn(fn["name"], names)
                self.assertNotIn(off, offsets)
                names.add(fn["name"])
                offsets.add(off)
                off += fn["size"]
                size += fn["size"]
                count += 1
            self.assertEqual(off, chunk["rom_end"])
        self.assertEqual((count, size), (143, 3908))

    def test_original_77_wave1_functions_reconciled_without_duplicates(self):
        wave1 = self.wave1["functions"]
        self.assertEqual(len(wave1), 77)
        self.assertEqual(sum(fn["size"] for fn in wave1), 2120)
        current = {fn["name"]: fn for c in self.fixture["chunks"] if c["kind"] == "c" for fn in c["functions"]}
        for fn in wave1:
            with self.subTest(name=fn["name"]):
                self.assertIn(fn["name"], current)
                self.assertEqual(current[fn["name"]]["off"], fn["rom_offset"])
                self.assertEqual(current[fn["name"]]["size"], fn["size"])
                self.assertEqual(current[fn["name"]]["vma"], fn["vma"])
        self.assertEqual(len(current) - len(wave1), 66)

    def test_research_proof_is_not_a_combined_production_gate(self):
        p = self.proof
        self.assertEqual(p["file11_c_functions_original_address_exact"], 143)
        self.assertEqual(p["additional_beyond_production_50"], 93)
        self.assertEqual(p["file11_original_C_instruction_bytes"], 3908)
        self.assertEqual(p["file11_relocation_records_original"], 8825)
        self.assertEqual(p["file11_relocation_records_candidate"], 8825)
        self.assertIs(p["whole_rom_byte_exact"], True)
        self.assertIs(p["semantic_relocations_match"], True)
        self.assertEqual(p["production_promotion_claims"], 0)
        self.assertIs(p["combined_210_plus_207_production_g2_ran"], False)


if __name__ == "__main__":
    unittest.main()
