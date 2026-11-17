"""Verify 385 researched file_12 C functions plus the 2 canonical file_12 C callbacks.

This builds original pinned upstream ASM + 387 C, not the canonical 342+385
central decomp build. Requires the original pinned ROM/toolchain and these two
source files from the connected Goemon-64-Tools decomp/candidates directory.
No game ROM, generated assembly, ELF or original code bytes are exported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil

try:
    from . import integrate_385 as expanded
except ImportError:
    import importlib.util
    _script = Path(__file__).resolve().with_name('integrate_385.py')
    _spec = importlib.util.spec_from_file_location('file12_expanded_coexistence', _script)
    expanded = importlib.util.module_from_spec(_spec)
    assert _spec.loader is not None
    _spec.loader.exec_module(expanded)

BASE_SPECS = expanded.SPECS
CANONICAL_STAGES = (
    ('file12_dialogue_copy', 'func_80222034_5DD504', 0x5DD504, 0x14,
     'bce7049e5438f50b9cb5bd7cea430fb2101067dcfdab760003ecaef3c2527fd2'),
    ('file12_dialogue_call', 'func_80222168_5DD638', 0x5DD638, 0x24,
     '2fff2f49dbeb427200ef469596a8a229c9763db6f70bee93e662a1b1016ef6d1'),
)


def validate_canonical_source_inputs(source_dir: Path) -> list[dict]:
    checked = []
    for stem, name, offset, size, expected_sha in CANONICAL_STAGES:
        source = source_dir / (stem + '.c')
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha:
            raise ValueError('Canonical file12 source missing or SHA-256 mismatch: ' + stem)
        checked.append({'name': name, 'offset': f'0x{offset:X}', 'bytes': size,
                        'source_sha256': expected_sha})
    return checked


def audit_canonical_comparison(path: Path) -> dict:
    """Check published central proof and reject overlap with the 385 new ranges."""
    proof = json.loads(path.read_text())
    cmp = proof.get('comparison', {})
    if (proof.get('status') != 'matched' or cmp.get('full_rom_match') is not True or
            cmp.get('matched_functions') != 342 or cmp.get('matched_function_bytes') != 17568 or
            cmp.get('claimed_functions') != 342 or len(cmp.get('functions', [])) != 342):
        raise ValueError('Expected exact canonical 342-function USA report')
    ranges = [(start, start + size) for _, _, start, size, _ in BASE_SPECS]
    # The registration cluster has 374 functions, represented by one interval.
    collisions = []
    for item in cmp['functions']:
        off = int(item['rom_offset'], 16)
        end = off + item['size']
        for a, b in ranges:
            if off < b and a < end:
                collisions.append(item['name'])
    if collisions:
        raise ValueError('Research C overlaps already-promoted functions: ' + repr(collisions))
    return {'canonical_function_count': 342, 'canonical_original_c_bytes': 17568,
            'original_sha1': cmp['expected_sha1'], 'prior_proof_sha256':
            hashlib.sha256(path.read_bytes()).hexdigest(), 'overlaps': []}


def run(upstream: Path, candidate: Path, canonical_sources: Path, jobs: int,
        comparison: Path | None = None) -> dict:
    canonical_sources = canonical_sources.resolve()
    checked_sources = validate_canonical_source_inputs(canonical_sources)
    audit = audit_canonical_comparison(comparison) if comparison else None
    original_stage = expanded.stage_inputs
    combined = BASE_SPECS + CANONICAL_STAGES

    def stage_with_canonical(upstream_path, temp):
        # Temporarily retain the old 385-item plan for the original source-copy
        # routine. Its wrapper generator and all 11 noncanonical sources remain
        # hash-pinned; the two additional sources are validated separately.
        expanded.SPECS = BASE_SPECS
        try:
            staged = original_stage(upstream_path, temp)
        finally:
            expanded.SPECS = combined
        for stem, _, _, _, _ in CANONICAL_STAGES:
            shutil.copyfile(canonical_sources / (stem + '.c'), staged / (stem + '.c'))
        return staged

    expanded.SPECS = combined
    expanded.stage_inputs = stage_with_canonical
    try:
        result = expanded.integrate_385(upstream, candidate, jobs)
    finally:
        expanded.SPECS = BASE_SPECS
        expanded.stage_inputs = original_stage
    if (result['reconstructed_function_count'] != 387 or
            result['reconstructed_original_code_bytes'] != 14268 or
            not result['file12_semantic_relocation_multiset_identical'] or
            result['full_rom_bytes_exact'] != 33_554_432):
        raise ValueError('Combined file12 original-ROM invariants changed')
    result.update({
        'status': 'original_usa_file12_385_research_plus_2_canonical_pass',
        'scope': 'Only file12 coexistence: pristine original upstream ASM + 387 C',
        'canonical_file12_sources': checked_sources,
        'canonical_published_proof_audit': audit,
        'canonical_727_central_G2_completed': False,
        'limitations': ('Canonical 342+385 complete C manifest, simultaneous central '
                        'decomp.verify, decomp.inventory and decomp.local_ci NOT executed'),
    })
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream', required=True, type=Path)
    p.add_argument('--candidate', required=True, type=Path)
    p.add_argument('--canonical-source-dir', required=True, type=Path,
                   help='Directory containing the two checked canonical file12_dialogue_*.c files')
    p.add_argument('--canonical-comparison', type=Path,
                   help='Current canonical decomp/results/combined.json; checks 342 proof and collisions')
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--report', required=True, type=Path)
    args = p.parse_args()
    if not 1 <= args.jobs <= 32:
        raise ValueError('Invalid job count')
    if args.report.exists():
        raise FileExistsError('Proof JSON destination must be new')
    result = run(args.upstream, args.candidate, args.canonical_source_dir, args.jobs,
                 args.canonical_comparison)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'objects'}, indent=2))


if __name__ == '__main__':
    main()
