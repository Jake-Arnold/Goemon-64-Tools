"""ROM-free checks of file-table indexing and CSV serialization."""

import csv
from io import StringIO
import struct
import unittest

from decomp import rom_file_inventory as inv


def synthetic_rom():
    # Minimal ROM fixture, containing no retail ROM data.
    data = bytearray(b"\x80\x37\x12\x40" + b"\0" * 128)
    sig_at = 16
    entry_at = sig_at + len(inv.SIGNATURE)
    start = 64
    words = [start | 0x80000000, start, start, start + 2, 0]
    data[sig_at:sig_at + len(inv.SIGNATURE)] = inv.SIGNATURE
    struct.pack_into(">5I", data, entry_at, *words)
    data[start:start + 2] = b"ok"
    return bytes(data)


class FileInventoryTests(unittest.TestCase):
    def test_byte_order_conversion(self):
        normal = b"\x80\x37\x12\x40\x11\x22\x33\x44"
        swapped = b"\x37\x80\x40\x12\x22\x11\x44\x33"
        reverse_words = b"\x40\x12\x37\x80\x44\x33\x22\x11"
        for raw in (normal, swapped, reverse_words):
            self.assertEqual(inv.normalize_rom(raw), normal)
        with self.assertRaises(ValueError):
            inv.normalize_rom(b"not a rom")

    def test_parse_monotone_and_terminator(self):
        data = bytearray(synthetic_rom())
        loc = data.find(inv.SIGNATURE) + len(inv.SIGNATURE)
        struct.pack_into(">5I", data, loc, 64, 64, 64, 66, 0)
        self.assertEqual(inv.parse_file_table(bytes(data), count=3),
                         [(64, False), (64, False), (64, False), (66, False)])
        struct.pack_into(">I", data, loc + 16, 5)
        with self.assertRaisesRegex(ValueError, "terminator"):
            inv.parse_file_table(bytes(data), count=3)

    def test_region_sizes_and_empty_slots(self):
        data = bytearray(synthetic_rom())
        loc = data.find(inv.SIGNATURE) + len(inv.SIGNATURE)
        struct.pack_into(">5I", data, loc, 64 | 0x80000000, 66, 66, 68, 0)
        rows = inv.region_entries(bytes(data), lambda _: b"ABCD", count=3)
        self.assertEqual([x["stored"] for x in rows], [2, 0, 2])
        self.assertEqual([x["expanded"] for x in rows], [4, 0, 2])
        self.assertEqual([x["compression"] for x in rows],
                         ["LZKN64", "Empty", "Uncompressed"])
        self.assertEqual([x["expanded_rom_offset"] for x in rows],
                         ["0x00000040", "0x00000044", "0x00000044"])

    def test_segment_classes(self):
        self.assertEqual(inv.classification(11, 6), "Executable: static overlay")
        self.assertEqual(inv.classification(23, 6), "Executable: static overlay")
        self.assertEqual(inv.classification(24, 6), "Executable: TLB overlay")
        self.assertEqual(inv.classification(80, 6), "Executable: TLB overlay")
        self.assertEqual(inv.classification(81, 6), "Opaque binary/data")
        self.assertEqual(inv.classification(43, 0), "Empty slot")

    def test_csv_header_and_diffs(self):
        row = {"stored": 12, "expanded": 20, "compression": "LZKN64",
               "rom_offset": "0x00000050", "expanded_rom_offset": "0x00000060"}
        jp = {**row, "stored": 13, "expanded": 24}
        with self.assertRaisesRegex(ValueError, "1,311"):
            inv.build_csv([row], [jp])
        rendered = inv.build_csv([row] * inv.COUNT, [jp] * inv.COUNT)
        records = list(csv.DictReader(StringIO(rendered)))
        self.assertEqual(len(records), inv.COUNT)
        self.assertEqual(records[0]["File"], "file_1")
        self.assertEqual(records[-1]["File"], "file_1311")
        self.assertEqual(records[0]["JP minus USA stored bytes"], "1")
        self.assertEqual(records[0]["JP minus USA expanded bytes"], "4")


if __name__ == "__main__":
    unittest.main()
