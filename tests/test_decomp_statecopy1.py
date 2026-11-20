"""Fail-closed identity checks for the new USA 0x35F98 C claim."""
from __future__ import annotations
import hashlib,json,unittest
from pathlib import Path
from decomp import overlay_statecopy1 as adapter
from decomp.verify import load_manifest,claimed_functions

class Statecopy1Tests(unittest.TestCase):
    def test_native_identity_and_live_deduplication(self):
        fixture=adapter.load_fixture();function=adapter.functions(fixture)[0]
        self.assertEqual(function['name'],'func_80035398_35F98')
        self.assertEqual((function['rom_offset'],function['vma'],function['size']),(0x35F98,0x80035398,12))
        self.assertEqual(function['original_code_sha256'],'2bde60ad28d9c7e327e3543580b3692be866a2f37c5c387d66cc2b05064e4071')
        source=(adapter.SOURCE_BASE/'statecopy1_000.c').read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(),fixture['units'][0]['source_sha256'])
        prior=json.loads((adapter.ROOT/'results/combined_1500_20261119.json').read_text())
        self.assertEqual(prior['comparison']['matched_functions'],1500)
        self.assertNotIn(function['name'],{f['name'] for f in prior['comparison']['functions']})
        current=load_manifest(adapter.ROOT/'manifest.json')
        names=[x['name'] for x in claimed_functions({k:v for k,v in current.items() if k!='overlay_checkpoint500_stage'})]
        self.assertEqual(len(names),1617)
        self.assertEqual(len(claimed_functions({k:v for k,v in current.items() if k not in ('overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage')})),1501)
        self.assertEqual(names.count(function['name']),1)
    def test_wrong_image_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'Invalid USA original ROM'):
            adapter.validate_sources(b'bad',adapter.load_fixture())
    def test_modified_source_does_not_match_authenticated_digest(self):
        fixture=adapter.load_fixture()
        expected=fixture['units'][0]['source_sha256']
        self.assertNotEqual(hashlib.sha256(b'void f(void) {}').hexdigest(),expected)


if __name__=='__main__': unittest.main()
