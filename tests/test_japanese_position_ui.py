"""Tk safety and presentation checks for Japan-0 manual XYZ controls."""
from types import SimpleNamespace
import unittest

from tests.test_japanese_fields_ui import JapanTkSmokeTest
from tests.test_japanese_fields import FakeRam


class JapanPositionUiTests(JapanTkSmokeTest):
    def test_position_controls_disabled_without_explicit_opt_in(self):
        host = self.host
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())
        self.assertEqual(host.jp_pos_x.get(), '-289.0')
        self.assertEqual(host.jp_pos_y.get(), '0.0')
        self.assertEqual(host.jp_pos_z.get(), '-167.0')
        host.use_japan_oedo_entrance()
        self.assertIn('no RAM write', host.jp_position_result.get())

    def test_read_current_and_preset_never_write_ram(self):
        import struct
        host = self.host
        guest = {
            (0x80151B10, 12): struct.pack('>fff', 18.5, 52.0, -120.25),
            (0x800CD2A2, 2): bytes.fromhex('0161'),
            (0x80161DCC, 4): bytes(4),
        }
        fake = FakeRam(guest)
        host.jp_rdram = fake
        host.refresh_japan_position()
        self.assertEqual(host.jp_pos_x.get(), '18.500000')
        self.assertEqual(host.jp_pos_y.get(), '52.000000')
        self.assertEqual(host.jp_pos_z.get(), '-120.250000')
        host.use_japan_oedo_entrance()
        self.assertEqual(host.jp_pos_x.get(), '-289.0')
        self.assertIn('no RAM write', host.jp_position_result.get())
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())

    def test_bounded_write_control_requires_all_verified_identifiers(self):
        host = self.host
        host.args = SimpleNamespace(
            enable_japan_position_writes=True, read_only=False,
            enable_japan_party_writes=False)
        host.game_pid = 123
        host.jp_backend = 'project64'
        host.connection_target = SimpleNamespace(get=lambda: 'project64')
        host.verified_rom_path = 'japan0.n64'
        host.jp_rdram = FakeRam()
        host.refresh_japan_position_controls()
        self.assertNotIn('disabled', host.jp_scene_position_apply_button.state())
        host.args.read_only = True
        host.refresh_japan_position_controls()
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())
        host.args.read_only = False
        host.connection_target = SimpleNamespace(get=lambda: 'mupen64plus')
        host.refresh_japan_position_controls()
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())
        host.connection_target = SimpleNamespace(get=lambda: 'project64')
        host.jp_rdram = None
        host.refresh_japan_position_controls()
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())


if __name__ == '__main__':
    unittest.main()
