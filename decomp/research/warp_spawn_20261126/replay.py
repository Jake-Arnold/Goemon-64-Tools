#!/usr/bin/env python3
"""Private-input replay of four isolated original-address IDO matches.
No ROM, generated assembly or compiled object is distributed with this script.
Run from an authenticated checkout with separately extracted pinned upstream.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
FLAGS = '-c -mips2 -O2 -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG'.split()
IDO_SHA256 = '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
ROMS = {'usa':'6ea0ed71032ce08fc2745f412d84936382197494','japan_0':'6f8745fecc3a5e7d4918c7a73353eb0726116ded'}
TARGETS = [
 ('usa','warp_wrapper','func_800358E8_364E8',124,['func_800357BC_363BC','func_80034D24_35924']),
 ('usa','player_init','func_800357BC_363BC',152,['func_80034CBC_358BC','func_80035964_36564']),
 ('japan_0','jp_warp_wrapper','func_80035558_36158',124,['func_8003542C_3602C','func_80034994_35594']),
 ('japan_0','jp_player_init','func_8003542C_3602C',152,['func_8003492C_3552C','func_800355D4_361D4']),
]

def sha(b): return hashlib.sha256(b).hexdigest()
def addr(s): return int(s.split('_')[1],16)
def rels(p):
    out=subprocess.check_output(['readelf','-Wr',str(p)],text=True)
    t=out.split("Relocation section '.rel.text'",1)[1].split('Relocation section',1)[0]
    return sorted((int(m[1],16),m[2],m[3]) for m in re.finditer(r'^([0-9a-f]+)\s+[0-9a-f]+\s+(R_MIPS_\w+)\s+[0-9a-f]+\s+(\S+)',t,re.M))
def identity(p,name):
    for l in subprocess.check_output(['readelf','-Ws',str(p)],text=True).splitlines():
        a=l.split()
        if len(a)==8 and a[-1]==name and a[3]=='FUNC':return (int(a[1],16),int(a[2]))
    raise AssertionError(name)
def main():
    p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    u=a.upstream.resolve();ido=u/'tools/ido-5.3/cc';assert sha(ido.read_bytes())==IDO_SHA256
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=u,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
    roms={r:(u/f'config/{r}/baserom.decompressed.z64').read_bytes() for r in ROMS}
    for r,b in roms.items():assert hashlib.sha1(b).hexdigest()==ROMS[r]
    rows=[]
    def run(*cmd):subprocess.run([str(x) for x in cmd],cwd=u,check=True,stdout=subprocess.DEVNULL)
    with tempfile.TemporaryDirectory(prefix='warp-proof-') as td:
        d=Path(td)
        for r,stem,name,n,callees in TARGETS:
            v=addr(name);off=int(name.split('_')[2],16);original=roms[r][off:off+n]
            if r=='usa':
                raw=(u/'asm/usa/35280.s').read_text();body=re.search(r'^glabel '+name+r'\n.*?^endlabel '+name+r'$',raw,re.M|re.S).group(0)
            else:body=(u/f'asm/japan_0/nonmatchings/main_34EF0/{name}.s').read_text()
            ref=d/'ref.s';ref.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text,"ax"\n'+body+'\n')
            ro=d/'ref.o';run('mips-linux-gnu-as','-EB','-mips3','-32','-I','include','-o',ro,ref)
            ld=d/'link.ld';ld.write_text(f'SECTIONS {{ .text {v:#x} : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(*) }} }}\n')
            def link(obj):
                elf=obj.with_suffix('.elf');b=obj.with_suffix('.bin');args=[]
                for c in callees:args+=['--defsym',f'{c}={addr(c):#x}']
                run('mips-linux-gnu-ld','-EB','-T',ld,*args,'-o',elf,obj);run('mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,b)
                return b.read_bytes()[:n],identity(elf,name)
            def textbytes(obj):
                b=obj.with_suffix('.raw');run('mips-linux-gnu-objcopy','-O','binary','-j','.text',obj,b);return b.read_bytes()[:n]
            rb,ri=link(ro);assert rb==original and ri==(v,n)
            src=HERE/(stem+'.c');negative=HERE/(stem+'_negative.c')
            for path,positive in [(src,True),(negative,False)]:
                ledger=a.ledger.read_bytes() # mandatory fresh preflight before each attempt
                obj=d/(path.stem+'.o');run(ido,*FLAGS,'-o',obj,path)
                b,i=link(obj);rs=rels(obj);rr=rels(ro);raw_exact=textbytes(obj)==textbytes(ro)
                matched=b==original and i==(v,n) and rs==rr and raw_exact
                diff=next((k for k in range(0,n,4) if b[k:k+4]!=original[k:k+4]),None)
                assert matched==positive,(name,positive,i,diff,rs,rr,raw_exact)
                rows.append(dict(region=r,function=name,rom_offset=hex(off),vma=hex(v),size=n,source=path.name,source_sha256=sha(path.read_bytes()),compiler_ledger_sha256=sha(ledger),positive=positive,outcome='NO_NEW_COMPILER_FINDING',first_instruction_mismatch=None if diff is None else hex(diff),match=matched,linked_sha256=sha(b),original_sha256=sha(original),original_rom_sha1=ROMS[r],function_identity_exact=i==(v,n),named_text_relocations_exact=rs==rr,relocations=rs,raw_object_text_exact=raw_exact))
    a.output.write_text(json.dumps(dict(status='RESEARCH_ONLY',compiler_sha256=IDO_SHA256,flags=FLAGS,attempts=rows,whole_rom='NOT_RUN',strict_candidate_inventory='NOT_RUN',promotion_integrity='NOT_RUN'),indent=2)+'\n')
    print('PASS: 4 positives and 4 rejected negative controls')
if __name__=='__main__':main()
