"""Native-IDO proof for 68 additional USA file_11 functions and 13 contiguous C groups.

Original USA decompressed ROM, pinned original-Splat assembly, IDO 5.3 and MIPS
binutils are external inputs. No original game bytes or objects are persisted
in repo. This is isolated original-VMA codegen evidence, NOT a full-ROM G2.

Usage:
 python3 -m decomp.research.file11_adjacent_native_probe \\
   --rom /path/to/baserom.decompressed.z64 \\
   --asm /path/to/original/asm/usa/587370.s \\
   --cc /path/to/ido-5.3/cc --ld /path/to/mips-linux-gnu-ld \\
   --objcopy /path/to/mips-linux-gnu-objcopy \\
   --report /tmp/new-file11-adjacent-report.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import tempfile

from decomp.overlay_file11 import ROM_SHA1, ROM_START, TEXT_END, VMA_START, FUNCTIONS as ALREADY_PROMOTED_SWITCH
from decomp.research.usa_file11_noop_groups import entries as promoted_noop_entries
from decomp.research.file11_expansion_probe import native_probe

FIXTURES = Path(__file__).with_name('file11_adjacent_sources.json')
EXPECTED_ASM_SHA256 = 'e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b'
EXPECTED_COUNT = 68
EXPECTED_BYTES = 2416
EXPECTED_GROUP_COUNT = 13
EXPECTED_GROUP_FUNCTIONS = 42
EXPECTED_GROUP_BYTES = 1576
EXPECTED_ROM_BYTES = 0x2000000
INDEX_RE = re.compile(r'(?m)^nonmatching (func_[0-9A-F]{8}_[0-9A-F]+), 0x([0-9A-Fa-f]+)\s*$')
PRIOR_PROOF = Path(__file__).resolve().parents[1] / 'results' / 'file11_expansion_native_20261116.json'
EXPECTED_PREFIX = 'goemon-file11-adjacent-source-fixtures-v1'


def digest(data: bytes, algorithm='sha256'):
    return hashlib.new(algorithm, data).hexdigest()


def parse_assembly_index(asm: str) -> dict[int, tuple[str, int]]:
    index = {}
    for name, sz in INDEX_RE.findall(asm):
        offset = int(name.rsplit('_', 1)[1], 16)
        if offset in index:
            raise ValueError('Duplicate original file_11 function offset')
        index[offset] = (name, int(sz, 16))
    if len(index) < 900:
        raise ValueError('Incomplete original file_11 Splat function inventory')
    return index


def load_fixtures(data: bytes) -> dict:
    rows = json.loads(data)
    if rows.get('format') != EXPECTED_PREFIX:
        raise ValueError('Unreviewed file_11 adjacent fixture format')
    if rows.get('decompressed_rom_sha1') != ROM_SHA1 or rows.get('generated_asm_sha256') != EXPECTED_ASM_SHA256:
        raise ValueError('Unreviewed original ROM/assembly contract')
    if len(rows.get('functions', [])) != EXPECTED_COUNT or len(rows.get('adjacent_groups', [])) != EXPECTED_GROUP_COUNT:
        raise ValueError('Adjacent function or group count differs')
    return rows


def checked_inputs(rom: bytes, assembly: bytes, fixtures: dict) -> tuple[list, list]:
    if len(rom) != EXPECTED_ROM_BYTES or digest(rom, 'sha1') != ROM_SHA1:
        raise ValueError('Original USA reference ROM authentication failed')
    if digest(assembly) != EXPECTED_ASM_SHA256:
        raise ValueError('Original Splat assembly SHA-256 differs from pinned source')
    index = parse_assembly_index(assembly.decode('utf-8'))
    entries = fixtures['functions']
    seen_offsets, seen_names = set(), set()
    previous = ROM_START
    for row in entries:
        name, off, vma, size = (row.get(k) for k in ('name', 'rom_offset', 'vma', 'size'))
        if (type(off) is not int or type(size) is not int or type(vma) is not int or
                not isinstance(name, str) or size <= 0 or size % 4 or off % 4 or
                not ROM_START <= off < TEXT_END or off + size > TEXT_END):
            raise ValueError('Invalid function metadata')
        if name in seen_names or off in seen_offsets or off < previous:
            raise ValueError('Duplicated, overlapping or unsorted native function')
        if index.get(off) != (name, size) or vma != VMA_START + off - ROM_START:
            raise ValueError('Candidate differs from original source function ownership')
        if digest(rom[off:off+size]) != row.get('original_sha256'):
            raise ValueError('Original function byte hash differs: '+name)
        source = row.get('source')
        if (not isinstance(source, str) or
                source.count('void '+name+'(') + source.count('unsigned int '+name+'(') != 1 or
                'GLOBAL_ASM' in source or '#include' in source):
            raise ValueError('Unreviewed C source fixture: '+name)
        bindings = row.get('bindings')
        if not isinstance(bindings, dict) or any(re.fullmatch(r'0x[0-9A-F]{8}', val) is None for val in bindings.values()):
            raise ValueError('Invalid original-address native symbol binding')
        if any(key not in ('handler', 'h1', 'h2', 'global', 'flags') for key in bindings):
            raise ValueError('Unreviewed external symbol name')
        seen_offsets.add(off)
        seen_names.add(name)
        previous = off + size
    promoted = {name for name, _, _, _ in ALREADY_PROMOTED_SWITCH}
    promoted.update(name for name, _ in promoted_noop_entries())
    if not PRIOR_PROOF.is_file():
        raise ValueError('Previous 77-function native probe proof missing')
    previous = json.loads(PRIOR_PROOF.read_text(encoding='utf-8'))
    if (previous.get('exact_matching_functions') != 77 or
            previous.get('exact_matching_bytes') != 2120 or
            len(previous.get('functions', [])) != 77):
        raise ValueError('Previous 77-function native probe proof changed')
    prior_names = {item['name'] for item in previous['functions']}
    if len(prior_names) != 77 or seen_names & (promoted | prior_names):
        raise ValueError('Adjacent candidate was previously promoted or already researched')
    if sum(row['size'] for row in entries) != EXPECTED_BYTES:
        raise ValueError('Original byte total differs')
    if len({row['rom_offset'] for row in entries}) != EXPECTED_COUNT:
        raise ValueError('Duplicate candidate offset')
    by_offset = {row['rom_offset']: row for row in entries}
    groups = fixtures['adjacent_groups']
    grouped = set()
    for group in groups:
        offsets = group.get('function_offsets')
        if not isinstance(offsets, list) or not offsets or offsets != sorted(offsets):
            raise ValueError('Invalid adjacent source order')
        if any(off in grouped or off not in by_offset for off in offsets):
            raise ValueError('Duplicated or missing adjacent function')
        first, last = offsets[0], offsets[-1]
        end = last + by_offset[last]['size']
        if group.get('start') != first or group.get('end') != end:
            raise ValueError('Invalid C island ownership extent')
        for a, b in zip(offsets, offsets[1:]):
            if a + by_offset[a]['size'] != b:
                raise ValueError('C island contains missing intervening ASM')
        if digest(rom[first:end]) != group.get('original_sha256'):
            raise ValueError('Adjacent C island original hash mismatch')
        grouped.update(offsets)
    if (len(grouped) != EXPECTED_GROUP_FUNCTIONS or
            sum(group['end']-group['start'] for group in groups) != EXPECTED_GROUP_BYTES):
        raise ValueError('Adjacent C grouping totals differ')
    return entries, groups


def build_group_source(rows: list[dict]) -> tuple[str, dict[str, int]]:
    """Give every small C function independent ABI names while retaining codegen."""
    snippets, symbols = [], {}
    for row in rows:
        off = row['rom_offset']
        source = row['source']
        for key, value in row['bindings'].items():
            alias = f'{key}_{off:06X}'
            source = re.sub(r'\b'+re.escape(key)+r'\b', alias, source)
            symbols[alias] = int(value, 16)
        for typename in ('Actor', 'Global', 'Inner'):
            source = re.sub(r'\b'+typename+r'\b', f'{typename}_{off:06X}', source)
        snippets.append(source)
    return '\n'.join(snippets)+'\n', symbols


def prove(rom: bytes, assembly: bytes, fixtures: dict, cc: Path, ld: Path,
          objcopy: Path, env=None) -> dict:
    entries, groups = checked_inputs(rom, assembly, fixtures)
    by_offset = {row['rom_offset']: row for row in entries}
    proofs, group_proofs = [], []
    with tempfile.TemporaryDirectory(prefix='goemon-file11-adjacent-') as directory:
        work = Path(directory)
        for row in entries:
            off, size = row['rom_offset'], row['size']
            symbols = {key: int(value, 16) for key, value in row['bindings'].items()}
            matched = native_probe(row['source'], row['vma'], symbols, cc, ld, objcopy,
                                   work, rom[off:off+size], env)
            proofs.append({
                'name': row['name'], 'rom_offset': f'0x{off:X}',
                'vma': f'0x{row["vma"]:08X}', 'size': size,
                'original_sha256': row['original_sha256'],
                'source_sha256': digest(row['source'].encode('utf-8')),
                'candidate_sha256': matched['candidate_sha256'],
                'matched_words': matched['matching_instruction_words'],
                'exact': matched['exact'], 'category': row['category'],
            })
        for group in groups:
            rows = [by_offset[o] for o in group['function_offsets']]
            source, symbols = build_group_source(rows)
            start, end = group['start'], group['end']
            matched = native_probe(source, VMA_START+start-ROM_START, symbols, cc, ld,
                                   objcopy, work, rom[start:end], env)
            group_proofs.append({
                'start': f'0x{start:X}', 'end': f'0x{end:X}',
                'functions': [r['name'] for r in rows],
                'function_count': len(rows), 'bytes': end-start,
                'original_sha256': group['original_sha256'],
                'source_sha256': digest(source.encode('utf-8')),
                'candidate_sha256': matched['candidate_sha256'],
                'exact': matched['exact'],
            })
    return {
        'format':'goemon-file11-adjacent-native-research-v1',
        'stage':'isolated_original_vma_ido_5_3_only',
        'original_rom_sha1': ROM_SHA1,
        'original_asm_sha256': EXPECTED_ASM_SHA256,
        'fixture_sha256': digest(json.dumps(fixtures,sort_keys=True).encode()),
        'functions_tested': len(proofs),
        'exact_functions': sum(p['exact'] for p in proofs),
        'exact_function_bytes': sum(p['size'] for p in proofs if p['exact']),
        'groups_tested': len(group_proofs),
        'exact_groups': sum(p['exact'] for p in group_proofs),
        'grouped_exact_functions': sum(p['function_count'] for p in group_proofs if p['exact']),
        'grouped_exact_bytes': sum(p['bytes'] for p in group_proofs if p['exact']),
        'full_rom_g2_verified': False,
        'new_production_claims': 0,
        'functions': proofs,
        'groups': group_proofs,
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True)
    parser.add_argument('--asm',type=Path,required=True)
    parser.add_argument('--cc',type=Path,required=True)
    parser.add_argument('--ld',type=Path,required=True)
    parser.add_argument('--objcopy',type=Path,required=True)
    parser.add_argument('--fixtures',type=Path,default=FIXTURES)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args(argv)
    if args.report.exists():
        parser.error('Refusing to overwrite an existing native proof report')
    f=load_fixtures(args.fixtures.read_bytes())
    result=prove(args.rom.read_bytes(),args.asm.read_bytes(),f,args.cc,args.ld,args.objcopy)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.report.open('x',encoding='utf-8') as out:
        json.dump(result,out,indent=2);out.write('\n')
    print(f"{result['exact_functions']}/{result['functions_tested']} original-VMA exact; "
          f"{result['exact_groups']}/{result['groups_tested']} contiguous C groups exact. "
          'Not a full-ROM proof.')
    return 0 if (result['exact_functions']==EXPECTED_COUNT and
                 result['exact_function_bytes']==EXPECTED_BYTES and
                 result['exact_groups']==EXPECTED_GROUP_COUNT) else 1


if __name__=='__main__':
    raise SystemExit(main())
