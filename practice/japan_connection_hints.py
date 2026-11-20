"""Per-executable Japan RDRAM hints, never a substitute for ROM verification.

These local preferences contain a host address and detected memory order. Every
connection independently verifies the PID, all three original-JP code probes,
RDRAM size and RAM plausibility before using any hint.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile

from practice.launcher_preferences import preferences_path

FORMAT = "goemon-japan-connection-hints-v1"
VALID_BACKENDS = frozenset(("recomp", "project64", "mupen64plus"))
VALID_ENDIAN = frozenset(("big", "wordswapped", "byteswapped"))
MAX_ROWS = 24
MAX_BYTES = 65536


def hints_path() -> Path:
    return preferences_path().parent / "japan-connection-hints.json"


def rom_probe_identity(probes) -> str:
    """Key hints to the specific verified ROM code/header, not just region."""
    if len(probes) < 3:
        raise ValueError("Cannot cache an unverified Japanese ROM")
    digest = hashlib.sha256()
    digest.update(getattr(probes, "cartridge_header", b""))
    for offset, code in probes:
        digest.update(int(offset).to_bytes(4, "big"))
        digest.update(code)
    return digest.hexdigest()


def _rows(path: Path) -> list[dict]:
    try:
        if path.stat().st_size > MAX_BYTES:
            return []
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or doc.get("format") != FORMAT:
            return []
        entries = doc.get("entries")
        if not isinstance(entries, list) or len(entries) > MAX_ROWS:
            return []
        good = []
        for item in entries:
            if not isinstance(item, dict):
                continue
            if not (isinstance(item.get("executable"), str)
                    and 0 < len(item["executable"]) <= 1024
                    and item.get("backend") in VALID_BACKENDS
                    and item.get("rom_signature") and
                    isinstance(item["rom_signature"], str)
                    and len(item["rom_signature"]) == 64
                    and type(item.get("base")) is int
                    and item["base"] > 0 and item["base"] % 16 == 0
                    and item.get("endian") in VALID_ENDIAN):
                continue
            # Old entries contain absolute addresses only. Mapping metadata
            # is optional and must never bypass executable/ROM validation.
            size = item.get("mapping_size")
            offset = item.get("mapping_offset")
            if not (type(size) is int and size >= 0x400000
                    and type(offset) is int and 0 <= offset < size
                    and offset % 16 == 0):
                item = {k: v for k, v in item.items()
                        if k not in ("mapping_size", "mapping_offset")}
            good.append(item)
        return good
    except (OSError, ValueError, TypeError):
        return []


def load_hint_record(executable: str, backend: str, probes, *, store=None):
    """Return a verified-identity cache record; the RAM is NOT verified yet."""
    if not executable or backend not in VALID_BACKENDS:
        return None
    source = Path(store) if store is not None else hints_path()
    signature = rom_probe_identity(probes)
    for entry in _rows(source):
        if (entry["executable"] == executable and
                entry["backend"] == backend and
                entry["rom_signature"] == signature):
            return dict(entry)
    return None


def load_hint(executable: str, backend: str, probes, *, store=None):
    """Retain the original two-value API for existing callers."""
    hint = load_hint_record(executable, backend, probes, store=store)
    return (hint["base"], hint["endian"]) if hint else None


def mapping_coordinates(process, base: int):
    """Find a host mapping-relative address, suitable for ASLR rebasing."""
    try:
        for start, length in process.regions():
            if start <= base < start + length:
                return length, base - start
    except (OSError, ValueError, AttributeError):
        pass
    return None


def save_hint(executable: str, backend: str, probes,
              base: int, endian: str, *, store=None,
              mapping_size=None, mapping_offset=None) -> None:
    if (not isinstance(executable, str) or not 0 < len(executable) <= 1024
            or backend not in VALID_BACKENDS or type(base) is not int
            or base <= 0 or base % 16 or endian not in VALID_ENDIAN):
        raise ValueError("Invalid Japan connection hint")
    if (mapping_size is None) != (mapping_offset is None):
        raise ValueError("Incomplete RAM mapping hint")
    if mapping_size is not None and not (
            type(mapping_size) is int and mapping_size >= 0x400000
            and type(mapping_offset) is int
            and 0 <= mapping_offset < mapping_size
            and mapping_offset % 16 == 0):
        raise ValueError("Invalid RAM mapping hint")
    target = Path(store) if store is not None else hints_path()
    signature = rom_probe_identity(probes)
    entry = dict(executable=executable, backend=backend,
                 rom_signature=signature, base=base, endian=endian)
    if mapping_size is not None:
        entry.update(mapping_size=mapping_size, mapping_offset=mapping_offset)
    rows = [e for e in _rows(target) if
            (e["executable"], e["backend"], e["rom_signature"]) !=
            (executable, backend, signature)]
    rows = ([entry] + rows)[:MAX_ROWS]
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=target.parent,
                delete=False, prefix=f".{target.name}.", suffix=".tmp") as fh:
            tmp = Path(fh.name)
            json.dump({"format": FORMAT, "entries": rows}, fh,
                      separators=(",", ":"))
            fh.write("\n")
        os.replace(tmp, target)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
