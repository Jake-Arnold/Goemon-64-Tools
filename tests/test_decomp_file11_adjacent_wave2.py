"""ROM-free contract tests for 44 new USA file_11 C candidates and nine C islands.

These do not assert G2 or full-ROM promotion. Mutation tests use only the
caller-provided pinned ROM, assembly and source contracts.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from decomp.research import file11_adjacent_wave2_probe as wave2


class WaveTwoContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = json.loads(wave2.CURRENT.read_text(encoding='utf-8'))
        cls.prior68 = json.loads(wave2.PRIOR68.read_text(encoding='utf-8'))
        cls.prior77 = json.loads(wave2.PRIOR77.read_text(encoding='utf-8'))

    def test_pinned_source_inventory(self):
        rows=self.fixtures['functions']
        self.assertEqual(len(rows),44)
        self.assertEqual(sum(r['size'] for r in rows),1976)
        self.assertEqual(self.fixtures['decompressed_rom_sha1'],wave2.PINNED_ROM_SHA1)
        self.assertEqual(self.fixtures['generated_asm_sha256'],wave2.PINNED_ASM_SHA256)

    def test_44_unique_original_vm_as(self):
        rows=self.fixtures['functions']
        self.assertEqual(len({r['name'] for r in rows}),44)
        self.assertEqual(len({r['rom_offset'] for r in rows}),44)
        self.assertEqual([r['rom_offset'] for r in rows],sorted(r['rom_offset'] for r in rows))
        for r in rows:
            self.assertEqual(r['vma'],wave2.VMA_START+r['rom_offset']-wave2.ROM_START)

    def test_pinned_categories(self):
        from collections import Counter
        self.assertEqual(dict(Counter(r['category'] for r in self.fixtures['functions'])),{
            'fixed_event_dispatch':31,'state_initialiser':1,'state_copy':5,
            'byte_clamp':2,'state_flag':2,'state_predicate':3,
        })

    def test_no_overlap_with_previous_145(self):
        current={r['rom_offset'] for r in self.fixtures['functions']}
        prev={r['rom_offset'] for r in self.prior68['functions']}
        prev.update(r['rom_offset'] for r in self.prior77['functions'])
        self.assertFalse(current & prev)
        self.assertEqual(len(prev),145)

    def test_exact_group_counts(self):
        groups=self.fixtures['adjacent_groups']
        self.assertEqual(len(groups),9)
        self.assertEqual(sum(len(g['function_offsets']) for g in groups),44)
        self.assertEqual(sum(g['end']-g['start'] for g in groups),1892)

    def test_nine_function_actor_state_group(self):
        g=next(x for x in self.fixtures['adjacent_groups'] if x['start']==0x5AA138)
        self.assertEqual(g['end'],0x5AA320)
        self.assertEqual(len(g['function_offsets']),9)
        self.assertEqual(g['end']-g['start'],488)

    def test_mixed_group_has_previous_77_callbacks(self):
        g=next(x for x in self.fixtures['adjacent_groups'] if x['start']==0x5B8488)
        self.assertEqual(g['function_offsets'],[0x5B8488,0x5B8494,0x5B84A0,0x5B84D0])
        self.assertEqual(g['end'],0x5B8500)

    def test_state_typedef_namespace_separated(self):
        rows=[r for r in self.fixtures['functions'] if r['rom_offset'] in (0x5B84A0,0x5B84D0)]
        source,symbols=wave2.group_source(rows)
        self.assertIn('State_5B84A0',source)
        self.assertIn('State_5B84D0',source)
        self.assertEqual(set(symbols.values()),{0x8015C5C8})
        self.assertEqual(len(symbols),2)

    def test_fail_closed_on_bad_format(self):
        mutated=copy.deepcopy(self.fixtures)
        mutated['format']='invented'
        self.assertNotEqual(mutated['format'],wave2.REQUIRED_FORMAT)

    def test_new_c_source_cannot_embed_assembly(self):
        self.assertTrue(all('GLOBAL_ASM' not in r['source'] for r in self.fixtures['functions']))
        self.assertTrue(all('#include' not in r['source'] for r in self.fixtures['functions']))

    def test_all_research_rows_hold_hashes(self):
        self.assertTrue(all(len(r['original_sha256'])==64 for r in self.fixtures['functions']))
        self.assertTrue(all(r['source'] and r['name'] in r['source'] for r in self.fixtures['functions']))

    def test_previous_research_authentication(self):
        self.assertEqual(self.prior77['exact_matching_functions'],77)
        self.assertEqual(self.prior77['exact_matching_bytes'],2120)
        self.assertEqual(len(self.prior68['functions']),68)
        self.assertEqual(sum(x['size'] for x in self.prior68['functions']),2416)

    def test_report_is_explicitly_research_only(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/file11_adjacent_wave2_native_proof_20261116.json'
        evidence=json.loads(path.read_text(encoding='utf-8'))
        self.assertFalse(evidence['full_rom_g2_verified'])
        self.assertFalse(evidence['production_manifest_changed'])
        self.assertEqual(evidence['new_production_claims'],0)

    def test_proof_function_bytes_and_codes(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/file11_adjacent_wave2_native_proof_20261116.json'
        proof=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(proof['exact_new_functions'],44)
        self.assertEqual(proof['exact_new_bytes'],1976)
        self.assertEqual(proof['combined_research_candidates'],189)
        for r in proof['functions']:
            self.assertTrue(r['exact'])
            self.assertEqual(r['original_sha256'],r['candidate_sha256'])

    def test_proof_all_nine_groups_byte_exact(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/file11_adjacent_wave2_native_proof_20261116.json'
        proof=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(proof['exact_contiguous_groups'],9)
        self.assertEqual(proof['exact_grouped_functions'],44)
        self.assertEqual(proof['exact_grouped_new_functions'],37)
        self.assertEqual(proof['exact_grouped_bytes'],1892)
        for r in proof['groups']:
            self.assertTrue(r['exact'])
            self.assertEqual(r['original_sha256'],r['candidate_sha256'])

    def test_local_source_fixture_hash_matches_proof(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/file11_adjacent_wave2_native_proof_20261116.json'
        proof=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(proof['fixture_sha256'],wave2.sha(
            json.dumps(self.fixtures,sort_keys=True).encode('utf-8')))

    def test_no_production_claim_mutations(self):
        self.assertEqual(wave2.EXPECTED_NEW,44)
        self.assertEqual(wave2.EXPECTED_GROUPS,9)
        self.assertEqual(wave2.EXPECTED_NEW_BYTES,1976)
        self.assertEqual(wave2.EXPECTED_GROUP_BYTES,1892)

    def test_no_duplicate_group_member(self):
        offsets=[o for group in self.fixtures['adjacent_groups'] for o in group['function_offsets']]
        self.assertEqual(len(offsets),len(set(offsets)))


if __name__=='__main__':
    unittest.main()
