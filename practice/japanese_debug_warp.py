"""Japan-0 original debug-menu entry: only 0x800CD284 is written.

The externally documented engine-mode byte is 0x800CD284 (0x0A debug).
The L-trigger cheat and US original debug menu use that engine mode.
Unlike an exit-bit/pending-map trick, a real game menu can own loading,
resources and spawn data. The Japan-0 path needs LIVE testing; menu cursor
selection and commit are still unmapped. No automatic destination warp here.
"""
from __future__ import annotations
from dataclasses import dataclass
from practice.scenes import SCENES
from practice.scene_controls import NATIVE_DEBUG_CATEGORIES

JAPAN_DEBUG_ENGINE_MODE = 0x800CD284
JAPAN_ORDINARY_ENGINE_MODE = 0x0D
JAPAN_NATIVE_DEBUG_MODE = 0x0A
JAPAN_DEBUG_SCENE = 0x800CD2A2
JAPAN_DEBUG_CHARACTER = 0x80161DCC
JAPAN_DEBUG_LOADING = 0x80161DC4
JAPAN_DEBUG_SUBMODE = 0x800CD294
JAPAN_DEBUG_EXIT = 0x800CD28F


@dataclass(frozen=True)
class DebugMenuEntryResult:
    before_state: int
    observed_state: int
    source_scene: int
    suggested_destination: int
    category_hint: str
    menu_index_hint: int
    changed: bool


def debug_menu_selection_hint(scene: int):
    """USA-derived menu category/index; not confirmed for native Japan menu."""
    if type(scene) is not int or scene not in SCENES:
        raise ValueError('Select a catalogued scene before opening the debug menu')
    for first_id, category in NATIVE_DEBUG_CATEGORIES:
        if scene >= first_id:
            return category, scene - first_id
    raise ValueError('Unknown native debug menu category')


def get_japan_debug_context(rdram):
    state = rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
    scene = int.from_bytes(rdram.read_guest(JAPAN_DEBUG_SCENE, 2), 'big')
    char = int.from_bytes(rdram.read_guest(JAPAN_DEBUG_CHARACTER, 4), 'big')
    loading = int.from_bytes(rdram.read_guest(JAPAN_DEBUG_LOADING, 4), 'big')
    submode = rdram.read_guest(JAPAN_DEBUG_SUBMODE, 1)[0]
    exit_flag = rdram.read_guest(JAPAN_DEBUG_EXIT, 1)[0]
    return state, scene, char, loading, submode, exit_flag


def _normal_gameplay(context):
    state, scene, character, loading, submode, exit_flag = context
    if (state != JAPAN_ORDINARY_ENGINE_MODE or not 0 < scene < 0x800
            or character not in (0, 1, 2, 3) or loading != 0 or
            submode not in (0, 1, 2, 3) or exit_flag != 0):
        raise RuntimeError(
            f'Debug menu refused: engine={state}, scene=0x{scene:03X}, '
            f'character={character}, loading={loading}, '
            f'submode={submode}, exit={exit_flag}; '
            'requires stable gameplay as any playable character')


def enter_japan_native_debug_menu(rdram, destination=None, *,
                                  expected_context=None):
    """Unrestricted original Japan debug menu: engine mode byte only.

    The connected writer must already have been verified for the correct
    Japanese executable, PID and RDRAM layout. Engine state, gameplay,
    loading, cutscene, character, source scene and destination are not
    preconditions. No dialog, artificial input or other RAM edit occurs here.

    The legacy destination/context parameters are accepted as *hints* only
    so older callers cannot accidentally re-enable gameplay restrictions.
    """
    before = rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
    changed = before != JAPAN_NATIVE_DEBUG_MODE
    if changed:
        # An exact physical byte write is required: a swapped 2/4-byte
        # read-modify-write could overwrite neighboring live engine fields.
        rdram.write_guest_byte_exact(
            JAPAN_DEBUG_ENGINE_MODE, JAPAN_NATIVE_DEBUG_MODE)
    observed = rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
    if observed != JAPAN_NATIVE_DEBUG_MODE:
        raise RuntimeError(
            f'Japanese engine mode 0x0A did not verify; read 0x{observed:02X}')
    # Scene selection is only a display hint; opening the original debug
    # menu never stages a map, entrance, character, or button press.
    scene = 0
    try:
        scene = int.from_bytes(rdram.read_guest(JAPAN_DEBUG_SCENE, 2), 'big')
    except (ValueError, OSError, PermissionError):
        pass
    hint = destination if type(destination) is int else None
    try:
        category, index = debug_menu_selection_hint(hint)
    except ValueError:
        category, index = '', -1
    return DebugMenuEntryResult(
        before_state=before, observed_state=observed,
        source_scene=scene, suggested_destination=hint,
        category_hint=category, menu_index_hint=index, changed=changed)
