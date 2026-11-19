"""Original-USA CI4 window-art and renderer-geometry regression tests."""
from __future__ import annotations
import os
import struct
import unittest
from unittest.mock import patch
from practice.dialogue_rom import extract_dialogue, encode_text, load_usa_image
from practice.dialogue_window import styles_from_rom, window_context_for_record
from practice.dialogue_layout import font_widths_from_rom, inspect_layout, wrap_plain_dialogue


class NativeHorizontalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image = load_usa_image(source)
        cls.records = extract_dialogue(cls.image)
        cls.styles = styles_from_rom(cls.image)
        cls.widths = font_widths_from_rom(cls.image)

    def test_visible_art_widths_are_not_the_256_stride(self):
        self.assertEqual([s.artwork_width for s in self.styles],
                         [256,256,160,160,160,160,256,256,256,256,256,256])
        self.assertTrue(all(s.texture_stride == 256 for s in self.styles))
        self.assertEqual([s.inner_right_x for s in self.styles],
                         [252,252,156,156,156,156,252,252,252,252,252,252])

    def test_native_glyph_inset_and_conservative_width_cap(self):
        for s in self.styles:
            self.assertEqual(s.text_x_inset, 14)
            self.assertEqual(s.glyph_box_width, 10)
            self.assertEqual(s.safe_advance_limit, s.artwork_width - 25)
            self.assertEqual(s.inner_right_x - s.text_x_inset -
                             s.glyph_box_width + min(self.widths) + 1,
                             s.safe_advance_limit)

    def test_kai_edited_overflows_original_artwork(self):
        record = next(r for r in self.records if r.resource_id == 82 and r.text_offset == 0x1C)
        ctx = window_context_for_record(self.image, record)
        self.assertIsNotNone(ctx)
        self.assertEqual((ctx.style.index,ctx.style.artwork_width,ctx.remaining_lines), (5,160,1))
        original=inspect_layout(record.tokens,self.widths,max_width=ctx.style.safe_advance_limit,max_lines=1,width_source='native safe')
        self.assertEqual(original.longest_line, 122)
        self.assertFalse(original.messages)
        change=inspect_layout(encode_text('Monster Monster Monster'),self.widths,max_width=ctx.style.safe_advance_limit,max_lines=1,width_source='native safe')
        self.assertEqual(change.longest_line,165)
        self.assertTrue(any('Width exceeds native safe limit' in msg for msg in change.messages))

    def test_native_glyph_position_and_box_size_original_mips(self):
        def word(vma):
            return struct.unpack_from('>I',self.image,vma-0x7FFFF400)[0]
        self.assertEqual(word(0x8000D0A0),0x8C790050)  # window +0x50=10
        self.assertEqual(word(0x8000D0A4),0x8468006E)  # x advance +0x6E
        self.assertEqual(word(0x8000D1E0),0x254B0004)  # glyph entry x adds 4
        self.assertEqual(word(0x8000D1D0),0x240E000A)  # entry glyph box 10px
        self.assertEqual(word(0x8000C7A8),0xAC580050)  # init x offset 10
        self.assertEqual(word(0x8000C810),0xA444003E)  # style stride separate from alpha width

    def test_tlut_alpha_mutant_rejected(self):
        changed=bytearray(self.image)
        # Make the original palette's transparent index 2 nontransparent.
        # This would falsely extend 160px artwork to 256px without checks;
        # fail closed when the computed artwork width disagrees with border.
        off=0x80062790 - 0x7FFFF400 + 4
        changed[off:off+2] = (1).to_bytes(2,'big')
        with self.assertRaisesRegex(ValueError, 'border|Unrecognized|glyph'):
            styles_from_rom(changed)

    def test_word_wrapping_with_native_limit_still_bounded(self):
        tokens=encode_text('Monster Monster Monster')
        with self.assertRaisesRegex(ValueError,'more than 1 lines'):
            wrap_plain_dialogue(tokens,self.widths,max_width=135,max_lines=1)
        wrapped=wrap_plain_dialogue(tokens,self.widths,max_width=135,max_lines=2)
        self.assertEqual(wrapped.count(-60),1)
        result=inspect_layout(wrapped,self.widths,max_width=135,max_lines=2)
        self.assertFalse(result.messages)


@unittest.skipUnless(os.environ.get('DISPLAY'),'Tk needs Xvfb')
class NativeHorizontalUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image=load_usa_image(source)
        cls.record=next(r for r in extract_dialogue(cls.image) if r.resource_id==82 and r.text_offset==0x1C)

    def setUp(self):
        import tkinter as tk
        from tkinter import ttk
        from practice.dialogue_ui import DialogueMixin
        self.root=tk.Tk();self.root.withdraw()
        self.app=type('DialogueApp',(DialogueMixin,),{})()
        self.app.root=self.root
        self.app.build_dialogue_tab(ttk.Notebook(self.root))
        self.app.dialogue_original_image=self.image
        self.app.dialogue_font_widths=font_widths_from_rom(self.image)
        self.app.dialogue_records=[self.record]
        self.app.dialogue_by_key={self.record.key:self.record}
        self.app.dialogue_tree.insert('', 'end', iid=self.record.key, values=(82,'0x1C',1,self.record.text))
        self.app.dialogue_tree.selection_set(self.record.key)
        self.app._dialogue_select()

    def tearDown(self):
        self.root.destroy()

    def test_auto_mode_uses_native_width_without_manual_entries(self):
        app=self.app
        self.assertEqual(app.dialogue_layout_mode.get(),'Native (auto when traced)')
        self.assertIn('disabled',app.dialogue_width_entry.state())
        self.assertIn('disabled',app.dialogue_line_entry.state())
        self.assertIn('conservative advance cap 135 units',app.dialogue_layout_summary.get())
        app.dialogue_editor.delete('1.0','end')
        app.dialogue_editor.insert('1.0','Monster Monster Monster')
        app._dialogue_analyze()
        self.assertIn('Width exceeds native safe limit',app.dialogue_layout_summary.get())

    def test_user_cannot_override_original_window_bound(self):
        app=self.app
        app.dialogue_layout_mode.set('Multi-line (manual cap)')
        self.assertNotIn('disabled',app.dialogue_width_entry.state())
        app.dialogue_width_limit.set('400')
        app.dialogue_line_limit.set('20')
        app.dialogue_editor.delete('1.0','end')
        app.dialogue_editor.insert('1.0','Monster Monster Monster')
        app._dialogue_analyze()
        self.assertIn('Width exceeds native safe limit',app.dialogue_layout_summary.get())
        with patch('practice.dialogue_ui.messagebox.showerror') as error:
            app._dialogue_wrap()
        error.assert_called_once()

    def test_auto_mode_rejects_wrap_for_one_line_area_name(self):
        with patch('practice.dialogue_ui.messagebox.showerror') as error:
            self.app._dialogue_wrap()
        error.assert_called_once()
        self.assertNotIn(self.record.key,self.app.dialogue_line_break_approved)

if __name__ == '__main__': unittest.main()
