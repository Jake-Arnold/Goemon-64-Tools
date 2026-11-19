"""ROM-free claim guard for 101-function file_11 research metadata."""
import json, unittest
from pathlib import Path
DATA = Path(__file__).resolve().parent / "results" / "file11_101_scratch_20261116.json"

class File11Scratch101Claims(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.x=json.loads(DATA.read_text())
    def test_exact_rom(self):
        self.assertTrue(self.x["complete_usa_rom_identical"])
        self.assertEqual(self.x["complete_usa_rom_bytes"], 33554432)
    def test_matching_counts(self):
        self.assertEqual(self.x["file11_total_scratch_C_functions"],101)
        self.assertEqual(self.x["file11_total_scratch_C_bytes"],2348)
        self.assertEqual(self.x["new_usa_exact_original_vma_functions"],28)
        self.assertEqual(self.x["new_japan_exact_original_vma_functions"],28)
        self.assertEqual(self.x["additional_matching_bytes_per_region"],892)
    def test_relocations_and_symbols(self):
        self.assertEqual(self.x["original_linked_elf_relocations"],8825)
        self.assertTrue(self.x["all_semantic_relocation_tuples_match"])
        self.assertFalse(self.x["raw_relocation_order_equal"])
        self.assertEqual(self.x["exact_reordered_indices"],[2506,2507,2508,6131,6132,6133])
        self.assertEqual(self.x["original_positive_function_entries"],7376)
        self.assertEqual(self.x["scratch_positive_function_entries"],7376)
        self.assertTrue(self.x["func_symbol_identity_sets_equal"])
    def test_no_formal_promotion_claim(self):
        self.assertEqual(self.x["central_canonical_matched_functions"],210)
        self.assertEqual(self.x["central_261_complete_g2"],"not_run")
        self.assertEqual(self.x["japanese_whole_rom"],"not_built")
        self.assertFalse(self.x["canonical_manifest_modified"])

if __name__=="__main__":unittest.main()
