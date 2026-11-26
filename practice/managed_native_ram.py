"""Bounded Linux RAM handle for an inspector-owned child, not PID discovery.

The inherited pipe reports the native 2.6.0 RDRAM base. A procfs descriptor
pins the original child's address space; all transfers are within 4 MiB.
No external PID or arbitrary host address can be supplied through the UI.
"""
from __future__ import annotations

import os
import sys

from practice.japanese_mupen_attach import verified_japan_probes, validate_rdram_base

SIZE = 0x400000


class ManagedNativeRam:
    def __init__(self, owner, base, *, writable=False):
        if sys.platform != 'linux' or type(base) is not int or base <= 0 or base % 16:
            raise ValueError('Invalid managed Linux RDRAM base')
        self.owner, self.pid, self.base = owner, owner.pid, base
        self.writable = bool(writable)
        self.fd = None
        self.check_alive()
        fd = os.open(f'/proc/{self.pid}/mem', os.O_RDWR if writable else os.O_RDONLY)
        try:
            self.check_alive()
        except BaseException:
            os.close(fd)
            raise
        self.fd = fd

    def check_alive(self):
        if self.owner.poll() is not None:
            raise OSError('Native inspector child exited; reconnect to a new session')

    def close(self):
        if self.fd is not None:
            fd, self.fd = self.fd, None
            os.close(fd)

    def _check(self, address, length):
        self.check_alive()
        if self.fd is None:
            raise OSError('Managed RAM connection is closed')
        if (type(address) is not int or type(length) is not int or length < 0
                or not self.base <= address <= self.base + SIZE - length):
            raise OSError('Transfer outside verified managed RDRAM')

    def read(self, address, length):
        self._check(address, length)
        data = os.pread(self.fd, length, address)
        if len(data) != length:
            raise OSError('Managed RDRAM short read')
        return data

    def write(self, address, data):
        if not self.writable:
            raise PermissionError('Managed RAM handle is read-only')
        if not isinstance(data, bytes):
            raise TypeError('Expected bytes')
        self._check(address, len(data))
        if os.pwrite(self.fd, data, address) != len(data):
            raise OSError('Managed RDRAM short write')

    def regions(self):
        self.check_alive()
        yield self.base, SIZE

    def writer(self):
        self.check_alive()
        if self.fd is None:
            raise OSError('Managed RAM connection is closed')
        return type(self)(self.owner, self.base, writable=True)


def connect_managed_japan(owner, base, rom_path):
    """Independently verify retail ROM and its three executable probes."""
    probes = verified_japan_probes(rom_path)
    host = ManagedNativeRam(owner, base)
    try:
        endian = 'wordswapped' if sys.byteorder == 'little' else 'big'
        reader = validate_rdram_base(host, base, endian, probes, allow_4mb=True)
        host.check_alive()
        return host, reader, endian
    except BaseException:
        host.close()
        raise
