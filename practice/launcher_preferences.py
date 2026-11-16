"""Persist only the preferred UI region for the unified launcher.

This is a convenience setting, NOT proof of live game region or memory identity.
Japanese ROM verification and independent process/RDRAM checks are unchanged.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile

FORMAT = "goemon-toolkit-launcher-v1"
VALID_REGIONS = frozenset(("usa", "japan"))


def preferences_path():
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or
                    Path.home() / "AppData" / "Local")
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or
                    Path.home() / ".config")
    return base / "GoemonSpeedrunTools" / "launcher-preferences.json"


def load_last_region(*, store=None) -> str:
    """Use USA by default; ignore missing, invalid or future schema versions."""
    path = Path(store) if store is not None else preferences_path()
    try:
        if path.stat().st_size > 4096:
            return "usa"
        doc = json.loads(path.read_text(encoding="utf-8"))
        if (isinstance(doc, dict) and doc.get("format") == FORMAT
                and doc.get("region") in VALID_REGIONS):
            return doc["region"]
    except (OSError, ValueError, TypeError):
        pass
    return "usa"


def save_last_region(region: str, *, store=None) -> None:
    """Atomically persist the Dashboard's region selection, never guest RAM."""
    if region not in VALID_REGIONS:
        raise ValueError("Unknown Goemon region")
    dest = Path(store) if store is not None else preferences_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=dest.parent, delete=False,
                prefix=f".{dest.name}.", suffix=".tmp") as stream:
            tmp = Path(stream.name)
            json.dump({"format": FORMAT, "region": region}, stream)
            stream.write("\n")
        os.replace(tmp, dest)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
