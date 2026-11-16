"""User-verified Japanese inventory progress shown in shared Story Progress.

Not a Japanese saved-event bitfield and not a translation of USA story bits.
All 17 selected fields already exist in the Japanese 33-row live-tested Unlocks
catalogue. No new RAM addresses are inferred here.
"""
from __future__ import annotations

from practice.unlocks import UNLOCKS
from practice.region_unlocks import japan_unlock_lead, japan_unlock_display_value

JAPAN_PROGRESS_SECTIONS = {
    'goemon_in_party': 'Other story',
    'ebisumaru_in_party': 'Other story',
    'sasuke_in_party': 'Other story',
    'yae_in_party': 'Other story',
    'silver_fortune_doll_progress': 'Fortune Dolls',
    'lord_s_pass': 'Keys & Locks',
    'gold_key': 'Keys & Locks',
    'triton_shell': 'Keys & Locks',
    'achilles_heel': 'Benkei & Kihachi',
    'cucumber': 'Collectibles & Miracles',
    'red_fish_count': 'Ushiwaka & Training',
    'blue_fish_count': 'Ushiwaka & Training',
    'yellow_fish_count': 'Ushiwaka & Training',
    'star': 'Collectibles & Miracles',
    'moon': 'Collectibles & Miracles',
    'flower': 'Collectibles & Miracles',
    'snowflake': 'Collectibles & Miracles',
}
JAPAN_PROGRESS_ITEMS = {
    item.slug: item for item in UNLOCKS if item.slug in JAPAN_PROGRESS_SECTIONS
}
assert len(JAPAN_PROGRESS_SECTIONS) == len(JAPAN_PROGRESS_ITEMS) == 17
assert all(japan_unlock_lead(item).user_verified
           for item in JAPAN_PROGRESS_ITEMS.values())


def japan_progress_row(item, reader):
    """Fresh read of a verified Japanese inventory-progress byte."""
    lead = japan_unlock_lead(item)
    if item.slug not in JAPAN_PROGRESS_SECTIONS or not lead.user_verified:
        raise ValueError('Not a live-verified Japanese progress entry')
    raw = None
    if reader is not None:
        try:
            data = reader.read_guest(lead.address, lead.width)
            if len(data) != lead.width:
                raise OSError('Short Japanese progress read')
            raw = int.from_bytes(data, 'big')
        except (OSError, ValueError, RuntimeError, PermissionError):
            pass
    display = japan_unlock_display_value(item, raw) if raw is not None else None
    return {
        'key': 'jp_unlock_' + item.slug,
        'name': item.label,
        'section': JAPAN_PROGRESS_SECTIONS[item.slug],
        'bank': 'JP confirmed inventory',
        'address': lead.address,
        'mask': '—',
        'value': ('—' if display is None else f'0x{display:02X}'),
        'raw': ('—' if raw is None else f'0x{raw:02X}'),
        'source': ('User-reported live-verified Japanese unlock; '
                   'inventory progress, not a mapped Japanese saved-event bit'),
    }


def japan_progress_edit_options(item):
    if item.slug not in JAPAN_PROGRESS_SECTIONS:
        return ()
    values = (range(item.max_value + 1) if item.quantity else item.values)
    return tuple(f'0x{value:02X}' for value in values)
