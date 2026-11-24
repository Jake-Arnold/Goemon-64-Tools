"""Check canonical JP13 ownership, frozen predecessor and native evidence."""
import copy,unittest
from unittest.mock import patch
from decomp import japan_consolidated13_promotion as j

class JapanConsolidated13Tests(unittest.TestCase):
    def test_canonical_additive(self):
        self.assertEqual(j.validate()['accepted_C'],2564)
        self.assertEqual(len(j.prior_names()),2551)
        self.assertFalse(j.prior_names() & {f['name'] for f in j.rows()})
        self.assertEqual(sum(f['original_bytes'] for f in j.rows()),2136)
    def test_source_manifest_rejects_drift(self):
        with patch.object(j,'MANIFEST_SHA','0'*64):
            with self.assertRaises(ValueError):j.rows()
    def test_native_metadata_rejects_forgery(self):
        p=j.read(j.ROOT/'results'/j.PROOF);self.assertEqual(j.validate_proof(p),p)
        for k,v in [('semantic_relocations',80654),('candidate_elf_sha256','0'*64),('native_negative_controls_rejected',12),('retail_exact',False)]:
            q=copy.deepcopy(p);q[k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):j.validate_proof(q)
        q=copy.deepcopy(p);q['strict_inventory']['newly_matching_c']=14
        with self.assertRaises(ValueError):j.validate_proof(q)
