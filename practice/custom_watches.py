"""Persistent user-defined guest-RAM watches for Live memory.

This module reads memory and saves user watch definitions; it never writes game
RAM. Its names do not become confirmed built-in address mappings.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import struct

from practice.inspector import Watch

FORMATS = {
    'u8': ('B', 1), 's8': ('b', 1),
    'u16': ('H', 2), 's16': ('h', 2),
    'u32': ('I', 4), 's32': ('i', 4),
    'f32': ('f', 4), 'f64': ('d', 8),
    'hex8': (None, 8),
}
FORMAT_ID = 'goemon-custom-watches-v1'
MAX_WATCHES = 128
MIN_ADDR = 0x80000000
MAX_ADDR_EXCLUSIVE = 0x80800000


@dataclass(frozen=True)
class CustomWatch:
    name: str
    address: int
    kind: str

    @property
    def width(self):
        return FORMATS[self.kind][1]

    @property
    def row_name(self):
        return f'Custom: {self.name}'


def parse_address(text):
    raw = text.strip()
    if not re.fullmatch(r'(?:0[xX])?[0-9a-fA-F]{1,8}', raw):
        raise ValueError('Enter a hexadecimal N64 address, e.g. 0x8015C574')
    return int(raw, 16)


def make_watch(name, address, kind):
    name = name.strip()
    if not name or len(name) > 64 or any(ord(c) < 32 for c in name):
        raise ValueError('Watch name must contain 1–64 printable characters')
    if kind not in FORMATS:
        raise ValueError('Unknown watch type')
    addr = parse_address(address) if isinstance(address, str) else address
    if type(addr) is not int or not MIN_ADDR <= addr < MAX_ADDR_EXCLUSIVE:
        raise ValueError('Guest address must be 0x80000000–0x807FFFFF')
    if addr + FORMATS[kind][1] > MAX_ADDR_EXCLUSIVE:
        raise ValueError('Watch extends beyond guest RAM')
    return CustomWatch(name, addr, kind)


def append_watch(entries, watch):
    if len(entries) >= MAX_WATCHES:
        raise ValueError(f'Maximum {MAX_WATCHES} watches')
    if any(item.name.casefold() == watch.name.casefold() for item in entries):
        raise ValueError('Duplicate custom watch name')
    return [*entries, watch]


def load_watches(path: Path):
    if not path.exists():
        return []
    doc = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(doc, dict) or doc.get('format') != FORMAT_ID or not isinstance(doc.get('watches'), list):
        raise ValueError('Unsupported custom watch file format')
    result = []
    for entry in doc['watches']:
        result = append_watch(result, make_watch(entry['name'], entry['address'], entry['type']))
    return result


def save_watches(path: Path, entries):
    validated = []
    for watch in entries:
        validated = append_watch(validated, make_watch(watch.name, watch.address, watch.kind))
    doc = {'format': FORMAT_ID,
           'watches': [{'name': w.name, 'address': f'0x{w.address:08X}', 'type': w.kind}
                       for w in validated]}
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def read_watch(ram, spec):
    try:
        data = ram.read_guest(spec.address, spec.width)
        if len(data) != spec.width:
            raise OSError('Incomplete memory read')
        raw = '0x' + data.hex().upper()
        fmt, _ = FORMATS[spec.kind]
        if fmt is None:
            decoded = raw
        else:
            value = struct.unpack('>' + fmt, data)[0]
            decoded = f'{value:.7g}' if isinstance(value, float) and math.isfinite(value) else str(value)
        return Watch(spec.row_name, spec.address, decoded, raw, 'CUSTOM',
                     f'user watch: {spec.kind}; unverified')
    except (OSError, ValueError, struct.error) as exc:
        return Watch(spec.row_name, spec.address, f'READ FAILED: {exc}', '—', 'ERROR',
                     f'user watch: {spec.kind}; unverified')
