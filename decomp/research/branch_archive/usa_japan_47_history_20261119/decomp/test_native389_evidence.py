"""ROM-free integrity guardrails for the 389-C native research evidence.

Does not assert that the current canonical production manifest is 389-C;
the linked proof and full current source CI remain separate mandatory gates.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROOF = ROOT / 'research/jp_recomp_to_c/native389_combined_proof.json'


class Native389EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = json.loads(PROOF.read_text(encoding='utf-8'))

    def test_original_rom_and_native_candidate_counts(self):
        p = self.p
        self.assertEqual(p['complete_rom_bytes'], 33554432)
        self.assertTrue(p['complete_original_rom_bytes_equal'])
        self.assertEqual(p['original_usa_sha1'], '6ea0ed71032ce08fc2745f412d84936382197494')
        self.assertEqual(p['canonical_original_usa_c'], 342)
        self.assertEqual(p['native_candidate_c_claims'], 389)
        self.assertEqual(p['new_cross_region_overlay_c'], 47)
        self.assertEqual(p['new_cross_region_overlay_c_bytes'], 2220)
        self.assertEqual(p['native_candidate_c_instruction_bytes'], 19788)
        self.assertFalse(p['formally_promoted'])
        self.assertFalse(p['canonical_production_manifest_updated'])

    def test_full_original_elf_and_reloc_counts(self):
        p = self.p
        self.assertEqual(p['elf_original_function_entries'], 7376)
        self.assertEqual(p['candidate_unmarked_c_entries'], 402)
        self.assertEqual(p['remaining_assembly_entries'], 6974)
        self.assertEqual(p['extra_positive_func_aliases'], 0)
        self.assertTrue(p['new_c_claims_match_exactly_removed_nonmatching_markers'])
        self.assertTrue(p['all_eight_semantic_relocation_multisets_equal'])
        self.assertEqual(p['relocations_original_vs_combined'], {
            'file_11': 8825, 'file_12': 7051, 'file_13': 9589,
            'file_14': 3041, 'file_15': 1625, 'file_17': 1739,
            'file_18': 3365, 'file_19': 1078,
        })

    def test_canonical_symbol_annotations_not_relaxed(self):
        self.assertEqual(self.p['original_vs_canonical_size_annotations'], {
            'func_8000D3B8_DFB8': {'original': 64, 'canonical_and_candidate': 72},
            'func_8003F6E8_402E8': {'original': 48, 'canonical_and_candidate': 56},
        })

    def test_research_source_inventory_distinct(self):
        source_dir = ROOT / 'research/jp_recomp_to_c/src'
        self.assertTrue(source_dir.is_dir())
        sources = list(source_dir.glob('func_*.c'))
        self.assertEqual(len(sources), 48)  # 47 new plus existing main C duplicate
        self.assertTrue((source_dir/'func_800166AC_172AC.c').is_file())


if __name__ == '__main__':
    unittest.main()
