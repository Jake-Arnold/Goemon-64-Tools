"""Automatic *candidate* PID discovery for Japanese Goemon.

Process names identify candidates only. The caller must open their memory and
verify all three pinned Japanese-ROM code signatures before accepting a PID.
Multiple verified processes are errors, not a guessed preferred target.
"""
from __future__ import annotations

from dataclasses import dataclass
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
            # A Linux process may not expose exe(). Cache by its process
            # name only as a last resort; every connection still verifies
            # all three original-ROM code signatures and live RAM state.
            if kind and not executable and name:
                executable = "name:" + name.lower()
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
    from practice.japan_connection_hints import load_hint_record
    from practice.japanese_mupen_attach import (
        AmbiguousJapaneseRdram, discover_japanese_mupen_rdram,
        validate_rdram_base,
    )
    from practice.japan_native_recomp import (
        discover_japan_recomp_rdram, validate_japan_recomp_context,
    )
    allow_4mb = candidate.backend == "project64"
    if base_hint is None and endian == "auto" and candidate.executable:
        hint = load_hint_record(candidate.executable, candidate.backend, probes)
        if hint is not None:
            # First try the previous absolute address. If Linux ASLR moved
            # the RDRAM allocation, reconstruct candidates from its position
            # within an identically sized host mapping. Never trust a cache
            # record without fresh code, size and live-context checks.
            guesses = [hint["base"]]
            size, offset = hint.get("mapping_size"), hint.get("mapping_offset")
            if size is not None and offset is not None:
                for start, length in process.regions():
                    if length == size:
                        address = start + offset
                        if address not in guesses and address % 16 == 0:
                            guesses.append(address)
            confirmed = []
            for address in guesses:
                try:
                    reader = validate_rdram_base(
                        process, address, hint["endian"], probes,
                        allow_4mb=allow_4mb)
                    validate_japan_recomp_context(
                        reader, strict_character=False)
                    confirmed.append((reader, address, hint["endian"]))
                except PermissionError:
                    raise
                except (OSError, ValueError, RuntimeError):
                    pass
            if len(confirmed) == 1:
                return confirmed[0]
            if len(confirmed) > 1:
                raise AmbiguousJapaneseRdram(
                    [(base, order) for _, base, order in confirmed])
            # Old cache layouts or rebuilt allocations may require a full scan.
    try:
        if candidate.backend == "recomp":
            reader, base, order = discover_japan_recomp_rdram(
                process, probes, mode=endian, base_hint=base_hint,
                strict_character=False)
        else:
            reader, base, order = discover_japanese_mupen_rdram(
                process, probes, mode=endian, base_hint=base_hint,
                allow_4mb=allow_4mb)
    except AmbiguousJapaneseRdram as exc:
        # Multiple code-matching copies are not necessarily live RDRAM.
        # Exclude implausible engine/scene state before asking the user.
        live = []
        for base, order in exc.candidates:
            try:
                reader = validate_rdram_base(
                    process, base, order, probes, allow_4mb=allow_4mb)
                validate_japan_recomp_context(
                    reader, strict_character=False)
                live.append((reader, base, order))
            except PermissionError:
                raise
            except (OSError, ValueError, RuntimeError):
                continue
        if len(live) == 1:
            return live[0]
        if len(live) > 1:
            raise AmbiguousJapaneseRdram(
                [(base, order) for _, base, order in live]) from exc
        raise RuntimeError(
            "Code-matching Japanese RAM buffers have no plausible live game state"
        ) from exc
    validate_japan_recomp_context(reader, strict_character=False)
    return reader, base, order


def remember_verified_connection(candidate: JapanProcessCandidate,
                                 probes, base: int, endian: str,
                                 *, process=None) -> None:
    """Store an independently proven address and ASLR-relocatable mapping."""
    if candidate.executable:
        from practice.japan_connection_hints import (
            mapping_coordinates, save_hint,
        )
        try:
            mapping = mapping_coordinates(process, base) if process else None
            options = (dict(mapping_size=mapping[0], mapping_offset=mapping[1])
                       if mapping else {})
            save_hint(candidate.executable, candidate.backend,
                      probes, base, endian, **options)
        except (OSError, ValueError, TypeError):
            # Hint persistence must never prevent a verified attachment.
            pass
