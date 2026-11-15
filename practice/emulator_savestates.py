"""Complete emulator savestate hotkeys; the emulator owns actual state files.

Only a verified Project64/Mupen64Plus window can receive F5/F7. No guest RAM
copy, ROM identity guarantee, or Goemon64Recomp savestate is implied.
"""
from __future__ import annotations
import ctypes
import os
import shutil
import subprocess
import sys

def emulator_kind(name: str) -> str | None:
    name = name.lower().replace("\\", "/").rsplit("/", 1)[-1]
    if name in ("project64.exe", "project64"):
        return "project64"
    if name in ("mupen64plus", "mupen64plus.exe", "mupen64plus-ui-console"):
        return "mupen64plus"
    return None

def _psutil():
    try:
        import psutil
    except ImportError as exc:
        raise RuntimeError("Install psutil for emulator process identification") from exc
    return psutil

def verified_emulator_pid(pid: int, target: str = "auto") -> tuple[int, str]:
    if target not in ("auto", "project64", "mupen64plus"):
        raise ValueError("Full savestates need Project64 or Mupen64Plus")
    if type(pid) is not int or pid <= 0:
        raise ValueError("Invalid emulator PID")
    p = _psutil()
    try:
        kind = emulator_kind(p.Process(pid).name())
    except (p.NoSuchProcess, p.AccessDenied) as exc:
        raise RuntimeError(f"Cannot inspect PID {pid}") from exc
    if kind is None or target not in ("auto", kind):
        raise ValueError("PID does not belong to the selected emulator")
    return pid, kind

def find_emulator_pid(target: str = "auto") -> tuple[int, str]:
    if target not in ("auto", "project64", "mupen64plus"):
        raise ValueError("Full savestates need Project64 or Mupen64Plus")
    matches = []
    for proc in _psutil().process_iter(["pid", "name"]):
        kind = emulator_kind(proc.info.get("name") or "")
        if kind and target in ("auto", kind):
            matches.append((proc.info["pid"], kind))
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise RuntimeError("Multiple emulators running; specify emulator and PID")
    raise RuntimeError("No running Project64/Mupen64Plus emulator found")

def _run_x11(*args):
    try:
        return subprocess.run(["xdotool", *map(str, args)], check=True,
                              text=True, capture_output=True, timeout=5).stdout.strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"X11 state hotkey failed: {exc}") from exc

def _send_x11(pid: int, keys: tuple[str, ...]):
    if os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11" or not os.environ.get("DISPLAY"):
        raise OSError("X11 required; Wayland hotkey dispatch is unsupported")
    if not shutil.which("xdotool"):
        raise OSError("Install xdotool for native emulator state hotkeys")
    windows = _run_x11("search", "--onlyvisible", "--pid", str(pid)).splitlines()
    for window in windows:
        if not window.isdecimal() or _run_x11("getwindowpid", window) != str(pid):
            continue
        if not _run_x11("getwindowname", window):
            continue
        _run_x11("windowactivate", "--sync", window)
        focused = _run_x11("getwindowfocus")
        if _run_x11("getwindowpid", focused) != str(pid):
            raise RuntimeError("Focused window is not the requested emulator")
        for key in keys:
            _run_x11("key", "--clearmodifiers", key)
        return
    raise RuntimeError("No visible emulator window belongs to the selected PID")

def _send_windows(pid: int, keys: tuple[str, ...]):
    if os.name != "nt":
        raise OSError("Windows hotkeys require Windows")
    from ctypes import wintypes
    user = ctypes.WinDLL("user32", use_last_error=True)
    CALLBACK = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user.EnumWindows.argtypes = (CALLBACK, wintypes.LPARAM)
    user.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
    user.GetForegroundWindow.restype = wintypes.HWND
    windows = []
    def add(hwnd, _):
        owner = wintypes.DWORD()
        user.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if (owner.value == pid and user.IsWindowVisible(hwnd) and
                user.GetWindowTextLengthW(hwnd) > 0):
            windows.append(hwnd)
        return True
    user.EnumWindows(CALLBACK(add), 0)
    if not windows or not user.SetForegroundWindow(windows[0]):
        raise RuntimeError("Cannot focus a visible window for this emulator PID")
    owner = wintypes.DWORD()
    user.GetWindowThreadProcessId(user.GetForegroundWindow(), ctypes.byref(owner))
    if owner.value != pid:
        raise RuntimeError("Focused Windows process does not match selected emulator")
    for key in keys:
        vk = {"F5": 0x74, "F7": 0x76}[key] if key in ("F5", "F7") else ord(key)
        user.keybd_event(vk, 0, 0, 0)
        user.keybd_event(vk, 0, 2, 0)

def send_state_command(pid: int, target: str, action: str, slot: int):
    verified_emulator_pid(pid, target)
    if action not in ("save", "load"):
        raise ValueError("Unknown savestate action")
    if type(slot) is not int or not 0 <= slot <= 9:
        raise ValueError("Savestate slot must be 0–9")
    keys = (str(slot), "F5" if action == "save" else "F7")
    if os.name == "nt":
        _send_windows(pid, keys)
    elif sys.platform == "linux":
        _send_x11(pid, keys)
    else:
        raise OSError("Only Windows and Linux X11 hotkeys are supported")
