"""Original-address structural checks for USA VM resource lookup at 0x8003F038.

Requires privately reconstructed MIPS assembly derived from the SHA-pinned ROM.
Does not prove that a proposed C translation matches original instructions.
"""
from pathlib import Path
import argparse
import re
import unittest

START = 0x8003F038
END = 0x8003F0FC
ROM_OFFSET = 0x3FC38
ANCHORS = {
    0x8003F038: r'addiu\s+\$sp,\s*\$sp,\s*-0x28',
    0x8003F04C: r'bne\s+\$a0,\s*\$at,\s*\.L8003F05C_3FC5C',
    0x8003F05C: r'bgez\s+\$a1,\s*\.L8003F06C_3FC6C',
    0x8003F060: r'sra\s+\$v1,\s*\$a1,\s*1',
    0x8003F064: r'addiu\s+\$at,\s*\$a1,\s*0x1',
    0x8003F06C: r'sll\s+\$t6,\s*\$v1,\s*1',
    0x8003F078: r'lh\s+\$v0,\s*%lo\(D_80077894_78494\)\(\$v0\)',
    0x8003F088: r'jal\s+func_800141C4_14DC4',
    0x8003F09C: r'jal\s+func_80013B14_14714',
    0x8003F0A0: r'lhu\s+\$a0,\s*0x1A\(\$sp\)',
    0x8003F0A4: r'jal\s+func_800141C4_14DC4',
    0x8003F0B0: r'bne\s+\$v0,\s*\$at,\s*\.L8003F0C0_3FCC0',
    0x8003F0CC: r'beqz\s+\$at,\s*\.L8003F0E8_3FCE8',
    0x8003F0D4: r'bgez\s+\$t9,\s*\.L8003F0E4_3FCE4',
    0x8003F0E4: r'addu\s+\$v1,\s*\$v0,\s*\$t0',
    0x8003F0F4: r'jr\s+\$ra',
}
ROW = re.compile(r'/\*\s+([0-9A-Fa-f]+)\s+(8003[0-9A-Fa-f]{4})\s+[0-9A-Fa-f]{8}\s*\*/\s*(.*)')

def parse_rows(source):
    found = {}
    for line in source.splitlines():
        hit = ROW.search(line)
        if hit:
            address = int(hit.group(2), 16)
            if address in found:
                raise ValueError(f'duplicate original VMA: {address:#x}')
            offset = int(hit.group(1), 16)
            if offset != ROM_OFFSET + address - START:
                raise AssertionError(f'ROM/VMA offset mismatch {address:#x}')
            found[address] = hit.group(3).strip()
    return found

def verify(source):
    got = parse_rows(source)
    expected = set(range(START, END, 4))
    if set(got) != expected:
        raise AssertionError('original 49-word extent/address sequence differs')
    for address, pattern in ANCHORS.items():
        if re.fullmatch(pattern, got[address]) is None:
            raise AssertionError(f'original instruction mismatch at {address:#x}: {got[address]}')
    print(f'VM resource: {len(got)} original address rows, {len(ANCHORS)} control-flow guards passed')

class ParserTests(unittest.TestCase):
    def test_empty_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'extent'):
            verify('')
    def test_duplicate_rejected(self):
        row = '/* 3FC38 8003F038 00000000 */ addiu $sp, $sp, -0x28'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            parse_rows(f'{row}\n{row}\n')
    def test_misaligned_origin_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'ROM/VMA'):
            parse_rows('/* 3FC3C 8003F038 00000000 */ nop')
    def test_missing_instruction_rejected(self):
        source = '\n'.join('/* %05X %08X 00000000 */ nop' % (ROM_OFFSET+4*i, START+4*i) for i in range(49))
        with self.assertRaisesRegex(AssertionError, 'mismatch'):
            verify(source)
    def test_guard_count(self):
        self.assertEqual(len(ANCHORS),16)
        self.assertIn(0x8003F0A0, ANCHORS)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('original',type=Path,nargs='?')
    args=ap.parse_args()
    if args.original: verify(args.original.read_text(encoding='utf-8'))
    else: unittest.main(argv=['test_original'])
