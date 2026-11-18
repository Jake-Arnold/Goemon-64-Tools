"""Bidirectional canonical saved-event parity and unresolved-field guards."""
import unittest
from practice.address_registry import lookup
from practice.story_progress import FLAGS, PLASMA_FLAGS
from practice.unlock_flag_catalog import USA_FLAGS, JAPAN_FLAGS
from practice.region_unlocks import REGION_DELTA
from scripts.sync_address_catalogue import check_saved_event_crosswalk


class CrosswalkParityTests(unittest.TestCase):
    def test_every_named_saved_event_has_two_region_records(self):
        self.assertEqual(len(FLAGS), 142)
        self.assertEqual(len(USA_FLAGS), len(JAPAN_FLAGS))
        usa = {row.key: row for row in USA_FLAGS}
        jp = {row.key: row for row in JAPAN_FLAGS}
        self.assertEqual(set(usa), set(jp))
        for key, source in usa.items():
            counterpart = jp[key]
            suffix = ('plasma:' if any(
                f.key == key for f in PLASMA_FLAGS) else 'event:') + key
            source_row = lookup('story:usa:' + key)
            counterpart_row = lookup('crosswalk:japan:' + suffix)
            self.assertEqual(source_row['counterpart'],
                             f'0x{counterpart.address:08X}')
            self.assertEqual(counterpart_row['counterpart'],
                             f'0x{source.address:08X}')
            self.assertEqual(source.mask, counterpart.mask)
            self.assertEqual(counterpart.address,
                             source.address + REGION_DELTA)
            if key.startswith(('placed_silver_doll_', 'placed_gold_doll_')):
                self.assertEqual(counterpart_row['confidence'], 'candidate')

    def test_sync_rejects_silent_missing_partner_but_allows_explicit_unknown(self):
        source = {'id': 'story:usa:sample', 'category': 'saved_event_bit',
                  'region': 'usa', 'address': '0x8015C608',
                  'mask': '0x1', 'counterpart': '0x80161DF8'}
        japan = dict(source, id='crosswalk:japan:event:sample',
                     region='japan', address='0x80161DF8',
                     counterpart='0x8015C608')
        check_saved_event_crosswalk([source, japan])
        with self.assertRaisesRegex(ValueError, 'Missing reciprocal'):
            check_saved_event_crosswalk([source])
        explicitly_unknown = dict(source, counterpart=None,
                                  crosswalk_status='unresolved')
        check_saved_event_crosswalk([explicitly_unknown])


if __name__ == '__main__':
    unittest.main()
