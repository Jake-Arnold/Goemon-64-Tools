"""Read-only Japan-0 float XYZ candidate finder from three WIDE captures.

A is stationary at start, B is after the player walked and stopped, and C is
stationary again at B's location. This is a heuristic, NOT a discovered
player pointer or proof that any returned triple belongs to the player.
Never authorise position edits, teleports or freezes from these candidates.
"""
from __future__ import annotations

import heapq
import math
import struct

from practice.japan_state_comparison import JapanMemoryCapture
from practice.value_search import GUEST_BASE

MAX_XYZ_CANDIDATES = 200
MIN_HORIZONTAL_MOVEMENT = 0.75
MAX_HORIZONTAL_MOVEMENT = 5000.0
MAX_VERTICAL_MOVEMENT = 300.0
STATIONARY_TOLERANCE = 0.5
MAX_PLAUSIBLE_COORD = 100000.0


def _valid_triple(values):
    return all(math.isfinite(value) and abs(value) <= MAX_PLAUSIBLE_COORD
               for value in values)


def _xyz_context(capture):
    return {'label': capture.label, 'utc': capture.utc,
            'scene': capture.map_id, 'character': capture.character}


def _validated_wide_buffers(before, moved, settled):
    captures = (before, moved, settled)
    if any(not isinstance(c, JapanMemoryCapture) for c in captures):
        raise ValueError('Three Japan-0 captures A/B/C are required')
    if any(c.identity != before.identity for c in captures[1:]):
        raise ValueError('Different Japanese ROM/PID/RDRAM; recapture A/B/C')
    if any(c.scope != 'wide' or len(c.regions) != 1 for c in captures):
        raise ValueError('XYZ discovery needs three WIDE Japanese A/B/C captures')
    if (before.map_id is None or before.character is None
            or any(c.map_id != before.map_id or c.character != before.character
                   for c in captures[1:])):
        raise ValueError('Keep the same validated scene and character across A/B/C')
    ra, rb, rc = (c.regions[0] for c in captures)
    if (ra.address != GUEST_BASE or
            any(r.name != ra.name or r.address != ra.address
                or len(r.data) != len(ra.data) for r in (rb, rc)) or
            len(ra.data) not in (0x400000, 0x800000)):
        raise ValueError('WIDE Japanese RAM ranges differ or are incomplete')
    return tuple(memoryview(r.data) for r in (ra, rb, rc))


def _xyz_candidate_rows(a, b, c, *, cancelled=None):
    """Yield every matching candidate, in guest-address order.

    Never collects a huge 8 MiB scan's matches in RAM. The same predicate
    serves both the limited Tk preview and the complete on-disk JSON export.
    """
    unpack = struct.Struct('>fff').unpack_from
    for offset in range(0, len(a) - 11, 4):
        if cancelled is not None and offset % 0x8000 == 0 and cancelled():
            raise RuntimeError('XYZ export cancelled after captures changed')
        if a[offset:offset + 12] == b[offset:offset + 12]:
            continue
        av, bv, cv = (unpack(buf, offset) for buf in (a, b, c))
        if not (_valid_triple(av) and _valid_triple(bv) and _valid_triple(cv)):
            continue
        dx, dy, dz = (bv[i] - av[i] for i in range(3))
        horizontal = math.hypot(dx, dz)
        if not (MIN_HORIZONTAL_MOVEMENT <= horizontal <= MAX_HORIZONTAL_MOVEMENT):
            continue
        if abs(dy) > MAX_VERTICAL_MOVEMENT:
            continue
        stable = max(abs(cv[i] - bv[i]) for i in range(3))
        if stable > STATIONARY_TOLERANCE:
            continue
        score = (round(50.0 - min(50.0, stable * 60.0), 3)
                 + (20 if abs(dy) <= 0.25 else 0)
                 + (10 if abs(dx) >= 0.75 and abs(dz) >= 0.75 else 0)
                 + (10 if 2.0 <= horizontal <= 250.0 else 0))
        address = GUEST_BASE + offset
        def fmt(values):
            return '(' + ', '.join(f'{value:.2f}' for value in values) + ')'
        yield {
            'address': f'0x{address:08X}', 'region': 'jp_full_rdram',
            'before': fmt(av), 'after': fmt(bv),
            'xor_mask': '—', 'c_stable_at_b': True,
            'kind': 'XYZ triple candidate', 'width': 12,
            'watch_type': 'f32', 'score': score,
            'xyz_A': list(av), 'xyz_B': list(bv), 'xyz_C': list(cv),
            'horizontal_delta': round(horizontal, 4),
            'vertical_delta': round(dy, 4),
            'stationary_delta_max': round(stable, 4),
        }


def _report_metadata(before, moved, settled, size):
    return {
        'format': 'goemon-japan-xyz-heuristic-v1',
        'region': 'japan-0',
        'scope': 'wide',
        'session': {'pid': before.identity[1],
                    'rdram_base': hex(before.identity[2]),
                    'endian': before.identity[3],
                    'guest_ram_size': size},
        'capture_A': _xyz_context(before),
        'capture_B': _xyz_context(moved),
        'capture_C': _xyz_context(settled),
        'event_flag_changes': [],
        'notes': ('Read-only aligned f32 XYZ-like triplets. A=stationary, '
                  'B=walked to new position, C=stationary at B. '
                  'A candidate can belong to scenery, NPCs or calculations. '
                  'No Japanese player pointer/XYZ field is confirmed. '
                  'The exported JSON contains every matching candidate, '
                  'but never the raw 4/8 MiB RAM snapshots.'),
    }


def find_japan_xyz_candidates(before, moved, settled, *, limit=MAX_XYZ_CANDIDATES):
    """Return at most 200 ranked matches for the interactive Tk table.

    Counts reflect ALL matches. Export uses the same match generator to
    write every candidate separately without this display-only cap.
    """
    if type(limit) is not int or not 1 <= limit <= MAX_XYZ_CANDIDATES:
        raise ValueError('XYZ candidate limit must be 1..200')
    a, b, c = _validated_wide_buffers(before, moved, settled)
    top = []
    possible = 0
    for row in _xyz_candidate_rows(a, b, c):
        possible += 1
        score = row['score']
        address = int(row['address'], 16)
        entry = (score, -address, row)
        if len(top) < limit:
            heapq.heappush(top, entry)
        elif entry[:2] > top[0][:2]:
            heapq.heapreplace(top, entry)
    rows = [entry[2] for entry in sorted(top, key=lambda x: (-x[0], -x[1]))]
    metadata = _report_metadata(before, moved, settled, len(a))
    metadata.update({
        'counts': {'regions_compared': 1, 'observed_changes': possible,
                   'candidate_count': possible,
                   'reported_candidates': len(rows)},
        'candidates': rows,
        'display_limit': limit,
        'export_policy': 'all_candidates_recompute_from_captures',
    })
    return metadata


def export_japan_xyz_all_candidates(before, moved, settled, destination, *,
                                     expected_count=None, cancelled=None):
    """Atomically stream ALL candidate rows to JSON, with bounded RAM usage.

    Display stays limited to the best 200, while export writes every match
    in ascending guest-address order for straightforward cross-run joins.
    No raw RAM snapshots or guest writes. A failed/cancelled export leaves
    no partial or incorrectly named final JSON.
    """
    import json
    import os
    from pathlib import Path
    import tempfile

    a, b, c = _validated_wide_buffers(before, moved, settled)
    path = Path(destination)
    metadata = _report_metadata(before, moved, settled, len(a))
    metadata['display_limit'] = MAX_XYZ_CANDIDATES
    metadata['export_policy'] = 'all_matched_candidates'
    metadata['candidate_order'] = 'guest_address_ascending'
    tmp_path = None
    count = 0
    try:
        with tempfile.NamedTemporaryFile(
                'w', encoding='utf-8', dir=path.parent,
                prefix=f'.{path.name}.', suffix='.tmp',
                delete=False) as output:
            tmp_path = Path(output.name)
            output.write('{\n')
            for name, value in metadata.items():
                output.write('  ' + json.dumps(name) + ': '
                             + json.dumps(value, ensure_ascii=False) + ',\n')
            output.write('  "candidates": [\n')
            for row in _xyz_candidate_rows(a, b, c, cancelled=cancelled):
                if count:
                    output.write(',\n')
                output.write('    ' + json.dumps(row, ensure_ascii=False))
                count += 1
            if cancelled is not None and cancelled():
                raise RuntimeError('XYZ export cancelled after captures changed')
            if expected_count is not None and count != expected_count:
                raise RuntimeError(
                    f'XYZ candidate count mismatch: preview counted {expected_count}, '
                    f'full export found {count}; no JSON committed')
            output.write('\n  ],\n')
            output.write('  "counts": ' + json.dumps({
                'regions_compared': 1, 'observed_changes': count,
                'candidate_count': count, 'reported_candidates': min(
                    count, MAX_XYZ_CANDIDATES),
                'exported_candidates': count
            }) + '\n}\n')
        if cancelled is not None and cancelled():
            raise RuntimeError('XYZ export cancelled after captures changed')
        os.replace(tmp_path, path)
        return count
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()
