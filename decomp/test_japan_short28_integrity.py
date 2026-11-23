"""Fail-closed immutable JP 2398-C regional promotion record tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json,unittest
from decomp import japan_short28_integrity as integ
class JapaneseShort28IntegrityTests(unittest.TestCase):
    def test_stored_original_rom_proof_and_ownership(self):
        result=integ.validate()
        self.assertEqual((result['canonical_matching_c'],result['asm_remaining'],result['semantic_relocations']),(2398,4978,80745))
    def test_tampered_original_relocation_reference_refused(self):
        with TemporaryDirectory() as tmp:
            d=json.loads(integ.PROOF.read_text());d['candidate_semantic_relocations']=80746
            p=Path(tmp)/'g2.json';p.write_text(json.dumps(d))
            with patch.object(integ,'PROOF',p):
                with self.assertRaisesRegex(ValueError,'mutated'):integ.validate()
    def test_tampered_source_claim_refused(self):
        with TemporaryDirectory() as tmp:
            d=json.loads(integ.INVENTORY.read_text());name=next(iter(d['source_sha256_by_function']))
            d['source_sha256_by_function'][name]='0'*64
            p=Path(tmp)/'inventory.json';p.write_text(json.dumps(d))
            with patch.object(integ,'INVENTORY',p):
                with self.assertRaisesRegex(ValueError,'source ownership'):integ.validate()
    def test_tampered_region_count_refused(self):
        with TemporaryDirectory() as tmp:
            d=json.loads(integ.REGIONAL.read_text());d['accepted_japan_c_after']=2370
            p=Path(tmp)/'region.json';p.write_text(json.dumps(d))
            with patch.object(integ,'REGIONAL',p):
                with self.assertRaisesRegex(ValueError,'regional manifest'):integ.validate()
if __name__=='__main__':unittest.main()
