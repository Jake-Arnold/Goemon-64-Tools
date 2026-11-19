"""Evidence and safe native line-capacity inference for USA dialogue windows."""
from __future__ import annotations

import os
import unittest

from practice.dialogue_rom import DialogueRecord, encode_text, extract_dialogue, load_usa_image
from practice.dialogue_window import (
    styles_from_rom, style_for_record, window_context_for_record,
)


class NativeWindowSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image = load_usa_image(source)
        cls.records = extract_dialogue(cls.image)

    def test_native_style_table_height_not_texture_width(self):
        styles = styles_from_rom(self.image)
        self.assertEqual(len(styles), 12)
        self.assertEqual([s.max_full_lines for s in styles],
                         [4, 4, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4])
        self.assertEqual(styles[5].texture_stride, 256)
        self.assertEqual(styles[5].background_height, 40)

    def test_kai_area_has_only_one_line_after_heading(self):
        name = next(r for r in self.records if r.resource_id == 82 and r.text_offset == 0x1C)
        heading = next(r for r in self.records if r.resource_id == 82 and r.text_offset == 0x4)
        self.assertEqual(name.references, (0x60,))
        self.assertEqual(heading.references, (0x58,))
        self.assertEqual(style_for_record(self.image, name).index, 5)
        self.assertEqual(window_context_for_record(self.image, heading).starting_line, 0)
        context = window_context_for_record(self.image, name)
        self.assertEqual(context.starting_line, 1)
        self.assertEqual(context.remaining_lines, 1)
        self.assertEqual(context.style.max_full_lines, 2)

    def test_unknown_or_untraced_reference_does_not_claim_a_style(self):
        unknown = DialogueRecord(82, 0x1C, 0, encode_text('Highway'), (0x80,))
        self.assertIsNone(window_context_for_record(self.image, unknown))
        self.assertIsNone(style_for_record(self.image, unknown))

    def test_native_height_is_source_guarded(self):
        changed = bytearray(self.image)
        # 36-byte style records at 0x633F0. Do not accept a different
        # unvalidated row as evidence for an automatic native cap.
        changed[0x633F0 + 5 * 36 + 16] = 0xFF
        with self.assertRaisesRegex(ValueError, 'Unrecognized'):
            styles_from_rom(bytes(changed))


@unittest.skipUnless(os.environ.get('DISPLAY'), 'Requires Xvfb')
class NativeWindowUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image = load_usa_image(source)
        cls.rec = next(r for r in extract_dialogue(cls.image)
                       if r.resource_id == 82 and r.text_offset == 0x1C)

    def setUp(self):
        import tkinter as tk
        from tkinter import ttk
        from practice.dialogue_ui import DialogueMixin
        from practice.dialogue_layout import font_widths_from_rom
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = type('Ui', (DialogueMixin,), {})()
        self.app.root = self.root
        self.app.build_dialogue_tab(ttk.Notebook(self.root))
        self.app.dialogue_original_image = self.image
        self.app.dialogue_font_widths = font_widths_from_rom(self.image)
        self.app.dialogue_records = [self.rec]
        self.app.dialogue_by_key = {self.rec.key: self.rec}
        self.app.dialogue_tree.insert('', 'end', iid=self.rec.key,
                                      values=(82, '0x1C', 1, self.rec.text))
        self.app.dialogue_tree.selection_set(self.rec.key)
        self.app._dialogue_select()

    def tearDown(self):
        self.root.destroy()

    def test_native_line_warning_wins_over_manual_twenty(self):
        app = self.app
        app.dialogue_layout_mode.set('Multi-line (manual cap)')
        app.dialogue_width_limit.set('120')
        app.dialogue_line_limit.set('20')
        app.dialogue_editor.delete('1.0', 'end')
        app.dialogue_editor.insert('1.0', 'Many\nmany\nlines\nthat are\nsupposed\nto wrap\nbut may\nnot wrap')
        app._dialogue_analyze()
        msg = app.dialogue_layout_summary.get()
        self.assertIn('Native style 5:', msg)
        self.assertIn('starts on line 2, 1 remaining', msg)
        self.assertIn('exceeds user limit 1', msg)
        self.assertIn('conservative advance cap 135 units', msg)

    def test_wrap_cannot_create_more_native_lines(self):
        from unittest.mock import patch
        app = self.app
        app.dialogue_layout_mode.set('Multi-line (manual cap)')
        app.dialogue_width_limit.set('100')
        app.dialogue_line_limit.set('20')
        app.dialogue_editor.delete('1.0', 'end')
        app.dialogue_editor.insert('1.0', 'Monster Monster Monster')
        with patch('practice.dialogue_ui.messagebox.showerror') as error:
            app._dialogue_wrap()
        error.assert_called_once()
        self.assertNotIn(self.rec.key, app.dialogue_line_break_approved)


if __name__ == '__main__':
    unittest.main()

class NativeControlEffectsTests(unittest.TestCase):
    """Source-anchored control helper fields, not guessed visual semantics."""

    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image = load_usa_image(source)

    def test_selected_native_mask_instructions(self):
        import struct
        def word(vma):
            return struct.unpack_from('>I', self.image, vma - 0x7FFFF400)[0]
        # Clear +0x1C bit 0x10 (C640), set (C60C).
        self.assertEqual(word(0x8000C668), 0x2401FFEF)
        self.assertEqual(word(0x8000C62C), 0x37290010)
        # Clear +0x1C bit 0x08 (C5A4), set (C570).
        self.assertEqual(word(0x8000C5CC), 0x2401FFF7)
        self.assertEqual(word(0x8000C590), 0x37290008)
        # Halfword +0x70 and a float field +0x88.
        self.assertEqual(word(0x8000C448), 0xA4450070)
        self.assertEqual(word(0x8000C600), 0xE44C0088)

    def test_negative_control_diagnostics_named_but_not_visual_claims(self):
        from practice.dialogue_layout import CONTROL_NOTES, OPAQUE_LAYOUT_TOKENS
        self.assertEqual(set(range(-57, -49)), OPAQUE_LAYOUT_TOKENS)
        for t in range(-57, -49):
            self.assertIn('window', CONTROL_NOTES[t])
        self.assertIn('bit 0x10', CONTROL_NOTES[-57])
        self.assertIn('bit 0x02', CONTROL_NOTES[-50])
