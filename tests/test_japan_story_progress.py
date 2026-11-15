"""Verified inventory rows in Japanese Story Progress; no USA saved flags."""
import unittest
from practice.japan_story_progress import (
    JAPAN_PROGRESS_ITEMS, JAPAN_PROGRESS_SECTIONS,
    japan_progress_edit_options, japan_progress_row,
)
from practice.region_unlocks import japan_unlock_lead
from tests.test_japanese_fields import FakeRam


class JapanStoryProgressTests(unittest.TestCase):
    def test_seventeen_named_rows_exclude_battery_and_us_only_flags(self):
        self.assertEqual(len(JAPAN_PROGRESS_ITEMS), 17)
        self.assertNotIn('sasuke_battery_1_collected', JAPAN_PROGRESS_ITEMS)
        for slug, item in JAPAN_PROGRESS_ITEMS.items():
            self.assertTrue(japan_unlock_lead(item).user_verified)
            self.assertEqual(JAPAN_PROGRESS_SECTIONS[slug],
                             japan_progress_row(item, None)['section'])

    def test_treasure_and_fortune_doll_are_named_separately_from_story_bits(self):
        ram = FakeRam({
            (0x8016204B, 1): b'\x01',
            (0x80161EF7, 1): b'\x04',
        })
        star = japan_progress_row(JAPAN_PROGRESS_ITEMS['star'], ram)
        doll = japan_progress_row(
            JAPAN_PROGRESS_ITEMS['silver_fortune_doll_progress'], ram)
        self.assertEqual(star['address'], 0x8016204B)
        self.assertEqual(star['value'], '0x01')
        self.assertEqual(star['raw'], '0x01')
        self.assertEqual(star['section'], 'Collectibles & Miracles')
        self.assertEqual(doll['section'], 'Fortune Dolls')
        self.assertEqual(doll['value'], '0x04')
        self.assertIn('not a mapped Japanese saved-event bit', doll['source'])

    def test_allowed_edit_states_use_original_unlocks_and_jp_status(self):
        self.assertEqual(
            japan_progress_edit_options(JAPAN_PROGRESS_ITEMS['star']),
            ('0x00', '0x01'))
        self.assertEqual(
            japan_progress_edit_options(
                JAPAN_PROGRESS_ITEMS['silver_fortune_doll_progress']),
            ('0x00', '0x01', '0x02', '0x03', '0x04'))
        self.assertEqual(
            japan_progress_edit_options(JAPAN_PROGRESS_ITEMS['blue_fish_count']),
            ('0x00', '0x01', '0x02', '0x03'))

    def test_disconnected_read_is_not_guessed(self):
        item = JAPAN_PROGRESS_ITEMS['gold_key']
        result = japan_progress_row(item, FakeRam(error=OSError('unavailable')))
        self.assertEqual(result['value'], '—')
        self.assertEqual(result['raw'], '—')
        self.assertEqual(result['address'], 0x80161F03)


if __name__ == '__main__':
    unittest.main()
