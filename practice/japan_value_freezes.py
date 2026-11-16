"""Japanese guest-RDRAM raw freezes; never use USA player/task pointers.

The existing ValueFreezes lock book and ten-millisecond worker remain shared.
Only the polling/writer for the Japan region differs: snapshot a stable Japan
gameplay context, inspect current bytes through the read-only reader, and open
a short-lived writable process only when an active lock actually diverges.
This is best effort, not a frame-perfect cheat engine hook.
"""
from __future__ import annotations

from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_LOADING,
    JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
)
from practice.value_freezes import ValueFreezes


def stable_japan_gameplay(ram):
    """Return stable Japanese context or None when loading/outside gameplay."""
    engine = ram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)
    scene = ram.read_guest(JAPAN_DEBUG_SCENE, 2)
    character = ram.read_guest(JAPAN_DEBUG_CHARACTER, 4)
    loading = ram.read_guest(JAPAN_DEBUG_LOADING, 4)
    if not (len(engine) == 1 and len(scene) == 2 and
            len(character) == 4 and len(loading) == 4):
        raise OSError('Incomplete Japan-0 gameplay identity')
    context = (
        engine[0], int.from_bytes(scene, 'big'),
        int.from_bytes(character, 'big'),
        int.from_bytes(loading, 'big'),
    )
    if (context[0] != 13 or not 0 < context[1] < 0x800
            or context[2] not in (0, 1, 2, 3) or context[3] != 0):
        return None
    return context


class RegionalValueFreezes(ValueFreezes):
    """Reuse USA freeze behaviour and lock UI; never mix regional writers."""

    def __init__(self, open_japan_writer):
        super().__init__()
        self._open_japan_writer = open_japan_writer

    def poll(self, ram, token, *, writable):
        if not (isinstance(token, tuple) and token and token[0] == 'japan'):
            return super().poll(ram, token, writable=writable)
        with self.guard:
            if not self.active():
                return 'No active freezes.'
            if not writable or ram is None or self.token != token:
                self.clear()
                return 'Freezes stopped: Japan-0 disconnected or session changed.'
            if self.keep_health or self.god_mode or self.enemy_pass_through:
                self.clear()
                return 'Freezes stopped: USA-only player/task lock on Japan-0.'
            try:
                identity = stable_japan_gameplay(ram)
                if identity is None:
                    return 'Japan freezes paused: waiting for stable gameplay.'
                targets = tuple(self.locks.values())
                changed = [
                    lock for lock in targets
                    if ram.read_guest(lock.address, len(lock.value)) != lock.value
                ]
                if changed:
                    host, writer = self._open_japan_writer(ram, token)
                    try:
                        if stable_japan_gameplay(writer) != identity:
                            return 'Japan freezes paused: scene/character changed.'
                        for lock in changed:
                            # A scene switch during the write batch is a hard
                            # pause; no USA task pointer is inspected or modified.
                            if stable_japan_gameplay(writer) != identity:
                                return 'Japan freezes paused: scene/character changed.'
                            if writer.read_guest(lock.address, len(lock.value)) == lock.value:
                                continue
                            writer.write_guest(lock.address, lock.value)
                            if writer.read_guest(lock.address, len(lock.value)) != lock.value:
                                raise OSError(
                                    f'Japanese freeze writeback failed at 0x{lock.address:08X}')
                    finally:
                        host.close()
                return f'Active: {len(targets)} Japanese raw freezes (10 ms best effort).'
            except (OSError, ValueError, RuntimeError, PermissionError) as exc:
                self.clear()
                return f'Freezes stopped after failure: {exc}'
