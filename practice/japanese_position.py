"""Japan-0 experimental *bounded* position writes backed by user gameplay tests.

Validated only for Goemon (index 0) in Oedo Town South (scene 0x0161).
Position offsets are fixed guest addresses; this does not imply that they
remain authoritative across scenes, actor swaps, boss fights or loading.
Never write unverified position copies or the character index.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import struct

JAPAN_PLAYER_XYZ = (0x80151B10, 0x80151B14, 0x80151B18)
JAPAN_PLAYER_XYZ_START = JAPAN_PLAYER_XYZ[0]
JAPAN_PLAYER_XYZ_SIZE = 12
JAPAN_OEDO_SOUTH_SCENE = 0x0161
JAPAN_OEDO_SOUTH_ENTRANCE = (-289.0, 0.0, -167.0)
JAPAN_CHARACTER_INDEX = 0x80161DCC
JAPAN_SCENE_INDEX = 0x800CD2A2
MAX_ABSOLUTE_COORDINATE = 10000.0


@dataclass(frozen=True)
class JapanPositionWriteResult:
    scene: int
    character: int
    before: tuple[float, float, float]
    requested: tuple[float, float, float]
    observed: tuple[float, float, float]
    changed: bool


def checked_japan_xyz(values) -> tuple[float, float, float]:
    """Reject NaN/infinity/extreme coordinates and unintended value types."""
    if not isinstance(values, (tuple, list)) or len(values) != 3:
        raise ValueError('XYZ must contain exactly three decimal coordinates')
    coordinates = []
    for value in values:
        if isinstance(value, bool):
            raise ValueError('Boolean is not a coordinate')
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError('Invalid XYZ decimal coordinate') from exc
        if not math.isfinite(number) or abs(number) > MAX_ABSOLUTE_COORDINATE:
            raise ValueError('XYZ requires finite coordinates within ±10000')
        coordinates.append(number)
    # Round to the exact floating point values the 1997 game actually stores.
    try:
        return struct.unpack('>fff', struct.pack('>fff', *coordinates))
    except (OverflowError, struct.error) as exc:
        raise ValueError('XYZ cannot be encoded as three float32 values') from exc


def _read_context(rdram):
    scene = int.from_bytes(rdram.read_guest(JAPAN_SCENE_INDEX, 2), 'big')
    character = int.from_bytes(rdram.read_guest(JAPAN_CHARACTER_INDEX, 4), 'big')
    return scene, character


def read_japan_position(rdram):
    raw = rdram.read_guest(JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE)
    if len(raw) != JAPAN_PLAYER_XYZ_SIZE:
        raise OSError('Incomplete Japanese XYZ position read')
    values = struct.unpack('>fff', raw)
    if not all(math.isfinite(value) and abs(value) < 1e6 for value in values):
        raise RuntimeError(f'Japanese player XYZ not plausible: {values}')
    return values


def move_japan_goemon_oedo_south(rdram, values, *, expected_before: bytes,
                                 expected_scene=JAPAN_OEDO_SOUTH_SCENE):
    """One confirmed-scene Goemon XYZ request, no repeated/frozen writes.

    Caller MUST verify ROM, PID, RAM base/endian/size, obtain fresh consent,
    compare read-only and writable handles, and own a short-lived writable
    process. This function is intentionally incapable of other scene writes.
    """
    if expected_scene != JAPAN_OEDO_SOUTH_SCENE:
        raise ValueError('Japan position writes supported only in Oedo Town South')
    proposed = checked_japan_xyz(values)
    raw = struct.pack('>fff', *proposed)
    if not isinstance(expected_before, bytes) or len(expected_before) != 12:
        raise ValueError('Expected before image must be exactly 12 guest bytes')
    scene, character = _read_context(rdram)
    if scene != JAPAN_OEDO_SOUTH_SCENE or character != 0:
        raise RuntimeError(
            f'Japan XYZ write refused: scene=0x{scene:03X}, character={character}; '
            'validated only for Goemon in Oedo Town South')
    before = rdram.read_guest(JAPAN_PLAYER_XYZ_START, 12)
    if before != expected_before:
        raise RuntimeError('Position changed after confirmation; refresh and retry')
    previous = struct.unpack('>fff', before)
    if not all(math.isfinite(value) and abs(value) < 1e6 for value in previous):
        raise RuntimeError('Current XYZ is not plausible; no write')
    if before == raw:
        return JapanPositionWriteResult(scene, character, previous, proposed, previous, False)
    # Fail closed if scene/actor or coordinates change during validation.
    if _read_context(rdram) != (scene, character):
        raise RuntimeError('Scene or character changed during XYZ validation')
    if rdram.read_guest(JAPAN_PLAYER_XYZ_START, 12) != before:
        raise RuntimeError('Position changed during XYZ validation')
    rdram.write_guest(JAPAN_PLAYER_XYZ_START, raw)
    observed = rdram.read_guest(JAPAN_PLAYER_XYZ_START, 12)
    if observed != raw:
        raise RuntimeError(
            'XYZ write was attempted but immediate read-back differs; '
            'inspect gameplay or restore the prior emulator savestate')
    return JapanPositionWriteResult(
        scene, character, previous, proposed, struct.unpack('>fff', observed), True)
