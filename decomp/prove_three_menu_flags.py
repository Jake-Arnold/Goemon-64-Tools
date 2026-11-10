"""Separate original-address linked MIPS proofs for three menu ASM candidates.

Requires private decompressed ROM and pinned IDO; never establishes a full-ROM
C integration and never automatically promotes any matching function.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

if __package__:
    from .prove_three_wrappers import (ROM_SHA1, ORIGINAL_LENGTH,
                                       check_linked_words, verified_symbol_size_and_address)
else:
    from prove_three_wrappers import (ROM_SHA1, ORIGINAL_LENGTH,
                                      check_linked_words, verified_symbol_size_and_address)

ROOT = Path(__file__).resolve().parent
FUNCTIONS = (
    ('menu_enable_b60.c', 'func_80011B60_12760', 0x12760, 84,
     '5573013c23b198d920562b122776d0d45e5e9d999bd2bce92cf2051493652ec6'),
    ('menu_disable_bb4.c', 'func_80011BB4_127B4', 0x127B4, 80,
     'e001c012b652a5dadd7923706e8728b51a3bce9203c0f0a2130114b831524a52'),
    ('menu_nested_c04.c', 'func_80011C04_12804', 0x12804, 84,
     '72715c034f10313d627651394040a836581fed4a3fdda8241556bd38268055bb'),
)
LINK_SYMBOLS = {
    'D_801FC624_5B8534': 0x801FC624,
    'D_801FC628_5B8538': 0x801FC628,
    'D_8015C5C8_15D1C8': 0x8015C5C8,
}

def prove(rom_path: Path, compiler: Path, linker: Path, objcopy: Path, readelf: Path) -> list[dict]:
    rom = rom_path.read_bytes()
    if len(rom) != ORIGINAL_LENGTH or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('wrong original 32 MiB decompressed ROM or SHA-1')
    records = []
    with tempfile.TemporaryDirectory(prefix='goemon-menu-') as d:
        workspace = Path(d)
        for file, function, offset, size, sha in FUNCTIONS:
            original_vma = offset + 0x7FFFF400
            src = ROOT / 'candidates' / file
            if not src.is_file():
                raise ValueError('missing research-only menu source')
            obj = workspace / 'menu.o'
            elf = workspace / 'menu.elf'
            result = workspace / 'menu.bin'
            script = workspace / 'original.ld'
            defines = ''.join(f'{symbol} = 0x{addr:08X};\n' for symbol,addr in LINK_SYMBOLS.items())
            script.write_text('OUTPUT_ARCH(mips)\n' + f'ENTRY({function})\n' + defines +
                              f'SECTIONS {{ .text 0x{original_vma:08X} : SUBALIGN(4) {{ *(.text) }} }}\n')
            subprocess.run([str(compiler), '-c', '-O2', '-mips2', '-G', '0', '-non_shared', str(src), '-o', str(obj)],check=True,capture_output=True)
            subprocess.run([str(linker), '-m', 'elf32btsmip', '-T', str(script), str(obj), '-o', str(elf)],check=True,capture_output=True)
            symtab = subprocess.run([str(readelf), '-Ws', str(elf)],check=True,capture_output=True,text=True).stdout
            verified_symbol_size_and_address(symtab,function,original_vma,size)
            subprocess.run([str(objcopy), '-O', 'binary', '--only-section=.text', str(elf), str(result)],check=True,capture_output=True)
            check_linked_words(result.read_bytes(),rom,offset,size,sha)
            records.append({'function':function,'offset':hex(offset),'original_bytes':size,
                            'sha256':sha,'isolated_linked_exact':True,'promoted':False})
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom',required=True,type=Path)
    p.add_argument('--ido',required=True,type=Path)
    p.add_argument('--linker',type=Path,default='ld.lld')
    p.add_argument('--objcopy',type=Path,default='llvm-objcopy')
    p.add_argument('--readelf',type=Path,default='readelf')
    args=p.parse_args()
    print(json.dumps({'isolated_function_matches':prove(args.rom,args.ido,args.linker,args.objcopy,args.readelf),
                      'whole_rom_rebuild_performed':False,'new_promotions':0},indent=2))
