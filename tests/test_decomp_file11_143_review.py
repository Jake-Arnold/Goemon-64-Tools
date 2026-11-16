"""ROM-free negative/positive checks of the 303-C acceptance report gate."""
from __future__ import annotations

import copy
import unittest

from decomp import review_file11_143 as review


class File11143ReviewTests(unittest.TestCase):
    def setUp(self):
        # Synthetic report data only; not a claim of any actual native build.
        self.claims = [
            {'name': f'func_{0x80010000+4*i:08X}_{4*i:X}',
             'rom_offset': 4*i, 'size': 52 if i < 302 else 476}
            for i in range(303)
        ]
        self.rows = [
            {'name': f['name'], 'size': f['size'],
             'guest_address': f"0x{int(f['name'].split('_')[1], 16):08X}",
             'rom_offset': f"0x{f['rom_offset']:X}",
             'matched': True, 'expected_sha256': '0'*64, 'candidate_sha256': '0'*64}
            for f in self.claims
        ]
        self.g2 = {
            'format': 'goemon-matching-build-result-v1', 'status': 'matched',
            'stage': 'complete',
            'comparison': {
                'full_rom_match': True, 'expected_sha1': review.ROM_SHA1,
                'candidate_sha1': review.ROM_SHA1, 'rom_size': review.ROM_SIZE,
                'claimed_functions': 303, 'matched_functions': 303,
                'matched_function_bytes': review.TOTAL_C_BYTES,
                'functions': self.rows,
            },
            'overlay_file11_stage': {
                'stage': review.STAGE_FORMAT, 'status': 'PASS',
                'original_address_matching_c': 143,
                'additional_beyond_50_existing': 93,
                'file11_C_instruction_bytes': 3908,
                'original_native_object_provenance_checked': 88,
                'original_semantic_file11_relocations': 8825,
                'candidate_semantic_file11_relocations': 8825,
                'original_rom_sha1': review.ROM_SHA1,
                'complete_rom_bytes_equal': review.ROM_SIZE,
                'normalised_NOP_asm_symbol_tables': ['0x5995e8','0x59d4dc','0x5aebdc'],
            },
            'overlay_file11_nop_aliases': {
                'removed_spurious_func_aliases': [
                    'func_801DD6D8_5995E8',
                    'func_801E15CC_59D4DC',
                    'func_801F2CCC_5AEBDC',
                ],
                'preserved_original_nops': 3,
            },
        }
        self.inventory = {
            'format': 'goemon-function-inventory-v1',
            'decompressed_sha1': review.ROM_SHA1,
            'summary': {
                'identified_function_entries': 7376,
                'upstream_unmarked_entries': 13,
                'newly_matching_c': 303,
                'current_unmarked_entries': 316,
                'remaining_assembly_entries': 7060,
                'extra_positive_alias_entries': 0,
                'function_entry_identity_sha256': review.ORIGINAL_INVENTORY_SHA256,
            }
        }

    def test_synthetic_good_reports_accept_only_review(self):
        self.assertEqual(review.verify_g2_report(self.g2,self.claims)['claimed_functions'],303)
        self.assertEqual(review.verify_inventory_report(self.inventory)['remaining_assembly_entries'],7060)

    def test_refuse_not_303_or_not_byte_exact(self):
        for key, value in [('matched_functions',302),('full_rom_match',False),
                           ('rom_size', 16_777_216),('matched_function_bytes',13336)]:
            with self.subTest(key=key):
                bad=copy.deepcopy(self.g2)
                bad['comparison'][key]=value
                with self.assertRaises(ValueError):
                    review.verify_g2_report(bad,self.claims)

    def test_refuse_duplicate_unmatched_or_moved_c_claim(self):
        for change in ('duplicate', 'unmatched', 'vma', 'digest'):
            with self.subTest(change=change):
                bad=copy.deepcopy(self.g2)
                row=bad['comparison']['functions'][0]
                if change=='duplicate':row['name']=bad['comparison']['functions'][1]['name']
                elif change=='unmatched':row['matched']=False
                elif change=='vma':row['guest_address']='0xDEADBEEF'
                else:row['candidate_sha256']='f'*64
                with self.assertRaises(ValueError):
                    review.verify_g2_report(bad,self.claims)

    def test_refuse_wrong_relocations_and_unreviewed_nop_aliases(self):
        for field,value in [('candidate_semantic_file11_relocations',8824),
                            ('normalised_NOP_asm_symbol_tables',[]),
                            ('normalised_NOP_asm_symbol_tables',['0x5995e8','0x59d4dc']),
                            ('original_native_object_provenance_checked',87)]:
            with self.subTest(field=field):
                bad=copy.deepcopy(self.g2)
                bad['overlay_file11_stage'][field]=value
                with self.assertRaises(ValueError):
                    review.verify_g2_report(bad,self.claims)

    def test_refuse_missing_third_nop_annotation_proof(self):
        for field, value in [('preserved_original_nops', 2),
                             ('removed_spurious_func_aliases',
                              ['func_801DD6D8_5995E8','func_801E15CC_59D4DC'])]:
            bad = copy.deepcopy(self.g2)
            bad['overlay_file11_nop_aliases'][field] = value
            with self.assertRaises(ValueError):
                review.verify_g2_report(bad, self.claims)

    def test_refuse_inventory_identity_and_aliases(self):
        for key,value in [('newly_matching_c',302),('remaining_assembly_entries',7061),
                          ('extra_positive_alias_entries',1),
                          ('function_entry_identity_sha256','0'*64)]:
            with self.subTest(key=key):
                bad=copy.deepcopy(self.inventory)
                bad['summary'][key]=value
                with self.assertRaises(ValueError):
                    review.verify_inventory_report(bad)


if __name__ == '__main__':
    unittest.main()
