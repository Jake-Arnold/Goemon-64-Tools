"""Read-only Japan-0 XYZ heuristic regression tests; synthetic RAM only."""
from __future__ import annotations

import struct
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from practice.japan_state_comparison import capture_japan_memory
from practice.japan_player_position_research import (
    find_japan_xyz_candidates, export_japan_xyz_all_candidates,
)
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
        self.assertTrue(row['c_stable_at_b'])
        self.assertNotIn('reverted', row)
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

    def test_export_all_xyz_candidates_beyond_the_display_limit(self):
        mem = FourMegabyteJapanRam()
        addresses = [XYZ_ADDR + 32 * i for i in range(240)]
        for i, addr in enumerate(addresses):
            put_xyz(mem, addr, (100.0 + i, 15.0, -75.0 + i / 4))
        a = capture(mem, 'A standing')
        for i, addr in enumerate(addresses):
            put_xyz(mem, addr, (112.0 + i, 15.0, -66.0 + i / 4))
        b = capture(mem, 'B moved')
        c = capture(mem, 'C still at B')
        preview = find_japan_xyz_candidates(a, b, c)
        self.assertEqual(len(preview['candidates']), 200)
        self.assertGreater(preview['counts']['candidate_count'], 200)
        with TemporaryDirectory() as temp:
            target = Path(temp) / 'all_xyz_candidates.json'
            count = export_japan_xyz_all_candidates(
                a, b, c, target,
                expected_count=preview['counts']['candidate_count'])
            export = json.loads(target.read_text(encoding='utf-8'))
            self.assertEqual(count, preview['counts']['candidate_count'])
            self.assertEqual(export['counts']['exported_candidates'], count)
            self.assertEqual(len(export['candidates']), count)
            self.assertEqual(export['candidate_order'], 'guest_address_ascending')
            self.assertEqual(export['session'], preview['session'])
            self.assertEqual(export['capture_A'], preview['capture_A'])
            self.assertNotIn('regions', export)
            self.assertNotIn('raw_snapshots', export)
            in_preview = {r['address'] for r in preview['candidates']}
            all_addresses = [r['address'] for r in export['candidates']]
            self.assertEqual(all_addresses, sorted(all_addresses))
            self.assertTrue(set(all_addresses) - in_preview)
            self.assertIn(f'0x{addresses[-1]:08X}', all_addresses)
            self.assertFalse(any(Path(temp).glob('*.tmp')))

    def test_full_xyz_export_rejects_bad_counts_and_cancelled_sessions(self):
        mem = FourMegabyteJapanRam()
        put_xyz(mem, XYZ_ADDR, (100.0, 20.0, -50.0))
        a = capture(mem)
        put_xyz(mem, XYZ_ADDR, (111.0, 20.0, -48.0))
        b = capture(mem, 'B')
        c = capture(mem, 'C')
        with TemporaryDirectory() as temp:
            target = Path(temp) / 'would_be_incomplete.json'
            with self.assertRaisesRegex(RuntimeError, 'count mismatch'):
                export_japan_xyz_all_candidates(
                    a, b, c, target, expected_count=999)
            self.assertFalse(target.exists())
            with self.assertRaisesRegex(RuntimeError, 'cancelled'):
                export_japan_xyz_all_candidates(
                    a, b, c, target, cancelled=lambda: True)
            self.assertFalse(target.exists())
            self.assertFalse(list(Path(temp).glob('*.tmp')))

    def test_stationary_A_and_B_identical_has_no_candidate(self):
        mem = FourMegabyteJapanRam()
        a = capture(mem)
        b = capture(mem, 'B')
        c = capture(mem, 'C')
        report = find_japan_xyz_candidates(a, b, c)
        self.assertEqual(report['counts']['candidate_count'], 0)


if __name__ == '__main__':
    unittest.main()
