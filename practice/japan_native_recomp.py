"""Japan-0 native recomp process identity and guarded guest-RAM discovery.

The Japanese recomp and the USA recomp use the same executable name. A process
name is *never* proof of the game's region. Live Japan-0 memory is accepted
only after comparison with three independent 64-byte code fingerprints from
the user's SHA-1-verified original Japanese retail ROM. The existing scanner
also rejects cartridge copies that resemble RDRAM.

No process writes are performed by this module. The native port may not retain
original guest code in its RDRAM in every build; in that case attachment fails
closed rather than interpreting an unverified buffer as the game.
"""
from __future__ import annotations

from pathlib import Path

from autosplitter.process_discovery import find_pid
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
)
from practice.japanese_mupen_attach import (
    discover_japanese_mupen_rdram, validate_rdram_base,
)


def verified_japan_recomp_pid(pid: int) -> tuple[int, str]:
    """Check executable identity, but do not infer ROM region from its name."""
    if type(pid) is not int or pid <= 0:
        raise ValueError('Invalid native recomp PID')
    try:
        import psutil
    except ImportError as exc:
        raise RuntimeError('Install psutil for native game process discovery') from exc
    try:
        process = psutil.Process(pid)
        name = process.name().lower()
    except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
        raise RuntimeError(f'Cannot inspect native recomp PID {pid}') from exc
    # Linux /proc/<pid>/comm truncates executable names to 15 characters.
    if 'goemon64recomp' not in name:
        raise ValueError('PID is not a Goemon64Recompiled native process')
    return pid, 'recomp'


def find_japan_recomp_pid() -> tuple[int, str]:
    """Reject multiple or missing native instances; user can supply --pid."""
    return verified_japan_recomp_pid(find_pid('recomp'))


def validate_japan_recomp_context(reader):
    """Sanity check Japan-specific live globals after the full ROM-code proof.

    This is an extra plausibility check, not a substitute for code signatures.
    Title screens and non-playable scenes may have no valid character.
    """
    state = reader.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
    scene = int.from_bytes(reader.read_guest(JAPAN_DEBUG_SCENE, 2), 'big')
    if state > 17 or scene >= 0x800:
        raise ValueError('Japanese recomp live engine state or scene is implausible')
    if state == 13:
        character = int.from_bytes(
            reader.read_guest(JAPAN_DEBUG_CHARACTER, 4), 'big')
        if character not in (0, 1, 2, 3):
            raise ValueError('Japanese recomp gameplay character is invalid')
    return reader


def discover_japan_recomp_rdram(process, probes, *, mode='auto',
                               base_hint=None):
    """Identify the actual live 8 MiB Japanese RDRAM, never a ROM-buffer copy."""
    reader, base, endian = discover_japanese_mupen_rdram(
        process, probes, mode=mode, base_hint=base_hint, allow_4mb=False)
    validate_japan_recomp_context(reader)
    return reader, base, endian


def validate_japan_recomp_writer(process, attached, probes):
    """Revalidate region and host mapping on each new native writable handle."""
    reader = validate_rdram_base(
        process, attached.base, attached.endian, probes, allow_4mb=False)
    if getattr(reader, 'rdram_size', 0x800000) != getattr(
            attached, 'rdram_size', 0x800000):
        raise RuntimeError('Japanese native recomp RAM size changed')
    validate_japan_recomp_context(reader)
    return reader
