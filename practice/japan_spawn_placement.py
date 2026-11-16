"""One-shot Japanese post-load XYZ placement for the shared USA entrance atlas.

The USA toolkit both stages an entrance record before 0x0C and performs a
guarded one-shot post-load XYZ placement. Japan now follows the same policy.
Only Goemon's vector (0x80151B10) in Oedo Town South (0x161) has
user-verified writable semantics. The shared atlas covers other scenes,
but staging the selected entrance is not permission to write this vector.
"""
from __future__ import annotations

import struct

from practice.entrances import Spawn
from practice.japanese_position import (
    JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE, JAPAN_OEDO_SOUTH_SCENE,
    checked_japan_xyz, read_japan_position,
)
from practice.japanese_debug_warp import get_japan_debug_context, _normal_gameplay


def place_japan_spawn_once(rdram, spawn: Spawn, *, expected_before: bytes):
    """Write exactly one Japanese Goemon XYZ vector after the destination loads.

    The caller has to reopen a region-verified writable RDRAM handle and
    ensure the matching PID/base/ROM, just as for every other JP native writer.
    No retries, character mutations, or unverified task/velocity writes.
    """
    spawn.validate()
    if spawn.destination != JAPAN_OEDO_SOUTH_SCENE:
        raise RuntimeError(
            'Japanese post-load XYZ writes are verified only for Goemon '
            'in Oedo Town South (0x161); other scenes use native entrance staging')
    if not isinstance(expected_before, bytes) or len(expected_before) != JAPAN_PLAYER_XYZ_SIZE:
        raise ValueError("Expected Japanese pre-placement XYZ must be 12 bytes")
    expected = checked_japan_xyz(spawn.position)
    desired = struct.pack(">fff", *expected)
    before = get_japan_debug_context(rdram)
    _normal_gameplay(before)
    if before[1] != spawn.destination:
        raise RuntimeError("Japanese destination scene changed before XYZ placement")
    if before[2] != 0:
        raise RuntimeError("Japanese post-load XYZ placement is validated only for Goemon")
    if rdram.read_guest(JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE) != expected_before:
        raise RuntimeError("Japanese player position moved; no stale XYZ write")
    if desired == expected_before:
        return expected
    # Recheck the scene/character/loading after reading the original vector.
    if get_japan_debug_context(rdram) != before:
        raise RuntimeError("Japanese scene or character changed during XYZ placement")
    rdram.write_guest(JAPAN_PLAYER_XYZ_START, desired)
    observed = rdram.read_guest(JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE)
    if observed != desired:
        raise RuntimeError("Japanese XYZ write-back differs from USA entrance coordinates")
    if get_japan_debug_context(rdram) != before:
        raise RuntimeError("Japanese scene/character changed immediately after XYZ placement")
    return read_japan_position(rdram)
