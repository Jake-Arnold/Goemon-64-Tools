"""Headless Tk integration checks for manual-cap text diagnostics and wrapping."""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from practice.dialogue_rom import DialogueRecord, encode_text
from practice.dialogue_layout import font_widths_from_rom
from practice.dialogue_ui import DialogueMixin


@unittest.skipUnless(os.environ.get('DISPLAY'), 'Run under Xvfb')
class DialogueLayoutUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        from pathlib import Path
        cls.rom_bytes = Path(source).read_bytes()

    def setUp(self):
        import tkinter as tk
        from tkinter import ttk
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = type('TestDialogueApp', (DialogueMixin,), {})()
        self.app.root = self.root
        self.app.build_dialogue_tab(ttk.Notebook(self.root))
        rec = DialogueRecord(96, 4, 0x74ECF0, encode_text('Monster Monster Monster') + (-61,), (0x100,))
        self.record = rec
        self.app.dialogue_font_widths = font_widths_from_rom(self.rom_bytes)
        self.app.dialogue_records = [rec]
        self.app.dialogue_by_key = {rec.key: rec}
        self.app.dialogue_selected_key = rec.key
        self.app.dialogue_editor.insert('1.0', rec.text)
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_live_report_warns_for_manually_defined_one_line_window(self):
        self.app.dialogue_layout_mode.set('Single-line (manual cap)')
        self.app.dialogue_width_limit.set('100')
        self.app._dialogue_analyze()
        self.assertIn('165 units', self.app.dialogue_layout_summary.get())
        self.assertIn('Controls: -61: state 3', self.app.dialogue_layout_summary.get())
        self.assertIn('Width exceeds user limit', self.app.dialogue_layout_summary.get())
        self.assertEqual(self.app.dialogue_line_break_approved, set())

    def test_multi_line_wrap_and_stage_explicit_authorization(self):
        self.app.dialogue_layout_mode.set('Multi-line (manual cap)')
        self.app.dialogue_width_limit.set('115')
        self.app.dialogue_line_limit.set('2')
        self.app._dialogue_wrap()
        self.assertIn('\n', self.app.dialogue_editor.get('1.0', 'end-1c'))
        self.assertIn(self.record.key, self.app.dialogue_line_break_approved)
        self.app._dialogue_stage()
        self.assertIn(self.record.key, self.app.dialogue_staged)
        self.app._dialogue_revert()
        self.assertNotIn(self.record.key, self.app.dialogue_staged)
        self.assertNotIn(self.record.key, self.app.dialogue_line_break_approved)

    def test_single_line_wrap_is_rejected(self):
        self.app.dialogue_layout_mode.set('Single-line (manual cap)')
        self.app.dialogue_width_limit.set('90')
        with patch('practice.dialogue_ui.messagebox.showerror') as error:
            self.app._dialogue_wrap()
        error.assert_called_once()
        self.assertEqual(self.app.dialogue_line_break_approved, set())


if __name__ == '__main__':
    unittest.main()
