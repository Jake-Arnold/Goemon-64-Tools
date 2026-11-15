"""Japan-0 instant area reload, ported from USA stage_reload_trial.

The shared Scene Browser double-click uses the pending 12-byte destination/
entrance structure (or the 2-byte destination alone), followed by engine mode
0x0C. It DOES NOT open the original debug menu (engine mode 0x0A), press A,
write the current map, or set the exit/title flag.

Japan pending-map and engine-mode addresses have independent read/behaviour
evidence; the 0x0C reload sequence is based on the USA implementation and
requires live Project64 verification before claiming a working stage load.
"""
from __future__ import annotations

from dataclasses import dataclass
from practice.entrances import Spawn
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
    JAPAN_ORDINARY_ENGINE_MODE, get_japan_debug_context, _normal_gameplay,
)
from practice.scenes import SCENES

JAPAN_PENDING_MAP = 0x800CD490
JAPAN_DIRECT_RELOAD_MODE = 0x0C
JAPAN_PENDING_BLOCK_SIZE = 12


@dataclass(frozen=True)
class JapanDirectReload:
    source_scene: int
    destination: int
    previous_pending_scene: int
    pending_width: int
    spawn: Spawn | None
    state_after_write: int
    target_character: int | None = None
    character_staged: bool = False


def stage_japan_direct_reload(rdram, destination: int, *,
                              expected_context: tuple, spawn: Spawn | None = None,
                              target_character: int | None = None):
    """Write pending destination/entrance, then 0x0D→0x0C immediately.

    The loaded game owns player reconstruction. Restore the previous pending
    data only if staging fails while STILL in ordinary source gameplay.
    """
    if type(destination) is not int or destination not in SCENES:
        raise ValueError('Select a known scene in the shared Scene Browser')
    if not isinstance(expected_context, tuple) or len(expected_context) != 6:
        raise ValueError('Missing complete Japanese source-gameplay context')
    _normal_gameplay(expected_context)
    if target_character is not None and (
            type(target_character) is not int or target_character not in range(4)):
        raise ValueError('Target character must be Goemon, Ebisumaru, Sasuke or Yae')
    if spawn is not None:
        if not isinstance(spawn, Spawn) or spawn.destination != destination:
            raise ValueError('Spawn must belong to the selected Japanese destination')
        requested = spawn.pending_bytes()  # 12-byte >HHhhhH, as in USA
    else:
        requested = destination.to_bytes(2, 'big')
    before = get_japan_debug_context(rdram)
    if before != expected_context:
        raise RuntimeError('Japanese scene/character/gameplay changed before reload')
    previous = rdram.read_guest(JAPAN_PENDING_MAP, len(requested))
    if len(previous) != len(requested):
        raise OSError('Short Japanese pending entrance read')
    wrote = False
    character_staged = False
    original_character = before[2].to_bytes(4, 'big')
    try:
        # Exactly the same operation ordering as USA stage_reload_trial:
        # stage pending map/entrance first, THEN trigger state 0x0C.
        if previous != requested:
            rdram.write_guest(JAPAN_PENDING_MAP, requested)
            wrote = True
        if rdram.read_guest(JAPAN_PENDING_MAP, len(requested)) != requested:
            raise OSError('Japanese pending scene did not verify; reload not sent')
        if get_japan_debug_context(rdram) != before:
            raise RuntimeError('Japanese source gameplay changed during pending staging')
        # Optional experimental target-character selection, matching the
        # USA browser control. Default is None: retain the playable character.
        # The engine rebuilds scene actors during the subsequent 0x0C reload.
        if target_character is not None and target_character != before[2]:
            requested_character = target_character.to_bytes(4, 'big')
            rdram.write_guest(JAPAN_DEBUG_CHARACTER, requested_character)
            character_staged = True
            if rdram.read_guest(JAPAN_DEBUG_CHARACTER, 4) != requested_character:
                raise OSError('Japanese target character write did not verify')
        rdram.write_guest(JAPAN_DEBUG_ENGINE_MODE, bytes([JAPAN_DIRECT_RELOAD_MODE]))
        observed = rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
        # State might already be back in ordinary gameplay if the game runs.
        if observed not in (JAPAN_DIRECT_RELOAD_MODE, JAPAN_ORDINARY_ENGINE_MODE):
            raise RuntimeError(
                f'Japanese reload entered unexpected state {observed}; '
                'inspect Project64 and restore a native savestate if necessary')
    except Exception:
        try:
            observed_context = get_japan_debug_context(rdram)
            safe = (observed_context[:2] == before[:2]
                    and observed_context[3:] == before[3:]
                    and observed_context[2] in (
                        before[2], target_character if target_character is not None else before[2]))
        except (OSError, ValueError, RuntimeError, PermissionError):
            safe = False
        if safe and character_staged:
            try:
                rdram.write_guest(JAPAN_DEBUG_CHARACTER, original_character)
            except (OSError, ValueError, RuntimeError, PermissionError):
                pass
        if safe and wrote:
            try:
                if rdram.read_guest(JAPAN_PENDING_MAP, len(requested)) == requested:
                    rdram.write_guest(JAPAN_PENDING_MAP, previous)
            except (OSError, ValueError, RuntimeError, PermissionError):
                pass
        raise
    return JapanDirectReload(
        source_scene=before[1], destination=destination,
        previous_pending_scene=int.from_bytes(previous[:2], 'big'),
        pending_width=len(requested), spawn=spawn,
        state_after_write=observed, target_character=target_character,
        character_staged=character_staged)
