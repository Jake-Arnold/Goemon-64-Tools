"""Additive 21 USA / 15 Japan candidate transaction. Native and ROM-free gates separate."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
from . import warp_batch_a_promotion as previous
from . import consolidated_batch_promotion as native
ROOT=Path(__file__).resolve().parent
BATCH=Path('research/promo36_20261125')
KEY='usa_promo36_promotion'; FORMAT='goemon-promo36-original-ido-v1'
BASE='8b195d8ce5a31723a71af428ee4f7bccf32b0bf8'
FROZEN={'manifest': 'f988004079a0fee24228b8420a5b05c1a7cd62c0562a3e64519c604745705705', 'combined': '086d1018e72339ac2943bfca9c739cebb870b096d8fabc8f4bda62cc35c21ebf', 'inventory': 'b8d7a64dc2be1439b985d86c807971732342f45f6378c6ee05db4647d9fc0087'}
REGIONS={'usa': {'added': 21, 'bytes': 1776, 'old': 3066, 'old_bytes': 210636, 'upstream': 13, 'relocs': 82080, 'globals': 26714, 'manifest': '830556266b8e0e0c7ae27ee1ddb69959b92cd54e4e8e4f805ddda6d07fd8eba5', 'prior': '1107b0f4d2d7eaf17107323ae5119076476a773aabba01f77d27113353abb6ff', 'rom': '6ea0ed71032ce08fc2745f412d84936382197494', 'retail': 'df8083a54296b8c151917c5333e1c85f014a2a66', 'relocation_sha': '4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722', 'identity': '4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798', 'elf': 'a2667d1677d9f283ab8abb27a439581439849157979f9876e95cdbff310cf3d6'}, 'japan_0': {'added': 15, 'bytes': 1176, 'old': 3004, 'old_bytes': 201000, 'upstream': 0, 'relocs': 80652, 'globals': 26393, 'manifest': '3578ca6519f2fb5511f360d0a2e89779668f92d4301e2cd5bb1d1c6fe7613991', 'prior': '8b62b85eb9e32bc5b499017ac882c54e34ad666bdd47f3cd3867d36477935b0d', 'rom': '6f8745fecc3a5e7d4918c7a73353eb0726116ded', 'retail': '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b', 'relocation_sha': 'a4094a4a38467b3f5369dd6d123a0194d43a0fb0be8dbf50a005395b6cb67354', 'identity': '9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e', 'elf': '26d14cc17af2046abd2e785feaee306f8dda2d1acade2a83778c7fa3c8436e5e'}}
GUARDED_ABS={'usa': [('build/usa/src/promo36/func_800369B4_375B4.c.o', 'D_3B014'), ('build/usa/src/promo36/func_800374AC_380AC.c.o', 'D_3AFE0'), ('build/usa/src/promo36/func_801E4194_60F574.c.o', 'D_8020EF08_63A2E8')], 'japan_0': [('build/japan_0/src/promo36/func_80036624_37224.c.o', 'D_3B014')]}
PREDECESSOR_VERIFIER_SHA='a901c9e137336e014a914bec63e4d570ceb1afa44b15e302a07f58c8215d486b'
def need(value,msg):
    if not value: raise ValueError('Promo36: '+msg)
sha=previous.sha;read=previous.read;write=previous.write

def frozen(k,root=ROOT):
    p=root/'results'/f'{k}_3066_before_promo36.json';need(sha(p.read_bytes())==FROZEN[k],'frozen predecessor '+k);return read(p)

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
        need(f.get('headers_sha256')=={p.name:sha(p.read_bytes()) for p in sorted((root/BATCH/f['source']).parent.glob('*.h'))},'header drift '+n)
        need(f['source_sha256']!=f['negative_sha256'] and re.fullmatch('[a-f0-9]{64}',f['code_sha256']) is not None,'control/code evidence '+n)
        if rom is not None:need(sha(rom[a:a+z])==f['code_sha256'],'original code mismatch '+n)
        names.add(n);spans.append((a,a+z))
    spans.sort();need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'candidate overlap');return rr

def claims(root=ROOT):return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows('usa',root)]
def predecessor(m,root=ROOT,rom=None):
    from .verify import claimed_functions
    old=frozen('manifest',root);need(m.get(KEY)=={'format':FORMAT} and old=={k:v for k,v in m.items() if k!=KEY},'USA predecessor manifest drift')
    before=claimed_functions(old);need((len(before),sum(x['size'] for x in before))==(3066,210636),'USA predecessor count')
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
    need(sorted((x['object'],x['symbol']) for x in p['guarded_abs_restorations'])==GUARDED_ABS[r],'unexpected ABS metadata restoration')
    need(all(x['code_and_relocations_unchanged'] is True and x['st_info_bytes_changed']==1 and x['compiler_outcome']=='EXISTING_QUIRK_REPRODUCED' for x in p['guarded_abs_restorations']),'ABS metadata evidence')
    i=p['strict_inventory'];need((i['identified_function_entries'],i['upstream_unmarked_entries'],i['newly_matching_c'],i['current_unmarked_entries'],i['remaining_assembly_entries'],i['extra_positive_alias_entries'],i['size_annotation_differences'],i['function_entry_identity_sha256'])==(7376,old,n,new,7376-new,0,[],prev['identity']),'strict inventory counts/identity')
    need(set(i['upstream_unmarked_names'])==prior and len(i['upstream_unmarked_names'])==old,'strict inventory predecessor names')
    return p

def proof_path(r,root=ROOT):return root/'results'/f'{r}_promo36_g2_20261126.json'
def proof_rows(root=ROOT):return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows('usa',root)]
def source_hashes(root=ROOT):return {str(BATCH/f['source']):f['source_sha256'] for f in rows('usa',root)}
def project(p,report,root=ROOT):
    validate_native('usa',p,root);c=report['comparison'];c['functions']+=proof_rows(root);c['matched_functions']+=21;c['claimed_functions']+=21;c['matched_function_bytes']+=1776;report['sources_sha256_lf'].update(source_hashes(root));report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa',root)}];report[KEY]=p

def run_native(r,co,pristine,w,uv='uv',jobs=4):
    need(__debug__,'assertions required');rows(r);b=ROOT/BATCH;w=Path(w).resolve();co=Path(co).resolve();pristine=Path(pristine).resolve();env=os.environ.copy();env['PYTHONPATH']=str(ROOT.parent)+os.pathsep+env.get('PYTHONPATH','');env.pop('PYTHONOPTIMIZE',None)
    subprocess.run([sys.executable,str(b/'attempt.py'),'--region',r,'--checkout',str(co),'--pristine',str(pristine),'--manifest',str(b/f'{r}-candidates.json'),'--work',str(w),'--uv',str(uv),'--jobs',str(jobs)],env=env,cwd=ROOT.parent,check=True)
    p=read(w/'summary.json');p.update(base_commit=BASE,source_manifest_sha256=REGIONS[r]['manifest'],compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),expanded_bytes=33554432)
    validate_native(r,p);write(w/'canonical-stage-proof.json',p);return p

def apply(co,base,work,uv,jobs,m,report,rom):
    predecessor(m,rom=rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(3066,210636),'fresh USA predecessor report');project(run_native('usa',co,base,Path(work)/'promo36',uv,jobs),report)

def documents(p,root=ROOT):
    out=frozen('combined',root);project(p,out,root);out['verifier_source_sha256_lf']=sha((root/'verify.py').read_bytes());i=frozen('inventory',root);i['candidate_elf_sha256']=REGIONS['usa']['elf'];i['summary'].update(newly_matching_c=3087,current_unmarked_entries=3100,remaining_assembly_entries=4276);return out,i

def audit_usa(root,m,p,i,historical_verifier_sha=None):
    try:
        need(previous.audit_usa(root,frozen('manifest',root),frozen('combined',root),frozen('inventory',root),historical_verifier_sha=PREDECESSOR_VERIFIER_SHA)['status']=='PASS','historical USA3066 integrity');predecessor(m,root)
        stage=read(proof_path('usa',root));need(p[KEY]==stage,'canonical/dated proof drift');expected,ei=documents(stage,root)
        if historical_verifier_sha is not None: expected['verifier_source_sha256_lf']=historical_verifier_sha
        need(p['status']=='matched' and all(p[k]==expected[k] for k in ('comparison','sources_sha256_lf','retained_assembly_functions','verifier_source_sha256_lf',KEY)),'canonical proof ownership/ROM drift');need(i==ei,'strict inventory drift')
        return {'status':'PASS','accepted_C':3087,'accepted_original_bytes':212412,'remaining_assembly':4276,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as exc:return {'status':'FAIL','errors':[str(exc)]}

JP_KEY='promo36_promotion'
JP_REG='japan_0_3019_promo36.json'
JP_INV='japan_0_3019_promo36_inventory_20261126.json'
JP_FROZEN_SHA='13054ee053168a53d1601db0bea79df3a087626ed84bb15ce4c63fef3b6f479a'

def jp_head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':3004,'new_original_C':15,'accepted_original_C':3019,'accepted_original_bytes':202176,'asm_remaining':4357,'canonical_semantic_relocations':80652,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+proof_path('japan_0').name,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_native('japan_0',p,root);fs=rows('japan_0',root);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':str(BATCH/f['source']),'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs];prior=sorted(prior_names('japan_0',root))
    return {'format':FORMAT,'region':'japan_0','base_c':3004,'matching_c':3019,'assembly_remaining':4357,'original_C_instruction_bytes':202176,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':3004,'matching_c_after':3019,'remaining_assembly':4357,'accepted_original_C_bytes':202176,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80652,'candidate_semantic_relocations':80652,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':REGIONS['japan_0']['prior'],'candidate_elf_sha256':REGIONS['japan_0']['elf'],'previous_C_names':prior,'new_C_names':sorted(f['name'] for f in fs),'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def master_predecessor(m,root=ROOT):
    path=root/'results/japan_0_3004_before_promo36.json';need(sha(path.read_bytes())==JP_FROZEN_SHA,'JP frozen predecessor fingerprint');old=read(path);need(m.get(JP_KEY)==jp_head() and {k:v for k,v in m.items() if k!=JP_KEY}==old,'JP3004 frozen predecessor mismatch');return old
def validate_jp(root=ROOT):
    need(previous.validate_jp(root)['accepted_C']==3004,'historical JP3004 integrity');master_predecessor(read(root/'regions/japan_0.json'),root);p=read(proof_path('japan_0',root));r,i=jp_documents(p,root);need(r==read(root/'regions'/JP_REG) and i==read(root/'results'/JP_INV),'Japan source/inventory drift');return {'status':'PASS','accepted_C':3019,'accepted_original_bytes':202176,'remaining_assembly':4357}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=REGIONS);parser.add_argument('--checkout',type=Path);parser.add_argument('--pristine',type=Path);parser.add_argument('--work',type=Path);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    if a.checkout:
        need(a.region and a.pristine and a.work,'native inputs required');print(json.dumps(run_native(a.region,a.checkout,a.pristine,a.work,a.uv,a.jobs),indent=2))
    else:print(json.dumps(validate_jp(),indent=2))
