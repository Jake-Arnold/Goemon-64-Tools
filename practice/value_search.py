"""Read-only aligned numeric searches over the original game's 8 MiB RDRAM.

All bytes come from read_guest() in canonical N64 big-endian order. Searches
keep only local snapshots and candidate flags; no memory writes or disk dumps.
"""
from __future__ import annotations

import math
import struct

GUEST_BASE = 0x80000000
RDRAM_SIZE = 0x800000
SCAN_CHUNK = 0x10000
DISPLAY_LIMIT = 200
FORMATS = {
    'u8': ('B', 1), 's8': ('b', 1),
    'u16': ('H', 2), 's16': ('h', 2),
    'u32': ('I', 4), 's32': ('i', 4),
    'f32': ('f', 4),
}
FILTERS = ('Exact', 'Increased', 'Decreased', 'Changed', 'Unchanged')


def encode_value(kind: str, text: str) -> bytes:
    if kind not in FORMATS:
        raise ValueError('Unsupported value type')
    raw = text.strip()
    if not raw:
        raise ValueError('Enter a number to search')
    fmt, _width = FORMATS[kind]
    try:
        if kind == 'f32':
            number = float(raw)
            if not math.isfinite(number):
                raise ValueError('Float must be finite')
        else:
            number = int(raw, 16 if raw.lower().lstrip('+-').startswith('0x') else 10)
        return struct.pack('>' + fmt, number)
    except (ValueError, OverflowError, struct.error) as exc:
        raise ValueError(f'Invalid {kind} value: {raw}') from exc


def read_ram(ram, *, size: int = RDRAM_SIZE, chunk: int = SCAN_CHUNK) -> bytes:
    """Read a complete guest-RAM snapshot; never silently accept partial reads."""
    if not 0 < size <= RDRAM_SIZE or chunk <= 0 or chunk % 4:
        raise ValueError('Invalid RDRAM read bounds')
    data = bytearray(size)
    for offset in range(0, size, chunk):
        length = min(chunk, size - offset)
        block = ram.read_guest(GUEST_BASE + offset, length)
        if len(block) != length:
            raise OSError(f'Incomplete guest-RAM read at 0x{GUEST_BASE + offset:08X}')
        data[offset:offset + length] = block
    return bytes(data)


class ValueScanner:
    """Narrow candidate addresses across successive read-only RAM snapshots.

    Only naturally aligned addresses are included, avoiding accidental matches
    across adjacent fields. A bytearray of one flag per candidate slot bounds
    memory usage even when millions of addresses match an initial zero search.
    """
    def __init__(self, *, size: int = RDRAM_SIZE, chunk: int = SCAN_CHUNK, aligned: bool = True):
        if not 0 < size <= RDRAM_SIZE or chunk <= 0 or chunk % 4:
            raise ValueError('Invalid scanner bounds')
        self.size = size
        self.chunk = chunk
        self.aligned = aligned
        self.clear()

    def clear(self):
        self.kind = None
        self.previous = None
        self.active = None  # None means every naturally aligned slot is eligible
        self.count = 0
        self.samples = 0

    def _read(self, ram):
        return read_ram(ram, size=self.size, chunk=self.chunk)

    def _stride(self, width):
        return width if self.aligned else 1

    def _slots(self, width):
        return max(0, (self.size - width) // self._stride(width) + 1)

    def start_unknown(self, ram, kind: str) -> int:
        if kind not in FORMATS:
            raise ValueError('Unsupported value type')
        snapshot = self._read(ram)
        self.kind = kind
        self.previous = snapshot
        self.active = None
        self.count = self._slots(FORMATS[kind][1])
        self.samples = 1
        return self.count

    def start_exact(self, ram, kind: str, text: str) -> int:
        target = encode_value(kind, text)
        snapshot = self._read(ram)
        width = len(target)
        flags = bytearray(self._slots(width))
        count = 0
        index = snapshot.find(target)
        while index >= 0:
            stride = self._stride(width)
            if index % stride == 0 and index // stride < len(flags):
                flags[index // stride] = 1
                count += 1
            index = snapshot.find(target, index + 1)
        self.kind = kind
        self.previous = snapshot
        self.active = flags
        self.count = count
        self.samples = 1
        return count

    def filter(self, ram, mode: str, text: str = '') -> int:
        if self.previous is None or self.kind is None:
            raise ValueError('Start an exact or unknown-value search first')
        if mode not in FILTERS:
            raise ValueError('Unsupported search filter')
        fmt, width = FORMATS[self.kind]
        target = encode_value(self.kind, text) if mode == 'Exact' else None
        latest = self._read(ram)
        old = self.previous
        flags = bytearray(self._slots(width))
        count = 0
        unpack = struct.Struct('>' + fmt).unpack_from
        for slot in range(len(flags)):
            if self.active is not None and not self.active[slot]:
                continue
            offset = slot * self._stride(width)
            if mode == 'Exact':
                matched = latest[offset:offset + width] == target
            elif mode in ('Changed', 'Unchanged'):
                changed = old[offset:offset + width] != latest[offset:offset + width]
                matched = changed if mode == 'Changed' else not changed
            else:
                a = unpack(old, offset)[0]
                b = unpack(latest, offset)[0]
                matched = (b > a) if mode == 'Increased' else (b < a)
            if matched:
                flags[slot] = 1
                count += 1
        self.previous = latest
        self.active = flags
        self.count = count
        self.samples += 1
        return count

    def _addresses(self, limit: int):
        if self.kind is None or limit < 0:
            return
        width = FORMATS[self.kind][1]
        stride = self._stride(width)
        remaining = min(limit, self.count)
        if self.active is None:
            for slot in range(remaining):
                yield slot * stride
        else:
            slot = self.active.find(1)
            while slot >= 0 and remaining:
                yield slot * stride
                remaining -= 1
                slot = self.active.find(1, slot + 1)

    def rows(self, limit: int = DISPLAY_LIMIT, *, ram=None) -> list[dict]:
        if self.previous is None or self.kind is None:
            return []
        fmt, width = FORMATS[self.kind]
        unpack = struct.Struct('>' + fmt).unpack
        result = []
        for offset in self._addresses(limit):
            data = (ram.read_guest(GUEST_BASE + offset, width) if ram is not None
                    else self.previous[offset:offset + width])
            if len(data) != width:
                raise OSError(f'Incomplete value read at 0x{GUEST_BASE + offset:08X}')
            value = unpack(data)[0]
            result.append({
                'address': GUEST_BASE + offset,
                'kind': self.kind,
                'value': f'{value:.7g}' if isinstance(value, float) else str(value),
                'hex': '0x' + data.hex().upper(),
            })
        return result
