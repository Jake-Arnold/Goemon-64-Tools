"""USA unlocks stay unchanged; Japan candidate mappings remain explicitly typed."""
import unittest

from practice.unlocks import UNLOCKS, GROUPS
from practice.region_unlocks import (
    REGION_DELTA, JAPAN_UNLOCK_LEADS, japan_unlock_lead,
    japan_unlock_all_targets, japan_unlock_wire_value,
    japan_unlock_display_value, write_japan_unlock,
)

ROWS = {field.slug: field for field in UNLOCKS}


class RegionUnlockMappingTests(unittest.TestCase):
    def test_original_usa_rows_and_groups_are_unchanged(self):
        self.assertEqual(len(UNLOCKS), 34)
        self.assertEqual(GROUPS, (
            'Party', 'Weapon upgrades', 'Weapons', 'Abilities',
            'Items and keys', 'Fish counts', 'Miracle items'))
        self.assertEqual(ROWS['sasuke_in_party'].address, 0x8015C6A7)
        self.assertEqual(ROWS['yae_in_party'].address, 0x8015C6AB)
        self.assertEqual(ROWS['chain_pipe'].values, (0, 2))

    def test_all_34_japanese_candidates_have_unique_addresses_and_evidence(self):
        self.assertEqual(len(JAPAN_UNLOCK_LEADS), 34)
        self.assertEqual(
            {lead.confidence for lead in JAPAN_UNLOCK_LEADS.values()},
            {'named', 'array', 'offset', 'guess'})
        self.assertEqual(
            {kind: sum(lead.confidence == kind for lead in JAPAN_UNLOCK_LEADS.values())
             for kind in ('named', 'array', 'offset', 'guess')},
            {'named': 9, 'array': 16, 'offset': 4, 'guess': 5})
        self.assertEqual(
            len({lead.address for lead in JAPAN_UNLOCK_LEADS.values()}), 34)
        for slug, lead in JAPAN_UNLOCK_LEADS.items():
            self.assertTrue(0x80000000 <= lead.address < 0x80800000)
            self.assertEqual(lead.width, 1)
            self.assertTrue(lead.evidence)
            self.assertIs(japan_unlock_lead(ROWS[slug]), lead)

    def test_source_named_japanese_fields_unchanged(self):
        expected = {
            'sasuke_in_party': 0x80161E97,
            'yae_in_party': 0x80161E9B,
            'triton_shell': 0x80161EEF,
            'lord_s_pass': 0x80161EF3,
            'achilles_heel': 0x80161EFF,
            'cucumber': 0x80161F07,
            'red_fish_count': 0x80161F0B,
            'yellow_fish_count': 0x80161F0F,
            'blue_fish_count': 0x80161F13,
        }
        for slug, address in expected.items():
            with self.subTest(slug=slug):
                self.assertEqual(JAPAN_UNLOCK_LEADS[slug].address, address)
                self.assertEqual(JAPAN_UNLOCK_LEADS[slug].confidence, 'named')

    def test_source_array_ranges_and_bazooka_slot_order(self):
        arrays = (
            ('goemon_pipe_upgrade', 'ebisumaru_hammer_upgrade',
             'sasuke_kunai_upgrade', 'yae_katana_upgrade'),
            ('chain_pipe', 'meat_saw_hammer',
             'fire_cracker_bomb', 'flute'),
            ('windup_camera', 'ice_kunai', 'bazooka', 'medal_of_flames'),
            ('sudden_impact', 'mini_ebisumaru',
             'super_jump', 'magic_mermaid'),
        )
        for start, group in zip(
            (0x80161E9F, 0x80161EAF, 0x80161EC3, 0x80161EDF),
            arrays,
        ):
            with self.subTest(start=hex(start)):
                for index, slug in enumerate(group):
                    lead = JAPAN_UNLOCK_LEADS[slug]
                    self.assertEqual(lead.address, start + index * 4)
                    self.assertEqual(lead.confidence, 'array')
                    self.assertEqual(lead.address, ROWS[slug].address + REGION_DELTA)
        self.assertEqual(JAPAN_UNLOCK_LEADS['bazooka'].address, 0x80161ECB)
        self.assertEqual(JAPAN_UNLOCK_LEADS['medal_of_flames'].address,
                         0x80161ECF)

    def test_four_scalar_offsets_and_five_speculative_guesses(self):
        for slug in ('goemon_in_party', 'ebisumaru_in_party',
                     'gold_key', 'silver_fortune_doll_progress'):
            lead = JAPAN_UNLOCK_LEADS[slug]
            self.assertEqual(lead.confidence, 'offset')
            self.assertEqual(lead.address, ROWS[slug].address + REGION_DELTA)
        guesses = {
            'sasuke_battery_1_collected': 0x80161DF9,
            'star': 0x8016204B,
            'moon': 0x8016204F,
            'flower': 0x80162053,
            'snowflake': 0x80162057,
        }
        for slug, address in guesses.items():
            self.assertEqual(JAPAN_UNLOCK_LEADS[slug].address, address)
            self.assertEqual(JAPAN_UNLOCK_LEADS[slug].confidence, 'guess')

    def test_bulk_skips_five_guesses_but_allows_manual_edit(self):
        targets = japan_unlock_all_targets()
        self.assertEqual(len(targets), 29)
        self.assertEqual(len(japan_unlock_all_targets(include_speculative=True)), 34)
        values = {field.slug: value for field, value in targets}
        for slug in ('star', 'moon', 'flower', 'snowflake',
                     'sasuke_battery_1_collected'):
            self.assertNotIn(slug, values)
        self.assertEqual(values['red_fish_count'], 8)
        self.assertEqual(values['yellow_fish_count'], 5)
        self.assertEqual(values['blue_fish_count'], 3)
        self.assertEqual(values['chain_pipe'], 2)

    def test_chain_pipe_wire_encoding_is_japan_01_usa_02(self):
        field = ROWS['chain_pipe']
        self.assertEqual(field.values, (0, 2))
        self.assertEqual(japan_unlock_wire_value(field, 2), 1)
        self.assertEqual(japan_unlock_wire_value(field, 0), 0)
        self.assertEqual(japan_unlock_display_value(field, 1), 2)
        self.assertEqual(japan_unlock_display_value(field, 0), 0)
        self.assertEqual(japan_unlock_display_value(field, 2), 2)

        class Ram:
            def __init__(self):
                self.raw = 0
            def read_guest(self, address, width):
                self.assert_address(address, width)
                return bytes((self.raw,))
            def write_guest(self, address, data):
                self.assert_address(address, len(data))
                self.raw = data[0]
            @staticmethod
            def assert_address(address, width):
                assert (address, width) == (0x80161EAF, 1)
        ram = Ram()
        self.assertTrue(write_japan_unlock(ram, field, 2))
        self.assertEqual(ram.raw, 1)
        self.assertFalse(write_japan_unlock(ram, field, 2))
        self.assertTrue(write_japan_unlock(ram, field, 0))

    def test_bitmask_guess_preserves_adjacent_flags(self):
        class Ram:
            def __init__(self):
                self.raw = 0x85
            def read_guest(self, address, width):
                assert (address, width) == (0x80161DF9, 1)
                return bytes((self.raw,))
            def write_guest(self, address, data):
                assert address == 0x80161DF9
                self.raw = data[0]
        ram = Ram()
        field = ROWS['sasuke_battery_1_collected']
        self.assertTrue(write_japan_unlock(ram, field, 1))
        self.assertEqual(ram.raw, 0xA5)
        self.assertEqual(japan_unlock_display_value(field, ram.raw), 1)
        self.assertTrue(write_japan_unlock(ram, field, 0))
        self.assertEqual(ram.raw, 0x85)

    def test_legacy_named_bytes_preserve_neighbours_both_endians(self):
        from tests.test_japanese_party_unlock import Process
        for endian in ('big', 'wordswapped'):
            with self.subTest(endian=endian):
                p = Process(endian)
                ram = p.rdram()
                p.set_guest(0x80161E94, bytes.fromhex('ABCDEF00'))
                p.set_guest(0x80161EEC, bytes.fromhex('12345600'))
                self.assertTrue(write_japan_unlock(ram, ROWS['sasuke_in_party'], 1))
                self.assertTrue(write_japan_unlock(ram, ROWS['triton_shell'], 1))
                self.assertEqual(ram.read_guest(0x80161E94, 4),
                                 bytes.fromhex('ABCDEF01'))
                self.assertEqual(ram.read_guest(0x80161EEC, 4),
                                 bytes.fromhex('12345601'))
                self.assertTrue(write_japan_unlock(ram, ROWS['sasuke_in_party'], 0))

    def test_unknown_future_row_has_no_fallback(self):
        from practice.unlocks import Unlock
        unknown = Unlock('Unmapped experimental field', 0x80101234, 'Items')
        self.assertIsNone(japan_unlock_lead(unknown))
        class Ram:
            def read_guest(self, address, length):
                raise AssertionError('Unknown row must not read memory')
        with self.assertRaisesRegex(ValueError, 'unknown'):
            write_japan_unlock(Ram(), unknown, 1)


if __name__ == '__main__':
    unittest.main()
