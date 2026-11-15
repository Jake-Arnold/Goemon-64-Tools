"""Japanese native debug menu controller: test consent/PID/ROM/one-byte only."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from autosplitter.memory import Rdram
from practice.toolkit import Toolkit
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
    JAPAN_DEBUG_LOADING, JAPAN_DEBUG_SUBMODE, JAPAN_DEBUG_EXIT,
)
from tests.test_japan_party_controller import Writer, Reader, Label


def screen(writer, *, opt_in=True, read_only=False, backend='project64',
           scene=0x161, state=13):
    for addr, data in (
        (JAPAN_DEBUG_ENGINE_MODE, bytes([state])),
        (JAPAN_DEBUG_SCENE, scene.to_bytes(2, 'big')),
        (JAPAN_DEBUG_CHARACTER, bytes(4)),
        (JAPAN_DEBUG_LOADING, bytes(4)),
        (JAPAN_DEBUG_SUBMODE, bytes([2])),
        (JAPAN_DEBUG_EXIT, bytes([0])),
    ):
        writer.set_guest(addr, data)
    writer.writes.clear()
    return SimpleNamespace(
        active_version=SimpleNamespace(key='japan'),
        _connecting=False,
        args=SimpleNamespace(
            read_only=read_only, enable_japan_debug_menu_writes=opt_in),
        jp_rdram=Rdram(Reader(writer), 0, 'wordswapped'),
        jp_backend=backend, game_pid=959604,
        connection_target=SimpleNamespace(get=lambda: backend),
        verified_rom_path='verified-japan-rom.n64',
        jp_debug_result=Label(), status=Label(), root=None,
        selected_japan_debug_scene=lambda: 0x161,
        refresh_japan_fields=lambda force=False: None,
    )


class JapaneseDebugMenuControllerTests(unittest.TestCase):
    def test_missing_opt_in_or_readonly_never_opens_writer(self):
        for options in (dict(opt_in=False), dict(read_only=True)):
            s = screen(Writer(), **options)
            with patch('practice.toolkit.HostProcess') as handle:
                Toolkit.open_japan_debug_for_selected_scene(s)
            handle.assert_not_called()
            self.assertIn('requires', s.jp_debug_result.value)

    def test_user_cancels_before_opening_writer(self):
        s = screen(Writer())
        with patch('practice.toolkit.messagebox.askyesno', return_value=False), \
             patch('practice.toolkit.HostProcess') as handle:
            Toolkit.open_japan_debug_for_selected_scene(s)
        handle.assert_not_called()
        self.assertIn('cancelled', s.jp_debug_result.value)

    def test_verified_project64_writes_only_native_engine_mode(self):
        writer = Writer()
        s = screen(writer)
        writable = writer.rdram()
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.messagebox.askyesno', return_value=True), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(959604, 'project64')), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=('verified',)), \
             patch('practice.toolkit.HostProcess', return_value=writer) as handle, \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=writable) as validate:
            Toolkit.open_japan_debug_for_selected_scene(s)
        handle.assert_called_once_with(959604, writable=True)
        self.assertTrue(validate.call_args.kwargs['allow_4mb'])
        self.assertEqual(writer.close_count, 1)
        self.assertEqual(writable.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0a')
        self.assertEqual(writable.read_guest(JAPAN_DEBUG_SCENE, 2),
                         bytes.fromhex('0161'))
        self.assertEqual(len(writer.writes), 1)
        self.assertEqual(len(writer.writes[0][1]), 4)
        self.assertIn('menu', s.status.value.lower())
        self.assertIn('MACHI / index 3', s.status.value)

    def test_pid_mismatch_and_unstable_game_refuse(self):
        for unstable in (False, True):
            writer = Writer()
            s = screen(writer, state=10 if unstable else 13)
            with patch('practice.toolkit.sys.platform', 'win32'), \
                 patch('practice.toolkit.messagebox.askyesno',
                       return_value=True), \
                 patch('practice.toolkit.verified_emulator_pid',
                       return_value=(123, 'project64')), \
                 patch('practice.toolkit.HostProcess') as handle:
                Toolkit.open_japan_debug_for_selected_scene(s)
            handle.assert_not_called()
            self.assertEqual(writer.writes, [])


if __name__ == '__main__':
    unittest.main()
