"""Final USA transition-state native C promotion; original ASM dispatch ABI only."""
import json,hashlib
from pathlib import Path
from .research.transition_final_20261124 import verify_usa_3cf0 as replay
ROOT=Path(__file__).resolve().parent
BATCH=replay.B;KEY='usa_transition_final_promotion';FORMAT='goemon-transition-final-usa-original-g2-v1'
NAME=replay.TARGET;SIZE=568;OFF=0x3cf0;VMA=0x800030f0
ORIGINAL='26227d5b03bbb1e1acdd224521eb50efdc312da3218ba9651676dfd442c9d4b1'
FROZEN={'manifest_2324_before_transition_final_20261124.json':'95f3addaf9df44a7da66208aff348a3b2c7202cd3a3fceebf9cc3f10eabfe5ac','combined_2324_before_transition_final_20261124.json':'d5f548064a448f1c5baf38f87e1e47e29069d995c6660b24711defc0590db1b5','inventory_2324_before_transition_final_20261124.json':'8143e5a00e72dba550bff2247b531d181b8aa2971577d8193d434c050ea8c43b'}
FILES={'arg_s32_add.c':replay.SOURCE,'transition.h':replay.HEADER,'verify_usa_3cf0.py':'dd772cca4d27cca61ee5a1c23d34db0f70d8de8e4d7b38abc113121a6e6ae41a','relocation-delta.json':'7e83d0f92485f5757f0050979766d2475896fe83ac4bb2497cc8101d45806205','strict-inventory.json':'3a139b95fb84ceba3aed605c1d63900a18dcf6d85598bf5f0dbd2c445c8071d9'}
PROOF='usa_transition_final_2325_g2_20261124.json'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError('Final transition promotion: '+msg)
def claims():return [{'name':NAME,'rom_offset':OFF,'vma':VMA,'size':SIZE}]
def verify_files():
    for file,h in FILES.items():need(sha((BATCH/file).read_bytes())==h,'source or reference drift '+file)
def frozen(root=ROOT):
    for file,h in FROZEN.items():need(sha((root/'results'/file).read_bytes())==h,'frozen predecessor drift '+file)
    return [read(root/'results'/file) for file in FROZEN]
def validate_predecessor(m,rom=None):
    from . import verify
    verify_files();old,_,_=frozen();need(m.get(KEY)=={'format':FORMAT},'unreviewed stage');need(old=={k:v for k,v in m.items() if k!=KEY},'frozen USA2324 manifest mismatch');rows=verify.claimed_functions(old);need((len(rows),sum(f['size'] for f in rows))==(2324,111852),'predecessor claims');need(not any(x['name']==NAME or x['rom_offset']<OFF+SIZE and OFF<x['rom_offset']+x['size'] for x in rows),'duplicate original owner');
    if rom is not None:need(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==replay.ROM and sha(rom[OFF:OFF+SIZE])==ORIGINAL,'original ROM or target drift')
    return rows

def validate_proof(p):
    verify_files();e={'status':'PASSED_G2_LOCAL','base_commit':replay.BASE,'target':NAME,'source_sha256':replay.SOURCE,'whole_source_sha256':'f9aa77062e4a1897d2c3f4d90b9448cd3ef115a5e0063735615980d248dbfd11','header_sha256':replay.HEADER,'original_bytes':568,'whole_unit_bytes':2256,'pool_bytes':20,'unit_text_relocations':125,'pool_relocations':5,'prior_elf_sha256':replay.PRIOR,'native_elf_sha256':replay.NATIVE,'shadow_elf_sha256':replay.SHADOW,'expanded_sha1':replay.ROM,'retail_sha1':replay.RETAIL,'expanded_bytes':33554432,'retail_bytes':16777216,'function_identities':7376,'stable_globals':26714,'prior_relocations':82098,'native_relocations':82080,'relocation_sha256':'4355f0fb9f6fa47bc6c301ac91b93c97682abb205df57db5052d31fa665a7722','relocation_delta_sha256':FILES['relocation-delta.json'],'inventory':read(BATCH/'strict-inventory.json'),'assembly_caller_contract':{'table_entry_rom':0x59544,'jalr_rom':0x2ca0,'sole_symbol_reference':True,'incoming_a0_overwritten':True,'live_c_callers_or_declarations':0,'historical_c_prototype':'UNKNOWN'},'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'};need(p==e,'native original-reference or caller-boundary proof mismatch');return p

def apply(candidate,baseline,work,uv,jobs,manifest,report,expected):
    validate_predecessor(manifest,expected);result=report['comparison'];need(result['full_rom_match'] and (result['matched_functions'],result['matched_function_bytes'])==(2324,111852),'fresh exact USA2324 predecessor required');proof=validate_proof(replay.run(candidate,baseline,Path(work)/'transition_2325',uv,ROOT/'COMPILER_QUIRKS.md',jobs));result['functions'].append(row());result['claimed_functions']+=1;result['matched_functions']+=1;result['matched_function_bytes']+=SIZE;report['retained_assembly_functions'].remove(NAME);report['sources_sha256_lf'].update(source_hashes());report[KEY]=proof

def row():return {'name':NAME,'size':SIZE,'guest_address':'0x800030F0','rom_offset':'0x3CF0','matched':True,'expected_sha256':ORIGINAL,'candidate_sha256':ORIGINAL}
def source_hashes():return {(BATCH/f).relative_to(ROOT).as_posix():FILES[f] for f in ('arg_s32_add.c','transition.h')}
def audit(root,m,p,i):
    from . import verify,transition_promotion as prior
    try:
        old,op,oi=frozen(root);validate_predecessor(m);need(prior.audit_usa(root,old,op,oi)['status']=='PASS','historical USA2324 gate');stage=validate_proof(p[KEY]);need(stage==read(root/'results'/PROOF),'dated G2 proof drift');c=p['comparison'];oc=op['comparison'];need(p['status']=='matched' and c['full_rom_match'] and (c['matched_functions'],c['claimed_functions'],c['matched_function_bytes'])==(2325,2325,112420) and (c['expected_sha1'],c['candidate_sha1'],c['rom_size'])==(replay.ROM,replay.ROM,33554432),'comparison counts or ROM mismatch');need(c['functions']==oc['functions']+[row()],'historical function proof changed');need(p['sources_sha256_lf']=={**op['sources_sha256_lf'],**source_hashes()},'source hashes drift');need(p['retained_assembly_functions']==[x for x in op['retained_assembly_functions'] if x!=NAME],'retained assembly ownership drift');need(i=={**oi,'candidate_elf_sha256':replay.NATIVE,'summary':stage['inventory']},'strict inventory/ELF drift');rows=verify.claimed_functions(m);need((len(rows),sum(x['size'] for x in rows))==(2325,112420),'claim count mismatch');return {'status':'PASS','accepted_C':2325,'accepted_original_bytes':112420,'remaining_assembly':5038,'errors':[]}
    except (KeyError,ValueError,TypeError,FileNotFoundError) as exc:return {'status':'FAIL','errors':[str(exc)]}
