"""Fail-closed metadata gate for unpromoted native-exact Goemon C research.

This queue is *not* an accepted-C manifest.  Full regional native G2 and CI
remain required before promoting any candidate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

QUEUE_PATH = Path(__file__).parent / 'data/promotion_candidates_20261120_post233.json'
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
SYM = re.compile(r'^func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
HEX40 = re.compile(r'^[0-9a-f]{40}$')


class ReviewError(ValueError):
    """Candidate cannot safely enter a combined original-ROM promotion build."""


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def validate(queue: dict, root: Path, *, strict_sources=False, rom: bytes | None = None) -> dict:
    if queue.get('format') != 'goemon-promotion-review-queue-v1':
        raise ReviewError('unknown review queue format')
    base = queue.get('production_accepted_baseline', {})
    if base != {'usa_functions': 1962, 'usa_instruction_bytes': 84340,
                'japan_0_functions': 39, 'japan_0_instruction_bytes': 2092}:
        raise ReviewError('stale or unrecognised accepted production checkpoint')
    inv = json.loads((root / 'decomp/results/inventory.json').read_text())
    if inv['summary']['newly_matching_c'] != base['usa_functions']:
        raise ReviewError('live USA accepted count changed; rebase and re-deduplicate')
    jp = json.loads((root / 'decomp/regions/japan_0.json').read_text())
    if sum(len(x['functions']) for x in jp['units']) != base['japan_0_functions']:
        raise ReviewError('live Japan accepted count changed; rebase')
    accepted = json.loads((root / 'decomp/results/combined.json').read_text())['comparison']['functions']
    accepted_names = {x['name'] for x in accepted}
    if len(accepted_names) != base['usa_functions']:
        raise ReviewError('accepted source proof inconsistent')
    with (root / 'decomp/data/rom_file_inventory.csv').open(newline='') as handle:
        records = list(csv.DictReader(handle))
    if len(records) != 1311:
        raise ReviewError('full ROM segment inventory unavailable')
    sections = {x['File']: x for x in records}
    main_end = int(records[0]['USA expanded ROM offset'], 16)
    ready = queue.get('candidates', [])
    blocked = queue.get('blocked_not_promotion_ready', [])
    if not isinstance(ready, list) or not isinstance(blocked, list):
        raise ReviewError('candidate lists missing')
    if not queue.get('no_promotion_claimed'):
        raise ReviewError('queue improperly claims accepted C')
    if rom is not None:
        if len(rom) != 33_554_432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
            raise ReviewError('wrong original USA expanded ROM')
    seen = set()
    intervals = {}
    counts = {}
    source_verified = set()
    for item in ready + blocked:
        n = item.get('name')
        match = SYM.fullmatch(n) if isinstance(n, str) else None
        if not match:
            raise ReviewError('invalid original function symbol')
        offset = int(item['rom_offset'], 16)
        vma = int(item['vma'], 16)
        size = item['size']
        region, segment = item['region'], item['segment']
        if region != 'usa' or vma != int(match.group(1), 16) or offset != int(match.group(2), 16):
            raise ReviewError(f'bad original address/region: {n}')
        if size <= 0 or size % 4 or offset % 4:
            raise ReviewError(f'bad original function extent: {n}')
        if segment == 'main':
            lower, upper = 0, main_end
        else:
            row = sections.get(segment)
            if not row or not row['Segment classification'].startswith('Executable:'):
                raise ReviewError(f'unknown original executable segment: {segment}')
            lower = int(row['USA expanded ROM offset'], 16)
            upper = lower + int(row['USA expanded bytes'])
        if not lower <= offset < offset + size <= upper:
            raise ReviewError(f'candidate lies outside original code segment: {n}')
        if n in accepted_names or n in seen:
            raise ReviewError(f'duplicate or already accepted function: {n}')
        seen.add(n)
        intervals.setdefault(segment, []).append((offset, offset+size, n))
        if item.get('status') != 'RESEARCH_ONLY' or item.get('canonical_g2') != 'NOT_RUN':
            raise ReviewError(f'unverified promotion: {n}')
        if not HEX64.fullmatch(item.get('original_code_sha256', '')):
            raise ReviewError(f'missing original instruction hash: {n}')
        if rom is not None and hashlib.sha256(rom[offset:offset+size]).hexdigest() != item['original_code_sha256']:
            raise ReviewError(f'original ROM function hash mismatch: {n}')
        source = item.get('source', {})
        source_path, blob_sha = source.get('path'), source.get('git_blob_sha', '')
        if (not isinstance(source_path, str) or not source_path.startswith('decomp/')
                or '..' in Path(source_path).parts or not HEX40.fullmatch(blob_sha)):
            raise ReviewError(f'untrusted source provenance: {n}')
        if strict_sources:
            source_file = (root / source_path).resolve()
            if not source_file.is_relative_to(root.resolve()) or not source_file.is_file():
                raise ReviewError(f'missing local source: {source_path}')
            raw = source_file.read_bytes()
            if git_blob_sha(raw) != blob_sha or n.encode() not in raw:
                raise ReviewError(f'source changed or candidate absent: {n}')
            source_verified.add(source_path)
        if item in ready:
            counts.setdefault(segment, {'functions': 0, 'bytes': 0})
            if item.get('review_state') != 'PROMOTION_CANDIDATE':
                raise ReviewError(f'ineligible review state: {n}')
            counts[segment]['functions'] += 1
            counts[segment]['bytes'] += size
        elif item.get('review_state') != 'BLOCKED_RELOCATION':
            raise ReviewError(f'blocked research incorrectly marked ready: {n}')
    for segment, spans in intervals.items():
        for a, b in zip(sorted(spans), sorted(spans)[1:]):
            if a[1] > b[0]:
                raise ReviewError(f'overlapping {segment} candidate extents: {a[2]} / {b[2]}')
    summary = queue.get('ready_for_combined_g2', {})
    if (len(ready), sum(x['size'] for x in ready), len(blocked)) != (0, 0, 1):
        raise ReviewError('expected zero review-ready candidates / one blocked relocation lead')
    if summary != {'functions': 0, 'bytes': 0, 'by_segment': counts}:
        raise ReviewError('review queue rollup changed')
    return {'review_candidates': len(ready), 'review_instruction_bytes': 0,
            'blocked_not_ready': len(blocked), 'by_segment': counts,
            'original_rom_check': 'PASS' if rom is not None else 'NOT_RUN',
            'source_blobs_checked': len(source_verified), 'status': 'RESEARCH_ONLY'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--queue', type=Path, default=QUEUE_PATH)
    parser.add_argument('--strict-sources', action='store_true')
    parser.add_argument('--usa-expanded', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.queue.read_text())
        result = validate(data, args.root, strict_sources=args.strict_sources,
                          rom=args.usa_expanded.read_bytes() if args.usa_expanded else None)
    except (ReviewError, OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(2, f'BLOCKED_INPUT: {exc}\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
