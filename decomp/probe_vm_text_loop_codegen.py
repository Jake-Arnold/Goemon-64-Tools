"""Compare an isolated VM text-loop IDO object with original ROM instructions.

This is a research diagnostic, not original-address relocation or ROM proof.
The original ROM is read only from a local, SHA-1-verified 32 MiB file.
No original ROM or object bytes are embedded in this script or written to Git.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import struct
import subprocess
import tempfile
from pathlib import Path

ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_SIZE = 33_554_432
ROM_OFFSET = 0x3E7EC
GUEST_ADDRESS = 0x8003DBEC
ORIGINAL_BYTES = 472
SYMBOL = 'func_8003DBEC_3E7EC'


def run(*args: str) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f'{args[0]} failed ({result.returncode}): {result.stderr.strip()}')
    return result.stdout


def parse_symbol_size(symbol_table: str) -> tuple[int, int]:
    for line in symbol_table.splitlines():
        fields = line.split()
        if len(fields) >= 8 and fields[3] == 'FUNC' and fields[-1] == SYMBOL:
            return int(fields[1], 16), int(fields[2], 10)
    raise ValueError(f'IDO output does not define {SYMBOL} as a function')


def parse_hexdump(hexdump: str) -> dict[int, int]:
    words = {}
    for line in hexdump.splitlines():
        found = re.match(r'^\s*0x([0-9a-fA-F]+)((?:\s+[0-9a-fA-F]{8}){1,4})(?:\s|$)', line)
        if not found:
            continue
        offset = int(found.group(1), 16)
        for index, hex_word in enumerate(found.group(2).split()):
            words[offset + index * 4] = int(hex_word, 16)
    return words


def parse_relocations(table: str) -> set[int]:
    # Every position containing a relocation is excluded, regardless of type;
    # a relocation-aware original-address link is required for true proof.
    offsets = set()
    for line in table.splitlines():
        match = re.match(r'^\s*([0-9a-fA-F]{8})\s+\S+\s+R_MIPS_', line)
        if match:
            offsets.add(int(match.group(1), 16))
    return offsets


def compare(rom: bytes, object_file: Path, readelf: str) -> dict[str, object]:
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('Expected pinned 32 MiB decompressed USA ROM SHA-1')
    symbol_offset, symbol_size = parse_symbol_size(run(readelf, '-Ws', str(object_file)))
    words = parse_hexdump(run(readelf, '-x', '.text', str(object_file)))
    relocations = parse_relocations(run(readelf, '-r', str(object_file)))
    baseline = struct.unpack('>118I', rom[ROM_OFFSET:ROM_OFFSET + ORIGINAL_BYTES])
    if symbol_offset % 4 or symbol_size % 4:
        raise ValueError('Candidate symbol is not 4-byte aligned')
    included = []
    matching = []
    mismatching = []
    for i, original in enumerate(baseline):
        relative = i * 4
        loc = symbol_offset + relative
        if relative >= symbol_size or loc not in words or loc in relocations:
            continue
        included.append(relative)
        if words[loc] == original:
            matching.append(relative)
        else:
            mismatching.append(relative)
    prologue = words.get(symbol_offset)
    frame_bytes = None
    if prologue is not None and prologue >> 16 == 0x27BD:
        signed_imm = (prologue & 0xFFFF)
        signed_imm -= 0x10000 if signed_imm & 0x8000 else 0
        frame_bytes = -signed_imm
    return {
        'original_size': ORIGINAL_BYTES,
        'candidate_size': symbol_size,
        'excluded_relocation_words': sum(symbol_offset <= r < symbol_offset + min(symbol_size, ORIGINAL_BYTES) for r in relocations),
        'compared_nonrelocation_words': len(included),
        'matching_nonrelocation_words': len(matching),
        'first_mismatch_addresses': [f'0x{GUEST_ADDRESS + offset:08X}' for offset in mismatching[:8]],
        'candidate_frame_bytes': frame_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decompressed-rom', type=Path, required=True)
    parser.add_argument('--candidate-source', type=Path, default=Path(__file__).parent / 'candidates/vm_text_loop.c')
    parser.add_argument('--ido-cc', type=Path, required=True)
    parser.add_argument('--readelf', default='readelf')
    args = parser.parse_args()
    rom = args.decompressed_rom.read_bytes()
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        parser.error('decompressed USA ROM length/SHA-1 mismatch')
    with tempfile.TemporaryDirectory(prefix='goemon-vm-codegen-') as temp:
        obj = Path(temp) / 'vm_text_loop.o'
        run(str(args.ido_cc), '-c', '-O2', '-mips2', '-G', '0', '-non_shared',
            str(args.candidate_source), '-o', str(obj))
        result = compare(rom, obj, args.readelf)
    for key, value in result.items():
        print(f'{key}: {value}')
    print('Unrelocated diagnostic only; not a matching-C promotion')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
