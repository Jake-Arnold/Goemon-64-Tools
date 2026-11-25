"""Additive USA202/JP100 native promotion, with immutable predecessors.

ROM-free validation authenticates stored source and proof relationships; only
run_native performs a new native acceptance attempt. No original binaries are
stored in this repository. The two regional checkouts must be independent.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
from . import consolidated_batch_promotion as prior_usa, japan_consolidated13_promotion as prior_jp
from . import glitch_g2_promotion as reloc, usa_opening_new2_promotion as symbols
from . import inventory, overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
BATCH=Path('research/batch302_20261125')
KEY='usa_batch302_promotion'
JP_KEY='batch302_promotion'
FORMAT='goemon-batch302-original-ido-v1'
BASE='3d7f793af4b616cb4fa72ee180a663e62431d614'
FROZEN={
 'manifest_2354_before_batch302.json':'053c92b900c470e78aefe9e38dd6c018f32ba62aef31cc4b7b0659f0d9b567a8',
 'combined_2354_before_batch302.json':'2c3bc6a84c0863696bbf15f1b8a10531ff5b73689e80c923157da003702bbfbd',
 'inventory_2354_before_batch302.json':'00e30d148f778700a251b022b63409eed9bd7357aed531eb603c7ea544b9d216',
 'japan_0_2564_before_batch302.json':'c43268546ca334574db2c6160df14462fa60862aee670440ad0208ddbd05d562',
 prior_jp.INV:'e4c0d4a5f4f1aa9db4847c141ae7560cecc8a320d90141dde781ec40584419ec',
}
REGIONS={
 'usa':dict(old=2354,added=202,bytes=28300,old_bytes=115792,upstream=13,relocations=82080,globals=26714,manifest='df1f3d38bd284056c4ac783ff71cd61be0971e92816f5a8dcfd40b7d18e8b835',prior=prior_usa.NEW,elf='2e3f1a026ace3822f9db944c92169a6fe7c6083b2b970841c76f3e11b6559151',rom=prior_usa.ROM,retail=prior_usa.RETAIL,relocation_sha='4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722',identity='4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798',abs_fixes=73),
 'japan_0':dict(old=2564,added=100,bytes=13820,old_bytes=141596,upstream=0,relocations=80655,globals=26393,manifest='101a61c4f88f0ea8dc6212a72bbc998e8038099d91c7dee874940b3e31fc2a33',prior=prior_jp.NEW,elf='ebe91bd0a279d5e4477303b6f462a0104a43cac3b1a08ac37e073e9f748b47d8',rom=prior_jp.ROM,retail=prior_jp.RETAIL,relocation_sha=prior_jp.RELOC,identity='9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e',abs_fixes=5),
}
MIXED={'92F0.c':('b84f712eb7d94ebfee8504d8bbca8d18c33c92a7e7f784b05074eff9c8f3d64f',{'func_8000A130_AD30'}),'return_zero.c':('c9baf3357eb19b81b59fed20e23c779420f2bf071be91e15d327d91f08825948',{'func_80023394_23F94','func_80023480_24080','func_800234D8_240D8','func_80023610_24210'})}
JP_INV='japan_0_2664_batch302_inventory_20261125.json'
JP_REG='japan_0_2664_batch302.json'

def need(ok,msg):
    if not ok:raise ValueError('Batch302: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,obj):Path(path).write_text(json.dumps(obj,indent=2)+'\n')
def frozen(name,root=ROOT):
    p=root/'results'/name;need(sha(p.read_bytes())==FROZEN[name],'frozen predecessor drift: '+name);return read(p)
def proof_path(r,root=ROOT):return root/'results'/f'{r}_batch302_g2_20261125.json'
def rows(r,root=ROOT,rom=None):
    cfg=REGIONS[r];b=root/BATCH;p=b/f'{r}-candidates.json';need(sha(p.read_bytes())==cfg['manifest'],'source manifest drift '+r);fs=read(p)
    need((len(fs),sum(f['original_bytes'] for f in fs))==(cfg['added'],cfg['bytes']),'candidate count/bytes '+r)
    names=set();spans=[]
    for f in fs:
        n=f['name'];a=f['rom_offset'];z=f['original_bytes'];v=f['vma'];need(f['region']==r and n not in names and re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',n) is not None and type(v) is int and a>=0 and z>0 and a%4==z%4==0 and a+z<=33554432,'candidate identity '+n)
        if n.startswith('func_'):need(n==f'func_{v:08X}_{a:X}','function address/name '+n)
        need(f['flags']==prior_usa.FLAGS and f['compiler_quirk_outcome'] in ('EXISTING_QUIRK_REPRODUCED','EXISTING_QUIRK_NOT_APPLICABLE','NEW_REPRODUCIBLE_QUIRK','NO_NEW_COMPILER_FINDING'),'compiler evidence '+n)
        for field,h,filename in [('source','source_sha256','candidate.c'),('negative_source','negative_sha256','negative.c')]:
            need(f[field]==f'sources/{r}/{n}/{filename}' and sha((b/f[field]).read_bytes())==f[h],'source drift '+n+' '+field)
        need(f['source_sha256']!=f['negative_sha256'] and re.fullmatch('[a-f0-9]{64}',f['code_sha256']) is not None,'control/code evidence '+n)
        if rom is not None:need(sha(rom[a:a+z])==f['code_sha256'],'original code mismatch '+n)
        names.add(n);spans.append((a,a+z))
    spans.sort();need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'candidate overlaps '+r)
    if r=='usa':
        for file,(h,_) in MIXED.items():need(sha((b/'mixed_units'/file).read_bytes())==h,'integrated mixed source drift '+file)
    return fs

def claims(root=ROOT):return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows('usa',root)]
def predecessor(m,root=ROOT,rom=None):
    from .verify import claimed_functions
    old=frozen('manifest_2354_before_batch302.json',root)
    need(m.get(KEY)=={'format':FORMAT} and old=={k:v for k,v in m.items() if k!=KEY},'USA predecessor manifest drift')
    before=claimed_functions(old);need((len(before),sum(x['size'] for x in before))==(2354,115792),'USA predecessor count')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==REGIONS['usa']['rom'],'USA original ROM')
    upstream=set(frozen('inventory_2354_before_batch302.json',root)['summary']['upstream_unmarked_names'])
    for f in rows('usa',root,rom):
        a=f['rom_offset'];b=a+f['original_bytes'];need(f['name'] not in upstream and not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in before),'existing USA ownership '+f['name'])
    return before

def prior_names(r,root=ROOT):
    if r=='usa':
        from .verify import claimed_functions
        old=frozen('manifest_2354_before_batch302.json',root);inv=frozen('inventory_2354_before_batch302.json',root)
        return {f['name'] for f in claimed_functions(old)}|set(inv['summary']['upstream_unmarked_names'])
    inv=frozen(prior_jp.INV,root);return set(inv['previous_C_names'])|set(inv['new_C_names'])

def validate_native(r,p,root=ROOT):
    cfg=REGIONS[r];fs=rows(r,root);byname={f['name']:f for f in fs};names=set(byname);prior=prior_names(r,root);old=cfg['old']+cfg['upstream'];n=cfg['added'];new=old+n
    need(len(prior)==old and not names&prior,'predecessor C ownership '+r)
    expected={'region':r,'requested':n,'stage':'completed_trial','base_commit':BASE,'source_manifest_sha256':cfg['manifest'],'compiler_sha256':prior_usa.stage.COMPILER_SHA,'prior_elf_sha256':cfg['prior'],'candidate_elf_sha256':cfg['elf'],'expanded_sha1':cfg['rom'],'expanded_bytes':33554432,'retail_sha1':cfg['retail'],'function_identities':7376,'semantic_relocations_before':cfg['relocations'],'semantic_relocations_after':cfg['relocations'],'semantic_relocation_sha256':cfg['relocation_sha'],'stable_globals':cfg['globals'],'observed_new_ownership':n}
    need(all(p.get(k)==v for k,v in expected.items()),'native proof identity '+r)
    need(all(p.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','semantic_relocations_exact','globals_exact','ownership_exact')),'native gate failed '+r)
    need(all(p.get(k)==[] for k in ('errors','blocked','function_removed','function_added','relocations_removed','relocations_added','globals_removed','globals_added')) and p.get('first_rom_mismatch') is None,'native discrepancies '+r)
    mixed=set().union(*(x[1] for x in MIXED.values())) if r=='usa' else set()
    native=p['native'];need(len(native)==n-len(mixed) and {x['name'] for x in native}==names-mixed,'native records '+r)
    for x in native:
        f=byname[x['name']];need(x.get('native_exact') is True and x.get('negative_rejected') is True and 'error' not in x and (x['offset'],x['size'],x['source_sha256'],x['prior_research_outcome'])==(f['rom_offset'],f['original_bytes'],f['source_sha256'],f['compiler_quirk_outcome']),'native source/control '+f['name'])
    if mixed:
        controls=p['mixed_controls'];need(len(controls)==len(mixed) and {x['name'] for x in controls}==mixed,'mixed controls missing')
        for x in controls:
            f=byname[x['name']];need(x['native_exact'] is True and x['negative_rejected'] is True and (x['source_sha256'],x['negative_sha256'])==(f['source_sha256'],f['negative_sha256']),'mixed control '+f['name'])
        units=p['mixed_units'];need(len(units)==2 and {x['unit'] for x in units}=={'src/'+f for f in MIXED},'mixed unit ownership')
        for x in units:
            h,ns=MIXED[Path(x['unit']).name];need(set(x['names'])==ns and x['integrated_source_sha256']==h and x['whole_unit_text_equal'] is True and x['old_text_bytes']==x['new_text_bytes']>0,'mixed unit whole text')
    need(len(p['guarded_abs_restorations'])==cfg['abs_fixes'] and all(x['code_and_relocations_unchanged'] is True and x['st_info_bytes_changed']==1 and x['compiler_outcome']=='EXISTING_QUIRK_REPRODUCED' for x in p['guarded_abs_restorations']),'guarded ABS metadata evidence')
    need(len(p['known_metadata_restorations'])==(2 if r=='usa' else 0),'known metadata evidence')
    i=p['strict_inventory'];need((i['identified_function_entries'],i['upstream_unmarked_entries'],i['newly_matching_c'],i['current_unmarked_entries'],i['remaining_assembly_entries'],i['extra_positive_alias_entries'],i['size_annotation_differences'],i['function_entry_identity_sha256'])==(7376,old,n,new,7376-new,0,[],cfg['identity']),'strict inventory '+r)
    need(i['upstream_unmarked_names']==sorted(prior) and i['baseline_zero_sized_function_labels_ignored']==i['candidate_zero_sized_function_labels_ignored']==(825 if r=='usa' else 0),'strict inventory identities '+r)
    return p

def proof_rows(root=ROOT):return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows('usa',root)]
def source_hashes(root=ROOT):
    ret={str(BATCH/f['source']):f['source_sha256'] for f in rows('usa',root)}
    ret.update({str(BATCH/'mixed_units'/f):h for f,(h,_) in MIXED.items()});return ret

def native_report(r,co,w,p,root=ROOT):
    cfg=REGIONS[r];co=Path(co);bd=co/'build'/r;elf=bd/'mnsg.elf';prior=Path(w)/'prior.elf';rom=prior_usa.stage.original(co,r)
    need(sha(elf.read_bytes())==cfg['elf'] and sha(prior.read_bytes())==cfg['prior'],'native ELF fingerprint')
    need((bd/'mnsg.z64').read_bytes()==rom and hashlib.sha1(rom).hexdigest()==cfg['rom'],'native original ROM')
    need(cross._funcs(elf)==cross._funcs(prior) and symbols.stable_globals(elf)==symbols.stable_globals(prior) and reloc.all_semantic_relocations(elf)==reloc.all_semantic_relocations(prior),'independent native recheck')
    p.update(base_commit=BASE,source_manifest_sha256=cfg['manifest'],compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),semantic_relocation_sha256=reloc.all_semantic_relocations(elf)[2],stable_globals=sum(symbols.stable_globals(elf).values()),retail_sha1=hashlib.sha1((co/f'config/{r}/baserom.z64').read_bytes()).hexdigest(),expanded_bytes=len(rom))
    return p

def run_native(r,co,pristine,w,uv='uv',jobs=4):
    need(__debug__,'optimized Python forbidden for native gates');rows(r);b=ROOT/BATCH;w=Path(w).resolve();co=Path(co).resolve();pristine=Path(pristine).resolve();env=os.environ.copy();env['PYTHONPATH']=str(ROOT.parent)+os.pathsep+env.get('PYTHONPATH','');env.pop('PYTHONOPTIMIZE',None)
    common=['--checkout',str(co),'--pristine',str(pristine)]
    subprocess.run([sys.executable,str(b/'attempt_full_batch.py'),'--region',r,*common,'--manifest',str(b/f'{r}-candidates.json'),'--work',str(w),'--uv',str(uv),'--jobs',str(jobs)],env=env,cwd=ROOT.parent,check=True)
    p=read(w/'summary.json')
    if r=='usa':
        controls=w/'mixed-controls';subprocess.run([sys.executable,str(b/'mixed_controls.py'),*common,'--work',str(controls)],cwd=ROOT.parent,env=env,check=True);p['mixed_controls']=read(controls/'summary.json')
    p=native_report(r,co,w,p);validate_native(r,p);write(w/'canonical-stage-proof.json',p);return p

def apply(co,base,work,uv,jobs,m,report,rom):
    predecessor(m,rom=rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(2354,115792),'fresh USA predecessor report')
    p=run_native('usa',co,base,Path(work)/'batch302',uv,jobs);c['functions']+=proof_rows();c['matched_functions']+=202;c['claimed_functions']+=202;c['matched_function_bytes']+=28300;report['sources_sha256_lf'].update(source_hashes());report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa')}];report[KEY]=p

def usa_documents(p,root=ROOT):
    validate_native('usa',p,root);old=frozen('combined_2354_before_batch302.json',root);i=frozen('inventory_2354_before_batch302.json',root);c=old['comparison'];c['functions']+=proof_rows(root);c['matched_functions']+=202;c['claimed_functions']+=202;c['matched_function_bytes']+=28300;old['sources_sha256_lf'].update(source_hashes(root));old['retained_assembly_functions']=[n for n in old['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa',root)}];old[KEY]=p
    i['candidate_elf_sha256']=REGIONS['usa']['elf'];i['summary'].update(newly_matching_c=2556,current_unmarked_entries=2569,remaining_assembly_entries=4807)
    return old,i

def audit_usa(root,m,p,i):
    try:
        prior=frozen('manifest_2354_before_batch302.json',root);op=frozen('combined_2354_before_batch302.json',root);oi=frozen('inventory_2354_before_batch302.json',root)
        need(prior_usa.audit(root,prior,op,oi)['status']=='PASS','historical USA2354 integrity');predecessor(m,root)
        stage=read(proof_path('usa',root));need(p[KEY]==stage,'canonical/dated native proof drift');expected,ei=usa_documents(stage,root)
        # The verifier emits new invocation metadata, but immutable ownership and
        # complete original-ROM comparison must be identical to the projection.
        need(p['status']=='matched' and all(p[k]==expected[k] for k in ('comparison','sources_sha256_lf','retained_assembly_functions',KEY)),'canonical proof ownership/ROM drift')
        need(i==ei,'strict full-original inventory drift');return {'status':'PASS','accepted_C':2556,'accepted_original_bytes':144092,'remaining_assembly':4807,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as e:return {'status':'FAIL','errors':[str(e)]}

def jp_head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2564,'new_original_C':100,'accepted_original_C':2664,'accepted_original_bytes':155416,'asm_remaining':4712,'canonical_semantic_relocations':80655,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+proof_path('japan_0').name,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_native('japan_0',p,root);fs=rows('japan_0',root);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':str(BATCH/f['source']),'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs];prior=sorted(prior_names('japan_0',root))
    return {'format':FORMAT,'region':'japan_0','base_c':2564,'matching_c':2664,'assembly_remaining':4712,'original_C_instruction_bytes':155416,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':2564,'matching_c_after':2664,'remaining_assembly':4712,'accepted_original_C_bytes':155416,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80655,'candidate_semantic_relocations':80655,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':REGIONS['japan_0']['prior'],'candidate_elf_sha256':REGIONS['japan_0']['elf'],'previous_C_names':prior,'new_C_names':sorted(f['name'] for f in fs),'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def validate_jp(root=ROOT):
    need(prior_jp.validate(root)['accepted_C']==2564,'historical JP2564 integrity');m=read(root/'regions/japan_0.json');
    if 'promo367_promotion' in m:
        from . import promo367_promotion as successor367
        m=successor367.master_predecessor(m,root)
    
    if 'wave194_promotion' in m:
        from . import wave194_promotion as successor
        m=successor.master_predecessor(m,root)
    need(m.pop(JP_KEY,None)==jp_head() and m==frozen('japan_0_2564_before_batch302.json',root),'Japan canonical master drift');p=read(proof_path('japan_0',root));r,i=jp_documents(p,root);need(r==read(root/'regions'/JP_REG) and i==read(root/'results'/JP_INV),'Japan source/inventory drift');return {'status':'PASS','accepted_C':2664,'accepted_original_bytes':155416,'remaining_assembly':4712}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=REGIONS);parser.add_argument('--checkout',type=Path);parser.add_argument('--pristine',type=Path);parser.add_argument('--work',type=Path);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    if a.checkout:
        need(a.region and a.pristine and a.work,'native inputs required');p=run_native(a.region,a.checkout,a.pristine,a.work,a.uv,a.jobs);print(json.dumps(p,indent=2))
    else:print(json.dumps(validate_jp(),indent=2))
