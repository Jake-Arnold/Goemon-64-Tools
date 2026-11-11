"""ROM-bound CFG anchors for USA VM main-step 0x8003D68C.

Run with the private Splat listing and decompressed USA ROM. This guards the
observed control-flow map; it is not a C translation or a matching-C proof.
"""
import argparse
import hashlib
import re
import struct
import unittest
from pathlib import Path

START = 0x8003D68C
END = 0x8003D9B8
ROM_OFFSET = 0x3E28C
VMA_BIAS = 0x7FFFF400
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
FUNCTION_SHA256 = "e49ad551d97f2f8cac887ee126e99dfdb29924901a4ff69f0792898207bf3da5"
ROW = re.compile(
    r"/\*\s+([0-9A-Fa-f]+)\s+(8003[0-9A-Fa-f]{4})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)"
)

ANCHORS = {
    0x8003D68C: r"addiu\s+\$sp,\s*\$sp,\s*-0x28",
    0x8003D69C: r"lw\s+\$t6,\s*0x0\(\$s1\)",
    0x8003D6A8: r"bnez\s+\$t6,\s*\.L8003D6B8_3E2B8",
    0x8003D6AC: r"sw\s+\$s0,\s*0x18\(\$sp\)",
    0x8003D6BC: r"lbu\s+\$t7,\s*%lo\(D_801C78FC_1C84FC\)\(\$t7\)",
    0x8003D6C0: r"beqz\s+\$t7,\s*\.L8003D6D0_3E2D0",
    0x8003D6CC: r"addiu\s+\$v0,\s*\$zero,\s*0x2",
    0x8003D6D0: r"jal\s+func_8003D17C_3DD7C",
    0x8003D6E4: r"beql\s+\$s0,\s*\$zero,\s*\.L8003D9A0_3E5A0",
    0x8003D6F4: r"sltiu\s+\$at,\s*\$t9,\s*0x7",
    0x8003D70C: r"jr\s+\$t9",
    0x8003D714: r"jal\s+func_8003DBEC_3E7EC",
    0x8003D754: r"jal\s+func_8003E5EC_3F1EC",
    0x8003D760: r"bnez\s+\$t0,\s*\.L8003D770_3E370",
    0x8003D778: r"jal\s+func_8003E620_3F220",
    0x8003D79C: r"jal\s+func_8003E654_3F254",
    0x8003D7AC: r"lw\s+\$v0,\s*0x0\(\$s0\)",
    0x8003D7C0: r"sltiu\s+\$at,\s*\$t3,\s*0x1F",
    0x8003D7C4: r"beqz\s+\$at,\s*\.L8003D988_3E588",
    0x8003D7C8: r"sw\s+\$t2,\s*0x0\(\$s1\)",
    0x8003D7DC: r"jr\s+\$t3",
    0x8003D7E4: r"jal\s+func_8003DB0C_3E70C",
    0x8003D828: r"jal\s+func_8003D9B8_3E5B8",
    0x8003D830: r"bnez\s+\$v0,\s*\.L8003D84C_3E44C",
    0x8003D854: r"jal\s+func_8003D428_3E028",
    0x8003D864: r"sb\s+\$t1,\s*%lo\(D_801C7930_1C8530\)\(\$at\)",
    0x8003D888: r"lw\s+\$s0,\s*0x0\(\$s1\)",
    0x8003D88C: r"lw\s+\$a2,\s*0x0\(\$s0\)",
    0x8003D898: r"jalr\s+\$a2",
    0x8003D8B8: r"jal\s+func_8003DBEC_3E7EC",
    0x8003D8BC: r"sw\s+\$v0,\s*%lo\(D_801C77E8_1C83E8\)\(\$at\)",
    0x8003D8C4: r"beqz\s+\$s0,\s*\.L8003D994_3E594",
    0x8003D8D8: r"bne\s+\$t6,\s*\$at,\s*\.L8003D8E8_3E4E8",
    0x8003D8F0: r"jal\s+func_8003E6C0_3F2C0",
    0x8003D918: r"jal\s+func_80024038_24C38",
    0x8003D934: r"jal\s+func_80024088_24C88",
    0x8003D950: r"jal\s+func_800240DC_24CDC",
    0x8003D958: r"beql\s+\$v0,\s*\$zero,\s*\.L8003D978_3E578",
    0x8003D964: r"jal\s+func_8003DE48_3EA48",
    0x8003D988: r"jal\s+func_8003D428_3E028",
    0x8003D994: r"bnel\s+\$s0,\s*\$zero,\s*\.L8003D6F0_3E2F0",
    0x8003D9A0: r"lw\s+\$ra,\s*0x24\(\$sp\)",
    0x8003D9B0: r"jr\s+\$ra",
    0x8003D9B4: r"addiu\s+\$sp,\s*\$sp,\s*0x28",
}

TABLES = {
    0x8007CF94: [
        0x8003D714, 0x8003D724, 0x8003D734, 0x8003D744,
        0x8003D754, 0x8003D778, 0x8003D79C,
    ],
    0x8007CFB0: [
        0x8003D7E4, 0x8003D988, 0x8003D800, 0x8003D988,
        0x8003D854, 0x8003D988, 0x8003D870, 0x8003D888,
        0x8003D988, 0x8003D988, 0x8003D988, 0x8003D988,
        0x8003D8A8, 0x8003D8F0, 0x8003D988, 0x8003D988,
        0x8003D988, 0x8003D988, 0x8003D988, 0x8003D988,
        0x8003D988, 0x8003D988, 0x8003D988, 0x8003D988,
        0x8003D988, 0x8003D988, 0x8003D988, 0x8003D988,
        0x8003D90C, 0x8003D928, 0x8003D944,
    ],
}


def parse_rows(source: str) -> dict[int, tuple[int, int, str]]:
    rows = {}
    for line in source.splitlines():
        match = ROW.search(line)
        if match is None:
            continue
        address = int(match.group(2), 16)
        if not START <= address < END:
            continue
        if address in rows:
            raise ValueError(f"duplicate original VMA: {address:#x}")
        offset = int(match.group(1), 16)
        expected_offset = ROM_OFFSET + address - START
        if offset != expected_offset:
            raise AssertionError(f"ROM/VMA offset mismatch at {address:#x}")
        rows[address] = (offset, int(match.group(3), 16), match.group(4).strip())
    return rows


def verify(assembly: str, rom: bytes) -> None:
    rows = parse_rows(assembly)
    expected_addresses = set(range(START, END, 4))
    if set(rows) != expected_addresses:
        raise AssertionError("original function extent is not 812 bytes / 203 words")
    if hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise AssertionError("decompressed USA ROM SHA-1 differs from the pinned image")

    image_slice = rom[ROM_OFFSET:ROM_OFFSET + END - START]
    if hashlib.sha256(image_slice).hexdigest() != FUNCTION_SHA256:
        raise AssertionError("original function SHA-256 differs from the pinned extent")
    for address, (offset, word, _) in rows.items():
        if rom[offset:offset + 4] != struct.pack(">I", word):
            raise AssertionError(f"listing word differs from ROM at {address:#x}")

    for address, pattern in ANCHORS.items():
        if re.fullmatch(pattern, rows[address][2]) is None:
            raise AssertionError(
                f"original instruction mismatch at {address:#x}: {rows[address][2]!r}"
            )

    for table_vma, expected_targets in TABLES.items():
        offset = table_vma - VMA_BIAS
        table = rom[offset:offset + 4 * len(expected_targets)]
        if len(table) != 4 * len(expected_targets):
            raise AssertionError(f"truncated dispatch table at {table_vma:#x}")
        targets = [word[0] for word in struct.iter_unpack(">I", table)]
        if targets != expected_targets:
            raise AssertionError(f"dispatch table differs at {table_vma:#x}")

    print(
        f"VM main step: {len(rows)} original words, {len(ANCHORS)} instruction "
        f"anchors, {len(TABLES[0x8007CF94])} state cases and "
        f"{len(TABLES[0x8007CFB0])} token cases passed"
    )


class ParserTests(unittest.TestCase):
    def test_duplicate_original_address_rejected(self):
        row = "/* 3E28C 8003D68C 27BDFFD8 */ addiu $sp, $sp, -0x28"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_rows(f"{row}\n{row}\n")

    def test_rom_vma_offset_rejected(self):
        with self.assertRaisesRegex(AssertionError, "ROM/VMA"):
            parse_rows("/* 3E290 8003D68C 27BDFFD8 */ addiu $sp, $sp, -0x28")

    def test_incomplete_function_rejected(self):
        with self.assertRaisesRegex(AssertionError, "812 bytes"):
            verify("", b"")

    def test_anchor_addresses_are_unique_and_inside_extent(self):
        self.assertEqual(len(ANCHORS), len(set(ANCHORS)))
        self.assertTrue(all(START <= address < END for address in ANCHORS))

    def test_jump_table_lengths(self):
        self.assertEqual(len(TABLES[0x8007CF94]), 7)
        self.assertEqual(len(TABLES[0x8007CFB0]), 31)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_asm", type=Path, nargs="?")
    parser.add_argument("rom", type=Path, nargs="?")
    args = parser.parse_args()
    if (args.original_asm is None) != (args.rom is None):
        parser.error("provide both original_asm and rom, or neither")
    if args.original_asm is not None:
        verify(
            args.original_asm.read_text(encoding="utf-8"),
            args.rom.read_bytes(),
        )
    else:
        unittest.main(argv=["test_vm_main_step_original"])


if __name__ == "__main__":
    main()
