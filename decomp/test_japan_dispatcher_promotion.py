import copy,unittest
from decomp import japan_dispatcher_promotion as p
class DispatcherTests(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(p.validate()['accepted_C'],2843)
    def test_negative_proof_controls(self):
        source=p.read(p.ROOT/p.PROOF)
        for key,value in [('native_negative_rejected',False),('expanded_rom_exact',False),('retail_rom_exact',False),('function_identity_exact',False),('globals_exact',False),('semantic_relocations_exact',False),('ownership_exact',False),('removed_original_reference_records',[]),('candidate_elf_sha256','0'*64),('source_sha256','0'*64)]:
            d=copy.deepcopy(source);d[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):p.validate_native(d)
        d=copy.deepcopy(source);d['strict_inventory']['upstream_unmarked_names'].pop()
        with self.assertRaises(ValueError):p.validate_native(d)
    def test_master_drift(self):
        d=p.read(p.ROOT/'regions/japan_0.json');d[p.KEY]['accepted_original_C']+=1
        with self.assertRaises(ValueError):p.master_predecessor(d)
