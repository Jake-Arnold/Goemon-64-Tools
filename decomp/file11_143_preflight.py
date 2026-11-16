"""Fail-closed, ROM-optional preflight for a prospective USA file_11 143-C stage.

This does not update a production manifest, invoke the compiler, or count new
matching-C functions. It validates the 50 existing file_11 functions and 93
new research candidates, then optionally emits reviewed source and Splat
inputs into a *new* external scratch directory for a future central G2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from . import overlay_file11
from .research import usa_file11_noop_groups
from .verify import claimed_functions, load_manifest

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / 'research/file11_143_candidate/file11_143_source_fixture.json'
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
FORMAT = 'goemon-file11-143-exact-staging-candidate-v1'
START, END, VMA = 0x587370, 0x5B8500, 0x801CB460
NAME = re.compile(r'func_[0-9A-F]{8}_[0-9A-F]+\Z')
STEM = re.compile(r'[a-z][a-z0-9_]*\Z')
SHA256 = re.compile(r'[0-9a-f]{64}\Z')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(manifest: dict, fixture: dict, original_rom: bytes | None = None) -> dict:
    """Validate reviewed source and ownership without making a C promotion."""
    if (manifest.get('format') != 'goemon-matching-decomp-v1'
            or manifest.get('overlay_file11_stage') !=
            {'format': 'goemon-file11-character-switch-50-v2'}
            or manifest.get('decompressed_sha1') != ROM_SHA1):
        raise ValueError('Expected the pinned canonical 210-C USA baseline')
    existing = claimed_functions(manifest)
    if len(existing) != 210 or len({x['name'] for x in existing}) != 210:
        raise ValueError('Canonical 210-function claim inventory changed')
    baseline = {(name, offset, size) for name, offset, size, _ in overlay_file11.FUNCTIONS}
    baseline.update((name, offset, 12) for name, offset in usa_file11_noop_groups.entries())
    if len(baseline) != 50 or sum(x[2] for x in baseline) != 1064:
        raise ValueError('Existing file_11 50-function stage changed')
    if fixture.get('format') != FORMAT or fixture.get('scope') != 'USA_file11_clean_upstream_overlay_only':
        raise ValueError('Unreviewed 143-function source fixture')
    pins = {
        'upstream_commit': '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee',
        'original_rom_sha1': ROM_SHA1,
        'original_elf_sha256': '83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038',
        'original_asm_sha256': 'e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b',
        'rom_length': 0x2000000, 'file11_relocations': 8825,
        'overlay_text_start': START, 'overlay_text_end': END,
        'original_file11_stage_c_functions': 50,
        'wave1_research_functions_covered': 77,
        'wave45_additional_functions_beyond_wave1': 16,
        'total_represented_functions': 143,
        'new_covered_functions_beyond_existing_50': 93,
        'all_C_text_bytes': 3908,
        'full_210_plus_research_g2_verified': False,
        'production_promotion_count': 0,
    }
    for key, value in pins.items():
        if fixture.get(key) != value:
            raise ValueError('Fixture provenance/claim disagrees: ' + key)
    chunks = fixture.get('chunks')
    if not isinstance(chunks, list) or len(chunks) != 88:
        raise ValueError('Expected 88 original-order file_11 text chunks')
    if original_rom is not None:
        if len(original_rom) != 0x2000000 or hashlib.sha1(original_rom).hexdigest() != ROM_SHA1:
            raise ValueError('Wrong original USA expanded 32 MiB ROM')
    previous, sources, functions, order = START, {}, [], []
    counts = {'c': 0, 'asm': 0}
    for part in chunks:
        start, end, size, kind = (part.get(k) for k in ('rom_start', 'rom_end', 'size', 'kind'))
        if (not isinstance(start, int) or not isinstance(end, int)
                or start != previous or end <= start or end > END
                or start % 4 or end % 4 or size != end - start
                or kind not in counts or not SHA256.fullmatch(part.get('original_sha256', ''))
                or not SHA256.fullmatch(part.get('trimmed_obj_sha256', ''))):
            raise ValueError('Gap, overlap, invalid digest or unreviewed text chunk')
        if original_rom is not None and sha(original_rom[start:end]) != part['original_sha256']:
            raise ValueError('Changed original-ROM text at ' + hex(start))
        if kind == 'c':
            stem, source = part.get('name'), part.get('source')
            if (not isinstance(stem, str) or not STEM.fullmatch(stem)
                    or not isinstance(source, str) or 'GLOBAL_ASM' in source
                    or '#include' in source or stem in sources
                    or sha(source.encode('utf-8')) != part.get('source_sha256')):
                raise ValueError('Unreviewed inline C translation unit')
            sources[stem] = source
            offset = start
            members = part.get('functions')
            if not isinstance(members, list) or not members:
                raise ValueError('C chunk missing original function identities')
            for f in members:
                name, at, vma, length = (f.get(k) for k in ('name', 'off', 'vma', 'size'))
                if (not isinstance(name, str) or not NAME.fullmatch(name)
                        or at != offset or not isinstance(length, int) or length <= 0
                        or length % 4 or vma != VMA + offset - START
                        or name not in source or int(name.split('_')[2], 16) != offset):
                    raise ValueError('C function name/boundary/address does not match source')
                functions.append((name, offset, length))
                offset += length
            if offset != end:
                raise ValueError('C source leaves unclaimed assembler gap')
            order.append((start, 'c', stem))
        else:
            if part.get('name') is not None or part.get('source') is not None:
                raise ValueError('Unexpected C source attached to ASM ownership')
            order.append((start, 'asm', None))
        counts[kind] += 1
        previous = end
    if previous != END or counts != {'c': 44, 'asm': 44}:
        raise ValueError('Incomplete original file_11 overlay ownership')
    if len(functions) != 143 or len(set(functions)) != 143 or len({x[0] for x in functions}) != 143:
        raise ValueError('Duplicated/missing C function identity')
    if len({x[1] for x in functions}) != 143 or sum(x[2] for x in functions) != 3908:
        raise ValueError('Duplicated/missing ROM offset or code bytes')
    current = set(functions)
    if not baseline <= current or len(current - baseline) != 93:
        raise ValueError('Existing 50 C functions not preserved or 93 additions not distinct')
    if {x['name'] for x in existing}.intersection(x[0] for x in current - baseline):
        raise ValueError('Research additions already claimed outside file_11')
    for name, offset, size in current:
        if offset < START or offset + size > END:
            raise ValueError('file_11 function outside pinned overlay text')
    return {
        'format': 'goemon-file11-143-preflight-v1',
        'status': 'PREFLIGHT_ONLY_NOT_PROMOTED',
        'baseline_usa_c': 210, 'existing_file11_c': 50,
        'additional_research_c': 93, 'prospective_usa_c': 303,
        'file11_c_total': 143, 'file11_c_instruction_bytes': 3908,
        'additional_instruction_bytes': 2844,
        'chunks': len(chunks), 'c_units': 44, 'asm_slices': 44,
        'rom_verified': original_rom is not None,
        'central_g2_verified': False, 'eligible_for_manifest_promotion': False,
        'ordered_segments': order, 'c_sources': sources,
    }


def emit(plan: dict, out: Path) -> None:
    """Write exact reviewed stage inputs into a new external scratch directory."""
    out = out.resolve()
    if out.exists():
        raise FileExistsError('Refusing an existing output directory: ' + str(out))
    repo_root = ROOT.parent.resolve()
    if out == repo_root or repo_root in out.parents:
        raise ValueError('Refusing to stage generated sources inside source repository')
    lines = [f'    - [0x{at:X}, {kind}' + (f', {stem}' if stem else '') + ']'
             for at, kind, stem in plan['ordered_segments']]
    out.mkdir(parents=True, exist_ok=False)
    source_dir = out / 'src'
    source_dir.mkdir()
    for stem, source in plan['c_sources'].items():
        (source_dir / (stem + '.c')).write_text(source, encoding='utf-8', newline='\n')
    (out / 'file11-subsegments.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    public = {key: value for key, value in plan.items() if key not in ('c_sources', 'ordered_segments')}
    (out / 'preflight.json').write_text(json.dumps(public, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT/'manifest.json')
    parser.add_argument('--fixture', type=Path, default=FIXTURE)
    parser.add_argument('--original-expanded-usa-rom', type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    fixture = json.loads(args.fixture.read_text(encoding='utf-8'))
    original = args.original_expanded_usa_rom.read_bytes() if args.original_expanded_usa_rom else None
    plan = validate(manifest, fixture, original)
    emit(plan, args.output_dir.resolve())
    print('file_11 143-C PREFLIGHT ONLY: 50 existing + 93 unpromoted; central G2 not run')


if __name__ == '__main__':
    main()
