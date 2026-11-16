"""Automatic *candidate* PID discovery for Japanese Goemon.

Process names identify candidates only. The caller must open their memory and
verify all three pinned Japanese-ROM code signatures before accepting a PID.
Multiple verified processes are errors, not a guessed preferred target.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath

from practice.emulator_savestates import emulator_kind

VALID_TARGETS = frozenset(("auto", "recomp", "project64", "mupen64plus"))


@dataclass(frozen=True)
class JapanProcessCandidate:
    pid: int
    backend: str
    executable: str = ""


def classify_candidate(name: str, executable: str = "") -> str | None:
    """Recognize well-known host process identities, not their ROM region."""
    for source in (name, executable.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]):
        kind = emulator_kind(source)
        if kind:
            return kind
        if "goemon64recomp" in source.lower():
            return "recomp"
    return None


def list_japan_processes(*, pid_hint: int | None = None, target="auto",
                         provider=None, allow_project64=True):
    if target not in VALID_TARGETS:
        raise ValueError("Unknown Japanese connection target")
    if pid_hint is not None and (type(pid_hint) is not int or pid_hint <= 0):
        raise ValueError("Invalid Japanese process PID")
    if provider is None:
        try:
            import psutil
        except ImportError as exc:
            raise RuntimeError("Install psutil for Japanese process discovery") from exc
        provider = psutil
    processes = ([provider.Process(pid_hint)] if pid_hint is not None else
                 provider.process_iter(["pid", "name", "exe"]))
    found = []
    for proc in processes:
        try:
            if pid_hint is not None:
                pid = proc.pid
                name = proc.name() or ""
                try:
                    executable = proc.exe() or ""
                except (provider.AccessDenied, OSError):
                    executable = ""
            else:
                data = proc.info
                pid = data.get("pid")
                name = data.get("name") or ""
                executable = data.get("exe") or ""
            kind = classify_candidate(name, executable)
            if (kind and (target == "auto" or target == kind)
                    and (allow_project64 or kind != "project64")
                    and type(pid) is int and pid > 0):
                found.append(JapanProcessCandidate(pid, kind, executable))
        except (provider.NoSuchProcess, provider.AccessDenied, OSError):
            if pid_hint is not None:
                raise RuntimeError(f"Cannot inspect selected PID {pid_hint}")
            continue
    found = sorted(set(found), key=lambda p: (p.pid, p.backend))
    if not found:
        hint = f"PID {pid_hint}" if pid_hint else "running supported clients"
        raise RuntimeError(f"No Japanese recomp/Mupen/Project64 candidate for {hint}")
    return tuple(found)


def describe_verified_connections(connections) -> str:
    """Report every valid PID/backend/layout instead of silently choosing."""
    return "; ".join(
        f"PID {pid} {backend} at 0x{base:X} ({endian})"
        for pid, backend, base, endian in connections)


def connect_candidate_ram(candidate: JapanProcessCandidate, process, probes, *,
                          base_hint=None, endian="auto"):
    """Verify a cached hint first; fall back to a full 3-signature scan.

    The hint is only a speed optimization, never proof of a live game. Manual
    host-base/endian overrides remain explicit and are re-verified.
    """
    from practice.japan_connection_hints import load_hint
    from practice.japanese_mupen_attach import (
        discover_japanese_mupen_rdram, validate_rdram_base,
    )
    from practice.japan_native_recomp import (
        discover_japan_recomp_rdram, validate_japan_recomp_context,
    )
    allow_4mb = candidate.backend == "project64"
    if base_hint is None and endian == "auto" and candidate.executable:
        hint = load_hint(candidate.executable, candidate.backend, probes)
        if hint is not None:
            base, cached_endian = hint
            try:
                reader = validate_rdram_base(
                    process, base, cached_endian, probes, allow_4mb=allow_4mb)
                if candidate.backend == "recomp":
                    validate_japan_recomp_context(
                        reader, strict_character=False)
                return reader, base, cached_endian
            except (OSError, ValueError, RuntimeError):
                # A recompilation update or ASLR may have changed the mapping.
                # Retrying a full scan is mandatory; do not accept the cache.
                pass
    if candidate.backend == "recomp":
        return discover_japan_recomp_rdram(
            process, probes, mode=endian, base_hint=base_hint,
            strict_character=False)
    return discover_japanese_mupen_rdram(
        process, probes, mode=endian, base_hint=base_hint,
        allow_4mb=allow_4mb)


def remember_verified_connection(candidate: JapanProcessCandidate,
                                 probes, base: int, endian: str) -> None:
    """Best-effort local preference; never part of the attach proof."""
    if candidate.executable:
        from practice.japan_connection_hints import save_hint
        try:
            save_hint(candidate.executable, candidate.backend,
                      probes, base, endian)
        except OSError:
            pass
