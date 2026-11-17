"""Region-qualified persistent flags for the shared Unlocks > Flags page.

The USA entries reuse Story Progress's existing named bit catalogue and
checked writer. Japanese entries are crosswalk observations, NOT automatic
write permissions: only independently user-confirmed JP event bits may be
toggled. A similar byte or +0x57F0 by itself never authorises a write.
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

# Crosswalk catalogue currently records one independently confirmed JP saved
# event: Benkei encounter. Other event/Plasma entries are research candidates
# even when their USA reader is known. Never translate external/placement bits
# as a blanket offset.
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
               CROSS_REGION_BY_KEY[
                   ('plasma:' if flag in PLASMA_FLAGS else 'event:') + flag.key
               ].evidence == 'user-confirmed')
    for flag in CURATED_FLAGS + PLASMA_FLAGS
)

assert len({f.key for f in USA_FLAGS}) == len(USA_FLAGS)
assert len({f.key for f in JAPAN_FLAGS}) == len(JAPAN_FLAGS)
assert sum(f.editable for f in JAPAN_FLAGS) == 1
assert next(f for f in JAPAN_FLAGS if f.editable).key == 'benkei_encounter'


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


def write_confirmed_japan_flag(writer, flag, target, expected):
    """Single allowlisted JP byte CAS via toolkit's verified raw writer."""
    if flag not in JAPAN_FLAGS or not flag.editable:
        raise PermissionError('Japanese event flag has not been independently confirmed')
    data = bytes((masked_flag_byte(flag, target, expected),))
    return writer(flag.address, data, expected=bytes((expected,)))
