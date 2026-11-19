"""ROM-free fail-closed contract tests for JP file_13 USA-to-JP 11-function port."""
from __future__ import annotations
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from decomp import japan_usa_equivalent_eleven as eq
from decomp import japan_character_switch_four as sw
from decomp import japan_noop_port as noop


class JapaneseUsEquivalentEleven(unittest.TestCase):
    def test_pinned_native_verified_candidates(self):
        m=eq.manifest()
        cs=m['candidates']
        self.assertEqual((len(cs),sum(c['sz'] for c in cs)),(11,728))
        self.assertEqual(len({c['jp'] for c in cs}),11)
        self.assertEqual(len({c['usa'] for c in cs}),11)
        self.assertEqual({c['asm'] for c in cs},{'602FA0.s'})
        self.assertEqual((m['expected_matching_c'],m['expected_matching_bytes']),(344,6416))
        self.assertTrue(all(c['sz']>12 for c in cs))
        self.assertTrue(all(len(c['original_jp_instruction_sha256'])==64 for c in cs))

    def test_pinned_usa_archived_sources(self):
        for c in eq.manifest()['candidates']:
            src=eq.SRC_ROOT/(c['usa']+'.c')
            self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),c['source_sha256'])
            jp=eq.c_source(c)
            self.assertIn(c['jp'],jp)
            self.assertNotIn(c['usa'],jp)
            self.assertNotIn('GLOBAL_ASM',jp)

    def test_no_duplicate_japanese_original_function(self):
        existing=json.loads((eq.HERE/'regions/japan_0.json').read_text())
        base={fn['name'] for unit in existing['units'] for fn in unit['functions']}
        noop_names={n for p in noop.load_manifest()['parents'] for n,_ in p['c']}
        new={c['jp'] for c in eq.manifest()['candidates']}
        self.assertEqual((len(base),len(noop_names),len(sw.EXPECTED_NAMES),len(new)),(39,290,4,11))
        self.assertEqual(len(base|noop_names|sw.EXPECTED_NAMES|new),344)

    def test_mismatch_source_rejected(self):
        with patch.object(eq,'sha256',lambda b:'0'*64):
            with self.assertRaisesRegex(ValueError,'source changed'):
                eq.manifest()

    def test_repeated_candidate_rejected(self):
        original=eq.MANIFEST
        m=eq.manifest()
        m['candidates'][1]['jp']=m['candidates'][0]['jp']
        class FakePath:
            def read_text(self):return json.dumps(m)
        with patch.object(eq,'MANIFEST',FakePath()):
            with self.assertRaisesRegex(ValueError,'Duplicated'):
                eq.manifest()

    def test_original_boundaries_and_region(self):
        m=eq.manifest()
        self.assertEqual(m['region'],'japan_0')
        self.assertEqual(m['original_parent'],'602FA0.s')
        self.assertEqual(eq.ORIG_FRAG,'asm/japan_0/jpport_602FA0_000.s')
        self.assertTrue(all(0x602FA0<=c['jp_rom'] and c['jp_rom']+c['sz']<=0x6075CC for c in m['candidates']))
        offsets=sorted((c['jp_rom'],c['jp_rom']+c['sz']) for c in m['candidates'])
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(offsets,offsets[1:])))

    def test_previous_japan_stages_preserved(self):
        text=(eq.HERE/'build_japan_usa_equiv_344.sh').read_text()
        self.assertIn('build_japan_switch_333.sh',text)
        self.assertIn('japan_usa_equivalent_eleven',text)
        self.assertIn('run verify',text)
        self.assertIn('set -euo pipefail',text)

if __name__=='__main__':unittest.main()
