"""Experimental Japanese Live Memory byte edits; synthetic Project64/Mupen RAM."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from tests.test_japan_party_controller import Writer, Reader
from autosplitter.memory import Rdram


def editor(writer, *, read_only=False):
    return SimpleNamespace(
        active_version=SimpleNamespace(key='japan'),
        _connecting=False,
        args=SimpleNamespace(read_only=read_only),
        jp_rdram=Rdram(Reader(writer), 0, 'wordswapped'),
        game_pid=959604,
        jp_backend='project64',
        connection_target=SimpleNamespace(get=lambda: 'project64'),
    )


class JapanLiveEditTests(unittest.TestCase):
    def test_arbitrary_japanese_addresses_write_one_two_and_four_bytes(self):
        for width, address, value in (
            (1, 0x80161E97, bytes((1,))),
            (2, 0x80161DDA, bytes.fromhex('00AF')),
            (4, 0x80151B10, bytes.fromhex('C3908000')),
        ):
            with self.subTest(width=width):
                writer = Writer()
                screen = editor(writer)
                expected = writer.rdram().read_guest(address, width)
                with patch('practice.toolkit.HostProcess', return_value=writer):
                    changed = Toolkit.write_japan_raw_bytes(
                        screen, address, value, expected=expected)
                self.assertTrue(changed)
                self.assertEqual(writer.rdram().read_guest(address, width),
                                 value)
                self.assertEqual(writer.close_count, 1)

    def test_stale_expected_value_rejected_without_write(self):
        writer = Writer()
        screen = editor(writer)
        with patch('practice.toolkit.HostProcess', return_value=writer):
            with self.assertRaisesRegex(RuntimeError, 'changed'):
                Toolkit.write_japan_raw_bytes(
                    screen, 0x80161EEF, bytes((1,)),
                    expected=bytes((3,)))
        self.assertEqual(writer.writes, [])
        self.assertEqual(writer.close_count, 1)

    def test_read_only_blocks_before_opening_host(self):
        screen = editor(Writer(), read_only=True)
        with patch('practice.toolkit.HostProcess') as host:
            with self.assertRaisesRegex(RuntimeError, 'write'):
                Toolkit.write_japan_raw_bytes(
                    screen, 0x80161EEF, bytes((1,)))
            host.assert_not_called()

    def test_unknown_guest_address_is_allowed_in_live_editor(self):
        writer = Writer()
        screen = editor(writer)
        address = 0x80161DBF
        before = writer.rdram().read_guest(address, 1)
        with patch('practice.toolkit.HostProcess', return_value=writer):
            self.assertTrue(Toolkit.write_japan_raw_bytes(
                screen, address, bytes((0x80,)), expected=before))
        self.assertEqual(writer.rdram().read_guest(address, 1), bytes((0x80,)))


if __name__ == '__main__':
    unittest.main()
