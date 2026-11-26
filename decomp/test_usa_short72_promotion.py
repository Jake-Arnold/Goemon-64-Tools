"""Non-ROM negative controls for USA short72 manifest and original source ownership."""
import copy
import hashlib
import json
import pathlib
import unittest
from unittest import mock
from decomp import usa_short72_promotion as stage
from decomp.verify import load_manifest, claimed_functions

class TestShort72(unittest.TestCase):
    def test_72_frozen_source_owners(self):
        d=stage.fixture();fs=d['functions']
        self.assertEqual((len(fs),sum(f['size'] for f in fs)),(72,4844))
        self.assertEqual(len(set(f['name'] for f in fs)),72)
        self.assertTrue(all(hashlib.sha256((stage.SOURCE/(f['source']+'.c')).read_bytes()).hexdigest()==f['source_sha256'] for f in fs))
    def test_accepted_predecessor_no_overlap(self):
        manifest=load_manifest(stage.ROOT/'results/manifest_2165_before_native151_20261123.json')
        manifest.pop('usa_script_vm_dual_reference',None)
        manifest.pop('usa_script_vm440_promotion',None)
        manifest.pop('usa_native151_promotion',None)
        manifest.pop('usa_script_vm436_promotion', None)  # exact historical source gate
        s=stage.validate_predecessor(manifest)
        previous=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_usa_short72_stage'})
        self.assertEqual((len(previous),sum(f['size'] for f in previous)),(2092,94760))
        self.assertFalse({f['name'] for f in previous} & {f['name'] for f in s['functions']})
    def test_final_claims_complete(self):
        claims=claimed_functions(load_manifest(stage.ROOT/'manifest.json'))
        self.assertEqual((len(claims),sum(f['size'] for f in claims)),(3052,207240))
    def test_modified_fixture_rejected(self):
        orig=stage.FIXTURE
        self.assertTrue(orig.is_file())
        with mock.patch.object(stage,'FIXTURE',stage.SOURCE/'short72-source-does-not-exist.json'):
            with self.assertRaises(FileNotFoundError):stage.fixture()
    def test_duplicate_original_address_rejected(self):
        manifest=load_manifest(stage.ROOT/'results/manifest_2165_before_native151_20261123.json')
        manifest.pop('usa_script_vm_dual_reference',None)
        manifest.pop('usa_script_vm440_promotion',None)
        manifest.pop('usa_native151_promotion',None)
        manifest.pop('usa_script_vm436_promotion', None)  # immutable historical stage
        prior=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_usa_short72_stage'})
        data=copy.deepcopy(stage.fixture())
        data['functions'][0]['rom_offset']=prior[0]['rom_offset']
        with mock.patch.object(stage,'fixture',return_value=data):
            with self.assertRaises(ValueError):stage.validate_predecessor(manifest)
if __name__=='__main__':unittest.main()
