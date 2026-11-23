#!/usr/bin/env python3
"""Independent ORIGINAL ASM reference experiment. Never a production waiver.

Original ASM is privately read from the authenticated, built Splat checkout.
Only two symbol expressions are changed in the shadow assembly source. No
compiled bytes, relocations or original production files are edited.
"""
import argparse, hashlib, json, os, re, subprocess, sys
from collections import Counter
from pathlib import Path

NAME='func_8003F37C_3FF7C'; SYMBOL='D_8007D108_7DD08'; TARGET=0x8007D108
VMA=0x8003F37C; OFFSET=0x3FF7C; SIZE=192
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
SOURCE_SHA='4cca0e20ec00d4b2e3b45b3acfe3d3c05fb74aa06c87f85e6da3026bdbee6cdb'
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
ASFLAGS='-EB -mtune=vr4300 -march=vr4300 -mabi=32 -Iinclude -I.'.split()
sha=lambda b:hashlib.sha256(b).hexdigest()

def require(test,message):
    if not test:raise ValueError(message)


def shadow_source(original):
    a=f'%hi({SYMBOL})';b=f'%lo({SYMBOL})';x='%hi(.Lvm_f37c_pool)';y='%lo(.Lvm_f37c_pool)'
    require(original.count(a)==original.count(b)==1,'original pool references not unique')
    result=original.replace(a,x).replace(b,y)
    require(result.replace(x,a).replace(y,b)==original,'non-pool source change')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    co=a.baseline.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32
    rom=(co/'config/usa/baserom.decompressed.z64').read_bytes();require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA and (co/'build/usa/mnsg.z64').read_bytes()==rom,'wrong original ROM')
    require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','upstream revision mismatch')
    cc=co/'tools/ido-5.3/cc';require(sha(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0','wrong IDO')
    source=Path(__file__).with_name('f37c.c');require(sha(source.read_bytes())==SOURCE_SHA,'wrong C source')
    old=Elf32((co/'build/usa/asm/usa/3DBA0.s.o').read_bytes());linked=Elf32((co/'build/usa/mnsg.elf').read_bytes());glob=linked.globals();require(glob[SYMBOL]==TARGET,'original pool identity mismatch')
    asm=(co/'asm/usa/3DBA0.s').read_text();match=re.search(r'^glabel '+NAME+r'\n.*?^endlabel '+NAME+r'\n',asm,re.M|re.S);require(match is not None,'original ASM function missing');body=match.group()
    require('/* 3FF80 8003F380' in body and '/* 3FF84 8003F384' in body,'original address annotations missing')
    # Read the original float from the original Splat data owner; the reference
    # does not use the C object's pool contents.
    data=(co/'asm/usa/data/main_continued.rodata.s').read_text();m=re.search(r'^dlabel '+SYMBOL+r'\n([^\n]+)\n([^\n]+)\nenddlabel '+SYMBOL+r'$',data,re.M);require(m is not None and '.float' in m[1] and '7DD08 8007D108' in m[1],'original data owner missing')
    float_line=m[1].split('*/',1)[1].strip()
    pre='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
    pool='\n.section .rodata, "a"\n.balign 4\n.Lvm_f37c_pool:\n'+float_line+'\n'
    named=pre+body+pool;shadow=pre+shadow_source(body)+pool
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
        if SYMBOL not in e.undefined():defs.append(f'{SYMBOL} = ADDR(.rodata);')
        script=out/(label+'.ld');script.write_text(f'ENTRY({NAME})\nSECTIONS {{ .text 0x{VMA:X} : SUBALIGN(4) {{ *(.text) }} .rodata 0x{base:X} : SUBALIGN(4) {{ *(.rodata) }} /DISCARD/ : {{ *(*) }} }}\n'+'\n'.join(defs)+'\n')
        dest=out/(label+'.elf');run([bins/'mips-linux-gnu-ld','-T',script,'--emit-relocs','-o',dest,obj]);return Elf32(dest.read_bytes())
    def assemble(text,label):
        f=out/(label+'.s');f.write_text(text);obj=out/(label+'.o');run([bins/'mips-linux-gnu-as',*ASFLAGS,'-o',obj,f]);return obj
    named_obj=assemble(named,'named_reference');shadow_obj=assemble(shadow,'shadow_reference')
    (a.repo.resolve()/'decomp/COMPILER_QUIRKS.md').read_text()
    c_obj=out/'native.o';run([cc,*FLAGS,source.resolve(),'-o',c_obj])
    e0,e1,e2=[Elf32(x.read_bytes()) for x in (named_obj,shadow_obj,c_obj)]
    r0,r1,r2=map(records,(e0,e1,e2));orig=records(old)
    missing=Counter({(4,5,SYMBOL):1,(8,6,SYMBOL):1});added=Counter({(4,5,'.rodata'):1,(8,6,'.rodata'):1})
    require(orig==r0 and sum(r0.values())==19,'named original relocations mismatch')
    require(r0-r1==missing and r1-r0==added and r1==r2,'independent section reference relocation mismatch')
    require(e0.code(e0.function(NAME))==e1.code(e1.function(NAME))==e2.code(e2.function(NAME)),'unlinked code differs')
    def verify(e):
        f=e.function(NAME);require(f.value==VMA and f.size==SIZE and e.code(f)==rom[OFFSET:OFFSET+SIZE],'linked original code mismatch')
        s=e.names.index('.rodata');require(e.sections[s][3]==TARGET and e.payload(s)[:4]==rom[0x7DD08:0x7DD0C] and not any(e.payload(s)[4:]),'original pool mismatch')
        require(e.globals()[SYMBOL]==TARGET,'named alias moved')
    for obj,label in ((named_obj,'named_linked'),(shadow_obj,'shadow_linked'),(c_obj,'native_linked')):verify(link(obj,label))
    cases=[]
    for label,obj,addr in [('wrong_pool_address',shadow_obj,TARGET+4),('wrong_pool_word',assemble(shadow.replace(float_line,'.float 0.2'),'wrong_pool_word'),TARGET),('wrong_pool_addend',assemble(shadow.replace('%lo(.Lvm_f37c_pool)','%lo(.Lvm_f37c_pool+4)'),'wrong_pool_addend'),TARGET)]:
        try:verify(link(obj,label+'_linked',addr))
        except ValueError:cases.append(label)
        else:raise AssertionError('negative accepted: '+label)
    result=dict(status='RESEARCH_ONLY_INDEPENDENT_ASM_REFERENCE_EXACT',function=NAME,base_sha='1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e',original_ROM_sha1=ROM_SHA,original_instruction_bytes=SIZE,original_code_sha256=sha(rom[OFFSET:OFFSET+SIZE]),native_source_sha256=SOURCE_SHA,original_asm_sha256=sha(body.encode()),shadow_asm_sha256=sha(shadow_source(body).encode()),named_original_relocations=19,shadow_reference_relocations=19,native_relocations=19,shadow_native_relocations_exact=True,original_to_shadow_removed=[list(x) for x in sorted(missing)],original_to_shadow_added=[list(x) for x in sorted(added)],pool_original_target=hex(TARGET),negative_controls_rejected=cases,compiler_quirk_outcome='EXISTING_QUIRK_REPRODUCED',canonical_named_relocation_gate='FAIL',full_new_claim_G2='NOT_RUN',full_new_claim_CI='NOT_RUN',gameplay='NOT_RUN')
    (out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
