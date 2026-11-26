"""Additive 13 USA / 52 Japan candidate transaction. Native and ROM-free gates separate."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
from . import promo195_promotion as previous
from . import japan_dispatcher_promotion as dispatcher
from . import consolidated_batch_promotion as native
ROOT=Path(__file__).resolve().parent
BATCH=Path('research/promo65_20261125')
KEY='usa_promo65_promotion'; FORMAT='goemon-promo65-original-ido-v1'
BASE='f4e4b6105796ec4c4e19b0415a24a9deea1f2e16'
FROZEN={'manifest': '027ef4d54709849220c3b8bfe63cf731c751b3bb4e7d7fe5cfea765b865c6001', 'combined': 'a381644f56d246964a7937e4244961c4fc27b21d96fb6219cf6278e2a4c78f7e', 'inventory': 'c077ca46ed2651214031e4ca2c5674da518e6efc6253aa8fa6b8fd499c683d42'}
REGIONS={'usa': {'added': 13, 'bytes': 1320, 'old': 3039, 'old_bytes': 205920, 'upstream': 13, 'relocs': 82080, 'globals': 26714, 'manifest': 'cfbbb52da4aa5f74dd5cf098d5fc3c41667e2f39b1e112836ce45e888854427e', 'prior': 'b2b8e73575741aa401345ea31c13fbae2abcf991699af455e94eed3b70d43aba', 'rom': '6ea0ed71032ce08fc2745f412d84936382197494', 'retail': 'df8083a54296b8c151917c5333e1c85f014a2a66', 'relocation_sha': '4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722', 'identity': '4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798', 'elf': '6f70966060da00ce4512b08d8773c317c9460f1628ea9e34ec29c12d1b1cf8c9'}, 'japan_0': {'added': 52, 'bytes': 6340, 'old': 2938, 'old_bytes': 190992, 'upstream': 0, 'relocs': 80652, 'globals': 26393, 'manifest': '8eace8e7a5abe46f8260e3dba33075e5094c7e22eb850431512383cbef147b8b', 'prior': 'd811b283cb622fc3dce9b6ad0cc461dadec19c797ff1de51fb937c8df095e222', 'rom': '6f8745fecc3a5e7d4918c7a73353eb0726116ded', 'retail': '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b', 'relocation_sha': 'a4094a4a38467b3f5369dd6d123a0194d43a0fb0be8dbf50a005395b6cb67354', 'identity': '9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e', 'elf': '968f658178568ae2b4222aeb060703c31d912871994b9429c6932a1c26d78896'}}
SDK_FLAGS={'usa': {'osCreateMesgQueue': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2'], 'osSpTaskYielded': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2'], 'osViSwapBuffer': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2'], 'osVirtualToPhysical': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2'], 'MusPtrBankGetCurrent': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O2', '-mips2', '-g3']}, 'japan_0': {'osSpTaskYielded': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2'], 'osVirtualToPhysical': ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm', '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.', '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM', '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O1', '-mips2']}}
PREDECESSOR_VERIFIER_SHA='52ab90ff5a8f0d99bf822a6373a972977db8eca23a035141c5a641279dcb4c41'
def need(value,msg):
    if not value: raise ValueError('Promo65: '+msg)
sha=previous.sha;read=previous.read;write=previous.write

def frozen(k,root=ROOT):
    p=root/'results'/f'{k}_3039_before_promo65.json';need(sha(p.read_bytes())==FROZEN[k],'frozen predecessor '+k);return read(p)

def rows(region,root=ROOT,rom=None):
    p=root/BATCH/f'{region}-candidates.json';cfg=REGIONS[region];need(sha(p.read_bytes())==cfg['manifest'],'manifest drift');rr=read(p)
    need((len(rr),sum(f['original_bytes'] for f in rr))==(cfg['added'],cfg['bytes']),'count/bytes')
    names=set();spans=[]
    for f in rr:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];v=f['vma'];need(f['region']==region and n not in names and re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',n) is not None and type(v) is int and a>=0 and z>0 and a%4==z%4==0 and a+z<=33554432,'identity '+n)
        if n.startswith('func_'):need(n==f'func_{v:08X}_{a:X}','address/name '+n)
        need(f['flags']==SDK_FLAGS[region].get(n,native.FLAGS) and f['nonstandard_sdk_flags']==(n in SDK_FLAGS[region]) and f['compiler_quirk_outcome'] in ('EXISTING_QUIRK_REPRODUCED','EXISTING_QUIRK_NOT_APPLICABLE','NEW_REPRODUCIBLE_QUIRK','NO_NEW_COMPILER_FINDING'),'compiler evidence '+n)
        need((root.parent/f['include_dir']).resolve().is_relative_to(root.resolve()) and (root.parent/f['include_dir']).is_dir(),'include directory '+n)
        for k,h,filename in [('source','source_sha256','candidate.c'),('negative_source','negative_sha256','negative.c')]:
            need(f[k]==f'sources/{region}/{n}/{filename}' and sha((root/BATCH/f[k]).read_bytes())==f[h],'source drift '+n+' '+k)
        need(f['source_sha256']!=f['negative_sha256'] and re.fullmatch('[a-f0-9]{64}',f['code_sha256']) is not None,'control/code evidence '+n)
        if rom is not None:need(sha(rom[a:a+z])==f['code_sha256'],'original code mismatch '+n)
        names.add(n);spans.append((a,a+z))
    spans.sort();need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'candidate overlap');return rr

def claims(root=ROOT):return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows('usa',root)]
def predecessor(m,root=ROOT,rom=None):
    from .verify import claimed_functions
    old=frozen('manifest',root);need(m.get(KEY)=={'format':FORMAT} and old=={k:v for k,v in m.items() if k!=KEY},'USA predecessor manifest drift')
    before=claimed_functions(old);need((len(before),sum(x['size'] for x in before))==(3039,205920),'USA predecessor count')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==REGIONS['usa']['rom'],'USA ROM')
    up=set(frozen('inventory',root)['summary']['upstream_unmarked_names'])
    for f in rows('usa',root,rom):
        a=f['rom_offset'];b=a+f['original_bytes'];need(f['name'] not in up and not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in before),'existing ownership '+f['name'])
    return before

def prior_names(r,root=ROOT):
    if r=='usa':
        from .verify import claimed_functions
        return {x['name'] for x in claimed_functions(frozen('manifest',root))}|set(frozen('inventory',root)['summary']['upstream_unmarked_names'])
    i=read(root/'results'/previous.JP_INV);return set(i['previous_C_names'])|set(i['new_C_names'])

def validate_native(r,p,root=ROOT):
    cfg=REGIONS[r];prev=cfg;fs=rows(r,root);byname={f['name']:f for f in fs};prior=prior_names(r,root);old=cfg['old']+cfg['upstream'];n=cfg['added'];new=old+n
    need(len(prior)==old and not set(byname)&prior,'predecessor ownership');need('elf' in cfg,'regional candidate not G2 verified')
    expected={'region':r,'requested':n,'stage':'completed_trial','base_commit':BASE,'source_manifest_sha256':cfg['manifest'],'compiler_sha256':native.stage.COMPILER_SHA,'prior_elf_sha256':cfg['prior'],'candidate_elf_sha256':cfg['elf'],'expanded_sha1':prev['rom'],'expanded_bytes':33554432,'retail_sha1':prev['retail'],'function_identities':7376,'semantic_relocations_before':cfg['relocs'],'semantic_relocations_after':cfg['relocs'],'semantic_relocation_sha256':prev['relocation_sha'],'stable_globals':cfg['globals'],'observed_new_ownership':n,'status':'PASSED_G2_LOCAL','staged':n}
    need(all(p.get(k)==v for k,v in expected.items()),'native proof identity')
    need(all(p.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','globals_exact','ownership_exact','semantic_relocations_exact')),'native gate failed')
    need(all(p.get(k)==[] for k in ('errors','blocked','function_removed','function_added','relocations_added','relocations_removed','globals_removed','globals_added')) and p.get('first_rom_mismatch') is None,'native discrepancies')
    need(len(p['native'])==n and {x['name'] for x in p['native']}==set(byname),'native records')
    for x in p['native']:
        f=byname[x['name']];need(x.get('native_exact') is True and x.get('negative_rejected') is True and 'error' not in x and (x['offset'],x['size'],x['source_sha256'],x['prior_research_outcome'])==(f['rom_offset'],f['original_bytes'],f['source_sha256'],f['compiler_quirk_outcome']),'native source/control '+f['name'])
    need(p['guarded_abs_restorations']==[],'unexpected new ABS metadata restoration')
    for x in p['native']:
        f=byname[x['name']];need(x.get('flags')==f['flags'],'actual compiler flags '+f['name'])
        need(x.get('default_flags_rejected') is True if f['nonstandard_sdk_flags'] else 'default_flags_rejected' not in x,'SDK default-flag control '+f['name'])
    need(all(x['code_and_relocations_unchanged'] is True and x['st_info_bytes_changed']==1 and x['compiler_outcome']=='EXISTING_QUIRK_REPRODUCED' for x in p['guarded_abs_restorations']),'ABS metadata evidence')
    i=p['strict_inventory'];need((i['identified_function_entries'],i['upstream_unmarked_entries'],i['newly_matching_c'],i['current_unmarked_entries'],i['remaining_assembly_entries'],i['extra_positive_alias_entries'],i['size_annotation_differences'],i['function_entry_identity_sha256'])==(7376,old,n,new,7376-new,0,[],prev['identity']),'strict inventory counts/identity')
    need(set(i['upstream_unmarked_names'])==prior and len(i['upstream_unmarked_names'])==old,'strict inventory predecessor names')
    return p

def proof_path(r,root=ROOT):return root/'results'/f'{r}_promo65_g2_20261125.json'
def proof_rows(root=ROOT):return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows('usa',root)]
def source_hashes(root=ROOT):return {str(BATCH/f['source']):f['source_sha256'] for f in rows('usa',root)}
def project(p,report,root=ROOT):
    validate_native('usa',p,root);c=report['comparison'];c['functions']+=proof_rows(root);c['matched_functions']+=13;c['claimed_functions']+=13;c['matched_function_bytes']+=1320;report['sources_sha256_lf'].update(source_hashes(root));report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa',root)}];report[KEY]=p

def run_native(r,co,pristine,w,uv='uv',jobs=4):
    need(__debug__,'assertions required');rows(r);b=ROOT/BATCH;w=Path(w).resolve();co=Path(co).resolve();pristine=Path(pristine).resolve();env=os.environ.copy();env['PYTHONPATH']=str(ROOT.parent)+os.pathsep+env.get('PYTHONPATH','');env.pop('PYTHONOPTIMIZE',None)
    subprocess.run([sys.executable,str(b/'attempt.py'),'--region',r,'--checkout',str(co),'--pristine',str(pristine),'--original-reference',str(pristine),'--manifest',str(b/f'{r}-candidates.json'),'--work',str(w),'--uv',str(uv),'--jobs',str(jobs)],env=env,cwd=ROOT.parent,check=True)
    p=read(w/'summary.json');p.update(base_commit=BASE,source_manifest_sha256=REGIONS[r]['manifest'],compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),expanded_bytes=33554432)
    validate_native(r,p);write(w/'canonical-stage-proof.json',p);return p

def apply(co,base,work,uv,jobs,m,report,rom):
    predecessor(m,rom=rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(3039,205920),'fresh USA predecessor report');project(run_native('usa',co,base,Path(work)/'promo65',uv,jobs),report)

def documents(p,root=ROOT):
    out=frozen('combined',root);project(p,out,root);out['verifier_source_sha256_lf']=sha((root/'verify.py').read_bytes());i=frozen('inventory',root);i['candidate_elf_sha256']=REGIONS['usa']['elf'];i['summary'].update(newly_matching_c=3052,current_unmarked_entries=3065,remaining_assembly_entries=4311);return out,i

def audit_usa(root,m,p,i):
    try:
        need(previous.audit_usa(root,frozen('manifest',root),frozen('combined',root),frozen('inventory',root),historical_verifier_sha=PREDECESSOR_VERIFIER_SHA)['status']=='PASS','historical USA3039 integrity');predecessor(m,root)
        stage=read(proof_path('usa',root));need(p[KEY]==stage,'canonical/dated proof drift');expected,ei=documents(stage,root)
        need(p['status']=='matched' and all(p[k]==expected[k] for k in ('comparison','sources_sha256_lf','retained_assembly_functions','verifier_source_sha256_lf',KEY)),'canonical proof ownership/ROM drift');need(i==ei,'strict inventory drift')
        return {'status':'PASS','accepted_C':3052,'accepted_original_bytes':207240,'remaining_assembly':4311,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as exc:return {'status':'FAIL','errors':[str(exc)]}

JP_KEY='promo65_promotion'
JP_REG='japan_0_2990_promo65.json'
JP_INV='japan_0_2990_promo65_inventory_20261125.json'
JP_FROZEN_SHA='3a1e039c1977af07277ae15c03284873126a89cba1dc9d197b40f8298a418d52'

def jp_head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2938,'new_original_C':52,'accepted_original_C':2990,'accepted_original_bytes':197332,'asm_remaining':4386,'canonical_semantic_relocations':80652,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+proof_path('japan_0').name,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_native('japan_0',p,root);fs=rows('japan_0',root);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':str(BATCH/f['source']),'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs];prior=sorted(prior_names('japan_0',root))
    return {'format':FORMAT,'region':'japan_0','base_c':2938,'matching_c':2990,'assembly_remaining':4386,'original_C_instruction_bytes':197332,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':2938,'matching_c_after':2990,'remaining_assembly':4386,'accepted_original_C_bytes':197332,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80652,'candidate_semantic_relocations':80652,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':REGIONS['japan_0']['prior'],'candidate_elf_sha256':REGIONS['japan_0']['elf'],'previous_C_names':prior,'new_C_names':sorted(f['name'] for f in fs),'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def master_predecessor(m,root=ROOT):
    path=root/'results/japan_0_2938_before_promo65.json';need(sha(path.read_bytes())==JP_FROZEN_SHA,'JP frozen predecessor fingerprint');old=read(path);need(m.get(JP_KEY)==jp_head() and {k:v for k,v in m.items() if k!=JP_KEY}==old,'JP2938 frozen predecessor mismatch');return old
def validate_jp(root=ROOT):
    need(previous.validate_jp(root)['accepted_C']==2938,'historical JP2938 integrity');master_predecessor(read(root/'regions/japan_0.json'),root);p=read(proof_path('japan_0',root));r,i=jp_documents(p,root);need(r==read(root/'regions'/JP_REG) and i==read(root/'results'/JP_INV),'Japan source/inventory drift');return {'status':'PASS','accepted_C':2990,'accepted_original_bytes':197332,'remaining_assembly':4386}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=REGIONS);parser.add_argument('--checkout',type=Path);parser.add_argument('--pristine',type=Path);parser.add_argument('--work',type=Path);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    if a.checkout:
        need(a.region and a.pristine and a.work,'native inputs required');print(json.dumps(run_native(a.region,a.checkout,a.pristine,a.work,a.uv,a.jobs),indent=2))
    else:print(json.dumps(validate_jp(),indent=2))
