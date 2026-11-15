"""Japan-0 original debug-menu transition research, never direct scene writes.

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


def enter_japan_native_debug_menu(rdram, destination: int, *,
                                  expected_context):
    """Only one byte 0x0D→0x0A at 0x800CD284, never a scene-id write.

    The selection is for a USER menu hint only; this does not auto-warp.
    ROM/PID/RDRAM re-verification and explicit consent belong to controller.
    """
    category, index = debug_menu_selection_hint(destination)
    if not isinstance(expected_context, tuple) or len(expected_context) != 6:
        raise ValueError('Missing verified Japanese gameplay context')
    _normal_gameplay(expected_context)
    before = get_japan_debug_context(rdram)
    if before != expected_context:
        raise RuntimeError('Japanese engine/scene context changed since confirmation')
    if get_japan_debug_context(rdram) != before:
        raise RuntimeError('Japanese gameplay context changed during debug-menu validation')
    rdram.write_guest(JAPAN_DEBUG_ENGINE_MODE, bytes([JAPAN_NATIVE_DEBUG_MODE]))
    observed = rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
    if observed not in (JAPAN_NATIVE_DEBUG_MODE, JAPAN_ORDINARY_ENGINE_MODE):
        raise RuntimeError(
            f'Unexpected Japanese debug engine state {observed}; '
            'inspect emulator or restore savestate')
    return DebugMenuEntryResult(
        before_state=JAPAN_ORDINARY_ENGINE_MODE,
        observed_state=observed,
        source_scene=before[1], suggested_destination=destination,
        category_hint=category, menu_index_hint=index,
        changed=True)
