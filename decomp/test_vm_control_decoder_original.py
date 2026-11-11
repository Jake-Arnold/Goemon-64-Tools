"""ROM-bound dispatch/cursor anchors for USA VM decoder 0x8003DF98.

Requires the private Splat listing and decompressed USA ROM. This is a static
original-behavior guard, not a C model or matching-C proof.
"""
import argparse
import hashlib
import re
import struct
import unittest
from pathlib import Path

START = 0x8003DF98
END = 0x8003E1A8
ROM_OFFSET = 0x3EB98
VMA_BIAS = 0x7FFFF400
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
FUNCTION_SHA256 = "76285ca92a7f611916d867d9938f93fcb3df32ebfa2962120083f2471a501631"
PACED_START = 0x8003DE80
PACED_END = 0x8003DF68
PACED_ROM_OFFSET = 0x3EA80
PACED_SIZE = PACED_END - PACED_START
PACED_SHA256 = "011db36716ef249608412e7cbfc0a20cf3b00e6653b7d3f93ff6990a7fcad9e1"
ROW = re.compile(
    r"/\*\s+([0-9A-Fa-f]+)\s+(8003[0-9A-Fa-f]{4})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)"
)

LISTING_RANGES = (
    (0x8003DBEC, 0x8003DDC4),  # DBEC calls paced DE80 and stores its cursor.
    (0x8003DE80, 0x8003DF68),  # Paced reader and its marker/repeat contract.
    (START, END),              # Negative-token decoder.
    (0x8003EB34, 0x8003EBA4),  # Unpaced reader and its sentinel contract.
)

ANCHORS = {
    # Paced reader: signed classification, likely delay, callback reread,
    # independent sentinel/delegation exits, and return delay.
    0x8003DEB0: r"lh\s+\$v0,\s*0x0\(\$s0\)",
    0x8003DEB4: r"bltzl\s+\$v0,\s*\.L8003DF14_3EB14",
    0x8003DEB8: r"addiu\s+\$v1,\s*\$zero,\s*-1",
    0x8003DEC4: r"beqz\s+\$v0,\s*\.L8003DEE8_3EAE8",
    0x8003DEC8: r"or\s+\$a0,\s*\$s1,\s*\$zero",
    0x8003DEE8: r"jal\s+func_8000D060_DC60",
    0x8003DEEC: r"lh\s+\$a1,\s*0x0\(\$s0\)",
    0x8003DEF4: r"lh\s+\$t7,\s*0x0\(\$s0\)",
    0x8003DEF8: r"addiu\s+\$s0,\s*\$s0,\s*0x2",
    0x8003DEFC: r"beqz\s+\$v1,\s*\.L8003DEB0_3EAB0",
    0x8003DF00: r"sh\s+\$t7,\s*0x8\(\$s3\)",
    0x8003DF14: r"bne\s+\$v1,\s*\$v0,\s*\.L8003DF28_3EB28",
    0x8003DF18: r"or\s+\$a0,\s*\$s1,\s*\$zero",
    0x8003DF1C: r"sh\s+\$v1,\s*0x8\(\$s3\)",
    0x8003DF20: r"b\s+\.L8003DF4C_3EB4C",
    0x8003DF24: r"or\s+\$v0,\s*\$zero,\s*\$zero",
    0x8003DF2C: r"jal\s+func_8003DF98_3EB98",
    0x8003DF30: r"or\s+\$a1,\s*\$s0,\s*\$zero",
    0x8003DF38: r"lw\s+\$t8,\s*%lo\(D_801C7798_1C8398\)\(\$t8\)",
    0x8003DF40: r"or\s+\$s0,\s*\$v0,\s*\$zero",
    0x8003DF44: r"sw\s+\$t8,\s*%lo\(D_801C77A0_1C83A0\)\(\$at\)",
    0x8003DF48: r"or\s+\$v0,\s*\$s0,\s*\$zero",
    0x8003DF60: r"jr\s+\$ra",
    0x8003DF64: r"addiu\s+\$sp,\s*\$sp,\s*0x28",
    # Decoder input range and dispatch.
    0x8003DF98: r"addiu\s+\$sp,\s*\$sp,\s*-0x20",
    0x8003DFA4: r"lh\s+\$t6,\s*0x0\(\$a1\)",
    0x8003DFAC: r"addiu\s+\$t7,\s*\$t6,\s*0x47",
    0x8003DFB0: r"sltiu\s+\$at,\s*\$t7,\s*0x28",
    0x8003DFB4: r"beqz\s+\$at,\s*\.L8003E190_3ED90",
    0x8003DFC4: r"lw\s+\$t7,\s*%lo\(jtbl_8007D068_7DC68\)\(\$at\)",
    0x8003DFC8: r"jr\s+\$t7",
    # Selected command bodies and cursor increment after callbacks.
    0x8003DFD0: r"jal\s+func_8000C3EC_CFEC",
    0x8003DFDC: r"addiu\s+\$s0,\s*\$s0,\s*0x2",
    0x8003DFF0: r"addiu\s+\$t8,\s*\$zero,\s*0x4",
    0x8003DFF8: r"sw\s+\$t8,\s*%lo\(D_801C77E0_1C83E0\)\(\$at\)",
    0x8003E004: r"lui\s+\$a0,\s*%hi\(D_801C7754_1C8354\)",
    0x8003E00C: r"lw\s+\$a0,\s*%lo\(D_801C7754_1C8354\)\(\$a0\)",
    0x8003E120: r"lui\s+\$a0,\s*%hi\(D_801C7754_1C8354\)",
    0x8003E124: r"jal\s+func_8000C570_D170",
    0x8003E128: r"lw\s+\$a0,\s*%lo\(D_801C7754_1C8354\)\(\$a0\)",
    0x8003E130: r"lw\s+\$a0,\s*%lo\(D_801C7754_1C8354\)\(\$a0\)",
    0x8003E134: r"jal\s+func_8000C568_D168",
    0x8003E138: r"lui\s+\$a1,\s*\(0x40400000\s*>>\s*16\)",
    0x8003E158: r"lui\s+\$a0,\s*%hi\(D_801C7754_1C8354\)",
    0x8003E160: r"jal\s+func_8000C5E4_D1E4",
    0x8003E164: r"lui\s+\$a1,\s*\(0x40000000\s*>>\s*16\)",
    0x8003E168: r"lui\s+\$a0,\s*%hi\(D_801C7754_1C8354\)",
    0x8003E16C: r"jal\s+func_8000C60C_D20C",
    0x8003E170: r"lw\s+\$a0,\s*%lo\(D_801C7754_1C8354\)\(\$a0\)",
    0x8003E190: r"addiu\s+\$s0,\s*\$s0,\s*0x2",
    0x8003E198: r"or\s+\$v0,\s*\$s0,\s*\$zero",
    # Paced caller: pre-gate token, post-output token/repeat reloads, negative path.
    0x8003DEB0: r"lh\s+\$v0,\s*0x0\(\$s0\)",
    0x8003DEB4: r"bltzl\s+\$v0,\s*\.L8003DF14_3EB14",
    0x8003DEBC: r"jal\s+func_8003DF68_3EB68",
    0x8003DEC0: r"nop",
    0x8003DEE8: r"jal\s+func_8000D060_DC60",
    0x8003DEEC: r"lh\s+\$a1,\s*0x0\(\$s0\)",
    0x8003DEF0: r"lw\s+\$v1,\s*0x0\(\$s2\)",
    0x8003DEF4: r"lh\s+\$t7,\s*0x0\(\$s0\)",
    0x8003DEF8: r"addiu\s+\$s0,\s*\$s0,\s*0x2",
    0x8003DF00: r"sh\s+\$t7,\s*0x8\(\$s3\)",
    0x8003DF1C: r"sh\s+\$v1,\s*0x8\(\$s3\)",
    0x8003DF2C: r"jal\s+func_8003DF98_3EB98",
    0x8003DF30: r"or\s+\$a1,\s*\$s0,\s*\$zero",
    0x8003DF38: r"lw\s+\$t8,\s*%lo\(D_801C7798_1C8398\)\(\$t8\)",
    0x8003DF44: r"sw\s+\$t8,\s*%lo\(D_801C77A0_1C83A0\)\(\$at\)",
    # Unpaced caller: signed read before output/decoder and pointer advance after.
    0x8003EB54: r"lh\s+\$a1,\s*0x0\(\$s0\)",
    0x8003EB5C: r"bltz\s+\$a1,\s*\.L8003EB74_3F774",
    0x8003EB64: r"jal\s+func_8000D060_DC60",
    0x8003EB70: r"addiu\s+\$s0,\s*\$s0,\s*0x2",
    0x8003EB74: r"beql\s+\$s2,\s*\$a1,\s*\.L8003EB90_3F790",
    0x8003EB7C: r"jal\s+func_8003DF98_3EB98",
    0x8003EB80: r"or\s+\$a1,\s*\$s0,\s*\$zero",
    0x8003EB88: r"or\s+\$s0,\s*\$v0,\s*\$zero",
    # Paced stream wrapper stores the returned cursor after DE80 returns.
    0x8003DC5C: r"lw\s+\$a1,\s*0x0\(\$s1\)",
    0x8003DC60: r"jal\s+func_8003DE80_3EA80",
    0x8003DC64: r"lw\s+\$a0,\s*0x0\(\$s4\)",
    0x8003DC6C: r"sw\s+\$v0,\s*0x0\(\$s1\)",
}

COMMAND_TABLE = [
    0x8003E028, 0x8003E018, 0x8003E190, 0x8003E190,
    0x8003E190, 0x8003E190, 0x8003E190, 0x8003E190,
    0x8003E004, 0x8003DFF0, 0x8003DFE0, 0x8003DFD0,
    0x8003E190, 0x8003E190, 0x8003E17C, 0x8003E158,
    0x8003E144, 0x8003E120, 0x8003E108, 0x8003E0F0,
    0x8003E0DC, 0x8003E0C8, 0x8003E190, 0x8003E190,
        0x8003E190, 0x8003E190, 0x8003E190, 0x8003E190,
        0x8003E190, 0x8003E190, 0x8003E190, 0x8003E190,
        0x8003E190, 0x8003E190,
        0x8003E0B0, 0x8003E098,
    0x8003E080, 0x8003E068, 0x8003E050, 0x8003E038,
]


def parse_rows(source: str) -> dict[int, tuple[int, int, str]]:
    rows = {}
    for line in source.splitlines():
        match = ROW.search(line)
        if match is None:
            continue
        address = int(match.group(2), 16)
        if not any(lo <= address < hi for lo, hi in LISTING_RANGES):
            continue
        if address in rows:
            raise ValueError(f"duplicate original VMA: {address:#x}")
        offset = int(match.group(1), 16)
        if offset != address - VMA_BIAS:
            raise AssertionError(f"ROM/VMA offset mismatch at {address:#x}")
        rows[address] = (offset, int(match.group(3), 16), match.group(4).strip())
    return rows


def verify(assembly: str, rom: bytes) -> None:
    rows = parse_rows(assembly)
    expected_decoder = set(range(START, END, 4))
    if not expected_decoder.issubset(rows):
        raise AssertionError("decoder extent is not 528 bytes / 132 words")
    if hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise AssertionError("decompressed USA ROM SHA-1 differs from the pinned image")
    verify_paced_reader_rom(rom)
    function = rom[ROM_OFFSET:ROM_OFFSET + END - START]
    if hashlib.sha256(function).hexdigest() != FUNCTION_SHA256:
        raise AssertionError("decoder SHA-256 differs from the pinned original extent")

    for address, (offset, word, _) in rows.items():
        if rom[offset:offset + 4] != struct.pack(">I", word):
            raise AssertionError(f"listing word differs from ROM at {address:#x}")
    for address, pattern in ANCHORS.items():
        if address not in rows or re.fullmatch(pattern, rows[address][2]) is None:
            raise AssertionError(
                f"original instruction mismatch at {address:#x}: "
                f"{rows.get(address, (None, None, None))[2]!r}; expected {pattern}"
            )

    table_offset = 0x8007D068 - VMA_BIAS
    raw_table = rom[table_offset:table_offset + 4 * len(COMMAND_TABLE)]
    if len(raw_table) != 4 * len(COMMAND_TABLE):
        raise AssertionError("truncated signed-token dispatch table")
    targets = [word[0] for word in struct.iter_unpack(">I", raw_table)]
    if targets != COMMAND_TABLE:
        raise AssertionError("signed-token dispatch table differs from the pinned ROM")

    reader_caller_anchor_count = sum(1 for address in ANCHORS if not START <= address < END)
    print(
        f"VM control decoder: 132 original words, {len(ANCHORS)} total anchors "
        f"({reader_caller_anchor_count} reader/caller anchors), 40 token-table entries passed"
    )


PACED_WORDS = {
    0x8003DEB0: 0x86020000,
    0x8003DEB4: 0x04420017,
    0x8003DEB8: 0x2403FFFF,
    0x8003DEC4: 0x10400008,
    0x8003DEC8: 0x02202025,
    0x8003DEE8: 0x0C003418,
    0x8003DEEC: 0x86050000,
    0x8003DEF4: 0x860F0000,
    0x8003DEF8: 0x26100002,
    0x8003DEFC: 0x1060FFEC,
    0x8003DF00: 0xA66F0008,
    0x8003DF14: 0x14620004,
    0x8003DF18: 0x02202025,
    0x8003DF1C: 0xA6630008,
    0x8003DF20: 0x1000000A,
    0x8003DF24: 0x00001025,
    0x8003DF2C: 0x0C00F7E6,
    0x8003DF30: 0x02002825,
    0x8003DF38: 0x8F187798,
    0x8003DF40: 0x00408025,
    0x8003DF44: 0xAC3877A0,
    0x8003DF48: 0x02001025,
    0x8003DF60: 0x03E00008,
    0x8003DF64: 0x27BD0028,
}


def verify_paced_reader_rom(rom: bytes) -> None:
    if len(rom) != 33554432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise AssertionError("decompressed USA ROM length/SHA-1 differs from the pinned image")
    function = rom[PACED_ROM_OFFSET:PACED_ROM_OFFSET + PACED_SIZE]
    if len(function) != PACED_SIZE:
        raise AssertionError("paced-reader extent is truncated")
    if hashlib.sha256(function).hexdigest() != PACED_SHA256:
        raise AssertionError("paced-reader extent differs from the pinned 232-byte function")
    for address, expected in PACED_WORDS.items():
        offset = PACED_ROM_OFFSET + address - PACED_START
        actual = struct.unpack_from(">I", rom, offset)[0]
        if actual != expected:
            raise AssertionError(
                f"paced-reader instruction differs at {address:#x}: "
                f"{actual:08x}, expected {expected:08x}"
            )
    print(
        f"VM paced reader: {PACED_SIZE // 4} original words, "
        f"{len(PACED_WORDS)} exact control/callback anchors passed"
    )


def compare_word_streams(original: bytes, candidate: bytes, start_vma: int):
    if len(original) % 4 or len(candidate) % 4:
        raise ValueError("word-stream comparison requires four-byte-aligned inputs")
    compared_bytes = min(len(original), len(candidate))
    mismatches = []
    for offset in range(0, compared_bytes, 4):
        old = struct.unpack_from(">I", original, offset)[0]
        new = struct.unpack_from(">I", candidate, offset)[0]
        if old != new:
            mismatches.append((start_vma + offset, old, new))
    return compared_bytes // 4, mismatches


def compare_paced_reader_candidate(rom: bytes, candidate_text: bytes) -> None:
    original = rom[PACED_ROM_OFFSET:PACED_ROM_OFFSET + PACED_SIZE]
    compared_words, mismatches = compare_word_streams(
        original, candidate_text, PACED_START
    )
    first = "none"
    if mismatches:
        address, old, new = mismatches[0]
        first = f"0x{address:08X}: original={old:08X} candidate={new:08X}"
    print(
        f"VM paced reader linked comparison: candidate_text={len(candidate_text)} "
        f"/ original={len(original)} bytes; {len(mismatches)}/{compared_words} "
        f"available words differ; first mismatch {first}"
    )


class ParserTests(unittest.TestCase):
    def test_paced_reader_extent_is_exactly_232_bytes(self):
        self.assertEqual(PACED_END - PACED_START, 232)
        self.assertEqual(PACED_SIZE, 58 * 4)

    def test_paced_reader_anchors_cover_signed_split_and_callback_reread(self):
        self.assertIn(0x8003DEB4, PACED_WORDS)
        self.assertIn(0x8003DEB8, PACED_WORDS)
        self.assertIn(0x8003DEF4, PACED_WORDS)
        self.assertIn(0x8003DF2C, PACED_WORDS)
        self.assertIn(0x8003DF24, PACED_WORDS)

    def test_word_comparison_reports_original_vma_and_word_mismatches(self):
        compared, mismatches = compare_word_streams(
            bytes.fromhex("0000000100000002"),
            bytes.fromhex("0000000100000003"),
            0x8003DE80,
        )
        self.assertEqual(compared, 2)
        self.assertEqual(mismatches, [(0x8003DE84, 2, 3)])

    def test_word_comparison_rejects_unaligned_inputs(self):
        with self.assertRaisesRegex(ValueError, "four-byte-aligned"):
            compare_word_streams(b"\0\0\0", b"\0\0\0", 0x8003DE80)

    def test_duplicate_address_rejected(self):
        row = "/* 3EB98 8003DF98 27BDFFE0 */ addiu $sp, $sp, -0x20"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_rows(f"{row}\n{row}\n")

    def test_rom_vma_offset_rejected(self):
        with self.assertRaisesRegex(AssertionError, "ROM/VMA"):
            parse_rows("/* 3EB9C 8003DF98 27BDFFE0 */ addiu $sp, $sp, -0x20")

    def test_incomplete_decoder_rejected(self):
        with self.assertRaisesRegex(AssertionError, "528 bytes"):
            verify("", b"")

    def test_anchor_addresses_are_unique_and_inside_listing_ranges(self):
        self.assertEqual(len(ANCHORS), len(set(ANCHORS)))
        self.assertTrue(all(any(lo <= a < hi for lo, hi in LISTING_RANGES) for a in ANCHORS))

    def test_command_table_has_all_signed_halfword_tokens(self):
        self.assertEqual(len(COMMAND_TABLE), 40)
        self.assertEqual((-0x47) & 0xFFFF, 0xFFB9)
        self.assertEqual((-0x20) & 0xFFFF, 0xFFE0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_asm", type=Path, nargs="?")
    parser.add_argument("rom", type=Path, nargs="?")
    parser.add_argument("--paced-rom", type=Path,
                        help="verify the exact local USA paced-reader extent and CFG anchors")
    parser.add_argument("--paced-candidate-text", type=Path,
                        help="compare a linked paced-reader .text binary at the original VMA")
    args = parser.parse_args()
    if args.paced_candidate_text is not None and args.paced_rom is None:
        parser.error("--paced-candidate-text requires --paced-rom")
    if args.paced_rom is not None:
        if args.original_asm is not None or args.rom is not None:
            parser.error("--paced-rom cannot be combined with original_asm or rom")
        rom = args.paced_rom.read_bytes()
        verify_paced_reader_rom(rom)
        if args.paced_candidate_text is not None:
            compare_paced_reader_candidate(rom, args.paced_candidate_text.read_bytes())
        return
    if (args.original_asm is None) != (args.rom is None):
        parser.error("provide both original_asm and rom, or neither")
    if args.original_asm is not None:
        verify(args.original_asm.read_text(encoding="utf-8"), args.rom.read_bytes())
    else:
        unittest.main(argv=["test_vm_control_decoder_original"])


if __name__ == "__main__":
    main()
