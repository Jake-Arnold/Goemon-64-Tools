"""ROM-free proof preservation for original-address file_12 promotion at 731 C."""
import hashlib,json,unittest
from pathlib import Path
from decomp.verify import claimed_functions, load_manifest
from decomp.candidate_registry import load_files,validate
ROOT=Path(__file__).resolve().parents[1]

class UsaFile12SpatialPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load_manifest(ROOT/'decomp/manifest.json')
        cls.manifest.pop('overlay_wide132_stage', None)
        cls.manifest.pop('overlay_wide109_stage', None)
        cls.manifest.pop('overlay_resource140_stage', None)
        cls.manifest.pop('overlay_graphics5_stage', None)
        cls.manifest.pop('overlay_file18_53_stage', None)
        cls.manifest.pop('overlay_callbacks10_stage', None)
        cls.manifest.pop('overlay_main19_stage', None)
        cls.manifest.pop('overlay_tiny9_stage', None)
        cls.manifest.pop('overlay_micro2_stage', None)
        cls.manifest.pop('overlay_micro15_stage', None)
        cls.manifest.pop('overlay_micro20_stage', None)
        cls.manifest.pop('overlay_menu2_stage', None)
        cls.manifest.pop('overlay_statecopy1_stage', None)
        cls.registry,cls.inventory=load_files(ROOT)
        cls.proof=json.loads((ROOT/'decomp/results/usa_file12_spatial_11_promotion_20261117.json').read_text())
    def test_exact_original_address_and_source_record(self):
        rows=self.proof['functions']
        self.assertEqual(len(rows),11)
        self.assertEqual(sum(row['size'] for row in rows),748)
        self.assertEqual(len({row['rom_offset'] for row in rows}),11)
        manifest_claims={fn['name']:fn for fn in claimed_functions(self.manifest)}
        self.assertEqual(len(manifest_claims),987)
        for row in rows:
            with self.subTest(name=row['name']):
                self.assertIn(row['name'],manifest_claims)
                expected=manifest_claims[row['name']]
                self.assertEqual(expected['rom_offset'],int(row['rom_offset'],16))
                self.assertEqual(expected['size'],row['size'])
                self.assertEqual(row['native_status'],'PASSED_G2')
                self.assertTrue((ROOT/row['source_staged']).is_file())
                staged=ROOT/row['source_staged']
                self.assertIn(row['name'],staged.read_text())
                research=ROOT/row['source']['path']
                self.assertEqual(staged.read_bytes(),research.read_bytes())
                self.assertEqual(hashlib.sha1(b'blob '+str(research.stat().st_size).encode()+b'\0'+research.read_bytes()).hexdigest(),row['source']['git_blob_sha'])
    def test_removed_promoted_candidates_but_others_stay_research_only(self):
        self.assertEqual(len(self.registry['candidates']),0)
        self.assertEqual(self.registry['accepted_baseline'],{'usa_functions':864,'japan_0_functions':39})
        self.assertEqual(self.registry['expected_pending'],{'usa_functions':0,'usa_bytes':0,'japan_0_functions':0,'japan_0_bytes':0})
        history=json.loads((ROOT/'decomp/data/candidate_registry_782_pending_20261117.json').read_text())
        self.assertEqual((len(history['candidates']),history['accepted_baseline']),(87,{'usa_functions':782,'japan_0_functions':34}))
        names={row['name'] for row in self.proof['functions']}
        self.assertFalse(any(row['name'] in names for row in self.registry['candidates']))
        self.assertEqual(validate(ROOT,self.registry,self.inventory)['functions'],{})
    def test_current_rom_and_inventory_proofs_bound_to_promotion(self):
        d=self.proof
        for path,sha in ((d['canonical_combined_proof'],d['canonical_combined_proof_sha256']),
                         (d['canonical_inventory'],d['canonical_inventory_sha256'])):
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
        combined=json.loads((ROOT/d['canonical_combined_proof']).read_text())
        inventory=json.loads((ROOT/d['canonical_inventory']).read_text())
        self.assertEqual(combined['status'],'matched')
        self.assertTrue(combined['comparison']['full_rom_match'])
        self.assertEqual(combined['comparison']['claimed_functions'],731)
        self.assertEqual(combined['comparison']['matched_function_bytes'],31932)
        self.assertEqual(combined['comparison']['candidate_sha1'],'6ea0ed71032ce08fc2745f412d84936382197494')
        self.assertEqual(inventory['summary']['newly_matching_c'],731)
        self.assertEqual(inventory['summary']['remaining_assembly_entries'],6632)
        self.assertEqual(inventory['summary']['identified_function_entries'],7376)
        self.assertEqual(inventory['summary']['extra_positive_alias_entries'],0)

if __name__=='__main__': unittest.main()
