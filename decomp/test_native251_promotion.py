import unittest,hashlib
from unittest.mock import patch
from decomp import native251_promotion as stage
from decomp import native251_integrity as jp
from decomp.verify import load_manifest,claimed_functions,ROOT
class Native251Tests(unittest.TestCase):
    def test_all_original_source_hashes_and_claims(self):
        fs=stage.validate_predecessor(load_manifest(ROOT/'results/manifest_2316_before_vm440_20261123.json'))
        self.assertEqual((len(fs),sum(x['original_bytes'] for x in fs)),(151,9808))
        jpfs=stage.rows('japan_0');stage.verify_japan_rows(jpfs)
        self.assertEqual((len(jpfs),sum(x['original_bytes'] for x in jpfs)),(100,7136))
        self.assertEqual(len({(x['region'],x['rom_offset']) for x in fs+jpfs}),251)
        self.assertEqual(len(claimed_functions(load_manifest(ROOT/'manifest.json'))),3039)
    def test_source_manifest_tamper_rejected(self):
        with patch.object(stage,'MANIFEST_SHA','0'*64):
            with self.assertRaises(ValueError):stage.rows('usa')
    def test_japan_full_stored_transaction(self):
        self.assertEqual(jp.validate()['status'],'PASS')
