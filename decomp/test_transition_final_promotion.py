"""Final original ASM boundary and independent-reference proof controls."""
import copy,unittest
from unittest.mock import patch
from decomp import transition_final_promotion as t,verify,promotion_integrity

class FinalTransitionTests(unittest.TestCase):
    def test_additive_ownership(self):
        m=verify.load_manifest(t.ROOT/'results/manifest_2325_before_consolidated29_20261124.json');rows=verify.claimed_functions(m)
        self.assertEqual((len(rows),sum(f['size'] for f in rows)),(2325,112420))
        self.assertEqual(rows[-1],t.claims()[0]);self.assertEqual(promotion_integrity.audit()['status'],'PASS')
        self.assertEqual(len(t.validate_predecessor(m)),2324)
    def test_modified_source_hash_fails(self):
        with patch.dict(t.FILES,{'arg_s32_add.c':'0'*64}):
            with self.assertRaisesRegex(ValueError,'source or reference drift'):t.verify_files()
    def test_native_proof_rejects_wrong_reference_and_abi(self):
        p=t.read(t.ROOT/'results'/t.PROOF);self.assertEqual(t.validate_proof(p),p)
        for k,v in [('native_relocations',82098),('pool_bytes',32),('native_elf_sha256','0'*64),('relocation_delta_sha256','0'*64),('unit_text_relocations',124),('retail_sha1','0'*40)]:
            q=copy.deepcopy(p);q[k]=v
            with self.subTest(key=k),self.assertRaises(ValueError):t.validate_proof(q)
        for k,v in [('sole_symbol_reference',False),('incoming_a0_overwritten',False),('live_c_callers_or_declarations',1),('historical_c_prototype','void')]:
            q=copy.deepcopy(p);q['assembly_caller_contract'][k]=v
            with self.subTest(key=k),self.assertRaises(ValueError):t.validate_proof(q)
    def test_bad_manifest_and_inventory_rejected(self):
        m=verify.load_manifest(t.ROOT/'results/manifest_2325_before_consolidated29_20261124.json');p=t.read(t.ROOT/'results/combined_2325_before_consolidated29_20261124.json');i=t.read(t.ROOT/'results/inventory_2325_before_consolidated29_20261124.json')
        q=copy.deepcopy(m);q['units'][0]['functions'][0]['size']+=4
        with self.assertRaisesRegex(ValueError,'frozen USA2324'):t.validate_predecessor(q)
        q=copy.deepcopy(i);q['summary']['candidate_zero_sized_function_labels_ignored']+=5
        self.assertEqual(t.audit(t.ROOT,m,p,q)['status'],'FAIL')
        q=copy.deepcopy(p);q['retained_assembly_functions'].append(t.NAME)
        self.assertEqual(t.audit(t.ROOT,m,q,i)['status'],'FAIL')
