"""Exercise live-RDRAM/retail-ROM duplicate rejection without any copyrighted ROM."""
from __future__ import annotations
import unittest
from practice.japanese_mupen_attach import (
    VerifiedJapaneseProbes, AmbiguousJapaneseRdram, _swapped_words,
    discover_japanese_mupen_rdram, ROM_TO_GUEST, PROBE_ROM_OFFSETS, PROBE_BYTES,
)

BASE = 0x10000000


class FakeProcess:
    def __init__(self, data):
        self.data = data

    def regions(self):
        return [(BASE, len(self.data))]

    def read(self, address, length):
        offset = address - BASE
        if not 0 <= offset <= len(self.data) - length:
            raise OSError('unmapped')
        return bytes(self.data[offset:offset + length])


def build_case(endian, *, with_rom_copy=True, with_second_rdram=False):
    rom = bytearray(16 << 20)
    rom[:64] = bytes((i * 31 + 17) % 256 for i in range(64))
    for index, offset in enumerate(PROBE_ROM_OFFSETS):
        rom[offset:offset + PROBE_BYTES] = bytes(
            (i * 17 + index * 53 + 8) % 256 for i in range(PROBE_BYTES))
    probes = VerifiedJapaneseProbes(
        [(off - ROM_TO_GUEST, bytes(rom[off:off + PROBE_BYTES]))
         for off in PROBE_ROM_OFFSETS], rom[:64])
    memory = bytearray(32 << 20)
    def encode(block):
        return _swapped_words(block) if endian == 'wordswapped' else block
    for offset, code in probes:
        memory[offset:offset + len(code)] = encode(code)
    false_base = None
    if with_rom_copy:
        cartridge_start = 12 << 20
        data = encode(bytes(rom))
        memory[cartridge_start:cartridge_start + len(data)] = data
        false_base = BASE + cartridge_start + ROM_TO_GUEST
    if with_second_rdram:
        second = 10 << 20
        for offset, code in probes:
            memory[second + offset:second + offset + len(code)] = encode(code)
        false_base = BASE + second
    return FakeProcess(memory), probes, false_base


class JapaneseRdramAmbiguityTests(unittest.TestCase):
    def test_rom_copy_rejected_big_endian(self):
        process, probes, decoy = build_case('big')
        _, base, endian = discover_japanese_mupen_rdram(
            process, probes, max_scan_mb=40)
        self.assertEqual((base, endian), (BASE, 'big'))
        with self.assertRaisesRegex(RuntimeError, 'Manual base'):
            discover_japanese_mupen_rdram(process, probes, base_hint=decoy)

    def test_rom_copy_rejected_word_swapped(self):
        process, probes, decoy = build_case('wordswapped')
        reader, base, endian = discover_japanese_mupen_rdram(
            process, probes, max_scan_mb=40)
        self.assertEqual((base, endian), (BASE, 'wordswapped'))
        self.assertEqual(reader.read_guest(0x80000450, 64), probes[0][1])
        with self.assertRaisesRegex(RuntimeError, 'Manual base'):
            discover_japanese_mupen_rdram(process, probes, base_hint=decoy)

    def test_two_valid_ram_copies_report_revalidatable_candidates(self):
        process, probes, second = build_case(
            'wordswapped', with_rom_copy=False, with_second_rdram=True)
        with self.assertRaises(AmbiguousJapaneseRdram) as caught:
            discover_japanese_mupen_rdram(process, probes, max_scan_mb=40)
        self.assertEqual(caught.exception.candidates,
                         ((BASE, 'wordswapped'), (second, 'wordswapped')))
        self.assertIn(f'0x{second:X}', str(caught.exception))
        _, base, endian = discover_japanese_mupen_rdram(
            process, probes, base_hint=second)
        self.assertEqual((base, endian), (second, 'wordswapped'))


if __name__ == '__main__':
    unittest.main()
