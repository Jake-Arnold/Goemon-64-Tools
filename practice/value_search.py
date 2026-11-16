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
    'f32': ('f', 4), 'f64': ('d', 8),
}
TEXT_ENCODINGS = {
    'ASCII': 'ascii',
    'Shift-JIS': 'shift_jis',
    'UTF-8': 'utf-8',
}
TEXT_KIND = 'text'

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
        self.initial = None  # Immutable first snapshot for initial-baseline filtering
        self.text_width = None
        self.text_encoding = None
        self.active = None  # None means every naturally aligned slot is eligible
        self.count = 0
        self.samples = 0

    def _read(self, ram):
        return read_ram(ram, size=self.size, chunk=self.chunk)

    def _stride(self, width):
        return (1 if self.kind == TEXT_KIND else
                width if self.aligned else 1)

    def _width(self):
        return self.text_width if self.kind == TEXT_KIND else FORMATS[self.kind][1]

    @staticmethod
    def encode_text(value, encoding):
        if encoding not in TEXT_ENCODINGS:
            raise ValueError('Select ASCII, Shift-JIS or UTF-8 encoding')
        if not isinstance(value, str) or not value:
            raise ValueError('Enter text to find')
        try:
            encoded = value.encode(TEXT_ENCODINGS[encoding], errors='strict')
        except UnicodeEncodeError as exc:
            raise ValueError(f'Text cannot be encoded as {encoding}') from exc
        if not 1 <= len(encoded) <= 128:
            raise ValueError('Enter 1–128 encoded bytes of text')
        return encoded

    def start_text(self, ram, value: str, *, encoding='ASCII') -> int:
        target = self.encode_text(value, encoding)
        snapshot = self._read(ram)
        width = len(target)
        flags = bytearray(max(0, self.size - width + 1))
        count = 0
        cursor = snapshot.find(target)
        while cursor >= 0:
            flags[cursor] = 1
            count += 1
            cursor = snapshot.find(target, cursor + 1)
        self.kind = TEXT_KIND
        self.text_width = width
        self.text_encoding = encoding
        self.previous = snapshot
        self.initial = snapshot
        self.active = flags
        self.count = count
        self.samples = 1
        return count

    def _slots(self, width):
        return max(0, (self.size - width) // self._stride(width) + 1)

    def start_unknown(self, ram, kind: str) -> int:
        if kind not in FORMATS:
            raise ValueError('Unsupported value type')
        snapshot = self._read(ram)
        self.kind = kind
        self.previous = snapshot
        self.initial = snapshot
        self.text_width = None
        self.text_encoding = None
        self.active = None
        self.count = self._slots(FORMATS[kind][1])
        self.samples = 1
        return self.count

    def start_exact(self, ram, kind: str, text: str) -> int:
        target = encode_value(kind, text)
        snapshot = self._read(ram)
        width = len(target)
        stride = width if self.aligned else 1
        flags = bytearray(max(0, (self.size - width) // stride + 1))
        count = 0
        index = snapshot.find(target)
        while index >= 0:
            if index % stride == 0 and index // stride < len(flags):
                flags[index // stride] = 1
                count += 1
            index = snapshot.find(target, index + 1)
        self.kind = kind
        self.previous = snapshot
        self.initial = snapshot
        self.text_width = None
        self.text_encoding = None
        self.active = flags
        self.count = count
        self.samples = 1
        return count

    def filter(self, ram, mode: str, text: str = '', *, compare_to='Previous') -> int:
        if self.previous is None or self.kind is None:
            raise ValueError('Start an exact, unknown or text search first')
        if mode not in FILTERS:
            raise ValueError('Unsupported search filter')
        if compare_to not in ('Previous', 'Initial'):
            raise ValueError('Comparison must use the previous or initial snapshot')
        width = self._width()
        if self.kind == TEXT_KIND:
            if mode in ('Increased', 'Decreased'):
                raise ValueError('Text supports Exact, Changed and Unchanged filters only')
            target = (self.encode_text(text, self.text_encoding)
                      if mode == 'Exact' else None)
            if target is not None and len(target) != width:
                raise ValueError('Text filter length must match initial search; start a new scan')
        else:
            target = encode_value(self.kind, text) if mode == 'Exact' else None
        latest = self._read(ram)
        old = self.initial if compare_to == 'Initial' else self.previous
        flags = bytearray(self._slots(width))
        count = 0
        unpack = (struct.Struct('>' + FORMATS[self.kind][0]).unpack_from
                  if self.kind != TEXT_KIND else None)
        stride = self._stride(width)
        for slot in range(len(flags)):
            if self.active is not None and not self.active[slot]:
                continue
            offset = slot * stride
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
        width = self._width()
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
        width = self._width()
        unpack = (struct.Struct('>' + FORMATS[self.kind][0]).unpack
                  if self.kind != TEXT_KIND else None)
        result = []
        offsets = list(self._addresses(limit))
        current = {}
        if ram is not None:
            # Nearby addresses share one guest RAM read. Dense unknown scans
            # would otherwise make 200 separate process-memory syscalls/poll.
            groups = []
            for off in offsets:
                if not groups or off + width - groups[-1][0] > 0x1000:
                    groups.append([off])
                else:
                    groups[-1].append(off)
            for group in groups:
                start, end = group[0], group[-1] + width
                blob = ram.read_guest(GUEST_BASE + start, end - start)
                if len(blob) != end - start:
                    raise OSError(f'Incomplete live value read at 0x{GUEST_BASE + start:08X}')
                for off in group:
                    current[off] = blob[off - start:off - start + width]

        def decoded(data):
            val = (data.decode(TEXT_ENCODINGS[self.text_encoding],
                               errors='replace') if self.kind == TEXT_KIND
                   else unpack(data)[0])
            return f'{val:.10g}' if isinstance(val, float) else str(val)

        for offset in offsets:
            data = (current[offset] if ram is not None else
                    self.previous[offset:offset + width])
            result.append({
                'address': GUEST_BASE + offset,
                'kind': (f'text/{self.text_encoding}' if self.kind == TEXT_KIND
                         else self.kind),
                'value': decoded(data),
                'initial': decoded(self.initial[offset:offset + width]),
                'previous': decoded(self.previous[offset:offset + width]),
                'hex': '0x' + data.hex().upper(),
            })
        return result
