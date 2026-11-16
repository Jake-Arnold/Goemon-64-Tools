"""ROM-free Japanese native recomp detection and toolkit routing regressions."""
import queue
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from practice.japan_native_recomp import (
    verified_japan_recomp_pid, discover_japan_recomp_rdram,
    validate_japan_recomp_context, validate_japan_recomp_writer,
)
from practice.japanese_mupen_attach import VerifiedJapaneseProbes
from practice.toolkit import Toolkit


HOST_BASE = 0x20000000
SIZE = 0x800000
PROBE_OFFSETS = (0x450, 0x600, 0x2400)
PROBE_BYTES = tuple(bytes((i * 47 + j * 3 + 1) % 256
                          for j in range(64)) for i in range(3))
PROBES = VerifiedJapaneseProbes(
    tuple(zip(PROBE_OFFSETS, PROBE_BYTES)), b'Original-JP-ROM-header-not-present-in-RAM'.ljust(64, b'!'))


class SyntheticNativeProcess:
    """Sparse-enough 8 MiB guest memory with executable code and game state."""

    def __init__(self, endian='wordswapped'):
        memory = bytearray(SIZE)
        for off, code in PROBES:
            memory[off:off + len(code)] = code
        memory[0xCD284] = 13  # Japan game-state byte.
        memory[0xCD2A2:0xCD2A4] = (0x161).to_bytes(2, 'big')
        memory[0x161DCC:0x161DD0] = (0).to_bytes(4, 'big')
        if endian == 'wordswapped':
            memory = bytearray(b''.join(memory[i:i+4][::-1]
                                        for i in range(0, len(memory), 4)))
        elif endian == 'byteswapped':
            memory = bytearray(b''.join(memory[i:i+2][::-1]
                                        for i in range(0, len(memory), 2)))
        self.memory = memory
        self.endian = endian

    def regions(self):
        return [(HOST_BASE, SIZE)]

    def read(self, address, size):
        off = address - HOST_BASE
        if not 0 <= off <= SIZE - size:
            raise OSError('Synthetic process address not mapped')
        return bytes(self.memory[off:off + size])


class JapaneseRecompAttachTests(unittest.TestCase):
    def test_native_process_name_is_required(self):
        with patch('psutil.Process') as ps:
            ps.return_value.name.return_value = 'Goemon64Recompi'
            self.assertEqual(verified_japan_recomp_pid(1234), (1234, 'recomp'))
            ps.return_value.name.return_value = 'Project64.exe'
            with self.assertRaisesRegex(ValueError, 'not a Goemon'):
                verified_japan_recomp_pid(1234)

    def test_native_recomp_discovers_verified_japan_ram_all_layouts(self):
        for endian in ('wordswapped', 'big', 'byteswapped'):
            with self.subTest(endian=endian):
                process = SyntheticNativeProcess(endian)
                reader, base, got = discover_japan_recomp_rdram(
                    process, PROBES)
                self.assertEqual((base, got), (HOST_BASE, endian))
                self.assertEqual(reader.read_guest(0x800CD284, 1), bytes((13,)))
                self.assertEqual(reader.read_guest(0x800CD2A2, 2),
                                 bytes.fromhex('0161'))

    def test_connection_does_not_require_playable_character_initialization(self):
        process = SyntheticNativeProcess('big')
        process.memory[0x161DCC:0x161DD0] = (99).to_bytes(4, 'big')
        reader, base, mode = discover_japan_recomp_rdram(process, PROBES)
        self.assertEqual((base, mode), (HOST_BASE, 'big'))
        self.assertEqual(reader.read_guest(0x80161DCC, 4),
                         (99).to_bytes(4, 'big'))
        with self.assertRaisesRegex(ValueError, 'character is invalid'):
            validate_japan_recomp_writer(process, reader, PROBES)

    def test_native_attach_rejects_missing_original_code(self):
        process = SyntheticNativeProcess('big')
        process.memory[0x2400] ^= 1
        with self.assertRaisesRegex(RuntimeError, 'No Japanese emulator RDRAM'):
            discover_japan_recomp_rdram(process, PROBES)

    def test_native_writer_revalidates_code_and_game_state(self):
        process = SyntheticNativeProcess('big')
        reader, _, _ = discover_japan_recomp_rdram(process, PROBES)
        writable = validate_japan_recomp_writer(process, reader, PROBES)
        self.assertEqual(writable.read_guest(0x800CD284, 1), bytes((13,)))
        process.memory[0x600] ^= 1
        with self.assertRaisesRegex(ValueError, 'verification failed'):
            validate_japan_recomp_writer(process, reader, PROBES)

    def test_native_gameplay_state_rejects_wrong_character(self):
        process = SyntheticNativeProcess('big')
        reader, _, _ = discover_japan_recomp_rdram(process, PROBES)
        process.memory[0x161DCC:0x161DD0] = (99).to_bytes(4, 'big')
        with self.assertRaisesRegex(ValueError, 'character is invalid'):
            validate_japan_recomp_context(reader)

    def test_toolkit_worker_uses_native_backend_and_not_emulator_detection(self):
        app = object.__new__(Toolkit)
        app._connect_queue = queue.SimpleQueue()
        process = SyntheticNativeProcess('big')
        with patch('practice.toolkit.verified_japan_recomp_pid',
                   return_value=(1234, 'recomp')) as native, \
             patch('practice.toolkit.verified_emulator_pid') as emulator, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES), \
             patch('practice.toolkit.HostProcess', return_value=process):
            app._connect_japan_worker((1234, 'verified_rom', None,
                                       'auto', None, 'recomp'))
        result = app._connect_queue.get_nowait()
        self.assertEqual(result[:3], ('japan-ok', 1234, 'recomp'))
        self.assertEqual(result[5:], (HOST_BASE, 'big'))
        native.assert_called_once_with(1234)
        emulator.assert_not_called()

    def test_toolkit_uses_native_writer_verification(self):
        app = object.__new__(Toolkit)
        app.jp_backend = 'recomp'
        app.game_pid = 1234
        app.verified_rom_path = 'verified_rom'
        process = SyntheticNativeProcess('big')
        reader, _, _ = discover_japan_recomp_rdram(process, PROBES)
        with patch('practice.toolkit.verified_japan_recomp_pid',
                   return_value=(1234, 'recomp')) as pid_check, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=PROBES):
            writer = Toolkit._japan_writable_reader(app, process, reader)
        self.assertEqual(writer.read_guest(0x800CD284, 1), bytes((13,)))
        pid_check.assert_called_once_with(1234)


if __name__ == '__main__':
    unittest.main()
