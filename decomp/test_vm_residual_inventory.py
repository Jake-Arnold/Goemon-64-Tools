import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "decomp" / "results" / "vm_residual_inventory.json"


class VmResidualInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text())
        cls.manifest = json.loads((ROOT / "decomp" / "manifest.json").read_text())
        cls.unit = next(
            unit for unit in cls.manifest["units"] if unit["source"] == "script_vm.c"
        )

    def test_inventory_is_the_complete_live_assembly_list_in_order(self):
        entries = self.ledger["residual_functions"]
        self.assertEqual(self.ledger["scope"]["residual_count"], 13)
        self.assertEqual(len(entries), 13)
        self.assertEqual(
            [entry["symbol"] for entry in entries], self.unit["assembly_functions"]
        )
        self.assertEqual(len({entry["symbol"] for entry in entries}), 13)
        self.assertTrue(all(entry["production_owner"] == "GLOBAL_ASM" for entry in entries))

    def test_original_extents_and_blockers_are_complete(self):
        expected_exactness = {
            "ISOLATED_NONMATCH",
            "UNIT_NONMATCH",
            "NO_C_CANDIDATE",
            "EXTENT_ONLY_NO_C_BODY",
        }
        for entry in self.ledger["residual_functions"]:
            with self.subTest(symbol=entry["symbol"]):
                self.assertGreater(entry["original_bytes"], 0)
                self.assertEqual(entry["original_bytes"] % 4, 0)
                self.assertEqual(
                    int(entry["rom_offset"], 16), int(entry["vma"], 16) - 0x7FFFF400
                )
                self.assertEqual(len(entry["original_instruction_sha256"]), 64)
                self.assertIn(entry["exactness"], expected_exactness)
                self.assertTrue(entry["concrete_blocker"].strip())
                self.assertTrue(entry["next_unblock_condition"].strip())
                self.assertTrue(entry["evidence"])
                for evidence in entry["evidence"]:
                    self.assertTrue((ROOT / evidence).is_file(), evidence)

    def test_current_source_and_whole_project_proof_fingerprints(self):
        sources = self.ledger["current_sources"]
        # The VM ledger preserves the exact historical 2090-C manifest, proof
        # and inventory. Verify that immutable predecessor without weakening the
        # current 2092-C canonical proof/inventory (checked by promotion_integrity).
        for field in ("production_source", "header"):
            path = ROOT / sources[field]
            self.assertTrue(path.is_file())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, sources[f"{field.split('/')[-1].split('.')[0]}_sha256"])
        self.assertTrue((ROOT / sources["verifier"]).is_file())
        current = json.loads((ROOT / "decomp/manifest.json").read_text())
        self.assertIn("overlay_usa_opening_new2_stage", current)
        historical = {k:v for k,v in current.items() if k not in ("overlay_usa_opening_new2_stage", "overlay_usa_short72_stage", "usa_script_vm436_promotion", "usa_native151_promotion", "usa_script_vm440_promotion", "usa_script_vm_dual_reference", "usa_cright4_promotion", "usa_transition1_promotion", "usa_transition_final_promotion", "usa_consolidated29_promotion", "usa_batch302_promotion", "usa_wave194_promotion", "usa_promo367_promotion", "usa_promo36_promotion")}
        original = (json.dumps(historical,indent=2)+"\n").encode()
        self.assertEqual(hashlib.sha256(original).hexdigest(), sources["manifest_sha256"])
        current_proof = json.loads((ROOT / "decomp/results/combined.json").read_text())
        self.assertEqual(
            hashlib.sha256((ROOT / sources["verifier"]).read_bytes()).hexdigest(),
            current_proof["verifier_source_sha256_lf"],
        )
        self.assertEqual(len(sources["verifier_sha256"]), 64)  # Preserved predecessor provenance.

        whole = self.ledger["whole_project_inventory"]
        frozen = {
            "report": "decomp/results/inventory_2090_pre_opening_new2_20261123.json",
            "combined_proof": "decomp/results/combined_2090_pre_opening_new2_20261123.json",
        }
        for path_key, hash_key in (
            ("report", "report_sha256"),
            ("combined_proof", "combined_proof_sha256"),
        ):
            path = ROOT / frozen[path_key]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), whole[hash_key])

        inventory = json.loads((ROOT / frozen["report"]).read_text())
        summary = inventory["summary"]
        self.assertEqual(summary["newly_matching_c"], whole["matching_c_functions"])
        self.assertEqual(summary["current_unmarked_entries"], whole["combined_c_entries"])
        self.assertEqual(summary["remaining_assembly_entries"], whole["asm_entries"])
        self.assertEqual(summary["identified_function_entries"], whole["identified_entries"])
        self.assertNotEqual(
            summary["upstream_unmarked_names"],
            [entry["symbol"] for entry in self.ledger["residual_functions"]],
        )

        combined = json.loads((ROOT / frozen["combined_proof"]).read_text())
        self.assertEqual(combined["status"], "matched")
        self.assertTrue(combined["comparison"]["full_rom_match"])
        self.assertEqual(combined["comparison"]["rom_size"], 33554432)
        self.assertEqual(combined["comparison"]["matched_functions"], whole["matching_c_functions"])
        self.assertEqual(combined["comparison"]["matched_function_bytes"], whole["matching_c_bytes"])

    def test_tracked_candidate_source_hashes_match(self):
        for entry in self.ledger["residual_functions"]:
            candidate = entry.get("tested_candidate")
            if not candidate or not candidate.get("path"):
                continue
            with self.subTest(symbol=entry["symbol"]):
                path = ROOT / candidate["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(), candidate["sha256"]
                )

    def test_private_rom_spans_when_local_input_is_available(self):
        rom_path = ROOT / "practice" / "diagnostics" / "decomp-100-inputs" / "usa-decompressed.z64"
        if not rom_path.is_file():
            self.skipTest("private decompressed ROM is not present in this checkout")
        rom = rom_path.read_bytes()
        expected = self.ledger["original_rom"]
        self.assertEqual(len(rom), expected["bytes"])
        self.assertEqual(hashlib.sha1(rom).hexdigest(), expected["decompressed_sha1"])
        for entry in self.ledger["residual_functions"]:
            start = int(entry["rom_offset"], 16)
            body = rom[start : start + entry["original_bytes"]]
            with self.subTest(symbol=entry["symbol"]):
                self.assertEqual(len(body), entry["original_bytes"])
                self.assertEqual(
                    hashlib.sha256(body).hexdigest(), entry["original_instruction_sha256"]
                )


if __name__ == "__main__":
    unittest.main()
