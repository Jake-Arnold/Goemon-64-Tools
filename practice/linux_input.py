"""Bounded X11-only key injection for native Linux Goemon64Recompiled.

The XTest path is intentionally disabled on Wayland: xdotool cannot reliably
confirm native Wayland foreground windows. Never inject into an unverified PID.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys


def _run(*args):
    try:
        return subprocess.run(["xdotool", *map(str, args)], check=True,
                              capture_output=True, text=True, timeout=4).stdout.strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"X11 input verification failed: {exc}") from exc


def _focused_game(pid: int) -> str:
    if sys.platform != "linux":
        raise OSError("Linux input adapter requires Linux")
    if type(pid) is not int or pid <= 0:
        raise ValueError("Invalid game PID")
    if os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11" or not os.environ.get("DISPLAY"):
        raise OSError("Automatic Goemon keys require an X11/Xorg desktop; Wayland cannot be safely verified. Press the game key manually.")
    if not shutil.which("xdotool"):
        raise OSError("Install xdotool for X11 game keys: sudo apt install xdotool")
    try:
        candidates = _run("search", "--onlyvisible", "--pid", pid, "--name", "[Gg]oemon").splitlines()
    except RuntimeError as exc:
        raise RuntimeError("No visible X11 Goemon game window for selected PID") from exc
    for window in candidates:
        if not window.isdecimal():
            continue
        if _run("getwindowpid", window) != str(pid):
            continue
        title = _run("getwindowname", window)
        if "goemon" not in title.lower():
            continue
        _run("windowactivate", "--sync", window)
        active = _run("getwindowfocus")
        if _run("getwindowpid", active) != str(pid):
            raise RuntimeError("The focused X11 window does not belong to the selected Goemon process")
        return window
    raise RuntimeError("Could not verify a visible Goemon window belonging to that PID")


def press_key(pid: int, key: str):
    if key not in ("Down", "space"):
        raise ValueError("Only the documented C-Down and N64 A keys are supported")
    _focused_game(pid)
    _run("keydown", "--clearmodifiers", key)
    released = False

    def release():
        nonlocal released
        if not released:
            released = True
            # Releasing even after focus changes prevents a stuck synthetic key.
            _run("keyup", key)

    return release
