"""ROM-free guardrails for consolidated cross-region C candidates."""
import copy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from decomp import candidate_registry as cr


class CandidateRegistryTests(unittest.TestCase):
    def setUp(self):
        self.scratch = TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "decomp/data").mkdir(parents=True)
        (self.root / "decomp/results").mkdir()
        (self.root / "decomp/regions").mkdir()
        (self.root / "decomp/research").mkdir()
        self.source_path = "decomp/research/candidate.c"
        source = b"void func_80001000_3000(void) {}\nvoid func_80001010_3010(void) {}\n"
        (self.root / self.source_path).write_bytes(source)
        self.source = {"path": self.source_path, "git_blob_sha": cr.git_blob_sha(source)}
        (self.root / "decomp/results/inventory.json").write_text(json.dumps({"summary":{"newly_matching_c":720}}))
        (self.root / "decomp/regions/japan_0.json").write_text(json.dumps({"units":[{"functions":[{}]*34}]}))
        self.inventory = []
        for n in range(1, 1312):
            self.inventory.append({
                "File": f"file_{n}",
                "Segment classification": "Executable: static overlay" if n == 11 else "Empty slot",
                "USA expanded ROM offset": "0x00003000" if n == 11 else "0x00001000",
                "USA expanded bytes": "4096" if n == 11 else "0",
                "Japan expanded ROM offset": "0x00003000" if n == 11 else "0x00001000",
                "Japan expanded bytes": "4096" if n == 11 else "0",
            })
        self.record = {
            "region": "usa", "segment": "file_11", "name": "func_80001000_3000",
            "rom_offset": "0x3000", "vma": "0x80001000", "size": 16,
            "original_code_sha256": hashlib.sha256(bytes(16)).hexdigest(),
            "status": "RESEARCH_ONLY", "canonical_g2": "NOT_RUN",
            "source": self.source, "provenance": ["PR #23"],
        }
        self.registry = {
            "format": "goemon-candidate-registry-v1",
            "accepted_baseline": {"usa_functions": 720, "japan_0_functions": 34},
            "expected_pending": {"usa_functions": 1, "usa_bytes": 16,
                                 "japan_0_functions": 0, "japan_0_bytes": 0},
            "candidates": [self.record],
        }

    def test_valid_metadata_and_source_git_identity(self):
        result = cr.validate(self.root, self.registry, self.inventory)
        self.assertEqual(result["functions"], {"usa": 1})
        self.assertEqual(result["groups"], {"usa/file_11": 1})
        self.assertEqual(result["source_files_checked"], 1)

    def test_reject_source_drift_and_fake_promotion(self):
        (self.root / self.source_path).write_text("void func_80001000_3000(){}")
        with self.assertRaisesRegex(cr.RegistryError, "source drift"):
            cr.validate(self.root, self.registry, self.inventory)
        (self.root / self.source_path).write_bytes(b"void func_80001000_3000(void) {}\nvoid func_80001010_3010(void) {}\n")
        wrong = copy.deepcopy(self.registry)
        wrong["candidates"][0]["status"] = "PROMOTED"
        with self.assertRaisesRegex(cr.RegistryError, "unverified promotion"):
            cr.validate(self.root, wrong, self.inventory)

    def test_reject_duplicate_and_overlapping_original_ranges(self):
        wrong = copy.deepcopy(self.registry)
        wrong["candidates"].append(copy.deepcopy(self.record))
        with self.assertRaisesRegex(cr.RegistryError, "duplicate"):
            cr.validate(self.root, wrong, self.inventory)
        wrong["candidates"][1]["rom_offset"] = "0x3010"
        wrong["candidates"][1]["name"] = "func_80001010_3010"
        wrong["candidates"][1]["vma"] = "0x80001010"
        wrong["candidates"][0]["size"] = 32
        wrong["expected_pending"] = {"usa_functions": 2, "usa_bytes": 48,
                                     "japan_0_functions": 0, "japan_0_bytes": 0}
        with self.assertRaisesRegex(cr.RegistryError, "overlapping"):
            cr.validate(self.root, wrong, self.inventory)

    def test_reject_crossing_overlay_and_symbol_mismatch(self):
        wrong = copy.deepcopy(self.registry)
        wrong["candidates"][0]["rom_offset"] = "0x3FFC"
        wrong["candidates"][0]["name"] = "func_80001000_3FFC"
        with self.assertRaisesRegex(cr.RegistryError, "outside"):
            cr.validate(self.root, wrong, self.inventory)
        wrong["candidates"][0]["rom_offset"] = "0x3000"
        with self.assertRaisesRegex(cr.RegistryError, "symbol/ROM-offset mismatch"):
            cr.validate(self.root, wrong, self.inventory)

    def test_reject_canonical_drift(self):
        (self.root / "decomp/results/inventory.json").write_text(json.dumps({"summary":{"newly_matching_c":721}}))
        with self.assertRaisesRegex(cr.RegistryError, "canonical inventory changed"):
            cr.validate(self.root, self.registry, self.inventory)

    def test_reject_wrong_original_image_and_hash(self):
        image = self.root / "wrong.z64"
        image.write_bytes(b"not a 32 MiB original")
        with self.assertRaisesRegex(cr.RegistryError, "wrong original"):
            cr.verify_original_images(self.registry, {"usa": image})

    def test_reject_unsupported_numbered_data_as_code(self):
        wrong = copy.deepcopy(self.registry)
        wrong["candidates"][0]["segment"] = "file_100"
        with self.assertRaisesRegex(cr.RegistryError, "outside"):
            cr.validate(self.root, wrong, self.inventory)


if __name__ == "__main__":
    unittest.main()
