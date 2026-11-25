"""Additive Japanese native promotion; replay from authenticated 2551-C predecessor.
No stored report substitutes for native verification. Original inputs stay private.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess
from .consolidated_batch_promotion import (sha,read,write,negative,exact,FLAGS,stage,cross,splice,opening,cright,glitch,inventory,jp55,probe)
from . import transition_promotion as transition
ROOT=Path(__file__).resolve().parent
KEY='consolidated13_promotion'
FORMAT='goemon-jp-consolidated13-post2551-v1'
MANIFEST_SHA='4d5def6c15d12f993fa4b0a330dff5e838729e57387b3dde8237ea8828e188ce'
PRIOR_INV_SHA='71bc0b8652c5f57afe694c22189b24e3b3e33f1ad6eb13aa06ec1fecacc4be4a'
PRIOR_MASTER_SHA='71368d84cc861f8aa0fe619d53bb6f205a6c52bf7ae876c83b566d51046c044e'
PRE='0bea1f6e25d5c06be5495d488210f49184e4accdf1052ee014c021a352b2f13a'
NEW='ff221878793c5936b86a0f7d8586fdc062129ae58711959a6f711e33dac3aabe'
ROM='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
RETAIL='9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
PROOF='japan_0_2564_consolidated13_g2_20261124.json'
INV='japan_0_2564_consolidated13_inventory_20261124.json'
REG='japan_0_consolidated13_2564.json'
RELOC='2ede77ef8e9fa7562cedf148aa11710c8a5f37b24b700bcbb9609be3d12d71f9'

def need(ok,msg):
    if not ok:raise ValueError('Japan consolidated13: '+msg)
def prior_names(root=ROOT):
    p=root/'results'/transition.JP_INV;need(sha(p.read_bytes())==PRIOR_INV_SHA,'frozen JP2551 inventory drift');i=read(p);n=i['previous_C_names']+i['new_C_names'];need(len(n)==len(set(n))==2551,'predecessor names');return set(n)
def rows(root=ROOT,rom=None):
    p=root/'research/consolidated42_20261124/japan_manifest.json';need(sha(p.read_bytes())==MANIFEST_SHA,'source manifest drift');fs=read(p)
    need((len(fs),sum(x['original_bytes'] for x in fs),sum(x['relocation_count'] for x in fs))==(13,2136,107),'source count/extent/relocations')
    names=set();spans=[]
    for f in fs:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];need(f['region']=='japan_0' and n==f'func_{f["vma"]:08X}_{a:X}' and z>0 and z%4==a%4==0 and n not in names,'source identity '+n)
        need(f['source']==f'research/consolidated42_20261124/japan_0/{n}.c','source path');s=(root/f['source']).read_bytes();need(sha(s)==f['source_sha256'],'source drift '+n)
        pos=[t for t in f['trials'] if t['status']=='EXACT'];neg=f['trials'][-1];need(len(pos)==1 and pos[0]['source_sha256']==sha(s) and pos[0]['flags']==FLAGS and neg['status']=='FAILED_NATIVE' and neg['flags']==FLAGS and sha(negative(s,n))==neg['source_sha256'],'native replay evidence '+n)
        if rom is not None:need(sha(rom[a:a+z])==f['code_sha256'],'original code drift '+n)
        names.add(n);spans.append((a,a+z))
    spans.sort();need(not names&prior_names(root) and all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'duplicate original owner');return fs

def head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2551,'new_original_C':13,'accepted_original_C':2564,'accepted_original_bytes':141596,'asm_remaining':4812,'canonical_semantic_relocations':80655,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+REG,'proof':'decomp/results/'+PROOF,'inventory':'decomp/results/'+INV}
def validate_proof(p,root=ROOT):
    old=read(root/'results'/transition.JP_INV);prior=prior_names(root);fs=rows(root);expected={'status':'PASSED_G2_LOCAL','region':'japan_0','source_manifest_sha256':MANIFEST_SHA,'base_c':2551,'added_c':13,'added_bytes':2136,'accepted_c_after':2564,'accepted_original_bytes_after':141596,'full_rom_match':True,'expanded_bytes':33554432,'expanded_sha1':ROM,'retail_exact':True,'retail_bytes':16777216,'retail_sha1':RETAIL,'positive_function_identities':7376,'stable_globals':26393,'semantic_relocations':80655,'semantic_relocation_sha256':RELOC,'prior_elf_sha256':PRE,'candidate_elf_sha256':NEW,'native_function_records':13,'native_negative_controls_rejected':13,'guarded_metadata_corrections':[],'compiler_outcome':'NO_NEW_COMPILER_FINDING','gameplay':'NOT_RUN'}
    need(all(p.get(k)==v for k,v in expected.items()),'native proof mismatch');i=p['strict_inventory'];need(i=={**old['strict_readelf_summary'],'upstream_unmarked_entries':2551,'newly_matching_c':13,'current_unmarked_entries':2564,'remaining_assembly_entries':4812,'upstream_unmarked_names':sorted(prior)},'strict inventory mismatch');return p
def documents(p,root=ROOT):
    validate_proof(p,root);fs=rows(root);prior=sorted(prior_names(root));ns=sorted(f['name'] for f in fs);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':f['source'],'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs]
    return {'format':FORMAT,'region':'japan_0','base_c':2551,'matching_c':2564,'assembly_remaining':4812,'original_C_instruction_bytes':141596,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':2551,'matching_c_after':2564,'remaining_assembly':4812,'accepted_original_C_bytes':141596,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80655,'candidate_semantic_relocations':80655,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':PRE,'candidate_elf_sha256':NEW,'previous_C_names':prior,'new_C_names':ns,'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def validate(root=ROOT):
    need(transition.validate_jp(root)['accepted_C']==2551,'historical JP2551 integrity');m=read(root/'regions/japan_0.json');
    if 'batch302_promotion' in m:
        from . import batch302_promotion as successor
        need({k:v for k,v in m.items() if k!=successor.JP_KEY}==successor.frozen('japan_0_2564_before_batch302.json',root),'JP2564 frozen predecessor mismatch')
        m=successor.frozen('japan_0_2564_before_batch302.json',root)
    need(m.pop(KEY,None)==head(),'regional master head mismatch');need(sha((json.dumps(m,indent=2)+'\n').encode())==PRIOR_MASTER_SHA,'regional predecessor drift');p=read(root/'results'/PROOF);r,i=documents(p,root);need(r==read(root/'regions'/REG) and i==read(root/'results'/INV),'regional source/inventory mismatch');return {'status':'PASS','accepted_C':2564,'remaining_assembly':4812,'accepted_original_bytes':141596}

def run(co,base,w,uv='uv',jobs=4):
    co,base,w=map(Path,(co,base,w));w.mkdir(parents=True,exist_ok=False);bd=co/'build/japan_0';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,'japan_0');fs=rows(rom=rom)
    need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','upstream pin');need(sha((co/'tools/ido-5.3/cc').read_bytes())==stage.COMPILER_SHA,'IDO pin')
    need(sha(elf.read_bytes())==PRE and (bd/'mnsg.z64').read_bytes()==rom and stage.original(base,'japan_0')==rom,'exact predecessor or pristine ROM missing')
    shutil.copyfile(elf,prior);f0=cross._funcs(prior);g0=opening.stable_globals(prior);r0=glitch.all_semantic_relocations(prior);n0=cright.c_identities(prior);targets={f['name'] for f in fs}
    need((sum(f0.values()),sum(g0.values()),r0[1],len(n0))==(7376,26393,80655,2551) and not n0&targets,'predecessor ELF/ownership')
    ledger=ROOT/'COMPILER_QUIRKS.md';need(b'NO_NEW_COMPILER_FINDING' in ledger.read_bytes(),'compiler ledger')
    d=stage.stage(co,'japan_0',candidates=[{**f,'source':str(ROOT/f['source'])} for f in fs],namespace='consolidate42');need(len(d['functions'])==13 and not d['blocked'],'active ASM ownership')
    ld=(co/'.splat/japan_0/mnsg.ld').read_text();stage.runmake(co,'japan_0',ld,[f'build/japan_0/{f["staged_path"]}.o' for f in d['functions']]+[f'build/japan_0/{f["path"]}.o' for f in d['fragments']],w/'compile.log',uv,jobs)
    for f in d['functions']:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];p=bd/(f['staged_path']+'.o');owner=base/'asm/japan_0'/f['owner'];probe.get_original_splat_lines(owner,n,a,f['vma'],z,rom[a:a+z]);raw=owner.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];need(len(m)==1,'reference source '+n);m=m[0];asm=w/(n+'.s');ref=w/(n+'.ref.o');asm.write_text(raw[:raw.index('/* Generated by')]+raw[m.start():m.end()]+'\n');subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(ref),str(asm)],cwd=co,check=True)
        need(exact(p,ref,f),'original native instruction/relocation or extent '+n);glitch.check_nontext(p);cross._trim_object(p,z,rom[a:a+z])
        # Deliberately changed source must fail native instruction/relocation equality.
        bad=w/(n+'.negative.c');bad.write_bytes(negative((ROOT/next(x['source'] for x in fs if x['name']==n)).read_bytes(),n));no=w/(n+'.negative.o');need(b'NO_NEW_COMPILER_FINDING' in ledger.read_bytes(),'compiler ledger');subprocess.run([str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(no),str(bad)],cwd=co,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);need(not exact(no,ref,f),'negative unexpectedly exact '+n)
    for f in d['fragments']:
        p=bd/(f['path']+'.o');a=f['start'];b=f['end']
        if f['suffix']=='.text.archive61':splice._trim_archive_asm(p,b-a)
        else:cross._trim_object(p,b-a,rom[a:b])
    def link(label):
        elf.unlink();(bd/'mnsg.z64').unlink();stage.runmake(co,'japan_0',ld,['build/japan_0/mnsg.z64'],w/(label+'.log'),uv,jobs)
        need((bd/'mnsg.z64').read_bytes()==rom and cross._funcs(elf)==f0 and glitch.all_semantic_relocations(elf)==r0 and cright.c_identities(elf)==n0|targets,'complete original native ROM/ELF/relocations/ownership')
    link('initial');need(opening.stable_globals(elf)==g0 and sha(elf.read_bytes())==NEW,'canonical globals or candidate ELF fingerprint')
    retail=w/'retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=co,check=True,stdout=subprocess.DEVNULL);rb=(co/'config/japan_0/baserom.z64').read_bytes();need(len(rb)==16777216 and hashlib.sha1(rb).hexdigest()==RETAIL and retail.read_bytes()==rb,'original retail mismatch');retail.unlink()
    strict=inventory.summarize_inventory(subprocess.check_output(['readelf','-Ws',str(prior)],text=True),subprocess.check_output(['readelf','-Ws',str(elf)],text=True),targets)
    need((strict['newly_matching_c'],strict['current_unmarked_entries'],strict['remaining_assembly_entries'])==(13,2564,4812) and not strict['size_annotation_differences'],'strict inventory')
    return {'status':'PASSED_G2_LOCAL','region':'japan_0','source_manifest_sha256':MANIFEST_SHA,'base_c':2551,'added_c':13,'added_bytes':2136,'accepted_c_after':2564,'accepted_original_bytes_after':141596,'full_rom_match':True,'expanded_bytes':33554432,'expanded_sha1':ROM,'retail_exact':True,'retail_bytes':16777216,'retail_sha1':RETAIL,'positive_function_identities':7376,'stable_globals':26393,'semantic_relocations':r0[1],'semantic_relocation_sha256':r0[2],'prior_elf_sha256':PRE,'candidate_elf_sha256':NEW,'native_function_records':13,'native_negative_controls_rejected':13,'guarded_metadata_corrections':[],'strict_inventory':strict,'compiler_outcome':'NO_NEW_COMPILER_FINDING','gameplay':'NOT_RUN'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path);p.add_argument('--pristine',type=Path);p.add_argument('--work',type=Path);p.add_argument('--uv',default='uv');p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
    if a.checkout:
        need(a.pristine and a.work,'native replay paths required');v=run(a.checkout,a.pristine,a.work,a.uv,a.jobs);write(a.work/'proof.json',v);print(json.dumps(v,indent=2))
    else:print(json.dumps(validate(),indent=2))
