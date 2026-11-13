"""Read one text record from the pinned decompressed Goemon USA image."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import struct

from decomp.compare_original import ROM_SHA1, ROM_SIZE

SOURCE_TABLE = 0x57FD8
VIRTUAL_TABLE = 0x556CC
MAX_RESOURCE_ID = 1311
MAX_TOKENS = 4096

# The atlas is in token order. Unverified symbols retain their numeric IDs.
GLYPHS = {token: chr(token + 32) for token in (
    0, 1, 7, 12, 13, 14, 15, 26, 27, 29, 31,
    *range(16, 26), *range(33, 59), *range(65, 91),
)}
GLYPHS.update({59: "[", 60: ",", 61: "]", 62: '"', 64: "."})
CONTROLS = {
    -71: "<close-window>",
    -70: "<open-window>",
    -63: "<clear-glyphs>",
    -62: "<state-4>",
    -61: "<state-3>",
    -60: "\n",
}


def resource_data(rom: bytes, resource_id: int) -> tuple[int, int, bytes]:
    """Return decompressed-image offset, virtual base, and exact resource bytes."""
    if not 1 <= resource_id <= MAX_RESOURCE_ID:
        raise ValueError("Resource ID must be in 1..1311")
    row = resource_id - 1
    source_row = SOURCE_TABLE + 4 * row
    virtual_row = VIRTUAL_TABLE + 8 * row
    if max(source_row, virtual_row) + 8 > len(rom):
        raise ValueError("Resource table row is truncated")
    start, end = struct.unpack_from(">II", rom, source_row)
    virtual_start, virtual_end = struct.unpack_from(">II", rom, virtual_row)
    if not (0 < start < end <= len(rom) and end - start == virtual_end - virtual_start):
        raise ValueError("Resource is empty, compressed, or has inconsistent bounds")
    return start, virtual_start, rom[start:end]


def text_operand(resource: bytes, virtual_base: int, command_offset: int) -> int:
    """Resolve a same-resource 0x8010 instruction to a resource-relative offset."""
    if command_offset < 0 or command_offset % 4 or command_offset + 8 > len(resource):
        raise ValueError("Expected a complete, word-aligned VM command")
    opcode, operand = struct.unpack_from(">II", resource, command_offset)
    if opcode != 0x8010:
        raise ValueError("Expected text opcode 0x8010 at the command offset")
    text_offset = operand - virtual_base
    if operand >= 0x80000000 or text_offset < 0 or text_offset % 2 or text_offset + 2 > len(resource):
        raise ValueError("Text operand must point to an aligned halfword in this resource")
    return text_offset


def read_tokens(resource: bytes, offset: int, *, limit: int = MAX_TOKENS) -> tuple[int, ...]:
    """Read signed big-endian tokens through the required sentinel, excluding it."""
    if offset < 0 or offset % 2 or offset + 2 > len(resource):
        raise ValueError("Expected a halfword-aligned text offset within the resource")
    if not 1 <= limit <= MAX_TOKENS:
        raise ValueError(f"Token limit must be in 1..{MAX_TOKENS}")
    end = min(len(resource) & ~1, offset + limit * 2)
    tokens = []
    for (token,) in struct.iter_unpack(">h", resource[offset:end]):
        if token == -1:
            return tuple(tokens)
        tokens.append(token)
    raise ValueError("No text terminator within the resource and token limit")


def format_tokens(tokens: tuple[int, ...]) -> str:
    """Render identified USA glyphs and retain controls and unmapped tokens."""
    return "".join(GLYPHS.get(token, CONTROLS.get(token, f"<token:{token}>")) for token in tokens)


def number(value: str) -> int:
    return int(value, 0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="Pinned decompressed USA .z64")
    parser.add_argument("resource", type=number, help="One-based resource ID")
    offset = parser.add_mutually_exclusive_group(required=True)
    offset.add_argument("--command-offset", type=number, help="Resource-relative offset of a 0x8010")
    offset.add_argument("--text-offset", type=number, help="Resource-relative offset of a text record")
    parser.add_argument("--summary", action="store_true", help="Print bounds and checksum without the dialogue")
    args = parser.parse_args(argv)

    try:
        rom = args.rom.read_bytes()
        if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
            raise ValueError("Expected the SHA-1-pinned decompressed USA image (see decomp/INPUTS.md)")
        start, virtual_base, resource = resource_data(rom, args.resource)
        text_offset = args.text_offset
        if args.command_offset is not None:
            text_offset = text_operand(resource, virtual_base, args.command_offset)
        tokens = read_tokens(resource, text_offset)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    end = text_offset + 2 * (len(tokens) + 1)
    if args.summary:
        digest = hashlib.sha256(resource[text_offset:end]).hexdigest()
        print(f"Resource {args.resource}, text +0x{text_offset:X}, "
              f"image [0x{start + text_offset:X}, 0x{start + end:X}), "
              f"{len(tokens)} tokens, SHA-256 {digest}")
    else:
        print(format_tokens(tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
