"""ROM-free structural tests for the original-VMA file_12 isolate proof."""
import unittest

from decomp.research.file12_spatial.verify_isolates import (
    ISOLATES, USA_SIZE, check_relocations, rom_offset, validate_image,
)


class File12IsolateTests(unittest.TestCase):
    def test_original_rom_offsets(self):
        self.assertEqual(rom_offset(0x80218E7C), 0x5D434C)
        self.assertEqual(rom_offset(0x80218F30), 0x5D4400)
        self.assertEqual(rom_offset(0x8021A644), 0x5D5B14)

    def test_three_nonoverlapping_original_functions(self):
        self.assertEqual(len(ISOLATES), 3)
        self.assertEqual(sum(v.size for v in ISOLATES), 420)
        self.assertEqual(sum(v.expected_reloc_count for v in ISOLATES), 25)
        ranges = sorted((f.vma, f.vma + f.size) for f in ISOLATES)
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:])))

    def test_wrong_rom_rejected(self):
        with self.assertRaisesRegex(ValueError, "original 32 MiB"):
            validate_image(b"")
        with self.assertRaisesRegex(ValueError, "original 32 MiB"):
            validate_image(bytes(USA_SIZE))

    def test_mismatched_relocations_rejected(self):
        with self.assertRaisesRegex(ValueError, "relocation count"):
            check_relocations("", ISOLATES[0])
        fake = "00000020 00000304 R_MIPS_26 00000000 wrong_symbol"
        with self.assertRaisesRegex(ValueError, "unexpected symbol"):
            check_relocations(fake, ISOLATES[0])


if __name__ == "__main__":
    unittest.main()
