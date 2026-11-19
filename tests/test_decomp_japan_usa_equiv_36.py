"""ROM-free provenance and fail-closed regression checks for Japanese 380-C stage."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp import japan_usa_equivalent_36 as port
from decomp import japan_usa_equivalent_eleven as old
from decomp import japan_noop_port as noop


class JapanUSAEquivalent36Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=port.manifest()

    def test_new_36_and_1492_original_instruction_bytes(self):
        m=self.fixture
        self.assertEqual((m['base_functions'],m['added_functions'],m['total_functions']), (344,36,380))
        self.assertEqual((m['base_bytes'],m['added_bytes'],m['total_bytes']), (6416,1492,7908))
        self.assertEqual(sum(x['sz'] for x in m['candidates']),1492)
        self.assertEqual(len({x['jp'] for x in m['candidates']}),36)

    def test_all_seven_overlays_have_sources(self):
        self.assertEqual({x['section'] for x in self.fixture['candidates']},
                         {'file_12','file_13','file_14','file_15','file_17','file_18','file_19'})
        self.assertEqual(len({x['original_parent'] for x in self.fixture['candidates']}),16)
        for x in self.fixture['candidates']:
            self.assertEqual(x['jp_rom'],int(x['jp'].rsplit('_',1)[-1],16))
            self.assertTrue(port.SRC.joinpath(x['usa']+'.c').is_file())

    def test_usa_verified_source_exactly_reemitted(self):
        for x in self.fixture['candidates']:
            src=port.c_source(x)
            self.assertIn(x['jp']+'(',src.replace(' (','('))
            self.assertNotIn(x['usa'],src)
            self.assertTrue(src.endswith('\n'))
            self.assertEqual(src.count(x['jp']),1)

    def test_reject_duplicate_original_jp_function(self):
        altered=copy.deepcopy(self.fixture)
        altered['candidates'][1]['jp']=altered['candidates'][0]['jp']
        self._rejected_manifest(altered)

    def test_reject_source_hash_mutation(self):
        altered=copy.deepcopy(self.fixture)
        altered['candidates'][0]['source_sha256']='0'*64
        self._rejected_manifest(altered)

    def test_reject_fabricated_usa_original_function(self):
        altered=copy.deepcopy(self.fixture)
        altered['candidates'][0]['usa']='func_99999999_999999'
        self._rejected_manifest(altered)

    def test_reject_rom_identity_drift(self):
        altered=copy.deepcopy(self.fixture)
        altered['original_jp_expanded_sha1']='0'*40
        self._rejected_manifest(altered)

    def test_original_address_and_range_deduplication(self):
        all_offsets=sorted((x['jp_rom'],x['jp_rom']+x['sz']) for x in self.fixture['candidates'])
        self.assertTrue(all(b<=c for (_,b),(c,_) in zip(all_offsets,all_offsets[1:])))
        previous={x['jp'] for x in old.manifest()['candidates']}
        self.assertFalse(previous.intersection(x['jp'] for x in self.fixture['candidates']))

    def test_assembly_linking_requires_original_rom(self):
        with patch.object(noop,'original_image',side_effect=ValueError('refuse unverified ROM')):
            with self.assertRaisesRegex(ValueError,'refuse unverified ROM'):
                port.stage(Path('/unused/not/a/repo'),self.fixture)

    def _rejected_manifest(self,manifest):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'invalid.json';p.write_text(json.dumps(manifest)+'\n')
            with patch.object(port,'MANIFEST',p):
                with self.assertRaises(ValueError):port.manifest()

if __name__=='__main__':unittest.main()
