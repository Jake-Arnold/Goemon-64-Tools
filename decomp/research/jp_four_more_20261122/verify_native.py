#!/usr/bin/env python3
"""Fail-closed isolated Japanese IDO comparisons; NEVER a combined G2 proof.

Use only your own authenticated original Japanese expanded ROM and original toolchain.
No ROM, assembly, compiler, linked code or binary is written to the research bundle.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

EXPECTED_ROM_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
SYMBOL = 'D_8016D430_16E030'
# Name, exact original expanded-ROM offset, original function extent, object relocation offsets
TARGETS = [
 ('func_8000BFFC_CBFC', 0xCBFC, 140, (4,12)),
 ('func_8000C088_CC88', 0xCC88, 76, (4,12)),
 ('func_8000C0D4_CCD4', 0xCCD4, 68, (4,12)),
 ('func_8000D108_DD08', 0xDD08, 64, (0,8)),
]

def run(argv):
    p = subprocess.run([str(a) for a in argv], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError('Failed '+str(argv)+'\n'+p.stderr[:1500])
    return p.stdout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',required=True,type=Path)
    parser.add_argument('--cc',required=True,type=Path)
    parser.add_argument('--ld',default='mips-linux-gnu-ld')
    parser.add_argument('--objdump',default='mips-linux-gnu-objdump')
    parser.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    rom=args.rom.read_bytes()
    if len(rom)!=33_554_432 or hashlib.sha1(rom).hexdigest()!=EXPECTED_ROM_SHA1:
        raise ValueError('Wrong original Japanese expanded ROM size or SHA-1')
    sources=Path(__file__).resolve().parent/'src'
    records=[]
    with tempfile.TemporaryDirectory(prefix='goemon-jp-four-more-') as td:
        scratch=Path(td)
        for name,off,extent,(hi,lo) in TARGETS:
            src=sources/(name+'.c')
            if not src.is_file(): raise FileNotFoundError(src)
            obj=scratch/(name+'.o')
            linked=scratch/(name+'.elf')
            binary=scratch/(name+'.bin')
            linker=scratch/(name+'.ld')
            vma=0x80000000+off-0xC00 # original main executable mapping, NOT an overlay
            run([args.cc,'-c','-G','0','-non_shared','-O2','-mips2','-I',sources,
                 '-o',obj,src])
            symrel=run([args.objdump,'-r',obj])
            reloc=[(int(a,16),b,c) for a,b,c in re.findall(
                r'^\s*([0-9a-f]{8})\s+(R_MIPS_\w+)\s+(\S+)',symrel,re.M)]
            wanted=[(hi,'R_MIPS_HI16',SYMBOL),(lo,'R_MIPS_LO16',SYMBOL)]
            if reloc!=wanted: raise AssertionError(f'{name}: relocation mismatch {reloc!r}')
            linker.write_text(f'{SYMBOL} = 0x8016D430;\n'
                f'SECTIONS {{ .text 0x{vma:08X} : SUBALIGN(1) {{ *(.text) }} '
                '/DISCARD/ : { *(.comment) *(.note*) } }\n')
            run([args.ld,'-T',linker,'-o',linked,obj])
            linked_symbols=run([args.objdump,'-t',linked])
            marker=re.compile('^'+f'{vma:08x}'+r'\s+g\s+F\s+\.text\s+\S+\s+'+re.escape(name)+r'$',re.M)
            if not marker.search(linked_symbols):
                raise AssertionError(f'{name}: linked guest VMA or symbol mismatch')
            run([args.objcopy,'-O','binary','--only-section=.text',linked,binary])
            machine=binary.read_bytes();expected=rom[off:off+extent]
            if machine[:extent]!=expected:
                first=next((i for i,(a,b) in enumerate(zip(machine[:extent],expected)) if a!=b),min(len(machine),extent))
                raise AssertionError(f'{name}: original byte mismatch at +0x{first:X}')
            if any(machine[extent:]):raise AssertionError(f'{name}: nonzero trailing text/padding')
            if len(machine)<extent:raise AssertionError(f'{name}: compiled text too short')
            record={
                'name':name,'original_expanded_rom_offset':f'0x{off:X}',
                'original_main_guest_vma':f'0x{vma:X}',
                'original_extent_bytes':extent,
                'original_instruction_sha256':hashlib.sha256(expected).hexdigest(),
                'candidate_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
                'linked_at_original_address_exact':True,
                'original_relocations':[{'offset':i,'type':t,'symbol':s} for i,t,s in reloc],
                'trailing_zero_padding_not_counted':len(machine)-extent,
            }
            records.append(record)
            print(f'PASSED_ISOLATED_NATIVE {name} {extent}/{extent} bytes; 2/2 symbolic relocs; VMA 0x{vma:X}')
    out={
        'region':'japan_0','status':'PASSED_ISOLATED_NATIVE / RESEARCH_ONLY',
        'original_expanded_rom_sha1':EXPECTED_ROM_SHA1,
        'toolchain':'SGI IDO 5.3 -O2 -mips2 -G 0',
        'new_previous_ASM_owned_candidate_functions':len(records),
        'isolated_exact_original_instruction_bytes':sum(x['original_extent_bytes'] for x in records),
        'isolated_original_symbolic_relocations':sum(len(x['original_relocations']) for x in records),
        'full_32MiB_and_16MiB_ROM_G2':'NOT_RUN',
        'all_7376_ELF_identities':'NOT_RUN',
        'all_80747_semantic_relocations':'NOT_RUN',
        'strict_C_ASM_inventory':'NOT_RUN','full_local_CI':'NOT_RUN',
        'new_official_C_promotions':0,'records':records}
    if args.report:args.report.write_text(json.dumps(out,indent=2)+'\n')
    print(f"PASSED_ISOLATED_NATIVE {len(records)} new research functions, {out['isolated_exact_original_instruction_bytes']} original bytes. NO FULL-ROM G2.")

if __name__=='__main__': main()
