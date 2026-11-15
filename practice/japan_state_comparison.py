"""Read-only Japanese A/B/C memory captures with explicit session provenance.

This module never uses USA pointer, saved-event, stage, or player layouts.
No address discovered here is automatically authorised for a write.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import heapq

from practice.value_search import RDRAM_SIZE, GUEST_BASE, read_ram

JAPAN_FOCUSED_RANGES = (
    ('jp_engine_candidates', 0x800CD000, 0x1000),
    ('jp_inventory_candidates', 0x80161C00, 0x1000),
)
JAPAN_WIDE_RANGE = ('jp_full_rdram', GUEST_BASE, RDRAM_SIZE)
MAX_RESULTS = 1200


@dataclass(frozen=True)
class JapanMemoryRegion:
    name: str
    address: int
    data: bytes


@dataclass(frozen=True)
class JapanMemoryCapture:
    label: str
    utc: str
    identity: tuple
    scope: str
    character: int | None
    map_id: int | None
    regions: tuple[JapanMemoryRegion, ...]


def capture_japan_memory(reader, label: str, *, scope='focused', identity=None):
    """Capture no-player-required Japan-0 guest RAM from a verified reader.

    Identity is ('japan-0', PID, host-RDRAM-base, endian), supplied by the
    connection owner. A different session must never reuse prior captures.
    """
    if scope not in ('focused', 'wide'):
        raise ValueError('Use focused or wide scope')
    if not isinstance(label, str) or not label.strip():
        raise ValueError('A capture label is required')
    if (not isinstance(identity, tuple) or len(identity) != 4
            or identity[0] != 'japan-0'
            or type(identity[1]) is not int or identity[1] <= 0
            or type(identity[2]) is not int or identity[2] <= 0
            or identity[3] not in ('big', 'wordswapped')):
        raise ValueError('Verified Japan-0 PID/RDRAM identity required')

    fields = JAPAN_FOCUSED_RANGES if scope == 'focused' else (JAPAN_WIDE_RANGE,)
    regions = []
    for name, addr, length in fields:
        if scope == 'wide':
            data = read_ram(reader, size=RDRAM_SIZE)
        else:
            data = reader.read_guest(addr, length)
        if len(data) != length:
            raise OSError(f'Incomplete Japanese memory capture for {name}')
        regions.append(JapanMemoryRegion(name, addr, bytes(data)))
    # Only Japanese-native observed globals are used for context.
    map_data = reader.read_guest(0x800CD2A2, 2)
    character_data = reader.read_guest(0x80161DCC, 4)
    if len(map_data) != 2 or len(character_data) != 4:
        raise OSError('Incomplete Japanese scene/character context')
    map_id = int.from_bytes(map_data, 'big')
    character = int.from_bytes(character_data, 'big')
    if character > 3:
        character = None
    return JapanMemoryCapture(
        label.strip(), datetime.now(timezone.utc).isoformat(), identity,
        scope, character, map_id, tuple(regions))


def _capture_context(capture):
    return dict(label=capture.label, utc=capture.utc,
                character=capture.character, map_id=capture.map_id)


def compare_japan_memory(before, after, reverted=None, *, limit=MAX_RESULTS):
    """Rank bounded raw byte candidates; optionally require a C→A reversion.

    The full 8 MiB may change during transitions. Keep at most `limit` result
    dictionaries in memory rather than constructing millions of result rows.
    Counter totals still include changes beyond the displayed shortlist.
    """
    if type(limit) is not int or not 1 <= limit <= MAX_RESULTS:
        raise ValueError('Invalid candidate result limit')
    sources = (before, after) if reverted is None else (before, after, reverted)
    if any(not isinstance(s, JapanMemoryCapture) for s in sources):
        raise ValueError('Japanese memory captures required')
    if any(s.identity != before.identity or s.scope != before.scope for s in sources[1:]):
        raise ValueError('Different Japanese ROM/PID/RDRAM or memory scope; recapture A/B/C')
    if not before.regions:
        raise ValueError('No Japanese memory ranges to compare')

    by_b = {(r.name, r.address): r for r in after.regions}
    by_c = {} if reverted is None else {
        (r.name, r.address): r for r in reverted.regions}
    total_changes = 0
    eligible = 0
    reverting = 0
    compared_regions = 0
    top = []
    for a in before.regions:
        key = (a.name, a.address)
        b = by_b.get(key)
        c = by_c.get(key) if reverted is not None else None
        if b is None or len(b.data) != len(a.data):
            raise ValueError(f'Missing or mismatched Japanese region {a.name} in B')
        if reverted is not None and (c is None or len(c.data) != len(a.data)):
            raise ValueError(f'Missing or mismatched Japanese region {a.name} in C')
        compared_regions += 1
        for offset, (old, new) in enumerate(zip(a.data, b.data)):
            if old == new:
                continue
            total_changes += 1
            returned = c is not None and c.data[offset] == old
            if reverted is not None and not returned:
                continue
            eligible += 1
            if returned:
                reverting += 1
            mask = old ^ new
            binary = old in (0, 1) and new in (0, 1)
            bit = mask.bit_count() == 1
            score = (50 if returned else 0) + (20 if binary else 0) + (
                12 if bit else 0)
            address = a.address + offset
            row = {
                'address': f'0x{address:08X}', 'region': a.name,
                'before': f'{old:02X}', 'after': f'{new:02X}',
                'xor_mask': f'{mask:02X}', 'reverted': returned,
                'score': score, 'kind': ('boolean candidate' if binary else
                                        'one-bit candidate' if bit else 'byte'),
                'width': 1,
            }
            # Higher score first; on ties prefer the earlier guest address.
            entry = (score, -address, row)
            if len(top) < limit:
                heapq.heappush(top, entry)
            elif (score, -address) > top[0][:2]:
                heapq.heapreplace(top, entry)

    rows = [item[2] for item in sorted(top, key=lambda x: (-x[0], -x[1]))]
    return {
        'format': 'goemon-japan-raw-difference-v1',
        'region': 'japan-0',
        'session': {'pid': before.identity[1], 'rdram_base': hex(before.identity[2]),
                    'endian': before.identity[3]},
        'capture_A': _capture_context(before),
        'capture_B': _capture_context(after),
        'capture_C': None if reverted is None else _capture_context(reverted),
        'scope': before.scope,
        'counts': {'regions_compared': compared_regions,
                   'observed_changes': total_changes,
                   'reverting_changes': reverting,
                   'candidate_count': eligible,
                   'reported_candidates': len(rows)},
        'event_flag_changes': [],  # JP event save bank is not mapped.
        'candidates': rows,
        'notes': ('Raw Japan-0 A/B/C guest-byte differences only. No Japanese '
                  'event flag, actor or writable field has been identified. '
                  'Full memory contents are never exported.'),
    }
