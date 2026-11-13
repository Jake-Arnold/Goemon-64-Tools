"""Native Linux process memory adapter for the Goemon RDRAM scanner.

Reads use process_vm_readv, falling back to /proc/PID/mem only when seccomp
reports ENOSYS. Requires Linux ptrace permissions; never elevates privileges.
"""
from __future__ import annotations

import ctypes
import errno
import os
from pathlib import Path
import sys


class _IOVec(ctypes.Structure):
    _fields_ = (("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t))


class LinuxProcess:
    def __init__(self, pid: int, writable: bool = False):
        if sys.platform != "linux":
            raise OSError("Native Linux process memory is available only on Linux")
        if type(pid) is not int or pid <= 0:
            raise ValueError("PID must be a positive integer")
        self.pid = pid
        self.writable = bool(writable)
        self._closed = False
        self._fallback_mem = False
        self._mem_fd = None
        self._maps = Path(f"/proc/{pid}/maps")
        with self._maps.open("r", encoding="ascii") as stream:
            stream.readline()
        self._libc = ctypes.CDLL(None, use_errno=True)
        for name in ("process_vm_readv", "process_vm_writev"):
            fn = getattr(self._libc, name, None)
            if fn is None:
                raise OSError(f"Linux libc does not expose {name}")
            fn.argtypes = (ctypes.c_int, ctypes.POINTER(_IOVec), ctypes.c_ulong,
                           ctypes.POINTER(_IOVec), ctypes.c_ulong, ctypes.c_ulong)
            fn.restype = ctypes.c_ssize_t

    def close(self):
        self._closed = True
        if self._mem_fd is not None:
            os.close(self._mem_fd)
            self._mem_fd = None

    @staticmethod
    def _iter_readable_maps(lines):
        for line in lines:
            fields = line.split(None, 5)
            if len(fields) < 2 or not fields[1].startswith("r"):
                continue
            try:
                first, last = fields[0].split("-", 1)
                start, end = int(first, 16), int(last, 16)
            except ValueError:
                continue
            if end > start:
                yield (start, end - start)

    def regions(self):
        if self._closed:
            raise OSError("Linux game process connection is closed")
        with self._maps.open("r", encoding="ascii") as stream:
            yield from self._iter_readable_maps(stream)

    def _transfer_via_proc(self, address: int, size: int, data: bytes | None):
        if self._mem_fd is None:
            self._mem_fd = os.open(f"/proc/{self.pid}/mem",
                                   os.O_RDWR if self.writable else os.O_RDONLY)
        if data is None:
            result = os.pread(self._mem_fd, size, address)
            if len(result) != size:
                raise OSError(f"/proc/{self.pid}/mem short read at 0x{address:X}")
            return result
        count = os.pwrite(self._mem_fd, data, address)
        if count != size:
            raise OSError(f"/proc/{self.pid}/mem short write at 0x{address:X}")
        return None

    def _transfer(self, address: int, size: int, name: str, data: bytes | None = None):
        if self._closed:
            raise OSError("Linux game process connection is closed")
        if type(address) is not int or address <= 0:
            raise ValueError("Invalid process memory address")
        if type(size) is not int or size < 0:
            raise ValueError("Invalid process memory length")
        if size == 0:
            return b"" if data is None else None
        if address + size - 1 >= 1 << (ctypes.sizeof(ctypes.c_void_p) * 8):
            raise ValueError("Process address exceeds pointer range")
        if self._fallback_mem:
            return self._transfer_via_proc(address, size, data)
        buffer = ctypes.create_string_buffer(size) if data is None else ctypes.create_string_buffer(data, size)
        local = _IOVec(ctypes.cast(buffer, ctypes.c_void_p), size)
        remote = _IOVec(ctypes.c_void_p(address), size)
        ctypes.set_errno(0)
        count = getattr(self._libc, name)(self.pid, ctypes.byref(local), 1,
                                         ctypes.byref(remote), 1, 0)
        if count == -1:
            code = ctypes.get_errno()
            if code == errno.ENOSYS:
                self._fallback_mem = True
                return self._transfer_via_proc(address, size, data)
            if code in (errno.EPERM, errno.EACCES):
                raise PermissionError(
                    code, f"{name} denied for PID {self.pid}; check Linux ptrace "
                          "permissions (launch the game from the toolkit or "
                          "inspect kernel.yama.ptrace_scope)")
            raise OSError(code, f"{name} failed for PID {self.pid}: {os.strerror(code)}")
        if count != size:
            raise OSError(f"{name} short transfer at 0x{address:X}: {count}/{size} bytes")
        return buffer.raw[:size] if data is None else None

    def read(self, address: int, length: int) -> bytes:
        return self._transfer(address, length, "process_vm_readv")

    def write(self, address: int, data: bytes):
        if not self.writable:
            raise PermissionError("Process connection is read-only")
        if not isinstance(data, bytes):
            raise TypeError("Process write requires bytes")
        return self._transfer(address, len(data), "process_vm_writev", data)
