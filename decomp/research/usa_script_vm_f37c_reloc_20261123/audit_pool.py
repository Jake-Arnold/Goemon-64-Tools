#!/usr/bin/env python3
"""Independent target-equivalence audit; never modifies a native or production object."""
import argparse, hashlib, json, struct, subprocess, os, sys
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--probes',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32
name='func_8003F37C_3FF7C';named='D_8007D108_7DD08';vma=0x8003F37C;pool=0x8007D108;romoff=0x3FF7C;pooloff=0x7DD08
rom=(a.baseline/'config/usa/baserom.decompressed.z64').read_bytes();assert hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494'
orig=Elf32((a.baseline/'build/usa/asm/usa/3DBA0.s.o').read_bytes());ref=Elf32((a.baseline/'build/usa/mnsg.elf').read_bytes());assert ref.globals()[named]==pool
obj=(a.probes/'01_literal.o').read_bytes();linked=(a.probes/'01_literal.elf').read_bytes()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def records(e,f):
    return Counter((r.offset-f.value,r.relocation_type,r.symbol.name or e.names[r.symbol.section]) for r in e.relocations(f.section) if f.value<=r.offset<f.value+f.size)
def pair_target(code):
    hi,lo=struct.unpack_from('>II',code,4);require(hi>>16==0x3c01 and lo>>16==0xc422,'unexpected load encoding');add=lo&65535;return ((hi&65535)<<16)+(add if add<32768 else add-65536)
def audit(raw,elf):
    e=Elf32(raw);f=e.function(name);l=Elf32(elf);lf=l.function(name);of=orig.function(name)
    require(f.size==lf.size==of.size==192 and lf.value==vma,'wrong function extent')
    require(l.code(lf)==rom[romoff:romoff+192],'wrong linked instructions')
    old=records(orig,of);new=records(e,f)
    require(sum(old.values())==sum(new.values())==19 and old-new==Counter({(4,5,named):1,(8,6,named):1}) and new-old==Counter({(4,5,'.rodata'):1,(8,6,'.rodata'):1}),'unexpected relocation delta')
    s=e.names.index('.rodata');ls=l.names.index('.rodata');require(e.sections[s][2]==2 and l.sections[ls][2]==2 and l.sections[ls][3]==pool,'wrong pool address or flags')
    data=e.payload(s);require(len(data)==16 and data[:4]==rom[pooloff:pooloff+4] and not any(data[4:]),'wrong native pool bytes')
    require(l.payload(ls)==data,'linked pool differs')
    for offset,kind in ((4,5),(8,6)):
        matches=[r for r in e.relocations(f.section) if r.offset-f.value==offset]
        require(len(matches)==1 and matches[0].relocation_type==kind and matches[0].symbol.kind==3 and matches[0].symbol.section==s and matches[0].symbol.value==0,'wrong native pool symbol')
    require(pair_target(e.code(f))==0,'wrong native pool addend')
    require(pair_target(l.code(lf))==pair_target(rom[romoff:romoff+192])==pool,'wrong resolved address')
    require(records(l,lf)==new,'unexpected linked relocation change')
    return {'status':'TARGET_EQUIVALENCE_ONLY_CANONICAL_RELOC_FAIL','exact_instructions':48,'original_named_relocations':19,'unchanged_named_relocations':17,'resolved_original_target':hex(pool),'native_pool_addend':0,'native_pool_bytes':4,'native_pool_alignment_padding':12,'native_pool_sha256':hashlib.sha256(data[:4]).hexdigest()}
result=audit(obj,linked)
# Alias via ordinary linker script: this must not silently convert compiler provenance.
script=a.probes/'literal_alias.ld';script.write_text((a.probes/'01_literal.ld').read_text()+f'{named} = ADDR(.rodata);\n')
alias=a.probes/'literal_alias.elf';env=os.environ.copy();env['LD_LIBRARY_PATH']=str(a.lib.resolve())+':'+env.get('LD_LIBRARY_PATH','')
subprocess.run([str(a.binutils.resolve()/'mips-linux-gnu-ld'),'-T',str(script.resolve()),'--emit-relocs','-o',str(alias.resolve()),str((a.probes/'01_literal.o').resolve())],env=env,check=True)
alias_raw=alias.read_bytes();assert audit(obj,alias_raw)==result;assert Elf32(alias_raw).globals()[named]==pool
result['ordinary_linker_alias_preserves_name_but_not_relocation_provenance']=True
# All mutations are in-memory test fixtures; native files remain untouched.
e=Elf32(obj);f=e.function(name);l=Elf32(linked);ls=l.names.index('.rodata');s=e.names.index('.rodata')
def changed(raw,offset):
    b=bytearray(raw);b[offset]^=1;return bytes(b)
# Change literal, native LO16 addend, linked instruction, and linked pool address.
section_header=struct.unpack_from('>I',linked,32)[0]+ls*40
cases=[('wrong_pool_word',changed(obj,e.sections[s][4]),linked),('wrong_native_addend',changed(obj,e.sections[f.section][4]+11),linked),('wrong_linked_instruction',obj,changed(linked,l.sections[l.function(name).section][4]+11)),('wrong_pool_address',obj,changed(linked,section_header+15))]
for label,b,c in cases:
    try:audit(b,c)
    except ValueError:pass
    else:raise AssertionError(label+' was accepted')
result['negative_controls_rejected']=[x[0] for x in cases];result['canonical_promotion']='NOT_RUN';print(json.dumps(result,indent=2))
