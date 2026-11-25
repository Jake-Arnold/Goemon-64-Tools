"""Fail-closed metadata and ownership checks for the two-region batch."""
import copy
import unittest
from unittest.mock import patch
from decomp import batch302_promotion as b, verify, promotion_integrity

class Batch302Tests(unittest.TestCase):
    def test_complete_canonical_claims(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');old=b.predecessor(m);claims=verify.claimed_functions(m)
        self.assertEqual(claims,old+b.claims())
        self.assertEqual((len(claims),sum(x['size'] for x in claims)),(2556,144092))
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
        self.assertEqual(b.validate_jp()['accepted_C'],2664)

    def test_negative_controls_reject_native_proof_forgery(self):
        for r in b.REGIONS:
            p=b.read(b.proof_path(r));b.validate_native(r,p)
            for k,v in [('retail_exact',False),('expanded_rom_exact',False),('candidate_elf_sha256','0'*64),('semantic_relocations_after',0),('observed_new_ownership',0),('source_manifest_sha256','0'*64)]:
                with self.subTest(r=r,k=k),self.assertRaises(ValueError):
                    q=copy.deepcopy(p);q[k]=v;b.validate_native(r,q)
            q=copy.deepcopy(p);q['native'][0]['negative_rejected']=False
            with self.assertRaises(ValueError):b.validate_native(r,q)
            q=copy.deepcopy(p);q['strict_inventory']['upstream_unmarked_names'].pop()
            with self.assertRaises(ValueError):b.validate_native(r,q)

    def test_mixed_unit_proof_required(self):
        p=b.read(b.proof_path('usa'));p['mixed_units'][0]['whole_unit_text_equal']=False
        with self.assertRaises(ValueError):b.validate_native('usa',p)
        p=b.read(b.proof_path('usa'));p['mixed_controls'][0]['negative_rejected']=False
        with self.assertRaises(ValueError):b.validate_native('usa',p)

    def test_predecessor_and_source_drift_rejected(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');m[b.KEY]['format']='unreviewed'
        with self.assertRaises(ValueError):b.predecessor(m)
        with patch.dict(b.REGIONS['usa'],{'manifest':'0'*64}):
            with self.assertRaises(ValueError):b.rows('usa')

    def test_canonical_inventory_tamper_rejected(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');p=b.read(b.ROOT/'results/combined.json');i=b.read(b.ROOT/'results/inventory.json');i['summary']['newly_matching_c']+=1
        self.assertEqual(b.audit_usa(b.ROOT,m,p,i)['status'],'FAIL')
