"""Narrow ELF32 big-endian MIPS .text tail trim preserving .rel.text records.

For a *private scratch build* only. Unlike ``objcopy --update-section``, this
edits the section-header length/alignment in place without removing relocations.
Rejects nonzero tails, truncation of relocation sites, and unexpected ELF types.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import struct


def trim_text_section(data: bytes, new_size: int) -> bytes:
    raw = bytearray(data)
    if len(raw) < 52 or raw[:4] != b"\x7fELF" or raw[4] != 1 or raw[5] != 2:
        raise ValueError("Expected ELF32 big-endian MIPS object")
    if struct.unpack_from(">H", raw, 18)[0] != 8:
        raise ValueError("Expected EM_MIPS")
    shoff = struct.unpack_from(">I", raw, 32)[0]
    shentsize, shnum, shstrndx = struct.unpack_from(">HHH", raw, 46)
    if shentsize < 40 or shnum == 0 or shstrndx >= shnum or shoff + shnum * shentsize > len(raw):
        raise ValueError("Invalid section header table")

    def header(n: int) -> int:
        return shoff + n * shentsize

    strings_header = header(shstrndx)
    strings_offset, strings_size = struct.unpack_from(">II", raw, strings_header + 16)
    if strings_offset + strings_size > len(raw):
        raise ValueError("Truncated section name table")
    sections: dict[str, int] = {}
    for index in range(shnum):
        location = header(index)
        name_offset = struct.unpack_from(">I", raw, location)[0]
        if name_offset >= strings_size:
            raise ValueError("Section name out of bounds")
        start = strings_offset + name_offset
        try:
            end = raw.index(0, start, strings_offset + strings_size)
        except ValueError as exc:
            raise ValueError("Unterminated section name") from exc
        sections[raw[start:end].decode("ascii")] = location
    if ".text" not in sections:
        raise ValueError("No .text section")
    text = sections[".text"]
    offset, old_size = struct.unpack_from(">II", raw, text + 16)
    if new_size <= 0 or new_size % 4 or new_size > old_size:
        raise ValueError("Invalid target .text size")
    if offset + old_size > len(raw) or any(raw[offset + new_size:offset + old_size]):
        raise ValueError("Nonzero or truncated .text padding")
    if ".rel.text" in sections:
        reloc = sections[".rel.text"]
        if struct.unpack_from(">I", raw, reloc + 4)[0] != 9:
            raise ValueError("Expected SHT_REL for .rel.text")
        rel_offset, rel_size = struct.unpack_from(">II", raw, reloc + 16)
        if rel_size % 8 or rel_offset + rel_size > len(raw):
            raise ValueError("Invalid ELF32 relocation table")
        for pos in range(rel_offset, rel_offset + rel_size, 8):
            if struct.unpack_from(">I", raw, pos)[0] >= new_size:
                raise ValueError("Trimming would discard a text relocation")
    struct.pack_into(">I", raw, text + 20, new_size)
    struct.pack_into(">I", raw, text + 32, 4)
    return bytes(raw)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("object_file", type=Path)
    parser.add_argument("size", type=lambda s: int(s, 0))
    args = parser.parse_args(argv)
    raw = args.object_file.read_bytes()
    result = trim_text_section(raw, args.size)
    args.object_file.write_bytes(result)
    print(f"Preserved relocations; trimmed {args.object_file} to 0x{args.size:X} bytes")


if __name__ == "__main__":
    main()