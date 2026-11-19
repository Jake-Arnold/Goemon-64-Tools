"""Synthetic safety tests; no proprietary Goemon ROM or generated game code."""
from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch
if __package__:
    from . import japan_recomp_codegen as port
else:
    import japan_recomp_codegen as port


def section_header(name, start, vram, size, executable=True):
    flags = 'CONTENTS, ALLOC, LOAD, RELOC, CODE' if executable else 'CONTENTS, ALLOC, LOAD, DATA'
    return f'  0 {name} {size:08x} {vram:08x} {start:08x} 00010000 2**4\n                  {flags}\n'


def section_spec():
    return section_header('.entry',0x1000,0x80000400,0x50)+section_header('.main',0x1050,0x80000450,0x100)+''.join(
        section_header(n, 0x2000+(i*0x100),0x08000000,0x80)
        for i,n in enumerate(port.OVERLAY_NAMES)) + section_header('.file_1',0x9000,0x05000000,0x40,False)


def sample_symbols():
    return ('80000400 g     F .entry 00000038 func_80000400_1000\n'
            '80000450 g     F .main 00000020 func_80000450_1050\n' +
            ''.join(f'08000000 g     F {name} 00000020 func_overlay_{i}\n'
                    for i,name in enumerate(port.OVERLAY_NAMES)))


class JapaneseRecompilerPreparationTests(unittest.TestCase):
    def test_genuine_layout_parses_as_toml_with_entrypoint_alias(self):
        generated, report = port.assemble(section_spec(), sample_symbols())
        parsed = tomllib.loads(generated['mnsg.japan_0.syms.toml'])
        self.assertEqual(len(parsed['section']), 59)
        self.assertEqual(parsed['section'][0]['functions'][0]['name'],'recomp_entrypoint')
        self.assertEqual(report['function_symbols'], 59)
        self.assertEqual(report['overlay_sections'], 57)
        self.assertNotIn('func_80000400_1000',generated['mnsg.japan_0.syms.toml'])
        self.assertNotIn('func_80038210_38E10',generated['mnsg.japan_0.toml'])
        self.assertIn('PREPARED_NOT_EXECUTED',str(report))

    def test_data_only_segments_are_not_mistaken_for_code(self):
        parsed=port.parse_sections(section_spec())
        self.assertNotIn('.file_1',parsed)

    def test_missing_overlay_or_wrong_entry_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'Missing Japanese recompiler overlay'):
            port.parse_sections(section_spec().replace(' .file_80 ', ' .missing '))
        with self.assertRaisesRegex(ValueError,'entrypoint'):
            port.parse_sections(section_spec().replace('80000400', '80000500', 1))

    def test_overlapping_and_duplicate_functions_rejected(self):
        sections=port.parse_sections(section_spec())
        with self.assertRaisesRegex(ValueError,'Invalid, duplicate'):
            port.parse_functions(sample_symbols()+ '80000450 g     F .main 00000020 func_80000450_1050\n',sections)
        changed=sample_symbols().replace('00000020 func_80000450_1050','000000F0 func_80000450_1050')
        with self.assertRaisesRegex(ValueError,'outside'):
            port.parse_functions(changed.replace('000000F0', '00000110'),sections)

    def test_rom_section_metadata_comes_from_lma_not_file_offset(self):
        parsed=port.parse_sections(section_spec())
        self.assertEqual(parsed['.main']['rom'],0x1050)
        self.assertEqual(parsed['.main']['vram'],0x80000450)

    def test_refuses_to_overwrite_existing_output_before_tools(self):
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'candidate'
            output.mkdir()
            with self.assertRaisesRegex(FileExistsError,'exists'):
                port.prepare(Path(td), output)

if __name__=='__main__': unittest.main()
