"""Synthetic, read-only RDRAM tests for numeric searches. No game required."""
import struct
import unittest

from practice.value_search import ValueScanner, encode_value, read_ram, GUEST_BASE


class Memory:
    def __init__(self, n=64):
        self.data = bytearray(n)
        self.reads = 0
        self.writes = 0
        self.partial = False

    def read_guest(self, addr, width):
        self.reads += 1
        offset = addr - GUEST_BASE
        if offset < 0 or offset + width > len(self.data):
            raise OSError('out of bounds')
        if self.partial:
            return bytes(self.data[offset:offset + width - 1])
        return bytes(self.data[offset:offset + width])

    def put(self, offset, kind, value):
        if kind == 'f32':
            data = struct.pack('>f', value)
        else:
            data = encode_value(kind, str(value))
        self.data[offset:offset + len(data)] = data


class ValueSearchTests(unittest.TestCase):
    def test_exact_value_and_narrowing_to_one_address(self):
        ram = Memory()
        for offset in (8, 24, 40):
            ram.put(offset, 'u16', 950)
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_exact(ram, 'u16', '950'), 3)
        ram.put(8, 'u16', 920)
        ram.put(24, 'u16', 920)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 2)
        ram.put(24, 'u16', 890)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 24)
        self.assertEqual(scanner.rows()[0]['value'], '890')
        self.assertEqual(ram.writes, 0)

    def test_unknown_enemy_hp_decreases_and_then_stays(self):
        ram = Memory()
        ram.put(12, 'u32', 300)
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_unknown(ram, 'u32'), 16)
        ram.put(12, 'u32', 200)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 1)
        self.assertEqual(scanner.filter(ram, 'Unchanged'), 1)
        ram.put(12, 'u32', 0)
        self.assertEqual(scanner.filter(ram, 'Exact', '0'), 1)
        self.assertEqual(scanner.rows()[0]['hex'], '0x00000000')

    def test_changed_and_increased_8bit(self):
        ram = Memory()
        scanner = ValueScanner(size=64, chunk=16)
        scanner.start_unknown(ram, 'u8')
        ram.put(4, 'u8', 1)
        ram.put(13, 'u8', 1)
        self.assertEqual(scanner.filter(ram, 'Changed'), 2)
        ram.put(13, 'u8', 2)
        self.assertEqual(scanner.filter(ram, 'Increased'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 13)

    def test_signed_and_float_values_big_endian(self):
        ram = Memory()
        ram.put(8, 's16', -12)
        ram.put(16, 'f32', 7.5)
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_exact(ram, 's16', '-12'), 1)
        self.assertEqual(scanner.rows()[0]['hex'], '0xFFF4')
        self.assertEqual(scanner.start_exact(ram, 'f32', '7.5'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 16)
        ram.put(16, 'f32', 4.5)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 1)
        with self.assertRaises(ValueError):
            encode_value('f32', 'nan')
        with self.assertRaises(ValueError):
            encode_value('u8', '256')

    def test_alignment_avoids_partial_matches(self):
        ram = Memory()
        ram.put(3, 'u16', 500)
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_exact(ram, 'u16', '500'), 0)
        ram.put(4, 'u16', 500)
        self.assertEqual(scanner.start_exact(ram, 'u16', '500'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 4)

    def test_optional_unaligned_search(self):
        ram = Memory()
        ram.put(3, 'u16', 500)
        scanner = ValueScanner(size=64, chunk=16, aligned=False)
        self.assertEqual(scanner.start_exact(ram, 'u16', '500'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 3)

    def test_failed_reads_keep_previous_search(self):
        ram = Memory()
        ram.put(8, 'u32', 77)
        scanner = ValueScanner(size=64, chunk=16)
        scanner.start_exact(ram, 'u32', '77')
        ram.partial = True
        with self.assertRaises(OSError):
            scanner.filter(ram, 'Changed')
        self.assertEqual(scanner.count, 1)
        self.assertEqual(scanner.samples, 1)
        self.assertEqual(scanner.rows()[0]['value'], '77')
        with self.assertRaises(OSError):
            scanner.start_unknown(ram, 'u8')
        self.assertEqual(scanner.kind, 'u32')

    def test_bounded_candidate_storage_and_live_preview(self):
        ram = Memory()
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_exact(ram, 'u8', '0'), 64)
        self.assertIsInstance(scanner.active, bytearray)
        self.assertEqual(len(scanner.rows(limit=5)), 5)
        ram.put(0, 'u8', 3)
        self.assertEqual(scanner.rows(limit=1)[0]['value'], '0')
        self.assertEqual(scanner.rows(limit=1, ram=ram)[0]['value'], '3')


    def test_filter_can_compare_with_immutable_initial_snapshot(self):
        ram = Memory()
        ram.put(8, 'u16', 100)
        scanner = ValueScanner(size=64, chunk=16)
        scanner.start_unknown(ram, 'u16')
        ram.put(8, 'u16', 90)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 1)
        self.assertEqual(scanner.rows()[0]['initial'], '100')
        self.assertEqual(scanner.rows()[0]['previous'], '90')
        ram.put(8, 'u16', 95)
        self.assertEqual(
            scanner.filter(ram, 'Decreased', compare_to='Initial'), 1)
        self.assertEqual(scanner.rows()[0]['value'], '95')
        ram.put(8, 'u16', 96)
        self.assertEqual(scanner.filter(ram, 'Decreased'), 0)

    def test_exact_filter_uses_new_number_not_original_scan(self):
        ram = Memory()
        ram.put(8, 'u16', 950)
        scanner = ValueScanner(size=64, chunk=16)
        scanner.start_exact(ram, 'u16', '950')
        ram.put(8, 'u16', 900)
        self.assertEqual(scanner.filter(ram, 'Exact', '900'), 1)
        self.assertEqual(scanner.rows()[0]['initial'], '950')

    def test_f64_big_endian_search_and_live_read(self):
        ram = Memory()
        ram.data[16:24] = struct.pack('>d', 7.25)
        scanner = ValueScanner(size=64, chunk=16)
        self.assertEqual(scanner.start_exact(ram, 'f64', '7.25'), 1)
        self.assertEqual(scanner.rows()[0]['value'], '7.25')
        ram.data[16:24] = struct.pack('>d', 8.5)
        self.assertEqual(scanner.filter(ram, 'Increased'), 1)
        self.assertEqual(scanner.rows()[0]['initial'], '7.25')

    def test_text_search_encodings_and_research_limitations(self):
        ram = Memory(128)
        ram.data[3:9] = b'GOEMON'
        scanner = ValueScanner(size=128, chunk=16)
        self.assertEqual(scanner.start_text(ram, 'GOEMON'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 3)
        self.assertEqual(scanner.rows()[0]['kind'], 'text/ASCII')
        ram.data[3:9] = b'GOLMON'
        self.assertEqual(scanner.filter(ram, 'Changed'), 1)
        self.assertEqual(scanner.filter(ram, 'Exact', 'GOLMON'), 1)
        with self.assertRaises(ValueError):
            scanner.filter(ram, 'Increased')
        with self.assertRaises(ValueError):
            scanner.filter(ram, 'Exact', 'different length')
        self.assertEqual(scanner.count, 1)  # Errors do not discard results.
        raw_japanese = 'ゴエモン'.encode('shift_jis')
        ram.data[20:20 + len(raw_japanese)] = raw_japanese
        self.assertEqual(scanner.start_text(
            ram, 'ゴエモン', encoding='Shift-JIS'), 1)
        self.assertEqual(scanner.rows()[0]['value'], 'ゴエモン')
        with self.assertRaises(ValueError):
            scanner.start_text(ram, 'ゴエモン', encoding='ASCII')

    def test_numeric_alignment_after_text_and_batched_live_reads(self):
        ram = Memory(128)
        ram.data[3:9] = b'GOEMON'
        scanner = ValueScanner(size=128, chunk=16)
        scanner.start_text(ram, 'GOEMON')
        ram.put(16, 'u16', 950)
        self.assertEqual(scanner.start_exact(ram, 'u16', '950'), 1)
        self.assertEqual(scanner.rows()[0]['address'], GUEST_BASE + 16)
        scanner.start_unknown(ram, 'u8')
        before = ram.reads
        rows = scanner.rows(limit=20, ram=ram)
        self.assertEqual(len(rows), 20)
        self.assertEqual(ram.reads, before + 1)
        self.assertEqual(rows[0]['initial'], rows[0]['previous'])

    def test_chunk_validation(self):
        ram = Memory()
        self.assertEqual(read_ram(ram, size=64, chunk=16), bytes(64))
        with self.assertRaises(ValueError):
            read_ram(ram, size=64, chunk=7)


if __name__ == '__main__':
    unittest.main()
