"""Synthetic Tk test of Japanese Event Sessions > Advanced RAM Comparison."""
from argparse import Namespace
from pathlib import Path
import json
from tempfile import TemporaryDirectory
import time
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.game_versions import selected_version
from tests.test_japan_state_comparison import ReadOnlyJapanRam


class JapanAdvancedComparisonUiTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f'Tk display required: {exc}')
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        with patch('practice.japanese_fields_ui.practice_data_dir',
                   return_value=Path(self.temp.name)):
            self.app = Toolkit(
                self.root, Namespace(
                    pid=None, base=None, endian='auto', route=None,
                    enable_teleport=True, enable_state_restore=True,
                    enable_debug_menu=True, enable_hex_edit=True,
                    enable_scene_warp=False, game_version='usa',
                    read_only=False, enable_japan_party_writes=False))
        self.app.active_version = selected_version('japan')
        self.app.game_version_choice.set(self.app.active_version.label)
        self.app._apply_game_version_ui()
        self.app.jp_rdram = ReadOnlyJapanRam()
        self.app.game_pid = 123

    def _finish_capture(self):
        deadline = time.monotonic() + 5
        while self.app._jp_probe_busy and time.monotonic() < deadline:
            self.root.update()
            time.sleep(0.01)
        self.root.update()
        self.assertFalse(self.app._jp_probe_busy, self.app.state_probe_status.get())

    def test_jp_advanced_only_tab_and_candidate_watch(self):
        app = self.app
        self.assertEqual(app.notebook.tab(app.event_sessions_tab, 'state'), 'normal')
        self.assertEqual(app.event_sections.tab(app.event_sections.tabs()[0], 'state'),
                         'disabled')
        self.assertEqual(app.event_sections.select(), str(app.state_discovery_tab))
        self.assertEqual(app.notebook.tab(app.value_search_tab, 'state'), 'normal')
        self.assertEqual(app.notebook.tab(app.unlock_tab, 'state'), 'disabled')
        self.assertEqual(app.state_probe_kind.get(), 'Scene transition')
        app.state_probe_scope.set('focused')

        app.capture_state_probe('A')
        self._finish_capture()
        self.assertIn('A', app.state_captures)
        app.jp_rdram.set_bytes(0x80161DD7, b'\x01')
        app.capture_state_probe('B')
        self._finish_capture()
        app.compare_state_probes()
        self.assertEqual(app.state_report['region'], 'japan-0')
        self.assertEqual(app.state_report['counts']['candidate_count'], 1)
        self.assertIn('unmapped', app.state_probe_status.get())

        table = app.state_probe_table
        table.selection_set(table.get_children()[0])
        app.watch_state_probe_candidate()
        self.assertEqual(len(app.jp_custom_watches), 1)
        self.assertTrue(app.jp_custom_watches[0].name.startswith('JP A/B/C'))
        self.assertEqual(app.notebook.select(), str(app.jp_fields_tab))

        app._disconnect_for_version_change()
        self.assertFalse(app.state_captures)
        self.assertIsNone(app.state_report)
        self.assertIsNone(app.jp_rdram)

    def test_japan_wide_xyz_research_and_float_watch(self):
        from tests.test_japan_player_position_research import (
            FourMegabyteJapanRam, XYZ_ADDR, put_xyz,
        )
        app = self.app
        app.jp_rdram = FourMegabyteJapanRam()
        app.state_probe_kind.set('Player movement')
        app._set_state_probe_instruction()
        self.assertEqual(app.state_probe_capture_buttons['C'].cget('text'),
                         'Capture C: Still at B')
        app.state_probe_scope.set('wide')
        put_xyz(app.jp_rdram, XYZ_ADDR, (100.0, 20.0, -50.0))
        app.capture_state_probe('A')
        self._finish_capture()
        put_xyz(app.jp_rdram, XYZ_ADDR, (111.0, 20.0, -48.0))
        app.capture_state_probe('B')
        self._finish_capture()
        app.capture_state_probe('C')
        self._finish_capture()
        app.find_japan_xyz_from_captures()
        self._finish_capture()
        self.assertEqual(app.state_report['format'], 'goemon-japan-xyz-heuristic-v1')
        self.assertIn('candidate', app.state_probe_status.get())
        self.assertEqual(app.state_probe_table.heading('returned', 'text'),
                         'C stable at B?')
        with patch('practice.state_discovery_ui.diagnostics_dir',
                   return_value=Path(self.temp.name)):
            app.export_state_probe()
            self._finish_capture()
        exported_files = list(Path(self.temp.name).glob('japan_state_probe_*.json'))
        self.assertEqual(len(exported_files), 1)
        exported = json.loads(exported_files[0].read_text(encoding='utf-8'))
        self.assertEqual(exported['export_policy'], 'all_matched_candidates')
        self.assertEqual(exported['counts']['exported_candidates'],
                         app.state_report['counts']['candidate_count'])
        self.assertEqual(len(exported['candidates']),
                         exported['counts']['candidate_count'])
        self.assertIn('Exported ALL', app.state_probe_status.get())
        iid = next(i for i in app.state_probe_table.get_children()
                   if app.state_probe_table.item(i, 'values')[0]
                   == f'0x{XYZ_ADDR:08X}')
        app.state_probe_table.selection_set(iid)
        app.watch_state_probe_candidate()
        self.assertEqual(app.jp_custom_watches[-1].kind, 'f32')
        self.assertEqual(app.jp_custom_watches[-1].address, XYZ_ADDR)
        self.assertTrue(app.jp_custom_watches[-1].name.startswith('JP XYZ candidate'))

    def test_disallow_comparison_after_reconnect(self):
        app = self.app
        app.capture_state_probe('A')
        self._finish_capture()
        app.jp_rdram = ReadOnlyJapanRam()
        app.capture_state_probe('B')
        self._finish_capture()
        app.compare_state_probes()
        # Same PID/base/endian alone cannot prove continuous physical identity.
        # UI invalidates snapshots during the actual disconnect/reconnect path.
        self.assertIn('Different Japanese', app.state_probe_status.get())


if __name__ == '__main__':
    unittest.main()
