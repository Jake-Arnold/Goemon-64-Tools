"""Additive USA original-ROM promotion from the accepted 2325-C predecessor.

The native replay requires private original ROMs and pinned IDO. The stored
integrity check is ROM-free and does not substitute for native proof.
"""
from pathlib import Path
import argparse, copy, hashlib, json, re, shutil, subprocess
from . import inventory, usa_cright4_promotion as stage, native251_promotion as native
from . import overlay_crossregion47 as cross, overlay_isolated233 as splice
from . import usa_opening_new2_promotion as opening, usa_short72_promotion as short72
from . import japan_cright_promotion as cright, glitch_g2_promotion as glitch
from . import japan_jp55_promotion as jp55, native_probe_helpers251 as probe
ROOT=Path(__file__).resolve().parent
KEY='usa_consolidated29_promotion'
FORMAT='goemon-usa-consolidated29-post2325-v1'
BASE='64e5445b5b044cfd1f841b21c23af81f44da5644'
BATCH=ROOT/'research/consolidated42_20261124'
MANIFEST_SHA='2f92e36edba2b754a7be6ad3f9737a21f1962204108ca72d6e5a1c4a27ba7592'
FROZEN={'manifest_2325_before_consolidated29_20261124.json':'79337f4c10cea9bede0bfe663e2e0bfe890131d3c0e2e7e6e2983d8c7816f723','combined_2325_before_consolidated29_20261124.json':'bc5680407934d37520b2a4dfcaf68f7de265561a56759f1b500c8814eb5229d6','inventory_2325_before_consolidated29_20261124.json':'36e591a3a65da7336eccf9c47c7a15ad05710fbbb34dc9edfd6ec591b27b859e'}
PROOF='usa_consolidated29_2354_g2_20261124.json'
PRE='bb2691558d9c65b6443aaa60d26154286d52ffcaf4f84ed0cfe3d1db6cbf082b'
NEW='23b0af722f70a8aa86a7ca73874a3a7cd0235cff896f6364333cac04f394d724'
ROM='6ea0ed71032ce08fc2745f412d84936382197494'
RETAIL='df8083a54296b8c151917c5333e1c85f014a2a66'
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def need(ok,msg):
    if not ok:raise ValueError('Consolidated29: '+msg)
def frozen(root=ROOT):
    out=[]
    for n,h in FROZEN.items():
        p=root/'results'/n;need(sha(p.read_bytes())==h,'frozen predecessor drift '+n);out.append(read(p))
    return out

def negative(source,name):
    m=re.search(rb'\b'+name.encode()+rb'\s*\([^;{}]*\)\s*\{',source);need(m is not None,'negative source boundary '+name)
    return source[:m.end()]+b'\nvolatile unsigned int goemon_negative_control = 1;\n'+source[m.end():]

def rows(root=ROOT,rom=None):
    p=root/'research/consolidated42_20261124/usa_manifest.json';need(sha(p.read_bytes())==MANIFEST_SHA,'source manifest drift');fs=read(p)
    need((len(fs),sum(x['original_bytes'] for x in fs),sum(x['relocation_count'] for x in fs))==(29,3372,140),'candidate extent/count')
    ranges=[];names=set()
    for f in fs:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];need(f['region']=='usa' and n==f'func_{f["vma"]:08X}_{a:X}' and z>0 and a%4==z%4==0 and n not in names,'candidate identity '+n)
        need(f['source']==f'research/consolidated42_20261124/usa/{n}.c','source path '+n)
        s=(root/f['source']).read_bytes();need(sha(s)==f['source_sha256'],'source drift '+n)
        pos=[t for t in f['trials'] if t['status']=='EXACT'];neg=f['trials'][-1]
        need(len(pos)==1 and pos[0]['source_sha256']==sha(s) and pos[0]['flags']==FLAGS and neg['status']=='FAILED_NATIVE' and sha(negative(s,n))==neg['source_sha256'] and neg['flags']==FLAGS,'native replay evidence '+n)
        if rom is not None:need(sha(rom[a:a+z])==f['code_sha256'],'original code drift '+n)
        names.add(n);ranges.append((a,a+z))
    ranges.sort();need(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'overlapping original ranges')
    return fs

def claims():return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows()]
def validate_predecessor(m,rom=None):
    from . import verify
    old,_,_=frozen();need(m.get(KEY)=={'format':FORMAT} and old=={k:v for k,v in m.items() if k!=KEY},'canonical predecessor manifest drift')
    before=verify.claimed_functions(old);need((len(before),sum(f['size'] for f in before))==(2325,112420),'canonical predecessor claims')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM,'original ROM mismatch')
    for f in rows(rom=rom):
        a=f['rom_offset'];b=a+f['original_bytes'];need(not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in before),'already owned '+f['name'])
    return before

def proof_rows():
    return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows()]
def source_hashes():return {f['source']:f['source_sha256'] for f in rows()}

def rels(p):
    t=subprocess.check_output(['readelf','-rW',str(p)],text=True);part=re.search(r"Relocation section '.rel.text'[^\n]*\n(.*?)(?=\nRelocation section|\Z)",t,re.S)
    return sorted((int(a,16),b,c) for a,b,c in re.findall(r'^\s*([a-fA-F0-9]+)\s+[a-fA-F0-9]+\s+(R_MIPS_\w+)\s+[a-fA-F0-9]+\s+(\S+)',part[1] if part else '',re.M))
def text(p):
    b=p.read_bytes();s=opening.elf_sections(b)['.text'];return b[s['offset']:s['offset']+s['size']]
def exact(p,ref,f):
    z=f['original_bytes'];n=f['name'];b=text(p);a=text(ref);s=subprocess.check_output(['readelf','-Ws',str(p)],text=True)
    ok,_=probe.check_size(s,n,z)
    return ok and len(b)>=z and not any(b[z:]) and b[:z]==a[:z] and rels(p)==rels(ref) and len(rels(ref))==f['relocation_count']

def run(co,base,w,uv='uv',jobs=4):
    co,base,w=map(Path,(co,base,w));w.mkdir(parents=True,exist_ok=False);bd=co/'build/usa';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,'usa');fs=rows(rom=rom)
    need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','upstream pin');need(sha((co/'tools/ido-5.3/cc').read_bytes())==stage.COMPILER_SHA,'IDO pin')
    need(sha(elf.read_bytes())==PRE and (bd/'mnsg.z64').read_bytes()==rom and (base/'build/usa/mnsg.z64').read_bytes()==rom,'exact predecessor or pristine ROM missing')
    shutil.copyfile(elf,prior);f0=cross._funcs(prior);g0=opening.stable_globals(prior);r0=glitch.all_semantic_relocations(prior);n0=cright.c_identities(prior);targets={f['name'] for f in fs}
    need((sum(f0.values()),sum(g0.values()),r0[1],len(n0))==(7376,26714,82080,2338) and not n0&targets,'predecessor ELF/ownership')
    ledger=ROOT/'COMPILER_QUIRKS.md';need(b'NO_NEW_COMPILER_FINDING' in ledger.read_bytes(),'compiler ledger')
    d=stage.stage(co,'usa',candidates=[{**f,'source':str(ROOT/f['source'])} for f in fs],namespace='consolidate42');need(len(d['functions'])==29 and not d['blocked'],'active ASM ownership')
    ld=(co/'.splat/usa/mnsg.ld').read_text();stage.runmake(co,'usa',ld,[f'build/usa/{f["staged_path"]}.o' for f in d['functions']]+[f'build/usa/{f["path"]}.o' for f in d['fragments']],w/'compile.log',uv,jobs)
    for f in d['functions']:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];p=bd/(f['staged_path']+'.o');owner=base/'asm/usa'/f['owner'];probe.get_original_splat_lines(owner,n,a,f['vma'],z,rom[a:a+z]);raw=owner.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];need(len(m)==1,'reference source '+n);m=m[0];asm=w/(n+'.s');ref=w/(n+'.ref.o');asm.write_text(raw[:raw.index('/* Generated by')]+raw[m.start():m.end()]+'\n');subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(ref),str(asm)],cwd=co,check=True)
        need(exact(p,ref,f),'original native instruction/relocation or extent '+n);glitch.check_nontext(p);cross._trim_object(p,z,rom[a:a+z])
        # Deliberately changed source must fail native instruction/relocation equality.
        bad=w/(n+'.negative.c');bad.write_bytes(negative((ROOT/next(x['source'] for x in fs if x['name']==n)).read_bytes(),n));no=w/(n+'.negative.o');need(b'NO_NEW_COMPILER_FINDING' in ledger.read_bytes(),'compiler ledger');subprocess.run([str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(no),str(bad)],cwd=co,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);need(not exact(no,ref,f),'negative unexpectedly exact '+n)
    for f in d['fragments']:
        p=bd/(f['path']+'.o');a=f['start'];b=f['end']
        if f['suffix']=='.text.archive61':splice._trim_archive_asm(p,b-a)
        else:cross._trim_object(p,b-a,rom[a:b])
    def link(label):
        elf.unlink();(bd/'mnsg.z64').unlink();stage.runmake(co,'usa',ld,['build/usa/mnsg.z64'],w/(label+'.log'),uv,jobs);short72.restore_original_abs_label_type(elf,prior);native.restore_inline_usa(elf,prior)
        need((bd/'mnsg.z64').read_bytes()==rom and cross._funcs(elf)==f0 and glitch.all_semantic_relocations(elf)==r0 and cright.c_identities(elf)==n0|targets,'complete original native ROM/ELF/relocations/ownership')
    link('initial');g=opening.stable_globals(elf);missing=list((g0-g).items());added=list((g-g0).items());need(len(missing)==len(added)==1 and missing[0][0][-1]==added[0][0][-1]=='D_801D7030_6A9C50' and missing[0][0][2]=='NOTYPE' and added[0][0][2]=='OBJECT','original symbol metadata negative control')
    fix=native.restore_undefined_type(bd/'src/consolidate42/func_801CBF5C_69EB7C.c.o','D_801D7030_6A9C50',36,g0);link('guarded');need(opening.stable_globals(elf)==g0 and sha(elf.read_bytes())==NEW,'canonical globals or candidate ELF fingerprint')
    retail=w/'retail.z64';subprocess.run([str(uv),'run','python','tools/rommy.py','compress','--input','build/usa/mnsg.z64','--output',str(retail),'--manifest','config/usa/rommy.yaml','--pad','--verify'],cwd=co,check=True,stdout=subprocess.DEVNULL);rb=(co/'config/usa/baserom.z64').read_bytes();need(len(rb)==16777216 and hashlib.sha1(rb).hexdigest()==RETAIL and retail.read_bytes()==rb,'original retail mismatch');retail.unlink()
    strict=inventory.summarize_inventory(subprocess.check_output(['readelf','-Ws',str(base/'build/usa/mnsg.elf')],text=True),subprocess.check_output(['readelf','-Ws',str(elf)],text=True),{f['name'] for f in frozen()[1]['comparison']['functions']}|targets)
    need((strict['newly_matching_c'],strict['remaining_assembly_entries'])==(2354,5009),'strict inventory')
    return {'status':'PASSED_G2_LOCAL','base_commit':BASE,'source_manifest_sha256':MANIFEST_SHA,'base_c':2325,'added_c':29,'added_bytes':3372,'accepted_c_after':2354,'accepted_original_bytes_after':115792,'full_rom_match':True,'expanded_bytes':33554432,'expanded_sha1':ROM,'retail_exact':True,'retail_bytes':16777216,'retail_sha1':RETAIL,'positive_function_identities':7376,'stable_globals':26714,'semantic_relocations':r0[1],'semantic_relocation_sha256':r0[2],'prior_elf_sha256':PRE,'candidate_elf_sha256':NEW,'native_function_records':29,'native_negative_controls_rejected':29,'guarded_metadata_correction':fix,'strict_inventory':strict,'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'}

def validate_proof(p,root=ROOT):
    _,_,i=frozen(root);need(p==read(root/'results'/PROOF),'dated native proof drift')
    expected={'status':'PASSED_G2_LOCAL','base_commit':BASE,'source_manifest_sha256':MANIFEST_SHA,'base_c':2325,'added_c':29,'added_bytes':3372,'accepted_c_after':2354,'accepted_original_bytes_after':115792,'full_rom_match':True,'expanded_bytes':33554432,'expanded_sha1':ROM,'retail_exact':True,'retail_bytes':16777216,'retail_sha1':RETAIL,'positive_function_identities':7376,'stable_globals':26714,'semantic_relocations':82080,'semantic_relocation_sha256':'4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722','prior_elf_sha256':PRE,'candidate_elf_sha256':NEW,'native_function_records':29,'native_negative_controls_rejected':29,'strict_inventory':{**i['summary'],'newly_matching_c':2354,'current_unmarked_entries':2367,'remaining_assembly_entries':5009},'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'}
    need(all(p.get(k)==v for k,v in expected.items()),'native proof or strict inventory mismatch');f=p['guarded_metadata_correction'];need(f['symbol']=='D_801D7030_6A9C50' and f['undefined_size']==36 and f['st_info_bytes_changed']==1 and f['code_and_relocations_unchanged'] is True,'metadata-only proof drift');return p

def apply(co,base,work,uv,jobs,m,report,rom):
    validate_predecessor(m,rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(2325,112420),'fresh predecessor report')
    p=run(co,base,Path(work)/'consolidated29',uv,jobs);c['functions']+=proof_rows();c['matched_functions']+=29;c['claimed_functions']+=29;c['matched_function_bytes']+=3372;report['sources_sha256_lf'].update(source_hashes());report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows()}];report[KEY]=p

def audit(root,m,p,i):
    from . import verify, transition_final_promotion as prior
    try:
        old,op,oi=frozen(root);validate_predecessor(m);rows(root);need(prior.audit(root,old,op,oi)['status']=='PASS','historical USA2325 integrity');pr=validate_proof(p[KEY],root);c=p['comparison'];oc=op['comparison'];need(p['status']=='matched' and c['full_rom_match'] is True and (c['matched_functions'],c['claimed_functions'],c['matched_function_bytes'])==(2354,2354,115792) and (c['expected_sha1'],c['candidate_sha1'],c['rom_size'])==(ROM,ROM,33554432),'comparison counts or ROM');need(c['functions']==oc['functions']+proof_rows(),'historical proof changed');need(p['sources_sha256_lf']=={**op['sources_sha256_lf'],**source_hashes()} and p['retained_assembly_functions']==[n for n in op['retained_assembly_functions'] if n not in {f['name'] for f in rows()}],'source ownership drift');need(i=={**oi,'candidate_elf_sha256':NEW,'summary':pr['strict_inventory']},'strict inventory drift');f=verify.claimed_functions(m);need((len(f),sum(x['size'] for x in f))==(2354,115792),'canonical claims');return {'status':'PASS','accepted_C':2354,'accepted_original_bytes':115792,'remaining_assembly':5009,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as e:return {'status':'FAIL','errors':[str(e)]}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',default='uv');p.add_argument('--jobs',type=int,default=4);a=p.parse_args();v=run(a.checkout,a.pristine,a.work,a.uv,a.jobs);write(a.work/'proof.json',v);print(json.dumps(v,indent=2))
