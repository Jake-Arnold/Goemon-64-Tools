"""Japan-0 raw freeze enforcement: no USA pointers or Tk worker calls."""
import unittest
from types import SimpleNamespace

from practice.japan_value_freezes import RegionalValueFreezes, stable_japan_gameplay
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
)


class Memory:
    def __init__(self):
        self.values = {
            JAPAN_DEBUG_ENGINE_MODE: b'\x0d',
            JAPAN_DEBUG_SCENE: bytes.fromhex('0161'),
            JAPAN_DEBUG_CHARACTER: bytes(4),
            JAPAN_DEBUG_LOADING: bytes(4),
            0x80161EC8: bytes.fromhex('00000001'),
        }
        self.writes = []
    def read_guest(self, address, width):
        if address in self.values:
            value = self.values[address]
            if len(value) != width:
                raise ValueError('Wrong test width')
            return value
        return bytes(width)
    def write_guest(self, address, value):
        self.writes.append((address, value))
        self.values[address] = value


class Host:
    def __init__(self):
        self.closed = False
    def close(self):
        self.closed = True


class JapanFreezeTests(unittest.TestCase):
    def setUp(self):
        self.ram = Memory()
        self.hosts = []
        self.opens = 0
        def open_writer(reader, token):
            self.assertIs(reader, self.ram)
            self.assertEqual(token, ('japan', 123, id(reader)))
            self.opens += 1
            host = Host()
            self.hosts.append(host)
            return host, self.ram
        self.freezes = RegionalValueFreezes(open_writer)
        self.token = ('japan', 123, id(self.ram))

    def test_freeze_corrects_one_byte_when_changed(self):
        address = 0x80161EC8
        self.freezes.add(self.token, address, bytes.fromhex('00000001'))
        self.assertIn('Active:', self.freezes.poll(self.ram, self.token, writable=True))
        self.assertEqual(self.opens, 0)
        self.ram.values[address] = bytes.fromhex('00000002')
        self.assertIn('Active:', self.freezes.poll(self.ram, self.token, writable=True))
        self.assertEqual(self.ram.values[address], bytes.fromhex('00000001'))
        self.assertEqual(self.opens, 1)
        self.assertTrue(self.hosts[0].closed)

    def test_pause_during_load_does_not_write_then_resume(self):
        address = 0x80161EC8
        self.freezes.add(self.token, address, b'\x00\x00\x00\x03')
        self.ram.values[JAPAN_DEBUG_LOADING] = (1).to_bytes(4, 'big')
        self.assertIn('paused', self.freezes.poll(self.ram, self.token, writable=True))
        self.assertEqual(self.opens, 0)
        self.ram.values[JAPAN_DEBUG_LOADING] = bytes(4)
        self.assertIn('Active:', self.freezes.poll(self.ram, self.token, writable=True))
        self.assertEqual(self.ram.values[address], b'\x00\x00\x00\x03')

    def test_token_change_and_readonly_stop_locks(self):
        self.freezes.add(self.token, 0x80161EC8, b'\x01\x02\x03\x04')
        self.assertIn('stopped', self.freezes.poll(
            self.ram, ('japan', 124, id(self.ram)), writable=True).lower())
        self.assertFalse(self.freezes.active())
        self.freezes.add(self.token, 0x80161EC8, b'\x01\x02\x03\x04')
        self.assertIn('stopped', self.freezes.poll(
            self.ram, self.token, writable=False).lower())
        self.assertFalse(self.freezes.active())
        self.assertEqual(self.opens, 0)

    def test_stable_context_verifies_all_four_japanese_fields(self):
        self.assertEqual(stable_japan_gameplay(self.ram), (13, 0x161, 0, 0))
        self.ram.values[JAPAN_DEBUG_ENGINE_MODE] = bytes((10,))
        self.assertIsNone(stable_japan_gameplay(self.ram))

    def test_usa_only_auto_features_refused_on_japan(self):
        self.freezes.add(self.token, 0x80161EC8, b'\x01')
        self.freezes.enable_health(self.token)
        self.assertIn('USA-only', self.freezes.poll(
            self.ram, self.token, writable=True))
        self.assertFalse(self.freezes.active())
        self.assertEqual(self.opens, 0)

    def test_writer_failure_stops_without_retrying_stale_process(self):
        address=0x80161EC8
        self.freezes.add(self.token, address, b'\x00\x00\x00\x07')
        def failing(reader, token):
            raise PermissionError('process write access denied')
        self.freezes._open_japan_writer = failing
        self.assertIn('access denied', self.freezes.poll(
            self.ram, self.token, writable=True))
        self.assertFalse(self.freezes.active())

    def test_overlap_bounds_and_unfreeze_share_existing_lock_book(self):
        self.freezes.add(self.token, 0x80161EC8, b'\x01\x02')
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            self.freezes.add(self.token, 0x80161EC9, b'\x01')
        self.assertIsNotNone(self.freezes.get(0x80161EC8))
        self.freezes.remove(0x80161EC8)
        self.assertFalse(self.freezes.active())


if __name__ == '__main__':
    unittest.main()
