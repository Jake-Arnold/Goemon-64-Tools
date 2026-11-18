"""ROM-free auto PID/backend/endian discovery and verified hint regressions."""
import queue
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from practice.japan_auto_attach import (
    JapanProcessCandidate, classify_candidate, list_japan_processes,
    connect_candidate_ram,
)
from practice.japan_connection_hints import save_hint, load_hint
from practice.toolkit import Toolkit
from tests.test_japanese_mupen_attach import Process as MupenProcess
from tests.test_japanese_mupen_attach import PROBES as MUPEN_PROBES
from tests.test_japanese_mupen_attach import BASE
from tests.test_japan_native_recomp import (
    SyntheticNativeProcess, PROBES, HOST_BASE,
)


class NativeWithClose(SyntheticNativeProcess):
    def __init__(self, endian='big', host_base=HOST_BASE):
        super().__init__(endian)
        self.host_base = host_base
        self.closed = False

    def regions(self):
        return [(self.host_base, len(self.memory))]

    def read(self, address, size):
        off = address - self.host_base
        if not 0 <= off <= len(self.memory) - size:
            raise OSError('Not mapped')
        return bytes(self.memory[off:off + size])

    def close(self):
        self.closed = True


class AutoJapaneseAttachTests(unittest.TestCase):
    def test_recognizes_backend_candidates_but_not_as_region_proof(self):
        self.assertEqual(classify_candidate('Goemon64Recompi'), 'recomp')
        self.assertEqual(classify_candidate('mupen64plus'), 'mupen64plus')
        self.assertEqual(classify_candidate('Project64.exe'), 'project64')
        self.assertIsNone(classify_candidate('python3'))
        records = (
            SimpleNamespace(info={'pid': 101, 'name': 'Goemon64Recompi',
                                  'exe': '/tmp/Goemon64RecompiledJP'}),
            SimpleNamespace(info={'pid': 102, 'name': 'mupen64plus',
                                  'exe': '/usr/bin/mupen64plus'}),
            SimpleNamespace(info={'pid': 103, 'name': 'python3',
                                  'exe': '/usr/bin/python3'}),
        )
        class FakeProvider:
            NoSuchProcess = OSError
            AccessDenied = PermissionError
            @staticmethod
            def process_iter(fields):
                return iter(records)
        out = list_japan_processes(provider=FakeProvider(),
                                  allow_project64=False)
        self.assertEqual(
            [(x.pid, x.backend) for x in out],
            [(101, 'recomp'), (102, 'mupen64plus')])

    def test_linux_auto_discovery_includes_project64_wine_candidate(self):
        process = NativeWithClose('big')
        choice = JapanProcessCandidate(4242, 'project64',
                                       '/usr/bin/wine64-preloader')
        fake_reader = SimpleNamespace(rdram_size=0x400000)
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        with patch('practice.toolkit.sys.platform', 'linux'), \
             patch('practice.toolkit.list_japan_processes',
                   return_value=(choice,)) as scan, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(4242, 'project64')) as identity, \
             patch('practice.toolkit.HostProcess',
                   return_value=process), \
             patch('practice.toolkit.connect_candidate_ram',
                   return_value=(fake_reader, HOST_BASE, 'big')) as ram, \
             patch('practice.toolkit.remember_verified_connection'):
            Toolkit._connect_japan_auto_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'auto'))
        scan.assert_called_once_with(
            pid_hint=None, target='auto', allow_project64=True)
        identity.assert_called_once_with(4242, 'project64')
        self.assertEqual(ram.call_count, 1)
        result = app._connect_queue.get_nowait()
        self.assertEqual(result[:3], ('japan-ok', 4242, 'project64'))
        self.assertFalse(process.closed)

    def test_linux_explicit_project64_reuses_checked_4mb_scanner(self):
        process = NativeWithClose('big')
        fake_reader = SimpleNamespace(rdram_size=0x400000)
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        with patch('practice.toolkit.sys.platform', 'linux'), \
             patch('practice.toolkit.find_emulator_pid',
                   return_value=(4242, 'project64')) as find, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.HostProcess',
                   return_value=process), \
             patch('practice.toolkit.discover_japanese_mupen_rdram',
                   return_value=(fake_reader, HOST_BASE, 'big')) as scan:
            Toolkit._connect_japan_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'project64'))
        find.assert_called_once_with('project64')
        scan.assert_called_once()
        self.assertTrue(scan.call_args.kwargs['allow_4mb'])
        self.assertEqual(app._connect_queue.get_nowait()[:3],
                         ('japan-ok', 4242, 'project64'))
        self.assertFalse(process.closed)

    def test_explicit_wine_connection_reuses_reverified_rom_bound_hint(self):
        process = NativeWithClose('big')
        reader = SimpleNamespace(rdram_size=0x400000)
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        with patch('practice.toolkit.find_emulator_pid',
                   return_value=(4242, 'project64')), \
             patch('psutil.Process') as pid_process, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.HostProcess', return_value=process), \
             patch('practice.japan_connection_hints.load_hint',
                   return_value=(HOST_BASE, 'big')) as hint, \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=reader) as verified, \
             patch('practice.japan_native_recomp.validate_japan_recomp_context'
                   ) as context, \
             patch('practice.toolkit.discover_japanese_mupen_rdram'
                   ) as full_scan, \
             patch('practice.toolkit.remember_verified_connection') as saved:
            pid_process.return_value.exe.return_value = '/tmp/wine64-preloader'
            Toolkit._connect_japan_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'project64'))
        hint.assert_called_once_with(
            '/tmp/wine64-preloader', 'project64', PROBES)
        verified.assert_called_once_with(
            process, HOST_BASE, 'big', PROBES, allow_4mb=True)
        context.assert_called_once_with(reader, strict_character=False)
        full_scan.assert_not_called()
        saved.assert_called_once()
        self.assertEqual(app._connect_queue.get_nowait()[:3],
                         ('japan-ok', 4242, 'project64'))
        self.assertFalse(process.closed)

    def test_stale_explicit_hint_falls_back_to_full_rom_scan(self):
        process = NativeWithClose('big')
        reader = SimpleNamespace(rdram_size=0x400000)
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        with patch('practice.toolkit.find_emulator_pid',
                   return_value=(4242, 'project64')), \
             patch('psutil.Process') as pid_process, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.HostProcess', return_value=process), \
             patch('practice.japan_connection_hints.load_hint',
                   return_value=(HOST_BASE + 16, 'big')), \
             patch('practice.toolkit.validate_rdram_base',
                   side_effect=ValueError('Wrong executable code')), \
             patch('practice.toolkit.discover_japanese_mupen_rdram',
                   return_value=(reader, HOST_BASE, 'big')) as scanner, \
             patch('practice.toolkit.remember_verified_connection') as saved:
            pid_process.return_value.exe.return_value = '/tmp/wine64-preloader'
            Toolkit._connect_japan_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'project64'))
        scanner.assert_called_once()
        self.assertTrue(scanner.call_args.kwargs['allow_4mb'])
        saved.assert_called_once()
        self.assertEqual(app._connect_queue.get_nowait()[:3],
                         ('japan-ok', 4242, 'project64'))
        self.assertFalse(process.closed)

    def test_16bit_byte_swap_detection_does_not_depend_on_user_selection(self):
        process = MupenProcess('byteswapped')
        candidate = JapanProcessCandidate(102, 'mupen64plus', '/usr/bin/mupen64plus')
        rdram, base, endian = connect_candidate_ram(
            candidate, process, MUPEN_PROBES)
        self.assertEqual((base, endian), (BASE, 'byteswapped'))
        self.assertEqual(rdram.read_guest(0x80000450, 64), MUPEN_PROBES[0][1])

    def test_three_code_probes_without_plausible_live_state_cannot_attach(self):
        process = MupenProcess('wordswapped')
        process.memory[0xCD284 ^ 3] = 255  # Invalid Japanese engine state
        candidate = JapanProcessCandidate(102, 'mupen64plus',
                                           '/usr/bin/mupen64plus')
        with self.assertRaisesRegex(ValueError, 'implausible'):
            connect_candidate_ram(candidate, process, MUPEN_PROBES)

    def test_executable_hint_persists_but_never_substitutes_for_code_checks(self):
        candidate = JapanProcessCandidate(102, 'mupen64plus', '/usr/bin/mupen64plus')
        process = MupenProcess()
        with TemporaryDirectory() as folder:
            store = Path(folder) / 'cache.json'
            save_hint(candidate.executable, candidate.backend, MUPEN_PROBES,
                      BASE, 'wordswapped', store=store)
            self.assertEqual(
                load_hint(candidate.executable, candidate.backend,
                          MUPEN_PROBES, store=store),
                (BASE, 'wordswapped'))
            self.assertIsNone(load_hint('/different/binary', candidate.backend,
                                        MUPEN_PROBES, store=store))
            # Wrong cache offset must be rejected; full three-code-probe
            # detection then recovers the actual memory mapping.
            with patch('practice.japan_connection_hints.load_hint',
                       return_value=(BASE + 16, 'wordswapped')):
                _, base, endian = connect_candidate_ram(
                    candidate, process, MUPEN_PROBES)
            self.assertEqual((base, endian), (BASE, 'wordswapped'))
            process.memory[0x2400] ^= 1
            with self.assertRaisesRegex(RuntimeError, 'No Japanese'):
                connect_candidate_ram(candidate, process, MUPEN_PROBES)

    def test_auto_worker_selects_only_verified_recomp_with_byte_swapped_ram(self):
        process = NativeWithClose('byteswapped')
        chosen = JapanProcessCandidate(321, 'recomp',
                                       '/tmp/Goemon64RecompiledJP')
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        with patch('practice.toolkit.list_japan_processes',
                   return_value=(chosen,)), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.verified_japan_recomp_pid',
                   return_value=(321, 'recomp')) as verified, \
             patch('practice.toolkit.HostProcess', return_value=process), \
             patch('practice.toolkit.remember_verified_connection') as cache:
            Toolkit._connect_japan_auto_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'auto'))
        result = app._connect_queue.get_nowait()
        self.assertEqual(result[:3], ('japan-ok', 321, 'recomp'))
        self.assertEqual(result[5:], (HOST_BASE, 'byteswapped'))
        verified.assert_called_once_with(321)
        cache.assert_called_once()
        self.assertFalse(process.closed)

    def test_restarting_process_revalidates_cached_layout_not_old_pid(self):
        old = NativeWithClose('big')
        new = NativeWithClose('wordswapped', HOST_BASE + 0x10000000)
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        first = JapanProcessCandidate(321, 'recomp', '/tmp/JP-binary')
        second = JapanProcessCandidate(654, 'recomp', '/tmp/JP-binary')
        with patch('practice.toolkit.list_japan_processes',
                   side_effect=((first,), (second,))), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.verified_japan_recomp_pid',
                   side_effect=lambda pid: (pid, 'recomp')), \
             patch('practice.toolkit.HostProcess',
                   side_effect=(old, new)), \
             patch('practice.japan_connection_hints.load_hint',
                   return_value=(HOST_BASE, 'big')), \
             patch('practice.toolkit.remember_verified_connection'):
            for _ in range(2):
                Toolkit._connect_japan_auto_worker(
                    app, (None, 'japan-rom', None, 'auto', None, 'auto'))
        first_result = app._connect_queue.get_nowait()
        second_result = app._connect_queue.get_nowait()
        self.assertEqual((first_result[1], first_result[5:]),
                         (321, (HOST_BASE, 'big')))
        self.assertEqual((second_result[1], second_result[5:]),
                         (654, (HOST_BASE+0x10000000, 'wordswapped')))

    def test_multiple_verified_processes_report_both_pids(self):
        one, two = NativeWithClose(), NativeWithClose()
        app = SimpleNamespace(_connect_queue=queue.SimpleQueue())
        choices = (
            JapanProcessCandidate(321, 'recomp', '/bin/JP1'),
            JapanProcessCandidate(654, 'recomp', '/bin/JP2'))
        with patch('practice.toolkit.list_japan_processes',
                   return_value=choices), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.verified_japan_recomp_pid',
                   side_effect=lambda pid: (pid, 'recomp')), \
             patch('practice.toolkit.HostProcess', side_effect=(one, two)), \
             patch('practice.toolkit.remember_verified_connection') as cache:
            Toolkit._connect_japan_auto_worker(
                app, (None, 'japan-rom', None, 'auto', None, 'auto'))
        result = app._connect_queue.get_nowait()
        self.assertEqual(result[0], 'error')
        self.assertIn('Multiple Japanese processes', result[1])
        self.assertIn('PID 321', result[1])
        self.assertIn('PID 654', result[1])
        self.assertTrue(one.closed)
        self.assertTrue(two.closed)
        cache.assert_not_called()


if __name__ == '__main__':
    unittest.main()
