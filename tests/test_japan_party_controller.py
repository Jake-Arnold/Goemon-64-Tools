"""Direct mapped Japanese Unlocks controller tests without emulator access."""
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from autosplitter.memory import Rdram
from practice.toolkit import Toolkit
from practice.unlocks import UNLOCKS
from practice.region_unlocks import japan_unlock_all_targets
from practice.japanese_party_unlock import CHARACTER_INDEX_ADDR
from tests.test_japanese_party_unlock import Process


class Writer(Process):
    def __init__(self):
        super().__init__("wordswapped", writable=True)
        self.close_count = 0

    def close(self):
        self.close_count += 1


class Reader:
    def __init__(self, writer):
        self.writer = writer

    def read(self, address, length):
        return self.writer.read(address, length)


def controller(writer, *, read_only=False, backend='mupen64plus'):
    return SimpleNamespace(
        active_version=SimpleNamespace(key='japan'),
        _connecting=False,
        args=SimpleNamespace(read_only=read_only),
        jp_rdram=Rdram(Reader(writer), 0, 'wordswapped'),
        game_pid=959604,
        jp_backend=backend,
        connection_target=SimpleNamespace(get=lambda: backend),
    )


def unlock(label):
    return next(x for x in UNLOCKS if x.label == label)


class JapanesePartyControllerTests(unittest.TestCase):
    def test_no_opt_in_or_dialog_for_sasuke_and_yae_on_off(self):
        writer = Writer()
        screen = controller(writer)
        sasuke = unlock('Sasuke in party')
        yae = unlock('Yae in party')
        with patch('practice.toolkit.HostProcess', return_value=writer) as host, \
             patch('practice.toolkit.messagebox.askyesno') as consent:
            self.assertEqual(Toolkit.apply_japan_unlocks(
                screen, ((sasuke, 1), (yae, 1))), (2, 2))
            self.assertEqual(writer.rdram().read_guest(0x80161E97, 1), bytes((1,)))
            self.assertEqual(writer.rdram().read_guest(0x80161E9B, 1), bytes((1,)))
            self.assertEqual(Toolkit.apply_japan_unlocks(
                screen, ((sasuke, 0), (yae, 0))), (2, 2))
        host.assert_called_with(959604, writable=True)
        consent.assert_not_called()
        self.assertEqual(writer.rdram().read_guest(0x80161E97, 1), bytes((0,)))
        self.assertEqual(writer.rdram().read_guest(0x80161E9B, 1), bytes((0,)))
        self.assertEqual(writer.rdram().read_guest(CHARACTER_INDEX_ADDR, 4), bytes(4))
        self.assertEqual(writer.close_count, 2)

    def test_direct_triton_shell_cucumber_and_fish_count(self):
        writer = Writer()
        screen = controller(writer, backend='project64')
        changes = (
            (unlock('Triton Shell'), 1),
            (unlock('Cucumber'), 1),
            (unlock('Blue fish count'), 3),
        )
        with patch('practice.toolkit.HostProcess', return_value=writer) as host:
            self.assertEqual(Toolkit.apply_japan_unlocks(screen, changes), (3, 3))
        host.assert_called_once_with(959604, writable=True)
        self.assertEqual(writer.rdram().read_guest(0x80161EEF, 1), bytes((1,)))
        self.assertEqual(writer.rdram().read_guest(0x80161F07, 1), bytes((1,)))
        self.assertEqual(writer.rdram().read_guest(0x80161F13, 1), bytes((3,)))

    def test_unlock_all_opens_one_process_and_never_writes_unknown(self):
        writer = Writer()
        screen = controller(writer)
        targets = japan_unlock_all_targets()
        self.assertEqual(len(targets), 9)
        with patch('practice.toolkit.HostProcess', return_value=writer) as host:
            changed, total = Toolkit.apply_japan_unlocks(screen, targets)
        self.assertEqual((changed, total), (9, 9))
        host.assert_called_once_with(959604, writable=True)
        self.assertEqual(writer.close_count, 1)
        self.assertEqual(writer.rdram().read_guest(0x80161F0B, 1), bytes((8,)))
        self.assertEqual(writer.rdram().read_guest(0x80161F0F, 1), bytes((5,)))
        self.assertEqual(writer.rdram().read_guest(0x80161F13, 1), bytes((3,)))
        self.assertEqual(len(writer.writes), 9)

    def test_unknown_row_rejected_before_opening_host(self):
        writer = Writer()
        screen = controller(writer)
        with patch('practice.toolkit.HostProcess') as host:
            with self.assertRaisesRegex(ValueError, 'unknown'):
                Toolkit.apply_japan_unlocks(
                    screen, ((unlock('Goemon in party'), 1),))
        host.assert_not_called()
        self.assertEqual(writer.writes, [])

    def test_explicit_read_only_blocks_writes(self):
        writer = Writer()
        screen = controller(writer, read_only=True)
        with patch('practice.toolkit.HostProcess') as host:
            with self.assertRaisesRegex(RuntimeError, 'write-enabled'):
                Toolkit.apply_japan_unlocks(
                    screen, ((unlock('Sasuke in party'), 1),))
        host.assert_not_called()
        self.assertEqual(writer.writes, [])

    def test_wrong_backend_rejected_before_write(self):
        writer = Writer()
        screen = controller(writer)
        screen.connection_target = SimpleNamespace(get=lambda: 'project64')
        with patch('practice.toolkit.HostProcess') as host:
            with self.assertRaisesRegex(RuntimeError, 'Connect Japanese'):
                Toolkit.apply_japan_unlocks(
                    screen, ((unlock('Sasuke in party'), 1),))
        host.assert_not_called()


if __name__ == '__main__':
    unittest.main()
