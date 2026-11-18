"""One read-only session interface for the USA and Japanese toolkit views.

Address semantics and writable policies remain with each regional backend.
This facade deliberately never guesses memory offsets or grants write access.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RegionSession:
    region: str
    reader: object | None
    pid: int | None
    backend: str | None

    @property
    def connected(self) -> bool:
        return self.reader is not None

    def read_guest(self, address: int, length: int) -> bytes:
        if not self.connected:
            raise RuntimeError('No game memory attached')
        return self.reader.read_guest(address, length)


def active_session(app) -> RegionSession:
    """Return only the selected game's reader, never a stale other-ROM reader."""
    region = app.active_version.key
    if region == 'usa':
        target = getattr(app, 'connection_target', None)
        backend = target.get() if target is not None else None
        return RegionSession(region, getattr(app, 'mem', None),
                             getattr(app, 'game_pid', None), backend)
    if region == 'japan':
        return RegionSession(region, getattr(app, 'jp_rdram', None),
                             getattr(app, 'game_pid', None),
                             getattr(app, 'jp_backend', None))
    raise ValueError(f'Unsupported game region: {region}')
