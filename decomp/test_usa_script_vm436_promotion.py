"""ROM-free fail-closed VM436 post-2164 stage and compiler-source invariants."""
import copy
import json
from pathlib import Path
import unittest

from decomp import usa_script_vm436_promotion as vm
from decomp.verify import load_manifest, claimed_functions

ROOT = Path(__file__).resolve().parent


class TestVM436Promotion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_manifest(ROOT / 'manifest.json')
        cls.m.pop('usa_native151_promotion',None)

    def test_new_claim_is_one_original_436_byte_function(self):
        before = {k: v for k, v in self.m.items() if k != 'usa_script_vm436_promotion'}
        fs = claimed_functions(before)
        self.assertEqual((len(fs), sum(f['size'] for f in fs)), (2164, 99604))
        after = claimed_functions(self.m)
        self.assertEqual((len(after), sum(f['size'] for f in after)), (2165, 100040))
        self.assertEqual(after[-1], {'name': vm.NAME, 'rom_offset': vm.OFFSET, 'vma': vm.VMA, 'size': vm.SIZE})
        self.assertEqual(sum(f['name'] == vm.NAME for f in after), 1)

    def test_pinned_original_source_reconstructs_exact_merged_source(self):
        self.assertEqual(vm.sha(vm.SOURCE.read_bytes()), vm.ORIGINAL_C_SOURCE_SHA256)
        self.assertEqual(vm.sha(vm.proposed_source().encode()), vm.MERGED_VM_SOURCE_SHA256)
        self.assertEqual(vm.proposed_source().count('void ' + vm.NAME), 1)
        self.assertNotIn(vm.ASM_PRAGMA, vm.proposed_source())

    def test_unreviewed_stage_is_rejected(self):
        bad = copy.deepcopy(self.m)
        bad['usa_script_vm436_promotion']['format'] = 'research_only'
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            vm.validate_predecessor(bad)

    def test_original_asm_owner_must_be_unique(self):
        bad = copy.deepcopy(self.m)
        u = next(x for x in bad['units'] if x['source'] == 'script_vm.c')
        u['assembly_functions'].remove(vm.NAME)
        with self.assertRaises(ValueError):
            vm.validate_predecessor(bad)

    def test_canonical_predecessor_cannot_be_contaminated(self):
        bad = copy.deepcopy(self.m)
        u = next(x for x in bad['units'] if x['source'] == 'script_vm.c')
        u['functions'].append({'name': vm.NAME, 'rom_offset': vm.OFFSET, 'size': vm.SIZE})
        with self.assertRaises(ValueError):
            vm.validate_predecessor(bad)

    def test_research_negative_controls_are_not_promoted(self):
        assert vm.SOURCE.read_bytes() != (vm.SOURCE.parent / 'negative_no_redundant_mask.c').read_bytes()
        assert vm.SOURCE.read_bytes() != (vm.SOURCE.parent / 'negative_split_final_line.c').read_bytes()
        self.assertEqual(vm.SOURCE.read_text().count('0xFFFF'), 2)


if __name__ == '__main__':
    unittest.main()
