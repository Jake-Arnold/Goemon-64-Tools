"""Read-only Japan-0 XYZ heuristic regression tests; synthetic RAM only."""
from __future__ import annotations

import struct
import unittest
from practice.japan_state_comparison import capture_japan_memory
from practice.japan_player_position_research import find_japan_xyz_candidates
from tests.test_japan_state_comparison import JP_ID, ReadOnlyJapanRam

XYZ_ADDR = 0x80034020


class FourMegabyteJapanRam(ReadOnlyJapanRam):
    def __init__(self):
        super().__init__()
        self.data = self.data[:0x400000]
        self.rdram_size = 0x400000


def put_xyz(memory, address, xyz):
    memory.set_bytes(address, struct.pack('>fff', *xyz))


def capture(memory, label='A', identity=JP_ID, scope='wide'):
    return capture_japan_memory(memory, label, identity=identity, scope=scope)


class JapanPlayerPositionResearchTests(unittest.TestCase):
    def test_walk_and_stop_returns_read_only_xyz_candidate_in_4mb(self):
        mem = FourMegabyteJapanRam()
        put_xyz(mem, XYZ_ADDR, (102.0, 18.0, -64.0))
        a = capture(mem, 'A standing')
        put_xyz(mem, XYZ_ADDR, (112.0, 18.0, -57.0))
        b = capture(mem, 'B after walk')
        put_xyz(mem, XYZ_ADDR, (112.1, 18.0, -57.0))
        c = capture(mem, 'C standing at B')
        report = find_japan_xyz_candidates(a, b, c)
        row = next(item for item in report['candidates']
                   if item['address'] == f'0x{XYZ_ADDR:08X}')
        self.assertEqual(row['watch_type'], 'f32')
        self.assertEqual(row['kind'], 'XYZ triple candidate')
        self.assertEqual(row['xyz_A'], [102.0, 18.0, -64.0])
        self.assertAlmostEqual(row['horizontal_delta'], (149) ** 0.5, places=3)
        self.assertLess(row['stationary_delta_max'], 0.11)
        self.assertEqual(report['session']['guest_ram_size'], 0x400000)
        self.assertEqual(report['format'], 'goemon-japan-xyz-heuristic-v1')
        self.assertNotIn('regions', report)
        self.assertFalse(hasattr(mem, 'write_guest'))

    def test_reverted_position_not_confused_with_staying_at_B(self):
        mem = FourMegabyteJapanRam()
        put_xyz(mem, XYZ_ADDR, (100.0, 20.0, 100.0))
        a = capture(mem)
        put_xyz(mem, XYZ_ADDR, (150.0, 20.0, 170.0))
        b = capture(mem, 'B')
        put_xyz(mem, XYZ_ADDR, (100.0, 20.0, 100.0))
        c = capture(mem, 'C')
        report = find_japan_xyz_candidates(a, b, c)
        self.assertFalse(any(r['address'] == f'0x{XYZ_ADDR:08X}'
                             for r in report['candidates']))

    def test_scene_change_or_connection_rejects_stale_snapshots(self):
        mem = FourMegabyteJapanRam()
        a = capture(mem)
        b = capture(mem, 'B')
        different = ('japan-0', JP_ID[1] + 1, *JP_ID[2:])
        c = capture(mem, 'C', identity=different)
        with self.assertRaisesRegex(ValueError, 'Different Japanese'):
            find_japan_xyz_candidates(a, b, c)
        mem.set_bytes(0x800CD2A2, (353).to_bytes(2, 'big'))
        c = capture(mem, 'C')
        with self.assertRaisesRegex(ValueError, 'same validated scene'):
            find_japan_xyz_candidates(a, b, c)

    def test_focused_rejected_and_limit_bounded(self):
        mem = FourMegabyteJapanRam()
        a = capture(mem, scope='focused')
        b = capture(mem, 'B', scope='focused')
        c = capture(mem, 'C', scope='focused')
        with self.assertRaisesRegex(ValueError, 'WIDE'):
            find_japan_xyz_candidates(a, b, c)
        with self.assertRaises(ValueError):
            find_japan_xyz_candidates(a, b, c, limit=0)
        with self.assertRaises(ValueError):
            find_japan_xyz_candidates(a, b, c, limit=201)

    def test_nonfinite_and_implausible_float_values_not_accepted(self):
        mem = FourMegabyteJapanRam()
        put_xyz(mem, XYZ_ADDR, (float('inf'), 0.0, 0.0))
        a = capture(mem)
        put_xyz(mem, XYZ_ADDR, (1000.0, 0.0, 0.0))
        b = capture(mem, 'B')
        c = capture(mem, 'C')
        report = find_japan_xyz_candidates(a, b, c)
        self.assertFalse(any(r['address'] == f'0x{XYZ_ADDR:08X}'
                             for r in report['candidates']))

    def test_stationary_A_and_B_identical_has_no_candidate(self):
        mem = FourMegabyteJapanRam()
        a = capture(mem)
        b = capture(mem, 'B')
        c = capture(mem, 'C')
        report = find_japan_xyz_candidates(a, b, c)
        self.assertEqual(report['counts']['candidate_count'], 0)


if __name__ == '__main__':
    unittest.main()
