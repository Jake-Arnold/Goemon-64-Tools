"""Canonical USA G2 reconciliation of 108 previously staged but not accepted C.

This module is intentionally *not* an isolated-research counter. It can only
extend the published 1,964-C canonical manifest, refuses duplicate names and
ROM ranges, and demands the original whole-ROM, ELF and relocation audit.

Sources are read from existing Git-owned research paths and checked against
both their immutable source hashes and original USA ROM code hashes. The 40-B
func_800108BC_114BC is already accepted in the 1,964-C manifest and MUST NOT
be restaged. No ROM/ASM bytes are included in source-control artifacts.
"""
from __future__ import annotations
from collections import Counter
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from . import overlay_isolated233 as splice
from . import overlay_crossregion47 as cross
from . import verify as native_verify
from .inventory import summarize_inventory
from . import usa_crossregion51_recovered27_g2_promotion as donor27
from . import glitch_g2_promotion as rotation

ROOT = Path(__file__).resolve().parent
DIR = ROOT / 'research/usa_canonical_reconcile108_20261122'
FIXTURE = DIR / 'manifest.json'
FORMAT = 'goemon-usa-canonical-reconcile108-v1'
FIXTURE_SHA256 = '9e683bba6262c7d58c49d1e26bf5970af8686b4c837d54874412edec5ed49abb'
SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
BASE_C = 1964
FINAL_C = 2072
BASE_BYTES = 84708
FINAL_BYTES = 92492
ADDED_C = 108
ADDED_BYTES = FINAL_BYTES - BASE_BYTES
KNOWN_HISTORICAL_ELF_FIX = ('func_8000D3B8_DFB8', 0x8000D3B8, 72, 64)


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fixture() -> dict:
    raw = FIXTURE.read_bytes()
    if digest(raw) != FIXTURE_SHA256:
        raise ValueError('Reconcile108 reviewed fixture changed')
    data = json.loads(raw)
    if (data['format'], data['region'], data['original_rom_sha1'],
            data['predecessor_c_functions'], data['predecessor_c_bytes'],
            data['unique_new_functions'], data['unique_new_instruction_bytes'],
            data['expected_c_functions'], data['expected_c_bytes'],
            data['original_elf_functions'], data['original_semantic_relocations']) != (
            FORMAT, 'usa', SHA1, BASE_C, BASE_BYTES, ADDED_C, ADDED_BYTES,
            FINAL_C, FINAL_BYTES, 7376, 82103):
        raise ValueError('Wrong reviewed reconcile108 identity or count')
    fs = data['functions']
    if (len(fs) != ADDED_C or sum(f['size'] for f in fs) != ADDED_BYTES or
            len({f['name'] for f in fs}) != ADDED_C or
            len({f['rom_offset'] for f in fs}) != ADDED_C or
            sum(f['embedded_owner'] is not None for f in fs) != 12):
        raise ValueError('Reconcile108 duplicate/size/source-ownership drift')
    if data['source_ownership_exception'] != [
            {'name': 'func_800108BC_114BC', 'source_batch': 'cross48',
             'reason': 'already canonical'}]:
        raise ValueError('Missing documented original-name duplicate exception')
    seen_src = {}
    for i, f in enumerate(fs):
        if not set(f) == {'name','rom_offset','vma','size','source','source_sha256',
                          'original_code_sha256','source_path','source_batch','embedded_owner'}:
            raise ValueError('Unreviewed C source metadata fields')
        if int(f['name'].split('_')[-1], 16) != f['rom_offset'] or int(f['name'].split('_')[1], 16) != f['vma']:
            raise ValueError('Reconcile108 mismatched original name/ROM/VMA')
        if f['size'] < 8 or f['size'] % 4 or (i and fs[i-1]['rom_offset']+fs[i-1]['size'] > f['rom_offset']):
            raise ValueError('Overlapping or invalid original instruction bounds')
        if f['source_path'].startswith('/') or '..' in Path(f['source_path']).parts or not f['source_path'].endswith('.c'):
            raise ValueError('Unsafe research source path')
        if f['source'] != Path(f['source_path']).stem or f['embedded_owner'] not in (None,'dialogue_window.c','rotation_angles.c'):
            raise ValueError('Unsafe/incorrect original source ownership')
        source = ROOT / f['source_path']
        if not source.is_file() or digest(source.read_bytes()) != f['source_sha256']:
            raise ValueError('Missing/modified original native source: '+f['name'])
        prior = seen_src.setdefault(f['source'], f['source_sha256'])
        if prior != f['source_sha256']:
            raise ValueError('Source filename collision with different implementation')
    for header in data['headers']:
        p=ROOT/header['source_path']
        if not p.is_file() or digest(p.read_bytes()) != header['sha256']:
            raise ValueError('Missing/modified observed-type header: '+str(p))
    return data


def claimed_previous(manifest: dict) -> list[dict]:
    if manifest.get('overlay_reconcile108_stage') != {'format': FORMAT}:
        raise ValueError('Reconcile108 stage is absent or not reviewed')
    predecessor = {k:v for k,v in manifest.items() if k != 'overlay_reconcile108_stage'}
    data = fixture()
    raw = (json.dumps(predecessor, indent=2) + '\n').encode()
    if digest(raw) != data['predecessor_manifest_sha256']:
        raise ValueError('Previous canonical manifest changed: rebase and redo all G2')
    prev = native_verify.claimed_functions(predecessor)
    compact = sorted((f['name'],f['rom_offset'],f['size']) for f in prev)
    fingerprint = digest(json.dumps(compact,separators=(',',':')).encode())
    if (len(prev),sum(f['size'] for f in prev),fingerprint) != (
            BASE_C,BASE_BYTES,data['predecessor_registry_sha256']):
        raise ValueError('Published predecessor claims changed or lost functions')
    names={f['name'] for f in prev}
    boundaries=sorted((f['rom_offset'], f['rom_offset'] + f['size']) for f in prev)
    for f in data['functions']:
        o,end=f['rom_offset'],f['rom_offset']+f['size']
        if f['name'] in names or any(o < hi and lo < end for lo,hi in boundaries):
            raise ValueError('Reconciled function already canonically accepted/overlaps: '+f['name'])
    if data['source_ownership_exception'][0]['name'] not in names:
        raise ValueError('Source-overlap exclusion is no longer canonically accepted')
    return prev


def validate_source_and_rom(rom: bytes) -> dict:
    data=fixture()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=SHA1:
        raise ValueError('Wrong private original USA expanded ROM')
    for f in data['functions']:
        o=f['rom_offset']
        if digest(rom[o:o+f['size']]) != f['original_code_sha256']:
            raise ValueError('Original USA instructions changed: '+f['name'])
    return data


def prepare_sources(checkout: Path, data: dict) -> Path:
    root = checkout/'build/usa/reconciled108-sources'
    if root.exists():
        raise ValueError('Reconcile108 stage scratch sources already exist')
    root.mkdir(parents=True)
    for f in data['functions']:
        src=ROOT/f['source_path']
        dst=root/(f['source']+'.c')
        if dst.exists():
            if dst.read_bytes()!=src.read_bytes():raise ValueError('Colliding native source '+f['source'])
        else:
            shutil.copyfile(src,dst)
    for h in data['headers']:
        src=ROOT/h['source_path']
        dst=root/src.name
        if dst.exists() or (checkout/'src'/src.name).exists():
            raise ValueError('Unreviewed native header collision: '+src.name)
        shutil.copyfile(src,dst)
        shutil.copyfile(src,checkout/'src'/src.name)
    return root


def embed_reconciled(checkout: Path, data: dict, source_root: Path):
    # This source is already C/ASM mixed in the authenticated upstream. Both
    # introduced C symbols are from the reviewed, byte-matching replacement.
    target=checkout/'src/rotation_angles.c'
    old=target.read_bytes()
    if digest(old) != '80357db43c81ae9d794f95da4e2e836dd9f729f083b3204c5e46d8d641fb947e':
        raise ValueError('Rotation owner changed since pinned original C proof')
    src=ROOT/'research/glitch_g2_20261121/sources/usa_rotation_angles.c'
    replacement=src.read_bytes()
    if digest(replacement) != '72742e59bf097de609062aac468e8dd3a11473939e67134f7853bc6c19050710':
        raise ValueError('Rotation source hash drift')
    for f in data['functions']:
        if f['embedded_owner']=='rotation_angles.c' and f['name'].encode() not in replacement:
            raise ValueError('Missing embedded rotation symbol '+f['name'])
    if b'func_8001FA80_20680.s' not in replacement:
        raise ValueError('Original unrelated rotation ASM removed')
    target.write_bytes(replacement)
    donor27.embed_recovered_dialogue(checkout,data,source_root)


@contextmanager
def isolated_helpers():
    """Restrict changed ASM owner map to this reviewed stage, then restore it."""
    saved_map=splice.EMBEDDED.copy()
    saved_embed=splice.embed_original
    try:
        splice.EMBEDDED.clear()
        splice.EMBEDDED.update({f['name']:f['embedded_owner'] for f in fixture()['functions']
                                if f['embedded_owner']})
        splice.embed_original=embed_reconciled
        yield
    finally:
        splice.EMBEDDED.clear()
        splice.EMBEDDED.update(saved_map)
        splice.embed_original=saved_embed


def validate_elf_and_inventory(baseline: Path, before: Path, candidate: Path,
                               expected: bytes, plan: dict, manifest: dict) -> dict:
    rom=(candidate/'build/usa/mnsg.z64').read_bytes()
    if rom != expected or hashlib.sha1(rom).hexdigest()!=SHA1:
        first=next((i for i,(x,y) in enumerate(zip(rom,expected)) if x!=y),None)
        raise ValueError('FAILED_ROM: reconciled source changed image at '+str(first))
    original=cross._funcs(baseline/'build/usa/mnsg.elf')
    previous=cross._funcs(before)
    actual=cross._funcs(candidate/'build/usa/mnsg.elf')
    if not (sum(original.values())==sum(previous.values())==sum(actual.values())==7376):
        raise ValueError('Original/reconciled ELF function entry count changed')
    # The previous verified source used an 8-byte-too-long annotation for
    # D3B8. The retained Japanese native C source corrects it to the original
    # 64-byte extent, independently observed in the original baseline ELF.
    name,vma,old_size,new_size=KNOWN_HISTORICAL_ELF_FIX
    before_key=(name,vma,old_size)
    original_key=(name,vma,new_size)
    adjusted=Counter(previous)
    if original[original_key]!=actual[original_key] or adjusted[before_key]!=1:
        raise ValueError('Historical D3B8 correction no longer matches original')
    adjusted[before_key]-=1
    if not adjusted[before_key]:del adjusted[before_key]
    adjusted[original_key]+=1
    if adjusted != actual:
        differences=list((adjusted-actual).items())[:5],list((actual-adjusted).items())[:5]
        raise ValueError('Reconcile108 ELF identity drift outside reviewed D3B8 fix: '+repr(differences))
    prev_rel=cross._relocations(before)
    after_rel=cross._relocations(candidate/'build/usa/mnsg.elf')
    orig_rel=cross._relocations(baseline/'build/usa/mnsg.elf')
    if set(prev_rel)!=set(after_rel) or set(orig_rel)!=set(after_rel):
        raise ValueError('Reconcile108 changed relocation sections')
    # Compare every record including symbolic spelling against the accepted
    # canonical predecessor. The original baseline has 14 PRE-EXISTING
    # file_11 alias-name differences (two names and the same guest targets);
    # comparing original vs candidate therefore uses resolved guest address,
    # relocation kind and addend. Check the alias set did not increase.
    def meaning(row):
        # _relocations: (guest_reloc_site, kind, resolved_guest_target,
        #                original_symbol_label, addend)
        return row[0],row[1],row[2],row[4]
    aliases_before=Counter()
    aliases_after=Counter()
    for k in orig_rel:
        if Counter(prev_rel[k])!=Counter(after_rel[k]):
            raise ValueError('Reconcile108 changed accepted canonical relocation labels/records in '+k)
        original_resolved=Counter(map(meaning,orig_rel[k]))
        final_resolved=Counter(map(meaning,after_rel[k]))
        if original_resolved!=final_resolved:
            raise ValueError('Reconcile108 original relocation target/type/addend changed in '+k)
        aliases_before[k]=sum((Counter(orig_rel[k])-Counter(prev_rel[k])).values())
        aliases_after[k]=sum((Counter(orig_rel[k])-Counter(after_rel[k])).values())
    if aliases_before!=aliases_after or aliases_after['file_11']!=14 or sum(aliases_after.values())!=14:
        raise ValueError('Reconcile108 historical symbol-alias exception drift')
    # Cross-overlay helper covers 67,152 of the canonical 82,103 relocation
    # records. The scheduler's *whole-ELF* parser covers all remaining main
    # and data sections. Require exact original-site/type/symbol identities
    # against the predecessor across every one of the 82,103 records.
    from .scheduler4_g2_promotion import relocs as all_relocs
    full_before=all_relocs(before)
    full_after=all_relocs(candidate/'build/usa/mnsg.elf')
    if full_before!=full_after or sum(full_after.values())!=82103:
        raise ValueError('Reconcile108 changed full-ELF 82103 original semantic relocation records')
    if sum(len(x) for x in after_rel.values())!=67152:
        raise ValueError('Wrong cross-overlay relocation subset')
    source_map=(candidate/'build/usa/mnsg.map').read_text()
    symbols=set(actual.elements())
    data=fixture()
    for f in data['functions']:
        owner=(f'build/usa/src/{f["embedded_owner"]}.o' if f['embedded_owner']
               else f'build/usa/src/{f["source"]}.c.o')
        if ((f['name'],f['vma'],f['size']) not in symbols or
            f['name']+'.NON_MATCHING' in source_map or
            owner not in source_map or
            rom[f['rom_offset']:f['rom_offset']+f['size']] != expected[f['rom_offset']:f['rom_offset']+f['size']]):
            raise ValueError('New original C has wrong ELF owner or bytes: '+f['name'])
    old_elf_text=subprocess.check_output(['readelf','-Ws',str(baseline/'build/usa/mnsg.elf')],text=True)
    new_elf_text=subprocess.check_output(['readelf','-Ws',str(candidate/'build/usa/mnsg.elf')],text=True)
    summary=summarize_inventory(old_elf_text,new_elf_text,
                                [f['name'] for f in native_verify.claimed_functions(manifest)])
    if (summary['newly_matching_c'] != FINAL_C or
        summary['remaining_assembly_entries'] != 5291 or
        summary['extra_positive_alias_entries'] or
        summary['identified_function_entries'] != 7376):
        raise ValueError('Reconcile108 strict inventory not accepted: '+repr(summary))
    return {'status':'PASS','function_count':ADDED_C,'original_instruction_bytes':ADDED_BYTES,
            'ROM_sha1':SHA1,'ROM_bytes':len(rom),'ELF_function_count':7376,
            'semantic_relocation_records':82103,
            'historical_symbol_name_aliases_unchanged':dict(aliases_after),
            'original_relocation_target_type_addend_exact':True,
            'canonical_full_relocation_records_unchanged':True,
            'before_c':BASE_C,'after_c':FINAL_C,
            'after_c_instruction_bytes':FINAL_BYTES,'remaining_asm':5291,
            'historical_ELF_size_correction':{'name':name,'previous':old_size,'original':new_size},
            'original_C_sources_from_research':len(data['functions']),
            'strict_inventory':summary}
