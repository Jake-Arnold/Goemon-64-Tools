"""Stored regional source/ROM/inventory consistency; not native proof."""
from pathlib import Path
import json,hashlib
from . import japan_crossregion30_integrity as prior
from . import native251_promotion as stage
ROOT=Path(__file__).resolve().parent

def validate():
    if prior.validate()['status']!='PASS':raise ValueError('JP2428 predecessor integrity')
    fs=stage.rows('japan_0');stage.verify_japan_rows(fs)
    p=json.loads((ROOT/'results/japan_0_2528_native100_g2_20261123.json').read_text())
    i=json.loads((ROOT/'results/japan_0_2528_native100_inventory_20261123.json').read_text())
    r=json.loads((ROOT/'regions/japan_0_native100_2528.json').read_text());h=json.loads((ROOT/'regions/japan_0.json').read_text())['native100_promotion']
    names={x['name'] for x in fs};old=i['previous_C_names'];new=i['new_C_names']
    if len(old)!=2428 or len(set(old))!=2428 or len(new)!=100 or set(new)!=names or set(old)&names:raise ValueError('JP native100 strict source ownership')
    if i['new_C_functions']!=r['functions'] or {x['name'] for x in r['functions']}!=names:raise ValueError('JP native100 inventory/source mismatch')
    for row in r['functions']:
        f=next(x for x in fs if x['name']==row['name'])
        if (row['rom_offset'],row['vma'],row['size'],row['source_sha256'],row['original_code_sha256'])!=(f['rom_offset'],f['vma'],f['original_bytes'],f['source_sha256'],f['code_sha256']) or hashlib.sha256((ROOT/row['source']).read_bytes()).hexdigest()!=row['source_sha256']:raise ValueError('JP native100 original address/source mismatch')
    expected={'status':'PASSED_G2_LOCAL','region':'japan_0','before_C':2428,'after_C':2528,'added_C':100,'added_bytes':7136,'original_bytes_after':137404,'asm_remaining':4848,'rom_bytes':33554432,'rom_sha1':stage.SHA['japan_0'],'retail_sha1':'9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','retail_ROM_exact':True,'elf_identities_exact':7376,'semantic_relocations_exact':80745,'semantic_relocations_sha256':stage.RELOCS['japan_0'][1],'stable_global_symbol_identities_exact':26393,'source_manifest_sha256':stage.MANIFEST_SHA,'ownership_exact':True}
    if any(p.get(k)!=v for k,v in expected.items()):raise ValueError('JP native100 full ROM/ELF/relocation proof mismatch')
    if len(p['abs_metadata_fixes'])!=4 or set(p['new_C_names'])!=names or i['candidate_elf_sha256']!=p['candidate_elf_sha256'] or i['predecessor_elf_sha256']!=p['predecessor_elf_sha256'] or i['matching_c_after']!=2528 or i['remaining_assembly']!=4848 or i['accepted_original_C_bytes']!=137404:raise ValueError('JP native100 strict inventory mismatch')
    if (r['matching_c'],r['assembly_remaining'],h['accepted_original_C'],h['asm_remaining'])!=(2528,4848,2528,4848):raise ValueError('JP native100 regional head mismatch')
    return {'status':'PASS','accepted_C':2528,'new_C':100,'remaining_assembly':4848,'original_bytes':137404}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
