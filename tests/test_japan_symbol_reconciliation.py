"""Synthetic tests for original-USA-symbol gate on Japanese call-target anchors."""
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import yaml

from decomp.japan_symbol_reconciliation import reconcile, FORMAT
from decomp.japan_function_map import SHA1


def write_splat(path: Path, region: str, rom: int, vram: int):
    path.write_text(yaml.safe_dump({
        'sha1': SHA1[region],
        'segments': [{'name': 'file_13', 'type': 'code', 'start': rom, 'vram': vram,
                      'subsegments': [[rom, 'asm'], [rom + 0x200, 'data']]}]
    }))


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        d = Path(self.temp.name)
        self.us_splat, self.jp_splat, self.syms = d/'usa.yaml', d/'jp.yaml', d/'us.toml'
        self.urom, self.jrom = 0x1000, 0x1800
        self.uvram, self.jvram = 0x801CB460, 0x801D0B90
        write_splat(self.us_splat, 'usa', self.urom, self.uvram)
        write_splat(self.jp_splat, 'japan_0', self.jrom, self.jvram)
        self.usa, self.jp = bytearray(0x3000), bytearray(0x3000)
        self.usa_pos, self.jp_pos = 0x20, 0x40
        for i in range(32):
            # Fully matching normalised MIPS but differing immediate values.
            w = (0x23 << 26) | (((i % 13) + 1) << 21) | (((i * 3 % 17) + 1) << 16) | (i+1)
            struct.pack_into('>I', self.usa, self.urom+self.usa_pos+4*i, w)
            struct.pack_into('>I', self.jp, self.jrom+self.jp_pos+4*i, (w&0xFFFF0000)|(i+99))
        self.syms.write_text(f'''[[section]]
name = ".file_13"
rom = {self.urom}
vram = {self.uvram}
size = 0x200
functions = [{{name = "original", vram = {self.uvram+self.usa_pos}, size = 0x80}}]
''')
        self.candidate = dict(format='goemon-japan-overlay-direct-jal-anchors-v1', sha1=dict(SHA1), signature_words=16,
                              mappings=[dict(section='.file_13',
                                            usa_vram=f'0x{self.uvram+self.usa_pos:X}',
                                            japan_vram=f'0x{self.jvram+self.jp_pos:X}',
                                            usa_rom=f'0x{self.urom+self.usa_pos:X}',
                                            japan_rom=f'0x{self.jrom+self.jp_pos:X}')])

    def run_audit(self):
        return reconcile(bytes(self.usa), bytes(self.jp), self.us_splat, self.jp_splat, self.syms, self.candidate)

    def test_full_function_match_includes_original_name_and_byte_count(self):
        result = self.run_audit()
        self.assertEqual(result['format'], FORMAT)
        self.assertEqual(result['totals']['full_structure_match'], 1)
        self.assertEqual(result['totals']['full_structure_bytes'], 128)
        self.assertEqual(result['totals']['exact_instruction_words'], 0)
        self.assertEqual(result['matches'][0]['usa_symbol'], 'original')

    def test_different_opcode_rejects_full_function(self):
        struct.pack_into('>I', self.jp, self.jrom+self.jp_pos+4*20, 0xFFFFFFFF)
        result = self.run_audit()
        self.assertEqual(result['totals']['full_structure_mismatch'], 1)
        self.assertEqual(result['matches'], [])

    def test_bad_candidate_addresses_fail_closed(self):
        self.candidate['mappings'][0]['japan_rom'] = '0x7777'
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            self.run_audit()

    def test_candidate_forged_japanese_anchor_rejected(self):
        self.candidate['mappings'][0]['japan_vram'] = f'0x{self.jvram+self.jp_pos+4:X}'
        self.candidate['mappings'][0]['japan_rom'] = f'0x{self.jrom+self.jp_pos+4:X}'
        with self.assertRaisesRegex(ValueError, 'non-unique candidate anchor'):
            self.run_audit()

    def test_short_symbol_is_not_pretended_a_full_function(self):
        self.syms.write_text(self.syms.read_text().replace('size = 0x80', 'size = 0x20'))
        report = self.run_audit()
        self.assertEqual(report['totals']['too_short_for_full_validation'], 1)
        self.assertEqual(report['matches'], [])

    def test_unknown_usa_symbol_is_categorised(self):
        self.syms.write_text(self.syms.read_text().replace('size = 0x80', 'size = 0x80').replace(
            f'vram = {self.uvram+self.usa_pos}', f'vram = {self.uvram+self.usa_pos+4}'))
        report = self.run_audit()
        self.assertEqual(report['totals']['not_a_named_usa_function_start'], 1)
        self.assertEqual(report['totals']['symbols_without_jal_anchor'], 1)

    def test_duplicate_japanese_targets_rejected(self):
        self.candidate['mappings'].append(dict(self.candidate['mappings'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate candidate'):
            self.run_audit()

    def test_unsupported_candidate_hashes_rejected(self):
        self.candidate['sha1']['japan_0'] = 'x'
        with self.assertRaisesRegex(ValueError, 'incompatible'):
            self.run_audit()


if __name__ == '__main__':
    unittest.main()
