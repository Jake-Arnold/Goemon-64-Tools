"""Original-USA file_11 research: verify a third batch of adjacent C islands.

This is an opt-in, read-only native IDO original-VMA probe, not a central G2 or
full-ROM matching-C promotion. It authenticates the user-provided USA ROM and
pinned upstream Splat asm as well as all earlier research candidate identities.
No ROM bytes, generated asm, toolchain outputs or original assets are included.

python3 -m decomp.research.file11_adjacent_wave3_probe \\
  --rom /path/to/usa/baserom.decompressed.z64 \\
  --asm /path/to/usa/asm/usa/587370.s \\
  --cc /path/to/ido-5.3/cc --ld /path/to/mips-linux-gnu-ld \\
  --objcopy /path/to/mips-linux-gnu-objcopy \\
  --report /tmp/unique-goemon-file11-wave3-proof.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from decomp.overlay_file11 import FUNCTIONS as PROMOTED_13, ROM_SHA1, ROM_START, TEXT_END, VMA_START
from decomp.research.file11_adjacent_native_probe import parse_assembly_index
from decomp.research.file11_expansion_probe import native_probe
from decomp.research.usa_file11_noop_groups import entries as promoted_noops

HERE = Path(__file__).parent
SOURCES = HERE / 'file11_adjacent_wave3_sources.json'
DECOMP = HERE.parent
PREVIOUS_77 = DECOMP / 'results/file11_expansion_native_20261116.json'
PREVIOUS_68 = HERE / 'file11_adjacent_sources.json'
PREVIOUS_44 = HERE / 'file11_adjacent_wave2_sources.json'
PINNED_ASM_SHA256 = 'e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b'
PINNED_UPSTREAM = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
FORMAT = 'goemon-file11-adjacent-wave3-source-fixtures-v1'
NEW_FUNCTIONS = 10
NEW_BYTES = 488
GROUPS = 9
GROUP_MEMBERS = 27
GROUP_BYTES = 984
ORIGINAL_ROM_SIZE = 0x2000000
EXPECTED_PREVIOUS = (77, 68, 44)


def digest(data: bytes, algorithm: str = 'sha256') -> str:
    return hashlib.new(algorithm, data).hexdigest()


def previously_identified(prior77: dict, prior68: dict, prior44: dict,
                          original: dict, rom: bytes) -> set[int]:
    """Fail closed if the pinned older candidate inventories are incomplete."""
    if (prior77.get('exact_matching_functions') != 77 or
            prior77.get('exact_matching_bytes') != 2120 or
            len(prior77.get('functions', [])) != 77 or
            prior68.get('format') != 'goemon-file11-adjacent-source-fixtures-v1' or
            len(prior68.get('functions', [])) != 68 or
            prior44.get('format') != 'goemon-file11-adjacent-wave2-source-fixtures-v1' or
            len(prior44.get('functions', [])) != 44):
        raise ValueError('Earlier original-VMA matching-C inventories changed')
    groups = [prior77['functions'], prior68['functions'], prior44['functions']]
    for group in groups:
        for entry in group:
            off, name, size = entry.get('rom_offset'), entry.get('name'), entry.get('size')
            if type(off) is not int or type(size) is not int or original.get(off) != (name, size):
                raise ValueError('Earlier original-USA function identity changed')
            if digest(rom[off:off+size]) != entry.get('original_sha256'):
                raise ValueError('Earlier original-USA function hash changed')
    offsets = [entry['rom_offset'] for rows in groups for entry in rows]
    if len(offsets) != sum(EXPECTED_PREVIOUS) or len(set(offsets)) != len(offsets):
        raise ValueError('Duplicated earlier original-USA research candidate')
    return set(offsets)


def validate_source_contract(fixtures: dict, prior77: dict, prior68: dict,
                             prior44: dict) -> None:
    """ROM-free rejection of duplicate claims, gaps and unreviewed C sources."""
    if (fixtures.get('format') != FORMAT or
            fixtures.get('upstream_commit') != PINNED_UPSTREAM or
            fixtures.get('decompressed_rom_sha1') != ROM_SHA1 or
            fixtures.get('generated_asm_sha256') != PINNED_ASM_SHA256 or
            any(fixtures.get(f'previous_research_{n}_count') != n for n in EXPECTED_PREVIOUS)):
        raise ValueError('Unreviewed third-wave research source contract')
    if (prior77.get('exact_matching_functions') != 77 or
            prior77.get('exact_matching_bytes') != 2120 or
            prior68.get('format') != 'goemon-file11-adjacent-source-fixtures-v1' or
            prior44.get('format') != 'goemon-file11-adjacent-wave2-source-fixtures-v1'):
        raise ValueError('Missing authenticated earlier candidate inventories')
    earlier = [prior77.get('functions'), prior68.get('functions'), prior44.get('functions')]
    if any(not isinstance(x, list) or len(x) != n
           for x, n in zip(earlier, EXPECTED_PREVIOUS)):
        raise ValueError('Earlier function counts changed')
    prior = {r.get('rom_offset') for pool in earlier for r in pool}
    if len(prior) != sum(EXPECTED_PREVIOUS):
        raise ValueError('Overlapping prior research identities')
    promoted = {off for _, off, _, _ in PROMOTED_13}
    promoted.update(off for _, off in promoted_noops())
    if prior & promoted:
        raise ValueError('Research includes already promoted functions')
    rows, groups = fixtures.get('functions'), fixtures.get('adjacent_groups')
    if not isinstance(rows, list) or len(rows) != NEW_FUNCTIONS or not isinstance(groups, list) or len(groups) != GROUPS:
        raise ValueError('Unexpected third-wave source function/group total')
    seen = set()
    old_ownership = {r['rom_offset']:r['size'] for pool in earlier for r in pool}
    old_ownership.update((off,size) for _,off,size,_ in PROMOTED_13)
    old_ownership.update((off,12) for _,off in promoted_noops())
    for r in rows:
        off, size, vma, name = (r.get(k) for k in ('rom_offset','size','vma','name'))
        if (type(off) is not int or type(size) is not int or type(vma) is not int or
                not isinstance(name, str) or off % 4 or size <= 0 or size % 4 or
                not ROM_START <= off < TEXT_END or off+size > TEXT_END or
                vma != VMA_START+off-ROM_START or
                not name.endswith(f'_{off:X}') or
                off in seen or off in old_ownership):
            raise ValueError('Duplicate, unpinned or overlapping new function')
        src, bindings = r.get('source'), r.get('bindings')
        if (not isinstance(src,str) or src.count(name+'(')!=1 or
                'GLOBAL_ASM' in src or '#include' in src or
                not isinstance(bindings,dict) or
                any(not isinstance(k,str) or not isinstance(v,str) or
                    re.fullmatch(r'0x[0-9A-F]{8}',v) is None
                    for k,v in bindings.items())):
            raise ValueError('Unreviewed native C body or external binding')
        seen.add(off)
        old_ownership[off] = size
    if [r['rom_offset'] for r in rows] != sorted(seen) or sum(r['size'] for r in rows)!=NEW_BYTES:
        raise ValueError('Native C function order or size total changed')
    grouped, covered_new = set(), set()
    for g in groups:
        start,end,offsets = (g.get(k) for k in ('start','end','function_offsets'))
        if (type(start) is not int or type(end) is not int or
                not isinstance(offsets,list) or not offsets or offsets != sorted(set(offsets)) or
                start != offsets[0] or end != offsets[-1]+old_ownership.get(offsets[-1],-1) or
                any(off not in old_ownership or off in grouped for off in offsets) or
                any(a+old_ownership[a] != b for a,b in zip(offsets,offsets[1:]))):
            raise ValueError('Unverified or discontinuous native C island')
        if (not isinstance(g.get('source'),str) or
                any(g['source'].count(r['name']+'(') != 1 for r in rows
                    if r['rom_offset'] in offsets) or
                'GLOBAL_ASM' in g['source'] or '#include' in g['source'] or
                not isinstance(g.get('bindings'),dict) or
                any(not isinstance(v,str) or re.fullmatch(r'0x[0-9A-F]{8}',v) is None
                    for v in g['bindings'].values())):
            raise ValueError('Unreviewed combined C island source')
        grouped.update(offsets)
        covered_new.update(off for off in offsets if off in seen)
    if (len(grouped)!=GROUP_MEMBERS or sum(g['end']-g['start'] for g in groups)!=GROUP_BYTES or
            covered_new != seen):
        raise ValueError('Missing source island or duplicate native C function')


def checked_inputs(rom: bytes, assembly: bytes, fixtures: dict,
                   prior77: dict, prior68: dict, prior44: dict):
    validate_source_contract(fixtures, prior77, prior68, prior44)
    if len(rom) != ORIGINAL_ROM_SIZE or digest(rom, 'sha1') != ROM_SHA1:
        raise ValueError('Original USA 32 MiB ROM identity mismatch')
    if digest(assembly) != PINNED_ASM_SHA256:
        raise ValueError('Original pinned 906-function Splat source mismatch')
    if (fixtures.get('format') != FORMAT or
            fixtures.get('upstream_commit') != PINNED_UPSTREAM or
            fixtures.get('decompressed_rom_sha1') != ROM_SHA1 or
            fixtures.get('generated_asm_sha256') != PINNED_ASM_SHA256 or
            any(fixtures.get(f'previous_research_{n}_count') != n for n in EXPECTED_PREVIOUS)):
        raise ValueError('Unreviewed third-wave source contract')
    original = parse_assembly_index(assembly.decode('utf-8'))
    prior = previously_identified(prior77, prior68, prior44, original, rom)
    promoted = {off for _, off, _, _ in PROMOTED_13}
    promoted.update(off for _, off in promoted_noops())
    if prior & promoted:
        raise ValueError('Prior research overlaps already promoted file_11 functions')
    rows, groups = fixtures.get('functions'), fixtures.get('adjacent_groups')
    if not isinstance(rows, list) or len(rows) != NEW_FUNCTIONS or not isinstance(groups, list) or len(groups) != GROUPS:
        raise ValueError('Unexpected new function or adjacent source group count')
    seen = set()
    for row in rows:
        off, name, size, vma = (row.get(key) for key in ('rom_offset','name','size','vma'))
        if (type(off) is not int or type(size) is not int or type(vma) is not int or
                not isinstance(name, str) or off % 4 or size <= 0 or size % 4 or
                not ROM_START <= off < TEXT_END or off + size > TEXT_END or
                off in seen or off in prior or off in promoted or
                original.get(off) != (name, size) or vma != VMA_START + off - ROM_START or
                digest(rom[off:off+size]) != row.get('original_sha256')):
            raise ValueError('Unpinned, duplicate or overlapping new original-USA C function')
        src = row.get('source')
        if (not isinstance(src, str) or src.count(name+'(') != 1 or
                'GLOBAL_ASM' in src or '#include' in src):
            raise ValueError('Unexpected C source declaration or opaque asm')
        bindings = row.get('bindings')
        if (not isinstance(bindings, dict) or
                any(not isinstance(k, str) or not re.fullmatch(r'0x[0-9A-F]{8}', v)
                    for k, v in bindings.items())):
            raise ValueError('Unpinned external original-VMA symbol binding')
        seen.add(off)
    if [r['rom_offset'] for r in rows] != sorted(seen) or sum(r['size'] for r in rows) != NEW_BYTES:
        raise ValueError('C function order or native byte total differs')
    new_by_offset = {r['rom_offset']: r for r in rows}
    original_groups = set()
    new_group_members = set()
    for group in groups:
        start, end, offsets = (group.get(k) for k in ('start','end','function_offsets'))
        if (type(start) is not int or type(end) is not int or not isinstance(offsets, list) or
                not offsets or offsets != sorted(set(offsets)) or start != offsets[0] or
                start < ROM_START or end > TEXT_END or end <= start or
                digest(rom[start:end]) != group.get('original_sha256')):
            raise ValueError('Invalid original-ROM C island extent')
        if any(off not in original or off in original_groups for off in offsets):
            raise ValueError('Unknown or duplicate adjacent C function')
        if (any(off not in prior and off not in promoted and off not in new_by_offset for off in offsets) or
                any(a + original[a][1] != b for a,b in zip(offsets,offsets[1:])) or
                end != offsets[-1] + original[offsets[-1]][1]):
            raise ValueError('Missing intervening assembly in adjacent C island')
        for off in offsets:
            if group.get('source','').count(original[off][0]+'(') != 1:
                raise ValueError('Combined source loses original FUNC identity')
        source, bindings = group.get('source'), group.get('bindings')
        if (not isinstance(source, str) or 'GLOBAL_ASM' in source or '#include' in source or
                not isinstance(bindings, dict) or
                any(not re.fullmatch(r'0x[0-9A-F]{8}', v) for v in bindings.values())):
            raise ValueError('Invalid contiguous C source or external bindings')
        original_groups.update(offsets)
        new_group_members.update(o for o in offsets if o in new_by_offset)
    if (len(original_groups) != GROUP_MEMBERS or
            sum(g['end']-g['start'] for g in groups) != GROUP_BYTES or
            new_group_members != seen):
        raise ValueError('C island group coverage differs from recorded 10 new C functions')
    return rows, groups


def prove(rom, assembly, fixtures, prior77, prior68, prior44,
          cc: Path, ld: Path, objcopy: Path, env=None) -> dict:
    rows, groups = checked_inputs(rom, assembly, fixtures, prior77, prior68, prior44)
    env = dict(os.environ if env is None else env)
    individual, combined = [], []
    original_names = parse_assembly_index(assembly.decode('utf-8'))
    with tempfile.TemporaryDirectory(prefix='goemon-file11-wave3-') as dirname:
        work = Path(dirname)
        for row in rows:
            off, size = row['rom_offset'], row['size']
            original = rom[off:off+size]
            out = native_probe(row['source'], row['vma'],
                               {k:int(v,16) for k,v in row['bindings'].items()},
                               cc, ld, objcopy, work, original, env)
            individual.append({
                'name':row['name'],'rom_offset':f'0x{off:X}','vma':f'0x{row["vma"]:08X}',
                'size':size,'category':row['category'],
                'original_sha256':row['original_sha256'],
                'source_sha256':digest(row['source'].encode()),
                'candidate_sha256':out['candidate_sha256'],
                'matched_words':out['matching_instruction_words'],'exact':out['exact']
            })
        for group in groups:
            start,end=group['start'],group['end']
            out=native_probe(group['source'], VMA_START+start-ROM_START,
                             {k:int(v,16) for k,v in group['bindings'].items()},
                             cc,ld,objcopy,work,rom[start:end],env)
            combined.append({
                'start':f'0x{start:X}','end':f'0x{end:X}',
                'functions':[original_names[off][0] for off in group['function_offsets']],
                'function_count':len(group['function_offsets']),
                'new_functions':sum(off in {r['rom_offset'] for r in rows}
                                    for off in group['function_offsets']),
                'bytes':end-start,'original_sha256':group['original_sha256'],
                'source_sha256':digest(group['source'].encode()),
                'candidate_sha256':out['candidate_sha256'],
                'matched_words':out['matching_instruction_words'],'exact':out['exact']
            })
    return {
        'format':'goemon-file11-adjacent-wave3-native-research-v1',
        'stage':'original_vma_isolated_and_contiguous_ido_5_3_only',
        'original_rom_sha1':ROM_SHA1,
        'original_asm_sha256':PINNED_ASM_SHA256,
        'fixture_sha256':digest(json.dumps(fixtures,sort_keys=True).encode()),
        'new_functions_tested':len(individual),
        'exact_new_functions':sum(r['exact'] for r in individual),
        'exact_new_bytes':sum(r['size'] for r in individual if r['exact']),
        'groups_tested':len(combined),
        'exact_groups':sum(g['exact'] for g in combined),
        'grouped_functions':sum(g['function_count'] for g in combined if g['exact']),
        'grouped_bytes':sum(g['bytes'] for g in combined if g['exact']),
        'previous_unpromoted_research_candidates':sum(EXPECTED_PREVIOUS),
        'total_unpromoted_research_candidates':sum(EXPECTED_PREVIOUS)+len(individual),
        'full_rom_g2_verified':False,
        'new_production_claims':0,
        'functions':individual,'groups':combined
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ('rom','asm','cc','ld','objcopy','report'):
        parser.add_argument('--'+flag,required=True,type=Path)
    parser.add_argument('--fixtures',type=Path,default=SOURCES)
    parser.add_argument('--prior77',type=Path,default=PREVIOUS_77)
    parser.add_argument('--prior68',type=Path,default=PREVIOUS_68)
    parser.add_argument('--prior44',type=Path,default=PREVIOUS_44)
    args=parser.parse_args(argv)
    if args.report.exists():
        parser.error('Will not overwrite previous native research proof')
    fixtures=json.loads(args.fixtures.read_text())
    prior=[json.loads(p.read_text()) for p in (args.prior77,args.prior68,args.prior44)]
    proof=prove(args.rom.read_bytes(),args.asm.read_bytes(),fixtures,*prior,
                args.cc,args.ld,args.objcopy)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.report.open('x') as fp:
        json.dump(proof,fp,indent=2)
        fp.write('\n')
    if proof['exact_new_functions'] != NEW_FUNCTIONS or proof['exact_groups'] != GROUPS:
        raise SystemExit('Native IDO codegen mismatch (research proof contains failures)')
    print(f'PASS: {NEW_FUNCTIONS} native C functions, {GROUPS} combined adjacent islands; research only')


if __name__=='__main__':
    main()
