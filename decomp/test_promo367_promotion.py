import copy, unittest
from unittest.mock import patch
from decomp import promo367_promotion as p, verify, promotion_integrity

class Promo367Tests(unittest.TestCase):
    def test_live_usa_claims(self):
        m=verify.load_manifest(p.ROOT/'results/manifest_2939_before_promo195.json');claims=verify.claimed_functions(m)
        self.assertEqual((len(claims),sum(x['size'] for x in claims)),(2939,192312))
        self.assertEqual(len({x['name'] for x in claims}),2939)
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
    def test_research_sources_and_manifest(self):
        for region,cfg in p.REGIONS.items():
            self.assertEqual(len(p.rows(region)),cfg['added'])
            with patch.dict(cfg,manifest='0'*64):
                with self.assertRaises(ValueError):p.rows(region)
    def test_regional_native_gate_negative_controls(self):
        for region in p.REGIONS:
            self.check_native_gate(region)
    def check_native_gate(self,region):
        d=p.read(p.proof_path(region));p.validate_native(region,d)
        for k,v in [('expanded_rom_exact',False),('retail_exact',False),('function_identity_exact',False),('semantic_relocations_exact',False),('globals_exact',False),('ownership_exact',False),('candidate_elf_sha256','0'*64),('observed_new_ownership',0),('compiler_sha256','0'*64)]:
            q=copy.deepcopy(d);q[k]=v
            with self.subTest(k=k),self.assertRaises(ValueError):p.validate_native(region,q)
        for k in ('native_exact','negative_rejected'):
            q=copy.deepcopy(d);q['native'][0][k]=False
            with self.assertRaises(ValueError):p.validate_native(region,q)
        q=copy.deepcopy(d);q['strict_inventory']['upstream_unmarked_names'].pop()
        with self.assertRaises(ValueError):p.validate_native(region,q)
    def test_predecessor_mutation(self):
        m=p.read(p.ROOT/'results/manifest_2939_before_promo195.json');m[p.KEY]['format']='bad'
        with self.assertRaises(ValueError):p.predecessor(m)
    def test_inventory_tamper(self):
        m=p.read(p.ROOT/'results/manifest_2939_before_promo195.json');d=p.read(p.ROOT/'results/combined_2939_before_promo195.json');i=p.read(p.ROOT/'results/inventory_2939_before_promo195.json');i['summary']['newly_matching_c']+=1
        self.assertEqual(p.audit_usa(p.ROOT,m,d,i)['status'],'FAIL')
    def test_japan_canonical(self):
        self.assertEqual(p.validate_jp()['accepted_C'],2842)
        m=p.read(p.ROOT/'regions/japan_0.json');m[p.JP_KEY]['asm_remaining']-=1
        with self.assertRaises(ValueError):p.master_predecessor(m)
