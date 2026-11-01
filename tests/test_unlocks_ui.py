"""Graphical unlock/sprites tab tests; run with Xvfb on Linux."""
from __future__ import annotations
import tkinter as tk
from argparse import Namespace
from unittest.mock import patch
import unittest

from practice.toolkit import Toolkit
from practice.unlocks import BY_ADDRESS, UNLOCKS
from tests.test_unlocks import FakeRAM


class TestUnlocksUI(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        self.app = Toolkit(self.root, Namespace(pid=None,base=None,endian='auto',route=None,
            enable_teleport=True, enable_state_restore=True, enable_debug_menu=True,
            enable_hex_edit=True, enable_scene_warp=False))

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_tabs_and_no_fictional_sprites(self):
        a = self.app
        self.assertEqual(a.notebook.tab(a.unlock_tab, 'text'), 'Unlocks')
        self.assertEqual(a.notebook.tab(a.sprite_tab, 'text'), 'Sprites')
        self.assertEqual(len(a.unlock_row_widgets), len(UNLOCKS))
        self.assertEqual(len(a.sprite_gallery_items), len(UNLOCKS))
        self.assertEqual(len(a.sprite_photos), 0)

    def test_button_writes_byte_without_confirmation_dialog(self):
        self.app.mem = FakeRAM()
        unlock = BY_ADDRESS[0x8015C6BF]
        with patch('tkinter.messagebox.askyesno', side_effect=AssertionError('confirmation dialog shown')):
            self.app.set_unlock(unlock, 2)
        self.assertEqual(self.app.mem.read_guest(unlock.address, 1), b'\x02')
        self.assertIn('verified', self.app.unlock_status.get())
        self.app.set_unlock(unlock, 0)
        self.assertEqual(self.app.mem.read_guest(unlock.address, 1), b'\x00')

    def test_sprite_card_toggle_behaves_correctly(self):
        self.app.mem = FakeRAM()
        field = BY_ADDRESS[0x8015C6C7]
        self.app.toggle_sprite_unlock(field)
        self.assertEqual(self.app.mem.read_guest(field.address, 1), b'\x01')
        self.app.toggle_sprite_unlock(field)
        self.assertEqual(self.app.mem.read_guest(field.address, 1), b'\x00')

    def test_disconnected_does_not_write(self):
        self.app.set_unlock(BY_ADDRESS[0x8015C6C7], 1)
        self.assertIn('Disconnected', self.app.unlock_status.get())


if __name__ == '__main__':
    unittest.main()
