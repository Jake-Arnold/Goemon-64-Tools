"""ROM-free research-claim regression guards for three additional file_11 C functions."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=ROOT/"results"/"file11_104_scratch_20261116.json"
class File11Scratch104Claims(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.p=json.loads(P.read_text())
    def test_original_rom(self):
        self.assertTrue(self.p["full_33554432_bytes_identical"])
        self.assertEqual(self.p["original_rom_sha1"],"6ea0ed71032ce08fc2745f412d84936382197494")
    def test_new_3_original_sizes(self):
        self.assertEqual(len(self.p["new_usa_functions"]),3)
        self.assertEqual(sum(x["size"] for x in self.p["new_usa_functions"]),148)
        self.assertEqual(self.p["file11_c_functions"],104)
        self.assertEqual(self.p["file11_c_bytes"],2496)
    def test_original_linker_and_inventory(self):
        self.assertEqual(self.p["file11_original_vma_link_chunks"],86)
        self.assertEqual(self.p["original_function_entries"],7376)
        self.assertEqual(self.p["candidate_function_entries"],7376)
    def test_explicit_relocation_exception(self):
        self.assertTrue(self.p["relocation_semantic_tuples_equal"])
        self.assertEqual(self.p["file11_relocations"],8825)
        self.assertFalse(self.p["raw_relocation_order_equal"])
        self.assertEqual(self.p["reordered_indices"],[2506,2507,2508,6131,6132,6133,6762,6763,6764])
    def test_no_central_promotion_claim(self):
        self.assertEqual(self.p["central_264_g2"],"not_run")
        self.assertEqual(self.p["japanese_whole_rom"],"not_built")
        self.assertFalse(self.p["canonical_manifest_modified"])
if __name__=="__main__":unittest.main()
