"""Opt-in, US Recomp-only experiments based on user-observed RAM behaviour.

These are NOT validated native game commands. Never infer a correct entrance
from a map ID, nor apply a position write while a destination loads.
"""
from __future__ import annotations

import math
import struct
from practice.checkpoints import MAP_ADDR, PHASE_ADDR, STATE_ADDR, _ensure_capture_safe
from practice.scene_controls import PENDING_MAP_ADDR
from practice.entrances import Spawn
from practice.scene_reload_source import (
    read_usa_reload_source, require_reload_source,
)

ACTIVE_CHARACTER_ADDR = 0x8015C5DC  # u32; area-entry actor loader reads this global

TASK_MOTION_OFFSET = 0x68
GAMEPLAY_STATE = 0x0D
RELOAD_STATE = 0x0C


def _gameplay(ram):
    if ram.u8(STATE_ADDR) != GAMEPLAY_STATE:
        raise ValueError('Experimental write requires normal gameplay (state 0x0D)')
    snap = ram.snapshot()
    if snap.get('loading') or snap.get('player_ptr') is None or snap.get('task_ptr') is None:
        raise ValueError('Game/player is loading or not ready')
    if snap.get('x') is None or snap.get('y') is None or snap.get('z') is None:
        raise ValueError('Player position is unavailable')
    return snap


def stage_reload_trial(ram, destination: int, scenes: dict, *,
                       spawn_character: int | None = None,
                       spawn: Spawn | None = None) -> dict:
    """Stage native entrance then 0x0C with or without a source player object.

    Impact battle (submode 4) uses fixed engine/map/character globals even
    when the ordinary Goemon player/task pointers do not exist. A missing
    source pointer does not justify writing an arbitrary current-map ID.
    The same verified pending-entrance + engine-reload sequence is used;
    destination actor construction/placement remains a separate guarded step.
    """
    if type(destination) is not int or destination not in scenes or not 0 <= destination <= 65535:
        raise ValueError('Choose a known USA destination')
    if spawn_character is not None and (
            type(spawn_character) is not int or spawn_character not in range(4)):
        raise ValueError('Selected spawn character must be 0–3')
    if spawn is not None:
        if not isinstance(spawn, Spawn) or spawn.destination != destination:
            raise ValueError('Spawn does not belong to the destination')
        spawn.validate()

    source_context = require_reload_source(
        read_usa_reload_source(ram), region='USA',
        explicit_character=spawn_character)
    _, origin, current_character, _, submode, _ = source_context
    # A best-effort snapshot validates USA system/RDRAM identity without
    # requiring a player object. It deliberately never invents a pointer.
    snap = ram.snapshot_for_monitoring()
    has_source_actor = bool(
        submode != 4 and snap.get('player_ptr') and snap.get('task_ptr')
        and snap.get('character') is not None
        and all(snap.get(k) is not None for k in ('x', 'y', 'z')))
    if has_source_actor:
        if snap['character'] != current_character:
            raise RuntimeError(
                'Global character disagrees with source player snapshot')
        if spawn is not None:
            guarded = _ensure_capture_safe(ram)
            if ((guarded['player_ptr'], guarded['task_ptr'])
                    != (snap['player_ptr'], snap['task_ptr'])):
                raise RuntimeError('Player changed before spawn staging')
    else:
        # An Impact actor is not a Goemon player. Reacquire the destination
        # player only after the game reconstructs it during the area load.
        snap = dict(snap, player_ptr=None, task_ptr=None,
                    x=None, y=None, z=None)

    if read_usa_reload_source(ram) != source_context:
        raise RuntimeError('USA scene source changed before reload staging')
    previous_pending = ram.read_guest(
        PENDING_MAP_ADDR, 12 if spawn is not None else 2)
    previous_character = ram.read_guest(ACTIVE_CHARACTER_ADDR, 4)
    if previous_character != current_character.to_bytes(4, 'big'):
        raise RuntimeError('USA character global changed before staging')
    selected_character = (
        current_character if spawn_character is None else spawn_character)
    selected_map = (spawn.pending_bytes() if spawn is not None
                    else destination.to_bytes(2, 'big'))
    requested_character = selected_character.to_bytes(4, 'big')
    wrote_character = False
    wrote_pending = False
    try:
        if previous_pending != selected_map:
            ram.write_guest(PENDING_MAP_ADDR, selected_map)
            wrote_pending = True
        if ram.read_guest(PENDING_MAP_ADDR, len(selected_map)) != selected_map:
            raise OSError('Pending destination did not verify; reload not sent')
        if read_usa_reload_source(ram) != source_context:
            raise RuntimeError('USA scene source changed during entrance staging')
        if selected_character != current_character:
            ram.write_guest(ACTIVE_CHARACTER_ADDR, requested_character)
            wrote_character = True
            if ram.read_guest(ACTIVE_CHARACTER_ADDR, 4) != requested_character:
                raise OSError('Character ID did not verify; reload not sent')
        expected_context = (
            source_context[:2] + (selected_character,) + source_context[3:])
        if read_usa_reload_source(ram) != expected_context:
            raise RuntimeError('USA source changed during reload staging')
        # Exactly one engine-mode byte triggers the game's own area loader.
        # Never overwrite the current scene or exit flag.
        ram.write_guest(STATE_ADDR, bytes((RELOAD_STATE,)))
    except Exception:
        # Roll back staged globals only if loading never began. No retry.
        try:
            state = read_usa_reload_source(ram)
            safe = (state[0] == GAMEPLAY_STATE and
                    state[1] == origin and state[3] == 0 and state[5] == 0)
        except (OSError, ValueError, RuntimeError, PermissionError):
            safe = False
        if safe:
            if (wrote_character and ram.read_guest(
                    ACTIVE_CHARACTER_ADDR, 4) == requested_character):
                try:
                    ram.write_guest(ACTIVE_CHARACTER_ADDR, previous_character)
                except (OSError, PermissionError):
                    pass
            if (wrote_pending and ram.read_guest(
                    PENDING_MAP_ADDR, len(selected_map)) == selected_map):
                try:
                    ram.write_guest(PENDING_MAP_ADDR, previous_pending)
                except (OSError, PermissionError):
                    pass
        raise
    return dict(
        destination=destination, source_map=origin,
        source_character=current_character,
        requested_character=selected_character,
        character_staged=wrote_character,
        source_position=[snap[k] for k in ('x', 'y', 'z')],
        task_ptr=snap['task_ptr'], player_ptr=snap['player_ptr'],
        previous_pending=int.from_bytes(previous_pending[:2], 'big'),
        staged_spawn=(dict(
            position=list(spawn.position), heading=spawn.heading,
            mode=spawn.mode, entrance_id=spawn.entrance_id)
            if spawn is not None else None),
        source_player_unavailable=not has_source_actor,
        status='reload_requested_character_and_spawn_unverified')


def task_float_probe(ram, *, direction: int = 1, speedup: bool = False) -> dict:
    """Write ONE f32 at dynamic player task +0x68, without editing +0x6C.

    The 'speedup' label is just a hypothesis: scales the present value or
    applies a small impulse if zero. No claim that this field is velocity.
    """
    if direction not in (-1, 1):
        raise ValueError('Direction must be -1 or +1')
    snap = _gameplay(ram)
    task = snap['task_ptr']
    addr = task + TASK_MOTION_OFFSET
    original = ram.read_guest(addr,4)
    if len(original) != 4: raise OSError('Incomplete player-task float read')
    current = struct.unpack('>f',original)[0]
    if not math.isfinite(current) or abs(current) > 1000:
        raise ValueError('Unreasonable task float; current task/offset may be invalid')
    if speedup:
        target = min(16., max(-16., current*1.5)) if abs(current)>=0.01 else 4.0
    else:
        target = 4.0 * direction
    desired = struct.pack('>f',target)
    if ram.u8(STATE_ADDR) != GAMEPLAY_STATE or ram.snapshot().get('task_ptr') != task:
        raise RuntimeError('Player task changed before experimental float write')
    if ram.read_guest(addr,4) != original:
        raise RuntimeError('Task float changed; repeat test on a new sample')
    # The game may update the float immediately. Record bytes at write time,
    # but don't interpret later rewrites as a failed experiment.
    ram.write_guest(addr,desired)
    return dict(address=f'0x{addr:08X}',task_base=f'0x{task:08X}',
                offset=f'+0x{TASK_MOTION_OFFSET:X}',old_f32=current,new_f32=target,
                bytes_written=desired.hex().upper(),kind='unverified_movement_pulse')
