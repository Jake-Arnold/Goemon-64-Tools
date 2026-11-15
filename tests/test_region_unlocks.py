"""Region-identified unlock mappings; absent addresses remain unknown."""
import unittest

from practice.unlocks import UNLOCKS, GROUPS
from practice.region_unlocks import (
    JAPAN_UNLOCK_LEADS, japan_unlock_lead, japan_unlock_all_targets,
    write_japan_unlock,
)


class RegionUnlockMappingTests(unittest.TestCase):
    def test_original_usa_rows_and_groups_are_unchanged(self):
        self.assertEqual(len(UNLOCKS), 34)
        self.assertEqual(GROUPS, (
            'Party', 'Weapon upgrades', 'Weapons', 'Abilities',
            'Items and keys', 'Fish counts', 'Miracle items'))
        self.assertEqual(
            (UNLOCKS[2].label, UNLOCKS[2].address),
            ('Sasuke in party', 0x8015C6A7))
        self.assertEqual(
            (UNLOCKS[3].label, UNLOCKS[3].address),
            ('Yae in party', 0x8015C6AB))

    def test_only_explicit_source_identified_japanese_addresses(self):
        by_label = {row.label: japan_unlock_lead(row) for row in UNLOCKS}
        self.assertEqual(by_label['Sasuke in party'].address, 0x80161E97)
        self.assertEqual(by_label['Yae in party'].address, 0x80161E9B)
        self.assertEqual(by_label['Triton Shell'].address, 0x80161EEF)
        self.assertEqual(by_label['Cucumber'].address, 0x80161F07)
        self.assertEqual(by_label['Red fish count'].address, 0x80161F0B)
        self.assertEqual(by_label['Yellow fish count'].address, 0x80161F0F)
        self.assertEqual(by_label['Blue fish count'].address, 0x80161F13)
        self.assertIsNone(by_label['Goemon in party'])
        self.assertIsNone(by_label['Goemon pipe upgrade'])
        self.assertIsNone(by_label['Gold Key'])
        self.assertIsNone(by_label['Star'])
        self.assertEqual(sum(x is not None for x in by_label.values()), 7)
        self.assertTrue(all(lead.address not in {r.address for r in UNLOCKS}
                            for lead in JAPAN_UNLOCK_LEADS.values()))

    def test_every_named_japanese_field_is_a_direct_write_target(self):
        self.assertEqual(len(japan_unlock_all_targets()), 7)
        targets = {row.slug: value for row, value in japan_unlock_all_targets()}
        self.assertEqual(targets['sasuke_in_party'], 1)
        self.assertEqual(targets['yae_in_party'], 1)
        self.assertEqual(targets['triton_shell'], 1)
        self.assertEqual(targets['cucumber'], 1)
        self.assertEqual(targets['red_fish_count'], 8)
        self.assertEqual(targets['yellow_fish_count'], 5)
        self.assertEqual(targets['blue_fish_count'], 3)

    def test_direct_writes_preserve_adjacent_bytes_in_both_host_endians(self):
        from tests.test_japanese_party_unlock import Process
        for endian in ('big', 'wordswapped'):
            with self.subTest(endian=endian):
                p = Process(endian)
                ram = p.rdram()
                sasuke = next(x for x in UNLOCKS
                              if x.label == 'Sasuke in party')
                triton = next(x for x in UNLOCKS
                              if x.label == 'Triton Shell')
                p.set_guest(0x80161E94, bytes.fromhex('ABCDEF00'))
                p.set_guest(0x80161EEC, bytes.fromhex('12345600'))
                self.assertTrue(write_japan_unlock(ram, sasuke, 1))
                self.assertTrue(write_japan_unlock(ram, triton, 1))
                self.assertEqual(ram.read_guest(0x80161E94, 4),
                                 bytes.fromhex('ABCDEF01'))
                self.assertEqual(ram.read_guest(0x80161EEC, 4),
                                 bytes.fromhex('12345601'))
                self.assertTrue(write_japan_unlock(ram, sasuke, 0))
                self.assertEqual(ram.read_guest(0x80161E94, 4),
                                 bytes.fromhex('ABCDEF00'))

    def test_direct_on_off_with_no_party_guard_and_no_usa_fallback(self):
        class RAM:
            def __init__(self):
                self.values = {}
                self.writes = []
            def read_guest(self, address, size):
                return bytes((self.values.get(address, 0),))
            def write_guest(self, address, data):
                self.writes.append((address, data))
                self.values[address] = data[0]
        ram = RAM()
        sasuke = next(x for x in UNLOCKS if x.label == 'Sasuke in party')
        triton = next(x for x in UNLOCKS if x.label == 'Triton Shell')
        unknown = next(x for x in UNLOCKS if x.label == 'Goemon in party')
        self.assertTrue(write_japan_unlock(ram, sasuke, 1))
        self.assertFalse(write_japan_unlock(ram, sasuke, 1))
        self.assertTrue(write_japan_unlock(ram, sasuke, 0))
        self.assertTrue(write_japan_unlock(ram, triton, 1))
        self.assertTrue(write_japan_unlock(ram, triton, 0))
        with self.assertRaisesRegex(ValueError, 'unknown'):
            write_japan_unlock(ram, unknown, 1)
        self.assertEqual(ram.writes, [
            (0x80161E97, bytes((1,))),
            (0x80161E97, bytes((0,))),
            (0x80161EEF, bytes((1,))),
            (0x80161EEF, bytes((0,))),
        ])

if __name__ == '__main__':
    unittest.main()
