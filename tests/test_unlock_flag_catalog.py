"""ROM-free protection for Unlocks > Story & event flags."""
import unittest

from practice.story_progress import FLAGS, CURATED_FLAGS, PLASMA_FLAGS, SAVED_BASE
from practice.region_unlocks import REGION_DELTA
from practice.unlock_flag_catalog import (
    USA_FLAGS, JAPAN_FLAGS, flags_for_region,
    read_flag_bytes, masked_flag_byte, write_confirmed_japan_flag,
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

    def test_japan_is_explicitly_mapped_and_only_benkei_writable(self):
        self.assertEqual(len(JAPAN_FLAGS), len(CURATED_FLAGS) + len(PLASMA_FLAGS))
        confirmed = [f for f in JAPAN_FLAGS if f.editable]
        self.assertEqual([f.key for f in confirmed], ['benkei_encounter'])
        self.assertEqual(confirmed[0].address, 0x80161DFC)
        self.assertEqual(confirmed[0].mask, 0x20)
        self.assertTrue(all(f.source == 'JP offset candidate'
                            for f in JAPAN_FLAGS if not f.editable))
        self.assertNotIn('congo_state_candidate', [f.key for f in confirmed])
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

    def test_only_confirmed_japan_bit_uses_expected_byte_write(self):
        confirmed = next(f for f in JAPAN_FLAGS if f.editable)
        candidate = next(f for f in JAPAN_FLAGS if not f.editable)
        writes = []
        def writer(address, data, *, expected):
            writes.append((address, data, expected))
            return True
        self.assertTrue(write_confirmed_japan_flag(
            writer, confirmed, 'Set', 0x81))
        self.assertEqual(writes, [(0x80161DFC, b'\xA1', b'\x81')])
        self.assertTrue(write_confirmed_japan_flag(
            writer, confirmed, 'Clear', 0xA1))
        self.assertEqual(writes[-1], (0x80161DFC, b'\x81', b'\xA1'))
        with self.assertRaises(PermissionError):
            write_confirmed_japan_flag(writer, candidate, 'Set', 0)
        self.assertEqual(len(writes), 2)

    def test_unavailable_and_short_reads_never_look_like_clear(self):
        class Short:
            def read_guest(self, *_args):
                return b'\0'
        with self.assertRaises(OSError):
            read_flag_bytes(Short(), 'japan')
