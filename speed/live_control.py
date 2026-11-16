"""Process-scoped control for a live-speed-enabled Goemon recomp host."""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
import ctypes
import mmap
import os
from pathlib import Path
import stat
import struct
import sys

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
def _open_linux_channel(pid):
    """Open only a verified user-owned mapping held by this exact process."""
    name = f"goemon64speed_{pid}"
    path = Path("/dev/shm") / name
    try:
        maps = Path(f"/proc/{pid}/maps").read_text(encoding="utf-8")
        if not any(f"/dev/shm/{name}" in line for line in maps.splitlines()):
            raise SpeedUnavailable("Selected process has no mapped Linux speed channel; rebuild a compatible recomp")
        flags = os.O_RDWR | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        fd = os.open(path, flags)
        try:
            meta = os.fstat(fd)
            if (not stat.S_ISREG(meta.st_mode) or meta.st_uid != os.geteuid()
                    or meta.st_size != 24 or (stat.S_IMODE(meta.st_mode) & 0o077)):
                raise SpeedUnavailable("Unsafe or incompatible Linux speed-channel permissions")
            with mmap.mmap(fd, 24, access=mmap.ACCESS_WRITE) as view:
                class Channel:
                    def read(self):
                        return struct.unpack_from("=6i", view, 0)
                    def request(self, rate):
                        # Aligned 32-bit process-shared store; the patched host
                        # acknowledges the applied rate in its next poll cycle.
                        struct.pack_into("=i", view, 12, rate)
                yield Channel()
        finally:
            os.close(fd)
    except (OSError, ValueError) as exc:
        raise SpeedUnavailable(f"Linux speed channel unavailable: {exc}") from exc


@contextmanager
def _open_channel(pid):
    if sys.platform == "linux":
        with _open_linux_channel(pid) as channel:
            yield channel
        return
    if os.name != 'nt':
        raise SpeedUnavailable('Live recomp speed control requires Windows or Linux')
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
