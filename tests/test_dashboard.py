"""Presentation smoke tests; do not depend on a running game process."""
from __future__ import annotations

import tkinter as tk
import time
import unittest
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import patch

from practice.inspector import Watch
from practice.theme import PALETTE
from practice.toolkit import Toolkit
from practice.game_versions import VERSIONS


class DashboardSmokeTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Graphical Tk display unavailable: {exc}')
        self.root.withdraw()
        # Per-user remembered ROM state must not alter presentation tests.
        rom_cache = patch('practice.toolkit.load_remembered_rom',
                          return_value=None)
        rom_cache.start()
        self.addCleanup(rom_cache.stop)
        region_store = patch('practice.toolkit.save_last_region')
        region_store.start()
        self.addCleanup(region_store.stop)
        opts = dict(pid=None, base=None, endian='auto', route=None,
                    game_version='usa',
                    enable_teleport=True, enable_state_restore=True,
                    enable_debug_menu=True, enable_hex_edit=True,
                    enable_scene_warp=False)
        self.toolkit = Toolkit(self.root, Namespace(**opts))
        self.assertEqual(self.toolkit.active_version.key, 'usa')

    def tearDown(self):
        # A shutdown regression test deliberately destroys Tk before cleanup.
        # Destroying the same root again raises TclError on Windows/Tk 3.14.
        if hasattr(self, 'root'):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()
            except tk.TclError:
                pass  # Already destroyed during the test or application close.

    def test_dashboard_only_has_connection_and_checkpoints(self):
        app = self.toolkit
        self.assertEqual(app.notebook.tab(app.notebook.tabs()[0], 'text'), 'Dashboard')
        self.assertFalse(hasattr(app, 'quick_scene_tree'))
        self.assertFalse(hasattr(app, 'quick_watch_tree'))
        self.assertFalse(hasattr(app, 'speed_launch_button'))
        self.assertTrue(app.connect_button.winfo_exists())
        self.assertTrue(app.restore_state_btn.winfo_exists())
        self.assertTrue(app.cancel_restore_btn.winfo_exists())
        self.assertTrue(app.capture_state_btn.winfo_exists())
        self.assertTrue(app.checkpoint_name.winfo_exists())
        self.assertFalse(hasattr(app,'bookmarks_box'))
        self.assertFalse(hasattr(app,'teleport_btn'))
        self.assertFalse(hasattr(app,'bookmark_name'))
        app.open_full_scene_tab()
        self.assertEqual(app.notebook.select(), str(app.scene_tab))
        app.open_live_memory_tab()
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))

    def test_initial_window_is_monitor_sized_not_fixed_790_high(self):
        # A withdrawn Tk root reports 1x1 until Tk/WM processes layout.
        self.root.deiconify()
        self.root.update()
        width, height = (
            int(value) for value in self.root.geometry().split('+')[0].split('x'))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.assertEqual(width, max(780, min(1480, screen_width - 80)))
        self.assertEqual(height, max(600, min(950, screen_height - 100)))
        self.assertGreaterEqual(height, 600)
        self.assertLessEqual(height, 950)
        if screen_height >= 900:
            self.assertGreater(height, 790)

    def test_dashboard_uses_two_columns_at_opening_size(self):
        app = self.toolkit
        # The setUp root is withdrawn; expose it to measure real Tk geometry.
        self.root.deiconify()
        self.root.update()
        app._arrange_dashboard(app.dashboard_canvas.winfo_width())
        self.root.update_idletasks()
        self.assertTrue(app.dashboard_wide)
        self.assertEqual(int(app.dashboard_connection_column.grid_info()['row']), 0)
        self.assertEqual(int(app.dashboard_connection_column.grid_info()['column']), 0)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['row']), 0)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['column']), 1)
        self.assertLessEqual(
            app.dashboard_checkpoints_column.winfo_y() +
            app.dashboard_checkpoints_column.winfo_height(),
            app.dashboard_canvas.winfo_height(),
        )
        self.assertLessEqual(
            app.dashboard_connection_column.winfo_y() +
            app.dashboard_connection_column.winfo_height(),
            app.dashboard_canvas.winfo_height(),
        )
        self.assertTrue(app.checkpoints_box.winfo_exists())

    def test_dashboard_stacks_when_narrow_and_recovers_on_resize(self):
        app = self.toolkit
        self.root.geometry('960x640')
        app._arrange_dashboard(900)
        self.assertFalse(app.dashboard_wide)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['row']), 1)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['column']), 0)
        app._arrange_dashboard(1200)
        self.assertTrue(app.dashboard_wide)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['row']), 0)
        self.assertEqual(int(app.dashboard_checkpoints_column.grid_info()['column']), 1)
        self.assertTrue(app.checkpoints_box.winfo_exists())

    def test_combined_selector_labels_full_and_legacy_position_without_misrepresentation(self):
        from tests.test_checkpoint import TestCheckpoint
        from practice.checkpoints import capture_checkpoint
        app=self.toolkit
        _,ram=TestCheckpoint().sample()
        full=capture_checkpoint(ram,'Complete snapshot')
        app.checkpoints=[full]
        app.legacy_bookmarks=[dict(name='Old room',x=1.5,y=2.5,z=3.5,character=0,map_id=35),
                              dict(name='No map',x=1,y=2,z=3,character=0)]
        labels=app.checkpoint_labels()
        self.assertEqual(app.checkpoint_choices(),[('logical',0),('position',0),('position',1)])
        self.assertIn('logical',labels[0]);self.assertIn('XYZ saved',labels[0])
        self.assertIn('POSITION ONLY',labels[1]);self.assertIn('no inventory',labels[1])
        self.assertIn('map unknown',labels[2])
        self.assertFalse(hasattr(app,'save_bookmark'))

    def test_cancel_pending_restore_after_tk_root_destroy_is_safe(self):
        """Closing the main window must not touch deleted Tcl widget commands."""
        app = self.toolkit
        self.root.destroy()
        # Regression: used to raise TclError: invalid command name ...button.
        app.cancel_pending_restore(quiet=True)
        self.assertIsNone(app.pending_restore)

    def test_native_savestates_replace_logical_dashboard(self):
        app = self.toolkit
        self.assertTrue(app.native_save_btn.winfo_exists())
        self.assertTrue(app.native_load_btn.winfo_exists())
        self.assertEqual(app.legacy_checkpoint_card.winfo_manager(), '')
        self.assertEqual(app.savestate_slot_box.get(), '0')

    def test_native_savestate_sends_emulator_command(self):
        app = self.toolkit
        app.connection_target.set('project64')
        with patch('practice.toolkit.find_emulator_pid', return_value=(1234, 'project64')), \
             patch('practice.toolkit.send_state_command') as command:
            app.native_savestate_action('save')
        command.assert_called_once_with(1234, 'project64', 'save', 0)
        self.assertIsNone(app.mem)
        self.assertIn('Requested project64 save', app.status.get())

    def test_native_savestate_rejects_recomp(self):
        app = self.toolkit
        app.connection_target.set('recomp')
        with patch('practice.toolkit.send_state_command') as command:
            app.native_savestate_action('load')
        command.assert_not_called()
        self.assertIn('cannot create complete savestates', app.status.get())

    def test_flag_switch_preserves_single_dashboard_and_scene_widgets(self):
        app = self.toolkit
        self.root.deiconify()
        self.root.update_idletasks()
        original_widgets = (
            str(app.dashboard_canvas),
            str(app.dashboard_connection_column),
            str(app.dashboard_checkpoints_column),
            str(app.named_native_frame),
            str(app.scene_list),
            str(app.scene_character),
            str(app.notebook),
        )
        original_layout = (
            app.dashboard_connection_column.grid_info()['row'],
            app.dashboard_checkpoints_column.grid_info()['row'],
        )
        original_heading = app.version_heading.get()
        self.assertEqual(app.region_usa_button.cget('text'), '')
        self.assertEqual(app.region_japan_button.cget('text'), '')
        self.assertTrue(app.region_usa_button.cget('image'))
        self.assertTrue(app.region_japan_button.cget('image'))
        self.assertEqual(app.region_label.get(), 'USA')
        self.assertFalse(app.connection_advanced_visible)
        self.assertEqual(app.connection_advanced_frame.winfo_manager(), '')
        self.assertEqual(app.named_native_frame.winfo_manager(), '')
        self.assertEqual(app.jp_card.winfo_manager(), '')
        self.assertEqual(app.jp_base_row.winfo_manager(), '')
        self.assertFalse(app.named_native_expanded)
        self.assertFalse(hasattr(app, 'version_selector'))

        app.scene_character.current(3)
        app.scene_list.selection_set(0)
        selected_scene = app.scene_list.get(0)
        for button, expected in (
            (app.region_japan_button, 'japan'),
            (app.region_usa_button, 'usa'),
            (app.region_japan_button, 'japan'),
            (app.region_usa_button, 'usa'),
        ):
            button.invoke()
            self.root.update_idletasks()
            self.assertEqual(app.active_version.key, expected)
            self.assertEqual(
                original_widgets,
                (str(app.dashboard_canvas),
                 str(app.dashboard_connection_column),
                 str(app.dashboard_checkpoints_column),
                 str(app.named_native_frame),
                 str(app.scene_list),
                 str(app.scene_character),
                 str(app.notebook)))
            self.assertEqual(
                original_layout,
                (app.dashboard_connection_column.grid_info()['row'],
                 app.dashboard_checkpoints_column.grid_info()['row']))
            self.assertEqual(app.named_native_frame.winfo_manager(), '')
            self.assertEqual(app.region_label.get(),
                             'Japan' if expected == 'japan' else 'USA')
            self.assertEqual(app.jp_card.winfo_manager(), '')
            self.assertEqual(app.jp_base_row.winfo_manager(), '')
            self.assertEqual(app.version_heading.get(), original_heading)
            self.assertEqual(app.scene_character.current(), 3)
            self.assertEqual(app.scene_list.get(0), selected_scene)
            self.assertIsNone(app.mem)
            self.assertIsNone(app.jp_rdram)

    def test_collapsible_dashboard_sections_do_not_change_region(self):
        app = self.toolkit
        self.assertEqual(app.connection_advanced_frame.winfo_manager(), '')
        self.assertEqual(app.named_native_frame.winfo_manager(), '')
        app.connection_advanced_toggle.invoke()
        self.assertEqual(app.connection_advanced_frame.winfo_manager(), 'pack')
        self.assertTrue(app.connection_backend_selector.winfo_exists())
        app.named_native_toggle.invoke()
        self.assertEqual(app.named_native_frame.winfo_manager(), 'pack')
        app.region_japan_button.invoke()
        self.assertEqual(app.active_version.key, 'japan')
        self.assertEqual(app.connection_advanced_frame.winfo_manager(), 'pack')
        self.assertEqual(app.named_native_frame.winfo_manager(), 'pack')
        app.connection_advanced_toggle.invoke()
        app.named_native_toggle.invoke()
        self.assertEqual(app.connection_advanced_frame.winfo_manager(), '')
        self.assertEqual(app.named_native_frame.winfo_manager(), '')

    def test_flags_are_platform_independent_raster_images(self):
        app = self.toolkit
        usa = app.region_flag_images['usa']
        japan = app.region_flag_images['japan']
        self.assertEqual((usa.width(), usa.height()), (48, 32))
        self.assertEqual((japan.width(), japan.height()), (48, 32))
        self.assertEqual(tuple(japan.get(24, 16)), (188, 0, 45))
        self.assertEqual(tuple(japan.get(1, 1)), (255, 255, 255))
        self.assertEqual(tuple(usa.get(1, 1)), (60, 59, 110))
        self.assertEqual(tuple(usa.get(46, 31)), (178, 34, 52))

    def test_region_switch_locks_both_flag_buttons(self):
        app = self.toolkit
        app._set_region_switch_enabled(False)
        self.assertTrue(all('disabled' in b.state()
                            for b in app.region_buttons))
        app._set_region_switch_enabled(True)
        self.assertTrue(all('disabled' not in b.state()
                            for b in app.region_buttons))

    def test_game_version_selector_gates_usa_writers_but_exposes_japan_reads(self):
        app = self.toolkit
        self.assertEqual(app.active_version.key, 'usa')
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key, 'japan')
        self.assertIn('Japan selected', app.status.get())
        self.assertNotIn('disabled', app.connect_button.state())
        # The same navigation tabs remain active for both game versions;
        # the content and individually writable features switch by region.
        self.assertEqual(app.notebook.tab(app.scene_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.unlock_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.value_freezes_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.live_memory_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.story_progress_tab, 'state'), 'normal')
        self.assertEqual(app.scene_character_line.winfo_manager(), 'pack')
        self.assertEqual(app.scene_character.get(), 'Keep current character')
        self.assertNotEqual(app.entrance_box.winfo_manager(), '')
        self.assertIn('Load original USA ROM', app.entrance_load_button.cget('text'))
        self.assertIn('0x0C', app.scene_instruction.cget('text'))
        # Japanese raw memory editing is available in the UI; real writes
        # still require independently verified ROM/PID/RDRAM and permissions.
        self.assertNotIn('disabled', app.raw_write_btn.state())
        self.assertNotIn('disabled', app.freeze_raw_button.state())
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertEqual(
            app.unlock_address_labels[0x8015C69F].cget('text'), '80161E8F')
        self.assertEqual(
            app.unlock_address_labels[0x8015C6A7].cget('text'), '80161E97')
        app.open_full_scene_tab()
        self.assertEqual(app.notebook.select(), str(app.scene_tab))
        app.open_live_memory_tab()
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))
        self.assertEqual(app.discovery_tabs.tab(app.value_search_tab, 'state'), 'normal')
        self.assertEqual(app.discovery_tabs.tab(app.event_sessions_tab, 'state'), 'normal')
        self.assertEqual(app.event_sections.tab(app.event_sections.tabs()[0], 'state'),
                         'normal')
        self.assertNotIn('disabled', app.event_region_entry.state())
        self.assertIn('Japan-0', app.event_region_note.get())
        self.assertEqual(app.event_region_start.get(), '0x80161DF8')
        self.assertEqual(app.notebook.tab(app.jp_fields_tab, 'state'), 'hidden')
        self.assertNotEqual(app.jp_scene_position_frame.winfo_manager(), '')
        self.assertFalse(hasattr(app, 'verify_rom_button'))
        # Auto PID/backend discovery is now the default for Japan. The
        # verified Japanese ROM remains mandatory before probing any process
        # and the USA RAM path must never be selected by Japan's Connect.
        app.connection_target.set('auto')
        with patch('practice.toolkit.filedialog.askopenfilename',
                   return_value='') as pick_rom:
            app.connect()
            self.assertIsNone(app.mem)
            self.assertIsNone(app.jp_rdram)
            self.assertIn('ROM selection cancelled', app.status.get())
            app.connection_target.set('mupen64plus')
            app.connect()
            self.assertIn('ROM selection cancelled', app.status.get())
            self.assertEqual(pick_rom.call_count, 2)
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertNotIn('disabled', app.connect_button.state())
        self.assertEqual(app.notebook.tab(app.scene_tab, 'state'), 'normal')
        self.assertNotEqual(app.scene_character_line.winfo_manager(), '')
        self.assertNotEqual(app.entrance_box.winfo_manager(), '')
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertEqual(
            app.unlock_address_labels[0x8015C69F].cget('text'), '8015C69F')
        self.assertEqual(
            app.unlock_address_labels[0x8015C6A7].cget('text'), '8015C6A7')
        self.assertNotIn('disabled', app.raw_write_btn.state())
        self.assertEqual(app.event_sections.tab(app.event_sections.tabs()[0], 'state'),
                         'normal')
        self.assertIn('disabled', app.event_region_entry.state())
        self.assertEqual(app.event_region_start.get(), '0x8015C608')

    def test_japan_project64_linux_wine_selection_reaches_rom_verification(self):
        app = self.toolkit
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        app.connection_target.set('project64')
        app.verified_rom_path = None
        with patch('practice.toolkit.sys.platform', 'linux'), patch(
                'practice.toolkit.filedialog.askopenfilename',
                return_value='') as pick_rom:
            app.connect()
        pick_rom.assert_called_once()
        self.assertIn('ROM selection cancelled', app.status.get())
        self.assertNotIn('Windows only', app.status.get())
        self.assertIsNone(app.jp_rdram)

    def test_linux_dashboard_does_not_label_project64_windows_only(self):
        # Static text must describe the implemented Wine/Linux connection.
        app = self.toolkit
        labels = []
        def inspect(widget):
            try:
                value = widget.cget('text')
            except tk.TclError:
                value = ''
            if isinstance(value, str):
                labels.append(value)
            for child in widget.winfo_children():
                inspect(child)
        inspect(app.jp_card)
        self.assertTrue(any('Wine/Linux' in s for s in labels))
        self.assertFalse(any('project64 (Windows)' in s for s in labels))

    def test_japan_project64_windows_selection_and_wrong_backend_guard(self):
        app = self.toolkit
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        app.connection_target.set('project64')
        with patch('practice.toolkit.sys.platform', 'win32'), patch(
                'practice.toolkit.filedialog.askopenfilename',
                return_value='') as pick_rom:
            app.connect()
        pick_rom.assert_called_once()
        self.assertIn('ROM selection cancelled', app.status.get())
        self.assertIsNone(app.mem)

        # A changed target cannot trigger the wrong emulator's savestate.
        app.jp_backend = 'project64'
        app.game_pid = 1234
        app.jp_rdram = object()
        app.connection_target.set('mupen64plus')
        with patch('practice.toolkit.send_state_command') as command:
            app.native_savestate_action('save')
        command.assert_not_called()
        self.assertIn('differs from connected', app.status.get())

    def test_japan_verification_is_offline_only(self):
        app = self.toolkit
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        with patch('practice.toolkit.filedialog.askopenfilename', return_value='test.n64'), \
             patch('practice.toolkit.verify_selected_rom', return_value=VERSIONS['japan']) as verify:
            app.verify_rom_for_version()
        verify.assert_called_once_with('test.n64', 'japan')
        self.assertIn('Verified Japan', app.status.get())
        self.assertIsNone(app.mem)

    def test_japanese_idle_tick_skips_all_hidden_expensive_tables(self):
        app = self.toolkit
        app.active_version = VERSIONS['japan']
        app.jp_rdram = object()
        app._jp_position_last_poll = time.monotonic()
        app._jp_story_last_poll = 0.0
        app.notebook.select(app.dashboard_canvas.master)
        with patch.object(app, '_watch_japan_process_restart'), \
             patch.object(app, 'poll_japan_native_scene_warp'), \
             patch.object(app, 'refresh_japan_party_controls') as party, \
             patch.object(app, 'refresh_inspector') as inspector, \
             patch.object(app, 'refresh_unlocks') as unlocks, \
             patch.object(app, 'refresh_story_progress') as story, \
             patch.object(app, '_refresh_unlocks_on_reader_change'), \
             patch.object(app.root, 'after'):
            app.tick()
        party.assert_called_once()
        inspector.assert_not_called()
        unlocks.assert_not_called()
        story.assert_not_called()

    def test_japanese_live_watch_tab_only_polls_its_own_visible_table(self):
        app = self.toolkit
        app.active_version = VERSIONS['japan']
        app.jp_rdram = object()
        app._jp_position_last_poll = time.monotonic()
        app.notebook.select(app.live_memory_tab)
        app.live_memory_sections.select(app.live_watches_page)
        with patch.object(app, '_watch_japan_process_restart'), \
             patch.object(app, 'poll_japan_native_scene_warp'), \
             patch.object(app, 'refresh_japan_party_controls') as party, \
             patch.object(app, 'refresh_inspector') as inspector, \
             patch.object(app, 'refresh_unlocks') as unlocks, \
             patch.object(app, 'refresh_story_progress') as story, \
             patch.object(app, '_refresh_unlocks_on_reader_change'), \
             patch.object(app.root, 'after'):
            app.tick()
        inspector.assert_called_once_with({})
        party.assert_not_called()
        unlocks.assert_not_called()
        story.assert_not_called()

    def test_repainting_identical_live_watches_does_not_rebuild_tree(self):
        app = self.toolkit
        app.watch_previous = {}
        app.watch_rows = [
            Watch('Counter A', 0x80010000, '1', '01', 'OBSERVED', 'source'),
            Watch('Counter B', 0x80010001, '2', '02', 'OBSERVED', 'source'),
        ]
        app.draw_watches()
        tree = app.watch_tree
        tree.selection_set('Counter A')
        with patch.object(tree, 'delete', wraps=tree.delete) as delete, \
             patch.object(tree, 'insert', wraps=tree.insert) as insert, \
             patch.object(tree, 'item', wraps=tree.item) as item, \
             patch.object(tree, 'move', wraps=tree.move) as move:
            app.draw_watches()
            delete.assert_not_called()
            insert.assert_not_called()
            item.assert_not_called()
            move.assert_not_called()
        self.assertEqual(tree.selection(), ('Counter A',))
        app.watch_rows[1] = Watch(
            'Counter B', 0x80010001, '3', '03', 'OBSERVED', 'source')
        with patch.object(tree, 'delete', wraps=tree.delete) as delete, \
             patch.object(tree, 'insert', wraps=tree.insert) as insert, \
             patch.object(tree, 'item', wraps=tree.item) as item:
            app.draw_watches()
            delete.assert_not_called()
            insert.assert_not_called()
            item.assert_called_once()
        self.assertEqual(tree.set('Counter B', 'raw'), '03')
        self.assertEqual(tree.selection(), ('Counter A',))

    def test_dark_theme_and_no_unsafe_warp_activation(self):
        self.assertEqual(self.root.cget('background'), PALETTE['background'])
        self.assertFalse(self.toolkit.direct_warp_confirmed)
        self.assertFalse(self.toolkit.pending_direct_warp)


if __name__ == '__main__':
    unittest.main()
