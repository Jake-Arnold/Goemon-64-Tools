#!/usr/bin/env python3
"""Independent ORIGINAL ASM reference experiment. Never a production waiver.

Original ASM is privately read from the authenticated, built Splat checkout.
Only pool and intra-function symbol visibility change in shadow assembly. No
compiled bytes, relocations or original production files are edited.
"""
import argparse, hashlib, json, os, re, subprocess, sys
from collections import Counter
from pathlib import Path

NAME='func_8003DF98_3EB98'; SYMBOL='jtbl_8007D068_7DC68'; TARGET=0x8007D068
VMA=0x8003DF98; OFFSET=0x3EB98; SIZE=528
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
SOURCE_SHA='8eaf68308afa51862d07ee5795db6cbfd09250070bd243ad69744f6aa144a1f9'
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
ASFLAGS='-EB -mtune=vr4300 -march=vr4300 -mabi=32 -Iinclude -I.'.split()
sha=lambda b:hashlib.sha256(b).hexdigest()

def require(test,message):
    if not test:raise ValueError(message)


def shadow_source(original):
    require(original.count(f'%hi({SYMBOL})')==original.count(f'%lo({SYMBOL})')==1,'pool references not unique')
    result=original.replace(SYMBOL,'.Lvm_dispatch_pool')
    result,n=re.subn(r'(?m)^  jlabel (\.L\w+)$',r'  \1:',result)
    require(n==21,'unexpected dispatch target count')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    co=a.baseline.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32
    rom=(co/'config/usa/baserom.decompressed.z64').read_bytes();require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA and (co/'build/usa/mnsg.z64').read_bytes()==rom,'wrong original ROM')
    require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','upstream revision mismatch')
    cc=co/'tools/ido-5.3/cc';require(sha(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0','wrong IDO')
    source=Path(__file__).with_name('df98.c');require(sha(source.read_bytes())==SOURCE_SHA,'wrong C source')
    old=Elf32((co/'build/usa/asm/usa/3DBA0.s.o').read_bytes());linked=Elf32((co/'build/usa/mnsg.elf').read_bytes());glob=linked.globals();require(glob[SYMBOL]==TARGET,'original pool identity mismatch')
    asm=(co/'asm/usa/3DBA0.s').read_text();match=re.search(r'^glabel '+NAME+r'\n.*?^endlabel '+NAME+r'\n',asm,re.M|re.S);require(match is not None,'original ASM function missing');body=match.group()
    require('/* 3EBBC 8003DFBC' in body and '/* 3EBC4 8003DFC4' in body,'original address annotations missing')
    data=(co/'asm/usa/data/main_continued.rodata.s').read_text();m=re.search(r'^dlabel '+SYMBOL+r'\n(.*?)^enddlabel '+SYMBOL+r'$',data,re.M|re.S);require(m is not None,'original data owner missing')
    table=m[1];require(len(re.findall(r'\.word \.L\w+',table))==40,'wrong table count')
    olddata=Elf32((co/'build/usa/asm/usa/data/main_continued.rodata.s.o').read_bytes())
    pre='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
    pool='\n.section .rodata, "a"\n.balign 4\n'
    named=pre+body+pool+'dlabel '+SYMBOL+'\n'+table+'enddlabel '+SYMBOL+'\n'
    shadow=pre+shadow_source(body)+pool+'.Lvm_dispatch_pool:\n'+table
    env=os.environ.copy();env['LD_LIBRARY_PATH']=str(a.lib.resolve())+':'+env.get('LD_LIBRARY_PATH','');bins=a.binutils.resolve()
    def run(cmd):subprocess.run([str(x) for x in cmd],cwd=co,env=env,check=True,stdout=subprocess.DEVNULL)
    def records(e):
        f=e.function(NAME)
        return Counter((r.offset-f.value,r.relocation_type,r.symbol.name or e.names[r.symbol.section]) for r in e.relocations(f.section) if f.value<=r.offset<f.value+f.size)
    def link(obj,label,base=TARGET):
        e=Elf32(obj.read_bytes());defs=[]
        for n in sorted(e.undefined()):
            require(n in glob and re.fullmatch(r'[A-Za-z_.$][A-Za-z0-9_.$]*',n),'unexpected undefined symbol')
            defs.append(f'{n} = 0x{glob[n]:08x};')
        if SYMBOL not in e.globals():defs.append(f'{SYMBOL} = ADDR(.rodata);')
        script=out/(label+'.ld');script.write_text(f'ENTRY({NAME})\nSECTIONS {{ .text 0x{VMA:X} : SUBALIGN(4) {{ *(.text) }} .rodata 0x{base:X} : SUBALIGN(4) {{ *(.rodata) }} /DISCARD/ : {{ *(*) }} }}\n'+'\n'.join(defs)+'\n')
        dest=out/(label+'.elf');run([bins/'mips-linux-gnu-ld','-T',script,'--emit-relocs','-o',dest,obj]);return Elf32(dest.read_bytes())
    def assemble(text,label):
        f=out/(label+'.s');f.write_text(text);obj=out/(label+'.o');run([bins/'mips-linux-gnu-as',*ASFLAGS,'-o',obj,f]);return obj
    named_obj=assemble(named,'named_reference');shadow_obj=assemble(shadow,'shadow_reference')
    (a.repo.resolve()/'decomp/COMPILER_QUIRKS.md').read_text()
    c_obj=out/'native.o';run([cc,*FLAGS,source.resolve(),'-o',c_obj])
    e0,e1,e2=[Elf32(x.read_bytes()) for x in (named_obj,shadow_obj,c_obj)]
    def table_records(e,start=0):
        k=e.names.index('.rodata')
        return Counter((r.offset-start,r.relocation_type,r.symbol.name or e.names[r.symbol.section]) for r in e.relocations(k) if start<=r.offset<start+160)
    r0,r1,r2=map(records,(e0,e1,e2));orig=records(old)
    t0,t1,t2=map(table_records,(e0,e1,e2));t_orig=table_records(olddata,olddata.globals()[SYMBOL])
    require(orig==r0 and t0==t_orig,'named original relocations mismatch')
    require(r1==r2 and t1==t2 and sum(t2.values())==40,'independent section reference relocation mismatch')
    require(e1.code(e1.function(NAME))==e2.code(e2.function(NAME)),'unlinked shadow code differs')
    require(e1.payload(e1.names.index('.rodata'))[:160]==e2.payload(e2.names.index('.rodata'))[:160],'unlinked shadow table differs')
    def verify(e):
        f=e.function(NAME);require(f.value==VMA and f.size==SIZE and e.code(f)==rom[OFFSET:OFFSET+SIZE],'linked original code mismatch')
        s=e.names.index('.rodata');require(e.sections[s][3]==TARGET and e.payload(s)[:160]==rom[0x7DC68:0x7DD08] and not any(e.payload(s)[160:]),'original table mismatch')
        require(e.globals()[SYMBOL]==TARGET,'named alias moved')
    for obj,label in ((named_obj,'named_linked'),(shadow_obj,'shadow_linked'),(c_obj,'native_linked')):verify(link(obj,label))
    first=re.findall(r'\.word (\.L\w+)',table);wrong_table=table.replace('.word '+first[0],'.word '+first[1],1)
    cases=[]
    for label,obj,addr in [('wrong_table_address',shadow_obj,TARGET+4),('wrong_table_entry',assemble(shadow.replace(table,wrong_table),'wrong_table_entry'),TARGET),('wrong_branch_target',assemble(shadow.replace('beqz       $at, .L8003E190_3ED90','beqz       $at, .L8003E194_3ED94'),'wrong_branch_target'),TARGET)]:
        try:verify(link(obj,label+'_linked',addr))
        except ValueError:cases.append(label)
        else:raise AssertionError('negative accepted: '+label)
    result=dict(status='RESEARCH_ONLY_INDEPENDENT_ASM_REFERENCE_EXACT',function=NAME,base_sha='1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e',original_ROM_sha1=ROM_SHA,original_instruction_bytes=SIZE,original_code_sha256=sha(rom[OFFSET:OFFSET+SIZE]),native_source_sha256=SOURCE_SHA,original_asm_sha256=sha(body.encode()),shadow_asm_sha256=sha(shadow_source(body).encode()),named_original_text_relocations=sum(r0.values()),shadow_reference_text_relocations=sum(r1.values()),native_text_relocations=sum(r2.values()),named_original_table_relocations=sum(t0.values()),shadow_native_table_relocations=sum(t2.values()),shadow_native_relocations_exact=True,original_to_shadow_text_removed=[list(x) for x in sorted((r0-r1).elements())],original_to_shadow_text_added=[list(x) for x in sorted((r1-r0).elements())],original_to_shadow_table_removed=[list(x) for x in sorted((t0-t1).elements())],original_to_shadow_table_added=[list(x) for x in sorted((t1-t0).elements())],pool_original_target=hex(TARGET),negative_controls_rejected=cases,compiler_quirk_outcome='EXISTING_QUIRK_REPRODUCED',canonical_named_relocation_gate='FAIL',full_new_claim_G2='NOT_RUN',full_new_claim_CI='NOT_RUN',gameplay='NOT_RUN')
    (out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
