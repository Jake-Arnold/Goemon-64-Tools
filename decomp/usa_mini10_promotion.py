"""Fail-closed USA Mini 10-function native-C promotion after canonical USA2079.

Preserves original ASM, other accepted C, and full 32MiB ROM/ELF/relocations.
Actual acceptance requires complete verifier + strict inventory + full local CI.
"""
from __future__ import annotations
from contextlib import contextmanager
from collections import Counter
from pathlib import Path
import hashlib,json

from . import overlay_isolated233 as splice
from . import overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/usa_mini10_20261123'
SRC=DIR/'sources'
FORMAT='goemon-usa-mini10-post2079-v1'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
PRIOR_SHA256='10a1a4623e012fe93968ea83372718c39972f040c8bea9434afd758ea61ba3f5'
FIXTURE_SHA256='6b3d4f26ee771228b484e2aff304afa24a04bba9ec0e6de315144d1568ef307a'
COUNT=10
BYTES=1268
EXPECTED_NAMES={
    'func_801E28D8_59E7E8':68,
    'func_801E31DC_59F0EC':104,
    'func_801E3278_59F188':92,
    'func_801E2180_59E090':160,
    'func_801E2220_59E130':68,
    'func_801E2800_59E710':176,
    'func_801E2AA0_59E9B0':180,
    'func_801E2BA8_59EAB8':168,
    'func_801E2CEC_59EBFC':64,
    'func_801E2D74_59EC84':188,
}
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()


def fixture():
    raw=(DIR/'manifest.json').read_bytes()
    if sha(raw)!=FIXTURE_SHA256:raise ValueError('Mini10 immutable fixture hash changed')
    d=json.loads(raw)
    if (d.get('format'),d.get('region'),d.get('prior_count'),d.get('prior_bytes'),d.get('original_rom_sha1')) != (FORMAT,'usa',2079,93016,ROM_SHA1):
        raise ValueError('Mini10 predecessor and original-USA hash changed')
    fs=d['functions']
    if (len(fs)!=COUNT or sum(f['size'] for f in fs)!=BYTES or
            {f['name']:f['size'] for f in fs}!=EXPECTED_NAMES or
            len({f['rom_offset'] for f in fs})!=COUNT or
            any(f['original_asm']!='file_11' for f in fs)):
        raise ValueError('Mini10 unexpected count, duplicate function or original ASM owner')
    seen=set();last=-1
    for f in fs:
        if set(f)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','original_asm'}:
            raise ValueError('Mini10 source metadata unreviewed')
        n,o,v,s=f['name'],f['rom_offset'],f['vma'],f['size']
        if (n!=f'func_{v:08X}_{o:X}' or o<last or o%4 or s%4 or
                f['source'] in seen or not f['source'].startswith('mini_')):
            raise ValueError('Mini10 invalid original function address/source')
        last=o+s;seen.add(f['source'])
        data=(SRC/(f['source']+'.c')).read_bytes()
        if sha(data)!=f['source_sha256'] or b'GLOBAL_ASM' in data:
            raise ValueError('Mini10 original native C source modified: '+n)
    return d


def validate_predecessor(manifest,reference_rom:bytes|None=None):
    from . import verify
    d=fixture()
    if manifest.get('overlay_mini10_stage') is not None:
        if manifest['overlay_mini10_stage'] != {'format':FORMAT}:
            raise ValueError('Mini10 unsupported canonical stage')
        prior={k:v for k,v in manifest.items() if k!='overlay_mini10_stage'}
    else:prior=manifest
    pinned=sha((json.dumps(prior,indent=2)+'\n').encode())
    if pinned!=PRIOR_SHA256:raise ValueError('Mini10 current canonical predecessor differs; require rebase')
    claims=verify.claimed_functions(prior)
    if len(claims)!=2079 or sum(f['size'] for f in claims)!=93016:
        raise ValueError('Mini10 requires 2079 accepted-C predecessor')
    old={f['name'] for f in claims};ranges=[(f['rom_offset'],f['rom_offset']+f['size']) for f in claims]
    for f in d['functions']:
        o=f['rom_offset'];e=o+f['size']
        if f['name'] in old or any(o<hi and lo<e for lo,hi in ranges):
            raise ValueError('Mini10 already canonical or overlap: '+f['name'])
    if reference_rom is not None:
        if len(reference_rom)!=33554432 or hashlib.sha1(reference_rom).hexdigest()!=ROM_SHA1:
            raise ValueError('Mini10 original USA ROM mismatch')
        for f in d['functions']:
            o,s=f['rom_offset'],f['size']
            if sha(reference_rom[o:o+s])!=f['original_code_sha256']:
                raise ValueError('Mini10 original code range changed: '+f['name'])
    return d

@contextmanager
def source_context():
    saved=splice.EMBEDDED.copy()
    try:
        splice.EMBEDDED.clear()
        yield
    finally:
        splice.EMBEDDED.clear();splice.EMBEDDED.update(saved)

def prove_combined(baseline,prior_elf,candidate,reference_rom,plan):
    with source_context():
        result=splice.verify_link(baseline,prior_elf,candidate,reference_rom,plan)
    original_relocs=cross._relocations(prior_elf)
    updated_relocs=cross._relocations(Path(candidate)/'build/usa/mnsg.elf')
    if (set(original_relocs)!=set(updated_relocs) or
        any(Counter(original_relocs[k])!=Counter(updated_relocs[k]) for k in original_relocs)):
        raise ValueError('Mini10 changed semantic relocations')
    if sum(map(len,original_relocs.values()))!=67152:
        raise ValueError('Mini10 overlay relocation baseline changed')
    # Compare every .rel section, including the 14,945 main + six entry
    # records deliberately omitted by cross._relocations' file_N parser.
    from .glitch_g2_promotion import all_semantic_relocations
    prev_all,nprev,prev_sha=all_semantic_relocations(prior_elf)
    new_all,nnew,new_sha=all_semantic_relocations(Path(candidate)/'build/usa/mnsg.elf')
    if nprev!=82103 or nnew!=82103 or prev_all!=new_all:
        raise ValueError('Mini10 all 82,103 semantic relocations differ')
    return {'status':'PASSED_G2_LOCAL','added_functions':COUNT,'added_bytes':BYTES,
            'after_c':2089,'after_instruction_bytes':94284,'remaining_asm':5274,
            'rom_bytes':result['rom_bytes'],'rom_sha1':result['sha1'],
            'positive_elf_identities':result['positive_elf_function_entries'],
            'semantic_relocations_unchanged':True,
            'original_semantic_relocations':82103,
            'all_semantic_relocations_sha256':prev_sha,
            'all_semantic_relocations_identical':True,
            'original_file11_relocations':len(original_relocs['file_11']),
            'old_ASM_slices_retained':result['retained_ASM_fragments']}
