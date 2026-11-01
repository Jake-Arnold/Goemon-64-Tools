"""Read-only repeated character-hover scanner for original N64 debug menu.

Scan genuine original N64 guest memory (including the level-select overlay).
No writes, host-process addresses, ROM assets, or raw dumps in reports.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from collections import Counter
import time

SCAN_BASE = 0x80080000
SCAN_SIZE = 0x00380000  # through 0x803FFFFF, incl. original level-select overlay
MENU_STATE = 10
ORDER = (0, 1, 2, 3, 3, 2, 1, 0)
CHARACTERS = ('Goemon', 'Ebisumaru', 'Sasuke', 'Yae')


@dataclass(frozen=True)
class CursorCapture:
    character: int
    first: bytes
    second: bytes
    context: dict


def menu_context(ram):
    """Read known game/menu state; used to prevent mismatched captures."""
    return {
        'state': ram.u8(0x800C7A94),
        'category': ram.u8(0x800C7AA4),
        'stage_offset': ram.u16(0x800C7AB4),
        'absolute_map': ram.u16(0x800C7AB2),
        'active_character': ram.u32(0x8015C5DC),
    }


def capture_cursor(ram, character: int, *, base=SCAN_BASE, size=SCAN_SIZE,
                   delay=0.30, sleeper=time.sleep):
    if character not in range(4):
        raise ValueError('Invalid highlighted character')
    before = menu_context(ram)
    if before['state'] != MENU_STATE:
        raise ValueError('Original native debug menu must be open (state 10)')
    first = ram.read_guest(base, size)
    sleeper(delay)
    second = ram.read_guest(base, size)
    after = menu_context(ram)
    if before != after:
        raise ValueError('Game state/category/stage/active character changed during capture. Repeat this character.')
    if len(first) != size or len(second) != size:
        raise ValueError('Incomplete RDRAM capture')
    return CursorCapture(character, first, second, before)


def validate_sequence(captures):
    chars = tuple(c.character for c in captures)
    if chars != ORDER:
        raise ValueError('Expected Goemon, Ebisumaru, Sasuke, Yae, then Yae, Sasuke, Ebisumaru, Goemon')
    if not captures:
        raise ValueError('No captures')
    size = len(captures[0].first)
    if not size or any(len(c.first) != size or len(c.second) != size for c in captures):
        raise ValueError('RAM snapshots have inconsistent sizes')
    context = captures[0].context
    if context.get('state') != MENU_STATE or any(c.context != context for c in captures):
        raise ValueError('Category, stage/map, active character, or menu state changed between captures. Record only character highlights on the same menu.')


def _pattern_kind(v):
    if v == (0, 1, 2, 3):
        return ('zero_based', 0, 1, 0)
    if v == (1, 2, 3, 4):
        return ('one_based', 1, 1, 1)
    step = v[1]-v[0]
    if step and v[2] == v[0] + 2*step and v[3] == v[0] + 3*step:
        priority = 2 if 0 < abs(step) <= 64 else 3
        return ('linear', v[0], step, priority)
    return ('lookup', v[0], None, 4)


def find_cursor_candidates(captures, *, base=SCAN_BASE):
    """Require every value to be stable for 300ms and reproduce on return.

    Reject byte-offset/width misalignment and arbitrary changing gameplay buffers.
    Exact 0..3/1..4 matches are ranked above pointer/index encodings.
    The fallback lookup admits distinct, repeated non-linear encodings; no
    discovered field is automatically made writable.
    """
    validate_sequence(captures)
    size = len(captures[0].first)
    first = [c.first for c in captures]
    second = [c.second for c in captures]
    out = []
    a, b = first[:2]
    aa, bb = second[:2]
    for width in (1, 2, 4):
        # The capture scan starts on a 4-byte boundary.
        if base % width:
            raise ValueError('Scan start must align to candidate width')
        for off in range(0, size-width+1, width):
            v0 = a[off:off+width]
            v1 = b[off:off+width]
            if v0 == v1 or v0 != aa[off:off+width] or v1 != bb[off:off+width]:
                continue
            # All four characters must differ, and all eight readings must
            # remain unchanged across their two snapshots.
            keys = (v0, v1, first[2][off:off+width], first[3][off:off+width])
            if len(set(keys)) != 4:
                continue
            if any(first[i][off:off+width] != second[i][off:off+width] for i in range(2,8)):
                continue
            if (first[4][off:off+width] != keys[3] or
                first[5][off:off+width] != keys[2] or
                first[6][off:off+width] != keys[1] or
                first[7][off:off+width] != keys[0]):
                continue
            values = tuple(int.from_bytes(x, 'big') for x in keys)
            kind, origin, stride, rank = _pattern_kind(values)
            out.append({
                'addr': f'0x{base+off:08X}', 'width': width,
                'encoding': kind, 'values': list(values),
                'base_value': origin, 'stride': stride,
                'verified_samples': 8, 'stability_checks': 8,
                '_rank': rank,
            })
    out.sort(key=lambda c: (c['_rank'], c['width'] != 1, c['width'], int(c['addr'],16)))
    for c in out:del c['_rank']
    return out


def make_cursor_report(captures, candidates, *, base=SCAN_BASE):
    validate_sequence(captures)
    return {
        'format': 'mnsg-usa-native-character-cursor-candidates-v1',
        'utc': datetime.now(timezone.utc).isoformat(),
        'scan_range': {'start': f'0x{base:08X}', 'end_exclusive': f'0x{base+len(captures[0].first):08X}'},
        'capture_order': [{'character': x.character, 'name': CHARACTERS[x.character]} for x in captures],
        'game_context': captures[0].context,
        'total_candidates': len(candidates),
        'encoding_counts': dict(Counter(c['encoding'] for c in candidates)),
        'candidates': candidates,
        'notes': 'Read-only N64 RAM comparisons. Eight stable highlights in forward and reverse order. No raw RAM dumps, no host pointers, no automatic memory writes. Cursor hypotheses require live validation.',
    }
