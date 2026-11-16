"""Fail-closed original-USA IDO 5.3 probe for the second file_11 adjacency scan.

Research only. Exact isolated MIPS code and contiguous translation units do not
prove an integrated overlay, linked relocations or a complete-ROM G2 build.
Do not commit private ROMs, upstream assembly, toolchain binaries or objects.

Example:
  python3 -m decomp.research.file11_adjacent_wave2_probe \\
    --rom /path/to/baserom.decompressed.z64 \\
    --asm /path/to/original/asm/usa/587370.s \\
    --cc /path/to/ido-5.3/cc --ld /path/to/mips-linux-gnu-ld \\
    --objcopy /path/to/mips-linux-gnu-objcopy \\
    --report /tmp/unique-file11-wave2-native-proof.json
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

from decomp.research import file11_adjacent_native_probe as previous_probe
from decomp.research.file11_expansion_probe import native_probe, ROM_SHA1
from decomp.overlay_file11 import FUNCTIONS as PROMOTED_13
from decomp.research.usa_file11_noop_groups import entries as promoted_empty_callbacks

CURRENT = Path(__file__).with_name('file11_adjacent_wave2_sources.json')
PRIOR68 = Path(__file__).with_name('file11_adjacent_sources.json')
PRIOR77 = Path(__file__).resolve().parents[1] / 'results' / 'file11_expansion_native_20261116.json'
PINNED_ASM_SHA256 = 'e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b'
PINNED_ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_START = 0x587370
VMA_START = 0x801CB460
TEXT_END = 0x5B8AF0
EXPECTED_NEW = 44
EXPECTED_NEW_BYTES = 1976
EXPECTED_GROUPS = 9
EXPECTED_GROUP_MEMBERS = 44
EXPECTED_GROUP_BYTES = 1892
PREVIOUS_77 = 77
PREVIOUS_68 = 68
REQUIRED_FORMAT = 'goemon-file11-adjacent-wave2-source-fixtures-v1'


def sha(data: bytes, algorithm='sha256') -> str:
    return hashlib.new(algorithm, data).hexdigest()


def authenticate(rom: bytes, assembly: bytes, fixtures: dict, prior68: dict,
                 prior77: dict):
    """Validate original inputs, all code hashes, and non-overlap before compilation."""
    if len(rom) != 0x2000000 or sha(rom, 'sha1') != PINNED_ROM_SHA1:
        raise ValueError('Original decompressed USA ROM hash/length mismatch')
    if sha(assembly) != PINNED_ASM_SHA256:
        raise ValueError('Original 906-function Splat source SHA256 mismatch')
    if fixtures.get('format') != REQUIRED_FORMAT:
        raise ValueError('Unknown wave-two source contract')
    if fixtures.get('decompressed_rom_sha1') != PINNED_ROM_SHA1 or \
            fixtures.get('generated_asm_sha256') != PINNED_ASM_SHA256 or \
            fixtures.get('upstream_commit') != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
        raise ValueError('Unpinned wave-two fixtures')
    if prior68.get('format') != 'goemon-file11-adjacent-source-fixtures-v1' or \
            len(prior68.get('functions', [])) != PREVIOUS_68:
        raise ValueError('Missing original 68-function source inventory')
    if prior77.get('exact_matching_functions') != PREVIOUS_77 or \
            prior77.get('exact_matching_bytes') != 2120 or \
            len(prior77.get('functions', [])) != PREVIOUS_77:
        raise ValueError('Missing previous 77-function native proof')
    original_index = previous_probe.parse_assembly_index(assembly.decode('utf-8'))
    previous68_rows = {r['rom_offset']: r for r in prior68['functions']}
    previous77_rows = {r['rom_offset']: r for r in prior77['functions']}
    if len(previous68_rows) != PREVIOUS_68 or len(previous77_rows) != PREVIOUS_77:
        raise ValueError('Duplicate previously identified function')
    all_prior = set(previous68_rows) | set(previous77_rows)
    already_promoted = {off for _, off, _, _ in PROMOTED_13}
    already_promoted.update(off for _, off in promoted_empty_callbacks())
    if len(all_prior) != PREVIOUS_68 + PREVIOUS_77:
        raise ValueError('Previous 68/77 research overlap')
    if fixtures.get('previous_research_68_count') != PREVIOUS_68 or \
            fixtures.get('previous_research_77_count') != PREVIOUS_77:
        raise ValueError('Prior research count changed')

    candidates = fixtures.get('functions')
    groups = fixtures.get('adjacent_groups')
    if not isinstance(candidates, list) or len(candidates) != EXPECTED_NEW or \
            not isinstance(groups, list) or len(groups) != EXPECTED_GROUPS:
        raise ValueError('Unreviewed wave-two function/group count')
    seen = set()
    for r in candidates:
        name, off, size, vma = (r.get(k) for k in ('name', 'rom_offset', 'size', 'vma'))
        if (not isinstance(off, int) or isinstance(off, bool) or not isinstance(size, int) or
                isinstance(size, bool) or not isinstance(vma, int) or
                not isinstance(name, str) or not ROM_START <= off < TEXT_END or
                size <= 0 or size % 4 or off % 4 or off + size > TEXT_END or
                off in seen or off in all_prior or off in already_promoted):
            raise ValueError('Duplicate, overlapping or invalid new function entry')
        if original_index.get(off) != (name, size) or vma != VMA_START + off - ROM_START:
            raise ValueError('Original function boundary/name/VMA changed')
        if sha(rom[off:off+size]) != r.get('original_sha256'):
            raise ValueError('Original instructions changed: ' + name)
        source = r.get('source')
        if (not isinstance(source, str) or name not in source or
                'GLOBAL_ASM' in source or '#include' in source or
                source.count(name+'(') != 1):
            raise ValueError('Missing or unreviewed native C candidate source')
        bindings = r.get('bindings')
        if not isinstance(bindings, dict) or any(
                re.fullmatch(r'0x[0-9A-F]{8}', value) is None for value in bindings.values()
                if isinstance(value, str)) or any(not isinstance(v, str) for v in bindings.values()):
            raise ValueError('Unreviewed original-address external symbol')
        if any(key not in ('handler','g_index') for key in bindings):
            raise ValueError('Unknown external symbol type')
        seen.add(off)
    if [r['rom_offset'] for r in candidates] != sorted(seen) or \
            sum(r['size'] for r in candidates) != EXPECTED_NEW_BYTES:
        raise ValueError('Invalid source order or native byte total')

    allrows = {r['rom_offset']: r for r in candidates}
    allrows.update(previous68_rows)
    prior_group_noops = {}
    for off, r in previous77_rows.items():
        if r.get('category') == 'empty_callback':
            name, size = original_index.get(off, (None,None))
            if size == 12 and r.get('name') == name and \
                    sha(rom[off:off+12]) == r.get('original_sha256'):
                prior_group_noops[off] = {
                    'name': name, 'rom_offset': off, 'size': 12,
                    'source': f'void {name}(void *a,void *b){{}}\n',
                    'bindings': {},
                }
    allrows.update(prior_group_noops)
    group_seen, group_starts = set(), set()
    for group in groups:
        start, end, offsets = (group.get(k) for k in ('start','end','function_offsets'))
        if (type(start) is not int or type(end) is not int or not isinstance(offsets,list) or
                not offsets or start in group_starts or start != offsets[0] or
                offsets != sorted(set(offsets)) or end <= start or
                sha(rom[start:end]) != group.get('original_sha256')):
            raise ValueError('Invalid adjacent island source bounds')
        if any(off in group_seen or off not in allrows for off in offsets):
            raise ValueError('Island includes unknown or duplicate function')
        for a, b in zip(offsets, offsets[1:]):
            if a + original_index[a][1] != b:
                raise ValueError('Island contains assembly between C functions')
        if end != offsets[-1] + original_index[offsets[-1]][1]:
            raise ValueError('Island tail differs from original function boundaries')
        group_seen.update(offsets)
        group_starts.add(start)
    if sum(len(g['function_offsets']) for g in groups) != EXPECTED_GROUP_MEMBERS or \
            sum(g['end']-g['start'] for g in groups) != EXPECTED_GROUP_BYTES:
        raise ValueError('Native island member/byte totals differ')
    return candidates, groups, allrows


def group_source(rows: list[dict]):
    """Namespace source typedefs/external symbols by original function offset."""
    patched = []
    for r in rows:
        src = re.sub(r'\bState\b', 'State_%06X' % r['rom_offset'], r['source'])
        patched.append({**r, 'source': src})
    return previous_probe.build_group_source(patched)


def prove(rom: bytes, assembly: bytes, fixtures: dict, prior68: dict,
          prior77: dict, cc: Path, ld: Path, objcopy: Path, env=None):
    candidates, groups, allrows = authenticate(rom,assembly,fixtures,prior68,prior77)
    env = dict(os.environ if env is None else env)
    individual, grouped = [], []
    with tempfile.TemporaryDirectory(prefix='goemon-file11-wave2-') as temp:
        work=Path(temp)
        for r in candidates:
            off,size=r['rom_offset'],r['size']
            result=native_probe(r['source'],r['vma'],{
                k:int(v,16) for k,v in r['bindings'].items()
            },cc,ld,objcopy,work,rom[off:off+size],env)
            individual.append({
                'name':r['name'],'rom_offset':f'0x{off:X}',
                'vma':f'0x{r["vma"]:08X}','size':size,
                'category':r['category'],'original_sha256':r['original_sha256'],
                'source_sha256':sha(r['source'].encode('utf-8')),
                'candidate_sha256':result['candidate_sha256'],
                'matching_instruction_words':result['matching_instruction_words'],
                'exact':result['exact'],
            })
        for group in groups:
            start,end=group['start'],group['end']
            source, symbols=group_source([allrows[x] for x in group['function_offsets']])
            result=native_probe(source,VMA_START+start-ROM_START,symbols,cc,ld,objcopy,
                                work,rom[start:end],env)
            grouped.append({
                'start':f'0x{start:X}','end':f'0x{end:X}',
                'functions':[allrows[x]['name'] for x in group['function_offsets']],
                'function_count':len(group['function_offsets']),
                'new_function_count':sum(x in {r['rom_offset'] for r in candidates}
                                         for x in group['function_offsets']),
                'bytes':end-start,'original_sha256':group['original_sha256'],
                'source_sha256':sha(source.encode('utf-8')),
                'candidate_sha256':result['candidate_sha256'],
                'matching_instruction_words':result['matching_instruction_words'],
                'exact':result['exact'],
            })
    return {
        'format':'goemon-file11-adjacent-wave2-native-research-v1',
        'stage':'original_vma_isolated_and_contiguous_ido_5_3_only',
        'original_rom_sha1':PINNED_ROM_SHA1,
        'original_asm_sha256':PINNED_ASM_SHA256,
        'fixture_sha256':sha(json.dumps(fixtures,sort_keys=True).encode()),
        'new_functions_tested':len(individual),
        'exact_new_functions':sum(r['exact'] for r in individual),
        'exact_new_bytes':sum(r['size'] for r in individual if r['exact']),
        'categories':dict(Counter(r['category'] for r in individual)),
        'contiguous_groups_tested':len(grouped),
        'exact_contiguous_groups':sum(g['exact'] for g in grouped),
        'exact_grouped_functions':sum(g['function_count'] for g in grouped if g['exact']),
        'exact_grouped_new_functions':sum(g['new_function_count'] for g in grouped if g['exact']),
        'exact_grouped_bytes':sum(g['bytes'] for g in grouped if g['exact']),
        'previous_research_candidates':PREVIOUS_77+PREVIOUS_68,
        'combined_research_candidates':PREVIOUS_77+PREVIOUS_68+len(individual),
        'full_rom_g2_verified':False,
        'production_manifest_changed':False,
        'new_production_claims':0,
        'functions':individual,
        'groups':grouped,
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ('rom','asm','cc','ld','objcopy','report'):
        parser.add_argument('--'+flag,required=True,type=Path)
    parser.add_argument('--fixtures',type=Path,default=CURRENT)
    parser.add_argument('--prior68',type=Path,default=PRIOR68)
    parser.add_argument('--prior77',type=Path,default=PRIOR77)
    args=parser.parse_args(argv)
    if args.report.exists():
        parser.error('Refusing to overwrite previous IDO proof')
    rom=args.rom.read_bytes()
    assembly=args.asm.read_bytes()
    fixtures=json.loads(args.fixtures.read_text(encoding='utf-8'))
    prior68=json.loads(args.prior68.read_text(encoding='utf-8'))
    prior77=json.loads(args.prior77.read_text(encoding='utf-8'))
    result=prove(rom,assembly,fixtures,prior68,prior77,args.cc,args.ld,args.objcopy)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.report.open('x',encoding='utf-8') as fd:
        json.dump(result,fd,indent=2)
        fd.write('\n')
    print(f"{result['exact_new_functions']}/{result['new_functions_tested']} new original-VMA functions "
          f"({result['exact_new_bytes']} bytes); "
          f"{result['exact_contiguous_groups']}/{result['contiguous_groups_tested']} "
          "complete C islands exact; research-only, not full G2.")
    return 0 if (result['exact_new_functions']==EXPECTED_NEW and
                 result['exact_new_bytes']==EXPECTED_NEW_BYTES and
                 result['exact_contiguous_groups']==EXPECTED_GROUPS and
                 result['exact_grouped_functions']==EXPECTED_GROUP_MEMBERS and
                 result['exact_grouped_bytes']==EXPECTED_GROUP_BYTES) else 1


if __name__=='__main__':
    raise SystemExit(main())
