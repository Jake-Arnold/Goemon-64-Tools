"""ROM-bound addressing and delay-slot guard for USA VM text loop 0x8003DBEC.

Usage: python test_vm_text_loop_addressing.py PATH_TO_ORIGINAL_ASM [DECOMPRESSED_ROM]
The ROM argument enables full 118-word and function-hash validation. This is
original-instruction evidence, not a C match or in-game verification.
"""
import argparse
import hashlib
import re
import struct
import unittest
from pathlib import Path

START = 0x8003DBEC
END = 0x8003DDC4
ROM_OFFSET = 0x3E7EC
VMA_BIAS = 0x7FFFF400
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
FUNCTION_SHA256 = "4ee117dd31f6b8f3ab30ca864c202eb7c974c28cc8236d233a94228b36a0a764"
ROW = re.compile(
    r"/\*\s+([0-9A-Fa-f]+)\s+(8003[0-9A-Fa-f]{4})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)"
)

ANCHORS = {
    # $s1 is the address of global storage, not the script pointer's pointee.
    0x8003DC38: r"lui\s+\$s1,\s*%hi\(D_801C77E8_1C83E8\)",
    0x8003DC3C: r"addiu\s+\$s1,\s*\$s1,\s*%lo\(D_801C77E8_1C83E8\)",
    0x8003DC5C: r"lw\s+\$a1,\s*0x0\(\$s1\)",
    0x8003DC6C: r"sw\s+\$v0,\s*0x0\(\$s1\)",
    # +0xA is a separate halfword in the global record.
    0x8003DC98: r"sh\s+\$zero,\s*0xA\(\$s1\)",
    0x8003DCD4: r"lhu\s+\$t2,\s*0xA\(\$s1\)",
    0x8003DD58: r"sh\s+\$t7,\s*0xA\(\$s1\)",
    # CONTROLLER_W halfwords are unsigned: +2 held, +4 pressed.
    0x8003DCC8: r"lhu\s+\$t0,\s*0x4\(\$s3\)",
    0x8003DD1C: r"lhu\s+\$t3,\s*0x2\(\$s3\)",
    0x8003DD48: r"lhu\s+\$t5,\s*0x4\(\$s3\)",
}

# The branch-likely delay slot runs only when its branch is taken. Checking the
# exact address and instruction in each slot guards the original annul logic.
LIKELY_SLOTS = {
    0x8003DC8C: (
        r"bnel\s+\$fp,\s*\$v1,\s*\.L8003DCA0_3E8A0",
        0x8003DC90,
        r"lw\s+\$t8,\s*0x0\(\$s1\)",
    ),
    0x8003DCC0: (
        r"bnel\s+\$t9,\s*\$zero,\s*\.L8003DD70_3E970",
        0x8003DCC4,
        r"lw\s+\$t8,\s*0x44\(\$sp\)",
    ),
    0x8003DCD0: (
        r"beql\s+\$t1,\s*\$zero,\s*\.L8003DD0C_3E90C",
        0x8003DCD4,
        r"lhu\s+\$t2,\s*0xA\(\$s1\)",
    ),
    0x8003DD14: (
        r"beql\s+\$t2,\s*\$zero,\s*\.L8003DD4C_3E94C",
        0x8003DD18,
        r"lhu\s+\$t5,\s*0x4\(\$s3\)",
    ),
    0x8003DD50: (
        r"beql\s+\$t6,\s*\$zero,\s*\.L8003DD70_3E970",
        0x8003DD54,
        r"lw\s+\$t8,\s*0x44\(\$sp\)",
    ),
    0x8003DD8C: (
        r"bnel\s+\$at,\s*\$zero,\s*\.L8003DC60_3E860",
        0x8003DD90,
        r"lw\s+\$a1,\s*0x0\(\$s1\)",
    ),
}
LIKELY_MNEMONICS = {"beql", "bnel", "bgezl", "bgtzl", "bltzl", "blezl"}


def parse_rows(text: str) -> dict[int, tuple[int, int, str]]:
    rows: dict[int, tuple[int, int, str]] = {}
    for line in text.splitlines():
        match = ROW.search(line)
        if match is None:
            continue
        address = int(match.group(2), 16)
        if not START <= address < END:
            continue
        if address in rows:
            raise ValueError(f"duplicate original VMA: {address:#x}")
        offset = int(match.group(1), 16)
        expected_offset = address - VMA_BIAS
        if offset != expected_offset:
            raise AssertionError(f"ROM/VMA offset mismatch at {address:#x}")
        rows[address] = (offset, int(match.group(3), 16), match.group(4).strip())
    return rows


def verify(assembly: str, rom: bytes | None = None) -> None:
    rows = parse_rows(assembly)
    expected_addresses = set(range(START, END, 4))
    if set(rows) != expected_addresses:
        raise AssertionError("original function extent is not 472 bytes / 118 words")

    for address, pattern in ANCHORS.items():
        if re.fullmatch(pattern, rows[address][2]) is None:
            raise AssertionError(
                f"original addressing mismatch at {address:#x}: {rows[address][2]!r}"
            )

    observed_likely = {
        address
        for address, (_, _, instruction) in rows.items()
        if instruction.split() and instruction.split()[0] in LIKELY_MNEMONICS
    }
    if observed_likely != set(LIKELY_SLOTS):
        raise AssertionError(
            f"branch-likely set differs: expected {sorted(LIKELY_SLOTS)}, "
            f"got {sorted(observed_likely)}"
        )
    for branch_address, (branch_pattern, delay_address, delay_pattern) in LIKELY_SLOTS.items():
        if re.fullmatch(branch_pattern, rows[branch_address][2]) is None:
            raise AssertionError(
                f"branch-likely differs at {branch_address:#x}: {rows[branch_address][2]!r}"
            )
        if re.fullmatch(delay_pattern, rows[delay_address][2]) is None:
            raise AssertionError(
                f"branch-likely delay slot differs at {delay_address:#x}: "
                f"{rows[delay_address][2]!r}"
            )

    if rom is not None:
        if len(rom) != 33_554_432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
            raise AssertionError("decompressed USA ROM length/SHA-1 differs from pinned image")
        extent = rom[ROM_OFFSET:ROM_OFFSET + END - START]
        if hashlib.sha256(extent).hexdigest() != FUNCTION_SHA256:
            raise AssertionError("original text-loop SHA-256 differs from pinned extent")
        for address, (offset, word, _) in rows.items():
            if rom[offset:offset + 4] != struct.pack(">I", word):
                raise AssertionError(f"Splat word differs from ROM at {address:#x}")

    proof_level = "ROM-bound" if rom is not None else "Splat-extent"
    print(
        f"VM text loop: {proof_level}; 472 bytes / {len(rows)} words, "
        f"{len(ANCHORS)} storage/controller anchors, "
        f"{len(LIKELY_SLOTS)} branch-likely delay slots"
    )


class TextLoopAddressGuardTests(unittest.TestCase):
    def test_extent_required(self):
        with self.assertRaisesRegex(AssertionError, "472 bytes / 118 words"):
            verify("")

    def test_duplicate_vma_rejected(self):
        row = "/* 3E7EC 8003DBEC 27BDFFB8 */ addiu $sp, $sp, -0x48"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_rows(f"{row}\n{row}")

    def test_rom_vma_offset_rejected(self):
        with self.assertRaisesRegex(AssertionError, "ROM/VMA"):
            parse_rows("/* 3E7F0 8003DBEC 27BDFFB8 */ addiu $sp, $sp, -0x48")

    def test_six_likely_slots_are_unique_and_inside_extent(self):
        self.assertEqual(len(LIKELY_SLOTS), 6)
        self.assertEqual(len(set(LIKELY_SLOTS)), 6)
        self.assertTrue(all(START <= address < END for address in LIKELY_SLOTS))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_asm", type=Path, nargs="?")
    parser.add_argument("rom", type=Path, nargs="?")
    args = parser.parse_args()
    if args.original_asm is None:
        if args.rom is not None:
            parser.error("provide original_asm before rom")
        unittest.main(argv=["test_vm_text_loop_addressing"])
    if args.rom is not None:
        verify(args.original_asm.read_text(encoding="utf-8"), args.rom.read_bytes())
    else:
        verify(args.original_asm.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
