"""ROM-free acceptance guard for canonical USA 732-C camera reset promotion."""
import hashlib
import json
import unittest
from pathlib import Path
from decomp.verify import load_manifest, claimed_functions
from decomp.candidate_registry import load_files, validate

ROOT=Path(__file__).resolve().parents[1]

class UsaCameraResetPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load_manifest(ROOT/'decomp/manifest.json')
        cls.registry,cls.file_inventory=load_files(ROOT)
        cls.proof=json.loads((ROOT/'decomp/results/usa_camera_reset_136_promotion_20261117.json').read_text())

    def test_camera_original_address_and_research_source_unchanged(self):
        f=self.proof['function']
        self.assertEqual(f['name'],'func_801F97D4_5B56E4')
        self.assertEqual((f['rom_offset'],f['vma'],f['size']),('0x5B56E4','0x801F97D4',136))
        claims={c['name']:c for c in claimed_functions(self.manifest)}
        self.assertEqual(len(claims),732)
        self.assertEqual(claims[f['name']],{'name':f['name'],'rom_offset':0x5B56E4,'vma':0x801F97D4,'size':136})
        original=(ROOT/f['source']['path']).read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest(),f['source']['git_blob_sha'])
        self.assertEqual(hashlib.sha256(original).hexdigest(),f['source_sha256'])
        self.assertEqual(f['original_code_sha256'],'f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a')
        self.assertEqual(f['native_status'],'PASSED_G2')

    def test_other_pending_claims_remain_research_only(self):
        self.assertEqual(self.registry['accepted_baseline'],{'usa_functions':732,'japan_0_functions':34})
        self.assertEqual(self.registry['expected_pending'],{'usa_functions':129,'usa_bytes':5732,'japan_0_functions':5,'japan_0_bytes':180})
        self.assertEqual(len(self.registry['candidates']),134)
        self.assertFalse(any(x['name']=='func_801F97D4_5B56E4' and x['region']=='usa' for x in self.registry['candidates']))
        self.assertEqual(validate(ROOT,self.registry,self.file_inventory)['functions'],{'usa':129,'japan_0':5})

    def test_independent_732_native_proof_and_historic_731(self):
        p=self.proof
        for name,digest in [(p['canonical_combined_proof'],p['canonical_combined_proof_sha256']),
                            (p['canonical_inventory'],p['canonical_inventory_sha256'])]:
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
        result=json.loads((ROOT/p['canonical_combined_proof']).read_text())
        inventory=json.loads((ROOT/p['canonical_inventory']).read_text())
        self.assertEqual(result['status'],'matched')
        self.assertTrue(result['comparison']['full_rom_match'])
        self.assertEqual((result['comparison']['matched_functions'],result['comparison']['matched_function_bytes']), (732,32068))
        self.assertEqual(result['comparison']['candidate_sha1'],'6ea0ed71032ce08fc2745f412d84936382197494')
        self.assertEqual(result['overlay_file11_stage']['original_semantic_file11_relocations'],8825)
        self.assertEqual(result['overlay_file11_stage']['candidate_semantic_file11_relocations'],8825)
        self.assertEqual(inventory['summary']['identified_function_entries'],7376)
        self.assertEqual(inventory['summary']['remaining_assembly_entries'],6631)
        self.assertEqual(inventory['summary']['extra_positive_alias_entries'],0)
        old=json.loads((ROOT/p['historic_combined_proof']).read_text())
        self.assertEqual((old['comparison']['matched_functions'],old['comparison']['matched_function_bytes']), (731,31932))
        old_inventory=json.loads((ROOT/p['historic_inventory']).read_text())
        self.assertEqual(old_inventory['summary']['newly_matching_c'],731)

if __name__=='__main__':unittest.main()
