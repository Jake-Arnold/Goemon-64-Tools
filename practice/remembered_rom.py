"""Persist the user's last exactly verified retail ROM *path*, not ROM bytes.

Each reuse re-hashes and re-identifies the file using verify_selected_rom.
Never trust the saved JSON, mtime alone, a filename, or a prior session
as evidence of the live emulator's ROM/RDRAM identity. Host probes remain
mandatory on EVERY process attachment.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import tempfile
from practice.game_versions import selected_version, verify_selected_rom

FORMAT = "goemon-verified-rom-paths-v1"


def registry_path():
    """Per-user config, never the Git checkout or temporary frozen app root."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or
                    Path.home() / "AppData" / "Local")
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or
                    Path.home() / ".config")
    return base / "GoemonSpeedrunTools" / "verified_rom_paths.json"


def _entries(path):
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
        if (not isinstance(document, dict) or document.get("format") != FORMAT
                or not isinstance(document.get("versions"), dict)):
            return {}
        return document["versions"]
    except (OSError, ValueError, TypeError):
        return {}


def remember_verified_rom(rom_path, version_key, *, store=None):
    """Record only a file that passes the exact retail ROM verifier."""
    version = verify_selected_rom(rom_path, version_key)
    resolved = Path(rom_path).resolve(strict=True)
    target = Path(store) if store is not None else registry_path()
    entries = dict(_entries(target))
    entries[version_key] = {"path": str(resolved), "canonical_sha1": version.sha1}
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", dir=target.parent, encoding="utf-8",
                prefix=f".{target.name}.", suffix=".tmp", delete=False) as fh:
            temporary = Path(fh.name)
            json.dump({"format": FORMAT, "versions": entries}, fh, indent=2)
            fh.write("\n")
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return resolved


def load_remembered_rom(version_key, *, store=None):
    """Return last path only if the bytes STILL pass exact-ROM verification.

    A missing or edited ROM results in None and requires explicit re-selection.
    This never opens a process, bypasses guest code probes, or trusts a
    previously saved hash without rechecking the ROM's actual bytes.
    """
    expected = selected_version(version_key)
    target = Path(store) if store is not None else registry_path()
    entry = _entries(target).get(version_key)
    if (not isinstance(entry, dict)
            or entry.get("canonical_sha1") != expected.sha1
            or not isinstance(entry.get("path"), str)
            or not entry["path"]):
        return None
    path = Path(entry["path"])
    try:
        verify_selected_rom(path, version_key)
        return path.resolve(strict=True)
    except (OSError, ValueError):
        return None
