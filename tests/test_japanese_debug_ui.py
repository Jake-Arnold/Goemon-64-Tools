"""Tk checks for the Japanese debug menu entry and scene selection hints."""
from types import SimpleNamespace

from tests.test_japanese_fields_ui import JapanTkSmokeTest
from tests.test_japanese_fields import FakeRam


class JapaneseDebugMenuTkTests(JapanTkSmokeTest):
    def test_native_menu_disabled_by_default_and_scene_index_is_hint(self):
        host = self.host
        self.assertFalse(host.jp_debug_controls_enabled)
        self.assertFalse(hasattr(host, 'jp_research_tabs'))
        self.assertEqual(host.selected_japan_debug_scene(), 0x161)
        host.show_japan_debug_target()
        self.assertIn('MACHI / stage index 3', host.jp_debug_result.get())
        self.assertIn('Double-click this room in Scene Browser',
                      host.jp_debug_result.get())
        self.assertFalse(hasattr(host, 'jp_warp_scene_list'))
        self.assertFalse(hasattr(host, 'jp_debug_scene_selector'))
        self.assertFalse(hasattr(host, 'jp_warp_a_key'))

    def test_debug_button_requires_verified_connection_not_gameplay_or_optin(self):
        host = self.host
        host.args = SimpleNamespace(
            enable_japan_debug_menu_writes=True, read_only=False,
            enable_japan_party_writes=False,
            enable_japan_position_writes=False)
        host.jp_rdram = FakeRam()
        host.game_pid = 55993
        host.jp_backend = 'project64'
        host.connection_target = SimpleNamespace(get=lambda: 'project64')
        host.refresh_japan_debug_controls()
        self.assertFalse(host.jp_debug_controls_enabled)
        host.verified_rom_path = 'verified-japan-rom.n64'
        host.args.enable_japan_debug_menu_writes = False
        host.connection_target = SimpleNamespace(get=lambda: 'auto')
        host.refresh_japan_debug_controls()
        self.assertTrue(host.jp_debug_controls_enabled)
        host.args.read_only = True
        host.refresh_japan_debug_controls()
        self.assertFalse(host.jp_debug_controls_enabled)
        host.args.read_only = False
        host.connection_target = SimpleNamespace(get=lambda: 'mupen64plus')
        host.refresh_japan_debug_controls()
        self.assertFalse(host.jp_debug_controls_enabled)
        host.connection_target = SimpleNamespace(get=lambda: 'project64')
        host.jp_rdram = None
        host.refresh_japan_debug_controls()
        self.assertFalse(host.jp_debug_controls_enabled)


if __name__ == '__main__':
    import unittest
    unittest.main()
