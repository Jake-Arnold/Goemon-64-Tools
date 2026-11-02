"""Read-only live watch for candidate N64 debug-menu selectors.

Never writes RAM or assumes that a matching value proves cursor semantics.
Uses guest big-endian bytes, independent of Goemon64Recomp's host RDRAM order.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class WatchedField:
    key: str
    label: str
    address: int
    width: int
    confidence: str


FIELDS = (
    WatchedField('state', 'Original menu state', 0x800C7A94, 1, 'Known: 10 = original debug menu'),
    WatchedField('scene_candidate', 'Stage offset (category)', 0x800C7AB4, 2, 'Verified native menu stage offset in state 10'),
    WatchedField('character_candidate', 'Character-state value (not cursor)', 0x800C7AAC, 2, 'Does not follow character highlights in debug menu'),
    WatchedField('submode', 'Native debug category', 0x800C7AA4, 1, 'When state 10: 0 MAIN, 1 SIRO, 2 DOUCHU, 3 MACHI, 4 SHOP, ... (user-observed)'),
    WatchedField('live_map', 'Absolute map ID', 0x800C7AB2, 2, 'Menu map ID = category base + stage offset; updates before load'),
    WatchedField('live_character', 'Active character (control)', 0x8015C5DC, 4, 'Loaded character; may differ from menu highlight'),
    WatchedField('phase', 'Game phase', 0x800C7A9E, 1, 'Known: 1 during stable ordinary gameplay'),
    WatchedField('exit_request', 'Exit request', 0x800C7A9F, 1, 'Known transition/exit flag'),
    WatchedField('pending_map', 'Pending scene', 0x800C7CA0, 2, 'Pending scene; does not identify the menu hover'),
    WatchedField('hover_pointer', 'Character menu entry pointer', 0x800C7E60, 4, 'Candidate: Goemon=0x8007BAD0, +12 bytes per character; READ ONLY'),
)


def read_fields(mem):
    values = {}
    for f in FIELDS:
        value = int.from_bytes(mem.read_guest(f.address, f.width), 'big')
        values[f.key] = value
    return values


def changed_fields(previous, current):
    return {key: (previous[key], value) for key, value in current.items()
            if key in previous and previous[key] != value}



def make_change_event(previous: dict, current: dict, utc: str):
    """Retain changes regardless of game state (including 10→13, loading).

    v0.9.3 silently discarded EVERY change recorded during gameplay or other
    transition states, so its exported log couldn't prove a successful load.
    """
    changes=changed_fields(previous,current)
    if not changes:
        return None
    return {'utc':utc,'kind':'change','values':dict(current),
            'changed':{k:list(pair) for k,pair in changes.items()}}


def can_mark_state(state: int):
    """User-labelled snapshots are useful both in menu and normal gameplay."""
    return state in (10,13)


# Observed in eight repeated forward/reverse native character menu captures.
# This is a pointer into an apparent four-entry menu table, not a literal
# character ID and NOT proven safe to write. Other builds may differ.
CHARACTER_MENU_POINTER_BASE = 0x8007BAD0
CHARACTER_MENU_POINTER_STRIDE = 12
CHARACTER_MENU_NAMES = ('Goemon', 'Ebisumaru', 'Sasuke', 'Yae')

def decode_hover_pointer(pointer: int):
    """Return matching observed name only for an exact table entry pointer.

    None means unrecognised rather than guessing a character or dereferencing
    a pointer outside a verified range. Does not access game memory.
    """
    if type(pointer) is not int:
        return None
    offset = pointer - CHARACTER_MENU_POINTER_BASE
    if offset < 0 or offset % CHARACTER_MENU_POINTER_STRIDE:
        return None
    index = offset // CHARACTER_MENU_POINTER_STRIDE
    return CHARACTER_MENU_NAMES[index] if index < len(CHARACTER_MENU_NAMES) else None
