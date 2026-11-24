"""New additive transition stage: immutable predecessor and fail-closed controls."""
import copy,unittest
from unittest.mock import patch
from decomp import transition_promotion as t,verify,promotion_integrity

class TransitionPromotionTests(unittest.TestCase):
    def test_exact_additive_ownership(self):
        m=verify.load_manifest(t.ROOT/'manifest.json');rows=verify.claimed_functions(m)
        self.assertEqual((len(rows),sum(f['size'] for f in rows)),(2324,111852))
        self.assertEqual(t.claims(),[{'name':'func_8000394C_454C','rom_offset':0x454C,'vma':0x8000394C,'size':116}])
        self.assertNotIn('func_800030F0_3CF0',{f['name'] for f in rows})
        self.assertEqual(t.validate_jp()['accepted_C'],2551)
        names={f['name'] for f in t.manifest()['japan']};self.assertEqual(len(names),17)
        self.assertFalse(names&t.previous_jp_names());self.assertNotIn('func_80003090_3C90',names)
    def test_source_manifest_and_predecessor_reject_drift(self):
        with patch.object(t,'MANIFEST_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'source manifest drift'):t.manifest()
        m=verify.load_manifest(t.ROOT/'manifest.json');m['units'][0]['functions'][0]['size']+=4
        with self.assertRaisesRegex(ValueError,'frozen USA predecessor'):t.validate_predecessor(m)
    def test_native_proof_rejects_forged_reference_and_inventory(self):
        for region,path in [('usa',t.USA_PROOF),('japan',t.JP_PROOF)]:
            p=t.read(t.ROOT/'results'/path);self.assertEqual(t.validate_compact(region,p),p)
            for k,v in [('native_relocations',0),('candidate_elf_sha256','0'*64),('independent_shadow_exact',False),('removed_original_abs_offset_relocations',[]),('prior_names_sha256','0'*64)]:
                with self.subTest(region=region,key=k):
                    q=copy.deepcopy(p);q[k]=v
                    with self.assertRaises(ValueError):t.validate_compact(region,q)
            q=copy.deepcopy(p);q['strict_predecessor_inventory']['function_entry_identity_sha256']='0'*64
            with self.assertRaises(ValueError):t.validate_compact(region,q)
    def test_us_inventory_and_retained_asm_rejected(self):
        m=verify.load_manifest(t.ROOT/'manifest.json');p=t.read(t.ROOT/'results/combined.json');i=t.read(t.ROOT/'results/inventory.json')
        self.assertEqual(t.audit_usa(t.ROOT,m,p,i)['status'],'PASS')
        bad=copy.deepcopy(i);bad['summary']['newly_matching_c']=2323
        self.assertEqual(t.audit_usa(t.ROOT,m,p,bad)['status'],'FAIL')
        bad=copy.deepcopy(p);bad['retained_assembly_functions'].append('func_8000394C_454C')
        self.assertEqual(t.audit_usa(t.ROOT,m,bad,i)['status'],'FAIL')
if __name__=='__main__':unittest.main()
