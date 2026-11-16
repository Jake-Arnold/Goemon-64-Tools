"""ROM-free tests for the fail-closed Japanese input preparation command."""
from __future__ import annotations

import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from decomp import prepare_japan_rom as subject


def fake_japan() -> bytes:
    raw = bytearray(subject.ROM_SIZE)
    raw[:4] = subject.MAGIC_Z64
    raw[0x3B:0x3F] = subject.JAPAN_GAME_CODE
    struct.pack_into(">II", raw, 0x10, *subject.JAPAN_CRC)
    return bytes(raw)


class JapaneseRomPreparationTests(unittest.TestCase):
    def test_normalizes_three_byte_orders(self):
        original = fake_japan()
        swapped16 = bytearray(len(original))
        swapped16[::2] = original[1::2]
        swapped16[1::2] = original[::2]
        swapped32 = bytearray(len(original))
        for i in range(4):
            swapped32[i::4] = original[3 - i::4]
        for input_rom, order in ((original, "z64"), (bytes(swapped16), "v64-16bit-swapped"),
                                 (bytes(swapped32), "n64-32bit-swapped")):
            with self.subTest(order=order):
                normalized, found = subject.normalize_rom(input_rom)
                self.assertEqual(normalized, original)
                self.assertEqual(found, order)

    def test_rejects_wrong_size_and_unknown_header(self):
        with self.assertRaisesRegex(ValueError, "Expected"):
            subject.normalize_rom(b"bad")
        with self.assertRaisesRegex(ValueError, "Unrecognized"):
            subject.normalize_rom(b"abcd" + bytes(subject.ROM_SIZE - 4))

    def test_rejects_wrong_region_hash_and_crc(self):
        original = fake_japan()
        with self.assertRaisesRegex(ValueError, "Wrong or modified"):
            subject.verify_japan_rom(original)
        bad_crc = bytearray(original)
        bad_crc[0x10] ^= 1
        with self.assertRaisesRegex(ValueError, "cartridge CRCs"):
            subject.verify_japan_rom(bytes(bad_crc))
        bad_region = bytearray(original)
        bad_region[0x3E] = ord("E")
        with self.assertRaisesRegex(ValueError, "Not Japanese"):
            subject.verify_japan_rom(bytes(bad_region))

    def test_prepares_new_file_and_refuses_overwrite(self):
        original = fake_japan()
        digest = hashlib.sha1(original).hexdigest()
        with tempfile.TemporaryDirectory() as d, mock.patch.object(subject, "JAPAN_SHA1", digest):
            source = Path(d, "original.n64")
            output = Path(d, "config", "japan_0", "baserom.z64")
            swapped = bytearray(len(original))
            swapped[::2], swapped[1::2] = original[1::2], original[::2]
            source.write_bytes(swapped)
            report = subject.prepare(source, output)
            self.assertEqual(report["sha1"], digest)
            self.assertEqual(output.read_bytes(), original)
            self.assertEqual(source.read_bytes(), swapped)
            with self.assertRaises(FileExistsError):
                subject.prepare(source, output)
            with self.assertRaisesRegex(ValueError, "overwrite"):
                subject.prepare(output, output)
            with self.assertRaisesRegex(ValueError, "end in .z64"):
                subject.prepare(source, Path(d, "bad.n64"))


if __name__ == "__main__":
    unittest.main()
