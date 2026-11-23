"""VM440 post-2316 canonical stage guards, no private ROM required."""
import copy
import unittest
from unittest.mock import patch
from decomp import usa_script_vm440_promotion as vm
from decomp.verify import load_manifest,claimed_functions,ROOT

class VM440Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load_manifest(ROOT/'results/manifest_2317_before_vmdual_20261123.json')

    def test_adds_one_nonoverlapping_original_claim(self):
        prior=vm.validate_predecessor(self.manifest)
        self.assertEqual((len(prior),sum(x['size'] for x in prior)),(2316,109848))
        self.assertEqual(claimed_functions(self.manifest),prior+[{'name':vm.NAME,'vma':vm.VMA,'rom_offset':vm.OFFSET,'size':440}])

    def test_source_preserves_whitespace_and_asm_peers(self):
        self.assertEqual(vm.sha(vm.SOURCE.read_bytes()),vm.SOURCE_SHA)
        s=vm.proposed_source()
        self.assertEqual(vm.sha(s.encode()),vm.MERGED_SHA)
        self.assertNotIn(f'GLOBAL_ASM("asm/usa/nonmatchings/script_vm/{vm.NAME}.s")',s)
        for name in ('func_8003F37C_3FF7C','func_8003DF98_3EB98'):
            self.assertIn(f'GLOBAL_ASM("asm/usa/nonmatchings/script_vm/{name}.s")',s)

    def test_stage_format_required(self):
        m=copy.deepcopy(self.manifest);m[vm.KEY]={'format':'unreviewed'}
        with self.assertRaises(ValueError):vm.validate_predecessor(m)

    def test_missing_owner_rejected(self):
        m=copy.deepcopy(self.manifest)
        next(x for x in m['units'] if x['source']=='script_vm.c')['assembly_functions'].remove(vm.NAME)
        with self.assertRaises(ValueError):vm.validate_predecessor(m)

    def test_source_drift_rejected(self):
        with patch.object(vm,'SOURCE_SHA','0'*64):
            with self.assertRaises(ValueError):vm.proposed_source()

    def test_wrong_rom_rejected(self):
        with self.assertRaises(ValueError):vm.validate_predecessor(self.manifest,b'wrong')
