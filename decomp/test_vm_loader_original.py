"""ROM-derived assembly regression for USA VM resource loader 0x8003D468.

Usage: python decomp/test_vm_loader_original.py PATH_TO_ORIGINAL_ASM
Original instructions must be generated privately by Splat from the pinned ROM.
This does not prove source C matches or replace full-ROM verification.
"""
import argparse
import re
from pathlib import Path

# Addresses are USA game VMAs, never assembled bytes.
EXPECTED = {
    0x8003D480: r'bnez\s+\$t6,\s*\.L8003D490_3E090',
    0x8003D484: r'sw\s+\$a0,\s*0x20\(\$sp\)',
    0x8003D49C: r'beq\s+\$a1,\s*\$a2,\s*\.L8003D538_3E138',
    0x8003D4A0: r'sw\s+\$a1,\s*0x0\(\$s1\)',
    0x8003D4BC: r'sw\s+\$v0,\s*0x14\(\$s0\)',
    0x8003D4C0: r'bne\s+\$v0,\s*\$at,\s*\.L8003D4E8_3E0E8',
    0x8003D4CC: r'lhu\s+\$a0,\s*0x2\(\$s1\)',
    0x8003D4D4: r'lw\s+\$a0,\s*0x0\(\$s1\)',
    0x8003D4DC: r'lw\s+\$a0,\s*0x0\(\$s1\)',
    0x8003D4F4: r'sw\s+\$t7,\s*0x14\(\$s0\)',
    0x8003D4FC: r'lw\s+\$a0,\s*0x0\(\$s1\)',
    0x8003D50C: r'jal\s+func_8003DDC4_3E9C4',
    0x8003D510: r'lw\s+\$a1,\s*0x24\(\$sp\)',
    0x8003D524: r'sw\s+\$t9,\s*%lo\(D_801C78F0_1C84F0\)\(\$at\)',
    0x8003D608: r'sw\s+\$zero,\s*0x0\(\$s0\)',
    0x8003D60C: r'sh\s+\$a2,\s*0x8\(\$s0\)',
    0x8003D618: r'sw\s+\$zero,\s*0xC\(\$s0\)',
    0x8003D624: r'sh\s+\$zero,\s*0xA\(\$s0\)',
    0x8003D648: r'jal\s+func_80024088_24C88',
    0x8003D64C: r'addiu\s+\$a0,\s*\$zero,\s*0x82',
    0x8003D668: r'sb\s+\$zero,\s*0x5C\(\$t2\)',
    0x8003D674: r'sb\s+\$zero,\s*0x5D\(\$t3\)',
}


def instruction_rows(asm: str) -> dict[int, str]:
    rows = {}
    for line in asm.splitlines():
        match = re.search(r'/\*\s+[0-9A-Fa-f]+\s+(8003[0-9A-Fa-f]{4})\s+[0-9A-Fa-f]{8}\s+\*/\s*(.*)', line)
        if match:
            address = int(match.group(1), 16)
            if address in rows:
                raise ValueError(f'duplicate USA instruction {address:#x}')
            rows[address] = match.group(2).strip()
    return rows


def check(asm: str) -> None:
    rows = instruction_rows(asm)
    for address, regex in EXPECTED.items():
        if address not in rows:
            raise AssertionError(f'missing original instruction {address:#x}')
        if re.fullmatch(regex, rows[address]) is None:
            raise AssertionError(f'{address:#x}: {rows[address]!r}; expected {regex!r}')
    for address, regex in {
        0x8003D490: r'lui\s+\$s1,\s*%hi\(D_801C78E8_1C84E8\)',
        0x8003D494: r'addiu\s+\$s1,\s*\$s1,\s*%lo\(D_801C78E8_1C84E8\)',
        0x8003D4B0: r'lui\s+\$s0,\s*%hi\(D_801C77E8_1C83E8\)',
        0x8003D4B4: r'addiu\s+\$s0,\s*\$s0,\s*%lo\(D_801C77E8_1C83E8\)',
    }.items():
        if address not in rows or re.fullmatch(regex, rows[address]) is None:
            raise AssertionError(f'global base construction mismatch {address:#x}')
    # Resource +2 halfword is not a script pointee field or work-record member.
    # VM work +0x14 is separate from the +0x0 script pointer.
    print(f'VM loader: {len(EXPECTED) + 4} original-address guards passed')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_asm', type=Path)
    args = parser.parse_args()
    check(args.original_asm.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
