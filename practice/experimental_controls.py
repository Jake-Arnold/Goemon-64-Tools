"""Opt-in, US Recomp-only experiments based on user-observed RAM behaviour.

These are NOT validated native game commands. Never infer a correct entrance
from a map ID, nor apply a position write while a destination loads.
"""
from __future__ import annotations

import math
import struct
from practice.checkpoints import MAP_ADDR, PHASE_ADDR, STATE_ADDR
from practice.scene_controls import PENDING_MAP_ADDR

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


def stage_reload_trial(ram, destination: int, scenes: dict, *, spawn_character: int | None = None) -> dict:
    """Experimental native-style area reload, optionally staging the spawn ID.

    The original area-entry model loader reads the global u32 character ID.
    Unlike ordinary gameplay writes, this one is immediately followed by the
    game's full 0x0C area reload. The original game may override the ID during
    teardown; the UI must verify BOTH global and task-local character on load.
    No post-load C-Down is synthesized. Do not write the old player task ID.
    """
    if type(destination) is not int or destination not in scenes or not 0 <= destination <= 65535:
        raise ValueError('Choose a known USA destination')
    if spawn_character is not None and (type(spawn_character) is not int or spawn_character not in range(4)):
        raise ValueError('Selected spawn character must be 0–3')
    snap = _gameplay(ram)
    origin = ram.u16(MAP_ADDR)
    previous_pending = ram.read_guest(PENDING_MAP_ADDR, 2)
    previous_character = ram.read_guest(ACTIVE_CHARACTER_ADDR, 4)
    current_character = int.from_bytes(previous_character,'big')
    if current_character not in range(4) or snap.get('character') != current_character:
        raise RuntimeError('Global character disagrees with player snapshot; refusing to stage reload')
    selected_character = current_character if spawn_character is None else spawn_character
    if ram.u8(STATE_ADDR) != GAMEPLAY_STATE or ram.u16(MAP_ADDR) != origin:
        raise RuntimeError('Game changed while preparing the reload')
    selected_map = destination.to_bytes(2,'big')
    desired_character = selected_character.to_bytes(4,'big')
    wrote_character = False
    wrote_pending = False
    try:
        # Stage the destination and character BEFORE requesting state 0x0C.
        # Every step is verified while we still have stable gameplay state.
        ram.write_guest(PENDING_MAP_ADDR, selected_map)
        wrote_pending = True
        if ram.read_guest(PENDING_MAP_ADDR,2) != selected_map:
            raise OSError('Pending destination did not verify; reload not requested')
        if selected_character != current_character:
            if ram.read_guest(ACTIVE_CHARACTER_ADDR,4) != previous_character:
                raise RuntimeError('Character changed while staging the reload')
            ram.write_guest(ACTIVE_CHARACTER_ADDR,desired_character)
            wrote_character = True
            if ram.read_guest(ACTIVE_CHARACTER_ADDR,4) != desired_character:
                raise OSError('Staged character ID did not verify; reload not requested')
        if ram.u8(STATE_ADDR) != GAMEPLAY_STATE or ram.u16(MAP_ADDR) != origin:
            raise RuntimeError('Game left the source scene before reload request')
        ram.write_guest(STATE_ADDR, bytes((RELOAD_STATE,)))
    except Exception:
        # Restore only while still in the unmodified source gameplay state.
        # Never roll back the character after loading has started, as doing so
        # could desynchronise a partially constructed actor or graphics buffer.
        try:
            safe = (ram.u8(STATE_ADDR) == GAMEPLAY_STATE and ram.u16(MAP_ADDR) == origin)
        except (OSError,ValueError):
            safe = False
        if safe:
            if wrote_character and ram.read_guest(ACTIVE_CHARACTER_ADDR,4) == desired_character:
                try:ram.write_guest(ACTIVE_CHARACTER_ADDR,previous_character)
                except OSError:pass
            if wrote_pending and ram.read_guest(PENDING_MAP_ADDR,2) == selected_map:
                try:ram.write_guest(PENDING_MAP_ADDR,previous_pending)
                except OSError:pass
        raise
    return dict(destination=destination, source_map=origin, source_character=current_character,
                requested_character=selected_character, character_staged=wrote_character,
                source_position=[snap[k] for k in ('x','y','z')],
                task_ptr=snap['task_ptr'], previous_pending=int.from_bytes(previous_pending,'big'),
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
