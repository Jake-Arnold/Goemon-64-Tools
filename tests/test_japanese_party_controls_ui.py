"""Tk smoke checks for opt-in Japanese party-flag unlock controls."""
from types import SimpleNamespace
from tests.test_japanese_fields_ui import JapanTkSmokeTest
from tests.test_japanese_fields import FakeRam


class JapanesePartyUiSmokeTest(JapanTkSmokeTest):
    def test_sasuke_yae_buttons_default_to_disabled(self):
        host = self.host
        self.assertIn('disabled', host.jp_party_buttons[2].state())
        self.assertIn('disabled', host.jp_party_buttons[3].state())
        host.refresh_japan_party_controls()
        self.assertIn('disabled', host.jp_party_buttons[2].state())

    def test_buttons_need_pid_connection_and_explicit_opt_in(self):
        host = self.host
        host.args = SimpleNamespace(enable_japan_party_writes=True, read_only=False)
        host.game_pid = 959604
        host.refresh_japan_party_controls()
        self.assertIn('disabled', host.jp_party_buttons[2].state())

        host.jp_rdram = FakeRam()
        host.refresh_japan_party_controls()
        for button in host.jp_party_buttons.values():
            self.assertNotIn('disabled', button.state())

        host.args.read_only = True
        host.refresh_japan_party_controls()
        self.assertIn('disabled', host.jp_party_buttons[2].state())

        host.args.read_only = False
        host.active_version.key = 'usa'
        host.refresh_japan_party_controls()
        self.assertIn('disabled', host.jp_party_buttons[3].state())

    def test_disconnect_disables_write_controls(self):
        host = self.host
        host.args = SimpleNamespace(enable_japan_party_writes=True, read_only=False)
        host.game_pid = 959604
        host.jp_rdram = FakeRam()
        host.refresh_japan_party_controls()
        self.assertNotIn('disabled', host.jp_party_buttons[2].state())
        host.jp_rdram = None
        host.clear_japan_field_values()
        self.assertIn('disabled', host.jp_party_buttons[2].state())
