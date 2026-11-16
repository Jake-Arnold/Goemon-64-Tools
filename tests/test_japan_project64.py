"""Japan-0 Project64 memory discovery regression tests (no real emulator).

Windows Project64 can use 4 MiB or 8 MiB RDRAM; automatic and explicit
host bases must pass the same three Japan-0 executable code probes as Mupen.
"""
from __future__ import annotations

import queue
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.japan_state_comparison import capture_japan_memory, compare_japan_memory
from practice.value_search import ValueScanner
from tests.test_japanese_mupen_attach import BASE, PROBES, Process, jp


class FourMegabyteProcess(Process):
    def __init__(self, endian='wordswapped'):
        super().__init__(endian)
        self.memory = self.memory[:jp.MIN_RDRAM_SIZE]
        self.close_count = 0

    def close(self):
        self.close_count += 1


class JapanProject64Tests(unittest.TestCase):
    def test_four_megabyte_project64_detects_and_bounds_reads(self):
        for endian in ('big', 'wordswapped'):
            with self.subTest(endian=endian):
                proc = FourMegabyteProcess(endian)
                reader, base, mode = jp.discover_japanese_mupen_rdram(
                    proc, PROBES, allow_4mb=True, max_scan_mb=5)
                self.assertEqual((base, mode), (BASE, endian))
                self.assertEqual(reader.rdram_size, 0x400000)
                self.assertEqual(reader.read_guest(0x80000450, 64), PROBES[0][1])
                self.assertEqual(len(reader.read_guest(0x803FFFFF, 1)), 1)
                with self.assertRaisesRegex(ValueError, 'verified emulator'):
                    reader.read_guest(0x80400000, 1)
                with self.assertRaisesRegex(ValueError, 'verified emulator'):
                    reader.write_guest(0x80400000, bytes((1,)))

    def test_four_megabyte_requires_explicit_project64_mode(self):
        with self.assertRaisesRegex(RuntimeError, 'No Japanese emulator'):
            jp.discover_japanese_mupen_rdram(
                FourMegabyteProcess(), PROBES, max_scan_mb=5)

    def test_manual_project64_base_is_still_code_verified(self):
        proc = FourMegabyteProcess()
        reader, base, endian = jp.discover_japanese_mupen_rdram(
            proc, PROBES, allow_4mb=True, base_hint=BASE)
        self.assertEqual((base, endian), (BASE, 'wordswapped'))
        self.assertEqual(reader.rdram_size, 0x400000)
        with self.assertRaises(RuntimeError):
            jp.discover_japanese_mupen_rdram(
                proc, PROBES, allow_4mb=True, base_hint=BASE+0x1000)

    def test_project64_8mb_still_supported(self):
        reader, base, endian = jp.discover_japanese_mupen_rdram(
            Process(), PROBES, allow_4mb=True, max_scan_mb=9)
        self.assertEqual((base, endian), (BASE, 'wordswapped'))
        self.assertEqual(reader.rdram_size, 0x800000)

    def test_4mb_scanner_and_japan_abc_wide_capture(self):
        proc = FourMegabyteProcess()
        # Published Japan Ryo u16, in bounds of the unexpanded mapping.
        offset = 0x161DDA
        # Project64's word-swapped storage: canonical guest bytes
        # 00 00 00 0C at this aligned word become 0C 00 00 00.
        proc.memory[(offset & ~3):(offset & ~3)+4] = bytes((12, 0, 0, 0))
        reader, _, _ = jp.discover_japanese_mupen_rdram(
            proc, PROBES, allow_4mb=True, base_hint=BASE)
        scanner = ValueScanner(size=reader.rdram_size)
        self.assertGreaterEqual(scanner.start_exact(reader, 'u16', '12'), 1)
        identity = ('japan-0', 1234, BASE, 'wordswapped', id(reader))
        before = capture_japan_memory(reader, 'A', scope='wide', identity=identity)
        self.assertEqual(len(before.regions[0].data), 0x400000)
        after = capture_japan_memory(reader, 'B', scope='wide', identity=identity)
        report = compare_japan_memory(before, after)
        self.assertEqual(report['counts']['observed_changes'], 0)
        self.assertEqual(report['scope'], 'wide')

    def test_project64_worker_uses_read_only_process_and_4mb_flag(self):
        proc = FourMegabyteProcess()
        received = queue.SimpleQueue()
        host = SimpleNamespace(_connect_queue=received)
        opts = (321, 'exact-jp-rom.z64', None, 'auto', None, 'project64')
        with patch('practice.toolkit.verified_emulator_pid',
                   return_value=(321, 'project64')) as identify, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.HostProcess', return_value=proc) as open_pid:
            Toolkit._connect_japan_worker(host, opts)
        result = received.get_nowait()
        self.assertEqual(result[0:3], ('japan-ok', 321, 'project64'))
        self.assertEqual(result[4].rdram_size, 0x400000)
        identify.assert_called_once_with(321, 'project64')
        open_pid.assert_called_once_with(321, writable=False)

    def test_wrong_emulator_kind_cannot_open_process(self):
        host = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        opts = (321, 'exact-jp-rom.z64', None, 'auto', None, 'project64')
        with patch('practice.toolkit.verified_emulator_pid',
                   return_value=(321, 'mupen64plus')), \
             patch('practice.toolkit.HostProcess') as process:
            Toolkit._connect_japan_worker(host, opts)
        result = host._connect_queue.get_nowait()
        self.assertEqual(result[0], 'error')
        self.assertIn('changed during discovery', result[1])
        process.assert_not_called()


if __name__ == '__main__':
    unittest.main()
