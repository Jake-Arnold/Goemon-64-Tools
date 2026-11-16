"""Tk smoke tests for region crosswalk (no ROM, no writes)."""
from practice.region_memory_crosswalk import CROSS_REGION_BY_KEY
from tests.test_japanese_fields import FakeRam
from tests.test_japanese_fields_ui import JapanTkSmokeTest


class CrosswalkUiTests(JapanTkSmokeTest):
    def test_candidate_table_and_readonly_baseline_comparison(self):
        host = self.host
        weapon = CROSS_REGION_BY_KEY["static:weapon_index"]
        self.assertTrue(host.jp_crosswalk_tree.exists(
            "jp_cross_static:weapon_index"))
        self.assertEqual(host.jp_crosswalk_tree.set(
            "jp_cross_static:pause_byte", "evidence"), "disputed")

        ram = FakeRam({(weapon.japan, 1): b"\x01"})
        ram.base, ram.endian = 0x10000000, "big"
        host.jp_rdram = ram
        self.assertTrue(host.refresh_japan_crosswalk(capture=True))
        self.assertEqual(host.jp_crosswalk_tree.set(
            "jp_cross_static:weapon_index", "value"), "0x01")

        ram.values[(weapon.japan, 1)] = b"\x02"
        self.assertTrue(host.refresh_japan_crosswalk(compare=True))
        self.assertIn("1 raw changes", host.jp_crosswalk_status.get())
        self.assertIn("RAW CHANGE", host.jp_crosswalk_tree.set(
            "jp_cross_static:weapon_index", "evidence"))
        self.assertEqual(len(host._jp_crosswalk_changes), 1)
        self.assertEqual(host._jp_crosswalk_changes[0][0].key,
                         "static:weapon_index")

        host.clear_japan_field_values()
        self.assertEqual(host.jp_crosswalk_tree.set(
            "jp_cross_static:weapon_index", "value"), "—")

    def test_no_japan_reader_before_connection(self):
        host = self.host
        self.assertFalse(host.refresh_japan_crosswalk())
        self.assertIn("Connect", host.jp_crosswalk_status.get())
