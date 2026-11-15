"""Region-identified unlock mappings; absent addresses remain unknown."""
import unittest

from practice.unlocks import UNLOCKS, GROUPS
from practice.region_unlocks import (
    JAPAN_UNLOCK_LEADS, JAPAN_WRITABLE_PARTY, japan_unlock_lead,
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

    def test_only_existing_verified_party_on_writes_are_exposed(self):
        self.assertEqual(JAPAN_WRITABLE_PARTY, {
            'sasuke_in_party': 2, 'yae_in_party': 3})
        self.assertTrue(set(JAPAN_WRITABLE_PARTY) <= set(JAPAN_UNLOCK_LEADS))
        self.assertNotIn('goemon_in_party', JAPAN_WRITABLE_PARTY)
        self.assertNotIn('triton_shell', JAPAN_WRITABLE_PARTY)


if __name__ == '__main__':
    unittest.main()
