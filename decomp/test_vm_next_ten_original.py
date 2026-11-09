"""Original-assembly address/word guards for next-ten VM targets 1, 2, 3.

Run with PRIVATE Splat assembly for the verified USA ROM. This proves original
instruction provenance, NOT equivalence of any research-only C candidates.
"""
import argparse
import hashlib
from pathlib import Path
import re
import struct
import unittest

# Main-segment VMA, ROM start, word count, original-instruction SHA-256.
SPECS = {
    'func_8003E234_3EE34': (0x8003E234, 0x3EE34, 110, 'acd6d1ecf74790033a8438ba6aae9c7652497de18d5ad7c205deaf2650268336'),
    'func_8003EBAC_3F7AC': (0x8003EBAC, 0x3F7AC, 109, '67f4730f98adcd92a28b506c7631437629ffa8bd08101f2594011ce982201539'),
    'func_8003F37C_3FF7C': (0x8003F37C, 0x3FF7C, 48, '74867178f34d8d45b1753520e1218d6e6c2307f44937258e95c3828f1cf1efd0'),
}
ANCHORS = {
    'func_8003E234_3EE34': {
        0x8003E234: r'lui\s+\$v1,\s*%hi\(D_8015C5CC_15D1CC\)',
        0x8003E23C: r'lw\s+\$v0,\s*0x0\(\$v1\)',
        0x8003E3B4: r'lbu\s+\$t8,\s*0x5D\(\$t6\)',
        0x8003E3E4: r'jr\s+\$ra',
        0x8003E3E8: r'sw\s+\$t6,\s*0x0\(\$v0\)',
    },
    'func_8003EBAC_3F7AC': {
        0x8003EBAC: r'lui\s+\$v1,\s*%hi\(D_8015C5CC_15D1CC\)',
        0x8003ECA0: r'addiu\s+\$t8,\s*\$a0,\s*0xF',
        0x8003ECB4: r'addiu\s+\$a1,\s*\$a1,\s*-0x2',
        0x8003ED18: r'lbu\s+\$a3,\s*0x5C\(\$t8\)',
        0x8003ED58: r'jr\s+\$ra',
        0x8003ED5C: r'sw\s+\$t9,\s*0x4\(\$v0\)',
    },
    'func_8003F37C_3FF7C': {
        0x8003F37C: r'addiu\s+\$sp,\s*\$sp,\s*-0x50',
        0x8003F384: r'lwc1\s+\$f2,\s*%lo\(D_8007D108_7DD08\)\(\$at\)',
        0x8003F388: r'mtc1\s+\$zero,\s*\$f0',
        0x8003F3DC: r'jal\s+func_80035690_36290',
        0x8003F3E0: r'swc1\s+\$f0,\s*0x18\(\$sp\)',
        0x8003F414: r'jal\s+func_80035244_35E44',
        0x8003F424: r'jal\s+func_80035214_35E14',
        0x8003F434: r'jr\s+\$ra',
        0x8003F438: r'nop',
    },
}
ROW = re.compile(r'/\*\s+([0-9A-Fa-f]+)\s+([0-9A-Fa-f]{8})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)')

def verify(source, function):
    base, offset, count, digest = SPECS[function]
    lines = source.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == 'glabel '+function]
    ends = [i for i, line in enumerate(lines) if line.strip() == 'endlabel '+function]
    if len(starts)!=1 or len(ends)!=1 or starts[0]>=ends[0]:
        raise ValueError('missing or ambiguous original function boundary')
    rows = {}
    for line in lines[starts[0]+1:ends[0]]:
        if re.match(r'\s*(glabel|endlabel)\s+',line):
            raise ValueError('nested original function labels')
        match=ROW.search(line)
        if not match:
            continue
        off, addr, word = (int(match.group(i),16) for i in (1,2,3))
        if addr in rows:
            raise ValueError('duplicate original address')
        if (off,addr)!=(offset+4*len(rows),base+4*len(rows)):
            raise ValueError('noncontiguous ROM/VMA')
        rows[addr]=(word,match.group(4).strip())
    if len(rows)!=count:
        raise ValueError('wrong original instruction extent')
    raw=b''.join(struct.pack('>I',x[0]) for x in rows.values())
    if hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError('original instruction SHA mismatch')
    for addr,regex in ANCHORS[function].items():
        if re.fullmatch(regex,rows[addr][1]) is None:
            raise ValueError(f'wrong original instruction at {addr:#x}')
    return len(rows)

class ParserNegativeControls(unittest.TestCase):
    def test_missing_label(self):
        with self.assertRaisesRegex(ValueError, 'boundary'):
            verify('', 'func_8003E234_3EE34')
    def test_duplicate_address(self):
        name='func_8003EBAC_3F7AC'; row='/* 3F7AC 8003EBAC 00000000 */ nop'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            verify(f'glabel {name}\n{row}\n{row}\nendlabel {name}',name)
    def test_wrong_offset(self):
        name='func_8003F37C_3FF7C'
        with self.assertRaisesRegex(ValueError, 'noncontiguous'):
            verify(f'glabel {name}\n/* 3FF80 8003F37C 00000000 */ nop\nendlabel {name}',name)
    def test_unique_targets_and_guards(self):
        self.assertEqual(len(SPECS),3)
        self.assertEqual(sum(row[2] for row in SPECS.values()),267)
        self.assertEqual(sum(map(len,ANCHORS.values())),20)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('private_assembly',type=Path,nargs='?')
    args=ap.parse_args()
    if args.private_assembly:
        text=args.private_assembly.read_text(encoding='utf-8')
        for name in SPECS:
            print(f'{name}: {verify(text,name)} original ROM/VMA words and {len(ANCHORS[name])} guards passed')
    else:
        unittest.main(argv=['test_vm_next_ten_original'])
