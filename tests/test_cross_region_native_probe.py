"""ROM-free regression tests for the cross-region isolated native proof."""
import hashlib
import unittest
from decomp.research.cross_region_native_probe import REGIONS, compare_native


class NativeProbeTest(unittest.TestCase):
    def test_both_regions_specify_four_distinct_functions(self):
        for region in ("usa", "japan"):
            entries = REGIONS[region]["calls"]
            self.assertEqual(set(entries), {"character_reader", "character_wrapper", "character_sync", "character_alternate"})
            self.assertEqual([entries[key][4] for key in entries], [12, 40, 148, 132])
            self.assertEqual(len({entries[key][1] for key in entries}), 4)
            self.assertEqual(len({entries[key][3] for key in entries}), 4)

    def test_exact_comparison(self):
        reference = b"\x00\x00\x00\x01\x10\x20\x30\x40\x00\x00\x00\x00"
        r = compare_native(reference, reference[4:], 4, 8)
        self.assertTrue(r["exact"])
        self.assertEqual((r["equal_instruction_words"], r["instruction_words"]), (2, 2))
        self.assertEqual(r["candidate_sha256"], hashlib.sha256(reference[4:]).hexdigest())

    def test_mismatch_is_not_exact(self):
        r = compare_native(bytes(12), b"\x00\x00\x00\x02" + bytes(8), 0, 12)
        self.assertFalse(r["exact"])
        self.assertEqual(r["equal_instruction_words"], 2)

    def test_rejects_bad_offsets_and_short_code(self):
        for offset, length in [(-1, 4), (0, 0), (4, 12)]:
            with self.subTest(offset=offset, length=length):
                with self.assertRaises(ValueError):
                    compare_native(bytes(12), bytes(12), offset, length)
        with self.assertRaises(ValueError):
            compare_native(bytes(16), bytes(4), 0, 12)


if __name__ == "__main__":
    unittest.main()