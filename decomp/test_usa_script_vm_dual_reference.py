"""ROM-free fail-closed controls for the independently assembled VM pair."""
import copy, unittest
from unittest.mock import patch
from collections import Counter
from decomp import usa_script_vm_dual_reference as stage
from decomp.verify import load_manifest,claimed_functions,ROOT

class VMDualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load_manifest(ROOT/'manifest.json')

    def test_two_disjoint_exact_original_claims(self):
        old=stage.validate_predecessor(self.manifest)
        self.assertEqual((len(old),sum(x['size'] for x in old)),(2317,110288))
        self.assertEqual(claimed_functions(self.manifest),old+stage.claims())
        self.assertEqual(sum(x['size'] for x in stage.claims()),720)

    def test_stage_format_and_source_drift_fail_closed(self):
        m=copy.deepcopy(self.manifest);m[stage.KEY]={'format':'unreviewed'}
        with self.assertRaises(ValueError):stage.validate_predecessor(m)
        with self.assertRaises(ValueError):stage.validate_predecessor(self.manifest,b'wrong')
        targets=copy.deepcopy(stage.TARGETS);targets[0]['source_sha256']='0'*64
        with patch.object(stage,'TARGETS',targets):
            with self.assertRaises(ValueError):stage.validate_predecessor(self.manifest)

    def test_missing_original_owner(self):
        m=copy.deepcopy(self.manifest)
        next(x for x in m['units'] if x['source']=='script_vm.c')['assembly_functions'].remove(stage.TARGETS[0]['name'])
        with self.assertRaises(ValueError):stage.validate_predecessor(m)

    def test_untrusted_asm_not_normalized(self):
        with self.assertRaises(ValueError):stage.reference_sources('not original','not original')

    def test_whole_relocation_reference_is_not_optional(self):
        a=Counter({('test',1,'x',0,'a'):82103});b=Counter({('test',1,'x',0,'a'):82102})
        wrong=Counter({('test',2,'x',0,'a'):82102})
        values=[(a,82103,stage.vm440.RELOC_SHA),(b,82102,stage.NEW_RELOC),(a,82103,stage.vm440.RELOC_SHA),(wrong,82102,stage.NEW_RELOC)]
        with patch.object(stage,'all_semantic_relocations',side_effect=values):
            with self.assertRaisesRegex(ValueError,'full relocation multisets differ'):stage.check_linked('a','b','c','d')

if __name__=='__main__':unittest.main()
