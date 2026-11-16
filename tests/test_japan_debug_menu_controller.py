"""Japanese original debug menu: 0x0A state write, no gameplay guards."""
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


def click_menu(screen_obj, writer, *, pid=959604):
    """Run controller through its real region/PID/code/memory validations."""
    with patch('practice.toolkit.sys.platform', 'win32'), \
         patch('practice.toolkit.messagebox.askyesno') as dialog, \
         patch('practice.toolkit.verified_emulator_pid',
               return_value=(pid, screen_obj.jp_backend)) as verify_pid, \
         patch('practice.toolkit.verified_japan_probes',
               return_value=('verified',)) as probes, \
         patch('practice.toolkit.HostProcess', return_value=writer) as host, \
         patch('practice.toolkit.validate_rdram_base',
               return_value=writer.rdram()) as validate:
        Toolkit.open_japan_debug_for_selected_scene(screen_obj)
    dialog.assert_not_called()
    return host, verify_pid, probes, validate


class JapaneseDebugMenuControllerTests(unittest.TestCase):
    def test_readonly_and_disconnected_never_open_writer(self):
        for read_only in (True,):
            s = screen(Writer(), read_only=read_only)
            with patch('practice.toolkit.HostProcess') as host:
                Toolkit.open_japan_debug_for_selected_scene(s)
            host.assert_not_called()
            self.assertIn('writes enabled', s.jp_debug_result.value)
        s = screen(Writer())
        s.jp_rdram = None
        with patch('practice.toolkit.HostProcess') as host:
            Toolkit.open_japan_debug_for_selected_scene(s)
        host.assert_not_called()

    def test_any_state_cutscene_character_loading_and_old_optin_are_ignored(self):
        for state in (0, 10, 12, 13, 255):
            with self.subTest(state=state):
                writer = Writer()
                s = screen(writer, state=state, opt_in=False)
                writer.set_guest(JAPAN_DEBUG_CHARACTER, (99).to_bytes(4, 'big'))
                writer.set_guest(JAPAN_DEBUG_LOADING, (1).to_bytes(4, 'big'))
                writer.set_guest(JAPAN_DEBUG_SUBMODE, b'\x06')
                writer.writes.clear()
                original_scene = writer.rdram().read_guest(JAPAN_DEBUG_SCENE, 2)
                host, pid, probes, validate = click_menu(s, writer)
                host.assert_called_once_with(959604, writable=True)
                pid.assert_called_once_with(959604, 'project64')
                probes.assert_called_once_with('verified-japan-rom.n64')
                self.assertTrue(validate.call_args.kwargs['allow_4mb'])
                self.assertEqual(
                    writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1),
                    b'\x0a')
                self.assertEqual(len(writer.writes), 0 if state == 10 else 1)
                self.assertEqual(writer.rdram().read_guest(JAPAN_DEBUG_SCENE, 2),
                                 original_scene)
                self.assertEqual(writer.rdram().read_guest(
                    JAPAN_DEBUG_CHARACTER, 4), (99).to_bytes(4, 'big'))
                self.assertEqual(writer.rdram().read_guest(
                    JAPAN_DEBUG_LOADING, 4), (1).to_bytes(4, 'big'))
                self.assertIn('no RAM write' if state == 10 else 'only',
                              s.status.value)
                self.assertEqual(writer.close_count, 1)

    def test_auto_backend_is_valid_for_an_already_verified_connection(self):
        writer = Writer()
        s = screen(writer, state=12)
        s.connection_target = SimpleNamespace(get=lambda: 'auto')
        click_menu(s, writer)
        self.assertEqual(len(writer.writes), 1)

    def test_process_identity_mismatch_rejects_without_write(self):
        writer = Writer()
        s = screen(writer, state=12)
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(123, 'project64')), \
             patch('practice.toolkit.HostProcess') as handle:
            Toolkit.open_japan_debug_for_selected_scene(s)
        handle.assert_not_called()
        self.assertEqual(writer.writes, [])

    def test_native_recomp_does_not_require_initialized_gameplay_character(self):
        writer = Writer()
        s = screen(writer, backend='recomp', state=13)
        writer.set_guest(JAPAN_DEBUG_CHARACTER, (0xFFFFFFFF).to_bytes(4, 'big'))
        writer.writes.clear()
        with patch('practice.toolkit.verified_japan_recomp_pid',
                   return_value=(959604, 'recomp')) as pid, \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=('verified',)), \
             patch('practice.toolkit.HostProcess', return_value=writer), \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=writer.rdram()) as validate, \
             patch('practice.toolkit.validate_japan_recomp_writer') as strict:
            Toolkit.open_japan_debug_for_selected_scene(s)
        pid.assert_called_once_with(959604)
        self.assertFalse(validate.call_args.kwargs['allow_4mb'])
        strict.assert_not_called()
        self.assertEqual(writer.rdram().read_guest(
            JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0a')
        self.assertEqual(len(writer.writes), 1)


if __name__ == '__main__':
    unittest.main()
