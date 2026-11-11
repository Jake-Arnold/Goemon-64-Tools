"""ROM-bound CFG and memory-access anchors for USA VM handler 0x8003ED60.

This guards the pinned original instruction extent and the one direct caller.
It records observed loads/stores without assigning names to opaque object fields
or command-buffer state. It is not a C translation or matching-C proof.
"""
import argparse
import hashlib
import struct
import unittest
from pathlib import Path

START = 0x8003ED60
END = 0x8003EFB0
ROM_OFFSET = 0x3F960
SIZE = END - START
CALLER_START = 0x8003EFB0
CALLER_END = 0x8003F038
CALLER_ROM_OFFSET = 0x3FBB0
VMA_BIAS = 0x7FFFF400
ROM_SIZE = 33_554_432
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
FUNCTION_SHA256 = "18db53295f30fa73a9808f3bed402aa085e97de238dfa36d25455f19dac8d89b"
CALLER_SHA256 = "2a21c3f52af4661feadecea27ee0a84f09d5d3533527f8abadae972ee9499d8a"
HELPER_JAL = 0x0C00FC0E
TARGET_JAL = 0x0C00FB58

ANCHORS = {
    # Entry, helper ABI, first result gate, and likely null exits.
    0x8003ED60: 0x27BDFFD0,  # addiu sp, sp, -0x30
    0x8003ED64: 0xAFBF0014,  # save caller ra at sp+0x14
    0x8003ED6C: 0x8C84785C,  # lw a0, D_8007785C
    0x8003ED70: HELPER_JAL,
    0x8003ED74: 0x00002825,  # move a1, zero in call delay slot
    0x8003ED78: 0x10400089,  # beqz v0, 0x8003EFA0
    0x8003ED7C: 0x3C028016,  # ordinary delay slot executes on either path
    0x8003ED80: 0x8C427C48,  # load pointer from D_80167C48
    0x8003ED84: 0x50400087,  # beqzl v0, 0x8003EFA4
    0x8003ED88: 0x8FBF0014,  # annulled unless the likely branch is taken
    0x8003ED8C: 0x8C4E0000,  # read 32-bit field at pointer+0
    0x8003ED90: 0x51C00084,  # beqzl t6, 0x8003EFA4
    0x8003ED94: 0x8FBF0014,
    0x8003ED98: 0x844F0030,  # signed halfword at pointer+0x30
    0x8003EDA4: 0x15E1007E,  # bne field, 4, 0x8003EFA0
    0x8003EDA8: 0x24C6C5CC,  # a2 = 0x8016C5CC (32-bit cursor slot)
    # Cursor movement and first raw two-word output pair.
    0x8003EDAC: 0x8CC30000,
    0x8003EDB8: 0x24780008,
    0x8003EDBC: 0xACD80000,
    0x8003EDC4: 0xAC790000,
    0x8003EDC8: 0xAC6E0004,
    # Second helper uses the same two arguments; stack+0x18 preserves its slot.
    0x8003EE08: HELPER_JAL,
    0x8003EE0C: 0xAFA30018,
    0x8003EE10: 0x8FBF0018,
    0x8003EE1C: 0xAFE20004,
    # Rectangle inputs are loaded as 32-bit words and masked to 12-bit fields.
    0x8003EED8: 0x8D6B7758,
    0x8003EEE8: 0x8D8C775C,
    0x8003EEFC: 0x332E0FFF,
    0x8003EF18: 0x31CF0FFF,
    # Final bit-dependent pair and epilogue.
    0x8003EF58: 0x8DCE785C,
    0x8003EF64: 0x31D80001,
    0x8003EF68: 0x13000003,
    0x8003EF74: 0x24050400,
    0x8003EFA0: 0x8FBF0014,
    0x8003EFA4: 0x27BD0030,
    0x8003EFA8: 0x03E00008,
    0x8003EFAC: 0x00000000,
}

CALLER_ANCHORS = {
    0x8003F010: 0x8DEF785C,  # read the same 32-bit global
    0x8003F014: 0x24010100,  # comparison constant 0x100
    0x8003F018: 0x51E10004,  # beql value, 0x100, epilogue
    0x8003F01C: 0x8FBF0014,  # likely delay restores RA when skipping call
    0x8003F020: TARGET_JAL,
    0x8003F024: 0x00000000,
    0x8003F02C: 0x27BD0018,
    0x8003F030: 0x03E00008,
    0x8003F034: 0x00000000,
}

CURSOR_ADVANCES = {
    0x8003EDB8: 0x24780008,
    0x8003EDD8: 0x246F0008,
    0x8003EDF4: 0x24790008,
    0x8003EE2C: 0x246F0008,
    0x8003EE4C: 0x246E0008,
    0x8003EE68: 0x24780008,
    0x8003EE84: 0x246F0008,
    0x8003EEA0: 0x24790008,
    0x8003EEC0: 0x24780008,
    0x8003EEF4: 0x246F0008,
    0x8003EF4C: 0x24990008,
    0x8003EF90: 0x24780008,
}


def read_word(rom: bytes, vma: int) -> int:
    offset = vma - VMA_BIAS
    return struct.unpack_from(">I", rom, offset)[0]


def branch_target(vma: int, instruction: int) -> int:
    immediate = instruction & 0xFFFF
    if immediate & 0x8000:
        immediate -= 0x10000
    return vma + 4 + immediate * 4


def verify(rom: bytes) -> None:
    if len(rom) != ROM_SIZE:
        raise AssertionError(f"USA ROM size is {len(rom)} bytes, expected {ROM_SIZE}")
    if hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise AssertionError("decompressed USA ROM SHA-1 differs from the pinned image")

    function = rom[ROM_OFFSET:ROM_OFFSET + SIZE]
    if len(function) != 592 or hashlib.sha256(function).hexdigest() != FUNCTION_SHA256:
        raise AssertionError("ED60 extent is not the pinned 592-byte original function")
    caller_size = CALLER_END - CALLER_START
    caller = rom[CALLER_ROM_OFFSET:CALLER_ROM_OFFSET + caller_size]
    if len(caller) != caller_size or hashlib.sha256(caller).hexdigest() != CALLER_SHA256:
        raise AssertionError("ED60 caller extent differs from the pinned original")

    for address, expected in {**ANCHORS, **CALLER_ANCHORS}.items():
        actual = read_word(rom, address)
        if actual != expected:
            raise AssertionError(
                f"original word mismatch at {address:#010x}: "
                f"{actual:08x} != {expected:08x}"
            )
    for address, expected in CURSOR_ADVANCES.items():
        if read_word(rom, address) != expected:
            raise AssertionError(f"8-byte cursor advance differs at {address:#010x}")

    branch_targets = {
        0x8003ED78: 0x8003EFA0,
        0x8003ED84: 0x8003EFA4,
        0x8003ED90: 0x8003EFA4,
        0x8003EDA4: 0x8003EFA0,
        0x8003F018: 0x8003F02C,
    }
    for address, expected_target in branch_targets.items():
        if branch_target(address, read_word(rom, address)) != expected_target:
            raise AssertionError(f"branch target differs at {address:#010x}")

    # The raw JAL encoding occurs once at an aligned word in the decompressed image.
    jal_bytes = struct.pack(">I", TARGET_JAL)
    hits = []
    offset = -1
    while True:
        offset = rom.find(jal_bytes, offset + 1)
        if offset < 0:
            break
        if offset % 4 == 0:
            hits.append(offset)
    if hits != [0x3FC20]:
        raise AssertionError(f"direct caller scan differs from pinned offset: {hits!r}")

    print(
        f"ED60: {SIZE} original bytes, {len(ANCHORS)} handler anchors, "
        f"{len(CURSOR_ADVANCES)} 8-byte cursor updates, two helper calls; "
        "one direct caller at 0x8003F020 passed"
    )


class OriginalEd60Tests(unittest.TestCase):
    def test_function_extent_and_vma_rom_mapping(self):
        self.assertEqual(SIZE, 592)
        self.assertEqual(ROM_OFFSET, START - VMA_BIAS)
        self.assertEqual(CALLER_ROM_OFFSET, CALLER_START - VMA_BIAS)
        self.assertEqual(END, CALLER_START)

    def test_handler_anchor_addresses_are_unique_and_in_extent(self):
        self.assertEqual(len(ANCHORS), len(set(ANCHORS)))
        self.assertTrue(all(START <= address < END for address in ANCHORS))
        self.assertEqual(len(CURSOR_ADVANCES), 12)

    def test_caller_anchor_addresses_are_unique_and_in_extent(self):
        self.assertEqual(len(CALLER_ANCHORS), len(set(CALLER_ANCHORS)))
        self.assertTrue(all(CALLER_START <= address < CALLER_END
                            for address in CALLER_ANCHORS))

    def test_branch_likely_and_exit_destinations(self):
        self.assertEqual(branch_target(0x8003ED78, 0x10400089), 0x8003EFA0)
        self.assertEqual(branch_target(0x8003ED84, 0x50400087), 0x8003EFA4)
        self.assertEqual(branch_target(0x8003ED90, 0x51C00084), 0x8003EFA4)
        self.assertEqual(branch_target(0x8003EDA4, 0x15E1007E), 0x8003EFA0)
        self.assertEqual(branch_target(0x8003F018, 0x51E10004), 0x8003F02C)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path,
                        help="verify against the private decompressed USA ROM")
    args = parser.parse_args()
    if args.rom is not None:
        verify(args.rom.read_bytes())
    else:
        unittest.main(argv=["test_vm_ed60_original"])


if __name__ == "__main__":
    main()
