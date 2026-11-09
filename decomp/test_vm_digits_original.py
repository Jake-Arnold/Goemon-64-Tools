"""Private-original-assembly regression for USA VM digit-formatting 0x8003F480.

Pass original assembly regenerated from the user's pinned USA ROM. Do not commit
that assembly or game bytes. Structural checks alone are NOT a matching-C proof.
"""
import argparse
from pathlib import Path
import re
import unittest

ANCHORS = {
    0x8003F480: r'addiu\s+\$sp,\s*\$sp,\s*-0x18',
    0x8003F49C: r'jal\s+sprintf',
    0x8003F4A0: r'addiu\s+\$a0,\s*\$a0,\s*%lo\(D_801C7780_1C8380\)',
    0x8003F4B4: r'lbu\s+\$t6,\s*0x0\(\$a0\)',
    0x8003F4C0: r'beqz\s+\$t6,\s*\.L8003F4F8_400F8',
    0x8003F4C4: r'or\s+\$v0,\s*\$a1,\s*\$zero',
    0x8003F4D8: r'sh\s+\$t8,\s*0x0\(\$v0\)',
    0x8003F4DC: r'lbu\s+\$v1,\s*0x1\(\$a0\)',
    0x8003F4E8: r'bnel\s+\$v1,\s*\$zero,\s*\.L8003F4D8_400D8',
    0x8003F4EC: r'addiu\s+\$t8,\s*\$v1,\s*-0x30',
    0x8003F4F4: r'sw\s+\$a0,\s*%lo\(D_801C779C_1C839C\)\(\$at\)',
    0x8003F4FC: r'sh\s+\$t9,\s*0x0\(\$v0\)',
    0x8003F508: r'sw\s+\$v0,\s*%lo\(D_801C77DC_1C83DC\)\(\$at\)',
    0x8003F50C: r'jal\s+func_8003EB34_3F734',
    0x8003F510: r'lw\s+\$a0,\s*%lo\(D_801C7754_1C8354\)\(\$a0\)',
}
ROW = re.compile(r'/\*\s+[0-9A-Fa-f]+\s+(8003[0-9A-Fa-f]{4})\s+[0-9A-Fa-f]{8}\s*\*/\s*(.*)')

def instruction_rows(content):
    rows = {}
    for line in content.splitlines():
        m=ROW.search(line)
        if m:
            address=int(m.group(1),16)
            if address in rows:
                raise ValueError(f'duplicate original address {address:#x}')
            rows[address]=m.group(2).strip()
    return rows

def verify(content):
    rows=instruction_rows(content)
    if len(rows)!=41 or min(rows,default=0)!=0x8003F480 or max(rows,default=0)!=0x8003F520:
        raise AssertionError('original function extent is not 164 bytes / 41 words')
    for address,pattern in ANCHORS.items():
        if address not in rows or re.fullmatch(pattern,rows[address]) is None:
            raise AssertionError(f'{address:#x} mismatch: {rows.get(address)!r}; expected {pattern}')
    print(f'VM digits: 41 original instruction addresses; {len(ANCHORS)} guarded instructions')

class ParserNegativeControls(unittest.TestCase):
    def test_duplicate_address_rejected(self):
        row='/* 40080 8003F480 00000000 */ addiu $sp, $sp, -0x18'
        with self.assertRaisesRegex(ValueError,'duplicate'):
            instruction_rows(row+'\n'+row)
    def test_empty_rejected(self):
        with self.assertRaisesRegex(AssertionError,'extent'):
            verify('')
    def test_missing_anchors_rejected(self):
        content='\n'.join('/* %05X %08X 00000000 */ nop' %(0x40080+4*j,0x8003F480+4*j) for j in range(41))
        with self.assertRaisesRegex(AssertionError,'mismatch'):
            verify(content)
    def test_unique_anchors(self):
        self.assertEqual(len(ANCHORS),15)
        self.assertIn(0x8003F4E8,ANCHORS)
        self.assertIn(0x8003F510,ANCHORS)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original',type=Path)
    args=parser.parse_args()
    verify(args.original.read_text(encoding='utf-8'))
