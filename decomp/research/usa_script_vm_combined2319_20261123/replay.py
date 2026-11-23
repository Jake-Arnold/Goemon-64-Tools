#!/usr/bin/env python3
"""Research-only whole-ROM replay of F37C and DF98 on exact E234 predecessor."""
import argparse,hashlib,json,shutil,struct,sys
from pathlib import Path

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--predecessor',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=8);a=p.parse_args();repo=a.repo.resolve();base=a.predecessor.resolve();out=a.out.resolve();out.mkdir(exist_ok=False,parents=True)
    sys.path.insert(0,str(repo));from decomp.probe import Elf32
    from decomp.native251_promotion import runmake,restore_inline_usa
    from decomp.usa_short72_promotion import restore_original_abs_label_type
    from decomp.usa_opening_new2_promotion import elf_sections,stable_globals
    from decomp.usa_script_vm440_promotion import MERGED_SHA
    from decomp.overlay_crossregion47 import _funcs
    from decomp.glitch_g2_promotion import all_semantic_relocations
    sha=lambda b:hashlib.sha256(b).hexdigest()
    prior=base/'build/usa/mnsg.elf';rom=(base/'config/usa/baserom.decompressed.z64').read_bytes()
    require(sha(prior.read_bytes())=='f03cb69cf367c2627d6e5e3e0838e2753b7bd13f67da3796f7d619d323043cad','wrong E234 predecessor ELF')
    require(hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494' and (base/'build/usa/mnsg.z64').read_bytes()==rom,'wrong original ROM')
    require(sha((base/'tools/ido-5.3/cc').read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0','wrong IDO')
    co=out/'candidate';shutil.copytree(base,co,symlinks=True);build=co/'build/usa';source=co/'src/script_vm.c';s=source.read_text();require(sha(s.encode())==MERGED_SHA,'wrong VM predecessor source')
    research=repo/'decomp/research';d=(research/'usa_script_vm_df98_reference_20261123/df98.c').read_text();f=(research/'usa_script_vm_f37c_reference_20261123/f37c.c').read_text()
    require(sha(d.encode())=='8eaf68308afa51862d07ee5795db6cbfd09250070bd243ad69744f6aa144a1f9' and sha(f.encode())=='4cca0e20ec00d4b2e3b45b3acfe3d3c05fb74aa06c87f85e6da3026bdbee6cdb','source drift')
    d=d.split('\n',1)[1];f=f.split('\n',1)[1].replace('extern u8 D_8015CC30_15D830[];\n','').replace('extern void *D_801C7750_1C8350;\n','').replace('D_8015CC30_15D830+','((u8 *)&D_8015CC30_15D830)+').replace('D_8015CC30_15D830[','((u8 *)&D_8015CC30_15D830)[').replace('D_801C7750_1C8350=ptr;','D_801C7750_1C8350=(u32)ptr;')
    for name,fn in [('func_8003DF98_3EB98',d),('func_8003F37C_3FF7C',f)]:
        anchor=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/{name}.s")';require(s.count(anchor)==1,'wrong ASM owner');s=s.replace(anchor,fn)
    source.write_text(s);obj=build/'src/script_vm.c.o';obj.unlink();ledger=repo/'decomp/COMPILER_QUIRKS.md';ledger.read_text()
    ld=(co/'.splat/usa/mnsg.ld').read_text();runmake(co,'usa',ld,['build/usa/src/script_vm.c.o'],out/'compile.log',a.uv,a.jobs)
    raw=obj.read_bytes();e=Elf32(raw);old=Elf32((base/'build/usa/src/script_vm.c.o.before-layout').read_bytes());r=e.names.index('.rodata');t=e.names.index('.text');data=e.payload(r)
    require(len(e.payload(t))==10112 and [i for i in range(0,10112,4) if e.payload(t)[i:i+4]!=old.payload(old.names.index('.text'))[i:i+4]]==[0x1014,0x1024,0x23e4],'unexpected unlinked text change')
    require(len(data)==224 and e.sections[r][8]==16,'unexpected pool layout')
    require([(x.offset,x.relocation_type,x.symbol.section,x.symbol.kind,x.symbol.value) for x in e.relocations(r)]==[(i*4,2,t,3,0) for i in range(55)],'pool relocation mismatch')
    require(b''.join(struct.pack('>I',0x8003cfa0+struct.unpack_from('>I',data,i*4)[0]) for i in range(55))+data[220:]==rom[0x7dc2c:0x7dd0c],'pool linked data not original')
    sec=elf_sections(raw);tab=sec['.symtab'];strings=sec['.strtab'];name='D_801C78DC_1C84DC';b=bytearray(raw);found=[]
    require([(x.kind,x.size,x.binding,x.section,x.value) for x in old.symbols if x.name==name]==[(0,0,1,0,0)],'wrong predecessor symbol')
    for i in range(tab['size']//16):
        at=tab['offset']+16*i;no=struct.unpack_from('>I',raw,at)[0];st=strings['offset']+no
        if raw[st:raw.index(0,st)].decode('ascii')==name:
            require(struct.unpack_from('>IIBBH',raw,at+4)==(0,4,0x11,0,0),'wrong compiler symbol');found.append(at);struct.pack_into('>I',b,at+8,0);b[at+12]=0x10
    require(len(found)==1,'ambiguous coordinate');sh=struct.unpack_from('>I',raw,32)[0];align=sh+r*40+32;struct.pack_into('>I',b,align,4)
    require({i for i,(x,y) in enumerate(zip(raw,b)) if x!=y}=={found[0]+11,found[0]+12,align+3},'unexpected object edit');fixed=Elf32(b)
    for section in ('.text','.rodata','.rel.text','.rel.rodata'):
        require(e.payload(e.names.index(section))==fixed.payload(fixed.names.index(section)),'native payload or relocation record changed')
    obj.write_bytes(b);dataowner=co/'asm/usa/data/main_continued_after_vm_store.rodata.s';text=dataowner.read_text();require(text.count('dlabel jtbl_8007D068_7DC68\n')==2 and text.count('enddlabel D_8007D108_7DD08')==1,'wrong original ASM data owner')
    dataowner.write_text('''.section .rodata, "a"
.globl jtbl_8007D068_7DC68
.type jtbl_8007D068_7DC68, @object
.set jtbl_8007D068_7DC68, . - 164
.size jtbl_8007D068_7DC68, 160
.globl D_8007D108_7DD08
.type D_8007D108_7DD08, @object
.set D_8007D108_7DD08, . - 4
.size D_8007D108_7DD08, 8
.word 0
''')
    for path in ('mnsg.elf','mnsg.z64','asm/usa/data/main_continued_after_vm_store.rodata.s.o'):(build/path).unlink()
    runmake(co,'usa',ld,['build/usa/mnsg.z64'],out/'link.log',a.uv,a.jobs)
    new=build/'mnsg.elf';restore_original_abs_label_type(new,prior);restore_inline_usa(new,prior)
    f0,f1=_funcs(prior),_funcs(new);g0,g1=stable_globals(prior),stable_globals(new);r0,n0,h0=all_semantic_relocations(prior);r1,n1,h1=all_semantic_relocations(new)
    require((build/'mnsg.z64').read_bytes()==rom and f0==f1 and g0==g1,'complete ROM or ELF identity differs')
    require((n0,n1)==(82103,82102) and sum((r0-r1).values())==45 and sum((r1-r0).values())==44,'unexpected full relocation delta')
    result={'status':'RESEARCH_ONLY','base_c':2317,'additional_candidates':2,'rom_exact':True,'functions_exact':True,'function_count':sum(f1.values()),'global_count':sum(g1.values()),'globals_removed':list((g0-g1).items()),'globals_added':list((g1-g0).items()),'relocation_before':n0,'relocation_after':n1,'relocation_removed':list((r0-r1).items()),'relocation_added':list((r1-r0).items()),'candidate_elf_sha256':sha(new.read_bytes()),'strict_named_relocation_gate':'FAIL','canonical_promotion':'NOT_RUN','compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED','mixed_source_sha256':sha(s.encode()),'ledger_sha256':sha(ledger.read_bytes())}
    (out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print('RESEARCH_ONLY: full original ROM, ELF identities and exact expected relocation delta reproduced')

if __name__=='__main__':main()
