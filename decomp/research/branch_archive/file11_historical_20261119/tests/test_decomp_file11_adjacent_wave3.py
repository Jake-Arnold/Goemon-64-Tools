"""ROM-free fail-closed contract tests for USA file_11 third adjacency research."""
from __future__ import annotations

import copy
import json
import unittest

from decomp.research import file11_adjacent_wave3_probe as probe


class File11AdjacentWave3ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads(probe.SOURCES.read_text())
        cls.previous=(
            json.loads(probe.PREVIOUS_77.read_text()),
            json.loads(probe.PREVIOUS_68.read_text()),
            json.loads(probe.PREVIOUS_44.read_text()),
        )

    def validate(self, fixture=None, earlier=None):
        probe.validate_source_contract(
            copy.deepcopy(self.fixture if fixture is None else fixture),
            *(copy.deepcopy(self.previous if earlier is None else earlier))
        )

    def test_authentic_source_contract(self):
        self.validate()
        self.assertEqual(len(self.fixture['functions']),10)
        self.assertEqual(sum(x['size'] for x in self.fixture['functions']),488)
        self.assertEqual(len(self.fixture['adjacent_groups']),9)
        self.assertEqual(sum(g['end']-g['start'] for g in self.fixture['adjacent_groups']),984)

    def test_new_source_is_unique_and_sorted(self):
        f=self.fixture['functions']
        self.assertEqual([r['rom_offset'] for r in f],sorted({r['rom_offset'] for r in f}))
        earlier=[r['rom_offset'] for group in self.previous for r in group['functions']]
        self.assertFalse({r['rom_offset'] for r in f}&set(earlier))

    def test_original_vmas_and_production_protection(self):
        from decomp.overlay_file11 import FUNCTIONS
        from decomp.research.usa_file11_noop_groups import entries
        promoted={off for _,off,_,_ in FUNCTIONS}|{off for _,off in entries()}
        for row in self.fixture['functions']:
            self.assertEqual(row['vma'],probe.VMA_START+row['rom_offset']-probe.ROM_START)
            self.assertNotIn(row['rom_offset'],promoted)

    def test_all_new_functions_covered_once_by_adjacent_groups(self):
        groups=self.fixture['adjacent_groups']
        offsets=[off for group in groups for off in group['function_offsets']]
        self.assertEqual(len(offsets),len(set(offsets)))
        self.assertTrue({r['rom_offset'] for r in self.fixture['functions']}.issubset(set(offsets)))
        self.assertEqual(len(offsets),27)

    def test_reject_source_contract_name_mutation(self):
        f=copy.deepcopy(self.fixture);f['format']='unknown'
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_wrong_upstream_commit(self):
        f=copy.deepcopy(self.fixture);f['upstream_commit']='wrong'
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_prior_77_count_mutation(self):
        previous=copy.deepcopy(self.previous)
        previous[0]['exact_matching_functions']=76
        with self.assertRaises(ValueError):self.validate(earlier=previous)

    def test_reject_prior_44_function_missing(self):
        previous=copy.deepcopy(self.previous)
        previous[2]['functions'].pop()
        with self.assertRaises(ValueError):self.validate(earlier=previous)

    def test_reject_previous_function_relabelled_as_new(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][0]['rom_offset']=self.previous[2]['functions'][0]['rom_offset']
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_new_function_offset_duplication(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][1]['rom_offset']=f['functions'][0]['rom_offset']
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_new_function_vma_corruption(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][1]['vma']+=4
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_c_replaced_with_assembly(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][0]['source']='GLOBAL_ASM("any");'
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_unpinned_external_binding(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][0]['bindings']['handler']='0x0'
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_unknown_c_function_size(self):
        f=copy.deepcopy(self.fixture)
        f['functions'][0]['size']+=4
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_assembly_gap_inside_contiguous_unit(self):
        f=copy.deepcopy(self.fixture)
        f['adjacent_groups'][0]['function_offsets']=f['adjacent_groups'][0]['function_offsets'][:1]
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_overlapping_adjacent_islands(self):
        f=copy.deepcopy(self.fixture)
        f['adjacent_groups'][1]['function_offsets'][0]=f['adjacent_groups'][0]['function_offsets'][0]
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_unmatched_group_source_symbol(self):
        f=copy.deepcopy(self.fixture)
        name=f['functions'][0]['name']
        for group in f['adjacent_groups']:
            if f['functions'][0]['rom_offset'] in group['function_offsets']:
                group['source']=group['source'].replace(name+'(',name+'_wrong(')
                break
        with self.assertRaises(ValueError):self.validate(f)

    def test_reject_c_group_external_binding_corruption(self):
        f=copy.deepcopy(self.fixture)
        first=next(g for g in f['adjacent_groups'] if g['bindings'])
        first['bindings'][next(iter(first['bindings']))]='8020AAAA'
        with self.assertRaises(ValueError):self.validate(f)


if __name__=='__main__':
    unittest.main()
