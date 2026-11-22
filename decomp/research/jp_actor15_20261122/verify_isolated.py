#!/usr/bin/env python3
"""Read-only Japanese rev-0 isolated native C proof; NOT combined G2 acceptance.

Requires the *user-owned* expanded 32 MiB original Japanese ROM, pinned IDO 5.3,
and MIPS GNU ld/objcopy/objdump. Does not redistribute game data or tools.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

ORIGINAL_SHA1='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
SYMBOL='D_8016D430_16E030'
TARGETS=[
 ('func_8000C118_CD18',0xCD18,36),
 ('func_8000C13C_CD3C',0xCD3C,52),
 ('func_8000C170_CD70',0xCD70,64),
 ('func_8000C1B0_CDB0',0xCDB0,52),
 ('func_8000C1E4_CDE4',0xCDE4,64),
 ('func_8000C224_CE24',0xCE24,36),
 ('func_8000C248_CE48',0xCE48,40),
 ('func_8000C270_CE70',0xCE70,40),
 ('func_8000C298_CE98',0xCE98,52),
 ('func_8000C2CC_CECC',0xCECC,64),
 ('func_8000C30C_CF0C',0xCF0C,40),
 ('func_8000C334_CF34',0xCF34,52),
 ('func_8000C368_CF68',0xCF68,64),
 ('func_8000C3A8_CFA8',0xCFA8,40),
 ('func_8000C600_D200',0xD200,52),
]

def run(cmd):
    result=subprocess.run(cmd,capture_output=True,text=True)
    if result.returncode:
        raise RuntimeError(f'Command failed: {cmd[0]}\n{result.stderr[:1200]}')
    return result.stdout

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',type=Path,required=True,help='Original 32 MiB expanded JP rev-0 z64')
    ap.add_argument('--cc',type=Path,required=True,help='Pinned SGI IDO 5.3 cc')
    ap.add_argument('--ld',default='mips-linux-gnu-ld')
    ap.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    ap.add_argument('--objdump',default='mips-linux-gnu-objdump')
    ap.add_argument('--report',type=Path,help='Optional JSON isolated proof output')
    a=ap.parse_args()
    original=a.rom.read_bytes()
    if len(original)!=33554432 or hashlib.sha1(original).hexdigest()!=ORIGINAL_SHA1:
        raise SystemExit('Wrong Japanese ROM: original size/SHA-1 do not match reference')
    srcdir=Path(__file__).resolve().parent/'src'
    out=[]
    with tempfile.TemporaryDirectory(prefix='jp_actor15_native_') as scratch:
        w=Path(scratch)
        for name,off,size in TARGETS:
            src=srcdir/(name+'.c')
            if not src.is_file():raise FileNotFoundError(src)
            obj=w/(name+'.o');elf=w/(name+'.elf');binfile=w/(name+'.bin');ldfile=w/(name+'.ld')
            # Main-executable JP region mapping, not an overlay-address heuristic.
            vma=0x80000000+off-0xC00
            run([str(a.cc),'-c','-G','0','-non_shared','-O2','-mips2','-I',str(srcdir),'-o',str(obj),str(src)])
            asmrel=run([str(a.objdump),'-r',str(obj)])
            relocations=[(int(pos,16),kind,sym) for pos,kind,sym in re.findall(
                r'^\s*([0-9a-f]{8})\s+(R_MIPS_\w+)\s+(\S+)',asmrel,re.M)]
            expected_reloc=[(4,'R_MIPS_HI16',SYMBOL),(12,'R_MIPS_LO16',SYMBOL)]
            if relocations!=expected_reloc:
                raise AssertionError(f'{name}: relocation set {relocations!r}')
            ldfile.write_text(
                f'{SYMBOL} = 0x8016D430;\n'
                f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(1) {{ *(.text) }} '
                '/DISCARD/ : { *(.comment) *(.note*) } }\n'
            )
            run([str(a.ld),'-T',str(ldfile),'-o',str(elf),str(obj)])
            symtext=run([str(a.objdump),'-t',str(elf)])
            if not re.search(r'^'+f'{vma:08x}'+r'\s+g\s+F\s+\.text\s+\S+\s+'+re.escape(name)+r'$',symtext,re.M):
                raise AssertionError(f'{name}: not linked at original VMA 0x{vma:X}')
            run([str(a.objcopy),'-O','binary','--only-section=.text',str(elf),str(binfile)])
            compiled=binfile.read_bytes()
            code=original[off:off+size]
            if compiled[:size]!=code:
                delta=next((i for i in range(size) if compiled[i]!=code[i]),-1)
                raise AssertionError(f'{name}: first original byte mismatch at +0x{delta:X}')
            alignment=compiled[size:]
            if any(alignment):raise AssertionError(f'{name}: nonzero trailing alignment')
            rec={
                'name':name,'rom_offset':f'0x{off:X}','guest_vma':f'0x{vma:X}',
                'original_function_bytes':size,
                'original_sha256':hashlib.sha256(code).hexdigest(),
                'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
                'linked_original_address_bytes_exact':True,
                'original_symbolic_relocations':[
                    {'offset':pos,'type':kind,'symbol':symbol}
                    for pos,kind,symbol in relocations
                ],
                'alignment_bytes_not_counted':len(alignment),
            }
            out.append(rec)
            print(f'PASSED_ISOLATED_NATIVE {name}: {size}/{size} bytes, 2/2 relocs, VMA 0x{vma:X}')
    result={
        'format':'goemon-jp-actor15-repro-native-v1',
        'region':'japan_0',
        'status':'PASSED_ISOLATED_NATIVE_RESEARCH_ONLY',
        'original_expanded_rom_sha1':ORIGINAL_SHA1,
        'native_compiler':'SGI IDO 5.3 -O2 -mips2 -G 0',
        'isolated_function_count':len(out),
        'isolated_original_bytes':sum(x['original_function_bytes'] for x in out),
        'isolated_original_relocations':sum(len(x['original_symbolic_relocations']) for x in out),
        'combined_rom_g2':'NOT_RUN',
        'retail_rom_g2':'NOT_RUN',
        'elf_function_inventory':'NOT_RUN',
        'complete_semantic_relocations':'NOT_RUN',
        'strict_c_asm_inventory':'NOT_RUN',
        'full_decomp_local_ci':'NOT_RUN',
        'new_matching_c_promotions':0,
        'functions':out,
    }
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(out)} isolated native functions, {result["isolated_original_bytes"]} original bytes, {result["isolated_original_relocations"]} original relocation records; NO FULL-ROM G2 CLAIM')

if __name__=='__main__':main()
