"""Fail-closed ROM-free test suite for final two exact-source USA/JP C equivalents."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp import japan_usa_equivalent_two_remaining as latest
from decomp import japan_usa_equivalent_thirtyseven_more as prior
from decomp import japan_noop_port as noop

class JapaneseUSAEquivalentTwoFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=latest.manifest()

    def test_original_identity_and_exact_counts(self):
        self.assertEqual((self.m['base_functions'],self.m['added_functions'],self.m['total_functions']), (421,2,423))
        self.assertEqual((self.m['base_bytes'],self.m['added_bytes'],self.m['total_bytes']), (9608,68,9676))
        self.assertEqual({x['jp'] for x in self.m['candidates']},{'func_0800B328_6C30A8','func_0800B308_6C3088'})

    def test_both_source_hashes_and_exact_jp_offsets(self):
        for x in self.m['candidates']:
            source=latest.HERE.parent/x['source_path']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),x['source_sha256'])
            self.assertEqual(x['jp_rom'],int(x['jp'].rsplit('_',1)[1],16))
            self.assertEqual(x['vma'],int(x['jp'].split('_')[1],16))
            self.assertIn(x['jp'],latest.c_source(x))
            self.assertNotIn(x['usa'],latest.c_source(x))
            self.assertEqual(x['original_parent'],'6B7D80.s')
            self.assertTrue(x['current_owner'].startswith('asm/japan_0/jpport_'))

    def test_source_has_no_rom_or_hardcoded_mips(self):
        for x in self.m['candidates']:
            s=latest.c_source(x)
            self.assertNotIn('GLOBAL_ASM',s)
            self.assertNotIn('asm volatile',s)

    def test_nonoverlapping_function_extents(self):
        bounds=sorted((x['jp_rom'],x['jp_rom']+x['sz']) for x in self.m['candidates'])
        self.assertLessEqual(bounds[0][1],bounds[1][0])
        for x in self.m['candidates']:
            self.assertLessEqual(x['owner_start'],x['jp_rom'])
            self.assertLessEqual(x['jp_rom']+x['sz'],x['owner_end'])

    def test_duplicate_jp_rejected(self):
        changed=copy.deepcopy(self.m)
        changed['candidates'][1]['jp']=changed['candidates'][0]['jp']
        self._reject(changed)

    def test_source_fingerprint_change_rejected(self):
        changed=copy.deepcopy(self.m)
        changed['candidates'][0]['source_sha256']='0'*64
        self._reject(changed)

    def test_code_authority_change_rejected(self):
        changed=copy.deepcopy(self.m)
        changed['total_bytes']+=4
        self._reject(changed)

    def test_wrong_overlay_source_rejected(self):
        changed=copy.deepcopy(self.m)
        changed['candidates'][0]['original_parent']='somewhere.s'
        self._reject(changed)

    def test_unavailable_original_rom_rejected_before_source_staging(self):
        with patch.object(noop,'original_image',side_effect=ValueError('original JAPAN unavailable')):
            with self.assertRaisesRegex(ValueError,'original JAPAN unavailable'):
                latest.stage(Path('/nonexistent'),self.m)

    def test_rebuild_chain_includes_every_earlier_stage(self):
        script=(latest.HERE/'build_japan_usa_equiv_423.sh').read_text()
        self.assertIn('build_japan_usa_equiv_421.sh',script)
        self.assertIn('verify',script)
        self.assertIn('set -euo pipefail',script)
        self.assertEqual(prior.manifest()['total_functions'],421)

    @staticmethod
    def _reject(changed):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'changed.json';file.write_text(json.dumps(changed)+'\n')
            with patch.object(latest,'MANIFEST',file):
                with unittest.TestCase().assertRaises(ValueError):latest.manifest()

if __name__=='__main__':unittest.main()
