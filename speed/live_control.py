"""Process-scoped control for a live-speed-enabled Goemon recomp host."""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
import ctypes
import os

MAGIC = 0x47363453
VERSION = 2


@dataclass(frozen=True)
class SpeedStatus:
    requested: int
    applied: int
    guest_millis: int


class SpeedUnavailable(RuntimeError):
    """The selected process has no compatible live-speed channel."""


@contextmanager
def _open_channel(pid):
    if os.name != 'nt':
        raise SpeedUnavailable('Live recomp speed control requires Windows')
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenFileMappingW.argtypes = (ctypes.c_uint32, ctypes.c_int, ctypes.c_wchar_p)
    kernel.OpenFileMappingW.restype = ctypes.c_void_p
    kernel.MapViewOfFile.argtypes = (ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_size_t)
    kernel.MapViewOfFile.restype = ctypes.c_void_p
    kernel.UnmapViewOfFile.argtypes = (ctypes.c_void_p,)
    kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
    handle = kernel.OpenFileMappingW(0x0006, False, f'Local\\Goemon64Speed_{pid}')
    if not handle:
        raise SpeedUnavailable('Selected game does not expose the live-speed channel')
    view = None
    try:
        view = kernel.MapViewOfFile(handle, 0x0006, 0, 0, 24)
        if not view:
            raise SpeedUnavailable('Cannot access the selected game speed channel')
        class Channel:
            def read(self):
                def word(index):
                    # Windows guarantees atomic aligned 32-bit reads; fields
                    # are aligned and published by the host with Interlocked.
                    return ctypes.c_int32.from_address(view + index*4).value
                return tuple(word(i) for i in range(6))
            def request(self, rate):
                # A single aligned 32-bit store; no read-modify-write needed.
                ctypes.c_int32.from_address(view + 12).value = rate
        yield Channel()
    finally:
        if view: kernel.UnmapViewOfFile(view)
        kernel.CloseHandle(handle)


def _validate(pid, words):
    if type(pid) is not int or not 0 < pid <= 0x7FFFFFFF:
        raise ValueError('Invalid process ID')
    if len(words) != 6 or words[:3] != (MAGIC, VERSION, pid):
        raise SpeedUnavailable('Selected game speed channel has an invalid identity')
    requested, applied, guest_millis = words[3:]
    if requested not in (1,2,3,4) or applied not in (1,2,3,4):
        raise SpeedUnavailable('Selected game speed channel has an invalid rate')
    return SpeedStatus(requested, applied, guest_millis & 0xFFFFFFFF)


def read_speed(pid):
    if type(pid) is not int or not 0 < pid <= 0x7FFFFFFF:
        raise ValueError('Invalid process ID')
    with _open_channel(pid) as channel:
        return _validate(pid, channel.read())


def request_speed(pid, multiplier):
    if type(multiplier) is not int or multiplier not in (1,2,3,4):
        raise ValueError('Speed must be 1x, 2x, 3x or 4x')
    if type(pid) is not int or not 0 < pid <= 0x7FFFFFFF:
        raise ValueError('Invalid process ID')
    with _open_channel(pid) as channel:
        current = _validate(pid, channel.read())
        channel.request(multiplier)
        return current
