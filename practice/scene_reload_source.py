"""Shared source-state contract for experimental native 0x0C area reloads.

USA and Japan pass the same six scene globals in the same order. This module
does NOT assert that their address layouts are interchangeable: the verified
regional readers supply their respective values.

A missing player/task is not by itself evidence of loading. In particular,
Impact combat is observed at gameplay submode 4, which has no normal actor.
Only engine 0x0D, a plausible scene, no loader or exit request, and submodes
0..4 may request the existing staged 0x0C path. This remains experimental.
"""
from __future__ import annotations


ENGINE_GAMEPLAY = 0x0D
ENGINE_RELOAD = 0x0C
SCENE_SUBMODES = frozenset((0, 1, 2, 3, 4))


def require_reload_source(context, *, region, explicit_character=None):
    """Validate fixed globals, never the existence of a dynamic player pointer.

    Context is (engine, current_scene, character_global, loading, submode,
    exit_flag). Missing/unknown character requires an explicit target choice.
    No raw memory writes are performed by this function.
    """
    if not isinstance(context, tuple) or len(context) != 6:
        raise ValueError('Complete six-field scene context is required')
    state, scene, character, loading, submode, exit_flag = context
    if explicit_character is not None and (
            type(explicit_character) is not int
            or explicit_character not in range(4)):
        raise ValueError('Target character must be 0–3')
    if (type(state) is not int or state != ENGINE_GAMEPLAY
            or type(scene) is not int or not 0 <= scene < 0x800
            or type(loading) is not int or loading != 0
            or type(submode) is not int or submode not in SCENE_SUBMODES
            or type(exit_flag) is not int or exit_flag != 0):
        raise RuntimeError(
            f'{region} scene reload refused: engine=0x{state:02X}, '
            f'scene=0x{scene:03X}, loading={loading}, '
            f'submode={submode}, exit={exit_flag}. '
            'Expected stable engine 0x0D, no active loading/exit, '
            'and observed gameplay submode 0–4 (including Impact battle). '
            'Original debug mode 0x0A is a separate manual action.')
    if type(character) is not int:
        raise ValueError('Character global must be an integer')
    if character not in range(4) and explicit_character is None:
        raise RuntimeError(
            f'{region} current character {character} is unavailable; '
            'choose Goemon/Ebisumaru/Sasuke/Yae explicitly instead of '
            'Keep current character.')
    return context


def read_usa_reload_source(ram):
    """Read the six independently mapped original-USA static globals."""
    from autosplitter.memory import CHARACTER_ID_ADDR, LOADING_FLAG_ADDR
    from practice.checkpoints import STATE_ADDR, MAP_ADDR, SUBMODE_ADDR, EXIT_ADDR
    return (
        ram.u8(STATE_ADDR), ram.u16(MAP_ADDR),
        ram.u32(CHARACTER_ID_ADDR), ram.u32(LOADING_FLAG_ADDR),
        ram.u8(SUBMODE_ADDR), ram.u8(EXIT_ADDR),
    )
