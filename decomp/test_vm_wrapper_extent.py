"""Verify the original USA VM wrapper's exact *48-byte* function extent.

The original private Splat assembly has 12 instructions / 48 bytes, not 56.
The independent readelf inventory historically reports candidate_size=56,
which is a candidate layout problem, NOT the archived original extent.

Run with private --rom to verify the pinned extent directly, or provide both
private --asm and --rom to compare the listing to the image. Neither file is
checked into Git. Synthetic parser tests are always runnable without a ROM.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct
import unittest

FUNCTION = 'func_8003F6E8_402E8'
VMA = 0x8003F6E8
OFFSET = 0x402E8
WORDS = 12
SIZE = WORDS * 4
VMA_BIAS = 0x7FFFF400
SHA256 = 'fd5b89364249c531ad5a2eaed23b97dccf062444ac92c1ddd250fb9f1ca097dd'
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_SIZE = 33554432
ROW = re.compile(r'/\*\s+([0-9A-Fa-f]+)\s+(8003[0-9A-Fa-f]{4})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)')


def original_rows(source: str) -> list[tuple[int, str]]:
    lines = source.splitlines()
    starts = [idx for idx, line in enumerate(lines)
              if re.fullmatch(r'glabel\s+' + re.escape(FUNCTION) + r'\s*', line.strip())]
    if len(starts) != 1:
        raise ValueError('missing or ambiguous function glabel')
    begin = starts[0]
    ends = [idx for idx in range(begin + 1, len(lines))
            if re.fullmatch(r'endlabel\s+' + re.escape(FUNCTION) + r'\s*', lines[idx].strip())]
    if len(ends) != 1:
        raise ValueError('missing or ambiguous function endlabel')
    end = ends[0]
    if any(re.match(r'(?:glabel|endlabel)\s+', line.strip()) for line in lines[begin + 1:end]):
        raise ValueError('nested labels inside wrapper')
    parsed = []
    for line in lines[begin + 1:end]:
        match = ROW.search(line)
        if match:
            index = len(parsed)
            rom = int(match.group(1), 16)
            address = int(match.group(2), 16)
            if rom != OFFSET + 4 * index or address != VMA + 4 * index:
                raise ValueError(f'noncontiguous ROM/VMA at {address:#x}')
            parsed.append((int(match.group(3), 16), match.group(4).strip()))
    if len(parsed) != WORDS:
        raise ValueError(f'original wrapper must contain 12 words (48 bytes), not {len(parsed)}')
    for index, regex in ((8, r'jr\s+\$ra'), (9, r'nop'),
                         (10, r'jr\s+\$ra'), (11, r'nop')):
        if re.fullmatch(regex, parsed[index][1]) is None:
            raise ValueError(f'wrong return/tail instruction at offset +0x{index*4:X}')
    return parsed


def verify_rom_extent(rom: bytes) -> bytes:
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('reference ROM size or SHA-1 mismatch')
    data = rom[OFFSET:OFFSET + SIZE]
    if len(data) != SIZE or hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError('original 48-byte function SHA-256 mismatch')
    if OFFSET != VMA - VMA_BIAS:
        raise ValueError('original VMA/ROM mapping differs')
    expected_tail = (0x03E00008, 0x00000000, 0x03E00008, 0x00000000)
    tail = tuple(word[0] for word in struct.iter_unpack('>I', data[-16:]))
    if tail != expected_tail:
        raise ValueError('original wrapper must end in two jr $ra/nop pairs')
    return data


def verify_private_rom(asm_text: str, rom_path: Path) -> None:
    rows = original_rows(asm_text)
    data = b''.join(struct.pack('>I', word) for word, _ in rows)
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError('original 48-byte function SHA-256 mismatch')
    rom_data = verify_rom_extent(rom_path.read_bytes())
    if rom_data != data:
        raise ValueError('original instruction bytes not found at original ROM offset')


class WrapperExtentTests(unittest.TestCase):
    @staticmethod
    def synthetic(count=12):
        rows = []
        for idx in range(count):
            op = 'jr $ra' if idx in (8, 10) else 'nop'
            rows.append(f'/* {OFFSET+4*idx:X} {VMA+4*idx:08X} 00000000 */ {op}')
        return 'glabel '+FUNCTION+'\n'+'\n'.join(rows)+'\nendlabel '+FUNCTION

    def test_twelve_word_extent_and_double_return_shape(self):
        self.assertEqual(len(original_rows(self.synthetic())), 12)
        self.assertEqual(SIZE, 48)
        self.assertEqual(OFFSET, VMA - VMA_BIAS)

    def test_56_byte_annotation_does_not_redefine_original_extent(self):
        with self.assertRaisesRegex(ValueError, '12 words'):
            original_rows(self.synthetic(14))

    def test_shortened_candidate_prefix_rejected(self):
        with self.assertRaisesRegex(ValueError, '12 words'):
            original_rows(self.synthetic(10))

    def test_missing_second_jr_rejected(self):
        s = self.synthetic().replace('/* 40310 8003F710 00000000 */ jr $ra',
                                     '/* 40310 8003F710 00000000 */ nop')
        with self.assertRaisesRegex(ValueError, 'return/tail'):
            original_rows(s)

    def test_duplicate_label_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            original_rows(self.synthetic()+'\nglabel '+FUNCTION)

    def test_noncontiguous_offset_rejected(self):
        s = self.synthetic().replace('/* 402E8 8003F6E8', '/* 402EC 8003F6E8')
        with self.assertRaisesRegex(ValueError, 'noncontiguous'):
            original_rows(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asm', type=Path)
    parser.add_argument('--rom', type=Path)
    args = parser.parse_args()
    if args.asm and not args.rom:
        parser.error('--asm requires --rom')
    if args.rom and args.asm:
        verify_private_rom(args.asm.read_text(encoding='utf-8'), args.rom)
        print('VM wrapper: 12/12 original words, exact 48-byte ROM extent and two returns passed')
    elif args.rom:
        verify_rom_extent(args.rom.read_bytes())
        print('VM wrapper: exact 48-byte original ROM extent and two jr $ra/nop tails passed')
    else:
        unittest.main(argv=['test_vm_wrapper_extent'], exit=False)
