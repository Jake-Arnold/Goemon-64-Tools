"""No-emulator, no-ROM tests for Japanese read-only values."""
import unittest
from practice.japanese_fields import (
    JAPAN_FIELDS, FIELD_GROUPS, JapanField, read_japan_field, read_japan_fields,
    JP_CHEATS, JP_DEBUG,
)


class FakeRam:
    def __init__(self, fields=None, error=None):
        self.values = fields or {}
        self.error = error
        self.reads = []

    def read_guest(self, address, length):
        self.reads.append((address, length))
        if self.error:
            raise self.error
        return self.values.get((address, length), bytes(length))


class JapaneseReadOnlyFieldsTest(unittest.TestCase):
    def test_unique_fields_with_known_sourced_addresses(self):
        self.assertEqual(len(JAPAN_FIELDS), 58)
        self.assertEqual(len(set(x.key for x in JAPAN_FIELDS)), 58)
        self.assertEqual(len(set((x.address, x.width) for x in JAPAN_FIELDS)), 58)
        self.assertTrue(set(x.source for x in JAPAN_FIELDS) <= {JP_CHEATS, JP_DEBUG})
        self.assertIn("World map", FIELD_GROUPS)

    def test_direct_health_ryo_lives_addresses_and_widths(self):
        by = {x.key: x for x in JAPAN_FIELDS}
        self.assertEqual((by["max_hp"].address, by["max_hp"].width), (0x80161DD3, 1))
        self.assertEqual((by["hp"].address, by["hp"].width), (0x80161DD7, 1))
        self.assertEqual((by["ryo"].address, by["ryo"].width), (0x80161DDA, 2))
        self.assertEqual((by["lives"].address, by["lives"].width), (0x80161DDF, 1))
        self.assertEqual(by["native_debug_state"].address, 0x800CD284)

    def test_repeated_game_shark_code_targets(self):
        by = {x.key: x.address for x in JAPAN_FIELDS}
        for prefix, base, count in (("weapon", 0x80161E9F, 4),
                                    ("jutsu", 0x80161EDF, 4),
                                    ("map_stop", 0x8016209F, 16),
                                    ("treasure", 0x8016204B, 4)):
            self.assertEqual([by[f"{prefix}_{n}"] for n in range(1, count+1)],
                             [base + i*4 for i in range(count)])

    def test_16_bit_ryo_decodes_big_endian_guest_bytes(self):
        ram = FakeRam({(0x80161DDA, 2): bytes.fromhex("270F")})
        field = next(x for x in JAPAN_FIELDS if x.key == "ryo")
        self.assertEqual(read_japan_field(ram, field).value, "9999")
        self.assertEqual(read_japan_field(ram, field).raw, "270F")

    def test_byte_flag_and_unusual_data_not_hidden(self):
        flag = next(x for x in JAPAN_FIELDS if x.key == "sasuke_party")
        self.assertEqual(read_japan_field(FakeRam({(flag.address, 1): b"\x01"}), flag).value, "Yes (1)")
        unusual = read_japan_field(FakeRam({(flag.address, 1): b"\x04"}), flag)
        self.assertEqual(unusual.value, "4")
        self.assertEqual(unusual.status, "CHECK: unusual value")

    def test_raw_time_is_not_guessed_as_seconds(self):
        field = next(x for x in JAPAN_FIELDS if x.key == "total_time_raw")
        observed = read_japan_field(FakeRam({(field.address, 4): bytes.fromhex("1234ABCD")}), field)
        self.assertEqual(observed.value, "0x1234ABCD")

    def test_all_fields_read_only(self):
        ram = FakeRam()
        values = read_japan_fields(ram)
        self.assertEqual(len(values), 58)
        self.assertEqual(len(ram.reads), 58)
        self.assertFalse(hasattr(ram, "write_guest"))

    def test_read_errors_are_isolated(self):
        field = JAPAN_FIELDS[0]
        result = read_japan_field(FakeRam(error=PermissionError("denied")), field)
        self.assertEqual(result.value, "—")
        self.assertIn("denied", result.status)

    def test_reject_out_of_bounds_field_schema(self):
        self.assertRaises(ValueError, __import__("practice.japanese_fields", fromlist=["_field"])._field,
                          "bad", "bad", 0x80800000, 1, "Group")


if __name__ == "__main__":
    unittest.main()
