#!/usr/bin/env python3
"""Independent full original-ROM shadow and native research replay from exact USA2323.
No canonical manifest or accepted inventory is changed by this executable.
Requires a private, expendable fresh USA2323 candidate checkout.
"""
import argparse, collections, hashlib, json, os, pathlib, shutil, subprocess, re
from decomp import usa_cright4_promotion as prior_stage, usa_short72_promotion as short72, native251_promotion as native251, japan_cright_promotion as cright, glitch_g2_promotion as glitch, overlay_crossregion47 as cross, usa_opening_new2_promotion as opening, inventory
P=pathlib.Path
B=P(__file__).resolve().parent
REGION='usa'; TARGET='func_8000394C_454C'; PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
# Use the repository's pinned retail digest (do not infer from an output).
RETAIL_SHA=prior_stage.RETAIL_SHA
BASE='4efacadb87c1d3f14fc082959e280325ccec5185'
LEDGER_BLOB='10313aba367418d71cd6c332086d2d6a9bf83e39'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=P,required=True);p.add_argument('--work',type=P,required=True);p.add_argument('--uv',required=True);p.add_argument('--ledger',type=P,required=True);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
    c=a.checkout.resolve();w=a.work.resolve();w.mkdir(parents=True,exist_ok=False);bd=c/'build/usa';elf=bd/'mnsg.elf';rom=(c/'config/usa/baserom.decompressed.z64').read_bytes();retail=(c/'config/usa/baserom.z64').read_bytes()
    require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA and (bd/'mnsg.z64').read_bytes()==rom,'wrong predecessor ROM');require(len(retail)==16777216 and hashlib.sha1(retail).hexdigest()==RETAIL_SHA,'wrong retail ROM')
    require(sha(elf.read_bytes())==prior_stage.NEW_ELF,'canonical USA2323 ELF mismatch');require(sha((c/'tools/ido-5.3/cc').read_bytes())==prior_stage.COMPILER_SHA,'wrong IDO');require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=c,text=True).strip()==PIN,'wrong upstream')
    ledger=a.ledger.read_bytes()[:58440];require(hashlib.sha1(b'blob '+str(len(ledger)).encode()+b'\0'+ledger).hexdigest()==LEDGER_BLOB,'compiler ledger drift; review current ledger before each attempt')
    old=w/'prior.elf';shutil.copyfile(elf,old);names0=cright.c_identities(old);require(len(names0)==2336 and TARGET not in names0,'predecessor C ownership drift');g0=opening.stable_globals(old);f0=cross._funcs(old);r0=glitch.all_semantic_relocations(old)
    src=c/'src/transition_state.c';asm=c/'asm/usa/nonmatchings/transition_state'/f'{TARGET}.s';obj=bd/'src/transition_state.c.o';ld=(c/'.splat/usa/mnsg.ld').read_text();src0=src.read_bytes();asm0=asm.read_bytes();obj0=obj.read_bytes()
    require(sha(src0)=='87cfc2d37719940f71e20dd747ac3d098477590d442dcd6f8df6d58cc2611006','wrong mixed owner');require(src0.count(f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/{TARGET}.s")'.encode())==1,'wrong pragma')
    # Splat-generated ABS offset is an integer displacement; audit its actual original definition.
    definitions=(c/'.splat/usa/undefined_syms_auto.ld').read_text();require(re.search(r'(?m)^D_3ADD6\s*=\s*0x0*3ADD6\s*;',definitions,re.I) is not None,'offset provenance not established')
    require(asm0.count(b'%hi(D_3ADD6)')==2 and asm0.count(b'%lo(D_3ADD6)')==2,'unexpected original offset sites')
    asmshadow=asm0.replace(b'%hi(D_3ADD6)',b'4').replace(b'%lo(D_3ADD6)',b'-21034')
    body=(B/'usa/454c.c').read_bytes();header=(B/'usa/transition.h').read_bytes();require(sha(body)=='609a5ba602914b8ad14af2cd7516f6716a6b8461f9152925f22b93e06423ad7f' and sha(header)=='9bbe57788cc6866b4d713e4b5f0f8cb07641d117a4d3e21cc8be4eee3df0cc74','source drift')
    def compile_unit(tag):
        obj.unlink(missing_ok=True);prior_stage.runmake(c,REGION,ld,['build/usa/src/transition_state.c.o'],w/f'{tag}-compile.log',a.uv,a.jobs);shutil.copyfile(obj,w/f'{tag}.o')
    def link(tag):
        elf.unlink();(bd/'mnsg.z64').unlink();prior_stage.runmake(c,REGION,ld,['build/usa/mnsg.z64'],w/f'{tag}-link.log',a.uv,a.jobs);short72.restore_original_abs_label_type(elf,old);native251.restore_inline_usa(elf,old)
        require((bd/'mnsg.z64').read_bytes()==rom,f'{tag} original expanded ROM differs');require(cross._funcs(elf)==f0 and sum(f0.values())==7376,f'{tag} positive FUNC identities differ');require(opening.stable_globals(elf)==g0,f'{tag} stable global identities differ')
        rp=w/f'{tag}-retail.z64';subprocess.run([a.uv,'run','python','tools/rommy.py','compress','--input','build/usa/mnsg.z64','--output',str(rp),'--manifest','config/usa/rommy.yaml','--pad','--verify'],cwd=c,check=True,stdout=subprocess.DEVNULL);require(rp.read_bytes()==retail,f'{tag} original retail ROM differs');rp.unlink();shutil.copyfile(elf,w/f'{tag}.elf');return glitch.all_semantic_relocations(elf)
    # Assemble the original shadow without reference to the candidate object.
    asm.write_bytes(asmshadow);compile_unit('shadow');rshadow=link('shadow');require(cright.c_identities(elf)==names0,'shadow ownership changed');removed=r0[0]-rshadow[0];added=rshadow[0]-r0[0];expected=collections.Counter({('.rel.main',0x80003994,'R_MIPS_HI16',0x3add6,'D_3ADD6'):1,('.rel.main',0x80003998,'R_MIPS_HI16',0x3add6,'D_3ADD6'):1,('.rel.main',0x800039a0,'R_MIPS_LO16',0x3add6,'D_3ADD6'):1,('.rel.main',0x800039ac,'R_MIPS_LO16',0x3add6,'D_3ADD6'):1})
    require(removed==expected and not added,f'unexpected full original-reference relocation delta: {removed}, {added}')
    asm.write_bytes(asm0);(c/'src/transition.h').write_bytes(header);src.write_bytes(src0.replace(f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/transition_state/{TARGET}.s")'.encode(),body.rstrip(),1));compile_unit('native');rnative=link('native');require(rnative==rshadow,'native vs independent shadow entire relocation multiset differs');names=cright.c_identities(elf);require(names==names0|{TARGET},'new C ownership mismatch')
    # Compare untouched whole mixed-unit text and original function bytes, not patched code.
    secs=opening.elf_sections(obj.read_bytes());shsecs=opening.elf_sections((w/'shadow.o').read_bytes());e=secs['.text'];s=shsecs['.text'];bt=obj.read_bytes()[e['offset']:e['offset']+e['size']];bs=(w/'shadow.o').read_bytes()[s['offset']:s['offset']+s['size']];require(bt==bs and len(bt)==2256,'whole mixed unit differs')
    inv=inventory.summarize_inventory(subprocess.check_output(['readelf','-Ws',str(old)],text=True),subprocess.check_output(['readelf','-Ws',str(elf)],text=True),{TARGET});require(inv['identified_function_entries']==7376 and inv['newly_matching_c']==1 and inv['remaining_assembly_entries']==5039,'strict inventory mismatch')
    data={'status':'FULL_ROM_EXACT_RESEARCH_NOT_PROMOTED','base_commit':BASE,'region':REGION,'target':TARGET,'original_bytes':116,'whole_unit_bytes':2256,'prior_elf_sha256':sha(old.read_bytes()),'shadow_elf_sha256':sha((w/'shadow.elf').read_bytes()),'candidate_elf_sha256':sha(elf.read_bytes()),'source_sha256':sha(body),'header_sha256':sha(header),'expanded_rom_bytes':len(rom),'expanded_rom_sha1':ROM_SHA,'retail_rom_bytes':len(retail),'retail_rom_sha1':RETAIL_SHA,'positive_function_identities':sum(f0.values()),'stable_globals':sum(g0.values()),'prior_relocations':r0[1],'native_relocations':rnative[1],'native_relocation_sha256':rnative[2],'independent_shadow_exact':True,'removed_original_abs_offset_relocations':[list(x) for x in sorted(removed)],'new_c_names':[TARGET],'inventory':inv,'full_canonical_CI':'NOT_RUN','compiler_outcome':'EXISTING_QUIRK_REPRODUCED'}; (w/'proof.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
