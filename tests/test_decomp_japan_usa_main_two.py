"""Original-address JP main text-stage and USA source provenance checks."""
from __future__ import annotations
import hashlib
import copy
import tempfile
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from decomp import japan_usa_main_two as current
from decomp import japan_usa_grouped_four as prior
from decomp import japan_noop_port as image

class TestJPOriginalMainTwo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=current.manifest()

    def test_exact_original_counts(self):
        self.assertEqual((self.m['previous_c'],self.m['added_c'],self.m['total_c']),(427,2,429))
        self.assertEqual((self.m['previous_bytes'],self.m['added_bytes'],self.m['total_bytes']),(9892,88,9980))
        self.assertEqual(prior.manifest()['total_c'],427)

    def test_original_source_and_code_hashes(self):
        for x in self.m['candidates']:
            p=current.HERE.parent/x['source_path']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['source_sha256'])
            self.assertEqual(len(x['code_sha256']),64)
            self.assertEqual(x['jp_rom'],int(x['jp'].rsplit('_',1)[1],16))
            self.assertEqual(x['vma'],int(x['jp'].split('_')[1],16))

    def test_clean_ported_c_has_no_inline_assembly(self):
        for x in self.m['candidates']:
            c=current.source_text(x)
            self.assertIn(x['jp'],c)
            self.assertNotIn(x['usa'],c)
            self.assertNotIn('GLOBAL_ASM',c)
            self.assertNotIn('asm volatile',c)
            self.assertNotIn('.word ',c)

    def test_disjoint_contiguous_original_main_functions(self):
        a,b=sorted(self.m['candidates'],key=lambda x:x['jp_rom'])
        self.assertEqual(a['jp_rom']+a['sz'],b['jp_rom'])
        self.assertEqual((a['jp_rom'],b['jp_rom']),(0x4D10,0x4D38))

    def test_duplicate_symbol_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][1]['jp']=m['candidates'][0]['jp'];self._reject(m)

    def test_wrong_original_main_owner_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][0]['original_parent']='asm/usa/main.s';self._reject(m)

    def test_wrong_region_rejected(self):
        m=copy.deepcopy(self.m);m['region']='usa';self._reject(m)

    def test_unreviewed_source_rejected(self):
        m=copy.deepcopy(self.m);m['candidates'][0]['source_path']='decomp/research/random.c';self._reject(m)

    def test_wrong_byte_count_rejected(self):
        m=copy.deepcopy(self.m);m['added_bytes']=92;self._reject(m)

    def test_rom_absent_fail_closed(self):
        with patch.object(image,'original_image',side_effect=ValueError('original ROM unavailable')):
            with self.assertRaisesRegex(ValueError,'original ROM unavailable'):
                current.stage(Path('/nonexistent'),self.m)

    def test_full_chain_rebuilds_427_first(self):
        script=(current.HERE/'build_japan_usa_main_429.sh').read_text()
        self.assertIn('build_japan_usa_grouped_427.sh',script)
        self.assertIn('set -euo pipefail',script)
        self.assertIn('verify',script)

    @staticmethod
    def _reject(m):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'m.json';path.write_text(json.dumps(m)+'\n')
            with patch.object(current,'MANIFEST',path):
                with unittest.TestCase().assertRaises(ValueError):current.manifest()

if __name__=='__main__':unittest.main()
