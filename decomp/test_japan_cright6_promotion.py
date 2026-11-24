import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from decomp import japan_cright6_promotion as stage
from decomp import japan_cright6_integrity as integrity

class JapanCRight6Tests(unittest.TestCase):
    def test_frozen_candidate_source_and_ownership(self):
        rows=stage.rows();prior=stage.previous_names()
        self.assertEqual(len(prior),2528)
        self.assertEqual((len(rows),sum(f['original_bytes'] for f in rows),sum(f['original_relocations'] for f in rows)),(6,624,24))
        self.assertFalse(prior & {f['name'] for f in rows})

    def test_manifest_drift_rejected(self):
        with patch.object(stage,'MANIFEST_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'source manifest drift'):stage.rows()

    def test_previous_ownership_overlap_rejected(self):
        name=stage.rows()[0]['name'];prior=stage.previous_names()
        with patch.object(stage,'previous_names',return_value=prior|{name}):
            with self.assertRaisesRegex(ValueError,'duplicate accepted function'):stage.rows()

    def test_rom_fingerprint_rejected(self):
        with self.assertRaisesRegex(ValueError,'wrong original ROM'):stage.rows(b'not an original ROM')

    def test_research_only_has_no_candidate_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'regions').mkdir();(root/'regions/japan_0.json').write_text('{}')
            paths=[root/x for x in ('regional','proof','inventory')]
            with patch.object(integrity,'ROOT',root),patch.object(integrity,'REGIONAL',paths[0]),patch.object(integrity,'PROOF',paths[1]),patch.object(integrity,'INVENTORY',paths[2]):
                self.assertEqual(integrity.validate()['status'],'RESEARCH_ONLY')
                paths[0].write_text('{}')
                with self.assertRaisesRegex(ValueError,'orphaned'):integrity.validate()

    def test_forged_candidate_claim_rejected(self):
        with self.assertRaisesRegex(ValueError,'complete native G2 proof mismatch'):
            integrity.validate_documents({}, {}, {'status':'PASSED_G2_LOCAL'}, {})

    def test_complete_candidate_report_negative_controls(self):
        import copy
        head=json.loads((stage.ROOT/'regions/japan_0.json').read_text()).get(stage.KEY)
        if head is None:
            self.assertEqual(integrity.validate()['status'],'RESEARCH_ONLY')
            return
        docs=[head,*(json.loads(p.read_text()) for p in (integrity.REGIONAL,integrity.PROOF,integrity.INVENTORY))]
        self.assertEqual(integrity.validate_documents(*docs)['status'],'PASS')
        for i,key,value in ((0,'accepted_original_C',2528),(1,'matching_c',2535),(2,'rom_sha1','0'*40),(2,'semantic_relocations_sha256','0'*64),(2,'ownership_exact',False),(3,'remaining_assembly',4841),(3,'previous_C_names',[])):
            with self.subTest(key=key):
                bad=copy.deepcopy(docs);bad[i][key]=value
                with self.assertRaises(ValueError):integrity.validate_documents(*bad)
        bad=copy.deepcopy(docs);bad[2]['abs_metadata_fix']['code_and_relocations_unchanged']=False
        with self.assertRaises(ValueError):integrity.validate_documents(*bad)

if __name__=='__main__':unittest.main()
