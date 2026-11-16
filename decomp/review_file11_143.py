"""Fail-closed USA 303-C file_11 central acceptance runner for production and historical reviews.

Runs the full central G2, original-ELF function inventory, and ROM-free local CI
before writing a review bundle. Never edits canonical manifests or proof files.
The bundle is evidence for human review, not an automatic production promotion.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

STAGE_FORMAT = 'goemon-file11-143-central-v1'
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_SIZE = 33_554_432
TOTAL_C = 303
TOTAL_C_BYTES = 16_180
FILE11_C = 143
FILE11_C_BYTES = 3_908
RELOCATIONS = 8_825
ENTRIES = 7_376
ORIGINAL_INVENTORY_SHA256 = '01f41037ac83f6e18e80c83489a18b870e4fef907c67d20a345871c7c34fe787'
SHA256_PATTERN = re.compile(r'[0-9a-f]{64}\Z')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def candidate_manifest(original: dict) -> tuple[dict, list[dict]]:
    """Validate current canonical 303 C or reconstruct from a historical 210-C manifest.

    Regardless of provenance, the exact same 143-C fixture, identities and
    complete native build/inventory/CI gates remain mandatory.
    """
    from . import verify, file11_143_stage
    stage = original.get('overlay_file11_stage')
    review = copy.deepcopy(original)
    if stage == {'format': STAGE_FORMAT}:
        # The new production default: no staged production mutations required.
        pass
    elif stage == {'format': 'goemon-file11-character-switch-50-v2'}:
        previous = verify.claimed_functions(original)
        if len(previous) != 210 or len({fn['name'] for fn in previous}) != 210:
            raise ValueError('Historical 210-C review baseline is not pinned')
        review['overlay_file11_stage'] = {'format': STAGE_FORMAT}
    else:
        raise ValueError('Unsupported production/research file_11 stage')
    plan = file11_143_stage.reviewed_plan(review)
    if (plan['prospective_usa_c'], plan['file11_c_instruction_bytes']) != (TOTAL_C, FILE11_C_BYTES):
        raise ValueError('143-C source fixture differs from the 303-C native proof')
    claims = verify.claimed_functions(review)
    if (len(claims) != TOTAL_C or len({r['name'] for r in claims}) != TOTAL_C
            or sum(r['size'] for r in claims) != TOTAL_C_BYTES):
        raise ValueError('Combined 303-C identities changed')
    return review, claims


def verify_g2_report(report: dict, claims: list[dict]) -> dict:
    if (report.get('format') != 'goemon-matching-build-result-v1'
            or report.get('status') != 'matched' or report.get('stage') != 'complete'):
        raise ValueError('Central G2 did not complete with matched status')
    comparison = report.get('comparison') or {}
    required = {
        'full_rom_match': True, 'expected_sha1': ROM_SHA1,
        'candidate_sha1': ROM_SHA1, 'rom_size': ROM_SIZE,
        'claimed_functions': TOTAL_C, 'matched_functions': TOTAL_C,
        'matched_function_bytes': TOTAL_C_BYTES,
    }
    for key, expected in required.items():
        if type(comparison.get(key)) is not type(expected) or comparison[key] != expected:
            raise ValueError('Central G2 mismatched ' + key)
    expected_by_name = {r['name']: r for r in claims}
    rows = comparison.get('functions')
    if (len(expected_by_name) != TOTAL_C or not isinstance(rows, list)
            or len(rows) != TOTAL_C):
        raise ValueError('Central G2 has incomplete 303-function evidence')
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Malformed G2 function row')
        name = row.get('name')
        if name not in expected_by_name or name in seen or row.get('matched') is not True:
            raise ValueError('Unmatched or duplicate C function row')
        seen.add(name)
        fn = expected_by_name[name]
        identity = {
            'size': fn['size'],
            'guest_address': f"0x{int(name.split('_')[1], 16):08X}",
            'rom_offset': f"0x{fn['rom_offset']:X}",
        }
        if any(type(row.get(k)) is not type(v) or row[k] != v for k,v in identity.items()):
            raise ValueError('G2 original function extent differs: ' + name)
        digest = row.get('expected_sha256')
        if (not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest)
                or row.get('candidate_sha256') != digest):
            raise ValueError('G2 function bytes differ: ' + name)
    stage = report.get('overlay_file11_stage') or {}
    stage_required = {
        'stage': STAGE_FORMAT, 'status': 'PASS',
        'original_address_matching_c': FILE11_C,
        'additional_beyond_50_existing': 93,
        'file11_C_instruction_bytes': FILE11_C_BYTES,
        'original_native_object_provenance_checked': 88,
        'original_semantic_file11_relocations': RELOCATIONS,
        'candidate_semantic_file11_relocations': RELOCATIONS,
        'original_rom_sha1': ROM_SHA1,
        'complete_rom_bytes_equal': ROM_SIZE,
    }
    for key, expected in stage_required.items():
        if type(stage.get(key)) is not type(expected) or stage[key] != expected:
            raise ValueError('143-C linked-stage evidence differs: ' + key)
    expected_aliases = (
        'func_801DD6D8_5995E8',
        'func_801E15CC_59D4DC',
        'func_801F2CCC_5AEBDC',
    )
    normalised_offsets = stage.get('normalised_NOP_asm_symbol_tables', [])
    if (not isinstance(normalised_offsets, list)
            or len(normalised_offsets) != 3
            or set(normalised_offsets) != {'0x5995e8', '0x59d4dc', '0x5aebdc'}):
        raise ValueError('Unexpected synthetic NOP alias normalization')
    alias_evidence = report.get('overlay_file11_nop_aliases') or {}
    if (alias_evidence.get('removed_spurious_func_aliases') != list(expected_aliases)
            or alias_evidence.get('preserved_original_nops') != 3):
        raise ValueError('Synthetic NOP ASM source annotation evidence differs')
    return {'claimed_functions': TOTAL_C, 'matched_bytes': TOTAL_C_BYTES,
            'file11_functions': FILE11_C, 'original_relocations': RELOCATIONS,
            'rom_sha1': ROM_SHA1}


def verify_inventory_report(report: dict) -> dict:
    if (report.get('format') != 'goemon-function-inventory-v1'
            or report.get('decompressed_sha1') != ROM_SHA1):
        raise ValueError('Inventory is not from the original USA ROM')
    summary = report.get('summary') or {}
    expected = {
        'identified_function_entries': ENTRIES,
        'upstream_unmarked_entries': 13,
        'newly_matching_c': TOTAL_C,
        'current_unmarked_entries': 316,
        'remaining_assembly_entries': 7_060,
        'extra_positive_alias_entries': 0,
        'function_entry_identity_sha256': ORIGINAL_INVENTORY_SHA256,
    }
    for key, value in expected.items():
        if type(summary.get(key)) is not type(value) or summary[key] != value:
            raise ValueError('Inventory identity differs: ' + key)
    return expected


def invoke(command: list[str], cwd: Path, log: Path) -> None:
    with log.open('x', encoding='utf-8') as stream:
        subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, check=True)


def run_review(args: argparse.Namespace) -> Path:
    from . import verify
    source = args.source_dir.resolve()
    repo = source.parent
    output = args.output_dir.resolve()
    work = args.workdir.resolve()
    canonical = source / 'manifest.json'
    upstream = args.upstream.resolve()
    if not canonical.is_file():
        raise ValueError('A full private decomp checkout is required')
    if (work.exists() or output.exists()
            or work.is_relative_to(repo) or output.is_relative_to(repo)
            or work.is_relative_to(upstream) or output.is_relative_to(upstream)
            or work == output or work.is_relative_to(output) or output.is_relative_to(work)):
        raise ValueError('Review output and G2 workdir must be new, separate, outside source trees')
    original_bytes = canonical.read_bytes()
    canonical_manifest = verify.load_manifest(canonical)
    trial, claims = candidate_manifest(canonical_manifest)
    output.mkdir(parents=True)
    trial_path = output / 'manifest.file11-143.review.json'
    trial_path.write_text(json.dumps(trial, indent=2) + '\n', encoding='utf-8')
    g2_path = output / 'full-central-g2.json'
    inventory_path = output / 'full-inventory.json'
    cmd = [sys.executable, '-m', 'decomp.verify',
           '--upstream', str(upstream),
           '--retail-rom', str(args.retail_rom.resolve()),
           '--workdir', str(work), '--report', str(g2_path),
           '--manifest', str(trial_path), '--source-dir', str(source),
           '--uv', args.uv, '--jobs', str(args.jobs)]
    if args.binutils_root:
        cmd.extend(['--binutils-root', str(args.binutils_root.resolve())])
    if args.baseline_cache:
        cmd.extend(['--baseline-cache', str(args.baseline_cache.resolve())])
    invoke(cmd, repo, output / 'g2.log')
    proof = verify_g2_report(json.loads(g2_path.read_text()), claims)
    baseline = args.baseline_cache.resolve() if args.baseline_cache else work / 'baseline'
    invoke([sys.executable, '-m', 'decomp.inventory', '--manifest', str(trial_path),
            '--baseline', str(baseline), '--candidate', str(work / 'candidate'),
            '--report', str(inventory_path)], repo, output / 'inventory.log')
    inventory = verify_inventory_report(json.loads(inventory_path.read_text()))
    invoke([sys.executable, '-m', 'decomp.local_ci'], repo, output / 'local-ci.log')
    if canonical.read_bytes() != original_bytes:
        raise ValueError('Canonical manifest changed during acceptance run')
    acceptance = {
        'format': 'goemon-file11-143-central-review-v1',
        'status': 'ready_for_human_review',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'canonical_manifest_sha256': sha256(original_bytes),
        'candidate_manifest_sha256': sha256(trial_path.read_bytes()),
        'g2_sha256': sha256(g2_path.read_bytes()),
        'inventory_sha256': sha256(inventory_path.read_bytes()),
        'g2': proof, 'inventory': inventory,
        'rom_free_local_ci': 'PASS',
        'official_production_manifest_unchanged': True,
    }
    with (output / 'REVIEW.json').open('x', encoding='utf-8') as handle:
        json.dump(acceptance, handle, indent=2)
        handle.write('\n')
    return output


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--upstream', type=Path, required=True)
    p.add_argument('--retail-rom', type=Path, required=True)
    p.add_argument('--workdir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--baseline-cache', type=Path)
    p.add_argument('--binutils-root', type=Path)
    p.add_argument('--uv', default='uv')
    p.add_argument('--jobs', type=int, default=4)
    args = p.parse_args(argv)
    if not 1 <= args.jobs <= 32:
        p.error('--jobs must be 1..32')
    try:
        path = run_review(args)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        p.exit(1, f'303-C promotion NOT verified: {exc}\n')
    print(f'303-C exact-ROM G2, inventory and local CI passed; review bundle: {path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
