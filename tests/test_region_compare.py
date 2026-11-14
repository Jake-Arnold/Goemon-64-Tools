"""ROM comparison tests with synthetic bytes only; no copyrighted ROMs."""
import random
import unittest

from decomp.region_compare import (ROM_SHA1, identify_rom,
                                   matching_rom_spans, normalize_byte_order)


class TestRegionCompare(unittest.TestCase):
    def test_byte_orders(self):
        z64 = b"\x80\x37\x12\x40" + bytes(range(4, 132))
        n64 = b"".join(z64[i:i + 4][::-1] for i in range(0, len(z64), 4))
        v64 = b"".join(z64[i:i + 2][::-1] for i in range(0, len(z64), 2))
        self.assertEqual(normalize_byte_order(z64), z64)
        self.assertEqual(normalize_byte_order(n64), z64)
        self.assertEqual(normalize_byte_order(v64), z64)
        with self.assertRaises(ValueError):
            normalize_byte_order(b"\0\0\0\0")

    def test_unknown_sha_is_rejected(self):
        fake = bytearray(16 * 1024 * 1024)
        fake[:4] = b"\x80\x37\x12\x40"
        fake[0x3B:0x3F] = b"NG5J"
        with self.assertRaisesRegex(ValueError, "Unsupported ROM SHA-1"):
            identify_rom(bytes(fake))
        self.assertEqual(len(ROM_SHA1), 2)

    def test_exact_relocated_spans(self):
        rng = random.Random(123)
        source = rng.randbytes(4096)
        usa = b"\x00" * 256 + source + b"\xff" * 256
        jp = b"\xff" * 512 + source + b"\x00" * 256
        spans = matching_rom_spans(usa, jp, anchor_size=64, stride=16, min_span=64)
        self.assertTrue(any(s["usa_offset"] == 256 and s["japan_offset"] == 512
                            and s["length"] == 4096 for s in spans))
        for s in spans:
            a, b, n = s["usa_offset"], s["japan_offset"], s["length"]
            self.assertEqual(usa[a:a+n], jp[b:b+n])

    def test_changed_content_is_not_reported_equal(self):
        rng = random.Random(456)
        source = rng.randbytes(4096)
        jp = bytearray(source)
        jp[2048] ^= 0xFF
        spans = matching_rom_spans(source, bytes(jp), anchor_size=64, stride=16,
                                   min_span=64)
        self.assertGreaterEqual(len(spans), 2)
        self.assertFalse(any(s["usa_offset"] <= 2048 < s["usa_offset"] + s["length"]
                             for s in spans))

    def test_parameter_validation(self):
        with self.assertRaises(ValueError):
            matching_rom_spans(b"a", b"b", anchor_size=0)


if __name__ == "__main__":
    unittest.main()
