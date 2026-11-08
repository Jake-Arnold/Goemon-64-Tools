"""Read-only whole-ROM byte diagnostics for candidate matching-C rebuilds.

The supplied reference must match the pinned decompressed ROM SHA-1. This tool
never writes or embeds game data in source control. Mismatch reports are local.
Neither a linked probe nor a hash comparison alone proves a matching C rebuild.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path

from .verify import load_manifest


def function_regions(manifest):
    """Sorted original-ROM ranges claimed as matching C in the manifest."""
    regions = sorted((f['rom_offset'], f['rom_offset'] + f['size'], f['name'])
                     for unit in manifest['units'] for f in unit['functions'])
    if any(left[1] > right[0] for left, right in zip(regions, regions[1:])):
        raise ValueError('Overlapping claimed function ranges')
    return regions


def compare_rom_bytes(reference: bytes, candidate: bytes, regions=(), limit=16):
    """Compare actual bytes, including size changes; hashes are informational.

    A mismatch is grouped by a 4-byte MIPS instruction word (not by differing
    byte). Counts include differing or missing trailing bytes. Changed claimed
    functions are summarized even when they fall beyond the example limit.
    MIPS function ranges must be word-aligned. No bytes from unmodified regions
    are included in the returned diagnostic examples.
    """
    if not 0 <= limit <= 256:
        raise ValueError('Mismatch example limit must be between 0 and 256')
    regions = sorted(regions)
    if any(start < 0 or end <= start for start, end, _ in regions):
        raise ValueError('Invalid function range')
    if any(a[1] > b[0] for a, b in zip(regions, regions[1:])):
        raise ValueError('Overlapping function ranges')
    if any(start % 4 or end % 4 for start, end, _ in regions):
        raise ValueError('MIPS function ranges must be word-aligned')
    starts = [start for start, _, _ in regions]
    examples = []
    changed_bytes = 0
    changed_words = 0
    changes_by_region = {}
    claimed_changed_bytes = 0
    claimed_changed_words = 0
    for offset in range(0, max(len(reference), len(candidate)), 4):
        before = reference[offset:offset + 4]
        after = candidate[offset:offset + 4]
        if before == after:
            continue
        changed_words += 1
        byte_count = sum(a != b for a, b in zip(before, after)) + abs(len(before) - len(after))
        changed_bytes += byte_count
        index = bisect_right(starts, offset) - 1
        in_function = index >= 0 and offset < regions[index][1]
        if in_function:
            claimed_changed_bytes += byte_count
            claimed_changed_words += 1
            if index not in changes_by_region:
                start, end, name = regions[index]
                changes_by_region[index] = dict(
                    name=name, rom_offset=f'0x{start:X}', size=end - start,
                    first_mismatch_offset=f'0x{offset:X}',
                    different_bytes=0, different_words=0)
            changes_by_region[index]['different_bytes'] += byte_count
            changes_by_region[index]['different_words'] += 1
        if len(examples) < limit:
            examples.append(dict(rom_offset=f'0x{offset:X}',
                                 function=regions[index][2] if in_function else None,
                                 reference_word=before.hex().upper(), candidate_word=after.hex().upper()))
    return dict(format='goemon-whole-rom-byte-diff-v1',
                exact_match=reference == candidate,
                reference_size=len(reference), candidate_size=len(candidate),
                reference_sha1=hashlib.sha1(reference).hexdigest(),
                candidate_sha1=hashlib.sha1(candidate).hexdigest(),
                reference_sha256=hashlib.sha256(reference).hexdigest(),
                candidate_sha256=hashlib.sha256(candidate).hexdigest(),
                different_bytes=changed_bytes, different_words=changed_words,
                claimed_different_bytes=claimed_changed_bytes,
                claimed_different_words=claimed_changed_words,
                unclaimed_different_bytes=changed_bytes - claimed_changed_bytes,
                unclaimed_different_words=changed_words - claimed_changed_words,
                changed_functions=[changes_by_region[i] for i in sorted(changes_by_region)],
                first_differences=examples)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True, help='Local decompressed reference ROM')
    parser.add_argument('--candidate', type=Path, required=True, help='Local rebuilt ROM')
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('manifest.json'))
    parser.add_argument('--limit', type=int, default=16, help='Maximum reported changed words (0-256)')
    parser.add_argument('--report', type=Path, help='Exclusive-create local JSON report; never overwrite')
    args = parser.parse_args(argv)
    manifest = load_manifest(args.manifest)
    reference = args.reference.read_bytes()
    if hashlib.sha1(reference).hexdigest() != manifest['decompressed_sha1']:
        parser.error('Reference does not match the pinned decompressed US ROM')
    result = compare_rom_bytes(reference, args.candidate.read_bytes(),
                               function_regions(manifest), args.limit)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.report:
        with args.report.open('x', encoding='utf-8') as output:
            output.write(encoded)
    print(encoded, end='')
    return 0 if result['exact_match'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
