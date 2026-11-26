"""Additive 100 USA / 95 Japan candidate transaction. Native and ROM-free gates separate."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
from . import promo367_promotion as previous
from . import japan_dispatcher_promotion as dispatcher
from . import consolidated_batch_promotion as native
ROOT=Path(__file__).resolve().parent
BATCH=Path('research/promo195_20261125')
KEY='usa_promo195_promotion'; FORMAT='goemon-promo195-original-ido-v1'
BASE='3669a15a807c77249e85cd177ef2704d5560e5d1'
FROZEN={'manifest': '3aa813c70b09cfe2ce6a696e1d543759795f48216560f32719cc21d9cd50a49c', 'combined': 'b69d267273026061868fbeb99552dd19681a7de8762e7c6f80f058e01764fc55', 'inventory': '04e1c24858fc6a9d07fb5953fa2351dcfa861b71587b7e80857a50aabed0d087'}
REGIONS={'usa': {'added': 100, 'bytes': 13608, 'old': 2939, 'old_bytes': 192312, 'upstream': 13, 'relocs': 82080, 'globals': 26714, 'manifest': 'fc2ed4938b94516f082816f8bd292f76db059d77a88e431d9ee578fa240d1622', 'prior': '2d3228155fc3cf06f386791094e86ba2b5205fcbc22a78f36239a57c2d340a03', 'rom': '6ea0ed71032ce08fc2745f412d84936382197494', 'retail': 'df8083a54296b8c151917c5333e1c85f014a2a66', 'relocation_sha': '4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722', 'identity': '4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798', 'elf': 'b2b8e73575741aa401345ea31c13fbae2abcf991699af455e94eed3b70d43aba'}, 'japan_0': {'added': 95, 'bytes': 12832, 'old': 2843, 'old_bytes': 178160, 'upstream': 0, 'relocs': 80652, 'globals': 26393, 'manifest': '7eec77c88f38d3db6955ecf3b5fa103d2235d913696f64455ceeba70324bb33a', 'prior': '5f1f7536e8b03a6911a35e09dcf92dced675c7aab5e0c63fea4f7d4adc4725a9', 'rom': '6f8745fecc3a5e7d4918c7a73353eb0726116ded', 'retail': '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b', 'relocation_sha': 'a4094a4a38467b3f5369dd6d123a0194d43a0fb0be8dbf50a005395b6cb67354', 'identity': '9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e', 'elf': 'd811b283cb622fc3dce9b6ad0cc461dadec19c797ff1de51fb937c8df095e222'}}
def need(value,msg):
    if not value: raise ValueError('Promo195: '+msg)
sha=previous.sha;read=previous.read;write=previous.write

def frozen(k,root=ROOT):
    p=root/'results'/f'{k}_2939_before_promo195.json';need(sha(p.read_bytes())==FROZEN[k],'frozen predecessor '+k);return read(p)

def rows(region,root=ROOT,rom=None):
    p=root/BATCH/f'{region}-candidates.json';cfg=REGIONS[region];need(sha(p.read_bytes())==cfg['manifest'],'manifest drift');rr=read(p)
    need((len(rr),sum(f['original_bytes'] for f in rr))==(cfg['added'],cfg['bytes']),'count/bytes')
    names=set();spans=[]
    for f in rr:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];v=f['vma'];need(f['region']==region and n not in names and re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',n) is not None and type(v) is int and a>=0 and z>0 and a%4==z%4==0 and a+z<=33554432,'identity '+n)
        if n.startswith('func_'):need(n==f'func_{v:08X}_{a:X}','address/name '+n)
        need(f['flags']==native.FLAGS and f['compiler_quirk_outcome'] in ('EXISTING_QUIRK_REPRODUCED','EXISTING_QUIRK_NOT_APPLICABLE','NEW_REPRODUCIBLE_QUIRK','NO_NEW_COMPILER_FINDING'),'compiler evidence '+n)
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
    before=claimed_functions(old);need((len(before),sum(x['size'] for x in before))==(2939,192312),'USA predecessor count')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==REGIONS['usa']['rom'],'USA ROM')
    up=set(frozen('inventory',root)['summary']['upstream_unmarked_names'])
    for f in rows('usa',root,rom):
        a=f['rom_offset'];b=a+f['original_bytes'];need(f['name'] not in up and not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in before),'existing ownership '+f['name'])
    return before

def prior_names(r,root=ROOT):
    if r=='usa':
        from .verify import claimed_functions
        return {x['name'] for x in claimed_functions(frozen('manifest',root))}|set(frozen('inventory',root)['summary']['upstream_unmarked_names'])
    i=read(root/dispatcher.INV);return set(i['previous_C_names'])|set(i['new_C_names'])

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
    need(len(p['guarded_abs_restorations'])==(1 if r=='usa' else 0),'ABS metadata count')
    if r=='usa':need(p['guarded_abs_restorations'][0]['symbol']=='D_8020EF30_63A310','original ABS symbol identity')
    need(all(x['code_and_relocations_unchanged'] is True and x['st_info_bytes_changed']==1 and x['compiler_outcome']=='EXISTING_QUIRK_REPRODUCED' for x in p['guarded_abs_restorations']),'ABS metadata evidence')
    i=p['strict_inventory'];need((i['identified_function_entries'],i['upstream_unmarked_entries'],i['newly_matching_c'],i['current_unmarked_entries'],i['remaining_assembly_entries'],i['extra_positive_alias_entries'],i['size_annotation_differences'],i['function_entry_identity_sha256'])==(7376,old,n,new,7376-new,0,[],prev['identity']),'strict inventory counts/identity')
    need(set(i['upstream_unmarked_names'])==prior and len(i['upstream_unmarked_names'])==old,'strict inventory predecessor names')
    return p

def proof_path(r,root=ROOT):return root/'results'/f'{r}_promo195_g2_20261125.json'
def proof_rows(root=ROOT):return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows('usa',root)]
def source_hashes(root=ROOT):return {str(BATCH/f['source']):f['source_sha256'] for f in rows('usa',root)}
def project(p,report,root=ROOT):
    validate_native('usa',p,root);c=report['comparison'];c['functions']+=proof_rows(root);c['matched_functions']+=100;c['claimed_functions']+=100;c['matched_function_bytes']+=13608;report['sources_sha256_lf'].update(source_hashes(root));report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa',root)}];report[KEY]=p

def run_native(r,co,pristine,w,uv='uv',jobs=4):
    need(__debug__,'assertions required');rows(r);b=ROOT/BATCH;w=Path(w).resolve();co=Path(co).resolve();pristine=Path(pristine).resolve();env=os.environ.copy();env['PYTHONPATH']=str(ROOT.parent)+os.pathsep+env.get('PYTHONPATH','');env.pop('PYTHONOPTIMIZE',None)
    subprocess.run([sys.executable,str(b/'attempt.py'),'--region',r,'--checkout',str(co),'--pristine',str(pristine),'--original-reference',str(pristine),'--manifest',str(b/f'{r}-candidates.json'),'--work',str(w),'--uv',str(uv),'--jobs',str(jobs)],env=env,cwd=ROOT.parent,check=True)
    p=read(w/'summary.json');p.update(base_commit=BASE,source_manifest_sha256=REGIONS[r]['manifest'],compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),expanded_bytes=33554432)
    validate_native(r,p);write(w/'canonical-stage-proof.json',p);return p

def apply(co,base,work,uv,jobs,m,report,rom):
    predecessor(m,rom=rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(2939,192312),'fresh USA predecessor report');project(run_native('usa',co,base,Path(work)/'promo195',uv,jobs),report)

def documents(p,root=ROOT,*,historical_verifier_sha=None):
    out=frozen('combined',root);project(p,out,root);out['verifier_source_sha256_lf']=historical_verifier_sha or sha((root/'verify.py').read_bytes());i=frozen('inventory',root);i['candidate_elf_sha256']=REGIONS['usa']['elf'];i['summary'].update(newly_matching_c=3039,current_unmarked_entries=3052,remaining_assembly_entries=4324);return out,i

def audit_usa(root,m,p,i,*,historical_verifier_sha=None):
    try:
        need(previous.audit_usa(root,frozen('manifest',root),frozen('combined',root),frozen('inventory',root))['status']=='PASS','historical USA2939 integrity');predecessor(m,root)
        stage=read(proof_path('usa',root));need(p[KEY]==stage,'canonical/dated proof drift');expected,ei=documents(stage,root,historical_verifier_sha=historical_verifier_sha)
        need(p['status']=='matched' and all(p[k]==expected[k] for k in ('comparison','sources_sha256_lf','retained_assembly_functions','verifier_source_sha256_lf',KEY)),'canonical proof ownership/ROM drift');need(i==ei,'strict inventory drift')
        return {'status':'PASS','accepted_C':3039,'accepted_original_bytes':205920,'remaining_assembly':4324,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as exc:return {'status':'FAIL','errors':[str(exc)]}

JP_KEY='promo195_promotion'
JP_REG='japan_0_2938_promo195.json'
JP_INV='japan_0_2938_promo195_inventory_20261125.json'
JP_FROZEN_SHA='609ab422e07bba023546e3bc594978fe9a3c13bf8dab4c9cbcd98eb0fbf07266'

def jp_head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2843,'new_original_C':95,'accepted_original_C':2938,'accepted_original_bytes':190992,'asm_remaining':4438,'canonical_semantic_relocations':80652,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+proof_path('japan_0').name,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_native('japan_0',p,root);fs=rows('japan_0',root);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':str(BATCH/f['source']),'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs];prior=sorted(prior_names('japan_0',root))
    return {'format':FORMAT,'region':'japan_0','base_c':2843,'matching_c':2938,'assembly_remaining':4438,'original_C_instruction_bytes':190992,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':2843,'matching_c_after':2938,'remaining_assembly':4438,'accepted_original_C_bytes':190992,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80652,'candidate_semantic_relocations':80652,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':REGIONS['japan_0']['prior'],'candidate_elf_sha256':REGIONS['japan_0']['elf'],'previous_C_names':prior,'new_C_names':sorted(f['name'] for f in fs),'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def master_predecessor(m,root=ROOT):
    if "promo65_promotion" in m:
        from . import promo65_promotion as successor
        m=successor.master_predecessor(m,root)
    path=root/'results/japan_0_2843_before_promo195.json';need(sha(path.read_bytes())==JP_FROZEN_SHA,'JP frozen predecessor fingerprint');old=read(path);need(m.get(JP_KEY)==jp_head() and {k:v for k,v in m.items() if k!=JP_KEY}==old,'JP2843 frozen predecessor mismatch');return old
def validate_jp(root=ROOT):
    need(dispatcher.validate(root)['accepted_C']==2843,'historical JP2843 integrity');master_predecessor(read(root/'regions/japan_0.json'),root);p=read(proof_path('japan_0',root));r,i=jp_documents(p,root);need(r==read(root/'regions'/JP_REG) and i==read(root/'results'/JP_INV),'Japan source/inventory drift');return {'status':'PASS','accepted_C':2938,'accepted_original_bytes':190992,'remaining_assembly':4438}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=REGIONS);parser.add_argument('--checkout',type=Path);parser.add_argument('--pristine',type=Path);parser.add_argument('--work',type=Path);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    if a.checkout:
        need(a.region and a.pristine and a.work,'native inputs required');print(json.dumps(run_native(a.region,a.checkout,a.pristine,a.work,a.uv,a.jobs),indent=2))
    else:print(json.dumps(validate_jp(),indent=2))
