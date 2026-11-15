"""Japan-0 native-menu scene warp, matching the USA selector/accept flow.

User has confirmed debug menu entry in Project64. The Japanese category and
stage field offsets are ported from the observed USA menu layout; the user
has requested that we proceed on the assumption that their writes will work.
Only category + stage are staged while engine state 0x0A is active; the game
owns scene loading after a real N64 A input. Direct map/exit writes are banned.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
    JAPAN_DEBUG_LOADING, JAPAN_DEBUG_EXIT,
    JAPAN_NATIVE_DEBUG_MODE, JAPAN_ORDINARY_ENGINE_MODE,
    debug_menu_selection_hint,
)
from practice.native_menu_categories import SCENE_FAMILY_CATEGORY_INDEX
from practice.japanese_position import read_japan_position

# Guest layout parallels observed USA menu category 0x800C7AA4 and
# stage offset 0x800C7AB4, both translated by +0x57F0 for Japan-0.
# This needs live behaviour confirmation; never stage outside original menu.
JAPAN_MENU_CATEGORY = 0x800CD294
JAPAN_MENU_STAGE_INDEX = 0x800CD2A4
JAPAN_MENU_CATEGORY_WIDTH = 1
JAPAN_MENU_STAGE_WIDTH = 2


@dataclass(frozen=True)
class JapanWarpSelection:
    destination: int
    category_name: str
    category_index: int
    stage_index: int


def japan_warp_selection(destination: int) -> JapanWarpSelection:
    name, stage = debug_menu_selection_hint(destination)
    category = SCENE_FAMILY_CATEGORY_INDEX[name]
    if not 0 <= stage <= 0xFFFF:
        raise ValueError('Native menu stage index is out of range')
    return JapanWarpSelection(destination, name, category, stage)


def read_japan_menu_selection(rdram):
    if rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0] != JAPAN_NATIVE_DEBUG_MODE:
        raise RuntimeError('Japanese debug menu is not active')
    category = rdram.read_guest(JAPAN_MENU_CATEGORY, 1)[0]
    stage = int.from_bytes(rdram.read_guest(JAPAN_MENU_STAGE_INDEX, 2), 'big')
    return category, stage


def stage_japan_native_destination(rdram, destination: int):
    """Stage only the native category byte and stage-offset halfword.

    This intentionally does NOT write current scene, pending scene, exit
    request, character index, Goemon XYZ, or any unrelated guest RAM.
    """
    selection = japan_warp_selection(destination)
    if rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0] != JAPAN_NATIVE_DEBUG_MODE:
        raise RuntimeError('Debug menu closed before destination staging')
    writes = (
        (JAPAN_MENU_CATEGORY, bytes([selection.category_index])),
        (JAPAN_MENU_STAGE_INDEX, selection.stage_index.to_bytes(2, 'big')),
    )
    # Stage category first so the native menu's category offset is selected
    # before selecting its specific level index.
    for address, data in writes:
        if rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0] != JAPAN_NATIVE_DEBUG_MODE:
            raise RuntimeError('Debug menu closed; no further writes')
        if rdram.read_guest(address, len(data)) != data:
            rdram.write_guest(address, data)
            if rdram.read_guest(address, len(data)) != data:
                raise RuntimeError(
                    f'Japanese debug selection write-back mismatch at 0x{address:08X}')
    if read_japan_menu_selection(rdram) != (
            selection.category_index, selection.stage_index):
        raise RuntimeError('Japanese original menu rewrote staged selection; A suppressed')
    return selection


def is_japan_scene_loaded(rdram, destination: int):
    """Require actual stable gameplay, not menu-highlight changing the map."""
    if rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0] != JAPAN_ORDINARY_ENGINE_MODE:
        return False
    if int.from_bytes(rdram.read_guest(JAPAN_DEBUG_SCENE, 2), 'big') != destination:
        return False
    if int.from_bytes(rdram.read_guest(JAPAN_DEBUG_LOADING, 4), 'big') != 0:
        return False
    if rdram.read_guest(JAPAN_DEBUG_EXIT, 1)[0] != 0:
        return False
    char = int.from_bytes(rdram.read_guest(JAPAN_DEBUG_CHARACTER, 4), 'big')
    if char not in (0, 1, 2, 3):
        return False
    xyz = read_japan_position(rdram)
    return all(isfinite(value) and abs(value) < 100000 for value in xyz)
