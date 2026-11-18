"""ROM-free protection for Unlocks > Story & event flags."""
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest

from practice.story_progress import FLAGS, CURATED_FLAGS, PLASMA_FLAGS, SAVED_BASE
from practice.region_unlocks import REGION_DELTA
from practice.unlock_flag_catalog import (
    USA_FLAGS, JAPAN_FLAGS, flags_for_region, load_flag_categories,
    read_flag_bytes, masked_flag_byte, write_japan_crosswalk_flag, UnlockFlag,
)
from tests.test_unlocks import FakeRAM


class CatalogTests(unittest.TestCase):
    def test_usa_keeps_every_existing_named_bit_and_exact_mask(self):
        self.assertEqual(len(USA_FLAGS), len(FLAGS))
        self.assertEqual(
            [(f.key, f.address, f.mask) for f in USA_FLAGS],
            [(f.key, f.address, f.mask) for f in FLAGS])
        self.assertTrue(all(f.editable for f in USA_FLAGS))
        self.assertEqual(len({(f.address, f.mask) for f in USA_FLAGS}), len(FLAGS))

    def test_japan_all_crosswalk_flags_are_writable_with_evidence_preserved(self):
        self.assertEqual(len(JAPAN_FLAGS), len(USA_FLAGS))
        self.assertTrue(all(f.editable for f in JAPAN_FLAGS))
        confirmed = next(f for f in JAPAN_FLAGS if f.key == 'benkei_encounter')
        self.assertEqual(confirmed.address, 0x80161DFC)
        self.assertEqual(confirmed.mask, 0x20)
        candidate = next(f for f in JAPAN_FLAGS
                         if f.key == 'oedo_old_man_dialogue_cycle')
        self.assertTrue(candidate.editable)
        self.assertEqual(candidate.source, 'JP offset candidate')
        self.assertNotIn('congo_state_candidate', [f.key for f in JAPAN_FLAGS if f.source == 'JP user-confirmed'])
        self.assertIn('external_sasuke_recruited', [f.key for f in JAPAN_FLAGS])
        receipt = next(f for f in JAPAN_FLAGS if f.key == 'external_super_pass')
        self.assertEqual((receipt.address, receipt.mask), (0x80161DF8, 0x01))
        self.assertTrue(receipt.editable)
        self.assertEqual(receipt.source, 'JP offset candidate')
        self.assertEqual(sum(f.key == 'external_super_pass' for f in JAPAN_FLAGS), 1)
        with self.assertRaises(ValueError):
            flags_for_region('unknown')

    def test_every_usa_story_flag_has_a_japanese_candidate_with_same_mask(self):
        from practice.address_registry import guest_bit, lookup
        from practice.story_progress import FLAGS
        self.assertEqual({x.key for x in USA_FLAGS},
                         {x.key for x in JAPAN_FLAGS})
        japanese = {x.key: x for x in JAPAN_FLAGS}
        for source in FLAGS:
            paired = japanese[source.key]
            self.assertEqual(paired.address, source.address + REGION_DELTA)
            self.assertEqual(paired.mask, source.mask)
            self.assertEqual(guest_bit(
                ('crosswalk:japan:plasma:' if source in PLASMA_FLAGS
                 else 'crosswalk:japan:event:') + source.key,
                region='japan'), (paired.address, paired.mask))
            registry_row = lookup('story:usa:' + source.key)
            self.assertEqual(registry_row['counterpart'],
                             f'0x{paired.address:08X}')
            self.assertEqual(paired.editable, True)
        placement = japanese['placed_silver_doll_0ca']
        self.assertEqual((placement.address, placement.mask),
                         (0x80161E11, 0x04))
        self.assertEqual(placement.source, 'JP offset candidate')

    def test_one_bank_read_and_bit_preservation_in_both_regions(self):
        for region in ('usa', 'japan'):
            ram = FakeRAM()
            base = SAVED_BASE + (REGION_DELTA if region == 'japan' else 0)
            ram.bytes[base + 4] = 0xA5
            rows = flags_for_region(region)
            sample = read_flag_bytes(ram, region, rows)
            self.assertEqual(len(sample), len(rows))
            self.assertTrue(all(base <= f.address < base + 0x64 for f in rows))
            self.assertEqual(sample[next(f.key for f in rows
                                         if f.address == base + 4)], 0xA5)
            self.assertEqual(read_flag_bytes(None, region), {})

    def test_masked_bit_keeps_unrelated_bits(self):
        flag = next(f for f in USA_FLAGS if f.key == 'benkei_encounter')
        self.assertEqual(masked_flag_byte(flag, 'Set', 0x81), 0xA1)
        self.assertEqual(masked_flag_byte(flag, 'Clear', 0xA1), 0x81)
        with self.assertRaises(ValueError):
            masked_flag_byte(flag, 'Toggle', 0x20)
        with self.assertRaises(ValueError):
            masked_flag_byte(flag, 'Set', -1)

    def test_confirmed_and_candidate_japan_bits_use_expected_byte_write(self):
        confirmed = next(f for f in JAPAN_FLAGS if f.source == 'JP user-confirmed')
        candidate = next(f for f in JAPAN_FLAGS if f.source == 'JP offset candidate')
        writes = []
        def writer(address, data, *, expected):
            writes.append((address, data, expected))
            return True
        self.assertTrue(write_japan_crosswalk_flag(
            writer, confirmed, 'Set', 0x81))
        self.assertEqual(writes, [(0x80161DFC, b'\xA1', b'\x81')])
        self.assertTrue(write_japan_crosswalk_flag(
            writer, confirmed, 'Clear', 0xA1))
        self.assertEqual(writes[-1], (0x80161DFC, b'\x81', b'\xA1'))
        self.assertTrue(write_japan_crosswalk_flag(
            writer, candidate, 'Set', 0))
        self.assertEqual(writes[-1], (
            candidate.address, bytes((candidate.mask,)), b'\x00'))
        self.assertTrue(write_japan_crosswalk_flag(
            writer, candidate, 'Clear', candidate.mask))
        self.assertEqual(writes[-1], (
            candidate.address, b'\x00', bytes((candidate.mask,))))
        unmapped = UnlockFlag('unknown', 'Unknown', 'Diagnostics',
                              0x80161DFC, 0x20, 'manual', '', True)
        with self.assertRaises(ValueError):
            write_japan_crosswalk_flag(writer, unmapped, 'Set', 0)
        self.assertEqual(len(writes), 4)

    def test_receipt_masked_writes_and_inventory_independence(self):
        receipt = next(f for f in JAPAN_FLAGS if f.key == 'external_super_pass')
        for initial, action, result in (
                (0x00, 'Set', 0x01), (0x01, 'Clear', 0x00),
                (0x04, 'Set', 0x05), (0x05, 'Clear', 0x04),
                (0xA4, 'Set', 0xA5), (0xA5, 'Clear', 0xA4),
                (0xFF, 'Clear', 0xFE), (0xFE, 'Set', 0xFF)):
            writes = []
            self.assertTrue(write_japan_crosswalk_flag(
                lambda address, data, *, expected:
                    writes.append((address, data, expected)) or True,
                receipt, action, initial))
            self.assertEqual(writes, [
                (0x80161DF8, bytes((result,)), bytes((initial,)))])
        ram = FakeRAM()
        ram.bytes[0x80161DF8] = 0x04
        ram.bytes[0x80161EF3] = 0x01
        def write(address, data, *, expected):
            self.assertEqual(ram.read_guest(address, 1), expected)
            ram.write_guest(address, data)
            return True
        ram.write_guest(0x80161EF3, b'\x00')
        self.assertEqual((ram.bytes[0x80161DF8], ram.bytes[0x80161EF3]),
                         (0x04, 0x00))
        write_japan_crosswalk_flag(write, receipt, 'Set', 0x04)
        self.assertEqual((ram.bytes[0x80161DF8], ram.bytes[0x80161EF3]),
                         (0x05, 0x00))
        ram.write_guest(0x80161EF3, b'\x01')
        self.assertEqual((ram.bytes[0x80161DF8], ram.bytes[0x80161EF3]),
                         (0x05, 0x01))
        write_japan_crosswalk_flag(write, receipt, 'Clear', 0x05)
        self.assertEqual((ram.bytes[0x80161DF8], ram.bytes[0x80161EF3]),
                         (0x04, 0x01))
        self.assertEqual(read_flag_bytes(ram, 'japan')[receipt.key], 0x04)

    def test_editable_json_lists_all_keys_and_preserves_address_masks(self):
        categories = load_flag_categories()
        self.assertEqual(set(categories), {f.key for f in FLAGS})
        from practice.unlock_flag_catalog import CATEGORY_FILE
        rows = json.loads(CATEGORY_FILE.read_text(encoding='utf-8'))['flags']
        self.assertEqual(sum('Japan' in row['regions'] for row in rows), 142)
        self.assertEqual(
            {row['key'] for row in rows if 'Japan' in row['regions']},
            {flag.key for flag in JAPAN_FLAGS})
        self.assertEqual(categories['benkei_encounter'],
                         ('Benkei & Kihachi', 'Unsorted'))
        self.assertEqual(categories['external_super_pass'],
                         ('External annotations', 'Unsorted'))
        for region, original in (('usa', USA_FLAGS), ('japan', JAPAN_FLAGS)):
            shown = flags_for_region(region)
            self.assertEqual(
                {f.key: (f.address, f.mask, f.source) for f in shown},
                {f.key: (f.address, f.mask, f.source) for f in original})
            self.assertTrue(all(f.subtype == 'Unsorted' for f in shown))
        japanese = next(f for f in flags_for_region('japan')
                        if f.key == 'oedo_old_man_dialogue_cycle')
        written = []
        self.assertTrue(write_japan_crosswalk_flag(
            lambda address, data, *, expected: written.append(
                (address, data, expected)) or True,
            japanese, 'Set', 0))
        self.assertEqual(written[0][0], japanese.address)

    def test_json_can_reassign_type_subtype_and_reorder_rows(self):
        from practice.unlock_flag_catalog import CATEGORY_FILE
        original = json.loads(CATEGORY_FILE.read_text(encoding='utf-8'))
        flags = original['flags']
        benkei = next(row for row in flags if row['key'] == 'benkei_encounter')
        benkei['type'] = 'Test area'
        benkei['subtype'] = 'First chapter'
        flags.insert(0, flags.pop(flags.index(benkei)))
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / 'types.json'
            test_file.write_text(json.dumps(original), encoding='utf-8')
            with patch('practice.unlock_flag_catalog.CATEGORY_FILE', test_file):
                self.assertEqual(load_flag_categories()['benkei_encounter'],
                                 ('Test area', 'First chapter'))
                usa = flags_for_region('usa')
                jp = flags_for_region('japan')
                self.assertEqual(usa[0].key, 'benkei_encounter')
                self.assertEqual(usa[0].group, 'Test area')
                self.assertEqual(usa[0].subtype, 'First chapter')
                self.assertEqual(jp[0].key, 'benkei_encounter')
                self.assertEqual(jp[0].address, 0x80161DFC)
                self.assertEqual(jp[0].mask, 0x20)

    def test_malformed_category_json_does_not_block_game_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            broken = Path(directory) / 'types.json'
            broken.write_text('{not json', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Cannot read'):
                load_flag_categories(broken)
            with patch('practice.unlock_flag_catalog.CATEGORY_FILE', broken):
                self.assertEqual(len(flags_for_region('usa')), len(FLAGS))
                self.assertEqual(len(flags_for_region('japan')), len(JAPAN_FLAGS))

    def test_unavailable_and_short_reads_never_look_like_clear(self):
        class Short:
            def read_guest(self, *_args):
                return b'\0'
        with self.assertRaises(OSError):
            read_flag_bytes(Short(), 'japan')
