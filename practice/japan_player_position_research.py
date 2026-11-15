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


def find_japan_xyz_candidates(before, moved, settled, *, limit=MAX_XYZ_CANDIDATES):
    """Rank aligned three-float groups moving A→B then stable at B→C.

    Runs only over complete, equal-length, same-session WIDE snapshots.
    No player task pointer or USA struct offset is assumed. Every result is
    a candidate for manual watch-and-walk validation, not a verified XYZ.
    """
    if type(limit) is not int or not 1 <= limit <= MAX_XYZ_CANDIDATES:
        raise ValueError('XYZ candidate limit must be 1..200')
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

    a, b, c = (memoryview(r.data) for r in (ra, rb, rc))
    unpack = struct.Struct('>fff').unpack_from
    top = []
    possible = 0
    for offset in range(0, len(a) - 11, 4):
        # Skip identical 12-byte groups before decoding expensive floats.
        if a[offset:offset + 12] == b[offset:offset + 12]:
            continue
        av = unpack(a, offset)
        bv = unpack(b, offset)
        cv = unpack(c, offset)
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
        # XYZ structures with a nearly unchanged vertical coordinate and
        # a settled endpoint are promising, but false positives are expected.
        possible += 1
        score = (round(50.0 - min(50.0, stable * 60.0), 3)
                 + (20 if abs(dy) <= 0.25 else 0)
                 + (10 if abs(dx) >= 0.75 and abs(dz) >= 0.75 else 0)
                 + (10 if 2.0 <= horizontal <= 250.0 else 0))
        address = GUEST_BASE + offset
        if len(top) >= limit and (score, -address) <= top[0][:2]:
            continue
        def fmt(v):
            return '(' + ', '.join(f'{x:.2f}' for x in v) + ')'
        row = {
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
        entry = (score, -address, row)
        if len(top) < limit:
            heapq.heappush(top, entry)
        else:
            heapq.heapreplace(top, entry)

    rows = [entry[2] for entry in sorted(top, key=lambda x: (-x[0], -x[1]))]
    return {
        'format': 'goemon-japan-xyz-heuristic-v1',
        'region': 'japan-0',
        'scope': 'wide',
        'session': {'pid': before.identity[1],
                    'rdram_base': hex(before.identity[2]),
                    'endian': before.identity[3],
                    'guest_ram_size': len(a)},
        'capture_A': _xyz_context(before),
        'capture_B': _xyz_context(moved),
        'capture_C': _xyz_context(settled),
        'counts': {'regions_compared': 1, 'observed_changes': possible,
                   'candidate_count': possible,
                   'reported_candidates': len(rows)},
        'event_flag_changes': [],
        'candidates': rows,
        'notes': ('Read-only aligned f32 XYZ-like triplets. A=stationary, '
                  'B=walked to new position, C=stationary at B. '
                  'A candidate can belong to scenery, NPCs or calculations. '
                  'No Japanese player pointer/XYZ field is confirmed. '
                  'The exported JSON omits all raw memory snapshots.'),
    }
