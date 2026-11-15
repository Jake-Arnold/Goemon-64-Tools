"""Japanese XYZ controller host/write isolation; no real Project64 process."""
import struct
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from autosplitter.memory import Rdram
from practice.toolkit import Toolkit
from practice.japanese_position import (
    JAPAN_PLAYER_XYZ_START, JAPAN_SCENE_INDEX, JAPAN_CHARACTER_INDEX,
    JAPAN_OEDO_SOUTH_ENTRANCE,
)
from tests.test_japan_party_controller import Writer, Reader, Label


class Field:
    def __init__(self, value):
        self.value = str(value)
    def get(self):
        return self.value


def fake_controller(writer, *, opt_in=True, read_only=False,
                    backend='project64', scene=0x161, character=0):
    writer.set_guest(JAPAN_SCENE_INDEX, scene.to_bytes(2, 'big'))
    writer.set_guest(JAPAN_CHARACTER_INDEX, character.to_bytes(4, 'big'))
    writer.set_guest(JAPAN_PLAYER_XYZ_START,
                     struct.pack('>fff', -174.5, 0.0, -142.0))
    writer.writes.clear()
    screen = SimpleNamespace(
        active_version=SimpleNamespace(key='japan'),
        _connecting=False,
        args=SimpleNamespace(
            read_only=read_only,
            enable_japan_position_writes=opt_in),
        jp_rdram=Rdram(Reader(writer), 0, 'wordswapped'),
        jp_backend=backend,
        game_pid=959604,
        connection_target=SimpleNamespace(get=lambda: backend),
        verified_rom_path='verified-japan-rom.n64',
        jp_pos_x=Field(JAPAN_OEDO_SOUTH_ENTRANCE[0]),
        jp_pos_y=Field(JAPAN_OEDO_SOUTH_ENTRANCE[1]),
        jp_pos_z=Field(JAPAN_OEDO_SOUTH_ENTRANCE[2]),
        jp_position_result=Label(),
        status=Label(),
        root=None,
        refresh_japan_position=lambda: None,
    )
    return screen


class JapanPositionControllerTests(unittest.TestCase):
    def test_missing_opt_in_does_not_open_host_writer(self):
        screen = fake_controller(Writer(), opt_in=False)
        with patch('practice.toolkit.HostProcess') as host:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_not_called()
        self.assertIn('require a verified connection', screen.jp_position_result.value)

    def test_read_only_overrides_flag(self):
        screen = fake_controller(Writer(), read_only=True)
        with patch('practice.toolkit.HostProcess') as host:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_not_called()

    def test_cancel_confirmation_never_opens_host_writer(self):
        screen = fake_controller(Writer())
        with patch('practice.toolkit.messagebox.askyesno', return_value=False), \
             patch('practice.toolkit.HostProcess') as host:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_not_called()
        self.assertIn('cancelled', screen.jp_position_result.value)

    def test_wrong_scene_refuses_even_if_flag_enabled(self):
        writer = Writer()
        screen = fake_controller(writer, scene=0x1D1)
        with patch('practice.toolkit.HostProcess') as host:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_not_called()
        self.assertEqual(writer.writes, [])

    def test_project64_success_only_writes_xyz_12_bytes_and_closes(self):
        writer = Writer()
        screen = fake_controller(writer)
        # Regression: our simple status stub intentionally has .set but no
        # .get; the successful writer must not assume every status proxy is a
        # full Tk StringVar.
        self.assertFalse(hasattr(screen.jp_position_result, 'get'))
        guest_writer = writer.rdram()
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.messagebox.askyesno', return_value=True), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(959604, 'project64')), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=('verified',)), \
             patch('practice.toolkit.HostProcess', return_value=writer) as host, \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=guest_writer) as validated:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_called_once_with(959604, writable=True)
        self.assertTrue(validated.call_args.kwargs['allow_4mb'])
        self.assertEqual(writer.close_count, 1)
        self.assertEqual(guest_writer.read_guest(JAPAN_PLAYER_XYZ_START, 12),
                         bytes.fromhex('c390800000000000c3270000'))
        self.assertEqual(len(writer.writes), 1)
        self.assertEqual(guest_writer.read_guest(JAPAN_CHARACTER_INDEX, 4),
                         bytes(4))
        self.assertIn('Goemon moved', screen.status.value)
        self.assertEqual(screen.jp_position_result.value, screen.status.value)

    def test_pid_mismatch_rejects_prior_to_opening_writable_handle(self):
        writer = Writer()
        screen = fake_controller(writer)
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.messagebox.askyesno', return_value=True), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(8989, 'project64')), \
             patch('practice.toolkit.HostProcess') as host:
            Toolkit.move_japan_oedo_xyz(screen)
        host.assert_not_called()
        self.assertEqual(writer.writes, [])
        self.assertIn('rejected', screen.status.value)

    def test_bad_coordinate_rejected_before_confirmation(self):
        screen = fake_controller(Writer())
        screen.jp_pos_y = Field('NaN')
        with patch('practice.toolkit.messagebox.askyesno') as confirm:
            Toolkit.move_japan_oedo_xyz(screen)
        confirm.assert_not_called()
        self.assertIn('rejected', screen.jp_position_result.value)


if __name__ == '__main__':
    unittest.main()
