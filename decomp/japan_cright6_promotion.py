"""Additive Japan C-Right6 native replay; stored evidence is not a native pass.

All original ROMs, upstream ELF files and compiler objects remain private.
Requires a separately rebuilt exact canonical JP2528 predecessor and pristine
Splat reference. No canonical ownership is updated by this executable.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, sys
from . import usa_cright4_promotion as shared
from . import native251_promotion as native
from . import native251_integrity
from . import japan_cright_promotion as cright
from . import overlay_crossregion47 as cross
from . import glitch_g2_promotion as glitch
from . import usa_opening_new2_promotion as opening
from . import inventory as strict_inventory

ROOT=Path(__file__).resolve().parent
BATCH=ROOT/'research/cright_promotion_checkpoint_20261124'
REGION='japan_0'
BASE='02e042d969c382217f4561fffd9cc719523de970'
FORMAT='goemon-jp-cright6-post2528-v1'
KEY='cright6_promotion'
MANIFEST=BATCH/'japan_manifest.json'
MANIFEST_SHA='eb75b75e6d19fe0667350b9cacd1e466e4b7a9e7160e4afb2e385f8fd82fd5bf'
PREDECESSOR_ELF='08423cd434cbd132e4f5827eb9fedc2e9cf21c5f903577876e509ef0166d094c'
RESEARCH_ELF='bac3a17e39eb80c54ab1dfc1a523d060455ab1f91ce0e6e871f242bb77b7b776'
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
RETAIL_SHA='9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
RELOC_SHA='43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0'
COMPILER_SHA=shared.COMPILER_SHA
OLD_INVENTORY=ROOT/'results/japan_0_2528_native100_inventory_20261123.json'


def require(value, message):
    if not value: raise ValueError('JP6: '+message)


def sha(data): return hashlib.sha256(data).hexdigest()


def write(path,data): Path(path).write_text(json.dumps(data,indent=2)+'\n')


def previous_names():
    require(sha(OLD_INVENTORY.read_bytes())=='f4c06596b1dffdd1337b5c9d9d9e29bb00c5a0e27f7c2dadb77d2a7b527f333c','frozen JP2528 inventory drift')
    require(native251_integrity.validate()['status']=='PASS','predecessor integrity')
    old=json.loads(OLD_INVENTORY.read_text())
    names=old['previous_C_names']+old['new_C_names']
    require(len(names)==2528 and len(set(names))==2528,'predecessor ownership drift')
    return set(names)


def rows(rom=None):
    require(sha(MANIFEST.read_bytes())==MANIFEST_SHA,'source manifest drift')
    m=json.loads(MANIFEST.read_text());fs=m['functions']; prior=previous_names()
    require(m['base_commit']==BASE and m['status']=='PROSPECTIVE_NOT_ACCEPTED' and m['predecessor_elf_sha256']==PREDECESSOR_ELF and m['expected_candidate_elf_sha256']==RESEARCH_ELF,'wrong original regional base')
    require(len(fs)==6 and sum(f['original_bytes'] for f in fs)==624 and sum(f['original_relocations'] for f in fs)==24,'wrong source extent/count')
    ranges=[];names=set()
    if rom is not None: require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA,'wrong original ROM')
    for f in fs:
        name=f['name'];off=f['rom_offset'];size=f['original_bytes'];vma=f['vma'];src=BATCH/f['source']
        match=re.fullmatch(r'func_([0-9A-F]+)_([0-9A-F]+)',name)
        require(match and (int(match[1],16),int(match[2],16))==(vma,off) and f['region']==REGION and size==4*f['original_words'] and off%4==0 and size>0,'original function address/extent drift '+name)
        require(name not in prior and name not in names and f['status']=='PASSED_ISOLATED_NATIVE','duplicate accepted function '+name)
        require(f['source']==f'japan_0/{name}.c' and sha(src.read_bytes())==f['source_sha256'],'source drift '+name)
        if rom is not None: require(sha(rom[off:off+size])==f['code_sha256'],'original function hash drift '+name)
        names.add(name);ranges.append((off,off+size))
    ranges.sort();require(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'overlapping original ranges')
    return fs


def linked_proof(candidate, pristine, work, uv='uv', jobs=4):
    co,base,work=map(Path,(candidate,pristine,work));work.mkdir(parents=True,exist_ok=False)
    bd=co/'build/japan_0';new=bd/'mnsg.elf';prior=work/'accepted2528.elf'
    rom=shared.original(co,REGION);fs=rows(rom);names0=previous_names();targets={f['name'] for f in fs}
    require(sha(new.read_bytes())==PREDECESSOR_ELF and (bd/'mnsg.z64').read_bytes()==rom,'canonical predecessor not exact')
    require(shared.original(base,REGION)==rom,'pristine ROM mismatch')
    require(sha((co/'tools/ido-5.3/cc').read_bytes())==COMPILER_SHA,'native compiler mismatch')
    require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','pinned upstream mismatch')
    shutil.copyfile(new,prior)
    require(cright.c_identities(prior)==names0,'exact canonical predecessor C-name set mismatch')
    d=shared.stage(co,REGION,candidates=fs)
    require(len(d['functions'])==6 and not d['blocked'],'active original ASM ownership mismatch')
    compile_result=shared.compile_pack(co,REGION,d,base,uv,jobs)
    require(compile_result['positive_full_flags']==6 and not compile_result['failures'],'native full-flags compile failed')
    g0=opening.stable_globals(prior)
    fix=native.restore_undefined_type(bd/'src/cright10/func_802124AC_5CDA3C.c.o','D_3B03C',0,g0)
    new.unlink();(bd/'mnsg.z64').unlink()
    shared.runmake(co,REGION,(co/'.splat/japan_0/mnsg.ld').read_text(),['build/japan_0/mnsg.z64'],bd/'cright10-metadata-relink.log',uv,jobs)
    require((bd/'mnsg.z64').read_bytes()==rom,'full expanded ROM differs')
    funcs=cross._funcs(prior);require(funcs==cross._funcs(new) and sum(funcs.values())==7376,'positive FUNC identity mismatch')
    rel0=glitch.all_semantic_relocations(prior);rel1=glitch.all_semantic_relocations(new)
    require(rel0==rel1 and rel1[1:]==(80745,RELOC_SHA),'semantic relocation multiset mismatch')
    require(g0==opening.stable_globals(new) and sum(g0.values())==26393,'stable global identity mismatch')
    names=cright.c_identities(new);require(names==names0|targets and len(names)==2534,'strict C inventory mismatch')
    inventory_summary=strict_inventory.summarize_inventory(
        subprocess.check_output(['readelf','-Ws',str(prior)],text=True),
        subprocess.check_output(['readelf','-Ws',str(new)],text=True), targets)
    require((inventory_summary['identified_function_entries'],inventory_summary['upstream_unmarked_entries'],inventory_summary['newly_matching_c'],inventory_summary['current_unmarked_entries'],inventory_summary['remaining_assembly_entries'])==(7376,2528,6,2534,4842) and not inventory_summary['size_annotation_differences'],'strict readelf inventory mismatch')
    linkmap=(bd/'mnsg.map').read_text()
    for f in d['functions']:
        require(f['name']+'.NON_MATCHING' not in linkmap and f'build/japan_0/{f["staged_path"]}.o' in linkmap,'C linker ownership mismatch '+f['name'])
    require(sha(new.read_bytes())==RESEARCH_ELF,'candidate ELF differs from independent exact integrated research')
    retail=work/'retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=co,check=True,stdout=subprocess.DEVNULL)
    rb=(base/'config/japan_0/baserom.z64').read_bytes();require(len(rb)==16777216 and hashlib.sha1(rb).hexdigest()==RETAIL_SHA and retail.read_bytes()==rb,'full retail ROM differs')
    proof={'status':'PASSED_G2_LOCAL','region':REGION,'base_commit':BASE,'before_C':len(names0),'after_C':len(names),'added_C':len(targets),'added_bytes':sum(f['original_bytes'] for f in fs),'original_bytes_after':138028,'asm_remaining':7376-len(names),'rom_bytes':len(rom),'rom_sha1':ROM_SHA,'retail_bytes':len(rb),'retail_sha1':RETAIL_SHA,'retail_ROM_exact':True,'full_ROM_exact':True,'elf_identities_exact':sum(funcs.values()),'semantic_relocations_exact':rel1[1],'semantic_relocations_sha256':rel1[2],'stable_global_symbol_identities_exact':sum(g0.values()),'source_manifest_sha256':MANIFEST_SHA,'predecessor_elf_sha256':sha(prior.read_bytes()),'candidate_elf_sha256':sha(new.read_bytes()),'abs_metadata_fix':fix,'ownership_exact':True,'new_C_names':sorted(targets),'native_compile_records':compile_result['records'],'compiler_sha256':COMPILER_SHA,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'}
    inventory={'format':FORMAT,'region':REGION,'base_c':2528,'matching_c_after':len(names),'remaining_assembly':7376-len(names),'accepted_original_C_bytes':138028,'original_positive_elf_count':7376,'original_semantic_relocations':80745,'candidate_semantic_relocations':rel1[1],'same_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':proof['predecessor_elf_sha256'],'candidate_elf_sha256':proof['candidate_elf_sha256'],'previous_C_names':sorted(names0),'new_C_names':sorted(targets),'strict_readelf_summary':inventory_summary,'new_C_functions':[{ 'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':(BATCH/f['source']).relative_to(ROOT).as_posix(),'source_sha256':f['source_sha256'],'original_code_sha256':f['code_sha256']} for f in fs]}
    write(work/'g2.json',proof);write(work/'inventory.json',inventory);return proof


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',default='uv');p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
    if not __debug__:p.error('Assertions are mandatory')
    print(json.dumps(linked_proof(a.checkout,a.pristine,a.work,a.uv,a.jobs),indent=2))

if __name__=='__main__':main()
