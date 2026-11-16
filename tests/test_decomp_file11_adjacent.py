"""ROM-free contract tests for original-USA file_11 adjacent matching-C research."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest
from unittest import mock

from decomp.research import file11_adjacent_native_probe as adj


class File11AdjacentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = adj.FIXTURES.read_bytes()
        cls.fixtures = adj.load_fixtures(cls.raw)
        cls.by_off = {r['rom_offset']: r for r in cls.fixtures['functions']}

    def test_source_metadata_is_exactly_68_original_functions(self):
        rows = self.fixtures['functions']
        self.assertEqual(len(rows), 68)
        self.assertEqual(sum(r['size'] for r in rows), 2416)
        self.assertEqual(len({r['name'] for r in rows}), 68)
        self.assertEqual(len({r['rom_offset'] for r in rows}), 68)
        self.assertTrue(all(row['name'].endswith(f'_{row["rom_offset"]:X}') for row in rows))

    def test_source_files_are_reproducible_without_original_rom(self):
        self.assertEqual(adj.load_fixtures(self.raw), self.fixtures)
        self.assertEqual(self.raw, (json.dumps(self.fixtures, indent=2)+'\n').encode())
        self.assertEqual(self.fixtures['decompressed_rom_sha1'], adj.ROM_SHA1)
        self.assertEqual(self.fixtures['generated_asm_sha256'], adj.EXPECTED_ASM_SHA256)

    def test_group_boundaries_are_contiguous_and_nonoverlapping(self):
        groups = self.fixtures['adjacent_groups']
        self.assertEqual(len(groups), 13)
        self.assertEqual(sum(len(g['function_offsets']) for g in groups), 42)
        self.assertEqual(sum(g['end']-g['start'] for g in groups), 1576)
        offsets=[]
        for group in groups:
            self.assertEqual(group['start'], group['function_offsets'][0])
            self.assertEqual(group['end'], group['function_offsets'][-1]+self.by_off[group['function_offsets'][-1]]['size'])
            for a,b in zip(group['function_offsets'],group['function_offsets'][1:]):
                self.assertEqual(a + self.by_off[a]['size'], b)
            offsets.extend(group['function_offsets'])
        self.assertEqual(len(offsets),len(set(offsets)))

    def test_largest_eight_function_island_is_original_size(self):
        group=next(g for g in self.fixtures['adjacent_groups'] if g['start']==0x5A6F30)
        self.assertEqual(group['end'],0x5A7090)
        self.assertEqual(len(group['function_offsets']),8)
        self.assertEqual(group['end']-group['start'],352)
        src, symbols=adj.build_group_source([self.by_off[o] for o in group['function_offsets']])
        self.assertEqual(len(symbols),8)
        self.assertTrue(all(s in src for s in symbols))
        self.assertEqual(src.count('void func_'),8)

    def test_adjacent_character_state_clear_island(self):
        group=next(g for g in self.fixtures['adjacent_groups'] if g['start']==0x59EE00)
        self.assertEqual(group['function_offsets'],[0x59EE00,0x59EE24,0x59EE48])
        self.assertEqual(group['end']-group['start'],84)
        src, symbols=adj.build_group_source([self.by_off[o] for o in group['function_offsets']])
        self.assertFalse(symbols)
        for off in group['function_offsets']:
            self.assertIn(f'func_801E',src)
            self.assertIn(f'Actor_{off:06X}',src)

    def test_global_bit_set_and_clear_are_adjacent(self):
        group=next(g for g in self.fixtures['adjacent_groups'] if g['start']==0x5A4070)
        self.assertEqual(group['function_offsets'],[0x5A4070,0x5A4088])
        src,symbols=adj.build_group_source([self.by_off[o] for o in group['function_offsets']])
        self.assertEqual(set(symbols.values()),{0x8015CC30})
        self.assertEqual(len(symbols),2)
        self.assertIn('flags|=1',src)
        self.assertIn('flags&=~1u',src)

    def test_duplicate_named_types_and_callees_are_renamed_per_function(self):
        group=next(g for g in self.fixtures['adjacent_groups'] if g['start']==0x5AAC94)
        src,symbols=adj.build_group_source([self.by_off[o] for o in group['function_offsets']])
        self.assertEqual(len(symbols),3)
        self.assertEqual(len(set(symbols)),3)
        self.assertEqual(src.count('void func_'),4)

    def test_unknown_fixture_format_is_rejected(self):
        o=copy.deepcopy(self.fixtures)
        o['format']='unreviewed'
        with self.assertRaisesRegex(ValueError,'format'):
            adj.load_fixtures(json.dumps(o).encode())

    def test_original_rom_identity_cannot_be_changed(self):
        o=copy.deepcopy(self.fixtures)
        o['decompressed_rom_sha1']='0'*40
        with self.assertRaisesRegex(ValueError,'ROM/assembly'):
            adj.load_fixtures(json.dumps(o).encode())

    def test_missing_function_fails_before_rom_access(self):
        o=copy.deepcopy(self.fixtures)
        o['functions'].pop()
        with self.assertRaisesRegex(ValueError,'count'):
            adj.load_fixtures(json.dumps(o).encode())

    def test_missing_adjacent_group_fails_before_rom_access(self):
        o=copy.deepcopy(self.fixtures)
        o['adjacent_groups'].pop()
        with self.assertRaisesRegex(ValueError,'count'):
            adj.load_fixtures(json.dumps(o).encode())

    def test_wrong_original_rom_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'ROM authentication'):
            adj.checked_inputs(b'bad',b'bad',self.fixtures)

    def test_wrong_original_splat_sha_is_rejected(self):
        # Only bypass the ROM hash so this test can run without game assets.
        with mock.patch.object(adj,'digest',side_effect=lambda blob, algorithm='sha256':
                               adj.ROM_SHA1 if algorithm=='sha1' else '0'*64):
            with self.assertRaisesRegex(ValueError,'Splat assembly'):
                adj.checked_inputs(bytes(adj.EXPECTED_ROM_BYTES),b'bad',self.fixtures)

    def test_incomplete_original_function_inventory_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Incomplete'):
            adj.parse_assembly_index('nonmatching func_801CB460_587370, 0x64\n')

    def test_duplicate_original_function_addresses_are_rejected(self):
        text='\n'.join('nonmatching func_801CB460_587370, 0x64' for i in range(901))
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            adj.parse_assembly_index(text)

    def test_source_bindings_cover_all_expected_external_symbols(self):
        for row in self.fixtures['functions']:
            _, symbols=adj.build_group_source([row])
            self.assertEqual(len(symbols),len(row['bindings']))
            self.assertTrue(all(isinstance(addr,int) for addr in symbols.values()))

    def test_report_rejects_existing_output(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d:
            existing=Path(d)/'report.json'
            existing.write_text('{}')
            with self.assertRaises(SystemExit):
                adj.main(['--rom','missing','--asm','missing','--cc','missing',
                          '--ld','missing','--objcopy','missing','--report',str(existing)])


if __name__=='__main__':
    unittest.main()
