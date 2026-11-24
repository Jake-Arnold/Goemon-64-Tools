"""Fail-closed stored JP2534 source/proof/inventory consistency.

This is not a replacement for fresh native proof or full local CI.
"""
import json
from . import japan_cright6_promotion as stage

ROOT=stage.ROOT
REGIONAL=ROOT/'regions/japan_0_cright6_2534.json'
PROOF=ROOT/'results/japan_0_2534_cright6_g2_20261124.json'
INVENTORY=ROOT/'results/japan_0_2534_cright6_inventory_20261124.json'


def validate_documents(head, regional, proof, inventory):
    prior=stage.previous_names();fs=stage.rows();names={f['name'] for f in fs}
    require=stage.require
    expected={'status':'PASSED_G2_LOCAL','region':stage.REGION,'base_commit':stage.BASE,'before_C':2528,'after_C':2534,'added_C':6,'added_bytes':624,'original_bytes_after':138028,'asm_remaining':4842,'rom_bytes':33554432,'rom_sha1':stage.ROM_SHA,'retail_bytes':16777216,'retail_sha1':stage.RETAIL_SHA,'retail_ROM_exact':True,'full_ROM_exact':True,'elf_identities_exact':7376,'semantic_relocations_exact':80745,'semantic_relocations_sha256':stage.RELOC_SHA,'stable_global_symbol_identities_exact':26393,'source_manifest_sha256':stage.MANIFEST_SHA,'predecessor_elf_sha256':stage.PREDECESSOR_ELF,'candidate_elf_sha256':stage.RESEARCH_ELF,'ownership_exact':True,'new_C_names':sorted(names),'compiler_sha256':stage.COMPILER_SHA,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED','gameplay':'NOT_RUN'}
    require(all(proof.get(k)==v for k,v in expected.items()),'complete native G2 proof mismatch')
    fix=proof.get('abs_metadata_fix',{})
    require(fix.get('symbol')=='D_3B03C' and fix.get('undefined_size')==0 and fix.get('st_info_bytes_changed')==1 and fix.get('code_and_relocations_unchanged') is True,'guarded original ABS metadata evidence mismatch')
    expected_rows=[{'name':f['name'],'rom_offset':f['rom_offset'],'vma':f['vma'],'size':f['original_bytes'],'source':(stage.BATCH/f['source']).relative_to(ROOT).as_posix(),'source_sha256':f['source_sha256'],'original_code_sha256':f['code_sha256']} for f in fs]
    fields={'format':stage.FORMAT,'region':stage.REGION,'base_c':2528,'matching_c_after':2534,'remaining_assembly':4842,'accepted_original_C_bytes':138028,'original_positive_elf_count':7376,'original_semantic_relocations':80745,'candidate_semantic_relocations':80745,'same_original_semantic_relocations':True,'full_original_G2':True,'predecessor_elf_sha256':stage.PREDECESSOR_ELF,'candidate_elf_sha256':stage.RESEARCH_ELF,'previous_C_names':sorted(prior),'new_C_names':sorted(names),'new_C_functions':expected_rows}
    require(all(inventory.get(k)==v for k,v in fields.items()),'strict inventory/ownership mismatch')
    strict=inventory.get('strict_readelf_summary',{})
    require((strict.get('identified_function_entries'),strict.get('upstream_unmarked_entries'),strict.get('newly_matching_c'),strict.get('current_unmarked_entries'),strict.get('remaining_assembly_entries'),strict.get('size_annotation_differences'))==(7376,2528,6,2534,4842,[]),'strict readelf inventory mismatch')
    require(strict.get('upstream_unmarked_names')==sorted(prior),'strict readelf predecessor ownership mismatch')
    records=proof.get('native_compile_records',[])
    require(len(records)==6 and {x.get('name') for x in records}==names and all(x.get('source_sha256')==next(f['source_sha256'] for f in fs if f['name']==x['name']) and len(x.get('relocations',[]))==next(f['original_relocations'] for f in fs if f['name']==x['name']) for x in records),'full-flags native source/relocation evidence mismatch')
    reg_fields={'format':stage.FORMAT,'region':stage.REGION,'base_c':2528,'matching_c':2534,'assembly_remaining':4842,'original_C_instruction_bytes':138028,'functions':expected_rows}
    require(all(regional.get(k)==v for k,v in reg_fields.items()),'regional manifest mismatch')
    expected_head={'format':stage.FORMAT,'status':'PASSED_G2_LOCAL','base_original_C':2528,'new_original_C':6,'accepted_original_C':2534,'accepted_original_bytes':138028,'asm_remaining':4842,'canonical_semantic_relocations':80745,'full_original_elf_identities':7376,'source_manifest':'decomp/regions/'+REGIONAL.name,'proof':'decomp/results/'+PROOF.name,'inventory':'decomp/results/'+INVENTORY.name}
    require(head==expected_head,'regional master head mismatch')
    return {'status':'PASS','region':stage.REGION,'accepted_C':2534,'new_C':6,'remaining_assembly':4842,'original_bytes':138028,'notice':'Stored proof only; fresh G2 and full CI required separately.'}


def validate():
    head=json.loads((ROOT/'regions/japan_0.json').read_text()).get(stage.KEY)
    if head is None:
        # A research-only stage must not silently leave promotion documents behind.
        stage.require(not any(p.exists() for p in (REGIONAL,PROOF,INVENTORY)),'orphaned JP6 promotion records')
        return {'status':'RESEARCH_ONLY','accepted_C':2528,'new_C':0}
    return validate_documents(head,*(json.loads(p.read_text()) for p in (REGIONAL,PROOF,INVENTORY)))


def main():
    print(json.dumps(validate(),indent=2))

if __name__=='__main__':main()
