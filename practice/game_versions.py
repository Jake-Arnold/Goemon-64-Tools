"""Strict Goemon release identities for the host toolkit.

Selecting a ROM does not prove the running process is that ROM's region.
Only USA RAM addresses and actions are currently supported.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from practice.entrances import canonical_rom

ROM_SIZE = 16 * 1024 * 1024


@dataclass(frozen=True)
class GameVersion:
    key: str
    label: str
    game_code: bytes
    sha1: str
    live_memory_supported: bool


VERSIONS = {
    "usa": GameVersion(
        "usa", "USA - Mystical Ninja", b"NG5E",
        "df8083a54296b8c151917c5333e1c85f014a2a66", True,
    ),
    "japan": GameVersion(
        "japan", "Japan - Ganbare Goemon", b"NG5J",
        "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b", False,
    ),
}


def selected_version(key: str) -> GameVersion:
    try:
        return VERSIONS[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported Goemon version: {key!r}") from exc


def identify_rom(data: bytes) -> GameVersion:
    """Accept only either exact 16 MiB retail revision after byte-order conversion."""
    if len(data) != ROM_SIZE:
        raise ValueError("Expected a 16 MiB N64 retail ROM")
    canonical = canonical_rom(data)
    digest = hashlib.sha1(canonical).hexdigest()
    for version in VERSIONS.values():
        if (digest == version.sha1 and canonical[0x3B:0x3F] == version.game_code
                and canonical[0x3F] == 0):
            return version
    raise ValueError("ROM not recognised as either verified USA or Japanese revision")


def verify_selected_rom(path: str | Path, version_key: str) -> GameVersion:
    expected = selected_version(version_key)
    found = identify_rom(Path(path).read_bytes())
    if found != expected:
        raise ValueError(f"Selected {expected.label}, but this ROM is {found.label}")
    return found
