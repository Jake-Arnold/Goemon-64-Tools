"""Original-USA E234 post-2316 stage. All predecessor gates are preserved."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib, shutil, struct
from . import usa_script_vm436_promotion as vm436
from . import native251_promotion as native151
from . import usa_short72_promotion as short72
from .probe import Elf32
from .elf_layout import pack_object_file
from .overlay_crossregion47 import _funcs
from .glitch_g2_promotion import all_semantic_relocations
from .usa_opening_new2_promotion import stable_globals,elf_sections

FORMAT='goemon-usa-script-vm440-post2316-v1'
KEY='usa_script_vm440_promotion'
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
RELOC_SHA='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97'
NAME='func_8003E234_3EE34';COORD='D_801C78DC_1C84DC';VMA=0x8003E234;OFFSET=0x3EE34;SIZE=440
SOURCE_SHA='837f4f51db537cf1ff5ca59c43b95f2e66519328fbc87f58a545c4eccb7f112d'
MERGED_SHA='c2374e3458499705603152eb3b03270e7997cfc6ab1947b09b922233b614a541'
CODE_SHA='acd6d1ecf74790033a8438ba6aae9c7652497de18d5ad7c205deaf2650268336'
SOURCE=Path(__file__).parent/'research/usa_script_vm440_20261123/sources'/f'{NAME}.c'
sha=lambda b:hashlib.sha256(b).hexdigest()

def validate_predecessor(manifest,rom=None):
    from .verify import claimed_functions
    if manifest.get(KEY)!={'format':FORMAT}:raise ValueError('Unreviewed VM440 stage')
    if manifest['decompressed_sha1']!=ROM_SHA or manifest['upstream_commit']!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':raise ValueError('VM440 provenance changed')
    prior=claimed_functions({k:v for k,v in manifest.items() if k!=KEY})
    if (len(prior),sum(f['size'] for f in prior))!=(2316,109848):raise ValueError('VM440 predecessor count changed')
    if any(f['name']==NAME or f['rom_offset']<OFFSET+SIZE and OFFSET<f['rom_offset']+f['size'] for f in prior):raise ValueError('VM440 duplicate owner')
    units=[u for u in manifest['units'] if u['source']=='script_vm.c']
    if len(units)!=1 or units[0]['assembly_functions'].count(NAME)!=1:raise ValueError('VM440 original ASM owner absent')
    if rom is not None and (len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA or sha(rom[OFFSET:OFFSET+SIZE])!=CODE_SHA):raise ValueError('VM440 original ROM mismatch')
    proposed_source()
    return prior

def proposed_source():
    s=vm436.proposed_source()
    src=SOURCE
    if sha(src.read_bytes())!=SOURCE_SHA:raise ValueError('VM440 C source drift')
    header=('typedef struct { u32 w0, w1; } VmGfx;\n' 'typedef struct { u8 pad[0x5C]; u8 field5C, field5D; } VmState;\n' 'extern u8 D_80076148_76D48;\n' 'extern u8 D_800777F0_783F0;\n' 'extern VmGfx *D_8015C5CC_15D1CC;\n\n')
    if not (s.count(header)==1):raise ValueError("VM440 native proof guard at source line 44")
    s=s.replace(header,'');fn=src.read_text();fn=fn[fn.index(f'void {NAME}('):];fn=fn.replace('Gfx *','VmGfx *').replace('&D_80077150_77D50','D_80077150_77D50').replace('D_801C78D8_1C84D8','D_801C78D8_1C84D8.x').replace('D_80077860_78460->field5D','((VmState *) D_80077860_78460)->field5D')
    anchor=f'#ifndef GOEMON_DECOMP_HOST_TEST\n#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/{NAME}.s")\n#endif'
    if not (s.count(anchor)==1):raise ValueError("VM440 native proof guard at source line 45")
    s=s.replace(anchor,'#ifndef GOEMON_DECOMP_HOST_TEST\n'+header+f'extern s32 {COORD};\n\n'+fn+'#endif')
    if not (sha(s.encode())==MERGED_SHA):raise ValueError("VM440 native proof guard at source line 46")
    return s

def restore_coordinate(raw,old_raw,g0):
    old=Elf32(old_raw);new=Elf32(raw)
    def unit_relocs(e,section):
        return Counter((r.offset,r.relocation_type,r.symbol.name or e.names[r.symbol.section],r.symbol.value,r.addend) for r in e.relocations(e.names.index(section)))
    for section,extent,count in (('.text',10112,740),('.rodata',64,15)):
        i=old.names.index(section);j=new.names.index(section)
        if not (len(old.payload(i))==extent and old.payload(i)==new.payload(j)):raise ValueError("VM440 native proof guard at source line 54")
        x,y=unit_relocs(old,section),unit_relocs(new,section)
        if not (x==y and sum(x.values())==count):raise ValueError("VM440 native proof guard at source line 55")
    f=new.function(NAME)
    if not (f.value==VMA-0x8003CFA0 and f.size==SIZE and old.code(old.function(NAME))==new.code(f)):raise ValueError("VM440 native proof guard at source line 56")
    if not (not any(x.name==NAME+'.NON_MATCHING' for x in new.symbols)):raise ValueError("VM440 native proof guard at source line 57")
    # Restore only the original undefined coordinate symbol metadata. Prove original
    # object and linked predecessor type/size; do not modify relocation records.
    old_sym=[x for x in old.symbols if x.name==COORD];new_sym=[x for x in new.symbols if x.name==COORD]
    if not (len(old_sym)==len(new_sym)==1 and (old_sym[0].kind,old_sym[0].size,old_sym[0].binding,old_sym[0].section,old_sym[0].value)==(0,0,1,0,0)):raise ValueError("VM440 native proof guard at source line 61")
    if not ((new_sym[0].kind,new_sym[0].size,new_sym[0].binding,new_sym[0].section,new_sym[0].value)==(1,4,1,0,0)):raise ValueError("VM440 native proof guard at source line 62")
    if not (sum(v for k,v in g0.items() if k[-1]==COORD and k[:2]==('801c78dc','0') and k[2]=='NOTYPE')==1):raise ValueError("VM440 native proof guard at source line 63")
    rs=[(r.offset-f.value,r.relocation_type) for r in new.relocations(f.section) if r.symbol.name==COORD]
    if not (sorted(rs)==[(0x114,5),(0x118,6),(0x144,5),(0x148,6)]):raise ValueError("VM440 native proof guard at source line 64")
    sec=elf_sections(raw);tab=sec['.symtab'];strings=sec['.strtab']
    if not (tab['entsize']==16 and tab['link']==strings['index']):raise ValueError("VM440 native proof guard at source line 65")
    positions=[]
    for i in range(tab['size']//16):
        at=tab['offset']+16*i;no=struct.unpack_from('>I',raw,at)[0];st=strings['offset']+no;name=raw[st:raw.index(0,st)].decode('ascii')
        if name==COORD:positions.append(at)
    if not (len(positions)==1):raise ValueError("VM440 native proof guard at source line 70")
    at=positions[0]
    if not (struct.unpack_from('>IIBBH',raw,at+4)==(0,4,0x11,0,0)):raise ValueError("VM440 native proof guard at source line 70")
    fixed=bytearray(raw);struct.pack_into('>I',fixed,at+8,0);fixed[at+12]=0x10
    if not (len(fixed)==len(raw) and {i for i,(x,y) in enumerate(zip(raw,fixed)) if x!=y}=={at+11,at+12}):raise ValueError("VM440 native proof guard at source line 72")
    patched=Elf32(fixed)
    for section in ('.text','.rodata','.rel.text','.rel.rodata'):
        if not (new.payload(new.names.index(section))==patched.payload(patched.names.index(section))):raise ValueError("VM440 native proof guard at source line 75")
    if not ([x for x in patched.symbols if x.name==COORD]==old_sym):raise ValueError("VM440 native proof guard at source line 76")
    return bytes(fixed)

def apply_usa(candidate,baseline,work,uv,jobs):
    candidate=Path(candidate);baseline=Path(baseline);work=Path(work);build=candidate/'build/usa'
    rom=(baseline/'config/usa/baserom.decompressed.z64').read_bytes()
    if not (len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA and sha(rom[OFFSET:OFFSET+SIZE])==CODE_SHA and (baseline/'build/usa/mnsg.z64').read_bytes()==(build/'mnsg.z64').read_bytes()==rom):raise ValueError('VM440 original ROM mismatch')
    if sha((candidate/'tools/ido-5.3/cc').read_bytes())!='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0':raise ValueError('VM440 IDO changed')
    ledger=Path(__file__).parent/'COMPILER_QUIRKS.md';ledger.read_text()
    prior=work/'accepted2316-before-vm440.elf';shutil.copyfile(build/'mnsg.elf',prior)
    r0,n0,h0=all_semantic_relocations(prior);g0=stable_globals(prior)
    if not(n0==82103 and h0==RELOC_SHA and sum(g0.values())==26714 and sum(_funcs(prior).values())==7376):raise ValueError('VM440 predecessor ELF changed')
    vm=candidate/'src/script_vm.c'
    if vm.read_text()!=vm436.proposed_source():raise ValueError('VM440 predecessor mixed source changed')
    s=proposed_source()
    obj=build/'src/script_vm.c.o';oldraw=obj.with_name(obj.name+'.before-layout')
    if not(oldraw.is_file() and obj.is_file()):raise ValueError('VM440 prior object missing')
    backup=work/'vm440-prior-unpacked.o';oldraw.rename(backup);obj.unlink();vm.write_text(s,encoding='utf-8',newline='\n')
    def make(target,log):native151.runmake(candidate,'usa',(candidate/'.splat/usa/mnsg.ld').read_text(),[target],work/log,uv,jobs)
    make('build/usa/src/script_vm.c.o','vm440-compile.log')
    fixed=restore_coordinate(obj.read_bytes(),backup.read_bytes(),g0)
    obj.write_bytes(fixed);layout=pack_object_file(obj)
    for n in ('mnsg.elf','mnsg.z64'):(build/n).unlink()
    make('build/usa/mnsg.z64','vm440-link.log')
    elf=build/'mnsg.elf';short72.restore_original_abs_label_type(elf,prior)
    if not ((build/'mnsg.z64').read_bytes()==rom):raise ValueError("VM440 native proof guard at source line 101")
    f0,f1=_funcs(prior),_funcs(elf)
    if not (f0==f1 and sum(f1.values())==7376 and (NAME,VMA,SIZE) in f1):raise ValueError("VM440 native proof guard at source line 102")
    r1,n1,h1=all_semantic_relocations(elf)
    if not (r0==r1 and n0==n1==82103 and h0==h1==RELOC_SHA):raise ValueError("VM440 native proof guard at source line 103")
    native151.restore_inline_usa(elf,prior)
    if not (stable_globals(elf)==g0):raise ValueError("VM440 native proof guard at source line 105")
    if not (NAME+'.NON_MATCHING' not in (build/'mnsg.map').read_text()):raise ValueError("VM440 native proof guard at source line 106")
    return dict(status='PASSED_G2_LOCAL',base_c=2316,accepted_c_after=2317,added_c=1,added_original_bytes=SIZE,accepted_original_bytes_after=110288,remaining_assembly=5046,full_rom_match=True,original_rom_sha1=ROM_SHA,original_32MiB_ROM_bytes_exact=len(rom),positive_elf_function_identities_exact=7376,semantic_relocations_exact=n1,semantic_relocation_sha256=h1,stable_global_symbols_exact=26714,source_sha256=SOURCE_SHA,mixed_source_sha256=MERGED_SHA,original_code_sha256=CODE_SHA,original_elf_sha256=sha((baseline/'build/usa/mnsg.elf').read_bytes()),predecessor_elf_sha256=sha(prior.read_bytes()),candidate_elf_sha256=sha(elf.read_bytes()),unit_text_bytes_exact=10112,unit_text_relocations_exact=740,unit_rodata_relocations_exact=15,metadata_only_changed_bytes=2,layout=layout,ownership_exact=True,compiler_quirk_outcome='EXISTING_QUIRK_REPRODUCED',ledger_sha256=sha(ledger.read_bytes()),gameplay='NOT_RUN')
