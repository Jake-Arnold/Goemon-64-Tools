"""Tk integration for Unlocks items and per-flag On/Off controls."""
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.game_versions import VERSIONS
from tests.test_unlocks import FakeRAM


class UnlockFlagsUITests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        remember = patch('practice.toolkit.save_last_region')
        remember.start()
        self.addCleanup(remember.stop)
        cache = patch('practice.toolkit.load_remembered_rom', return_value=None)
        cache.start()
        self.addCleanup(cache.stop)
        self.app = Toolkit(self.root, parse_args([
            '--game-version', 'usa', '--enable-hex-edit']))
        self.addCleanup(self._close)

    def _close(self):
        try:
            for callback in self.root.tk.call('after', 'info'):
                self.root.after_cancel(callback)
            self.root.destroy()
        except tk.TclError:
            pass

    def _open_flags(self):
        app = self.app
        app.unlock_sections.select(app.unlock_flags_page)
        app.on_unlock_section_changed()
        app.refresh_unlock_flags(force=True)

    def _expand(self, type_name='Benkei & Kihachi', subtype='Unsorted'):
        app = self.app
        section = (type_name, subtype)
        self.assertIn(section, app.unlock_flag_sections)
        app._set_unlock_flag_section_expanded(section, True)
        app.filter_unlock_flags()
        app.refresh_unlock_flags(force=True)
        self._drain_render()

    def _drain_render(self):
        # CI can deterministically flush deferred batches without sleeping
        # or relying on the window manager's repaint schedule.
        for _ in range(64):
            if not self.app._unlock_flag_pending:
                return
            for section in tuple(self.app._unlock_flag_pending):
                self.app._populate_unlock_flag_batch(section)
        self.fail('Flag rendering did not drain')

    def _select_japan(self):
        app = self.app
        app.game_version_choice.set(VERSIONS['japan'].label)
        app.on_game_version_changed()
        self.assertEqual(app.active_version.key, 'japan')

    def test_two_pages_keep_all_items_and_create_inline_buttons_lazily(self):
        app = self.app
        self.assertEqual([
            app.unlock_sections.tab(item, 'text')
            for item in app.unlock_sections.tabs()],
            ['Items & equipment', 'Story & event flags'])
        self.assertEqual(app.usa_unlock_shell.winfo_manager(), 'pack')
        self.assertEqual(len(app.unlock_row_widgets), 34)
        self.assertGreater(len(app.unlock_flag_rows), 100)
        self.assertEqual(app.unlock_flag_widgets, {})
        app.mem = FakeRAM()
        self._open_flags()
        self.assertEqual(app.unlock_flag_widgets, {})
        self.assertEqual(len(app.unlock_flag_sections), 7)
        self.assertEqual(app.unlock_flag_expanded, set())
        self._expand()
        self.assertLess(len(app.unlock_flag_widgets),
                        len(app.unlock_flag_rows))
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertEqual(widgets['on'].cget('text'), 'On')
        self.assertEqual(widgets['off'].cget('text'), 'Off')
        self.assertEqual(widgets['state'].get(), 'Off')
        self.assertNotIn('disabled', widgets['on'].state())
        self.assertFalse(hasattr(app, 'unlock_flag_set'))
        self.assertFalse(hasattr(app, 'unlock_flag_tree'))

    def test_usa_each_flag_has_its_own_on_off_and_preserves_other_bits(self):
        app = self.app
        app.mem = FakeRAM()
        app.mem.bytes[0x8015C60C] = 0x81
        self._open_flags()
        self._expand()
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertEqual(widgets['state'].get(), 'Off')
        widgets['on'].invoke()
        self.assertEqual(app.mem.bytes[0x8015C60C], 0xA1)
        self.assertEqual(widgets['state'].get(), 'On')
        self.assertEqual(widgets['on'].cget('style'), 'FlagOn.TButton')
        widgets['off'].invoke()
        self.assertEqual(app.mem.bytes[0x8015C60C], 0x81)
        self.assertEqual(widgets['state'].get(), 'Off')
        self.assertEqual(widgets['off'].cget('style'), 'FlagOff.TButton')
        self.assertEqual(
            [w[0] for w in app.mem.writes], [0x8015C60C, 0x8015C60C])

    def test_usa_stale_and_read_only_refuse_writes_without_reverting_other_bits(self):
        app = self.app
        ram = FakeRAM()
        app.mem = ram
        self._open_flags()
        self._expand()
        widgets = app.unlock_flag_widgets['benkei_encounter']
        ram.bytes[0x8015C60C] = 0x10
        widgets['on'].invoke()
        self.assertEqual(ram.writes, [])
        self.assertIn('blocked', app.unlock_status.get())
        self.assertEqual(widgets['state'].get(), 'Off')
        self.assertIn('changed', app.unlock_flag_feedback.get())
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        self.assertIn('disabled', widgets['on'].state())
        self.assertIn('disabled', widgets['off'].state())
        widgets['on'].invoke()
        self.assertEqual(ram.writes, [])

    def test_japan_confirmed_and_candidate_have_individual_on_off(self):
        app = self.app
        self._select_japan()
        ram = FakeRAM()
        ram.bytes[0x80161DFC] = 0x81
        app.jp_rdram = ram
        app.game_pid = 1234
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        self._open_flags()
        self._expand()
        benkei = app.unlock_flag_rows['benkei_encounter']
        self.assertEqual(benkei.address, 0x80161DFC)
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertNotIn('disabled', widgets['on'].state())
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            widgets['on'].invoke()
            writer.assert_called_once_with(
                0x80161DFC, b'\xA1', expected=b'\x81')
        candidate = app.unlock_flag_rows['oedo_old_man_dialogue_cycle']
        self.assertTrue(candidate.editable)
        self.assertEqual(candidate.source, 'JP offset candidate')
        self._expand('Other story')
        section = ('Other story', 'Unsorted')
        table = app._unlock_flag_treeviews[section]
        self.assertEqual(table.set(candidate.key, 'on'), 'On')
        self.assertEqual(table.set(candidate.key, 'off'), 'Off')
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            app._activate_unlock_flag_tree_cell(section, candidate.key, 'Set')
            writer.assert_called_once_with(
                candidate.address, bytes((candidate.mask,)),
                expected=b'\x00')
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        self.assertEqual(table.set(candidate.key, 'on'), '—')
        self.assertEqual(table.set(candidate.key, 'off'), '—')
        with patch.object(app, 'write_japan_raw_bytes') as writer:
            app._activate_unlock_flag_tree_cell(section, candidate.key, 'Clear')
            writer.assert_not_called()

    def test_japan_receipt_flag_independent_cas_and_region_switch(self):
        app = self.app
        self._select_japan()
        ram = FakeRAM()
        ram.bytes[0x80161DF8] = 0x04  # Adjacent Oedo story bit.
        ram.bytes[0x80161EF3] = 0x01  # Separate inventory field.
        app.jp_rdram = ram
        app.game_pid = 1234
        app.jp_backend = 'project64'
        app.connection_target.set('project64')
        self._open_flags()
        self._expand('External annotations')
        flag = app.unlock_flag_rows['external_super_pass']
        self.assertEqual((flag.address, flag.mask), (0x80161DF8, 0x01))
        section = ('External annotations', 'Unsorted')
        table = app._unlock_flag_treeviews[section]
        self.assertEqual(table.set(flag.key, 'on'), 'On')
        self.assertEqual(table.set(flag.key, 'off'), 'Off')
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            app._activate_unlock_flag_tree_cell(section, flag.key, 'Set')
            writer.assert_called_once_with(
                0x80161DF8, b'\x05', expected=b'\x04')
        ram.bytes[0x80161DF8] = 0x05
        app.refresh_unlock_flags(force=True)
        with patch.object(app, 'write_japan_raw_bytes', return_value=True) as writer:
            app._activate_unlock_flag_tree_cell(section, flag.key, 'Clear')
            writer.assert_called_once_with(
                0x80161DF8, b'\x04', expected=b'\x05')
        self.assertEqual(ram.bytes[0x80161EF3], 0x01)
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        self.assertEqual(table.set(flag.key, 'on'), '—')
        self.assertEqual(table.set(flag.key, 'off'), '—')
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertEqual(app.unlock_flag_rows[flag.key].address, 0x8015C608)

    def test_filter_and_region_switch_replace_controls_and_no_old_address(self):
        app = self.app
        self._open_flags()
        app.unlock_flag_query.set('benkei')
        self._drain_render()
        self.assertLess(int(app.unlock_flag_counter.get().split(' / ')[0]),
                        len(app.unlock_flag_rows))
        self.assertEqual(
            app.unlock_flag_widgets['benkei_encounter']['frame'].winfo_manager(),
            'grid')
        # Search matches name AND provenance; a row can be constructed
        # because its research evidence mentions Benkei even if its title
        # does not. Only matched visibility and region-safe identity matter.
        self.assertEqual(
            app.unlock_flag_widgets['benkei_encounter']['frame'].winfo_manager(),
            'grid')
        self.assertEqual(
            app.unlock_flag_sections[('Other story', 'Unsorted')].winfo_manager(),
            '')
        self._select_japan()
        self.assertNotIn('external_sasuke_recruited', app.unlock_flag_widgets)
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].address,
                         0x80161DFC)
        app.game_version_choice.set(VERSIONS['usa'].label)
        app.on_game_version_changed()
        self.assertIn('external_sasuke_recruited', app.unlock_flag_rows)
        # Regional controls may be lazily instantiated for search
        # matches; no stale Japanese addresses may persist in the model.
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].address,
                         0x8015C60C)
        app.unlock_flag_query.set('')
        self.assertEqual(
            int(app.unlock_flag_counter.get().split(' / ')[0]),
            len(app.unlock_flag_rows))

    def test_type_and_subtype_filters_control_row_and_header_visibility(self):
        app = self.app
        self._open_flags()
        self.assertIn('All types', app.unlock_flag_type_box['values'])
        self.assertIn('Benkei & Kihachi', app.unlock_flag_type_box['values'])
        self.assertEqual(app.unlock_flag_rows['benkei_encounter'].subtype,
                         'Unsorted')
        app.unlock_flag_type.set('Benkei & Kihachi')
        app.on_unlock_flag_type_changed()
        self.assertEqual(app.unlock_flag_subtype.get(), 'All subtypes')
        self.assertIn('Unsorted', app.unlock_flag_subtype_box['values'])
        self.assertNotIn('benkei_encounter', app.unlock_flag_widgets)
        self._expand()
        self.assertEqual(
            app.unlock_flag_widgets['benkei_encounter']['frame'].winfo_manager(),
            'grid')
        self.assertNotIn('oedo_old_man_dialogue_cycle',
                         app.unlock_flag_widgets)
        self.assertEqual(
            app.unlock_flag_sections[('Benkei & Kihachi', 'Unsorted')].winfo_manager(),
            'grid')
        self.assertEqual(
            app.unlock_flag_sections[('Other story', 'Unsorted')].winfo_manager(),
            '')
        app.unlock_flag_subtype.set('Unsorted')
        app.filter_unlock_flags()
        self.assertEqual(
            int(app.unlock_flag_counter.get().split(' / ')[0]), 9)
        app.unlock_flag_type.set('All types')
        app.on_unlock_flag_type_changed()
        self.assertEqual(
            int(app.unlock_flag_counter.get().split(' / ')[0]),
            len(app.unlock_flag_rows))

    def test_compact_flag_rows_have_consistent_contrasting_backgrounds(self):
        app = self.app
        self._open_flags()
        self._expand()
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertEqual(widgets['frame'].cget('style'), 'FlagRow.TFrame')
        self.assertEqual(widgets['off'].cget('style'), 'Flag.TButton')
        self.assertEqual(widgets['on'].cget('style'), 'Flag.TButton')
        self.assertEqual(
            app.unlock_status_label.winfo_parent(), str(app.unlock_items_page))
        self.assertEqual(len(app.unlock_flag_sections), 7)

    def test_folders_start_collapsed_and_preserve_buttons_when_reopened(self):
        app = self.app
        self._open_flags()
        section = ('Benkei & Kihachi', 'Unsorted')
        self.assertEqual(len(app.unlock_flag_widgets), 0)
        self.assertEqual(app.unlock_flag_expanded, set())
        self.assertIn('▸', app.unlock_flag_section_buttons[section].cget('text'))
        self._expand()
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertIn('▾', app.unlock_flag_section_buttons[section].cget('text'))
        app.toggle_unlock_flag_section(section)
        self.assertNotIn(section, app.unlock_flag_expanded)
        self.assertEqual(
            app.unlock_flag_section_bodies[section].winfo_manager(), '')
        app.toggle_unlock_flag_section(section)
        self.assertIn(section, app.unlock_flag_expanded)
        self.assertIs(app.unlock_flag_widgets['benkei_encounter'], widgets)

    def test_large_folder_uses_single_tree_with_direct_bit_actions_and_cached_rows(self):
        app = self.app
        app.mem = FakeRAM()
        self._open_flags()
        section = ('Fortune Dolls', 'Unsorted')
        rows = app.unlock_flag_section_rows[section]
        self.assertEqual(len(rows), 45)
        with patch.object(app, '_create_unlock_flag_row') as native_row:
            app.toggle_unlock_flag_section(section)
            native_row.assert_not_called()
        self.assertNotIn(section, app._unlock_flag_pending)
        self.assertNotIn(section, app._unlock_flag_jobs)
        table = app._unlock_flag_treeviews[section]
        self.assertEqual(len(table.get_children()), len(rows))
        self.assertFalse(any(flag.key in app.unlock_flag_widgets for flag in rows))
        first = rows[0]
        self.assertEqual(table.set(first.key, 'value'), 'Off')
        self.assertEqual(table.set(first.key, 'on'), 'On')
        self.assertEqual(table.set(first.key, 'off'), 'Off')
        before = app.mem.bytes[first.address]
        app._activate_unlock_flag_tree_cell(section, first.key, 'Set')
        self.assertEqual(app.mem.bytes[first.address], before | first.mask)
        self.assertEqual(table.set(first.key, 'value'), 'On')
        app._activate_unlock_flag_tree_cell(section, first.key, 'Clear')
        self.assertEqual(app.mem.bytes[first.address], before & ~first.mask)
        app.toggle_unlock_flag_section(section)
        self.assertNotIn(section, app.unlock_flag_expanded)
        app.toggle_unlock_flag_section(section)
        self.assertIs(table, app._unlock_flag_treeviews[section])
        self.assertEqual(len(table.get_children()), 45)
        self.assertEqual(app._unlock_flag_pending, {})

    def test_large_folder_single_tk_table_is_bounded_and_readonly(self):
        app = self.app
        app.mem = FakeRAM()
        self._open_flags()
        section = ('Fortune Dolls', 'Unsorted')
        app.toggle_unlock_flag_section(section)
        table = app._unlock_flag_treeviews[section]
        self.assertEqual(table.cget('height'), 14)
        # One Treeview and scrollbar, not hundreds of per-row Tk widgets.
        self.assertLess(len(table.winfo_children()), 5)
        key = app.unlock_flag_section_rows[section][0].key
        app.args.read_only = True
        app.refresh_unlock_flags(force=True)
        self.assertEqual(table.set(key, 'on'), '—')
        with patch.object(app, 'set_unlock_flag') as setter:
            app._activate_unlock_flag_tree_cell(section, key, 'Set')
            setter.assert_not_called()
        app.args.read_only = False
        app.refresh_unlock_flags(force=True)
        self.assertEqual(table.set(key, 'on'), 'On')
        table.selection_set(key)
        app._refresh_unlock_flag_tree_selection(section)
        off, on = app._unlock_flag_tree_buttons[section]
        self.assertNotIn('disabled', off.state())
        self.assertNotIn('disabled', on.state())

    def test_collapse_and_region_switch_discard_large_folder_tree(self):
        app = self.app
        self._open_flags()
        section = ('External annotations', 'Unsorted')
        app.toggle_unlock_flag_section(section)
        table = app._unlock_flag_treeviews[section]
        self.assertNotIn(section, app._unlock_flag_pending)
        app.toggle_unlock_flag_section(section)
        self.assertNotIn(section, app._unlock_flag_jobs)
        self.root.update()
        self.assertTrue(table.winfo_exists())
        app.toggle_unlock_flag_section(section)
        self.assertIs(table, app._unlock_flag_treeviews[section])
        self._select_japan()
        self.assertEqual(app._unlock_flag_treeviews, {})
        self.assertEqual(app._unlock_flag_tree_by_key, {})
        self.assertEqual(app._unlock_flag_tree_cache, {})
        self.assertIn('external_sasuke_recruited', app.unlock_flag_rows)
        self.root.update()
        self.assertFalse(table.winfo_exists())

    def test_search_filters_big_folder_without_creating_native_rows(self):
        app = self.app
        self._open_flags()
        section = ('Fortune Dolls', 'Unsorted')
        app.toggle_unlock_flag_section(section)
        table = app._unlock_flag_treeviews[section]
        self.assertEqual(len(table.get_children()), 45)
        with patch.object(app, '_create_unlock_flag_row') as native_row:
            app.unlock_flag_query.set('never-matches-this-flag')
            self.assertEqual(table.get_children(), ())
            self.assertNotIn(section, app._unlock_flag_pending)
            app.unlock_flag_query.set('fortune doll')
            self.assertGreater(len(table.get_children()), 0)
            app.unlock_flag_query.set('')
            self.assertEqual(len(table.get_children()), 45)
            native_row.assert_not_called()
        self.assertIs(table, app._unlock_flag_treeviews[section])

    def test_idle_tick_uses_reader_transition_not_forced_offline_refresh(self):
        app = self.app
        self.assertIsNone(app.mem)
        self.assertIsNone(app.jp_rdram)
        with (patch.object(app, '_watch_japan_process_restart'),
              patch.object(app, '_refresh_unlocks_on_reader_change') as poll,
              patch.object(app, 'refresh_unlocks') as refresh,
              patch.object(self.root, 'after')):
            app.tick()
            poll.assert_called_once_with()
            refresh.assert_not_called()

    def test_disconnected_controls_do_not_write(self):
        app = self.app
        self._open_flags()
        self._expand()
        widgets = app.unlock_flag_widgets['benkei_encounter']
        self.assertEqual(widgets['state'].get(), '—')
        self.assertIn('disabled', widgets['on'].state())
        self.assertIn('disabled', widgets['off'].state())
        self.assertIn('Disconnected', app.unlock_flag_feedback.get())


if __name__ == '__main__':
    unittest.main()
