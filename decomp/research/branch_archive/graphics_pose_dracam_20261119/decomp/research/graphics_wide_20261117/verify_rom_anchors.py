"""Verify USA 32 MiB reference and nine unpromoted actor/camera C source anchors.

No original ROM bytes or generated assembly are embedded or emitted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

USA_EXPANDED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
TARGETS = (
    ('func_80011610_12210', 0x12210, 36, '3710d62b2c4dae001b7703483c4cc39b97f3aaab36eb88deae537dc8f9ff5434'),
    ('func_800124A0_130A0', 0x130A0, 12, '122ded41f6b955a0eae41f7cd16293d7fad4e38d9ded8735fbbf657f0d6fa106'),
    ('func_80012500_13100', 0x13100, 24, 'a3e48ab8383ee90e5cf6011fcd180361bfd050df6839c36ad6c0f528f321c47e'),
    ('func_800127B8_133B8', 0x133B8, 48, '11229bb836a4ea8cfc9542b6ccfe7bdf84039631f63c343712be8b505a515d31'),
    ('func_800127E8_133E8', 0x133E8, 20, '6cbe01ddb844308ccd8f2894c0268a652cb4ad452a09f5cf582a72c0b9a74747'),
    ('func_800127FC_133FC', 0x133FC, 28, '7675051da7c384a3110b4a9e598b51523bfa5b35923ef551021b87781f24208b'),
    ('func_80012818_13418', 0x13418, 48, '28908f1630030c3f5847c3a0eb82b58f405c07044f213e8234e34418c7e65ea1'),
    ('func_80012848_13448', 0x13448, 20, '8c18ebaa4b8aab5f97c0ede00016753e5a48b647eb589d905c5fa3459c692dbb'),
    ('func_8001285C_1345C', 0x1345C, 28, 'b3b3d2f53ac8fb239cb55eb930d2326ffd410862b34f5c2cea895e385cf58366'),
)

def verify(rom):
    if len(rom) != 33_554_432 or hashlib.sha1(rom).hexdigest() != USA_EXPANDED_SHA1:
        raise ValueError('Expected original, SHA-1-authenticated USA expanded 32 MiB ROM')
    last_end = 0
    for name, start, length, digest in TARGETS:
        if start < last_end or start % 4 or length <= 0 or length % 4:
            raise ValueError('Overlapping or unaligned candidate interval: ' + name)
        if hashlib.sha256(rom[start:start+length]).hexdigest() != digest:
            raise ValueError('Original MIPS instruction hash differs: ' + name)
        last_end = start+length
    return {'status': 'PASS', 'region': 'usa', 'verified_functions': len(TARGETS),
            'verified_instruction_bytes': sum(x[2] for x in TARGETS),
            'original_expanded_sha1': USA_EXPANDED_SHA1,
            'source_association': 'source-instructions only; NOT canonical C promotion'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--usa-expanded', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.usa_expanded.read_bytes()), indent=2))

if __name__ == '__main__':
    main()
