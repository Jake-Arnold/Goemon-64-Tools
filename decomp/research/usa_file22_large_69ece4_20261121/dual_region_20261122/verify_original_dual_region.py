#!/usr/bin/env python3
"""Strict ROM-hash-gated cross-region original file22 function equivalence check.

This prints only metadata; it never emits ROM instructions, source assets or ASM.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

SIZE = 33554432
FUNCTION_SIZE = 1808
ORIGINALS = (
    ("usa", 0x69ECE4, "6ea0ed71032ce08fc2745f412d84936382197494",
     "eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9",
     0x801D701C),
    ("japan", 0x6A37D4, "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
     "51a7ff3b9863ee6bcdae6ca0796934ecf91218ace5d39e48b8b1c892cf1084ae",
     0x801DC74C),
)

def load_and_verify(path: Path, region):
    name, offset, full_sha1, slice_sha256, cursor = region
    data = path.read_bytes()
    if len(data) != SIZE or hashlib.sha1(data).hexdigest() != full_sha1:
        raise ValueError(f"{name} must be the pinned original decompressed 32MiB ROM")
    code = data[offset:offset + FUNCTION_SIZE]
    if hashlib.sha256(code).hexdigest() != slice_sha256:
        raise ValueError(f"{name} original function identity mismatch")
    hi = struct.unpack_from('>I', code, 0x40)[0]
    lo = struct.unpack_from('>I', code, 0x4C)[0]
    if hi >> 16 != 0x3C03 or lo >> 16 != 0x2463:
        raise ValueError(f"{name} unexpected symbol address instructions")
    signed_lo = struct.unpack('>h', struct.pack('>H', lo & 0xFFFF))[0]
    address = (((hi & 0xFFFF) << 16) + signed_lo) & 0xFFFFFFFF
    if address != cursor:
        raise ValueError(f"{name} source symbol address mismatch")
    return code

def check(usa_path: Path, japan_path: Path):
    usa = load_and_verify(usa_path, ORIGINALS[0])
    japan = load_and_verify(japan_path, ORIGINALS[1])
    offsets = [i for i in range(0, FUNCTION_SIZE, 4)
               if usa[i:i+4] != japan[i:i+4]]
    if offsets != [0x40, 0x4C]:
        raise ValueError(f"Unexpected region differences at {[hex(i) for i in offsets]}")
    return {
        'status': 'AUTHENTIC_ORIGINAL_REGION_CODE_IDENTITY',
        'function_bytes_per_region': FUNCTION_SIZE,
        'instruction_words_per_region': FUNCTION_SIZE // 4,
        'exact_original_instruction_words': FUNCTION_SIZE // 4 - len(offsets),
        'region_variant_instruction_offsets': ['0x40', '0x4C'],
        'original_symbol_relocation_pair': 'R_MIPS_HI16/R_MIPS_LO16',
        'usa_cursor': '0x801D701C',
        'japan_cursor': '0x801DC74C',
        'overlay_address_delta': '0x5730',
        'original_function_matches_C': 'NOT_TESTED_BY_THIS_SCRIPT',
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--usa', required=True, type=Path)
    parser.add_argument('--japan', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.usa, args.japan), indent=2))

if __name__ == '__main__':
    main()
