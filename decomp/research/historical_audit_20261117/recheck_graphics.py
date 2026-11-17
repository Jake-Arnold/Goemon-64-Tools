#!/usr/bin/env python3
"""Revalidate the five USA graphics C research candidates against private ROM.

Requires original IDO 5.3 and MIPS binutils. This proves *isolated/grouped*
original-address code bytes and linked FUNC size only, NOT complete canonical G2.
No private ROM or generated ELF/ASM is written into the repository.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

PINNED_ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
SOURCE_SHA1 = {
    'anim_matrix.c':'2f73e1d3a17c5a2e33e3d24c34dd31c9424c9113',
    'gfx_wrapper.c':'167bf266292d3c38025617692272e48f9f7d659c',
    'gfx_vectors.c':'6b4a15c80f210811af709f648eafc12b21b04038',
}
FUNCTIONS = [
    ('func_8001965C_1A25C', 'segment0.bin', 0, 0x1A25C, 72, 0x8001965C),
    ('func_8001B918_1C518', 'segment2.bin', 0, 0x1C518, 56, 0x8001B918),
    ('func_8001C970_1D570', 'segment3.bin', 0, 0x1D570, 76, 0x8001C970),
    ('func_8001C9BC_1D5BC', 'segment3.bin', 76, 0x1D5BC, 28, 0x8001C9BC),
    ('func_8001C9D8_1D5D8', 'segment3.bin', 104, 0x1D5D8, 52, 0x8001C9D8),
]


def call(args, cwd=None):
    r=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(f'{args[0]} returned {r.returncode}: {r.stderr[:3000]}')
    return r.stdout


def verify(rom_path,ido,readelf,ld,objcopy,source_dir):
    rom=rom_path.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=PINNED_ROM_SHA1:
        raise ValueError('USA expanded ROM failed size/SHA1 authentication')
    for name,sha in SOURCE_SHA1.items():
        raw=(source_dir/name).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if blob!=sha:
            raise ValueError('Source provenance mismatch '+name)
    with tempfile.TemporaryDirectory(prefix='goemon-gfx-native-recheck-') as scratch:
        p=Path(scratch)
        for base in ('anim_matrix','gfx_wrapper','gfx_vectors'):
            call([ido,'-c','-O2','-mips2','-G','0','-non_shared',
                  source_dir/(base+'.c'),'-o',p/(base+'.o')])
        script=p/'graphics_link.ld'
        script.write_text('''SECTIONS {
 .text 0x8001965C : SUBALIGN(4) { anim_matrix.o(.text) }
 .text2 0x8001B918 : SUBALIGN(4) { gfx_wrapper.o(.text) }
 .text3 0x8001C970 : SUBALIGN(4) { gfx_vectors.o(.text) }
 .rodata : SUBALIGN(4) { *(.rodata*) }
 .data : SUBALIGN(4) { *(.data*) }
 .bss : SUBALIGN(4) { *(.bss*) *(COMMON) }
}
func_8001B950_1C550 = 0x8001B950;
''')
        call([ld,'-T',script,'anim_matrix.o','gfx_wrapper.o','gfx_vectors.o','-o','graphics.elf'],cwd=p)
        symtab=call([readelf,'-Ws',p/'graphics.elf'])
        symbols={}
        for line in symtab.splitlines():
            f=line.split()
            if len(f)>=8 and f[3]=='FUNC' and f[6]!='UND':
                symbols[f[-1]]=(int(f[1],16),int(f[2],10))
        for sec,n in [('.text','segment0.bin'),('.text2','segment2.bin'),('.text3','segment3.bin')]:
            call([objcopy,'-O','binary',f'--only-section={sec}',p/'graphics.elf',p/n])
        rows=[]
        for name,binname,start,off,size,vma in FUNCTIONS:
            got=(p/binname).read_bytes()[start:start+size]
            original=rom[off:off+size]
            actual=symbols.get(name)
            if actual != (vma,size) or len(got)!=size:
                raise RuntimeError(f'Original address/FUNC size mismatch {name}: {actual}')
            mismatches=[i for i in range(0,size,4) if got[i:i+4]!=original[i:i+4]]
            rows.append({'name':name,'rom_offset':hex(off),'vma':hex(vma),'size':size,
                         'matched':not mismatches,
                         'first_mismatch':hex(mismatches[0]) if mismatches else None,
                         'original_sha256':hashlib.sha256(original).hexdigest(),
                         'reproduced_sha256':hashlib.sha256(got).hexdigest()})
    return {'format':'goemon-graphics-five-new-native-recheck-v1',
            'date_utc':'2026-11-17','region':'usa','status':'RESEARCH_ONLY',
            'original_rom_sha1':PINNED_ROM_SHA1,
            'production_accepted_usa':864,'production_accepted_japan':39,
            'original_compiler':'IDO 5.3 -O2 -mips2 -G 0 -non_shared',
            'native_original_address_results':rows,
            'matching_functions':sum(x['matched'] for x in rows),
            'matching_instruction_bytes':sum(x['size'] for x in rows if x['matched']),
            'original_source_blob_sha1':SOURCE_SHA1,
            'full_864_plus_5_rom_gate':'NOT_RUN',
            'full_canonical_inventory':'NOT_RUN',
            'full_original_relocation_equality':'NOT_RUN',
            'native_proof_tier':'ISOLATED_OR_COHERENT_GROUP_EXACT_NOT_PRODUCTION',
            'source_provenance':'Original GitHub PR #63 graphics research blobs; verified unmodified',
            'limitations':['Original-address scratch link used one explicit external target constant',
                           'No full 864-C production integration or canonical original ELF relocation proof',
                           'No source/ASM split staging; original production ASM must remain unchanged']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom',type=Path,required=True)
    p.add_argument('--ido',type=Path,required=True)
    p.add_argument('--readelf',default='mips-linux-gnu-readelf')
    p.add_argument('--ld',default='mips-linux-gnu-ld')
    p.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    p.add_argument('--sources',type=Path,default=Path(__file__).resolve().parents[1]/'graphics_adjacent_20261117')
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    result=verify(args.rom,args.ido,args.readelf,args.ld,args.objcopy,args.sources)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'native_exact':result['matching_functions'],
                      'native_bytes':result['matching_instruction_bytes'],
                      'full_864_plus_5_rom_gate':result['full_864_plus_5_rom_gate']}))
    if result['matching_functions']!=5:raise SystemExit(1)

if __name__=='__main__':main()
