"""JP2843 dispatcher promotion: source-pinned native and strict inventory evidence."""
from pathlib import Path
import hashlib,json
from . import promo367_promotion as previous
from .consolidated_batch_promotion import FLAGS
ROOT=Path(__file__).resolve().parent
KEY='dispatcher_promotion'
FORMAT='goemon-jp-dispatcher-original-ido-v1'
FROZEN='results/japan_0_2842_before_dispatcher.json'
PROOF='results/japan_0_2843_dispatcher_g2_20261125.json'
REG='regions/japan_0_2843_dispatcher.json'
INV='results/japan_0_2843_dispatcher_inventory_20261125.json'
BATCH='research/jp_dispatcher_20261125/'
NAME='func_80001FE0_2BE0'
SOURCE='726d1a127d44f9141217260104e2587f01174cdc78c4981a6164d8b8f3d96b3a'
NEGATIVE='bf4972ecaceaad4108a552f16e7f09609a8990bded4c09dfc4eddf89a38a93f1'
HEADER='8f7de327cfe734c25c69ba97e93fae7620a5b9a414a32241c0756884e141e616'
CODE='b9fb4d42ce7d73da6bf609ad97073c0309c52d0f40cd0ae14a391e215bba7f4a'
PRIOR='49e6afe39bc1146bbcfc7e268f7a349a066ffa0d0dea7cf9882cccf4084cd290'
NEW='5f1f7536e8b03a6911a35e09dcf92dced675c7aab5e0c63fea4f7d4adc4725a9'
SHADOW='64f6a440f0b8f1ab79b6b1a4e6fe948237c31449c1b2ea881a39f2cfea573ffa'
RELOC='a4094a4a38467b3f5369dd6d123a0194d43a0fb0be8dbf50a005395b6cb67354'
DELTA=[['.rel.main',2147491880,'R_MIPS_HI16',241108,'D_3ADD4'],['.rel.main',2147491888,'R_MIPS_LO16',241108,'D_3ADD4']]
def read(p):return json.loads(p.read_text())
def need(ok,msg):
    if not ok:raise ValueError('JP dispatcher: '+msg)
def head():return {'format':FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2842,'new_original_C':1,'accepted_original_C':2843,'accepted_original_bytes':178160,'asm_remaining':4533,'canonical_semantic_relocations':80652,'full_original_elf_identities':7376,'source_manifest':'decomp/'+REG,'proof':'decomp/'+PROOF,'inventory':'decomp/'+INV}
def master_predecessor(m,root=ROOT):
    if "promo195_promotion" in m:
        from . import promo195_promotion as successor
        m=successor.master_predecessor(m,root)
    b=(root/FROZEN).read_bytes();need(hashlib.sha256(b).hexdigest()=='cfed25697349af7f79d3ea63bf819bb91fbf5374bf47c53fd67b2f2d3d07f336','frozen predecessor drift');old=json.loads(b);need(m.get(KEY)==head() and {k:v for k,v in m.items() if k!=KEY}==old,'master drift');return old
def prior_names(root=ROOT):
    p=read(root/'results'/previous.JP_INV);names=set(p['previous_C_names'])|set(p['new_C_names']);need(len(names)==2842 and NAME not in names,'prior ownership');return sorted(names)
def validate_native(p,root=ROOT):
    for n,h in [('candidate.c',SOURCE),('negative.c',NEGATIVE),('jp_transition.h',HEADER)]:need(hashlib.sha256((root/BATCH/n).read_bytes()).hexdigest()==h,'source drift '+n)
    expect={'status':'PASSED_G2_LOCAL','stage':'complete','region':'japan_0','target':NAME,'original_offset':11232,'vma':2147491808,'size':120,'source_sha256':SOURCE,'negative_sha256':NEGATIVE,'header_sha256':HEADER,'original_code_sha256':CODE,'flags':FLAGS,'prior_elf_sha256':PRIOR,'prior_relocation_count':80654,'prior_relocation_sha256':'7bc07e5036daed61d6bf0d70fe2472705f8d673ef8a9f7ba99eba5c883fd05ce','original_named_relocations':6,'independent_numeric_relocations':4,'isolated_reference_delta':[[72,'R_MIPS_HI16','D_3ADD4'],[80,'R_MIPS_LO16','D_3ADD4']],'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','active_owner':'asm/japan_0/wave194_050_000.s','active_owner_range':[11232,11352],'shadow_elf_sha256':SHADOW,'shadow_relocation_count':80652,'shadow_relocation_sha256':RELOC,'removed_original_reference_records':DELTA,'expanded_sha1':'6f8745fecc3a5e7d4918c7a73353eb0726116ded','expanded_bytes':33554432,'retail_sha1':'9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','retail_bytes':16777216,'function_identities':7376,'stable_globals':26393,'candidate_relocations':80652,'semantic_relocation_sha256':RELOC,'candidate_elf_sha256':NEW,'canonical_delta':0}
    for k,v in expect.items():need(p.get(k)==v,'native proof '+k)
    for k in ('native_positive_exact','native_negative_rejected','shadow_full_rom_exact','expanded_rom_exact','retail_rom_exact','function_identity_exact','globals_exact','semantic_relocations_exact','ownership_exact'):need(p.get(k) is True,'failed gate '+k)
    i=p['strict_inventory'];need(i=={'identified_function_entries':7376,'upstream_unmarked_entries':2842,'newly_matching_c':1,'current_unmarked_entries':2843,'remaining_assembly_entries':4533,'baseline_zero_sized_function_labels_ignored':0,'candidate_zero_sized_function_labels_ignored':0,'extra_positive_alias_entries':0,'upstream_unmarked_names':prior_names(root),'size_annotation_differences':[],'function_entry_identity_sha256':'9eaf3e7abf903df6256cdfe306330e99daf3f827c5ae828ebcb0ac549811f43e'},'strict inventory drift')
    return p
def documents(p,root=ROOT):
    validate_native(p,root);f={'name':NAME,'rom_offset':11232,'vma':2147491808,'size':120,'source':BATCH+'candidate.c','source_sha256':SOURCE,'original_sha256':CODE}
    return {'format':FORMAT,'region':'japan_0','base_c':2842,'matching_c':2843,'assembly_remaining':4533,'original_C_instruction_bytes':178160,'functions':[f]},{'format':FORMAT,'region':'japan_0','base_c':2842,'matching_c_after':2843,'remaining_assembly':4533,'accepted_original_C_bytes':178160,'original_positive_elf_count':7376,'independent_original_semantic_relocations':80652,'candidate_semantic_relocations':80652,'same_independent_original_semantic_relocations':True,'prior_named_semantic_relocations':80654,'independent_reference_delta':DELTA,'full_original_G2':True,'predecessor_elf_sha256':PRIOR,'candidate_elf_sha256':NEW,'previous_C_names':prior_names(root),'new_C_names':[NAME],'strict_readelf_summary':p['strict_inventory'],'new_C_functions':[f]}
def validate(root=ROOT):
    master_predecessor(read(root/'regions/japan_0.json'),root);need(previous.validate_jp(root)['accepted_C']==2842,'historical JP2842 integrity');r,i=documents(read(root/PROOF),root);need(r==read(root/REG) and i==read(root/INV),'source/inventory drift');return {'status':'PASS','accepted_C':2843,'accepted_original_bytes':178160,'remaining_assembly':4533}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
