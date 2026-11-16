"""One bounded N64 A keyboard press to the verified Project64 window.

The classic Project64/Jabo keyboard layout maps N64 A to X. Other users may
have rebound it, so the toolkit's selector must match their PJ64 settings.
Only the chosen emulator PID can receive the press. Caller schedules release.
"""
from __future__ import annotations
import ctypes
import os
from ctypes import wintypes
from practice.emulator_savestates import verified_emulator_pid

PROJECT64_A_KEY_OPTIONS = ("X", "Z", "C", "SPACE", "ENTER", "A", "S", "J", "K", "L")

VKEYS = {**{letter: ord(letter) for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
         "SPACE": 0x20, "ENTER": 0x0D}


def press_project64_native_a(pid: int, key: str = "X"):
    """Press selected keyboard binding, return a one-shot key-release function.

    Key-up must be invoked even if menu loading, toolkit exit or a connection
    change interrupts the operation. No virtual-button memory patching.
    """
    if type(key) is not str or key not in PROJECT64_A_KEY_OPTIONS:
        raise ValueError("Choose an allowed Project64 N64 A keyboard binding")
    if os.name != 'nt':
        raise OSError('Automatic N64 A keyboard input requires Windows Project64')
    verified_emulator_pid(pid, "project64")
    user = ctypes.WinDLL("user32", use_last_error=True)
    CALLBACK = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user.EnumWindows.argtypes = (CALLBACK, wintypes.LPARAM)
    user.GetWindowThreadProcessId.argtypes = (
        wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
    user.GetForegroundWindow.restype = wintypes.HWND
    windows = []

    def candidate(hwnd, _):
        owner = wintypes.DWORD()
        user.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if (owner.value == pid and user.IsWindowVisible(hwnd)
                and user.GetWindowTextLengthW(hwnd) > 0):
            windows.append(hwnd)
        return True

    user.EnumWindows(CALLBACK(candidate), 0)
    if not windows or not user.SetForegroundWindow(windows[0]):
        raise RuntimeError('Cannot focus Project64 window for native A input')
    owner = wintypes.DWORD()
    user.GetWindowThreadProcessId(user.GetForegroundWindow(),
                                  ctypes.byref(owner))
    if owner.value != pid:
        raise RuntimeError('Focused window PID differs from verified Project64')

    vk = VKEYS[key]
    user.MapVirtualKeyW.argtypes = (wintypes.UINT, wintypes.UINT)
    user.keybd_event.argtypes = (
        wintypes.BYTE, wintypes.BYTE, wintypes.DWORD, ctypes.c_size_t)
    scan = user.MapVirtualKeyW(vk, 0)
    user.keybd_event(vk, scan, 0, 0)
    released = False

    def release():
        nonlocal released
        if not released:
            released = True
            user.keybd_event(vk, scan, 0x0002, 0)

    return release
