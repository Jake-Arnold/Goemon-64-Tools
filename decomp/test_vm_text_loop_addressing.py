"""Static addressing guard for original USA VM text loop; not matching-C proof.

Usage: python test_vm_text_loop_addressing.py PATH_TO_ORIGINAL_ASM
"""
import re
import sys
from pathlib import Path


def check(text: str) -> None:
    rows = {}
    for line in text.splitlines():
        m = re.search(r'/\* [0-9A-Fa-f]+ (8003[0-9A-Fa-f]{4}) [0-9A-Fa-f]{8} \*/\s*(.*)', line)
        if m:
            rows[int(m.group(1), 16)] = m.group(2).strip()
    expected = {
        0x8003DC3C: r'addiu\s+\$s1,\s*\$s1,\s*%lo\(D_801C77E8_1C83E8\)',
        0x8003DC5C: r'lw\s+\$a1,\s*0x0\(\$s1\)',
        0x8003DC6C: r'sw\s+\$v0,\s*0x0\(\$s1\)',
        0x8003DC98: r'sh\s+\$zero,\s*0xA\(\$s1\)',
        0x8003DCD4: r'lhu\s+\$t2,\s*0xA\(\$s1\)',
        0x8003DCC8: r'lhu\s+\$t0,\s*0x4\(\$s3\)',
        0x8003DD1C: r'lhu\s+\$t3,\s*0x2\(\$s3\)',
        0x8003DD58: r'sh\s+\$t7,\s*0xA\(\$s1\)',
    }
    for address, pattern in expected.items():
        assert address in rows, f'missing original instruction at {address:#x}'
        assert re.fullmatch(pattern, rows[address]), (hex(address), rows[address])
    assert re.search(r'\blui\s+\$s1,\s*%hi\(D_801C77E8_1C83E8\)', rows[0x8003DC38])
    # $s1 points at the global *storage*, not at the script pointer's pointee.
    # In particular, sh +0xA($s1) accesses global 0x801C77F2.
    print('VM text-loop: 9 original-address global/controller addressing guards passed')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python test_vm_text_loop_addressing.py ORIGINAL_ASM')
    check(Path(sys.argv[1]).read_text())
