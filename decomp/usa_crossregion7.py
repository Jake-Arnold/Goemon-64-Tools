"""Fail-closed seven-function JP→USA original-address production candidate.

These 7 sources were isolated-native-exact at original USA MIPS VMAs.
Acceptance is ONLY full canonical 2072→2079 ROM/ELF/relocation G2 plus
strict inventory and full local CI. Never publish this stage on isolated proof.
"""
from __future__ import annotations
from contextlib import contextmanager
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil

from . import overlay_isolated233 as splice

ROOT=Path(__file__).resolve().parent
STAGE=ROOT/'research/usa_crossregion7_20261122'
SRC=STAGE/'sources'
MANIFEST=STAGE/'manifest.json'
FORMAT='goemon-usa-crossregion7-post-2072-v1'
FIXTURE_SHA256='8ea0be51e996f1a907d30a72e46608c6b3e42d9c5cc8f2fc45752efeb8323a68'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
COUNT=7
BYTES=524

def sha(raw:bytes)->str:return hashlib.sha256(raw).hexdigest()


def fixture():
    raw=MANIFEST.read_bytes()
    if sha(raw)!=FIXTURE_SHA256:raise ValueError('Crossregion7 reviewed manifest hash changed')
    f=json.loads(raw)
    if (f.get('format')!=FORMAT or f.get('region')!='usa' or f.get('original_rom_sha1')!=ROM_SHA1
            or f.get('prior_c')!=2072 or f.get('prior_c_bytes')!=92492 or
            f.get('new_functions')!=COUNT or f.get('new_original_bytes')!=BYTES or
            f.get('accepted_after')!=2079 or f.get('accepted_after_bytes')!=93016):
        raise ValueError('Crossregion7 target count / source provenance changed')
    fs=f['functions']
    if len(fs)!=COUNT or sum(x['size'] for x in fs)!=BYTES:
        raise ValueError('Crossregion7 source-count/byte mismatch')
    fields={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','jp_offset','jp_name','original_asm','source_relocations'}
    seen=set(); source_names=set(); ranges=[]
    for x in fs:
        n,o,s=x['name'],x['rom_offset'],x['size']
        if set(x)!=fields or n in seen or x['source'] in source_names or o%4 or s<8 or s%4 or not re.fullmatch('xreg7_00[0-6]',x['source']):
            raise ValueError('Crossregion7 invalid source metadata '+str(n))
        if n != f'func_{x["vma"]:08X}_{o:X}' or any(o<b and a<o+s for a,b in ranges):
            raise ValueError('Crossregion7 original VMAs or ROM ownership overlap '+n)
        if not re.fullmatch('[0-9a-f]{64}',x['source_sha256']) or not re.fullmatch('[0-9a-f]{64}',x['original_code_sha256']):
            raise ValueError('Crossregion7 invalid pin '+n)
        code=(SRC/(x['source']+'.c')).read_bytes()
        if sha(code)!=x['source_sha256'] or b'GLOBAL_ASM' in code:
            raise ValueError('Crossregion7 native C source changed '+n)
        seen.add(n);source_names.add(x['source']);ranges.append((o,o+s))
    for filename,pin in f['headers'].items():
        if filename not in ('probe_common.h','m2c_macros.h') or sha((SRC/filename).read_bytes())!=pin:
            raise ValueError('Crossregion7 native include identity changed '+filename)
    if set(f['headers'])!={'probe_common.h','m2c_macros.h'}:
        raise ValueError('Missing pinned IDO source headers')
    return f


def validate_predecessor(manifest):
    if manifest.get('overlay_crossregion7_stage') != {'format':FORMAT}:
        raise ValueError('Missing unambiguous crossregion7 canonical stage')
    predecessor={k:v for k,v in manifest.items() if k!='overlay_crossregion7_stage'}
    data=fixture()
    # The canonical manifest must be identical to the authenticated branch at
    # the start of this research. A moving HEAD requires an explicit rebase.
    serialized=(json.dumps(predecessor,indent=2)+'\n').encode()
    if sha(serialized)!=data['prior_manifest_sha256']:
        raise ValueError('Crossregion7 predecessor canonical manifest changed; rebase needed')
    from . import verify as native
    prior=native.claimed_functions(predecessor)
    if len(prior)!=2072 or sum(x['size'] for x in prior)!=92492:
        raise ValueError('Crossregion7 predecessor missing accepted C')
    names={x['name'] for x in prior}
    ranges=[(x['rom_offset'],x['rom_offset']+x['size']) for x in prior]
    for f in data['functions']:
        o=f['rom_offset'];s=f['size']
        if f['name'] in names or any(o < end and start < o+s for start,end in ranges):
            raise ValueError('Crossregion7 duplicates canonical C '+f['name'])
    return data


def validate_original_rom(rom:bytes):
    if len(rom)!=0x2000000 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:
        raise ValueError('Crossregion7 wrong original expanded USA ROM')
    f=fixture()
    for row in f['functions']:
        at=row['rom_offset'];s=row['size']
        if sha(rom[at:at+s])!=row['original_code_sha256']:
            raise ValueError('Crossregion7 wrong original function bytes '+row['name'])
    return f


def add_source_headers(checkout:Path):
    for fname in ('probe_common.h','m2c_macros.h'):
        dest=checkout/'src'/fname
        raw=(SRC/fname).read_bytes()
        if dest.exists():
            if dest.read_bytes()!=raw:
                raise ValueError('Unreviewed existing native C header collision: '+fname)
        else:
            dest.write_bytes(raw)

@contextmanager
def source_context():
    # Do not change the canonical isolated241 embedded/ASM ownership map.
    original=splice.EMBEDDED.copy()
    try:
        splice.EMBEDDED.clear()
        # Original func_800363F4 belongs to the already accepted object_flags.c
        # mixed ASM/C owner. Replace its precise GLOBAL_ASM pragma in-place.
        splice.EMBEDDED['func_800363F4_36FF4']='object_flags.c'
        yield
    finally:
        splice.EMBEDDED.clear()
        splice.EMBEDDED.update(original)


def stage(checkout:Path,rom:bytes,fixture_doc:dict):
    add_source_headers(checkout)
    with source_context():
        owners=splice.find_owners(checkout,fixture_doc)
    return owners


def resolve_embedded_owner_header(checkout:Path):
    """Use the owner's already-defined N64 ABI types in the mixed original unit.

    Standalone probe_common.h uses int s32; object_flags.h includes libultra's
    long s32 on MIPS. They are both 32-bit but may not be redeclared together.
    Change only the one include generated for the reviewed new function.
    """
    path=checkout/'src/object_flags.c'
    code=path.read_text()
    anchor='/* Original native C for func_800363F4_36FF4 */\n#include "probe_common.h"'
    if code.count(anchor)!=1:
        raise ValueError('Original object_flags.c embedded C anchor changed')
    code=code.replace(anchor,'/* Original native C for func_800363F4_36FF4 */\n#include "m2c_macros.h"',1)
    path.write_text(code,encoding='utf-8')


def production_exact(baseline:Path,prior_elf:Path,candidate:Path,rom:bytes,plan:dict):
    with source_context():
        # Checks complete native ROM, unchanged 7,376 original positive-sized
        # ELF symbols, all semantic relocation records, and each new C owner.
        proof=splice.verify_link(baseline,prior_elf,candidate,rom,plan)
    return {'status':'PASS','promoted_functions':COUNT,'promoted_bytes':BYTES,
            'accepted_after':2079,'accepted_instruction_bytes':93016,
            'retained_asm':5284,'full_rom_exact':True,
            'full_rom_sha1':ROM_SHA1,
            'original_elf_functions':proof['positive_elf_function_entries'],
            'semantic_relocations_unchanged':True,
            'retained_asm_fragments':proof['retained_ASM_fragments']}
