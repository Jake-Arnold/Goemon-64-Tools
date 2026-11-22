#!/usr/bin/env python3
"""Fail-closed isolated original-address Japanese MIPS IDO comparison.

Not a complete 32 MiB original-ROM G2 verifier. Does not modify the repository.
Requires the user's original authenticated expanded Japan rev-0 image and tools.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, tempfile
from pathlib import Path

ROM_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
SYMBOLS = {
    'g_system_ptr': 0x80161DB8,
    'D_C5F78': 0xC5F78,
    'D_C5F7C': 0xC5F7C,
    'D_8005B960_5C560': 0x8005B960,
    'D_800708B8_714B8': 0x800708B8,
    'func_800058D0_64D0': 0x800058D0,
    'D_8016D6DA_16E2DA': 0x8016D6DA,
}
R = lambda offset, kind, sym: (offset, f'R_MIPS_{kind}', sym)
TARGETS = [
    ('func_80008500_9100', 0x9100, 64, [
        R(0,'HI16','g_system_ptr'), R(4,'LO16','g_system_ptr'),
        R(12,'HI16','D_8005B960_5C560'), R(24,'LO16','D_8005B960_5C560'),
        R(16,'HI16','D_C5F78'), R(36,'LO16','D_C5F78'),
        R(28,'HI16','D_800708B8_714B8'), R(44,'LO16','D_800708B8_714B8'),
        R(40,'26','func_800058D0_64D0'),
    ]),
    ('func_80008540_9140', 0x9140, 24, [
        R(0,'HI16','g_system_ptr'), R(4,'LO16','g_system_ptr'),
        R(8,'HI16','D_C5F7C'), R(20,'LO16','D_C5F7C'),
    ]),
    ('func_80008558_9158', 0x9158, 28, []),
    ('func_80010118_10D18', 0x10D18, 28, [
        R(12,'HI16','D_8016D6DA_16E2DA'), R(24,'LO16','D_8016D6DA_16E2DA'),
    ]),
]

def run(args):
    p = subprocess.run(list(map(str,args)),text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError(f'FAILED {args}: code {p.returncode}\n{p.stderr[-1500:]}')
    return p.stdout

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--cc',type=Path,required=True)
    ap.add_argument('--ld',default='mips-linux-gnu-ld')
    ap.add_argument('--objdump',default='mips-linux-gnu-objdump')
    ap.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    ap.add_argument('--report',type=Path)
    a = ap.parse_args()
    data=a.rom.read_bytes()
    if len(data)!=33554432 or hashlib.sha1(data).hexdigest()!=ROM_SHA1:
        raise ValueError('Original Japan rev-0 expanded ROM size/SHA-1 mismatch')
    src=Path(__file__).resolve().parent/'src'
    rows=[]
    with tempfile.TemporaryDirectory(prefix='goemon-jp-new4-') as tmp:
        tmp=Path(tmp)
        for name,off,size,expected_reloc in TARGETS:
            original=data[off:off+size]
            vma=0x80000000+off-0xC00
            cs=src/(name+'.c')
            obj=tmp/(name+'.o');elf=tmp/(name+'.elf');s=tmp/(name+'.ld'); b=tmp/(name+'.bin')
            run([a.cc,'-c','-non_shared','-G','0','-O2','-mips2','-o',obj,cs])
            reltxt=run([a.objdump,'-r',obj])
            observed=[(int(m.group(1),16),m.group(2),m.group(3))
                for m in re.finditer(r'^\s*([0-9a-fA-F]{8})\s+(R_MIPS_\w+)\s+(\S+)',reltxt,re.M)]
            if sorted(observed)!=sorted(expected_reloc):
                raise AssertionError(f'{name} semantic relocation mismatch: {observed!r} != {expected_reloc!r}')
            s.write_text(''.join(f'{k} = 0x{v:X};\n' for k,v in SYMBOLS.items())+
                f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(1) {{ *(.text) }} '
                '/DISCARD/ : { *(.comment) *(.note*) } }\n')
            run([a.ld,'-T',s,'-o',elf,obj])
            symbol_txt=run([a.objdump,'-t',elf])
            if not re.search('^'+f'{vma:08x}'+r'\s+g\s+F\s+\.text\s+\S+\s+'+name+r'$',symbol_txt,re.M):
                raise AssertionError(f'{name}: missing exact original-address function symbol')
            run([a.objcopy,'-O','binary','--only-section=.text',elf,b])
            code=b.read_bytes()
            if len(code)<size: raise AssertionError(f'{name}: compiled too short ({len(code)}<{size})')
            for i in range(0,size,4):
                if code[i:i+4]!=original[i:i+4]:
                    raise AssertionError(f'{name} original-address mismatch +0x{i:X}: {original[i:i+4].hex()} != {code[i:i+4].hex()}')
            if any(code[size:]):raise AssertionError(f'{name}: nonzero trailing code/padding')
            record={
                'name':name, 'expanded_rom_offset':f'0x{off:X}',
                'original_guest_vma':f'0x{vma:X}',
                'original_extent_bytes':size,
                'original_instruction_sha256':hashlib.sha256(original).hexdigest(),
                'original_C_source_sha256':hashlib.sha256(cs.read_bytes()).hexdigest(),
                'native_original_address_exact_bytes':size,
                'trailing_zero_text_alignment_bytes':len(code)-size,
                'symbolic_relocations':[{'offset':offset,'type':kind,'symbol':sym} for offset,kind,sym in sorted(observed)],
                'native_instruction_match':True,
                'original_symbolic_reloc_match':True,
            }
            rows.append(record)
            print(f'PASS_ISOLATED_NATIVE {name} {size}/{size} original bytes; {len(observed)} relocations')
    proof={
        'format':'goemon-japan-new-four-research-only-v1', 'region':'japan_0',
        'status':'PASSED_ISOLATED_NATIVE / RESEARCH_ONLY',
        'rom_bytes':33554432,'original_rom_sha1':ROM_SHA1,
        'compiler':'SGI IDO 5.3 -O2 -mips2 -G 0',
        'new_candidate_functions':len(rows),
        'native_exact_original_bytes':sum(r['original_extent_bytes'] for r in rows),
        'isolated_symbolic_relocations':sum(len(r['symbolic_relocations']) for r in rows),
        'records':rows,
        'complete_japan_32MiB_rom':'NOT_RUN',
        'complete_japan_retail_16MiB_rom':'NOT_RUN',
        'all_7376_original_ELF_function_identities':'NOT_RUN',
        'all_80747_original_semantic_relocations':'NOT_RUN',
        'strict_C_ASM_inventory':'NOT_RUN',
        'full_local_CI':'NOT_RUN','newly_promoted_C_functions':0,
    }
    if a.report:a.report.write_text(json.dumps(proof,indent=2)+'\n')
    print('ISOLATED ONLY: four unique candidates, 144/144 original bytes, 15/15 isolated relocs; NO PROMOTION')

if __name__=='__main__':main()
