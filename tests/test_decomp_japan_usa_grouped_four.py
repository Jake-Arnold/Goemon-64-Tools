"""Fail-closed ROM-free tests for four grouped USA-source Japanese C transfers."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from decomp import japan_usa_grouped_four as latest
from decomp import japan_usa_equivalent_two_remaining as jp423
from decomp import japan_noop_port as jp329

class TestJPGroupedFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=latest.manifest()

    def test_exact_counts_and_region(self):
        self.assertEqual((self.m['baseline_c'],self.m['added_c'],self.m['total_c']),(423,4,427))
        self.assertEqual((self.m['baseline_bytes'],self.m['added_bytes'],self.m['total_bytes']),(9676,216,9892))
        self.assertEqual(jp423.manifest()['total_functions'],423)

    def test_pinned_source_file_and_code_hashes(self):
        for x in self.m['candidates']:
            self.assertEqual(hashlib.sha256((latest.HERE.parent/x['source_path']).read_bytes()).hexdigest(),x['source_sha256'])
            self.assertEqual(x['jp_rom'],int(x['jp'].rsplit('_',1)[1],16))
            self.assertEqual(x['vma'],int(x['jp'].split('_')[1],16))
            self.assertEqual(len(x['code_sha256']),64)

    def test_port_is_real_c_not_instruction_literal(self):
        for x in self.m['candidates']:
            source=latest.source_text(x)
            self.assertIn(x['jp'],source)
            self.assertNotIn(x['usa'],source)
            self.assertNotIn('GLOBAL_ASM(',source)
            self.assertNotIn('asm volatile',source)
            self.assertNotIn('.word ',source)

    def test_original_ranges_are_disjoint(self):
        spans=sorted((x['jp_rom'],x['jp_rom']+x['sz']) for x in self.m['candidates'])
        for a,b in zip(spans,spans[1:]):self.assertLessEqual(a[1],b[0])

    def test_duplicate_symbol_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][1]['jp']=m['candidates'][0]['jp'];self.reject(m)

    def test_source_sha_change_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][0]['source_sha256']='0'*64;self.reject(m)

    def test_wrong_source_parent_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][0]['original_parent']='asm/usa/other.s';self.reject(m)

    def test_wrong_rom_region_rejected(self):
        m=copy.deepcopy(self.m);m['region']='usa';self.reject(m)

    def test_count_change_rejected(self):
        m=copy.deepcopy(self.m);m['total_bytes']+=4;self.reject(m)

    def test_original_rom_absence_fails_closed(self):
        with patch.object(jp329,'original_image',side_effect=ValueError('original JP ROM missing')):
            with self.assertRaisesRegex(ValueError,'original JP ROM missing'):
                latest.stage(Path('/nonexistent'),self.m)

    def test_full_chain_uses_prior_423_stage(self):
        s=(latest.HERE/'build_japan_usa_grouped_427.sh').read_text()
        self.assertIn('build_japan_usa_equiv_423.sh',s)
        self.assertIn('set -euo pipefail',s)
        self.assertIn('verify',s)

    @staticmethod
    def reject(m):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manifest.json';path.write_text(json.dumps(m)+'\n')
            with patch.object(latest,'MANIFEST',path):
                with unittest.TestCase().assertRaises(ValueError):latest.manifest()

if __name__=='__main__':unittest.main()
