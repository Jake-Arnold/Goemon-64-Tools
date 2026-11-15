"""Japanese region-scoped A/B/C memory capture tests; never writes game RAM."""
import unittest
from practice.japan_state_comparison import (
    capture_japan_memory, compare_japan_memory, JAPAN_WIDE_RANGE,
)
from practice.value_search import GUEST_BASE, RDRAM_SIZE

JP_ID = ('japan-0', 123, 0x10000000, 'wordswapped')


class ReadOnlyJapanRam:
    def __init__(self):
        self.base, self.endian = JP_ID[2:]
        self.data = bytearray(RDRAM_SIZE)
        self.data[0xCD2A2:0xCD2A4] = (352).to_bytes(2, 'big')
        self.data[0x161DCC:0x161DD0] = (0).to_bytes(4, 'big')
        self.reads = 0

    def read_guest(self, address, width):
        self.reads += 1
        start = address - GUEST_BASE
        if start < 0 or start + width > len(self.data):
            raise OSError('out-of-bounds guest memory')
        return bytes(self.data[start:start + width])

    def set_bytes(self, address, data):
        start = address - GUEST_BASE
        self.data[start:start + len(data)] = data


class JapanAbcReadOnlyTests(unittest.TestCase):
    def test_focused_before_after_revert_and_session_identity(self):
        mem = ReadOnlyJapanRam()
        hp = 0x80161DD7
        mem.set_bytes(hp, b'\x64')
        a = capture_japan_memory(mem, 'HP before', identity=JP_ID)
        self.assertEqual(a.character, 0)
        self.assertEqual(a.map_id, 352)
        self.assertEqual({r.name for r in a.regions},
                         {'jp_engine_candidates', 'jp_inventory_candidates'})
        mem.set_bytes(hp, b'\x5A')
        b = capture_japan_memory(mem, 'HP after', identity=JP_ID)
        report = compare_japan_memory(a, b)
        row = next(x for x in report['candidates']
                   if x['address'] == f'0x{hp:08X}')
        self.assertEqual((row['before'], row['after']), ('64', '5A'))
        self.assertEqual(report['event_flag_changes'], [])
        self.assertEqual(report['region'], 'japan-0')
        mem.set_bytes(hp, b'\x64')
        c = capture_japan_memory(mem, 'HP recovered', identity=JP_ID)
        report = compare_japan_memory(a, b, c)
        self.assertEqual(report['counts']['reverting_changes'], 1)
        self.assertEqual(report['counts']['candidate_count'], 1)
        self.assertFalse(hasattr(mem, 'write_guest'))

    def test_reject_different_pid_base_endian_or_range(self):
        mem = ReadOnlyJapanRam()
        a = capture_japan_memory(mem, 'A', identity=JP_ID)
        b = capture_japan_memory(mem, 'B',
                                 identity=('japan-0', 124, JP_ID[2], JP_ID[3]))
        with self.assertRaisesRegex(ValueError, 'Different Japanese'):
            compare_japan_memory(a, b)
        with self.assertRaises(ValueError):
            capture_japan_memory(mem, 'A', identity=('usa', 123, JP_ID[2], JP_ID[3]))
        with self.assertRaises(ValueError):
            capture_japan_memory(mem, 'A', scope='invalid', identity=JP_ID)

    def test_wide_reads_full_eight_megabytes_without_exporting_raw_data(self):
        mem = ReadOnlyJapanRam()
        a = capture_japan_memory(mem, 'Wide A', scope='wide', identity=JP_ID)
        self.assertEqual(len(a.regions[0].data), RDRAM_SIZE)
        self.assertEqual((a.regions[0].name, a.regions[0].address),
                         JAPAN_WIDE_RANGE[:2])
        mem.set_bytes(0x807FFFF0, b'\x01')
        b = capture_japan_memory(mem, 'Wide B', scope='wide', identity=JP_ID)
        report = compare_japan_memory(a, b, limit=3)
        self.assertEqual(report['counts']['candidate_count'], 1)
        self.assertEqual(report['candidates'][0]['address'], '0x807FFFF0')
        self.assertNotIn('regions', report)
        self.assertNotIn('data', report['candidates'][0])

    def test_bounded_candidate_storage_and_full_count(self):
        mem = ReadOnlyJapanRam()
        a = capture_japan_memory(mem, 'A', identity=JP_ID)
        for i in range(32):
            mem.set_bytes(0x80161E00 + i, b'\x01')
        b = capture_japan_memory(mem, 'B', identity=JP_ID)
        report = compare_japan_memory(a, b, limit=5)
        self.assertEqual(report['counts']['observed_changes'], 32)
        self.assertEqual(report['counts']['candidate_count'], 32)
        self.assertEqual(report['counts']['reported_candidates'], 5)
        self.assertEqual(len(report['candidates']), 5)
        self.assertTrue(all(r['kind'] == 'boolean candidate'
                            for r in report['candidates']))


if __name__ == '__main__':
    unittest.main()
