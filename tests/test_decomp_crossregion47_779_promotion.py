"""Fail-closed canonical 47-function cross-overlay USA promotion assertions."""
import hashlib,json,unittest
from pathlib import Path
from decomp.verify import load_manifest,claimed_functions,crossregion47_stage,_verify_expanded_cross_overlay_map
from decomp import overlay_crossregion47 as cross
from decomp.candidate_registry import load_files,validate
ROOT=Path(__file__).resolve().parents[1]
class UsaCrossRegion47PromotionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=load_manifest(ROOT/'decomp/manifest.json')
  cls.manifest.pop('overlay_reconcile108_stage', None)  # Historical 779-C checkpoint
  cls.manifest.pop('overlay_crossregion7_stage', None)  # Preserve historical C stage
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
  cls.manifest.pop('overlay_archive22_stage', None); cls.manifest.pop('overlay_archive33_stage', None); cls.manifest.pop('overlay_archive61_stage', None); cls.manifest.pop('overlay_checkpoint500_stage', None); cls.manifest.pop('overlay_rediscovery5_stage', None); cls.manifest.pop('overlay_native49_stage', None); cls.manifest.pop('overlay_native51_stage', None); cls.manifest.pop('overlay_isolated233_stage', None)
  cls.proof=json.loads((ROOT/'decomp/results/usa_crossregion47_779_promotion_20261117.json').read_text())
  cls.registry,cls.inventory=load_files(ROOT)
 def test_manifest_extends_historical_779_and_preserves_fixture_boundaries(self):
  fixture=crossregion47_stage(self.manifest)
  self.assertEqual(fixture['format'],cross.STAGE_FORMAT)
  self.assertEqual(len(fixture['functions']),47)
  self.assertEqual(sum(f['size'] for f in fixture['functions']),2220)
  claims=claimed_functions(self.manifest)
  self.assertEqual((len(claims),len({x['name'] for x in claims}),sum(x['size'] for x in claims)),(987,987,42640))
  for f in fixture['functions']:
   path=ROOT/'decomp/research/jp_recomp_to_c/src'/(f['name']+'.c')
   self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),f['source_sha256'])
 def test_registry_and_independent_proofs(self):
  self.assertEqual(self.registry['accepted_baseline'],{'usa_functions':864,'japan_0_functions':39})
  self.assertEqual(self.registry['expected_pending'],{'usa_functions':0,'usa_bytes':0,'japan_0_functions':0,'japan_0_bytes':0})
  self.assertEqual(validate(ROOT,self.registry,self.inventory)['functions'],{})
  history=json.loads((ROOT/'decomp/data/candidate_registry_782_pending_20261117.json').read_text())
  self.assertEqual((len(history['candidates']),history['accepted_baseline']),(87,{'usa_functions':782,'japan_0_functions':34}))
  self.assertEqual(self.proof['status'],'PASSED_G2')
  # The published 779-C proof is immutable; use its dated archive, not the new 782-C canonical report.
  archives={'decomp/results/combined.json':'decomp/results/combined_779_20261117.json',
            'decomp/results/inventory.json':'decomp/results/inventory_779_20261117.json'}
  for path,expected in ((self.proof['canonical_combined_proof'],self.proof['canonical_combined_proof_sha256']),
                        (self.proof['canonical_inventory'],self.proof['canonical_inventory_sha256'])):
   self.assertEqual(hashlib.sha256((ROOT/archives.get(path,path)).read_bytes()).hexdigest(),expected)
  r=json.loads((ROOT/archives.get(self.proof['canonical_combined_proof'],self.proof['canonical_combined_proof'])).read_text())
  self.assertEqual((r['comparison']['matched_functions'],r['comparison']['matched_function_bytes']),(779,34288))
  self.assertTrue(r['comparison']['full_rom_match'])
  self.assertEqual(r['comparison']['candidate_sha1'],'6ea0ed71032ce08fc2745f412d84936382197494')
  self.assertEqual(r['overlay_crossregion47_stage']['exact_semantic_relocations'],cross.EXACT_COUNTS)
  self.assertEqual(r['overlay_file11_stage']['candidate_semantic_file11_relocations'],8825)
  inv=json.loads((ROOT/archives.get(self.proof['canonical_inventory'],self.proof['canonical_inventory'])).read_text())
  self.assertEqual((inv['summary']['identified_function_entries'],inv['summary']['newly_matching_c'],inv['summary']['remaining_assembly_entries'],inv['summary']['extra_positive_alias_entries']),(7376,779,6584,0))
  old=json.loads((ROOT/self.proof['historic_combined_proof']).read_text())
  self.assertEqual((old['comparison']['matched_functions'],old['comparison']['matched_function_bytes']),(732,32068))
 def test_bad_stage_contract_fails_closed(self):
  bad=dict(self.manifest);bad['overlay_crossregion47_stage']={'format':'unknown'}
  with self.assertRaises(ValueError):crossregion47_stage(bad)
 def test_split_map_rejects_gaps_and_reordered_or_moved_sources(self):
  parent='build/usa/asm/usa/orig.s.o';a='build/usa/asm/usa/a.s.o';b='build/usa/src/f.c.o'
  good={'parents':[{'parent':'orig','section':'file_12','start':0x100,'end':0x120}],
        'assembly':[{'object':a,'section':'file_12','start':0x100,'end':0x110}],
        'functions':[{'name':'f','section':'file_12','rom_offset':0x110,'size':16}]}
  block='\n'.join([' '+a+'(.text)',' .text 0x80000100 0x10 '+a,' '+b+'(.text)',' .text 0x80000110 0x10 '+b])
  result=_verify_expanded_cross_overlay_map(block,[(parent,0x100,0x120)],good,'file_12',0x100,0x80000100)
  self.assertEqual(result['inputs_after_split'],2)
  mutated=json.loads(json.dumps(good));mutated['assembly'][0]['end']=0x10C
  with self.assertRaises(ValueError):_verify_expanded_cross_overlay_map(block,[(parent,0x100,0x120)],mutated,'file_12',0x100,0x80000100)
  bad_map=block.replace('0x80000110','0x80000114')
  with self.assertRaises(ValueError):_verify_expanded_cross_overlay_map(bad_map,[(parent,0x100,0x120)],good,'file_12',0x100,0x80000100)
if __name__=='__main__':unittest.main()
