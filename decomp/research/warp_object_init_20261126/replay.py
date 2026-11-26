#!/usr/bin/env python3
"""Independent native task-system text-owner replay. Private ROM/toolchain inputs only."""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLAGS = '-c -mips2 -O2 -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG'.split()
PIN = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
IDO = '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
HEADER = '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
REGIONS = [
    ('usa', 'usa', 0x35280, 'df8083a54296b8c151917c5333e1c85f014a2a66', '6ea0ed71032ce08fc2745f412d84936382197494', 'func_80035964_36564', 'func_80035A5C_3665C'),
    ('jp', 'japan_0', 0x34ef0, '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b', '6f8745fecc3a5e7d4918c7a73353eb0726116ded', 'func_800355D4_361D4', 'func_800356CC_362CC'),
]

def sha(b): return hashlib.sha256(b).hexdigest()

def syms(p):
    out = subprocess.check_output(['readelf', '-Ws', str(p)], text=True)
    return [(a[-1], int(a[1],16), int(a[2]), a[3], a[6]) for l in out.splitlines() if len(a:=l.split())==8 and a[0].rstrip(':').isdigit()]

def funcs(p): return sorted((n,v,z) for n,v,z,t,sh in syms(p) if t=='FUNC' and z>0 and sh!='UND')

def rels(p):
    out = subprocess.check_output(['readelf', '-Wr', str(p)], text=True)
    t = out.split("Relocation section '.rel.text'",1)[1].split('Relocation section',1)[0]
    return sorted((int(m[1],16),m[2],int(m[3],16),m[4]) for m in re.finditer(r'^([0-9a-f]+)\s+[0-9a-f]+\s+(R_MIPS_\w+)\s+([0-9a-f]+)\s+(\S+)',t,re.M))

def main():
    p=argparse.ArgumentParser();p.add_argument('--usa-upstream',type=Path,required=True);p.add_argument('--jp-upstream',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=[]
    with tempfile.TemporaryDirectory(prefix='warp-owner-') as td:
        for tag,region,off,retail,expanded,f1,f2 in REGIONS:
            u=(a.usa_upstream if tag=='usa' else a.jp_upstream).resolve();d=Path(td)/tag;d.mkdir();base=0x80000000+off-0xc00
            def run(*cmd): return subprocess.check_output(list(map(str,cmd)),cwd=u,stderr=subprocess.STDOUT)
            assert run('git','rev-parse','HEAD').decode().strip()==PIN
            assert not run('git','status','--porcelain','--untracked-files=no')
            ido=u/'tools/ido-5.3/cc';assert sha(ido.read_bytes())==IDO
            assert hashlib.sha1((u/f'config/{region}/baserom.z64').read_bytes()).hexdigest()==retail
            rom=(u/f'config/{region}/baserom.decompressed.z64').read_bytes();assert hashlib.sha1(rom).hexdigest()==expanded
            original=rom[off:off+0x14d0]
            if tag=='usa': asm=(u/'asm/usa/35280.s').read_text()
            else: asm=HEADER+''.join((u/path).read_text()+'\n' for path in re.findall(r'GLOBAL_ASM\("([^"]+)"\)',(u/'src/main_34EF0.c').read_text()))
            prefix=asm[:asm.index('nonmatching '+f1)].replace('.section .text, "ax"','.section .text.prefix, "ax"')
            def assemble(name,src):
                s=d/(name+'.s');s.write_text(src);o=d/(name+'.o');run('mips-linux-gnu-as','-EB','-mips3','-32','-I','include','-o',o,s);return o
            ref=assemble('owner_ref',asm);pre=assemble('prefix',prefix)
            def extract(p,section='.text'):
                b=p.with_suffix('.raw');run('mips-linux-gnu-objcopy','-O','binary','-j',section,p,b);return b.read_bytes()
            ref_raw=extract(ref);assert len(ref_raw)==0x14d0
            ref_rels=rels(ref);symmap={}
            for path in [u/f'config/{region}/symbol_addrs/symbol_addrs.txt',u/f'.splat/{region}/undefined_syms_auto.ld',u/f'.splat/{region}/undefined_funcs_auto.ld']:
                symmap.update((m[1],int(m[2],16)) for m in re.finditer(r'^(\w+)\s*=\s*(0x[\da-fA-F]+);',path.read_text(),re.M))
            def defs(objects):
                defined={n for obj in objects for n,_,_,_,sh in syms(obj) if sh!='UND'}
                und={n for obj in objects for n,_,_,_,sh in syms(obj) if sh=='UND'}-defined
                args=[]
                for n in sorted(und):
                    v=symmap.get(n)
                    if v is None:
                        m=re.fullmatch(r'(?:func|D)_([\da-fA-F]+)(?:_[\da-fA-F]+)?',n);assert m,n;v=int(m[1],16)
                    args+=['--defsym',f'{n}={v:#x}']
                return args
            def link(name,objs,vma,owner=False):
                ld=d/(name+'.ld');ld.write_text(f'SECTIONS {{ .text {vma:#x} : SUBALIGN(4) {{ *(.text.prefix) *(.text)'+(' . = ALIGN(16);' if owner else '')+' } /DISCARD/ : { *(*) } }\n');elf=d/(name+'.elf');run('mips-linux-gnu-ld','-EB','--emit-relocs','-T',ld,*defs(objs),'-o',elf,*objs);return elf,extract(elf)
            origelf,orig=link('original_owner',[ref],base,True);assert orig==original
            assert len(funcs(origelf))==59 and len(rels(origelf))==167
            tail=(HERE/(tag+'_tail.c')).read_text();second=tail.index('Task *'+f2);first=tail.index('Task *'+f1)
            variants=[(f1,tail[:second],0x12e4,248),(f2,tail[:first]+tail[second:],0x13dc,232)]
            def compile_src(name,src):
                ledger=a.ledger.read_bytes()  # mandatory preflight for each attempt
                assert b'Per-native-attempt outcome' in ledger
                path=d/(name+'.c');path.write_text(src);o=path.with_suffix('.o');run(ido,*FLAGS,'-o',o,path);return o,sha(ledger)
            attempts=[]
            for idx,(name,src,start,n) in enumerate(variants):
                for kind,source in [('positive',src),('negative',src.replace('o->field7e=0;','o->field7e=1;'))]+([('numeric_offset',src.replace('(unsigned int)D_C2D90','0xC2D90u'))] if idx==0 else []):
                    obj,ledger_sha=compile_src(f'{idx}_{kind}',source);elf,b=link(f'{idx}_{kind}_linked',[obj],base+start);raw=extract(obj)
                    expected=original[start:start+n];ownrel=[(at-start,t,val,s) for at,t,val,s in ref_rels if start<=at<start+n]
                    linkedref=[r for r in rels(origelf) if base+start<=r[0]<base+start+n]
                    identity=funcs(elf)==[(name,base+start,n)];raw_equal=raw[:n]==ref_raw[start:start+n];raw_rels_equal=rels(obj)==ownrel;linked_rels_equal=rels(elf)==linkedref
                    exact=b[:n]==expected and identity and raw_equal and raw_rels_equal and linked_rels_equal
                    assert exact==(kind=='positive'),(tag,name,kind)
                    mismatch=next((k for k in range(0,n,4) if b[k:k+4]!=expected[k:k+4]),None)
                    if mismatch is None and not linked_rels_equal: category='relocation provenance'
                    elif mismatch is not None: category='instruction / scheduling'
                    else: category=None
                    attempts.append(dict(function=name,vma=hex(base+start),rom_offset=hex(off+start),size=n,compiled_function_size=funcs(elf)[0][2],kind=kind,source_sha256=sha(source.encode()),ledger_sha256=ledger_sha,linked_sha256=sha(b[:n]),original_sha256=sha(expected),function_identity_exact=identity,raw_text_exact=raw_equal,raw_relocs_exact=raw_rels_equal,linked_relocs_exact=linked_rels_equal,first_instruction_mismatch=None if mismatch is None else hex(mismatch),mismatch_category=category,match=exact,outcome='EXISTING_QUIRK_REPRODUCED' if kind=='numeric_offset' else 'NO_NEW_COMPILER_FINDING',raw_relocations=rels(obj),linked_relocations=rels(elf)))
            co,ls=compile_src('combined_tail',tail);cr=extract(co);assert cr==ref_raw[0x12e4:0x14c4]
            assert rels(co)==[(at-0x12e4,t,val,s) for at,t,val,s in ref_rels if at>=0x12e4]
            mixelf,mix=link('mixed_owner',[pre,co],base,True);assert mix==original and funcs(mixelf)==funcs(origelf) and rels(mixelf)==rels(origelf)
            def ext(p):return {n:(v,z,t) for n,v,z,t,sh in syms(p) if sh=='ABS' and t!='FILE'}
            ea,eb=ext(origelf),ext(mixelf);assert set(ea)==set(eb);assert all(ea[k][:2]==eb[k][:2] for k in ea)
            types={k:[ea[k][2],eb[k][2]] for k in ea if ea[k]!=eb[k]}
            rows.append(dict(region=region,retail_sha1=retail,expanded_sha1=expanded,attempts=attempts,combined_source_sha256=sha(tail.encode()),combined_ledger_sha256=ls,combined_outcome='EXISTING_QUIRK_REPRODUCED' if types else 'NO_NEW_COMPILER_FINDING',owner_offset=hex(off),owner_vma=hex(base),owner_bytes=len(original),owner_sha256=sha(original),owner_equal=True,func_count=len(funcs(origelf)),function_identities_equal=True,relocation_count=len(rels(origelf)),named_relocations_equal=True,absolute_symbol_type_differences=types,absolute_symbol_values_equal=True))
    a.output.write_text(json.dumps(dict(status='UNIT_TEXT_EXACT_RESEARCH_ONLY',upstream=PIN,compiler_sha256=IDO,flags=FLAGS,regions=rows,full_candidate_rom='NOT_RUN',strict_candidate_inventory='NOT_RUN',promotion_integrity='NOT_RUN'),indent=2)+'\n')
    print('PASS: four isolated functions, six rejected controls, two complete 5328-byte text owners')
if __name__=='__main__':main()
