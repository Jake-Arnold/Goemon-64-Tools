"""Structural checks for G64-090's ROM-bound return_zero.c audit.

The 13 assembly functions are separate Memory Pak routines, not zero-return
stubs. The optional private inputs verify every checked-in extent against the
pinned Splat disassembly and 32 MiB USA image without exposing instruction data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import unittest


ROOT = Path(__file__).resolve().parent
AUDIT_PATH = ROOT / 'plans/execution/2026-11-11-g64-090-return-zero-audit.json'
ROM_SIZE = 33_554_432
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
UPSTREAM_COMMIT = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
ROW = re.compile(r'/\*\s*([0-9A-Fa-f]+)\s+([0-9A-Fa-f]{8})\s+([0-9A-Fa-f]{8})\s*\*/')


def read_audit(path=AUDIT_PATH):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def verify_private_sources(asm_text, rom, audit):
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('reference ROM size or SHA-1 mismatch')
    source = audit['original_source']
    if source['upstream_commit'] != UPSTREAM_COMMIT:
        raise ValueError('original source commit differs from the pinned USA source')
    if hashlib.sha256(asm_text.encode()).hexdigest() != source['asm_sha256']:
        raise ValueError('pinned Splat assembly source hash mismatch')
    for item in [audit['existing_constant_return'], *audit['functions']]:
        name = item['name']
        offset = int(item['rom_offset'], 16)
        vma = int(item['vma'], 16)
        size = item['size_bytes']
        declarations = re.findall(r'^nonmatching\s+' + re.escape(name) + r',\s*0x([0-9A-Fa-f]+)\s*$',
                                  asm_text, re.MULTILINE)
        start = re.findall(r'^glabel\s+' + re.escape(name) + r'\s*$', asm_text, re.MULTILINE)
        end = re.findall(r'^endlabel\s+' + re.escape(name) + r'\s*$', asm_text, re.MULTILINE)
        if len(declarations) != 1 or len(start) != 1 or len(end) != 1:
            raise ValueError('missing or ambiguous original assembly boundary: ' + name)
        if int(declarations[0], 16) != size:
            raise ValueError('original Splat size differs: ' + name)
        begin = re.search(r'^glabel\s+' + re.escape(name) + r'\s*$', asm_text, re.MULTILINE)
        finish = re.search(r'^endlabel\s+' + re.escape(name) + r'\s*$', asm_text[begin.end():], re.MULTILINE)
        body = asm_text[begin.start():begin.end() + finish.end()]
        words = []
        for line in body.splitlines():
            match = ROW.search(line)
            if not match:
                continue
            index = len(words)
            if int(match[1], 16) != offset + index * 4 or int(match[2], 16) != vma + index * 4:
                raise ValueError('noncontiguous original ROM/VMA annotations: ' + name)
            words.append(int(match[3], 16))
        if len(words) * 4 != size:
            raise ValueError('original instruction count disagrees with size: ' + name)
        assembly_bytes = b''.join(struct.pack('>I', word) for word in words)
        rom_bytes = rom[offset:offset + size]
        if len(rom_bytes) != size or assembly_bytes != rom_bytes:
            raise ValueError('assembly words do not match original ROM extent: ' + name)
        if hashlib.sha256(rom_bytes).hexdigest() != item['sha256']:
            raise ValueError('original function hash mismatch: ' + name)
    return len(audit['functions'])


class ReturnZeroAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = read_audit()
        cls.manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
        cls.proof = json.loads((ROOT / 'results/combined.json').read_text(encoding='utf-8'))

    def test_audit_covers_exact_manifest_assembly_set(self):
        units = [unit for unit in self.manifest['units'] if unit['source'] == 'return_zero.c']
        self.assertEqual(len(units), 1)
        expected = units[0]['assembly_functions']
        self.assertEqual([item['name'] for item in self.audit['functions']], expected)
        self.assertEqual(len(expected), 13)
        self.assertEqual(self.audit['unit']['name'], 'return_zero.c')

    def test_each_stub_has_extent_effect_cfg_and_nonzero_classification(self):
        for item in self.audit['functions']:
            with self.subTest(function=item['name']):
                self.assertGreater(item['size_bytes'], 0)
                self.assertEqual(item['vma'], '0x' + item['name'].split('_')[1].upper())
                self.assertEqual(item['rom_offset'], '0x' + item['name'].split('_')[2].upper())
                self.assertTrue(item['side_effects'])
                self.assertTrue(item['cfg_classification'])
                self.assertFalse(item['constant_zero'])
                self.assertIn('GLOBAL_ASM', item['disposition'])

    def test_neighboring_c_stub_is_the_actual_zero_return(self):
        item = self.audit['existing_constant_return']
        units = [unit for unit in self.manifest['units'] if unit['source'] == 'return_zero.c']
        function = next(fn for fn in units[0]['functions'] if fn['name'] == item['name'])
        self.assertEqual(function['size'], item['size_bytes'])
        self.assertIn('return 0;', (ROOT / 'return_zero.c').read_text(encoding='utf-8'))
        matched = [fn for fn in self.proof['comparison']['functions'] if fn['name'] == item['name']]
        self.assertEqual(len(matched), 1)
        self.assertTrue(matched[0]['matched'])

    def test_no_g2_promotion_is_reported(self):
        self.assertEqual(self.audit['decision']['matching_c_delta'], 0)
        self.assertEqual(self.audit['decision']['full_rom_g2'], 'NOT_RUN')
        self.assertEqual(self.audit['decision']['inventory_rebuild'], 'NOT_RUN')
        self.assertEqual(self.audit['decision']['candidate_count'], 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asm', type=Path)
    parser.add_argument('--rom', type=Path)
    args = parser.parse_args()
    if bool(args.asm) != bool(args.rom):
        parser.error('--asm and --rom must be supplied together')
    if args.asm and args.rom:
        count = verify_private_sources(args.asm.read_text(encoding='utf-8'), args.rom.read_bytes(), read_audit())
        print(f'Return-zero audit: {count}/13 exact extents match the pinned original ROM')
    else:
        unittest.main(argv=['test_return_zero_audit'], exit=False)
