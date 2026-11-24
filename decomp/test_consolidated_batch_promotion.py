"""Fail-closed checks for the additive USA consolidated native stage."""
import copy, unittest
from unittest.mock import patch
from decomp import consolidated_batch_promotion as b, verify, promotion_integrity

class Consolidated29Tests(unittest.TestCase):
    def test_canonical_stage(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');old=b.validate_predecessor(m);new=verify.claimed_functions(m)
        self.assertEqual(new,old+b.claims());self.assertEqual((len(new),sum(x['size'] for x in new)),(2354,115792))
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
    def test_manifest_and_source_negative_controls(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');bad=copy.deepcopy(m);bad[b.KEY]['format']='unreviewed'
        with self.assertRaises(ValueError):b.validate_predecessor(bad)
        with patch.object(b,'MANIFEST_SHA','0'*64):
            with self.assertRaises(ValueError):b.rows()
    def test_proof_rejects_wrong_original(self):
        p=b.read(b.ROOT/'results'/b.PROOF);self.assertEqual(b.validate_proof(p),p)
        for k,v in [('semantic_relocations',82081),('stable_globals',26713),('retail_exact',False),('native_negative_controls_rejected',28),('candidate_elf_sha256','0'*64)]:
            q=copy.deepcopy(p);q[k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):b.validate_proof(q)
    def test_inventory_cannot_count_unproven_source(self):
        m=verify.load_manifest(b.ROOT/'manifest.json');p=b.read(b.ROOT/'results/combined.json');i=b.read(b.ROOT/'results/inventory.json');bad=copy.deepcopy(i);bad['summary']['newly_matching_c']+=1
        self.assertEqual(b.audit(b.ROOT,m,p,bad)['status'],'FAIL')
