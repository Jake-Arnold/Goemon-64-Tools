"""Additive USA101/JP93 native promotion, with immutable predecessors.

ROM-free validation authenticates stored source and proof relationships; only
run_native performs a new native acceptance attempt. No original binaries are
stored in this repository. The two regional checkouts must be independent.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys
from . import consolidated_batch_promotion as prior_usa, batch302_promotion as previous
from . import japan_consolidated13_promotion as prior_jp
from . import glitch_g2_promotion as reloc, usa_opening_new2_promotion as symbols
from . import inventory, overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
BATCH=Path('research/wave194_20261125')
KEY='usa_wave194_promotion'
JP_KEY='wave194_promotion'
FORMAT='goemon-wave194-original-ido-v1'
BASE='f16e8f4224501d57359f054bb4e09146ac68f502'
FROZEN={'manifest_2556_before_wave194.json': '02812a65bf121c735cef5d89ca2ffe2922662b43258dfe44614f786bd715383b', 'combined_2556_before_wave194.json': 'a4f34fdff8cbdb7883bac0a9196d21cdb68c8944233e6e28e461a87e6c69f269', 'inventory_2556_before_wave194.json': '8a10a07c435a199e376b3789d23216d86268bd51d67fd4984dee33fd4f3b0660', 'japan_0_2664_before_wave194.json': '045786a7aea71f08c5093cb4694c1f4a0a2388d85013f42c1acd3d8b30b1477c', 'japan_0_2664_batch302_inventory_20261125.json': 'b3a9a6e617000ddc549bbf1ab199cf1d0ffe28688f9ae650d0ce6f93ac6018c9'}
REGIONS={'usa': {'old': 2556, 'added': 101, 'bytes': 12580, 'old_bytes': 144092, 'upstream': 13, 'relocations': 82080, 'after_relocations': 82080, 'globals': 26714, 'manifest': 'd5fc877228cc05324bbdedca2753aae09f068e7f5a17c193e9d0ddb239a54bb4', 'prior': '2e3f1a026ace3822f9db944c92169a6fe7c6083b2b970841c76f3e11b6559151', 'elf': 'e9cfc974970b9012dc276b243430499a166fbed1b7a9f34b591e34998929a3ee', 'rom': '6ea0ed71032ce08fc2745f412d84936382197494', 'retail': 'df8083a54296b8c151917c5333e1c85f014a2a66', 'relocation_sha': '4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722', 'identity': '4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798', 'abs_fixes': 47}, 'japan_0': {'old': 2664, 'added': 93, 'bytes': 12004, 'old_bytes': 155416, 'upstream': 0, 'relocations': 80655, 'after_relocations': 80654, 'globals': 26393, 'manifest': '78f782b74203fa068a13e3fa1be673502c20f955c0cea6d7661a42e0874f4838', 'prior': 'ebe91bd0a279d5e4477303b6f462a0104a43cac3b1a08ac37e073e9f748b47d8', 'elf': 'ad93cd3f7c0d52ef86a91a9358072dc9799efb81752f89bcdb9132ff277b2185', 'rom': '6f8745fecc3a5e7d4918c7a73353eb0726116ded', 'retail': '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b', 'relocation_sha': '7bc07e5036daed61d6bf0d70fe2472705f8d673ef8a9f7ba99eba5c883fd05ce', 'identity': '9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e', 'abs_fixes': 35}}
JP_INV="japan_0_2757_wave194_inventory_20261125.json"
JP_REG="japan_0_2757_wave194.json"

def need(ok,msg):
    if not ok:raise ValueError('Wave194: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,obj):Path(path).write_text(json.dumps(obj,indent=2)+'\n')
def frozen(name,root=ROOT):
    p=root/'results'/name;need(sha(p.read_bytes())==FROZEN[name],'frozen predecessor drift: '+name);return read(p)
def proof_path(r,root=ROOT):return root/'results'/f'{r}_wave194_g2_20261125.json'
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
    return fs

def claims(root=ROOT):return [{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes']} for f in rows('usa',root)]
def predecessor(m,root=ROOT,rom=None):
    from .verify import claimed_functions
    old=frozen('manifest_2556_before_wave194.json',root)
    need(m.get(KEY)=={'format':FORMAT} and old=={k:v for k,v in m.items() if k!=KEY},'USA predecessor manifest drift')
    before=claimed_functions(old);need((len(before),sum(x['size'] for x in before))==(2556,144092),'USA predecessor count')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==REGIONS['usa']['rom'],'USA original ROM')
    upstream=set(frozen('inventory_2556_before_wave194.json',root)['summary']['upstream_unmarked_names'])
    for f in rows('usa',root,rom):
        a=f['rom_offset'];b=a+f['original_bytes'];need(f['name'] not in upstream and not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in before),'existing USA ownership '+f['name'])
    return before

def prior_names(r,root=ROOT):
    if r=='usa':
        from .verify import claimed_functions
        old=frozen('manifest_2556_before_wave194.json',root);inv=frozen('inventory_2556_before_wave194.json',root)
        return {f['name'] for f in claimed_functions(old)}|set(inv['summary']['upstream_unmarked_names'])
    inv=frozen(previous.JP_INV,root);return set(inv['previous_C_names'])|set(inv['new_C_names'])

def validate_native(r,p,root=ROOT):
    cfg=REGIONS[r];fs=rows(r,root);byname={f['name']:f for f in fs};names=set(byname);prior=prior_names(r,root);old=cfg['old']+cfg['upstream'];n=cfg['added'];new=old+n
    need(len(prior)==old and not names&prior,'predecessor C ownership '+r)
    expected={'region':r,'requested':n,'stage':'completed_trial','base_commit':BASE,'source_manifest_sha256':cfg['manifest'],'compiler_sha256':prior_usa.stage.COMPILER_SHA,'prior_elf_sha256':cfg['prior'],'candidate_elf_sha256':cfg['elf'],'expanded_sha1':cfg['rom'],'expanded_bytes':33554432,'retail_sha1':cfg['retail'],'function_identities':7376,'semantic_relocations_before':cfg['relocations'],'semantic_relocations_after':cfg['after_relocations'],'semantic_relocation_sha256':cfg['relocation_sha'],'stable_globals':cfg['globals'],'observed_new_ownership':n,'status':'PASSED_G2_LOCAL','staged':n}
    need(all(p.get(k)==v for k,v in expected.items()),'native proof identity '+r)
    need(all(p.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','globals_exact','ownership_exact')),'native gate failed '+r)
    need(all(p.get(k)==[] for k in ('errors','blocked','function_removed','function_added','relocations_added','globals_removed','globals_added')) and p.get('first_rom_mismatch') is None,'native discrepancies '+r)
    if r=='usa':
        need(p['semantic_relocations_exact'] is True and p['relocations_removed']==[] and p['preserved_original_labels']==[], 'USA relocation/label identity')
    else:
        validate_jp_reference(p)
    native=p['native'];need(len(native)==n and {x['name'] for x in native}==names,'native records '+r)
    for x in native:
        f=byname[x['name']];need(x.get('native_exact') is True and x.get('negative_rejected') is True and 'error' not in x and (x['offset'],x['size'],x['source_sha256'],x['prior_research_outcome'])==(f['rom_offset'],f['original_bytes'],f['source_sha256'],f['compiler_quirk_outcome']),'native source/control '+f['name'])
    need(len(p['guarded_abs_restorations'])==cfg['abs_fixes'] and all(x['code_and_relocations_unchanged'] is True and x['st_info_bytes_changed']==1 and x['compiler_outcome']=='EXISTING_QUIRK_REPRODUCED' for x in p['guarded_abs_restorations']),'guarded ABS metadata evidence')
    need(len(p['known_metadata_restorations'])==(2 if r=='usa' else 0),'known metadata evidence')
    i=p['strict_inventory'];need((i['identified_function_entries'],i['upstream_unmarked_entries'],i['newly_matching_c'],i['current_unmarked_entries'],i['remaining_assembly_entries'],i['extra_positive_alias_entries'],i['size_annotation_differences'],i['function_entry_identity_sha256'])==(7376,old,n,new,7376-new,0,[],cfg['identity']),'strict inventory '+r)
    need(i['upstream_unmarked_names']==sorted(prior) and i['baseline_zero_sized_function_labels_ignored']==i['candidate_zero_sized_function_labels_ignored']==(825 if r=='usa' else 0),'strict inventory identities '+r)
    return p

def validate_jp_reference(p):
    d=['.rel.file_30',0x08004154,'R_MIPS_PC16',0x08004178,'.L08004178_6C8338']
    need(p['semantic_relocations_exact'] is False and p['relocations_removed']==[[d,1]],'JP predecessor relocation delta')
    a=p['preserved_original_labels'];need(len(a)==1 and a[0]['name']==d[-1] and a[0]['owner']=='func_080040B8_6C8278' and a[0]['offset']==192 and a[0]['original_address']==d[3] and a[0]['identity_exact'] is True,'JP original interior label')
    q=p['independent_original_reference'];need(q['status']=='PASS' and q['removed_named_record']==d and q['added_named_records']==[] and q['native_relocation_records_unmodified'] is True and q['no_alias_link_negative_rejected'] is True,'JP independent original reference gate')
    need(q['original_asm_sha256']=='40d6847098fbf15fcd614c161d392a98027dc34b6054d140da8e90adfe43a367' and q['active_asm_sha256']=='8b406b09a818fe13e8ac86d0e5804aab07b97265503852b5bd1c384e955586fd','JP independently extracted source fingerprints')
    links=q['reference_links'];need(len(links)==2,'both reference links required')
    for x,mode,n,h,src in zip(links,['prior_global','original_local'],[80655,80654],[prior_jp.RELOC,REGIONS['japan_0']['relocation_sha']],['cef52c4dcbc9e8e7a614605ff4950f0d5ef7f247fbb043b7e626c707b08a2faf','759c9bdf5b3f27fda9cc2da09aafac1f253eeee293bf384acb385fe98dbe6da4']):
        need((x['mode'],x['relocations'],x['relocation_sha256'],x['source_sha256'],x['expanded_sha1'])==(mode,n,h,src,REGIONS['japan_0']['rom']) and all(x[k] is True for k in ('full_rom_exact','full_relocations_exact','function_identities_exact','stable_globals_exact','label_identity_exact')),'JP independent full-link identity '+mode)

def proof_rows(root=ROOT):return [{'name':f['name'],'size':f['original_bytes'],'guest_address':f'0x{f["vma"]:08X}','rom_offset':f'0x{f["rom_offset"]:X}','matched':True,'expected_sha256':f['code_sha256'],'candidate_sha256':f['code_sha256']} for f in rows('usa',root)]
def source_hashes(root=ROOT):
    return {str(BATCH/f['source']):f['source_sha256'] for f in rows('usa',root)}

def native_report(r,co,w,p,root=ROOT):
    cfg=REGIONS[r];co=Path(co);bd=co/'build'/r;elf=bd/'mnsg.elf';prior=Path(w)/'prior.elf';rom=prior_usa.stage.original(co,r)
    need(sha(elf.read_bytes())==cfg['elf'] and sha(prior.read_bytes())==cfg['prior'],'native ELF fingerprint')
    need((bd/'mnsg.z64').read_bytes()==rom and hashlib.sha1(rom).hexdigest()==cfg['rom'],'native original ROM')
    need(cross._funcs(elf)==cross._funcs(prior) and symbols.stable_globals(elf)==symbols.stable_globals(prior),'independent native recheck')
    before=reloc.all_semantic_relocations(prior);after=reloc.all_semantic_relocations(elf)
    if r=='usa':need(before==after,'USA independent relocation recheck')
    else:
        from collections import Counter
        d=('.rel.file_30',0x08004154,'R_MIPS_PC16',0x08004178,'.L08004178_6C8338')
        need(before[0]-after[0]==Counter({d:1}) and not after[0]-before[0] and before[2]==prior_jp.RELOC,'JP independent original relocation recheck')
        validate_jp_reference(p)
    p.update(base_commit=BASE,source_manifest_sha256=cfg['manifest'],compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),semantic_relocation_sha256=after[2],stable_globals=sum(symbols.stable_globals(elf).values()),retail_sha1=hashlib.sha1((co/f'config/{r}/baserom.z64').read_bytes()).hexdigest(),expanded_bytes=len(rom))
    return p

def run_native(r,co,pristine,w,uv='uv',jobs=4):
    need(__debug__,'optimized Python forbidden for native gates');rows(r);b=ROOT/BATCH;w=Path(w).resolve();co=Path(co).resolve();pristine=Path(pristine).resolve();env=os.environ.copy();env['PYTHONPATH']=str(ROOT.parent)+os.pathsep+env.get('PYTHONPATH','');env.pop('PYTHONOPTIMIZE',None)
    subprocess.run([sys.executable,str(b/'attempt.py'),'--region',r,'--checkout',str(co),'--pristine',str(pristine),'--manifest',str(b/f'{r}-candidates.json'),'--work',str(w),'--uv',str(uv),'--jobs',str(jobs)],env=env,cwd=ROOT.parent,check=True)
    p=native_report(r,co,w,read(w/'summary.json'));validate_native(r,p);write(w/'canonical-stage-proof.json',p);return p

def apply(co,base,work,uv,jobs,m,report,rom):
    predecessor(m,rom=rom);c=report['comparison'];need(c['full_rom_match'] and (c['matched_functions'],c['matched_function_bytes'])==(2556,144092),'fresh USA predecessor report')
    p=run_native('usa',co,base,Path(work)/'wave194',uv,jobs);c['functions']+=proof_rows();c['matched_functions']+=101;c['claimed_functions']+=101;c['matched_function_bytes']+=12580;report['sources_sha256_lf'].update(source_hashes());report['retained_assembly_functions']=[n for n in report['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa')}];report[KEY]=p

def usa_documents(p,root=ROOT):
    validate_native('usa',p,root);old=frozen('combined_2556_before_wave194.json',root);i=frozen('inventory_2556_before_wave194.json',root);c=old['comparison'];c['functions']+=proof_rows(root);c['matched_functions']+=101;c['claimed_functions']+=101;c['matched_function_bytes']+=12580;old['sources_sha256_lf'].update(source_hashes(root));old['retained_assembly_functions']=[n for n in old['retained_assembly_functions'] if n not in {f['name'] for f in rows('usa',root)}];old[KEY]=p
    i['candidate_elf_sha256']=REGIONS['usa']['elf'];i['summary'].update(newly_matching_c=2657,current_unmarked_entries=2670,remaining_assembly_entries=4706)
    return old,i

def audit_usa(root,m,p,i):
    try:
        prior=frozen('manifest_2556_before_wave194.json',root);op=frozen('combined_2556_before_wave194.json',root);oi=frozen('inventory_2556_before_wave194.json',root)
        need(previous.audit_usa(root,prior,op,oi)['status']=='PASS','historical USA2556 integrity');predecessor(m,root)
        stage=read(proof_path('usa',root));need(p[KEY]==stage,'canonical/dated native proof drift');expected,ei=usa_documents(stage,root)
        # The verifier emits new invocation metadata, but immutable ownership and
        # complete original-ROM comparison must be identical to the projection.
        need(p['status']=='matched' and all(p[k]==expected[k] for k in ('comparison','sources_sha256_lf','retained_assembly_functions',KEY)),'canonical proof ownership/ROM drift')
        need(i==ei,'strict full-original inventory drift');return {'status':'PASS','accepted_C':2657,'accepted_original_bytes':156672,'remaining_assembly':4706,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as e:return {'status':'FAIL','errors':[str(e)]}

def jp_head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2664,'new_original_C':93,'accepted_original_C':2757,'accepted_original_bytes':167420,'asm_remaining':4619,'canonical_semantic_relocations':80654,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+proof_path('japan_0').name,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_native('japan_0',p,root);fs=rows('japan_0',root);rr=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':str(BATCH/f['source']),'source_sha256':f['source_sha256'],'original_sha256':f['code_sha256']} for f in fs];prior=sorted(prior_names('japan_0',root))
    return {'format':FORMAT,'region':'japan_0','base_c':2664,'matching_c':2757,'assembly_remaining':4619,'original_C_instruction_bytes':167420,'functions':rr},{'format':FORMAT,'region':'japan_0','base_c':2664,'matching_c_after':2757,'remaining_assembly':4619,'accepted_original_C_bytes':167420,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80654,'candidate_semantic_relocations':80654,'same_independent_original_semantic_relocations':True,'prior_globalized_semantic_relocations':80655,'independent_original_reference':p['independent_original_reference'],'full_original_G2':True,'predecessor_elf_sha256':REGIONS['japan_0']['prior'],'candidate_elf_sha256':REGIONS['japan_0']['elf'],'previous_C_names':prior,'new_C_names':sorted(f['name'] for f in fs),'strict_readelf_summary':p['strict_inventory'],'new_C_functions':rr}
def master_predecessor(m,root=ROOT):
    need(m.get(JP_KEY)==jp_head() and {k:v for k,v in m.items() if k!=JP_KEY}==frozen('japan_0_2664_before_wave194.json',root),'JP2664 frozen predecessor mismatch');return frozen('japan_0_2664_before_wave194.json',root)

def validate_jp(root=ROOT):
    need(previous.validate_jp(root)['accepted_C']==2664,'historical JP2664 integrity');m=read(root/'regions/japan_0.json');
    if 'promo36_promotion' in m:
        from . import promo36_promotion as successor36
        m=successor36.master_predecessor(m,root)
    if 'promo367_promotion' in m:
        from . import promo367_promotion as successor367
        m=successor367.master_predecessor(m,root)
    need(m.pop(JP_KEY,None)==jp_head() and m==frozen('japan_0_2664_before_wave194.json',root),'Japan canonical master drift');p=read(proof_path('japan_0',root));r,i=jp_documents(p,root);need(r==read(root/'regions'/JP_REG) and i==read(root/'results'/JP_INV),'Japan source/inventory drift');return {'status':'PASS','accepted_C':2757,'accepted_original_bytes':167420,'remaining_assembly':4619}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--region',choices=REGIONS);parser.add_argument('--checkout',type=Path);parser.add_argument('--pristine',type=Path);parser.add_argument('--work',type=Path);parser.add_argument('--uv',default='uv');parser.add_argument('--jobs',type=int,default=4);a=parser.parse_args()
    if a.checkout:
        need(a.region and a.pristine and a.work,'native inputs required');p=run_native(a.region,a.checkout,a.pristine,a.work,a.uv,a.jobs);print(json.dumps(p,indent=2))
    else:print(json.dumps(validate_jp(),indent=2))
