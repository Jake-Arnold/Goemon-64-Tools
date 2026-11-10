"""Local research proof for three isolated IDO-linked wrappers. Never promotes C."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ORIGINAL_LENGTH = 33554432
FUNCTIONS = (
    ('resource_wrapper_ed4.c', 'func_80034ED4_35AD4', 0x35AD4, 36, 'b6e4ba1efa16865b5ae60da5cb79335e06098a2e2771be5b53cc99252d21531a'),
    ('resource_wrapper_f20.c', 'func_80034F20_35B20', 0x35B20, 36, 'e014867b2e08c89e528e37e0545ac991cd13ce8c105395bffee9be375c9e555e'),
    ('object_dispatch_c94.c', 'func_80035094_35C94', 0x35C94, 48, '7f8f2a83dbc5179d76609db3b186ea481e9aa78bd0b1e6f46ceb798637fe0c36'),
)
ABSOLUTE_LINK_SYMBOLS = {
    'D_8016DAB4_16E6B4': 0x8016DAB4,
    'func_80034EF8_35AF8': 0x80034EF8,
    'func_80034F44_35B44': 0x80034F44,
    'func_800362DC_36EDC': 0x800362DC,
    'func_800350C4_35CC4': 0x800350C4,
}

def check_linked_words(linked: bytes, rom: bytes, offset: int, size: int, hash_expected: str) -> None:
    if len(linked) < size:
        raise ValueError('candidate section shorter than the symbol')
    if offset < 0 or offset + size > len(rom):
        raise ValueError('function original ROM offset is outside reference')
    data = linked[:size]
    if hashlib.sha256(rom[offset:offset + size]).hexdigest() != hash_expected:
        raise ValueError('unexpected original function reference SHA-256')
    if data != rom[offset:offset + size]:
        raise ValueError('linked candidate differs from the original instruction bytes')

def verified_symbol_size_and_address(symbol_table: str, function: str, vma: int, size: int) -> None:
    """Do not mistake correct linker padding for a correctly sized C symbol."""
    rows = []
    for line in symbol_table.splitlines():
        match = re.fullmatch(
            r"\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+(\d+)\s+" +
            re.escape(function) + r"\s*", line)
        if match:
            rows.append((int(match.group(1),16), int(match.group(2))))
    if rows != [(vma, size)]:
        raise ValueError(f'wrong or ambiguous original function symbol size/address: {function}')


def prove(rom_path: Path, compiler: Path, linker: Path, objcopy: Path, readelf: Path) -> list[dict]:
    rom = rom_path.read_bytes()
    if len(rom) != ORIGINAL_LENGTH or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('wrong original 32 MiB decompressed ROM or SHA-1')
    records = []
    with tempfile.TemporaryDirectory(prefix='goemon-wrappers-') as d:
        directory = Path(d)
        for file, function, offset, length, sha in FUNCTIONS:
            src = ROOT / 'candidates' / file
            if not src.is_file():
                raise ValueError('source candidate is missing')
            obj = directory / 'candidate.o'
            elf = directory / 'candidate.elf'
            binpath = directory / 'candidate.bin'
            symbols = '\n'.join(f'{name} = 0x{value:08X};' for name, value in ABSOLUTE_LINK_SYMBOLS.items())
            vma = offset + 0x7FFFF400
            ldscript = directory / 'original.ld'
            ldscript.write_text('OUTPUT_ARCH(mips)\n' + f'ENTRY({function})\n' + symbols + '\n' +
                                'SECTIONS { .text 0x%08X : SUBALIGN(4) { *(.text) } }\n' % vma)
            subprocess.run([str(compiler), '-c', '-O2', '-mips2', '-G', '0', '-non_shared', str(src), '-o', str(obj)], check=True, capture_output=True)
            subprocess.run([str(linker), '-m', 'elf32btsmip', '-T', str(ldscript), str(obj), '-o', str(elf)], check=True, capture_output=True)
            symtab = subprocess.run([str(readelf), '-Ws', str(elf)], check=True, capture_output=True, text=True).stdout
            verified_symbol_size_and_address(symtab, function, vma, length)
            subprocess.run([str(objcopy), '-O', 'binary', '--only-section=.text', str(elf), str(binpath)], check=True, capture_output=True)
            linked = binpath.read_bytes()
            check_linked_words(linked, rom, offset, length, sha)
            records.append({'function':function, 'rom_offset':hex(offset), 'bytes':length,
                            'sha256':sha, 'isolated_linked_original_bytes_equal':True,
                            'promoted':False})
    return records

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom', required=True, type=Path)
    p.add_argument('--ido', required=True, type=Path)
    p.add_argument('--linker', default='ld.lld', type=Path)
    p.add_argument('--objcopy', default='llvm-objcopy', type=Path)
    p.add_argument('--readelf', default='readelf', type=Path)
    a = p.parse_args()
    import json
    print(json.dumps({'result':prove(a.rom,a.ido,a.linker,a.objcopy,a.readelf),
                      'proof_level':'isolated linked only; full ROM integration NOT tested'},indent=2))
