import json,hashlib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'manifest.json').read_text())
FUN=DATA['functions']
class TestNative34SourceOnly(unittest.TestCase):
 def test_34(self):self.assertEqual(len(FUN),34)
 def test_29_novel(self):self.assertEqual(sum(x['previous_draft_match'] is None for x in FUN),29)
 def test_5_prior(self):self.assertEqual(sum(x['previous_draft_match']=='PR_183' for x in FUN),5)
 def test_8_symbolic(self):self.assertEqual(sum(x['symbolic'] for x in FUN),8)
 def test_1364_bytes(self):self.assertEqual(sum(x['original_instruction_bytes'] for x in FUN),1364)
 def test_original_offsets_unique(self):self.assertEqual(len({(x['region'],x['original_rom_offset']) for x in FUN}),34)
 def test_explicit_negative_controls(self):
  for x in FUN:
   self.assertEqual(x['negative_control'],'PASS_NATIVE_DIFFERENCE')
   self.assertNotEqual(x['candidate_source_sha256'],x['negative_source_sha256'])
 def test_source_sha256(self):
  for x in FUN:
   for key in ('candidate','negative'):
    p=ROOT/x[key+'_source_path']
    self.assertTrue(p.is_file(),str(p))
    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x[key+'_source_sha256'])
 def test_no_false_rom_proof(self):
  self.assertEqual(DATA['full_original_rom_G2'],'NOT_RUN')
  self.assertTrue(all(x['whole_regional_ROM_G2']=='NOT_RUN' and not x['new_accepted_C'] for x in FUN))
 def test_accepted_C_unchanged(self):self.assertEqual(DATA['accepted_c_snapshot'],{'usa':2164,'japan_0':2398})
 def test_all_rom_range_hashes(self):
  self.assertTrue(all(len(x['original_code_sha256'])==64 for x in FUN))
 def test_replay_present(self):self.assertTrue((ROOT/'replay.py').is_file())
if __name__=='__main__':unittest.main(verbosity=2)
