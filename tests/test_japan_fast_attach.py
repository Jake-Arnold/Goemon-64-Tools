"""ROM-free Japanese recomp quick-path, ASLR hint and ambiguity regressions."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from practice.japan_auto_attach import (
    JapanProcessCandidate, connect_candidate_ram,
    remember_verified_connection, list_japan_processes,
)
from practice.japan_connection_hints import (
    load_hint, load_hint_record, save_hint,
)
from practice.japanese_mupen_attach import (
    AmbiguousJapaneseRdram, discover_japanese_mupen_rdram,
)
from tests.test_japan_native_recomp import (
    HOST_BASE, SIZE, PROBES, SyntheticNativeProcess,
)
from tests.test_japan_auto_attach import NativeWithClose


class TwoMappings:
    """Two independent valid 8 MiB game-memory copies in one process."""
    def __init__(self, valid_second=True):
        self.bases = (HOST_BASE + 0x10000000, HOST_BASE + 0x20000000)
        self.data = (SyntheticNativeProcess('wordswapped').memory,
                     SyntheticNativeProcess('wordswapped').memory)
        if not valid_second:
            # Guest 0x800CD284: native word-swapped engine-state u8.
            self.data[1][0xCD284 ^ 3] = 255

    def regions(self):
        return [(base, SIZE) for base in self.bases]

    def read(self, address, size):
        for base, data in zip(self.bases, self.data):
            offset = address - base
            if 0 <= offset <= len(data) - size:
                return bytes(data[offset:offset + size])
        raise OSError('unmapped address')


class JapaneseFastAttachTests(unittest.TestCase):
    def test_exact_8mb_mapping_avoids_4mb_bulk_reads(self):
        process = NativeWithClose('wordswapped')
        reads = []
        original = process.read

        def traced(address, size):
            reads.append(size)
            return original(address, size)
        process.read = traced
        reader, base, order = discover_japanese_mupen_rdram(process, PROBES)
        self.assertEqual((base, order), (HOST_BASE, 'wordswapped'))
        self.assertEqual(reader.read_guest(0x80000450, 4), PROBES[0][1][:4])
        self.assertLessEqual(max(reads), 64)

    def test_separate_valid_8mb_mappings_still_report_ambiguity(self):
        with self.assertRaises(AmbiguousJapaneseRdram) as ctx:
            discover_japanese_mupen_rdram(TwoMappings(), PROBES)
        self.assertEqual(len(ctx.exception.candidates), 2)

    def test_ambiguous_code_copies_with_bad_game_state_choose_plausible(self):
        process = TwoMappings(valid_second=False)
        candidate = JapanProcessCandidate(123, 'recomp', 'name:goemon64recompi')
        _, base, endian = connect_candidate_ram(candidate, process, PROBES)
        self.assertEqual((base, endian), (process.bases[0], 'wordswapped'))

    def test_two_plausible_copy_candidates_remain_manual(self):
        candidate = JapanProcessCandidate(123, 'recomp', 'name:goemon64recompi')
        with self.assertRaises(AmbiguousJapaneseRdram):
            connect_candidate_ram(candidate, TwoMappings(), PROBES)

    def test_reuse_mapping_offset_after_linux_aslr_relocation(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / 'hints.json'
            candidate = JapanProcessCandidate(123, 'recomp', '/tmp/Goemon64RecompiledJP')
            old = NativeWithClose('wordswapped', HOST_BASE)
            new = NativeWithClose('wordswapped', HOST_BASE + 0x10000000)
            with patch('practice.japan_connection_hints.hints_path',
                       return_value=store):
                remember_verified_connection(
                    candidate, PROBES, HOST_BASE, 'wordswapped', process=old)
                record = load_hint_record(candidate.executable, 'recomp', PROBES)
                self.assertEqual((record['mapping_size'],
                                  record['mapping_offset']), (SIZE, 0))
                sizes = []
                original = new.read

                def counted(address, size):
                    sizes.append(size)
                    return original(address, size)
                new.read = counted
                _, base, order = connect_candidate_ram(candidate, new, PROBES)
            self.assertEqual((base, order),
                             (HOST_BASE + 0x10000000, 'wordswapped'))
            self.assertLessEqual(max(sizes), 64)

    def test_multiple_rebased_valid_mappings_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / 'hints.json'
            candidate = JapanProcessCandidate(123, 'recomp', '/tmp/Goemon64RecompiledJP')
            old = NativeWithClose('wordswapped')
            with patch('practice.japan_connection_hints.hints_path',
                       return_value=store):
                remember_verified_connection(
                    candidate, PROBES, HOST_BASE, 'wordswapped', process=old)
                with self.assertRaises(AmbiguousJapaneseRdram):
                    connect_candidate_ram(candidate, TwoMappings(), PROBES)

    def test_previous_absolute_only_cache_format_is_compatible(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / 'hints.json'
            save_hint('name:goemon64recompi', 'recomp', PROBES,
                      HOST_BASE, 'wordswapped', store=store)
            self.assertEqual(
                load_hint('name:goemon64recompi', 'recomp', PROBES,
                          store=store), (HOST_BASE, 'wordswapped'))
            record = load_hint_record('name:goemon64recompi',
                                      'recomp', PROBES, store=store)
            self.assertNotIn('mapping_size', record)

    def test_process_name_is_cached_when_exe_is_unavailable(self):
        from types import SimpleNamespace
        class Provider:
            NoSuchProcess = OSError
            AccessDenied = PermissionError
            @staticmethod
            def process_iter(fields):
                return iter([SimpleNamespace(info={
                    'pid': 123, 'name': 'Goemon64Recompi', 'exe': None})])
        matches = list_japan_processes(
            provider=Provider(), target='recomp')
        self.assertEqual(matches[0].executable, 'name:goemon64recompi')


if __name__ == '__main__':
    unittest.main()
