"""ROM-free integrity check for separate JP 2,398-C canonical regional proof.

This verifies published evidence consistency, not new native original-ROM proof.
Keep the USA-specific top-level manifest/combined/inventory intact.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json
from . import japan_short28_promotion as jp28

RESULTS=Path(__file__).parent/'results'
REGIONAL=Path(__file__).parent/'regions/japan_0_short28_2398.json'
PROOF=RESULTS/'japan_0_2398_short28_g2_20261123.json'
INVENTORY=RESULTS/'japan_0_2398_short28_inventory_20261123.json'
ORIGINAL=RESULTS/'japan_0_2370_cright_inventory_20261123.json'

def validate():
    proof=json.loads(PROOF.read_text())
    inv=json.loads(INVENTORY.read_text())
    region=json.loads(REGIONAL.read_text())
    before=json.loads(ORIGINAL.read_text())
    rows=jp28.rows()
    names={r['name'] for r in rows}
    offsets={r['name']:r['rom_offset'] for r in rows}
    hashes={r['name']:r['source_sha256'] for r in rows}
    reloc={r['name']:r['native_relocation_count'] for r in rows}
    expected={
        'original_c_before':2370,'candidate_c_after':2398,
        'original_instruction_bytes_before':127008,'added_original_instruction_bytes':1980,
        'original_instruction_bytes_after':128988,'asm_before':5006,'asm_after':4978,
        'original_full_decompressed_bytes':33554432,
        'original_full_decompressed_sha1':jp28.ROM_SHA,
        'original_full_retail_bytes':16777216,
        'original_full_retail_sha1':'9843ee979b5f6c80f5eda85df0baed9ae7c4e73b',
        'elf_positive_func_identities_exact':7376,
        'original_asm_reference_semantic_relocations':80745,
        'candidate_semantic_relocations':80745,
        'original_reference_and_candidate_relocation_sha256':jp28.BASE_RELOC_HASH,
        'full_decompressed_original_rom_byte_exact':True,
        'full_recompressed_original_retail_rom_byte_exact':True,
    }
    for key,value in expected.items():
        if proof.get(key)!=value:raise ValueError('JP2398 G2 evidence mutated '+key)
    if (proof.get('status')!='PASSED_G2_LOCAL' or
        proof.get('region')!='japan_0' or
        proof.get('base_git_sha')!='56e4754255403f012cc9bc88ba39ec1f4fadfb6c' or
        proof.get('local_ci')!='PASS_EXIT_0'):
        raise ValueError('JP2398 regional base/proof/CI status inconsistent')
    if len(proof['functions'])!=28 or {f['name'] for f in proof['functions']}!=names:
        raise ValueError('JP2398 complete C-claim list differs')
    if (proof['preexisting_jp2370_two_synthetic_splat_symbols_review']['new_exceptions_for_short28']!=0 or
        before['candidate_c_after']!=2370 or before['candidate_original_bytes']!=127008 or
        before['candidate_relocations']!=80745 or
        before['independent_and_candidate_sha256']!=jp28.BASE_RELOC_HASH):
        raise ValueError('JP2398 predecessor changed or relocation exceptions widened')
    for key,value in {'total_matching_c':2398,'new_matching_c':28,
                      'total_matching_c_original_instruction_bytes':128988,
                      'remaining_original_asm':4978,
                      'original_elf_positive_func_identities':7376,
                      'preserved_elf_identities':7376,
                      'new_positive_aliases':0,
                      'prior_dual_original_semantic_relocations':80745,
                      'candidate_semantic_relocations':80745,
                      'relocation_multiset_sha256':jp28.BASE_RELOC_HASH,
                      'original_full_rom_exact':True,
                      'retail_full_rom_exact':True}.items():
        if inv.get(key)!=value:raise ValueError('JP2398 inventory mismatch '+key)
    if inv['source_sha256_by_function']!=hashes or inv['original_rom_offsets_by_function']!=offsets or inv['source_native_relocations_by_function']!=reloc:
        raise ValueError('JP2398 source ownership, original offset or relocations stale')
    if (region['accepted_japan_c_after']!=2398 or region['base_accepted_japan_c']!=2370
        or region['accepted_original_bytes_after']!=128988 or region['remaining_original_assembly']!=4978
        or {f['name'] for f in region['functions']}!=names or not region['canonical_usa_manifest_untouched']):
        raise ValueError('JP2398 canonical regional manifest differs')
    if any(r['source_sha256']!=hashes[r['name']] or r['rom_offset']!=offsets[r['name']] for r in region['functions']):
        raise ValueError('JP2398 regional entry/source mismatch')
    return {'status':'PASS','region':'japan_0','canonical_matching_c':2398,
            'new_matching_c':28,'instruction_bytes':128988,'asm_remaining':4978,
            'ELF_identities':7376,'semantic_relocations':80745,'gameplay':'NOT_RUN'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate',action='store_true')
    opt=parser.parse_args()
    if not opt.validate:parser.error('Use --validate to check the stored JP regional proof')
    print(json.dumps(validate(),sort_keys=True))
if __name__=='__main__':main()
