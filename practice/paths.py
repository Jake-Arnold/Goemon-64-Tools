"""Read-only application assets and writable user files.

Source checkout: preserve the existing practice/ file layout.
Frozen executable: never write into PyInstaller's temporary _MEIPASS tree.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def resource_root() -> Path:
    if is_frozen():
        return Path(sys._MEIPASS)  # PyInstaller's read-only extraction directory.
    return Path(__file__).resolve().parents[1]


def practice_data_dir() -> Path:
    if not is_frozen():
        return Path(__file__).resolve().parent
    local_appdata = os.environ.get("LOCALAPPDATA")
    base = Path(local_appdata) if local_appdata else Path.home() / "AppData" / "Local"
    path = base / "GoemonSpeedrunTools"
    path.mkdir(parents=True, exist_ok=True)
    return path


def diagnostics_dir() -> Path:
    path = practice_data_dir() / "diagnostics"
    path.mkdir(parents=True, exist_ok=True)
    return path
