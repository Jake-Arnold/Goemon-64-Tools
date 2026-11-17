"""Region-qualified persistent flags for the shared Unlocks > Flags page.

The USA entries reuse Story Progress's existing named bit catalogue and
checked writer. All Japanese crosswalk entries have editable Set/Clear
controls for direct gameplay testing, even when the address remains only an
offset candidate. An edit is NOT evidence that an event meaning is proven.
"""
from __future__ import annotations

from dataclasses import dataclass

from practice.story_progress import (
    FLAGS, CURATED_FLAGS, PLASMA_FLAGS, EXTERNAL_FLAGS,
    PLACEMENT_PICKUPS, DOLL_PLACEMENT_FLAGS, SAVED_BASE,
    story_section_for_key,
)
from practice.region_memory_crosswalk import CROSS_REGION_BY_KEY
from practice.region_unlocks import REGION_DELTA


@dataclass(frozen=True)
class UnlockFlag:
    key: str
    label: str
    group: str
    address: int
    mask: int
    source: str
    evidence: str
    editable: bool

    def __post_init__(self):
        if not (0x80000000 <= self.address < 0x80800000):
            raise ValueError('Flag outside guest memory')
        if not (0 < self.mask < 256 and self.mask.bit_count() == 1):
            raise ValueError('Flag must be exactly one bit')


def _usa_source(flag):
    if flag in PLASMA_FLAGS:
        return 'ROM/Plasma'
    if flag in EXTERNAL_FLAGS:
        return 'External annotation'
    if flag in PLACEMENT_PICKUPS or flag in DOLL_PLACEMENT_FLAGS:
        return 'ROM pickup lead'
    return 'Curated research'


USA_FLAGS = tuple(
    UnlockFlag(flag.key, flag.label, story_section_for_key(flag.key),
               flag.address, flag.mask, _usa_source(flag),
               flag.evidence, True)
    for flag in FLAGS
)

# Every mapped JP event/Plasma crosswalk is editable for direct experiments.
# Candidate labels identify evidence quality, not write access. External and
# placement flags are not currently in the canonical reciprocal crosswalk.
JAPAN_FLAGS = tuple(
    UnlockFlag(flag.key, flag.label, story_section_for_key(flag.key),
               CROSS_REGION_BY_KEY[
                   ('plasma:' if flag in PLASMA_FLAGS else 'event:') + flag.key
               ].japan,
               flag.mask,
               'JP user-confirmed' if CROSS_REGION_BY_KEY[
                   ('plasma:' if flag in PLASMA_FLAGS else 'event:') + flag.key
               ].evidence == 'user-confirmed' else 'JP offset candidate',
               CROSS_REGION_BY_KEY[
                   ('plasma:' if flag in PLASMA_FLAGS else 'event:') + flag.key
               ].note,
               True)
    for flag in CURATED_FLAGS + PLASMA_FLAGS
)

assert len({f.key for f in USA_FLAGS}) == len(USA_FLAGS)
assert len({f.key for f in JAPAN_FLAGS}) == len(JAPAN_FLAGS)
assert all(f.editable for f in JAPAN_FLAGS)


def flags_for_region(region):
    if region == 'usa':
        return USA_FLAGS
    if region == 'japan':
        return JAPAN_FLAGS
    raise ValueError(f'Unsupported game region: {region}')


def read_flag_bytes(ram, region, flags=None):
    """One bounded 100-byte guest read, preserving raw bytes for CAS writes.

    None denotes unavailable, never a false/clear flag. A crosswalk candidate
    can be *observed* at an offset but cannot be called a proven game event.
    """
    flags = flags_for_region(region) if flags is None else tuple(flags)
    if ram is None:
        return {}
    base = SAVED_BASE + (REGION_DELTA if region == 'japan' else 0)
    if region not in ('usa', 'japan'):
        raise ValueError('Unsupported region')
    for flag in flags:
        if not base <= flag.address < base + 0x64:
            raise ValueError('Not in the 100-byte saved event bank')
    data = ram.read_guest(base, 0x64)
    if len(data) != 0x64:
        raise OSError('Incomplete saved event bank read')
    return {flag.key: data[flag.address - base] for flag in flags}


def masked_flag_byte(flag, target, expected):
    """Propose a single byte preserving unrelated packed story bits."""
    if target not in ('Set', 'Clear'):
        raise ValueError('Target must be Set or Clear')
    if not isinstance(expected, int) or not 0 <= expected <= 0xFF:
        raise ValueError('Expected guest byte unavailable')
    return (expected | flag.mask) if target == 'Set' else (expected & ~flag.mask)


def write_japan_crosswalk_flag(writer, flag, target, expected):
    """Single mapped JP bit CAS via toolkit's connected raw writer.

    Candidate evidence does not block experiments, but an unknown/unmapped
    address is not silently promoted into this catalogue.
    """
    if flag not in JAPAN_FLAGS:
        raise ValueError('Address has no saved-event crosswalk entry')
    data = bytes((masked_flag_byte(flag, target, expected),))
    return writer(flag.address, data, expected=bytes((expected,)))
