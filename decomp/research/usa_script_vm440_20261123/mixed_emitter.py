#!/usr/bin/env python3
"""Stage only E234 after a fresh USA2165 canonical scratch build or independently replayed USA2316 predecessor.
The canonical verifier and counts are NOT changed. This is research evidence.
"""
import argparse, hashlib, json, os, shutil, struct, subprocess, sys
from collections import Counter
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--work',type=Path,required=True,help='Completed fresh 2165 verifier workdir (mutates candidate only)');p.add_argument('--predecessor-report',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);p.add_argument('--uv',type=Path,required=True);p.add_argument('--jobs',type=int,default=5);p.add_argument('--native151-proof',type=Path);a=p.parse_args()
a.repo=a.repo.resolve();a.work=a.work.resolve();a.out=a.out.resolve();a.out.mkdir(exist_ok=False,parents=True)
sys.path.insert(0,str(a.repo));from decomp.probe import Elf32
from decomp.elf_layout import pack_object_file
from decomp import usa_script_vm436_promotion as vm436,usa_short72_promotion as short72
from decomp.overlay_crossregion47 import _funcs
from decomp.glitch_g2_promotion import all_semantic_relocations
from decomp.usa_opening_new2_promotion import stable_globals,elf_sections
sha=lambda b:hashlib.sha256(b).hexdigest()
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494';RELOC_SHA='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97'
NAME='func_8003E234_3EE34';COORD='D_801C78DC_1C84DC';VMA=0x8003E234;OFFSET=0x3EE34;SIZE=440
report=json.loads(a.predecessor_report.read_text());cmp=report['comparison']
assert report['status']=='matched' and cmp['full_rom_match'] and cmp['matched_functions']==cmp['claimed_functions']==2165 and cmp['matched_function_bytes']==100040
base_c=2165; base_claims={f['name'] for f in cmp['functions']}
if a.native151_proof:
    from decomp import native251_promotion as native151
    from decomp.verify import load_manifest,claimed_functions
    proof=json.loads(a.native151_proof.read_text());assert proof['status']=='PASSED_G2_LOCAL' and proof['accepted_c_after']==2316 and proof['full_rom_match'] and proof['semantic_relocations_exact']==82103 and proof['stable_global_symbols_exact']==26714
    claims=claimed_functions(load_manifest(a.repo/'decomp/manifest.json'));assert len(claims)==2316 and sum(f['size'] for f in claims)==109848
    assert base_claims <= {f['name'] for f in claims};base_claims={f['name'] for f in claims};base_c=2316
baseline=a.work/'baseline';candidate=a.work/'candidate';build=candidate/'build/usa';rom=(baseline/'config/usa/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA and (baseline/'build/usa/mnsg.z64').read_bytes()==(build/'mnsg.z64').read_bytes()==rom
assert sha((candidate/'tools/ido-5.3/cc').read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
ledger=a.repo/'decomp/COMPILER_QUIRKS.md';ledger.read_text()
prior=a.out/'prior.elf';shutil.copyfile(build/'mnsg.elf',prior)
assert sum(_funcs(prior).values())==7376
if a.native151_proof:assert sha(prior.read_bytes())==proof['candidate_elf_sha256']
r0,n0,h0=all_semantic_relocations(prior);g0=stable_globals(prior);assert n0==82103 and h0==RELOC_SHA and sum(g0.values())==26714
assert NAME not in base_claims and NAME in report['retained_assembly_functions']
vm=candidate/'src/script_vm.c';s=vm.read_text();assert sha(s.encode())==vm436.MERGED_VM_SOURCE_SHA256 and s==vm436.proposed_source()
src=Path(__file__).parent/'sources'/f'{NAME}.c';assert sha(src.read_bytes())=='837f4f51db537cf1ff5ca59c43b95f2e66519328fbc87f58a545c4eccb7f112d'
header=('typedef struct { u32 w0, w1; } VmGfx;\n' 'typedef struct { u8 pad[0x5C]; u8 field5C, field5D; } VmState;\n' 'extern u8 D_80076148_76D48;\n' 'extern u8 D_800777F0_783F0;\n' 'extern VmGfx *D_8015C5CC_15D1CC;\n\n')
assert s.count(header)==1;s=s.replace(header,'');fn=src.read_text();fn=fn[fn.index(f'void {NAME}('):];fn=fn.replace('Gfx *','VmGfx *').replace('&D_80077150_77D50','D_80077150_77D50').replace('D_801C78D8_1C84D8','D_801C78D8_1C84D8.x').replace('D_80077860_78460->field5D','((VmState *) D_80077860_78460)->field5D')
anchor=f'#ifndef GOEMON_DECOMP_HOST_TEST\n#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/{NAME}.s")\n#endif';assert s.count(anchor)==1
s=s.replace(anchor,'#ifndef GOEMON_DECOMP_HOST_TEST\n'+header+f'extern s32 {COORD};\n\n'+fn+'#endif');assert sha(s.encode())=='c2374e3458499705603152eb3b03270e7997cfc6ab1947b09b922233b614a541'
obj=build/'src/script_vm.c.o';oldraw=obj.with_name(obj.name+'.before-layout');assert oldraw.is_file() and obj.is_file();oldraw.rename(a.out/'prior-unpacked.o');shutil.copyfile(obj,a.out/'prior-packed.o');obj.unlink();vm.write_text(s,encoding='utf-8',newline='\n')
env=os.environ.copy();env['PATH']=str(a.binutils.resolve())+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(a.lib.resolve())+':'+env.get('LD_LIBRARY_PATH','')
def make(target,log):
    if a.native151_proof:
        os.environ.update(env);native151.runmake(candidate,'usa',(candidate/'.splat/usa/mnsg.ld').read_text(),[target],a.out/log,str(a.uv.resolve()),a.jobs)
    else:
        with (a.out/log).open('w') as f:subprocess.run(['make','-j'+str(a.jobs),'UV='+str(a.uv.resolve()),'VERSION=usa',target],cwd=candidate,env=env,check=True,stdout=f,stderr=subprocess.STDOUT)
make('build/usa/src/script_vm.c.o','compile.log')
old=Elf32((a.out/'prior-unpacked.o').read_bytes());raw=obj.read_bytes();new=Elf32(raw)
def unit_relocs(e,section):
    return Counter((r.offset,r.relocation_type,r.symbol.name or e.names[r.symbol.section],r.symbol.value,r.addend) for r in e.relocations(e.names.index(section)))
for section,extent,count in (('.text',10112,740),('.rodata',64,15)):
    i=old.names.index(section);j=new.names.index(section);assert len(old.payload(i))==extent and old.payload(i)==new.payload(j)
    x,y=unit_relocs(old,section),unit_relocs(new,section);assert x==y and sum(x.values())==count
f=new.function(NAME);assert f.value==VMA-0x8003CFA0 and f.size==SIZE and old.code(old.function(NAME))==new.code(f)
assert not any(x.name==NAME+'.NON_MATCHING' for x in new.symbols)
# Restore only the original undefined coordinate symbol metadata. Prove original
# object and linked predecessor type/size; do not modify relocation records.
old_sym=[x for x in old.symbols if x.name==COORD];new_sym=[x for x in new.symbols if x.name==COORD]
assert len(old_sym)==len(new_sym)==1 and (old_sym[0].kind,old_sym[0].size,old_sym[0].binding,old_sym[0].section,old_sym[0].value)==(0,0,1,0,0)
assert (new_sym[0].kind,new_sym[0].size,new_sym[0].binding,new_sym[0].section,new_sym[0].value)==(1,4,1,0,0)
assert sum(v for k,v in g0.items() if k[-1]==COORD and k[:2]==('801c78dc','0') and k[2]=='NOTYPE')==1
rs=[(r.offset-f.value,r.relocation_type) for r in new.relocations(f.section) if r.symbol.name==COORD];assert sorted(rs)==[(0x114,5),(0x118,6),(0x144,5),(0x148,6)]
sec=elf_sections(raw);tab=sec['.symtab'];strings=sec['.strtab'];assert tab['entsize']==16 and tab['link']==strings['index']
positions=[]
for i in range(tab['size']//16):
    at=tab['offset']+16*i;no=struct.unpack_from('>I',raw,at)[0];st=strings['offset']+no;name=raw[st:raw.index(0,st)].decode('ascii')
    if name==COORD:positions.append(at)
assert len(positions)==1;at=positions[0];assert struct.unpack_from('>IIBBH',raw,at+4)==(0,4,0x11,0,0)
fixed=bytearray(raw);struct.pack_into('>I',fixed,at+8,0);fixed[at+12]=0x10
assert len(fixed)==len(raw) and {i for i,(x,y) in enumerate(zip(raw,fixed)) if x!=y}=={at+11,at+12}
patched=Elf32(fixed)
for section in ('.text','.rodata','.rel.text','.rel.rodata'):
    assert new.payload(new.names.index(section))==patched.payload(patched.names.index(section))
assert [x for x in patched.symbols if x.name==COORD]==old_sym
obj.write_bytes(fixed);layout=pack_object_file(obj)
for n in ('mnsg.elf','mnsg.z64'):(build/n).unlink()
make('build/usa/mnsg.z64','link.log')
elf=build/'mnsg.elf';short72.restore_original_abs_label_type(elf,prior)
assert (build/'mnsg.z64').read_bytes()==rom
f0,f1=_funcs(prior),_funcs(elf);assert f0==f1 and sum(f1.values())==7376 and (NAME,VMA,SIZE) in f1
r1,n1,h1=all_semantic_relocations(elf);assert r0==r1 and n0==n1==82103 and h0==h1==RELOC_SHA
if a.native151_proof:native151.restore_inline_usa(elf,prior)
assert stable_globals(elf)==g0
assert NAME+'.NON_MATCHING' not in (build/'mnsg.map').read_text()
result=dict(status='FULL_ROM_EXACT_SCRATCH',canonical_promotion='NOT_RUN',base_c=base_c,potential_c=base_c+1,added_bytes=SIZE,function=NAME,rom_offset=hex(OFFSET),vma=hex(VMA),source_sha256=sha(src.read_bytes()),mixed_source_sha256=sha(s.encode()),original_code_sha256=sha(rom[OFFSET:OFFSET+SIZE]),original_rom_sha1=ROM_SHA,complete_rom_bytes_exact=len(rom),original_elf_functions_exact=7376,stable_globals_exact=26714,canonical_named_relocations_exact=n1,relocation_sha256=h1,unit_text_bytes_exact=10112,unit_text_relocations_exact=740,unit_rodata_relocations_exact=15,metadata_only_changed_bytes=2,original_elf_sha256=sha(prior.read_bytes()),candidate_elf_sha256=sha(elf.read_bytes()),layout=layout,compiler_quirk_outcome='EXISTING_QUIRK_REPRODUCED',strict_inventory='NOT_RUN',full_new_claim_ci='NOT_RUN',gameplay='NOT_RUN')
from decomp.inventory import summarize_inventory
read=lambda p:subprocess.check_output(['readelf','-Ws',str(p)],text=True)
summary=summarize_inventory(read(baseline/'build/usa/mnsg.elf'),read(elf),base_claims|{NAME})
assert summary['newly_matching_c']==base_c+1 and summary['remaining_assembly_entries']==7363-base_c-1 and not summary['extra_positive_alias_entries']
result['strict_inventory']='PASS_SCRATCH';result['inventory_summary']=summary
(a.out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
