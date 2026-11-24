"""Final additive transition stages. Rebuild from original-address predecessors;
never infer native acceptance from stored metadata. Original inputs stay private.
"""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BATCH=ROOT/'research/transition_state_20261124'
KEY='usa_transition1_promotion'
JP_KEY='transition17_promotion'
FORMAT='goemon-transition-state-original-g2-v1'
BASE='4efacadb87c1d3f14fc082959e280325ccec5185'
MANIFEST_SHA='2900fb0760cc11927c4c51e21291ffe2b8bd9c39c9b411e894d6438c0725869e'
FROZEN={
    'manifest_2323_before_transition_20261124.json':'f08dac2e4fd8da53b918e96269aebe63ed447bd38b709d6d164e0f763e4946c3',
    'combined_2323_before_transition_20261124.json':'ce468fe6d6d59b2130db5bb74ec1365e72a2014523ce083be05bd99946184f8b',
    'inventory_2323_before_transition_20261124.json':'abb8cc739892deedbc3b974efd75f2d01de61fe2543ac8bc6358d5cd5496a17d',
}
USA_PROOF='usa_transition1_2324_g2_20261124.json'
JP_PROOF='japan_0_2551_transition17_g2_20261124.json'
JP_INV='japan_0_2551_transition17_inventory_20261124.json'
JP_REG='japan_0_transition17_2551.json'
JP_PRIOR='japan_0_2534_cright6_inventory_20261124.json'
JP_PRIOR_SHA='0508b494e2da9e2ca5ac2b67daa2ab9c16e27f2a2d99fa2bf599306fe7c27fa5'
LEDGER_BLOB='10313aba367418d71cd6c332086d2d6a9bf83e39'

def sha(data):return hashlib.sha256(data).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError('Transition promotion: '+msg)
def read(p):return json.loads(p.read_text())
def manifest():
    p=BATCH/'promotion_manifest.json';need(sha(p.read_bytes())==MANIFEST_SHA,'source manifest drift')
    doc=read(p);need(doc['base_commit']==BASE,'wrong base')
    for file,h in doc['headers'].items():need(sha((BATCH/file).read_bytes())==h,'header drift '+file)
    for region,fs in [('usa',[doc['usa']]),('japan',doc['japan'])]:
        need((len(fs),sum(f['size'] for f in fs))==((1,116) if region=='usa' else (17,1432)),'wrong regional extent')
        names=set();ranges=[]
        for f in fs:
            name=f['name'];m=re.fullmatch(r'func_([0-9A-F]+)_([0-9A-F]+)',name)
            need(m and (int(m[1],16),int(m[2],16))==(f['vma'],f['rom_offset']) and f['vma']==f['rom_offset']+0x80000000-0xC00,'address drift '+name)
            need(name not in names and f['size']>0 and f['size']%4==0,'duplicate or invalid extent '+name)
            need(sha((BATCH/f['source']).read_bytes())==f['source_sha256'],'source drift '+name);names.add(name);ranges.append((f['rom_offset'],f['rom_offset']+f['size']))
        ranges.sort();need(all(a[1]<=b[0] for a,b in zip(ranges,ranges[1:])),'overlapping target ranges')
    return doc

def claims():
    f=manifest()['usa'];return [{k:f[k] for k in ('name','rom_offset','vma','size')}]
def source_path(f):return (BATCH/f['source']).relative_to(ROOT).as_posix()
def validate_predecessor(m,rom=None):
    from . import verify
    need(m.get(KEY)=={'format':FORMAT},'unreviewed USA stage')
    before={k:v for k,v in m.items() if k!=KEY}
    frozen=ROOT/'results/manifest_2323_before_transition_20261124.json'
    need(sha(frozen.read_bytes())==FROZEN[frozen.name] and before==read(frozen),'frozen USA predecessor manifest mismatch')
    old=verify.claimed_functions(before)
    need((len(old),sum(f['size'] for f in old))==(2323,111736),'wrong USA predecessor count')
    f=manifest()['usa'];a=f['rom_offset'];b=a+f['size']
    need(not any(x['name']==f['name'] or x['rom_offset']<b and a<x['rom_offset']+x['size'] for x in old),'duplicate USA original owner')
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494' and sha(rom[a:b])==f['original_sha256'],'original USA ROM/source drift')
    return old

def previous_jp_names(root=ROOT):
    p=root/'results'/JP_PRIOR;need(sha(p.read_bytes())==JP_PRIOR_SHA,'frozen JP2534 inventory drift');j=read(p)
    names=j['previous_C_names']+j['new_C_names'];need(len(names)==2534 and len(set(names))==2534,'JP predecessor ownership drift');return set(names)

def check_native(region,p):
    """Validate full actual replay metadata, including every ABS relocation delta."""
    m=manifest();usa=region=='usa';fs=[m['usa']] if usa else m['japan'];names=sorted(f['name'] for f in fs)
    exp={'status':'FULL_ROM_EXACT_RESEARCH_NOT_PROMOTED','region':'usa' if usa else 'japan_0','base_commit':BASE,'expanded_rom_bytes':33554432,'retail_rom_bytes':16777216,'expanded_rom_sha1':'6ea0ed71032ce08fc2745f412d84936382197494' if usa else '6f8745fecc3a5e7d4918c7a73353eb0726116ded','retail_rom_sha1':'df8083a54296b8c151917c5333e1c85f014a2a66' if usa else '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','positive_function_identities':7376,'stable_globals':26714 if usa else 26393,'prior_relocations':82102 if usa else 80745,'native_relocations':82098 if usa else 80655,'native_relocation_sha256':'9a8e95185c44f31cf2d4ea5f798f41b4b7a4bb120a1871d86a48d47fcce3a198' if usa else '2ede77ef8e9fa7562cedf148aa11710c8a5f37b24b700bcbb9609be3d12d71f9','prior_elf_sha256':'8cc24cf708723517dfdc2efcd4484dc8695961abfaecf0649bee81e7087d1ade' if usa else 'bac3a17e39eb80c54ab1dfc1a523d060455ab1f91ce0e6e871f242bb77b7b776','candidate_elf_sha256':'efd759f4bf2e7024d695a15998427ab8696a5016c85e5c48c967df8db0d21c7f' if usa else '0bea1f6e25d5c06be5495d488210f49184e4accdf1052ee014c021a352b2f13a','shadow_elf_sha256':'9297864ab77cce310ca022d6f2efe8d99543962d731e250c059004eb30f12983' if usa else '0a4de156ceb9f20e0afd05ce01d7ea3cb76448747f4adc173f3a30ef73d3dcae','independent_shadow_exact':True,'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','new_c_names':names,'removed_original_abs_offset_relocations':m['removed_relocations'][region]}
    if usa:exp.update(target=fs[0]['name'],original_bytes=116,whole_unit_bytes=2256,source_sha256=fs[0]['source_sha256'],header_sha256=m['headers']['usa/transition.h'])
    else:exp.update(before_C=2534,after_C=2551,added_C=17,added_bytes=1432)
    need(all(p.get(k)==v for k,v in exp.items()),'full native original-reference proof mismatch: '+','.join(k for k,v in exp.items() if p.get(k)!=v))
    i=p['inventory'];n0=2336 if usa else 2534;n1=n0+len(fs)
    need((i.get('identified_function_entries'),i.get('upstream_unmarked_entries'),i.get('newly_matching_c'),i.get('current_unmarked_entries'),i.get('remaining_assembly_entries'),i.get('extra_positive_alias_entries'),i.get('size_annotation_differences'))==(7376,n0,len(fs),n1,7376-n1,0,[]),'strict predecessor inventory mismatch')
    need(i.get('function_entry_identity_sha256')==('4875cd876203aa2c1f9a6131ed69c6ec70f0cccb108d497d10caa923f3842798' if usa else '9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e') and i.get('baseline_zero_sized_function_labels_ignored')==i.get('candidate_zero_sized_function_labels_ignored')==(830 if usa else 0),'strict ELF identity drift')
    prior=i['upstream_unmarked_names'];need(len(prior)==n0 and len(set(prior))==n0 and not set(names)&set(prior),'strict predecessor names mismatch')
    if not usa:
        need(set(prior)==previous_jp_names(),'JP predecessor ownership mismatch')
        records=p['source_records'];need(len(records)==17 and {x['name'] for x in records}==set(names),'JP native source record count')
        for f in fs:
            x=next(x for x in records if x['name']==f['name']);need(x['exact'] is True and x['numeric_relocs_equal'] is True and x['size']==f['size'] and x['source_sha256']==f['source_sha256'] and x['original_sha256']==f['original_sha256']==x['linked_sha256'] and x['native_relocs']==f['numeric_relocs'] and x['named_relocs']==f['named_relocs'],'JP source record drift '+f['name'])
    compact={k:v for k,v in p.items() if k not in ('inventory','source_records','full_canonical_CI')}
    compact['strict_predecessor_inventory']={k:v for k,v in i.items() if k!='upstream_unmarked_names'}
    compact['prior_names_sha256']=sha(json.dumps(sorted(prior),separators=(',',':')).encode())
    compact['status']='PASSED_G2_LOCAL';compact['source_manifest_sha256']=MANIFEST_SHA;compact['gameplay']='NOT_RUN'
    return compact

def replay(region,checkout,work,uv,jobs=4):
    # The replay verifies the original ledger prefix. New ledger entries must
    # be reviewed separately before invoking this stage.
    script=BATCH/('verify_usa_454c.py' if region=='usa' else 'verify_japan_17.py')
    subprocess.run([sys.executable,str(script),'--checkout',str(checkout),'--work',str(work),'--uv',str(uv),'--ledger',str(ROOT/'COMPILER_QUIRKS.md'),'--jobs',str(jobs)],cwd=ROOT.parent,check=True)
    return check_native(region,read(Path(work)/'proof.json'))

def apply_usa(candidate,baseline,work,uv,jobs):
    return replay('usa',candidate,Path(work)/'transition_2324',uv,jobs)

def validate_compact(region,p,root=ROOT):
    # Reconstruct the predecessor names from frozen accepted ownership; check
    # exactly the same native metadata constraints without inventing ROM proof.
    m=manifest();usa=region=='usa';fs=[m['usa']] if usa else m['japan']
    if usa:
        from . import verify
        old=verify.load_manifest(root/'results/manifest_2323_before_transition_20261124.json')
        prior=sorted({x['name'] for x in verify.claimed_functions(old)}|set(read(root/'results/inventory_2323_before_transition_20261124.json')['summary']['upstream_unmarked_names']))
    else:prior=sorted(previous_jp_names(root))
    need(p.get('status')=='PASSED_G2_LOCAL' and p.get('source_manifest_sha256')==MANIFEST_SHA and p.get('gameplay')=='NOT_RUN','unreviewed G2 status/source')
    temp={k:v for k,v in p.items() if k not in ('strict_predecessor_inventory','prior_names_sha256','source_manifest_sha256','gameplay')};temp['status']='FULL_ROM_EXACT_RESEARCH_NOT_PROMOTED';temp['inventory']={**p['strict_predecessor_inventory'],'upstream_unmarked_names':prior}
    if not usa:
        records=read(BATCH/'japan/native_replay.json')['rows'];r={x['name']:x for x in records if x['exact']};r.update({x['name']:x for x in read(BATCH/'japan/alias_free_replay.json')['rows']});temp['source_records']=[r[f['name']] for f in fs]
    need(check_native(region,temp)==p,'compact native proof mismatch')
    return p

def jp_head():
    return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2534,'new_original_C':17,'accepted_original_C':2551,'accepted_original_bytes':139460,'asm_remaining':4825,'canonical_semantic_relocations':80655,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+JP_REG,'proof':'decomp/results/'+JP_PROOF,'inventory':'decomp/results/'+JP_INV}
def jp_documents(p,root=ROOT):
    validate_compact('japan',p,root);fs=manifest()['japan'];prior=sorted(previous_jp_names(root));ns=sorted(f['name'] for f in fs)
    rows=[{**{k:f[k] for k in ('name','rom_offset','vma','size','source_sha256','original_sha256')},'source':source_path(f)} for f in fs]
    regional={'format':FORMAT,'region':'japan_0','base_c':2534,'matching_c':2551,'assembly_remaining':4825,'original_C_instruction_bytes':139460,'functions':rows}
    inv={'format':FORMAT,'region':'japan_0','base_c':2534,'matching_c_after':2551,'remaining_assembly':4825,'accepted_original_C_bytes':139460,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80655,'candidate_semantic_relocations':80655,'same_independent_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':p['prior_elf_sha256'],'candidate_elf_sha256':p['candidate_elf_sha256'],'previous_C_names':prior,'new_C_names':ns,'strict_readelf_summary':{**p['strict_predecessor_inventory'],'upstream_unmarked_names':prior},'new_C_functions':rows}
    return regional,inv

def validate_jp(root=ROOT):
    from . import japan_cright6_integrity
    need(japan_cright6_integrity.validate()['status']=='PASS','JP2534 historical integrity')
    head=read(root/'regions/japan_0.json').get(JP_KEY)
    paths=[root/'regions'/JP_REG,root/'results'/JP_PROOF,root/'results'/JP_INV]
    if head is None:
        need(not any(x.exists() for x in paths),'orphaned Japan promotion files');return {'status':'RESEARCH_ONLY','accepted_C':2534}
    need(head==jp_head(),'JP master head mismatch');r,p,i=map(read,paths);er,ei=jp_documents(p,root);need((r,i)==(er,ei),'JP regional manifest/inventory mismatch');return {'status':'PASS','accepted_C':2551,'remaining_assembly':4825,'accepted_original_bytes':139460}

def audit_usa(root,m,p,i):
    from . import verify,promotion_integrity
    try:
        for name,h in FROZEN.items():need(sha((root/'results'/name).read_bytes())==h,'historical USA record drift '+name)
        old=verify.load_manifest(root/'results/manifest_2323_before_transition_20261124.json');op=read(root/'results/combined_2323_before_transition_20261124.json');oi=read(root/'results/inventory_2323_before_transition_20261124.json')
        need(old=={k:v for k,v in m.items() if k!=KEY},'USA predecessor manifest changed');need(promotion_integrity._audit_cright4(root,old,op,oi)['status']=='PASS','USA2323 historical integrity')
        f=manifest()['usa'];stage=p[KEY];validate_compact('usa',stage,root);need(stage==read(root/'results'/USA_PROOF),'USA dated native proof mismatch')
        c=p['comparison'];oc=op['comparison'];s=i['summary'];os=oi['summary'];row={'name':f['name'],'size':116,'guest_address':'0x8000394C','rom_offset':'0x454C','matched':True,'expected_sha256':f['original_sha256'],'candidate_sha256':f['original_sha256']}
        need(p['status']=='matched' and c['full_rom_match'] is True and (c['matched_functions'],c['claimed_functions'],c['matched_function_bytes'])==(2324,2324,111852) and (c['expected_sha1'],c['candidate_sha1'],c['rom_size'])==('6ea0ed71032ce08fc2745f412d84936382197494','6ea0ed71032ce08fc2745f412d84936382197494',33554432),'USA comparison mismatch')
        need(c['functions']==oc['functions']+[row],'USA historical function proof changed')
        oldsrc=op['sources_sha256_lf'];newsrc={**oldsrc,source_path(f):f['source_sha256'],(BATCH/'usa/transition.h').relative_to(ROOT).as_posix():manifest()['headers']['usa/transition.h']}
        need(p['sources_sha256_lf']==newsrc and p['retained_assembly_functions']==[x for x in op['retained_assembly_functions'] if x!=f['name']],'USA source or retained ASM mismatch')
        need((s['newly_matching_c'],s['current_unmarked_entries'],s['remaining_assembly_entries'])==(2324,2337,5039),'USA inventory C count mismatch')
        need(i=={**oi,'candidate_elf_sha256':stage['candidate_elf_sha256'],'summary':{**os,'newly_matching_c':2324,'current_unmarked_entries':2337,'remaining_assembly_entries':5039}},'USA strict inventory/ELF drift')
        need((len(verify.claimed_functions(m)),sum(x['size'] for x in verify.claimed_functions(m)))==(2324,111852),'USA canonical claims mismatch')
        return {'status':'PASS','accepted_C':2324,'accepted_original_bytes':111852,'remaining_assembly':5039,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as exc:return {'status':'FAIL','errors':[str(exc)]}

if __name__=='__main__':
    print(json.dumps(validate_jp(),indent=2))
