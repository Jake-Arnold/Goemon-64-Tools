"""ROM-free safety and provenance tests for separately native-proved JP 4+37 C."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp import japan_usa_equivalent_four_more as four
from decomp import japan_usa_equivalent_thirtyseven_more as more
from decomp import japan_noop_port as noop

class JapaneseUSAExtra41Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=four.manifest()
        cls.b=more.manifest()

    def test_exact_counts_and_instruction_bytes(self):
        self.assertEqual((self.a['base_functions'],self.a['added_functions'],self.a['total_functions']), (380,4,384))
        self.assertEqual((self.a['base_bytes'],self.a['added_bytes'],self.a['total_bytes']), (7908,80,7988))
        self.assertEqual((self.b['base_functions'],self.b['added_functions'],self.b['total_functions']), (384,37,421))
        self.assertEqual((self.b['base_bytes'],self.b['added_bytes'],self.b['total_bytes']), (7988,1620,9608))

    def test_distinct_original_jp_function_ranges(self):
        candidates=self.a['candidates']+self.b['candidates']
        self.assertEqual(len({x['jp'] for x in candidates}),41)
        self.assertEqual(sum(x['sz'] for x in candidates),1700)
        boundaries=sorted((x['jp_rom'],x['jp_rom']+x['sz']) for x in candidates)
        self.assertTrue(all(e<=n for (_,e),(n,_) in zip(boundaries,boundaries[1:])))

    def test_all_source_hashes_match_and_renamed_text(self):
        for module,manifest in ((four,self.a),(more,self.b)):
            for x in manifest['candidates']:
                source=module.HERE.parent/x['source_path']
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),x['source_sha256'])
                generated=module.c_source(x)
                self.assertEqual(generated.count(x['jp']),1)
                self.assertNotIn(x['usa'],generated)
                self.assertNotIn('GLOBAL_ASM',generated)
                self.assertEqual(x['jp_rom'],int(x['jp'].rsplit('_',1)[1],16))
                self.assertEqual(x['vma'],int(x['jp'].split('_')[1],16))

    def test_original_source_owner_bounds_pinned(self):
        for x in self.b['candidates']:
            self.assertLessEqual(x['owner_start'],x['jp_rom'])
            self.assertLessEqual(x['jp_rom']+x['sz'],x['owner_end'])
            self.assertTrue(x['current_owner'].startswith('asm/japan_0/'))
        self.assertEqual({x['section'] for x in self.a['candidates']},{'file_24','file_29'})

    def test_reject_function_double_count(self):
        altered=copy.deepcopy(self.b)
        altered['candidates'][1]['jp']=altered['candidates'][0]['jp']
        self._reject(more,altered)

    def test_reject_source_modification(self):
        altered=copy.deepcopy(self.a)
        altered['candidates'][0]['source_sha256']='0'*64
        self._reject(four,altered)

    def test_reject_rom_hash_drift(self):
        altered=copy.deepcopy(self.b)
        altered['original_jp_expanded_sha1']='0'*40
        self._reject(more,altered)

    def test_reject_invented_jp_source_owner(self):
        altered=copy.deepcopy(self.b)
        altered['candidates'][0]['original_parent']='6B7D80.s'
        self._reject(more,altered)

    def test_reject_invented_source_file_path(self):
        altered=copy.deepcopy(self.b)
        altered['candidates'][0]['source_path']='../../../../etc/passwd'
        self._reject(more,altered)

    def test_reject_original_rom_unavailable(self):
        for module,manifest in ((four,self.a),(more,self.b)):
            with patch.object(noop,'original_image',side_effect=ValueError('missing original Japan ROM')):
                with self.assertRaisesRegex(ValueError,'missing original Japan ROM'):
                    module.stage(Path('/not/a/checkout'),manifest)

    def test_build_chain_keeps_complete_380_original_c(self):
        script=(four.HERE/'build_japan_usa_equiv_421.sh').read_text()
        self.assertIn('build_japan_usa_equiv_380.sh',script)
        self.assertIn('japan_usa_equivalent_four_more',script)
        self.assertIn('japan_usa_equivalent_thirtyseven_more',script)
        self.assertIn('verify',script)
        self.assertIn('set -euo pipefail',script)

    @staticmethod
    def _reject(module,data):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'invalid.json';p.write_text(json.dumps(data)+'\n')
            with patch.object(module,'MANIFEST',p):
                with unittest.TestCase().assertRaises(ValueError):module.manifest()

if __name__=='__main__':unittest.main()
