"""Presentation smoke tests; do not depend on a running game process."""
from __future__ import annotations

import tkinter as tk
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
        opts = dict(pid=None, base=None, endian='auto', route=None,
                    enable_teleport=True, enable_state_restore=True,
                    enable_debug_menu=True, enable_hex_edit=True,
                    enable_scene_warp=False)
        self.toolkit = Toolkit(self.root, Namespace(**opts))

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

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
        self.assertEqual(app.scene_character_line.winfo_manager(), '')
        self.assertEqual(app.entrance_box.winfo_manager(), '')
        self.assertIn('JAPAN:', app.scene_instruction.cget('text'))
        self.assertIn('disabled', app.raw_write_btn.state())
        self.assertIn('disabled', app.freeze_raw_button.state())
        self.assertEqual(app.jp_unlock_panel.winfo_manager(), 'pack')
        app.open_full_scene_tab()
        self.assertEqual(app.notebook.select(), str(app.scene_tab))
        app.open_live_memory_tab()
        self.assertEqual(app.notebook.select(), str(app.live_memory_tab))
        self.assertEqual(app.notebook.tab(app.value_search_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.event_sessions_tab, 'state'), 'normal')
        self.assertEqual(app.event_sections.tab(app.event_sections.tabs()[0], 'state'),
                         'normal')
        self.assertNotIn('disabled', app.event_region_entry.state())
        self.assertIn('Japan-0', app.event_region_note.get())
        self.assertEqual(app.event_region_start.get(), '0x80161D80')
        self.assertEqual(app.notebook.tab(app.jp_fields_tab, 'state'), 'normal')
        # Direct connect must never fall through to unsupported USA process memory.
        app.connect()
        self.assertIsNone(app.mem)
        self.assertIsNone(app.jp_rdram)
        self.assertIn('requires target mupen64plus', app.status.get())
        app.connection_target.set('mupen64plus')
        app.connect()
        self.assertIn('Verify the exact Japan-0 ROM', app.status.get())
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertNotIn('disabled', app.connect_button.state())
        self.assertEqual(app.notebook.tab(app.scene_tab, 'state'), 'normal')
        self.assertNotEqual(app.scene_character_line.winfo_manager(), '')
        self.assertNotEqual(app.entrance_box.winfo_manager(), '')
        self.assertEqual(app.jp_unlock_panel.winfo_manager(), '')
        self.assertNotIn('disabled', app.raw_write_btn.state())
        self.assertEqual(app.event_sections.tab(app.event_sections.tabs()[0], 'state'),
                         'normal')
        self.assertIn('disabled', app.event_region_entry.state())
        self.assertEqual(app.event_region_start.get(), '0x8015C608')

    def test_japan_project64_windows_selection_and_wrong_backend_guard(self):
        app = self.toolkit
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        app.connection_target.set('project64')
        with patch('practice.toolkit.sys.platform', 'win32'):
            app.connect()
        self.assertIn('Verify the exact Japan-0 ROM', app.status.get())
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

    def test_dark_theme_and_no_unsafe_warp_activation(self):
        self.assertEqual(self.root.cget('background'), PALETTE['background'])
        self.assertFalse(self.toolkit.direct_warp_confirmed)
        self.assertFalse(self.toolkit.pending_direct_warp)


if __name__ == '__main__':
    unittest.main()
