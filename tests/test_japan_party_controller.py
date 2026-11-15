"""No-process tests for the Japan party write controller's explicit safeguards."""
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from autosplitter.memory import Rdram
from practice.toolkit import Toolkit
from practice.japanese_party_unlock import CHARACTER_INDEX_ADDR
from tests.test_japanese_party_unlock import Process


class Label:
    def __init__(self):
        self.value = ""

    def set(self, value):
        self.value = value


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

    # Intentionally no write method.


def controller(writer, *, opt_in=True, read_only=False, backend='mupen64plus'):
    status = Label()
    party = Label()
    screen = SimpleNamespace(
        active_version=SimpleNamespace(key="japan"),
        _connecting=False,
        args=SimpleNamespace(read_only=read_only, enable_japan_party_writes=opt_in),
        jp_rdram=Rdram(Reader(writer), 0, "wordswapped"),
        game_pid=959604,
        jp_backend=backend,
        connection_target=SimpleNamespace(get=lambda: backend),
        verified_rom_path="verified-rom.n64",
        jp_party_result=party,
        status=status,
        root=None,
        refresh_japan_fields=lambda force=False: None,
    )
    return screen


class JapanesePartyControllerTests(unittest.TestCase):
    def test_no_opt_in_does_not_open_writable_handle(self):
        screen = controller(Writer(), opt_in=False)
        with patch("practice.toolkit.HostProcess") as host:
            Toolkit.enable_japan_party(screen, 2)
        host.assert_not_called()
        self.assertIn("unavailable", screen.jp_party_result.value)

    def test_read_only_overrides_opt_in(self):
        screen = controller(Writer(), read_only=True)
        with patch("practice.toolkit.HostProcess") as host:
            Toolkit.enable_japan_party(screen, 2)
        host.assert_not_called()

    def test_consent_denied_never_opens_handle(self):
        screen = controller(Writer())
        with patch("practice.toolkit.messagebox.askyesno", return_value=False), \
             patch("practice.toolkit.HostProcess") as host:
            Toolkit.enable_japan_party(screen, 3)
        host.assert_not_called()
        self.assertIn("cancelled", screen.jp_party_result.value)

    def test_pid_mismatch_prevents_write_and_closes_nothing(self):
        writer = Writer()
        screen = controller(writer)
        with patch("practice.toolkit.messagebox.askyesno", return_value=True), \
             patch("practice.toolkit.verified_emulator_pid", return_value=(111, "mupen64plus")), \
             patch("practice.toolkit.HostProcess") as host:
            Toolkit.enable_japan_party(screen, 2)
        host.assert_not_called()
        self.assertEqual(writer.writes, [])
        self.assertIn("rejected", screen.jp_party_result.value)

    def test_success_opens_one_short_lived_writer_and_preserves_index(self):
        writer = Writer()
        screen = controller(writer)
        guest_writer = writer.rdram()
        with patch("practice.toolkit.messagebox.askyesno", return_value=True), \
             patch("practice.toolkit.verified_emulator_pid", return_value=(959604, "mupen64plus")), \
             patch("practice.toolkit.verified_japan_probes", return_value=("verified",)), \
             patch("practice.toolkit.HostProcess", return_value=writer) as host, \
             patch("practice.toolkit.validate_rdram_base", return_value=guest_writer) as validate:
            Toolkit.enable_japan_party(screen, 2)
        host.assert_called_once_with(959604, writable=True)
        validate.assert_called_once()
        self.assertEqual(validate.call_args.kwargs['allow_4mb'], False)
        self.assertEqual(writer.close_count, 1)
        self.assertEqual(guest_writer.read_guest(0x80161E97, 1), b"\x01")
        self.assertEqual(guest_writer.read_guest(CHARACTER_INDEX_ADDR, 4), bytes(4))
        self.assertEqual(len(writer.writes), 1)
        self.assertIn("Sasuke party flag set", screen.status.value)


    def test_project64_win32_one_shot_write_revalidates_four_megabyte_mode(self):
        writer = Writer()
        screen = controller(writer, backend='project64')
        guest_writer = writer.rdram()
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.messagebox.askyesno', return_value=True), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(959604, 'project64')) as verify_pid, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=('verified',)), \
             patch('practice.toolkit.HostProcess', return_value=writer) as host, \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=guest_writer) as validate:
            Toolkit.enable_japan_party(screen, 3)
        verify_pid.assert_called_once_with(959604, 'project64')
        host.assert_called_once_with(959604, writable=True)
        self.assertEqual(validate.call_args.kwargs['allow_4mb'], True)
        self.assertEqual(guest_writer.read_guest(0x80161E9B, 1), b'\\x01')
        self.assertEqual(len(writer.writes), 1)
        self.assertEqual(writer.close_count, 1)

    def test_project64_rejects_non_windows_without_opening_writer(self):
        writer = Writer()
        screen = controller(writer, backend='project64')
        with patch('practice.toolkit.sys.platform', 'linux'), \
             patch('practice.toolkit.messagebox.askyesno', return_value=True), \
             patch('practice.toolkit.HostProcess') as host:
            Toolkit.enable_japan_party(screen, 2)
        host.assert_not_called()
        self.assertEqual(writer.writes, [])



if __name__ == "__main__":
    unittest.main()
