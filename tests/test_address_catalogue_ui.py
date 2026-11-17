"""Headless Tk tests for the shared searchable Memory Address Catalogue."""
from __future__ import annotations

import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.game_versions import VERSIONS
from tests.test_unlocks import FakeRAM


class AddressCatalogueUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        save = patch("practice.toolkit.save_last_region")
        save.start()
        self.addCleanup(save.stop)
        remembered = patch(
            "practice.toolkit.load_remembered_rom", return_value=None)
        remembered.start()
        self.addCleanup(remembered.stop)
        self.app = Toolkit(self.root, parse_args(["--game-version", "usa"]))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for token in self.root.tk.call("after", "info"):
                self.root.after_cancel(token)
            self.root.destroy()
        except tk.TclError:
            pass

    def _open(self):
        app = self.app
        self.assertFalse(app.catalogue_loaded)
        self.assertEqual(
            app.live_memory_sections.tab(app.address_catalogue_page, "text"),
            "Address catalogue")
        app.live_memory_sections.select(app.address_catalogue_page)
        app.show_address_catalogue()
        self.assertTrue(app.catalogue_loaded)
        self.assertGreater(len(app.catalogue_rows), 490)

    def test_existing_live_watches_preserved_and_catalogue_offline(self):
        app = self.app
        self.assertEqual(
            app.live_memory_sections.tab(app.live_watches_page, "text"),
            "Live watches")
        self._open()
        self.assertIsNone(app.mem)
        self.assertIsNone(app.jp_rdram)
        self.assertTrue(app.catalogue_tree.exists(
            "research:vm_text_stream_cursor"))
        self.assertIn("Registry v", app.catalogue_status.get())
        self.assertIsNotNone(app.watch_tree)

    def test_search_filters_and_sort_return_vm_and_disputed(self):
        app = self.app
        self._open()
        app.catalogue_query.set("1C77E8")
        self.assertEqual(len(app.catalogue_tree.get_children()), 1)
        self.assertTrue(app.catalogue_tree.exists(
            "research:vm_text_stream_cursor"))
        app.catalogue_query.set("")
        app.catalogue_region.set("japan")
        app.catalogue_evidence.set("disputed")
        self.assertGreaterEqual(len(app.catalogue_tree.get_children()), 1)
        app.catalogue_category.set("saved_event_bit")
        app.catalogue_type.set("u8")
        app.catalogue_region.set("usa")
        app.catalogue_evidence.set("all")
        self.assertGreater(len(app.catalogue_tree.get_children()), 40)
        app.sort_address_catalogue("name")
        app.sort_address_catalogue("address")
        self.assertEqual(app.catalogue_sort[0], "address")

    def test_selection_shows_full_evidence_related_fields_and_copy(self):
        app = self.app
        self._open()
        app.catalogue_tree.selection_set("story:usa:benkei_encounter")
        app.select_catalogue_address()
        text = app.catalogue_detail.get("1.0", "end")
        self.assertIn("benkei_encounter", text)
        self.assertIn("ROM script + user tests", text)
        self.assertIn("overlapping_or_related_fields", text)
        app.copy_catalogue_address()
        self.assertEqual(self.root.clipboard_get(), "0x8015C60C")
        app.copy_catalogue_address_mask()
        self.assertEqual(self.root.clipboard_get(), "0x8015C60C & 0x20")

    def test_add_watch_copies_known_decoder_and_never_writes(self):
        app = self.app
        self._open()
        app.catalogue_tree.selection_set("research:vm_text_stream_cursor")
        with patch.object(app, "add_custom_watch") as add:
            app.add_catalogue_watch()
            add.assert_called_once_with()
        self.assertEqual(app.user_watch_address.get(), "0x801C77E8")
        self.assertEqual(app.user_watch_type.get(), "u32")
        app.catalogue_tree.selection_set("external:warp_slot:01")
        with patch.object(app, "add_custom_watch") as add:
            app.add_catalogue_watch()
            add.assert_not_called()

    def test_selected_vm_can_read_one_field_through_usa_backend(self):
        app = self.app
        self._open()
        ram = FakeRAM()
        ram.bytes.update({
            0x801C77E8: 0x80,
            0x801C77E9: 0x1C,
            0x801C77EA: 0x77,
            0x801C77EB: 0xE8,
        })
        app.mem = ram
        app.catalogue_tree.selection_set("research:vm_text_stream_cursor")
        app.inspect_catalogue_address()
        # Drain one deterministic worker result, without any Tk writes off
        # the UI thread.
        import time
        deadline = time.monotonic() + 1.5
        while app.catalogue_busy and time.monotonic() < deadline:
            try:
                app._poll_catalogue_worker()
            except tk.TclError:
                break
            time.sleep(0.01)
        self.assertIn("0x801C77E8", app.catalogue_selected.get())
        self.assertEqual(ram.writes, [])

    def test_japan_backend_is_independent_and_research_leads_remain_visible(self):
        app = self.app
        self._open()
        app.catalogue_tree.selection_set("crosswalk:japan:event:benkei_encounter")
        app.inspect_catalogue_address()
        self.assertIn("Region mismatch", app.catalogue_selected.get())
        app.game_version_choice.set(VERSIONS["japan"].label)
        app.on_game_version_changed()
        app.catalogue_region.set("japan")
        self.assertTrue(app.catalogue_tree.exists(
            "crosswalk:japan:event:benkei_encounter"))
        app.catalogue_tree.selection_set("crosswalk:japan:event:benkei_encounter")
        app.inspect_catalogue_address()
        self.assertIn("Disconnected", app.catalogue_selected.get())

    def test_control_navigation_preserves_original_unlock_tabs(self):
        app = self.app
        self._open()
        app.catalogue_tree.selection_set("story:usa:benkei_encounter")
        app.open_catalogue_control()
        self.assertEqual(app.notebook.select(), str(app.unlock_tab))
        self.assertEqual(app.unlock_sections.select(),
                         str(app.unlock_flags_page))
        self.assertIn("Benkei", app.unlock_flag_query.get())

    def test_refresh_error_preserves_locally_bundled_catalogue(self):
        app = self.app
        self._open()
        original = len(app.catalogue_rows)
        app.catalogue_events.put(
            ("refresh", None, None, "Offline, blocked or HTTP 404"))
        app.catalogue_busy = True
        app._poll_catalogue_worker()
        self.assertFalse(app.catalogue_busy)
        self.assertEqual(len(app.catalogue_rows), original)
        self.assertIn("Offline", app.catalogue_selected.get())


if __name__ == "__main__":
    unittest.main()
