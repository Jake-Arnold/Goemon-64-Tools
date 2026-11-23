"""Fail-closed ROM-free source/provenance/verified-G2 integrity for Japan 2,428 matching C.

This validates *stored* original-ROM evidence and original-region ownership; fresh
original-ROM proof must be produced by japan_crossregion30_promotion.build/verify.
"""
from pathlib import Path
import hashlib, json, argparse
from . import japan_crossregion30_promotion as jp
from . import japan_short28_integrity as predecessor

ROOT=Path(__file__).resolve().parent
PROOF=ROOT/'results/japan_0_2428_crossregion30_g2_20261123.json'
INVENTORY=ROOT/'results/japan_0_2428_crossregion30_inventory_20261123.json'
REGIONAL=ROOT/'regions/japan_0_crossregion30_2428.json'
REGION_HEAD=ROOT/'regions/japan_0.json'
RESEARCH=ROOT/'research/crossregion_native34_full_20261123'


def require(test,message):
    if not test:raise ValueError(message)


def validate():
    require(predecessor.validate()['status']=='PASS','JP2398 base integrity failed')
    proof=json.loads(PROOF.read_text())
    inventory=json.loads(INVENTORY.read_text())
    reg=json.loads(REGIONAL.read_text())
    head=json.loads(REGION_HEAD.read_text())
    rows=jp.rows()
    require(len(rows)==30 and sum(r['size'] for r in rows)==1280,'JP30 precise 30 original extents/bytes')
    names={r['name'] for r in rows}
    require(len(names)==30,'duplicate JP30 positive functions')
    blocked=jp.RETAIN_ASM_ABS_RELOCS
    require(len(blocked)==3 and not(names&blocked),'blocked ABS-reloc functions falsely promoted')
    require(len(reg['functions'])==30 and {r['name'] for r in reg['functions']}==names,'source regional entries drift')
    require({r['name'] for r in reg['functions']}==set(proof['target_unique_C_names']),'G2 accepted function names drift')
    require(len(inventory['source_sha256_by_name'])==30,'strict inventory source coverage')
    original=json.loads((RESEARCH/'manifest.json').read_text())
    require(original['function_count']==34 and original['previous_PR_183_reproduced']==5,'source native34 provenance drift')
    for f in reg['functions']:
        source=ROOT/f['source']
        require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest()==f['source_sha256'],f['name']+' original C source SHA drift')
        require(f['source_sha256']==inventory['source_sha256_by_name'][f['name']],'strict inventory C source differs')
        require(f['rom_offset']==inventory['original_rom_offset_by_name'][f['name']],'original offset drift')
        old=next(r for r in rows if r['name']==f['name'])
        require(f['size']==old['size'] and f['rom_offset']==old['rom_offset'] and f['original_code_sha256']==old['original_code_sha256'],'original ROM extent/hash altered')
        require(f['research_source_sha256']==old['source_sha256'],'original isolated native C source provenance drift')
        original_f=next(r for r in original['functions'] if r['region']=='japan_0' and r['name']==f['name'])
        neg=RESEARCH/original_f['negative_source_path']
        require(neg.is_file() and hashlib.sha256(neg.read_bytes()).hexdigest()==original_f['negative_source_sha256'],f['name']+' original native negative control altered')
    native_variants=json.loads((RESEARCH/'canonical_variants/native_negative_evidence.json').read_text())
    require(len(native_variants['negative_controls'])==4,'canonical C variant negative controls missing')
    for neg in native_variants['negative_controls']:
        name=neg['name']
        require(name in names,'canonical variant was not accepted')
        path=RESEARCH/'canonical_variants/negative_controls'/f'{name}.c'
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==neg['negative_sha256'],name+' native control source drift')
        require(neg['original_IDO_native_negative']=='PASS_DIFFERENT_CODE','native negative control did not reject')
    expected={'original_matching_c_before':2398,'new_matching_c':30,'original_matching_c_after':2428,'original_instruction_bytes_before':128988,'new_original_instruction_bytes':1280,'original_instruction_bytes_after':130268,'original_assembly_before':4978,'original_assembly_after':4948,'original_expanded_bytes':33554432,'original_retail_bytes':16777216,'original_elf_function_identical':7376,'original_jp_semantic_relocations':80745,'candidate_jp_semantic_relocations':80745,'canonical_relocation_sha256':jp.BASE_RELOC_HASH,'full_expanded_ROM_exact':True,'full_retail_ROM_exact':True,'semantic_relocation_multiset_equal':True,'function_identity_positive_ELF_equal':True,'local_ci':'PASS_EXIT_0','stable_global_symbol_identities_exact':26393,'metadata_only_absolute_symbol_type_corrections':3}
    for k,v in expected.items():require(proof.get(k)==v,'JP2428 original G2 evidence inconsistent: '+k)
    require(proof['local_ci_provenance'].startswith('FRESH_UNMODIFIED_FULL_PYTHON3_M_DECOMP_LOCAL_CI_PASS_EXIT_0'),'Full canonical CI provenance not verified')
    require(inventory.get('stable_global_symbol_identities_exact')==26393 and inventory.get('metadata_only_absolute_symbol_type_corrections')==3,'Global symbol exact/guard evidence drift')
    require(reg.get('stable_global_symbol_identities_exact')==26393 and reg.get('metadata_only_absolute_symbol_type_corrections')==3 and reg.get('full_local_ci')=='PASS_EXIT_0','Published regional proof gate drift')
    require(proof['status']=='PASSED_G2_LOCAL' and proof['region']=='japan_0','JP2428 original G2 provenance/region invalid')
    require(proof['original_expanded_sha1']==jp.ROM_SHA and proof['original_retail_sha1']=='9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','Original Japanese expanded/retail hash changed')
    for k,v in {'matching_c_after':2428,'new_native_C':30,'remaining_assembly':4948,'accepted_original_C_bytes':130268,'original_positive_elf_count':7376,'original_semantic_relocations':80745,'candidate_semantic_relocations':80745,'same_original_semantic_relocations':True,'full_original_G2':True}.items():require(inventory.get(k)==v,'strict JP2428 inventory mismatch '+k)
    require(set(inventory['retained_original_asm_excluded'])==blocked,'Three original ASM function blockers not preserved')
    require(reg['base_c']==2398 and reg['matching_c']==2428 and reg['assembly_remaining']==4948 and reg['original_C_instruction_bytes']==130268,'regional stage drift')
    h=head.get('crossregion30_native_promotion') or {}
    require(h.get('accepted_original_C')==2428 and h.get('asm_remaining')==4948 and h.get('canonical_semantic_relocations')==80745,'Japanese regional head not updated coherently')
    return {'status':'PASS','region':'japan_0','accepted_C':2428,'new_C':30,'accepted_original_bytes':130268,'ASM_remaining':4948,'ELF_positive_functions':7376,'original_semantic_relocations':80745,'unchanged_USA_accepted_C':2164}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--validate',action='store_true')
    a=p.parse_args()
    if not a.validate:p.error('Pass --validate to check stored source, regional G2 and strict inventory')
    print(json.dumps(validate(),sort_keys=True))

if __name__=='__main__':main()
