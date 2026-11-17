#!/usr/bin/env python3
"""Read-only exact native IDO verifier for source-only resource27 research.

User supplies own legally held *decompressed* USA retail ROM and original
IDO/mips toolchain. Generates ELF/MIPS outputs in a local temporary directory.
No ROM/game assets included in this source or committed to GitHub.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, tempfile

SHA='6ea0ed71032ce08fc2745f412d84936382197494'
CCFLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
GROUPS=(
    ('group490.c', 0x08000490, 0x6AF8A0, 108, 3),
    ('group59c.c', 0x0800059C, 0x6AF9AC, 172, 3),
    ('group8c4.c', 0x080008C4, 0x6AFCD4, 276, 3),
    ('groupa7c.c', 0x08000A7C, 0x6AFE8C, 380, 5),
    ('group1380.c',0x08001380, 0x6B0790, 304, 5),
    ('wrapper172c_v1.c',0x0800172C,0x6B0B3C,64,1),
    ('noop37ec_v1.c', 0x080037EC, 0x6B2BFC,12,1),
)
FILE25=('file25_last_v3.c',0x08001228,0x6AE5E8,72,1)

def run(cmd,env=None):
    p=subprocess.run([str(x) for x in cmd], capture_output=True, text=True, env=env)
    if p.returncode:
        raise RuntimeError(f'{cmd[0]} returned {p.returncode}:\n{p.stderr[-2500:]}')
    return p.stdout

def symbols_from_source(text):
    defined=set(re.findall(r'^\s*(?:void|int|u32)\s+(func_[A-Fa-f0-9_]+)\s*\([^\n)]*\)\s*\{',text,re.M))
    external=set(re.findall(r'^extern\s+[^\n]*?\b((?:func|D)_[A-Fa-f0-9_]+)\s*(?=\(|;)',text,re.M))
    external-=defined
    return {s:int(s.split('_')[1],16) for s in external}, defined

def unit(source,vm,offset,size,count,rom,ido,assembler,linker,objcopy,root,env):
    src=root/source
    text=src.read_text()
    syms,names=symbols_from_source(text)
    assert len(names)==count,(source,names,count)
    stem=root/('unit_'+source.replace('.c',''))
    obj=stem.with_suffix('.o');ld=stem.with_suffix('.ld');elf=stem.with_suffix('.elf');data=stem.with_suffix('.bin')
    run([ido,*CCFLAGS,'-o',obj,src],env)
    ld.write_text(f'SECTIONS {{ .text 0x{vm:08X} : SUBALIGN(4) {{ *(.text) *(.text.*) }} /DISCARD/ : {{ *(.note*) *(.comment*) }} }}\n')
    run([linker,'-T',ld,*[f'--defsym={s}=0x{val:08X}' for s,val in syms.items()],'-o',elf,obj],env)
    run([objcopy,'-O','binary','-j','.text',elf,data],env)
    actual=data.read_bytes();expected=rom[offset:offset+size]
    if actual[:size]!=expected or any(actual[size:]):
        idx=next((n for n,(a,b) in enumerate(zip(actual,expected)) if a!=b),None)
        raise AssertionError(f'{source}: MIPS mismatch original=0x{offset:X}, first mismatch={idx}, full generated length={len(actual)}')
    original_sh=hashlib.sha256(expected).hexdigest()
    return {'source':source,'vma':f'0x{vm:08X}','rom':f'0x{offset:X}','functions':count,'matched_original_instruction_bytes':size,'original_sha256':original_sh,'passed':True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom',type=Path,required=True,help='own decompressed USA 32 MiB ROM')
    p.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--ido',type=Path,required=True)
    p.add_argument('--linker',default='mips-linux-gnu-ld')
    p.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    p.add_argument('--include-file25',action='store_true',help='isolated match only; has extra source relocation')
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    rom=args.rom.read_bytes();assert len(rom)==33_554_432 and hashlib.sha1(rom).hexdigest()==SHA
    env=dict(os.environ)
    with tempfile.TemporaryDirectory(prefix='goemon-file27-') as tmp:
        out=Path(tmp)
        for f in (args.source_dir).iterdir():
            if f.suffix=='.c':(out/f.name).write_bytes(f.read_bytes())
        groups=list(GROUPS)+(list([FILE25]) if args.include_file25 else [])
        results=[unit(*g,rom,args.ido,'',args.linker,args.objcopy,out,env) for g in groups]
    summary={'status':'PASS','region':'usa','decompressed_rom_sha1':SHA,
     'function_count':sum(x['functions'] for x in results),'original_instruction_bytes':sum(x['matched_original_instruction_bytes'] for x in results),
     'contains_upstream_full_rom_proof':False,'canonical_decomp_production_proof':False,
     'file25_relocation_warning':'File25 C uses extra address-symbol relocations and is isolated-only' if args.include_file25 else None,'units':results}
    if args.report:args.report.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
