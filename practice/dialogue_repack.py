"""Pinned USA ROM retail repacker for the Goemon Dialogue tab.

Uses the original retail file's compression decisions and the verified LZKN64
Python module. No game assets or compressed resources are embedded in source.
The original USA uses CIC-6102; other bootcodes/regions are rejected.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import struct
import tempfile
import zlib

from practice.dialogue_rom import (
    FILE_TABLE_ENTRIES, ORIGINAL_LAST_FILE_END, RESOURCE_TABLE, ROM_SIZE,
    DialogueRecord, load_usa_image, patch_image,
)

USA_RETAIL_SHA1 = 'df8083a54296b8c151917c5333e1c85f014a2a66'
USA_RETAIL_SIZE = 16 * 1024 * 1024
USA_CIC_6102_BOOTCODE_CRC = 0x90BB6CB5
FIRST_FILE_OFFSET = 0x576E00
TABLE_END = RESOURCE_TABLE + 4 * (FILE_TABLE_ENTRIES + 1)


def load_usa_retail(source: str | Path) -> bytes:
    original = Path(source).read_bytes()
    if len(original) != USA_RETAIL_SIZE or hashlib.sha1(original).hexdigest() != USA_RETAIL_SHA1:
        raise ValueError('Expected the original USA 16 MiB retail ROM (SHA-1 pinned)')
    return original


def _rol(value: int, count: int) -> int:
    count &= 31
    return ((value << count) | (value >> ((32 - count) & 31))) & 0xFFFFFFFF


def _update_usa_crc(rom: bytearray) -> None:
    """N64 CIC-6102 CRC1/CRC2 over [0x1000,0x101000)."""
    if zlib.crc32(rom[0x40:0x1000]) & 0xFFFFFFFF != USA_CIC_6102_BOOTCODE_CRC:
        raise ValueError('Refusing unknown N64 CIC bootcode')
    seed = 0xF8CA4DDC
    t1 = t2 = t3 = t4 = t5 = t6 = seed
    for (word,) in struct.iter_unpack('>I', rom[0x1000:0x101000]):
        if t6 + word > 0xFFFFFFFF:
            t4 = (t4 + 1) & 0xFFFFFFFF
        t6 = (t6 + word) & 0xFFFFFFFF
        t3 ^= word
        rotated = _rol(word, word & 31)
        t5 = (t5 + rotated) & 0xFFFFFFFF
        if t2 > word:
            t2 ^= rotated
        else:
            t2 ^= t6 ^ word
        t1 = (t1 + (t5 ^ word)) & 0xFFFFFFFF
    struct.pack_into('>II', rom, 0x10, t6 ^ t4 ^ t3, t5 ^ t2 ^ t1)


def repack_usa_retail(patched_image: bytes, original_retail: bytes) -> bytes:
    """Recompress all files, rewrite retail offsets/flags and fix CIC CRCs.

    A decompressed image must originate from the separately pinned ROM patcher;
    do not call this with arbitrary edited file tables or unknown game regions.
    All file-table entries are checked before invoking compression.
    """
    if len(patched_image) != ROM_SIZE or patched_image[:4] != b'\x80\x37\x12\x40':
        raise ValueError('Expected a 32 MiB big-endian USA decompressed image')
    if len(original_retail) != USA_RETAIL_SIZE or hashlib.sha1(original_retail).hexdigest() != USA_RETAIL_SHA1:
        raise ValueError('Expected the original USA 16 MiB retail ROM')
    if patched_image.find(b'Nisitenma-Ichigo') != RESOURCE_TABLE - 16:
        raise ValueError('Unexpected resource-table signature')

    try:
        import lzkn64
    except ImportError as exc:
        raise RuntimeError('Retail rebuild requires the lzkn64 Python package (pip install lzkn64)') from exc

    starts = [struct.unpack_from('>I', patched_image, RESOURCE_TABLE + 4 * i)[0]
              for i in range(FILE_TABLE_ENTRIES + 1)]
    if (starts[0] != FIRST_FILE_OFFSET or starts[-1] != 0 or
            any(s <= 0 or s > ROM_SIZE for s in starts[:-1]) or
            any(b < a for a, b in zip(starts[:-2], starts[1:-1]))):
        raise ValueError('Invalid decompressed resource table')
    raw_entries = [struct.unpack_from('>I', original_retail, RESOURCE_TABLE + 4 * i)[0]
                   for i in range(FILE_TABLE_ENTRIES + 1)]
    if raw_entries[-1] != 0 or (raw_entries[0] & 0x7FFFFFFF) != FIRST_FILE_OFFSET:
        raise ValueError('Unexpected original retail resource table')
    # The decompressed file table is kept uncompressed; its real last file is
    # empty and its end is represented by the terminating zero entry.
    if starts[-2] < ORIGINAL_LAST_FILE_END:
        raise ValueError('Original resource extent was truncated')
    result = bytearray(patched_image[:FIRST_FILE_OFFSET])
    for i in range(FILE_TABLE_ENTRIES):
        start = starts[i]
        end = starts[i + 1] if i + 1 < FILE_TABLE_ENTRIES else start
        if not start <= end <= ROM_SIZE:
            raise ValueError(f'Invalid decompressed resource bounds at index {i}')
        data = patched_image[start:end]
        compress = bool(raw_entries[i] & 0x80000000)
        if compress and data:
            data = lzkn64.compress(data)
            if len(data) & 1:
                data += b'\0'
        offset = len(result)
        if offset >= 0x80000000:
            raise ValueError('Retail file offset exceeds file table range')
        struct.pack_into('>I', result, RESOURCE_TABLE + i * 4,
                         offset | (0x80000000 if compress and data else 0))
        result.extend(data)
        if len(result) > USA_RETAIL_SIZE:
            raise ValueError('Repacked resources exceed the 16 MiB USA cartridge size')
    struct.pack_into('>I', result, RESOURCE_TABLE + FILE_TABLE_ENTRIES * 4, 0)
    result.extend(b'\0' * (USA_RETAIL_SIZE - len(result)))
    _update_usa_crc(result)
    return bytes(result)


def save_retail_rom(decompressed_source: str | Path, retail_source: str | Path,
                    destination: str | Path, records: list[DialogueRecord],
                    replacements: dict[str, str]) -> str:
    """Build output atomically without altering either original ROM."""
    source = Path(decompressed_source)
    retail = Path(retail_source)
    destination = Path(destination)
    if destination.resolve() in {source.resolve(), retail.resolve()}:
        raise ValueError('Output path must not replace either source ROM')
    patched = patch_image(load_usa_image(source), records, replacements)
    output = repack_usa_retail(patched, load_usa_retail(retail))
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged_name = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.goemon-rom-build-', suffix='.z64',
                                         dir=destination.parent, delete=False) as file:
            staged_name = file.name
            file.write(output)
        os.replace(staged_name, destination)
    finally:
        if staged_name and os.path.exists(staged_name):
            os.unlink(staged_name)
    return hashlib.sha1(output).hexdigest()
