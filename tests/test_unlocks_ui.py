"""Graphical unlock tab tests; run with Xvfb on Linux."""
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

    def test_unlock_tab_without_sprites_tab(self):
        app = self.app
        self.assertEqual(app.notebook.tab(app.unlock_tab, 'text'), 'Unlocks')
        self.assertNotIn('Sprites', [app.notebook.tab(tab, 'text') for tab in app.notebook.tabs()])
        self.assertEqual(len(app.unlock_row_widgets), len(UNLOCKS))
        self.assertEqual(len(app.unlock_count_entries), 3)

    def test_button_writes_byte_without_confirmation_dialog(self):
        self.app.mem = FakeRAM()
        unlock = BY_ADDRESS[0x8015C6BF]
        with patch('tkinter.messagebox.askyesno', side_effect=AssertionError('confirmation dialog shown')):
            self.app.set_unlock(unlock, 2)
        self.assertEqual(self.app.mem.read_guest(unlock.address, 1), b'\x02')
        self.assertIn('verified', self.app.unlock_status.get())
        self.app.set_unlock(unlock, 0)
        self.assertEqual(self.app.mem.read_guest(unlock.address, 1), b'\x00')

    def test_refresh_handles_windows_combobox_popdown_focus(self):
        self.app.mem = FakeRAM()
        with patch.object(self.root, 'focus_get', side_effect=KeyError('popdown')):
            self.app.refresh_unlocks(force=True)
        self.assertIn('0x00', [state.cget('text')
                        for state, _controls in self.app.unlock_row_widgets.values()])

    def test_fish_count_widget_accepts_hex_and_clamps_to_minigame_max(self):
        self.app.mem = FakeRAM()
        caps={0x8015C71B:8,0x8015C723:3,0x8015C71F:5}
        for address,cap in caps.items():
            field=BY_ADDRESS[address]
            self.assertIn(field.address,self.app.unlock_count_inputs)
            self.app.set_unlock_hex(field,'FF')
            self.assertEqual(self.app.mem.read_guest(field.address,1),bytes((cap,)))
            self.app.set_unlock_hex(field,'1FF')
            self.assertEqual(self.app.mem.read_guest(field.address,1),bytes((cap,)))

    def test_unsafe_live_raw_write_any_hex(self):
        self.app.mem = FakeRAM()
        self.app.hex_advanced.set(True)
        self.app.raw_address.set('8015C5E8')
        self.app.raw_width.set('4')
        self.app.raw_value.set('DEADBEEF')
        self.app.write_raw_hex()
        self.assertEqual(self.app.mem.read_guest(0x8015C5E8,4),bytes.fromhex('DEADBEEF'))
        self.app.hex_advanced.set(False)
        self.app.raw_value.set('AABBCCDD')
        self.app.write_raw_hex()
        self.assertEqual(self.app.mem.read_guest(0x8015C5E8,4),bytes.fromhex('DEADBEEF'))

    def test_first_battery_toggle_preserves_other_event_bits(self):
        self.app.mem=FakeRAM()
        addr=0x8015C609
        self.app.mem.bytes[addr]=0x85
        item=BY_ADDRESS[addr]
        self.app.set_unlock(item,1)
        self.assertEqual(self.app.mem.bytes[addr],0xA5)
        self.app.set_unlock(item,0)
        self.assertEqual(self.app.mem.bytes[addr],0x85)

    def test_disconnected_does_not_write(self):
        self.app.set_unlock(BY_ADDRESS[0x8015C6C7], 1)
        self.assertIn('Disconnected', self.app.unlock_status.get())


if __name__ == '__main__':
    unittest.main()
