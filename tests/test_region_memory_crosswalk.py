"""ROM-free tests for explicitly source-qualified USA/JP memory crosswalk."""
import unittest

from practice.region_memory_crosswalk import (
    CROSS_REGION_FIELDS, CROSS_REGION_BY_KEY, CrossRegionField,
    read_cross_region_field, read_cross_region_fields,
    changed_cross_region_fields,
)
from practice.region_unlocks import REGION_DELTA
from practice.story_progress import CURATED_FLAGS, PLASMA_FLAGS
from practice.unlocks import UNLOCKS


class FakeJP:
    def __init__(self, values=None):
        self.values = values or {}
        self.reads = []

    def read_guest(self, addr, size):
        self.reads.append((addr, size))
        return self.values.get((addr, size), bytes(size))

    def write_guest(self, *_args):
        raise AssertionError("Crosswalk must never write guest RAM")


class CrosswalkTests(unittest.TestCase):
    def test_inventory_and_flag_catalogue_includes_all_named_fields(self):
        self.assertGreaterEqual(len(CROSS_REGION_FIELDS),
                                len(UNLOCKS) + len(CURATED_FLAGS)
                                + len(PLASMA_FLAGS))
        self.assertEqual(len(CROSS_REGION_FIELDS), len(CROSS_REGION_BY_KEY))
        self.assertTrue(all(
            f.japan == f.usa + REGION_DELTA or f.is_exception
            for f in CROSS_REGION_FIELDS))
        for item in UNLOCKS:
            self.assertIn("unlock:" + item.slug, CROSS_REGION_BY_KEY)
        for flag in CURATED_FLAGS:
            self.assertIn("event:" + flag.key, CROSS_REGION_BY_KEY)
        for flag in PLASMA_FLAGS:
            self.assertIn("plasma:" + flag.key, CROSS_REGION_BY_KEY)

    def test_four_new_user_confirmations_have_exact_addresses(self):
        expected = {
            "static:weapon_index": 0x80161DF7,
            "static:gameplay_submode": 0x800CD294,
            "static:map_overlay": 0x80161D64,
            "event:benkei_encounter": 0x80161DFC,
        }
        for key, address in expected.items():
            f = CROSS_REGION_BY_KEY[key]
            self.assertEqual(f.japan, address)
            self.assertEqual(f.evidence, "user-confirmed")
        self.assertEqual(CROSS_REGION_BY_KEY["event:benkei_encounter"].mask, 0x20)

    def test_disputed_pause_and_unverified_battery_not_promoted(self):
        self.assertEqual(CROSS_REGION_BY_KEY["static:pause_byte"].japan,
                         0x800CD2D6)
        self.assertEqual(CROSS_REGION_BY_KEY["static:pause_byte"].evidence,
                         "disputed")
        self.assertEqual(
            CROSS_REGION_BY_KEY["unlock:sasuke_battery_1_collected"].evidence,
            "candidate")

    def test_known_snowflake_layout_exception(self):
        f = CROSS_REGION_BY_KEY["unlock:snowflake"]
        self.assertTrue(f.is_exception)
        self.assertEqual(f.japan, 0x80162057)
        self.assertEqual(f.predicted_japan, 0x80162056)

    def test_dynamic_pointers_and_vm_are_not_automatically_translated(self):
        known_usa = {f.usa for f in CROSS_REGION_FIELDS}
        for addr in (0x801FC60C, 0x801FC604, 0x801C77E0,
                     0x80077858, 0x802F7060):
            self.assertNotIn(addr, known_usa)

    def test_read_only_big_endian_and_mask(self):
        f = CROSS_REGION_BY_KEY["event:benkei_encounter"]
        guest = FakeJP({(f.japan, 1): b"\x20"})
        r = read_cross_region_field(guest, f)
        self.assertEqual(r.raw, "20")
        self.assertIn("True", r.value)
        self.assertEqual(guest.reads, [(f.japan, 1)])

    def test_short_read_reports_error_without_promotion(self):
        f = CROSS_REGION_BY_KEY["static:weapon_index"]
        r = read_cross_region_field(FakeJP({(f.japan, 1): b""}), f)
        self.assertTrue(r.error)
        self.assertEqual(r.value, "—")

    def test_comparison_is_raw_only_and_detects_changes(self):
        f = CROSS_REGION_BY_KEY["static:weapon_index"]
        before = read_cross_region_fields(FakeJP({(f.japan, 1): b"\x01"}))
        after = read_cross_region_fields(FakeJP({(f.japan, 1): b"\x02"}))
        changes = changed_cross_region_fields(before, after)
        self.assertEqual([(field.key, a, b) for field, a, b in changes],
                         [("static:weapon_index", "01", "02")])

    def test_invalid_addresses_rejected(self):
        with self.assertRaises(ValueError):
            CrossRegionField("bad", "test", "test", 0x80800000, 0x808057F0)


if __name__ == "__main__":
    unittest.main()
