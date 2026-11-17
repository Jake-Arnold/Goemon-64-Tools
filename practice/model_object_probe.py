"""Interpret a manually captured USA game Object graphics header read-only.

Source: klorfmorf/Goemon64Recomp dev patches/types.h, Object / OverlayInfo.
No guest RAM access, pointer follow, model extraction, file writes, or actor ID
inference. This source layout was established for the USA version ONLY.

Project64 original-USA execution breakpoint at func_80018CA0_198A0:
  a0: Skeleton*; a1: Object*. Copy 0x68 bytes starting at a1.
The register value is a temporary runtime pointer and must be observed in-game.
"""
from __future__ import annotations

import argparse
import json
import re
import struct

OBJECT_HEADER_BYTES = 0x68
GRAPHICS_1_OFFSET = 0x2C
GRAPHICS_2_OFFSET = 0x30
OVERLAY_INFO_OFFSET = 0x34
OVERLAY_INFO_STRIDE = 8
OVERLAY_COUNT = 6
MAX_FILE_ID = 1310


def parse_snapshot_hex(value):
    """Accept exactly 104 byte values; refuse row addresses and bad tokens."""
    if not isinstance(value, str):
        raise ValueError('Snapshot must be text')
    # Accept a plain 208-nibble hex stream or 104 whitespace-delimited bytes,
    # not copied addresses mixed with data (which could silently corrupt it).
    text = value.strip()
    if text.startswith('0x') and not any(c.isspace() for c in text):
        text = text[2:]
    if re.fullmatch(r'[a-fA-F0-9]{208}', text):
        return bytes.fromhex(text)
    tokens = text.split()
    if len(tokens) != OBJECT_HEADER_BYTES or any(not re.fullmatch(r'[a-fA-F0-9]{2}', x) for x in tokens):
        raise ValueError('Paste exactly 0x68 bytes: 208 hex digits or 104 two-digit hex byte tokens; omit address columns')
    return bytes(int(x, 16) for x in tokens)


def interpret_usa_object_graphics(snapshot):
    """Return structured, non-persistent metadata with unverified identity."""
    if not isinstance(snapshot, bytes) or len(snapshot) != OBJECT_HEADER_BYTES:
        raise ValueError('USA Object graphics snapshot must be exactly 0x68 bytes')
    graphics_1, graphics_2 = struct.unpack_from('>II', snapshot, GRAPHICS_1_OFFSET)
    overlays=[]
    for index in range(OVERLAY_COUNT):
        off = OVERLAY_INFO_OFFSET + OVERLAY_INFO_STRIDE*index
        file_id, unk2, vram = struct.unpack_from('>HHI', snapshot, off)
        overlays.append(dict(index=index, file_id=file_id,
                             plausible_rom_file_id=1 <= file_id <= MAX_FILE_ID,
                             file_id_hex=f'0x{file_id:03X}',
                             vram_addr=f'0x{vram:08X}',
                             unknown_2=f'0x{unk2:04X}'))
    return dict(format='goemon-usa-object-graphics-header-v1',region='usa',
                evidence='Manually supplied Object struct bytes; not authenticated as a live actor',
                graphics_1=f'0x{graphics_1:08X}',graphics_2=f'0x{graphics_2:08X}',
                overlays=overlays,source='Goemon64Recomp dev patches/types.h',
                warning='Pointers and file IDs are unverified until correlated with game debugger registers and draw calls; not an actor or model assignment')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hex', required=True, help='0x68 contiguous bytes or 104 whitespace-separated byte hex values (no address columns)')
    args=parser.parse_args(argv)
    try:
        result=interpret_usa_object_graphics(parse_snapshot_hex(args.hex))
        print(json.dumps(result,indent=2,sort_keys=True))
    except ValueError as exc:
        parser.exit(1,f'Invalid snapshot: {exc}\n')


if __name__ == '__main__':
    main()
