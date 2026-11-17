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
        self.assertEqual(len(JAPAN_FLAGS), len(CURATED_FLAGS) + len(PLASMA_FLAGS))
        self.assertTrue(all(f.editable for f in JAPAN_FLAGS))
        confirmed = next(f for f in JAPAN_FLAGS if f.key == 'benkei_encounter')
        self.assertEqual(confirmed.address, 0x80161DFC)
        self.assertEqual(confirmed.mask, 0x20)
        candidate = next(f for f in JAPAN_FLAGS
                         if f.key == 'oedo_old_man_dialogue_cycle')
        self.assertTrue(candidate.editable)
        self.assertEqual(candidate.source, 'JP offset candidate')
        self.assertNotIn('congo_state_candidate', [f.key for f in JAPAN_FLAGS if f.source == 'JP user-confirmed'])
        self.assertNotIn('external_sasuke_recruited', [f.key for f in JAPAN_FLAGS])
        with self.assertRaises(ValueError):
            flags_for_region('unknown')

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

    def test_editable_json_lists_all_keys_and_preserves_address_masks(self):
        categories = load_flag_categories()
        self.assertEqual(set(categories), {f.key for f in FLAGS})
        from practice.unlock_flag_catalog import CATEGORY_FILE
        rows = json.loads(CATEGORY_FILE.read_text(encoding='utf-8'))['flags']
        self.assertEqual(sum('Japan' in row['regions'] for row in rows), 58)
        self.assertEqual(
            {row['key'] for row in rows if 'Japan' in row['regions']},
            {flag.key for flag in JAPAN_FLAGS})
        self.assertEqual(categories['benkei_encounter'],
                         ('Benkei & Kihachi', 'Unsorted'))
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
