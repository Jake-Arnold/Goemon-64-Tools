"""ROM-free fail-closed checks for three newly exact Japanese original-main C functions."""
from __future__ import annotations
import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from decomp import japan_usa_main_three as current
from decomp import japan_usa_main_two as prior
from decomp import japan_noop_port as image

class TestJapanUSAOriginalMainThree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=current.manifest()

    def test_original_region_and_count(self):
        self.assertEqual((self.m['prior_c'],self.m['new_c'],self.m['total_c']),(429,3,432))
        self.assertEqual((self.m['prior_bytes'],self.m['new_bytes'],self.m['total_bytes']),(9980,428,10408))
        self.assertEqual(prior.manifest()['total_c'],429)

    def test_exact_original_addresses_and_sources(self):
        for x in self.m['functions']:
            p=current.HERE.parent/x['source_path']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['source_sha256'])
            self.assertEqual(len(x['code_sha256']),64)
            self.assertEqual(int(x['jp'].rsplit('_',1)[1],16),x['jp_rom'])
            self.assertEqual(int(x['jp'].split('_')[1],16),x['vma'])
            self.assertEqual('main',x['section'])

    def test_ported_source_is_c_and_not_rom_literal(self):
        for x in self.m['functions']:
            s=current.source_text(x)
            self.assertIn(x['jp'],s)
            self.assertNotIn(x['usa'],s)
            self.assertNotIn('GLOBAL_ASM',s)
            self.assertNotIn('asm volatile',s)
            self.assertNotIn('0x3E228, 340',s)

    def test_three_original_source_owners(self):
        self.assertEqual(len({x['current_asm_owner'] for x in self.m['functions']}),3)
        self.assertEqual(sorted(x['sz'] for x in self.m['functions']),[32,56,340])
        spans=sorted((x['jp_rom'],x['jp_rom']+x['sz']) for x in self.m['functions'])
        for a,b in zip(spans,spans[1:]):self.assertLessEqual(a[1],b[0])

    def test_duplicate_function_rejected(self):
        m=copy.deepcopy(self.m);m['functions'][1]['jp']=m['functions'][0]['jp'];self.reject(m)

    def test_wrong_region_rejected(self):
        m=copy.deepcopy(self.m);m['region']='usa';self.reject(m)

    def test_original_usa_source_hash_rejected(self):
        m=copy.deepcopy(self.m);m['functions'][0]['source_sha256']='0'*64;self.reject(m)

    def test_unknown_original_linker_owner_rejected(self):
        m=copy.deepcopy(self.m);m['functions'][0]['current_asm_owner']='asm/usa/other.s';self.reject(m)

    def test_wrong_function_bytes_rejected(self):
        m=copy.deepcopy(self.m);m['new_bytes']+=4;self.reject(m)

    def test_original_rom_unavailable_rejected(self):
        with patch.object(image,'original_image',side_effect=ValueError('JP original ROM not provided')):
            with self.assertRaisesRegex(ValueError,'JP original ROM not provided'):
                current.stage(Path('/nonexistent'),self.m)

    def test_build_chain_starts_with_prior_429_gate(self):
        s=(current.HERE/'build_japan_usa_main_432.sh').read_text()
        self.assertIn('build_japan_usa_main_429.sh',s)
        self.assertIn('set -euo pipefail',s)
        self.assertIn('verify',s)

    @staticmethod
    def reject(m):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'manifest.json';path.write_text(json.dumps(m)+'\n')
            with patch.object(current,'MANIFEST',path):
                with unittest.TestCase().assertRaises(ValueError):current.manifest()

if __name__=='__main__':unittest.main()
