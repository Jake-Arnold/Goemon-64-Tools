"""Read-only original-USA file_12 entity-streaming opcode anchor verifier.

No ROM content, original assembly, entity data, or extracted assets are emitted.
Run: python3 -m decomp.file12_spatial_probe --rom /path/to/USA.decompressed.z64
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

USA_DECOMPRESSED_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
USA_DECOMPRESSED_SIZE = 33_554_432
FILE12_ROM_START = 0x5C8770
FILE12_ROM_CODE_END = 0x5E3C90
FILE12_VRAM_START = 0x8020D2A0

# (virtual PC, opcode, source reg, destination reg, immediate, evidence label)
# Decoded instruction fields only; no instruction bytes or copied game data.
I_ANCHORS = (
    (0x8020D500, 0x24, 17, 12, 0x10, "spatial scan reads placement active byte"),
    (0x8020D508, 0x05, 12, 0, 0x32, "skip occupied placement"),
    (0x8020D5B8, 0x28, 12, 10, 0x10, "mark placement active"),
    (0x8020D5CC, 0x2B, 16, 13, 0x68, "set active actor state 8"),
    (0x8020D5D0, 0x2B, 16, 11, 0x70, "store actor placement pointer"),
    (0x8020D5D8, 0x09, 17, 17, 0x14, "next 20-byte placement record"),
    (0x80218A98, 0x25, 2, 24, 0x0, "load actor ID from resolved definition"),
    (0x80218AA4, 0x29, 16, 24, 0x5C, "store actor ID"),
    (0x80218AD8, 0x21, 6, 13, 0x0, "source X"),
    (0x80218AF0, 0x39, 3, 6, 0x8, "destination X float"),
    (0x80218AF4, 0x21, 6, 14, 0x2, "source Y"),
    (0x80218B04, 0x39, 3, 10, 0xC, "destination Y float"),
    (0x80218B08, 0x21, 6, 15, 0x4, "source Z"),
    (0x80218B18, 0x39, 3, 18, 0x10, "destination Z float"),
    (0x80218B1C, 0x25, 6, 24, 0x6, "source parameter 1"),
    (0x80218B20, 0x29, 3, 24, 0x14, "destination parameter 1"),
    (0x80218B24, 0x25, 6, 25, 0x8, "source parameter 2"),
    (0x80218B2C, 0x29, 3, 25, 0x16, "destination parameter 2"),
    (0x80218B30, 0x25, 6, 9, 0xA, "source parameter 3"),
    (0x80218B38, 0x29, 3, 9, 0x18, "destination parameter 3"),
    (0x80218B5C, 0x2B, 16, 0, 0x70, "initializer clears placement link"),
    (0x80218B68, 0x28, 16, 25, 0x76, "initializer stores range multiplier byte"),
    (0x8021A330, 0x23, 4, 14, 0x68, "read actor lifecycle flags"),
    (0x8021A334, 0x0C, 14, 15, 0x8, "test lifecycle flag 0x8"),
    (0x8021A340, 0x23, 4, 3, 0x70, "load actor placement link"),
    (0x8021A34C, 0x21, 3, 24, 0x0, "compare placement X"),
    (0x8021A390, 0x24, 4, 25, 0x76, "read actor range multiplier byte"),
    (0x8021A3D8, 0x21, 3, 8, 0x2, "compare placement Y"),
    (0x8021A424, 0x21, 3, 9, 0x4, "compare placement Z"),
    (0x8021A4B8, 0x28, 3, 0, 0x10, "clear placement active byte"),
    (0x8021A4BC, 0x09, 0, 14, 0x2, "prepare actor state 2"),
    (0x8021A4C0, 0x2B, 4, 0, 0x70, "clear actor placement link"),
    (0x8021A4C4, 0x2B, 4, 14, 0x68, "set actor state 2"),
)
JAL_ANCHORS = (
    (0x8020D354, 0x8020D36C, "entry calls spatial grid scanner"),
    (0x8020D5BC, 0x80218A54, "spatial scan calls actor initializer"),
    (0x8020DAFC, 0x80218A54, "alternate caller 1"),
    (0x8020DC18, 0x80218A54, "alternate caller 2"),
    (0x80218F14, 0x8021A328, "actor update calls range/removal check"),
)


def file12_offset(pc: int) -> int:
    """Map an original file_12 instruction's guest PC to decompressed-ROM offset."""
    offset = FILE12_ROM_START + (pc - FILE12_VRAM_START)
    if not (FILE12_ROM_START <= offset < FILE12_ROM_CODE_END) or pc % 4:
        raise ValueError(f"Not an aligned file_12 code address: 0x{pc:08X}")
    return offset


def check_anchors(rom: bytes) -> list[str]:
    errors = []
    for pc, op, rs, rt, imm, label in I_ANCHORS:
        word = struct.unpack_from(">I", rom, file12_offset(pc))[0]
        actual = ((word >> 26) & 63, (word >> 21) & 31,
                  (word >> 16) & 31, word & 0xFFFF)
        if actual != (op, rs, rt, imm):
            errors.append(f"0x{pc:08X} {label}: decoded fields mismatch")
    for pc, target, label in JAL_ANCHORS:
        word = struct.unpack_from(">I", rom, file12_offset(pc))[0]
        actual_op = (word >> 26) & 63
        actual_target = ((pc + 4) & 0xF0000000) | ((word & 0x03FFFFFF) << 2)
        if actual_op != 3 or actual_target != target:
            errors.append(f"0x{pc:08X} {label}: call mismatch")
    return errors


def audit(rom: bytes) -> dict:
    sha1 = hashlib.sha1(rom).hexdigest()
    if len(rom) != USA_DECOMPRESSED_SIZE or sha1 != USA_DECOMPRESSED_SHA1:
        raise ValueError("Input is not the verified original 32 MiB decompressed USA ROM")
    problems = check_anchors(rom)
    if problems:
        raise ValueError("ROM instruction anchor mismatch: " + "; ".join(problems))
    return {
        "status": "original_usa_file12_anchors_match",
        "decompressed_rom_sha1": sha1,
        "file12_rom_start": f"0x{FILE12_ROM_START:X}",
        "file12_vram_start": f"0x{FILE12_VRAM_START:X}",
        "instruction_anchor_count": len(I_ANCHORS) + len(JAL_ANCHORS),
        "scope": "static original-code opcode anchors only; no gameplay, C or linked-ROM proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="Original verified decompressed USA ROM")
    args = parser.parse_args()
    print(json.dumps(audit(args.rom.read_bytes()), indent=2))


if __name__ == "__main__":
    main()
