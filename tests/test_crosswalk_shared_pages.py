"""ROM-free shared-page crosswalk regression coverage.

Japanese cross-region addresses appear in the normal Live Memory / Story
Progress data models, never as a new JavaScript/Tk diagnostics panel.
"""
import unittest

from practice.region_views import japan_live_watches, japan_story_crosswalk_rows
from practice.region_memory_crosswalk import CROSS_REGION_BY_KEY


class FakeRdram:
    def __init__(self, contents=None):
        self.contents = contents or {}
        self.reads = []

    def read_guest(self, address, size):
        self.reads.append((address, size))
        return self.contents.get((address, size), bytes(size))

    def write_guest(self, *_args):
        raise AssertionError("Crosswalk research must not write guest memory")


class CrosswalkSharedPagesTests(unittest.TestCase):
    def test_live_memory_shows_confirmed_static_fields_in_existing_page(self):
        rows = japan_live_watches(FakeRdram())
        weapon = [r for r in rows if r.addr == 0x80161DF7]
        self.assertEqual(len(weapon), 1)
        self.assertIn("Equipped weapon", weapon[0].name)
        self.assertIn("USA 0x8015C607", weapon[0].source)
        # The existing scene-probe lead can still be shown, but the
        # crosswalk must not create a second or confirmed pause entry.
        disputed = [r for r in rows if r.addr == 0x800CD2D6]
        self.assertLessEqual(len(disputed), 1)
        self.assertTrue(all('user-confirmed' not in r.source for r in disputed))

    def test_story_progress_uses_explicit_japan_address_and_mask(self):
        addr = 0x80161DFC
        rows = japan_story_crosswalk_rows(FakeRdram({(addr, 1): b"\x20"}))
        benkei = next(row for row in rows
                      if row["key"] == "jp_cross_event_benkei_encounter")
        self.assertEqual(benkei["address"], addr)
        self.assertEqual(benkei["mask"], "0x20")
        self.assertEqual(benkei["value"], "Set")
        self.assertEqual(benkei["section"], "Benkei & Kihachi")

    def test_ungrounded_saved_bits_are_marked_unverified_not_true_events(self):
        rows = japan_story_crosswalk_rows(FakeRdram())
        candidates = [row for row in rows
                      if "candidate" in row["bank"].lower()]
        self.assertGreater(len(candidates), 0)
        self.assertTrue(all("unverified" in row["value"].lower()
                            for row in candidates))
        self.assertTrue(all("read-only" in row["source"] for row in rows))
        self.assertTrue(all(row["key"].startswith("jp_cross_") for row in rows))

    def test_stale_disconnected_guest_has_no_semantic_state(self):
        rows = japan_story_crosswalk_rows(None)
        self.assertTrue(all(row["value"] == "Unavailable" and row["raw"] == "—"
                            for row in rows))

    def test_dynamic_pointer_excluded_from_mapping_catalogue(self):
        self.assertNotIn("static:menu_pointer", CROSS_REGION_BY_KEY)
        self.assertEqual(CROSS_REGION_BY_KEY["static:pause_byte"].evidence,
                         "disputed")


if __name__ == "__main__":
    unittest.main()
