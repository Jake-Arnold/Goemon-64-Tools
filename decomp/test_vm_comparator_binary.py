"""ROM-gated isolated IDO 5.3 match for USA VM comparator (not full-ROM proof).

Requires the user's LOCAL pinned 32 MiB decompressed ROM, compiler and readelf.
Never bundles, uploads, emits or writes original instruction bytes.  This is
an isolated-function gate only; a full current-branch build is still required
before updating matching-C totals.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_SIZE = 33554432
OFFSET = 0x3E5B8
ADDRESS = 0x8003D9B8
SIZE = 340
SYMBOL = 'func_8003D9B8_3E5B8'
EXPECTED_SHA256 = 'bfa8ec5494880607e6b7d822dc952b22da49d7617ab50d59c6e920cbc45983a0'


def read_symbol(table: str) -> tuple[int, int]:
    for row in table.splitlines():
        parts = row.split()
        if len(parts) >= 8 and parts[3] == 'FUNC' and parts[-1] == SYMBOL:
            return int(parts[1], 16), int(parts[2])
    raise ValueError('Missing required ELF FUNC symbol')


def read_text_words(dump: str) -> bytes:
    """Read ELF .text hex dump, excluding its ASCII preview."""
    words: dict[int, bytes] = {}
    for line in dump.splitlines():
        m = re.match(r'^\s*0x([0-9A-Fa-f]+)((?:\s+[0-9A-Fa-f]{8}){1,4})(?:\s|$)', line)
        if m is None:
            continue
        addr = int(m.group(1), 16)
        for chunk in m.group(2).split():
            words[addr] = bytes.fromhex(chunk)
            addr += 4
    if not words:
        raise ValueError('No .text instructions found')
    if sorted(words) != list(range(0, max(words) + 4, 4)):
        raise ValueError('Discontinuous ELF .text hexdump')
    return b''.join(words[a] for a in sorted(words))


def check_object(obj: Path, rom: bytes, readelf: str = 'readelf') -> int:
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('Incorrect local decompressed USA ROM (length/SHA-1)')

    def elf(*options: str) -> str:
        return subprocess.check_output([readelf, *options, str(obj)], text=True)

    address, size = read_symbol(elf('-Ws'))
    if size != SIZE or address % 4:
        raise ValueError(f'Unexpected comparator symbol position or size: {address:#x}, {size}')
    relocation_table = elf('-r')
    if 'There are no relocations in this file.' not in relocation_table:
        raise ValueError('Object has relocations; an isolated raw-byte match is insufficient')
    section = read_text_words(elf('-x', '.text'))
    compiled = section[address:address + size]
    original = rom[OFFSET:OFFSET + SIZE]
    if len(compiled) != SIZE:
        raise ValueError('Truncated candidate symbol')
    for pos in range(0, SIZE, 4):
        if compiled[pos:pos + 4] != original[pos:pos + 4]:
            raise ValueError(f'Instruction mismatch at original VMA 0x{ADDRESS + pos:08X}')
    if hashlib.sha256(compiled).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Unexpected comparator identity despite equal bytes')
    return SIZE // 4


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decompressed-rom', type=Path, required=True)
    parser.add_argument('--ido-cc', type=Path, required=True)
    parser.add_argument('--readelf', default='readelf')
    parser.add_argument('--candidate', type=Path,
                        default=Path(__file__).parent / 'candidates/vm_comparator_exact.c')
    args = parser.parse_args()
    rom = args.decompressed_rom.read_bytes()
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        parser.error('Local ROM must match the pinned 32 MiB decompressed USA SHA-1')
    with tempfile.TemporaryDirectory(prefix='goemon-vm-comparator-') as temp:
        obj = Path(temp) / 'comparator.o'
        subprocess.run([str(args.ido_cc), '-c', '-O2', '-mips2', '-G', '0', '-non_shared',
                        str(args.candidate), '-o', str(obj)], check=True)
        matched = check_object(obj, rom, args.readelf)
    print(f'{SYMBOL}: {matched}/{SIZE // 4} original instructions exact ({SIZE} bytes)')
    print('Isolated IDO match only; no current full-ROM or formal verifier gate')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
