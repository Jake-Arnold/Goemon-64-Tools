"""ROM-free contract checks for the additive original-ROM Promo65 proof."""
import copy, unittest
from unittest.mock import patch
from decomp import promo65_promotion as p, verify, promotion_integrity

class Promo65Tests(unittest.TestCase):
    def test_live_claims_and_integrity(self):
        claims=verify.claimed_functions(verify.load_manifest(p.ROOT/'results/manifest_3052_before_ebi_slide9.json'))
        self.assertEqual((len(claims),sum(x['size'] for x in claims)),(3052,207240))
        self.assertEqual(len({x['name'] for x in claims}),3052)
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
        self.assertEqual(p.validate_jp()['accepted_C'],2990)

    def test_flags_and_mutation_gates(self):
        for region,cfg in p.REGIONS.items():
            rows=p.rows(region); proof=p.read(p.proof_path(region)); p.validate_native(region,proof)
            self.assertEqual(len(rows),cfg['added'])
            self.assertEqual(sum(f['nonstandard_sdk_flags'] for f in rows),len(p.SDK_FLAGS[region]))
            for key,value in [('expanded_rom_exact',False),('retail_exact',False),('function_identity_exact',False),('semantic_relocations_exact',False),('globals_exact',False),('ownership_exact',False),('candidate_elf_sha256','0'*64),('observed_new_ownership',0),('compiler_sha256','0'*64)]:
                bad=copy.deepcopy(proof);bad[key]=value
                with self.subTest(region=region,key=key),self.assertRaises(ValueError):p.validate_native(region,bad)
            for field in ['native_exact','negative_rejected','flags']:
                bad=copy.deepcopy(proof);bad['native'][0][field]=False
                with self.assertRaises(ValueError):p.validate_native(region,bad)
            for record in proof['native']:
                if record['name'] not in p.SDK_FLAGS[region]:continue
                bad=copy.deepcopy(proof);next(x for x in bad['native'] if x['name']==record['name'])['default_flags_rejected']=False
                with self.assertRaises(ValueError):p.validate_native(region,bad)
            with patch.dict(cfg,manifest='0'*64):
                with self.assertRaises(ValueError):p.rows(region)

    def test_predecessor_and_inventory_tamper(self):
        m=p.read(p.ROOT/'results/manifest_3052_before_ebi_slide9.json');m[p.KEY]['format']='bad'
        with self.assertRaises(ValueError):p.predecessor(m)
        m=p.read(p.ROOT/'results/manifest_3052_before_ebi_slide9.json');d=p.read(p.ROOT/'results/combined_3052_before_ebi_slide9.json');i=p.read(p.ROOT/'results/inventory_3052_before_ebi_slide9.json');i['summary']['newly_matching_c']+=1
        self.assertEqual(p.audit_usa(p.ROOT,m,d,i)['status'],'FAIL')
        m=p.read(p.ROOT/'regions/japan_0.json');m[p.JP_KEY]['asm_remaining']-=1
        with self.assertRaises(ValueError):p.master_predecessor(m)
