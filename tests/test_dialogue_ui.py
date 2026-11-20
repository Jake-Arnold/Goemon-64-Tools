"""Tk Dialogue tab smoke tests; display-dependent checks skip without DISPLAY."""
from __future__ import annotations
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from practice.dialogue_ui import DialogueMixin


@unittest.skipUnless(os.environ.get('DISPLAY'), 'Tk UI requires a display or Xvfb')
class DialogueTabTests(unittest.TestCase):
    def setUp(self):
        import tkinter as tk
        from tkinter import ttk
        self.tk = tk
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = type('DemoDialogueApp', (DialogueMixin,), {})()
        self.app.root = self.root
        self.app.build_dialogue_tab(ttk.Notebook(self.root))
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_controls_and_original_retail_selection(self):
        self.assertEqual(self.app.dialogue_retail_build_button.cget('text'),
                         'Build retail .z64')
        self.assertIsNone(self.app.dialogue_retail_path)
        self.assertFalse(self.app.dialogue_build_running)

    def test_longer_staged_text_and_background_build(self):
        from practice.dialogue_rom import DialogueRecord
        old = DialogueRecord(97, 4, 0x759DF4, (57, 65, 69), (0x9608,))
        self.app.dialogue_records = [old]
        self.app.dialogue_by_key = {old.key: old}
        self.app.dialogue_selected_key = old.key
        self.app.dialogue_editor.insert('1.0', 'Yae and some more text')
        self.app._dialogue_stage()
        self.assertIn(old.key, self.app.dialogue_staged)
        self.app.dialogue_path = Path('/home/test/decompressed.z64')
        self.app.dialogue_retail_path = Path('/home/test/retail.z64')
        with tempfile.TemporaryDirectory() as folder:
            target = str(Path(folder) / 'mod.z64')
            with patch('practice.dialogue_ui.filedialog.asksaveasfilename',
                       return_value=target), patch(
                       'practice.dialogue_ui.save_retail_rom', return_value='a' * 40) as repack:
                self.app._dialogue_build_retail()
                self.assertTrue(self.app.dialogue_build_running)
                deadline = time.monotonic() + 5
                while self.app.dialogue_build_running and time.monotonic() < deadline:
                    self.root.update()
                    time.sleep(.02)
                self.assertFalse(self.app.dialogue_build_running)
                repack.assert_called_once()
                self.assertIn('Built 16 MiB retail', self.app.dialogue_status.get())
                self.assertNotIn('disabled', self.app.dialogue_retail_build_button.state())


if __name__ == '__main__':
    unittest.main()
