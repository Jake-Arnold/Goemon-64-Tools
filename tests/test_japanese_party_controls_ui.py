"""No duplicate Sasuke/Yae controls in Japanese diagnostics.

The verified one-shot party writers remain tested separately, and the shared
Unlocks tab owns the only party toggle buttons for either ROM.
"""
from tests.test_japanese_fields_ui import JapanTkSmokeTest


class JapanesePartyUiSmokeTest(JapanTkSmokeTest):
    def test_no_duplicate_party_buttons_in_japan_live(self):
        host = self.host
        self.assertFalse(hasattr(host, 'jp_party_buttons'))
        self.assertFalse(hasattr(host, 'jp_party_result'))
        self.assertFalse(hasattr(host, 'jp_research_tabs'))

    def test_legacy_refresh_keeps_independent_controls_safe(self):
        host = self.host
        host.refresh_japan_party_controls()
        self.assertIn('disabled', host.jp_scene_position_apply_button.state())
        self.assertFalse(host.jp_debug_controls_enabled)
