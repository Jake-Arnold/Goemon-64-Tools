"""ROM-free negative controls for the nine-function Ebi Slide promotion."""
import copy, unittest
from decomp import ebi_slide9_promotion as p, verify, promotion_integrity
class EbiSlide9Tests(unittest.TestCase):
    def test_current_claims(self):
        c=verify.claimed_functions(verify.load_manifest(p.ROOT/'results/manifest_3056_before_warp_batch_a.json'))
        self.assertEqual((len(c),sum(f['size'] for f in c)),(3056,209088))
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
        self.assertEqual(p.validate_jp()['accepted_C'],2995)
    def test_native_proof_rejects_mutation(self):
        for r in p.REGIONS:
            proof=p.read(p.proof_path(r));p.validate_native(r,proof)
            for k,v in [('expanded_rom_exact',False),('retail_exact',False),('function_identity_exact',False),('semantic_relocations_exact',False),('globals_exact',False),('ownership_exact',False),('candidate_elf_sha256','0'*64),('observed_new_ownership',0)]:
                with self.subTest(region=r,field=k):
                    bad=copy.deepcopy(proof);bad[k]=v
                    with self.assertRaises(ValueError):p.validate_native(r,bad)
            for k in ('native_exact','negative_rejected','flags'):
                bad=copy.deepcopy(proof);bad['native'][0][k]=False
                with self.assertRaises(ValueError):p.validate_native(r,bad)
