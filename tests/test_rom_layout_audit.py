"""ROM-free synthetic MIPS reference scanner tests; never use actual ROM bytes."""
import struct
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from practice.rom_layout_audit import compare, direct_word_refs, load_verified


def instructions(*words):
    return b"".join(struct.pack(">I", word) for word in words)


class DirectReferenceTests(unittest.TestCase):
    def test_signed_low_immediate_and_japanese_positive_offset(self):
        usa = instructions(0x3C088016, 0x8D09C6D8, 0xAD09C6D8, 0)
        japan = instructions(0x3C088016, 0x8D091EC8, 0xAD091EC8, 0)
        result = compare(
            usa, japan, [("bazooka", 0x8015C6DB, 0x80161ECB, "array")])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["usa_accesses"], {"lw": 1, "sw": 1})
        self.assertEqual(result[0]["japan_accesses"], {"lw": 1, "sw": 1})
        self.assertTrue(result[0]["both_have_same_direct_access_pattern"])

    def test_missing_direct_reference_does_not_prove_correspondence(self):
        data = instructions(0x3C088016, 0x8D091EC8, 0)
        row = compare(
            data, data, [("candidate", 0x8015C6DB, 0x80161ECB, "guess")])
        self.assertFalse(row[0]["both_have_same_direct_access_pattern"])

    def test_nonword_aligned_image_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "word-aligned"):
            direct_word_refs(b"bad", {0x80161EC8})

    def test_unverified_rom_input_is_rejected(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.z64"
            path.write_bytes(b"none")
            with self.assertRaisesRegex(ValueError, "decompressed ROM"):
                load_verified(path, "usa")


if __name__ == "__main__":
    unittest.main()
