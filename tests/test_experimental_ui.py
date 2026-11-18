"""Tk smoke tests for deliberately separated experimental buttons."""
import unittest
import tkinter as tk
from argparse import Namespace
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.checkpoints import STATE_ADDR
from practice.scene_controls import PENDING_MAP_ADDR
from practice.entrances import SCHEMA,US_RETAIL_SHA1,digest
from tests.test_checkpoint import TestCheckpoint

class TestExperimentalGUI(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()
        self.app=Toolkit(self.root,Namespace(pid=None,base=None,endian='auto',route=None,
            enable_teleport=True,enable_state_restore=True,enable_debug_menu=True,
            enable_hex_edit=True,enable_scene_warp=False))
        _,self.ram=TestCheckpoint().sample()
        self.app.mem=self.ram
        self.ram.write_guest(PENDING_MAP_ADDR,(35).to_bytes(2,'big'))
        payload=dict(format=SCHEMA,rom_sha1=US_RETAIL_SHA1,rooms=[35,353],entries=[dict(id='test',kind='exit',source_map=35,source_file=0x337,definition=0,exit_id=1,destination=353,position=[95,0,-350],heading=0x300,mode=0x10)])
        self.app.entrance_atlas={'payload':payload,'sha256':digest(payload)}
        self.app.scene_list.delete(0,'end')

    def tearDown(self):
        if hasattr(self,'root'):self.root.destroy()

    def test_removed_ineffective_movement_buttons_and_f1_opens_memory(self):
        self.assertFalse(hasattr(self.app, 'try_motion_pulse'))
        tab=self.app.live_memory_tab
        self.app.notebook.select(self.app.scene_tab)
        self.assertEqual(self.app._on_f1_open_memory(), 'break')
        self.assertEqual(self.app.notebook.select(), str(tab))
        self.assertTrue(self.root.bind_all('<F1>'))

    def test_character_staged_before_reload_no_c_down_and_verified_on_entry(self):
        from practice.checkpoints import MAP_ADDR
        from autosplitter.memory import CHARACTER_ID_ADDR
        self.app.scene_character.current(3)  # Sasuke in shared Keep/0/1/2/3 selector
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):
            self.app.try_reload_warp()
        pending=self.app.pending_direct_warp
        self.assertEqual(pending['selected_character'],2)
        self.assertTrue(pending['character_staged'])
        self.assertEqual(self.ram.u32(CHARACTER_ID_ADDR),2)
        self.assertEqual(self.ram.u8(STATE_ADDR),12)
        self.ram.write_guest(MAP_ADDR,(353).to_bytes(2,'big'))
        self.ram.write_guest(STATE_ADDR,b'\x0d')
        self.ram.write_guest(self.ram.snapshot()['task_ptr']+0x60,b'\x02')
        with patch('practice.native_character.press_native_c_down',side_effect=AssertionError('NO C-Down permitted')):
            for dt in (1,1.2,1.4):
                self.app.poll_direct_warp(pending['start_at']+dt)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('Character verified',self.app.scene_status.get())
        self.assertEqual(self.ram.snapshot()['x'],95)

    def test_wrong_spawn_character_is_reported_without_postload_input(self):
        from practice.checkpoints import MAP_ADDR
        from autosplitter.memory import CHARACTER_ID_ADDR
        self.app.scene_character.current(4)  # Yae in shared Keep/0/1/2/3 selector
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):
            self.app.try_reload_warp()
        pending=self.app.pending_direct_warp
        self.ram.write_guest(MAP_ADDR,(353).to_bytes(2,'big'))
        self.ram.write_guest(STATE_ADDR,b'\x0d')
        self.ram.write_guest(CHARACTER_ID_ADDR,(0).to_bytes(4,'big'))
        self.ram.write_guest(self.ram.snapshot()['task_ptr']+0x60,b'\x00')
        with patch('practice.native_character.press_native_c_down',side_effect=AssertionError('NO C-Down permitted')):
            for dt in (1,1.2,1.4,16):
                self.app.poll_direct_warp(pending['start_at']+dt)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('timed out',self.app.scene_status.get())
        self.assertAlmostEqual(self.ram.snapshot()['x'],125.25)
        self.assertEqual(self.ram.u32(CHARACTER_ID_ADDR),0)

    def test_scene_banner_is_same_for_both_regions_without_player_pointer(self):
        from practice.game_versions import VERSIONS
        from practice.checkpoints import MAP_ADDR
        from autosplitter.memory import PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR
        from tests.test_unlocks import FakeRAM
        self.ram.write_guest(MAP_ADDR, (0x161).to_bytes(2, 'big'))
        self.ram.write_guest(PLAYER_OBJECT_PTR_ADDR, bytes(4))
        self.ram.write_guest(PLAYER_TASK_PTR_ADDR, bytes(4))
        self.app.refresh_scene_banner(force=True)
        original = self.app.scene_live.get()
        self.assertTrue(original.startswith('Current map: 353 (0x161): '))

        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        japan = FakeRAM()
        japan.bytes[0x800CD2A2] = 0x01
        japan.bytes[0x800CD2A3] = 0x61
        self.app.jp_rdram = japan
        self.app.refresh_scene_banner(force=True)
        self.assertEqual(self.app.scene_live.get(), original)

    def test_both_regions_share_keep_current_character_option(self):
        from practice.game_versions import VERSIONS
        expected = ('Keep current character', 'Goemon', 'Ebisumaru',
                    'Sasuke', 'Yae')
        self.assertEqual(tuple(self.app.scene_character['values']), expected)
        self.assertEqual(self.app.scene_character.current(), 0)
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.assertEqual(tuple(self.app.scene_character['values']), expected)
        self.assertEqual(self.app.scene_character.current(), 0)

    def test_double_click_reloads_without_confirmation(self):
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):
            self.assertEqual(self.app.activate_selected_scene(), 'break')
        self.assertEqual(self.ram.u8(STATE_ADDR),12)
        self.assertEqual(self.ram.u16(PENDING_MAP_ADDR),353)
        self.assertIsNotNone(self.app.pending_direct_warp)

    def test_impact_no_player_doubleclick_stages_reload(self):
        from practice.checkpoints import SUBMODE_ADDR
        from autosplitter.memory import (
            PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR)
        self.ram.write_guest(SUBMODE_ADDR, bytes([4]))
        self.ram.write_guest(PLAYER_OBJECT_PTR_ADDR, bytes(4))
        self.ram.write_guest(PLAYER_TASK_PTR_ADDR, bytes(4))
        self.app.scene_options = [(353, 'Destination')]
        self.app.scene_list.insert('end', 'Destination')
        self.app.scene_list.selection_set(0)
        with patch('practice.ui_extension.messagebox.askyesno',
                   side_effect=AssertionError('No modal on doubleclick')):
            self.assertEqual(
                self.app.activate_selected_scene(), 'break')
        pending = self.app.pending_direct_warp
        self.assertIsNotNone(pending, self.app.scene_status.get())
        self.assertEqual(self.ram.u8(STATE_ADDR), 12)
        self.assertEqual(self.ram.u16(PENDING_MAP_ADDR), 353)
        self.assertIsNone(pending['placement'].source_player)
        self.assertIsNone(pending['placement'].source_task)

    def test_enter_debug_menu_requires_no_destination_and_never_stages_warp(self):
        self.assertFalse(self.app.scene_list.curselection())
        from practice.checkpoints import MAP_ADDR
        before = self.ram.u16(MAP_ADDR)
        with patch.object(self.app, 'open_debug_for_selected_scene',
                          side_effect=AssertionError('Destination-specific path')):
            self.app.enter_debug_menu()
        self.assertEqual(self.ram.u8(STATE_ADDR),10)
        self.assertEqual(self.ram.u16(MAP_ADDR),before)
        self.assertIsNone(self.app.pending_native_warp)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('0x0A', self.app.scene_status.get())

    def test_read_only_blocks_both_scene_routes(self):
        self.app.scene_options=[(353,'Test destination')]
        self.app.scene_list.insert('end','Test destination')
        self.app.scene_list.selection_set(0)
        self.app.args.read_only=True
        with patch.object(self.ram, 'write_guest', side_effect=AssertionError('No guest writes')):
            self.app.activate_selected_scene()
            self.app.open_debug_for_selected_scene()
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIsNone(self.app.pending_native_warp)
        self.assertEqual(self.ram.u8(STATE_ADDR),13)

if __name__=='__main__':unittest.main()
