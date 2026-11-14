"""Tk custom-watch workflow tests using fake game memory."""
import unittest
import tkinter as tk
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from practice.toolkit import Toolkit
from practice.custom_watches import load_watches
from practice.watch_names import load_watch_names
from types import SimpleNamespace
from tests.test_checkpoint import TestCheckpoint

class CustomWatchUITests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'custom_watches.json'
        mock=patch('practice.ui_extension.CUSTOM_WATCHES_PATH',self.path)
        mock.start()
        self.addCleanup(mock.stop)
        names_patch=patch('practice.ui_extension.WATCH_NAMES_PATH',
                          Path(self.tmp.name)/'watch_names.json')
        names_patch.start()
        self.addCleanup(names_patch.stop)
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.app=Toolkit(self.root,Namespace(pid=None,base=None,endian='auto',route=None,
            enable_teleport=True,enable_state_restore=True,enable_debug_menu=True,
            enable_hex_edit=True,enable_scene_warp=False))

    def test_add_read_and_remove(self):
        app=self.app
        app.user_watch_name.set('Map trigger')
        app.user_watch_address.set('0x8015C574')
        app.user_watch_type.set('u8')
        app.add_custom_watch()
        self.assertEqual(len(load_watches(self.path)),1)
        _,ram=TestCheckpoint().sample()
        ram.write_guest(0x8015C574,b'\x7A')
        app.mem=ram
        app.current=ram.snapshot()
        app.last_inspect_at=0
        app.refresh_inspector(app.current)
        self.assertEqual(app.watch_tree.item('Custom: Map trigger','values')[2],'0x7A')
        app.watch_tree.selection_set('Custom: Map trigger')
        app.remove_custom_watch()
        self.assertEqual(load_watches(self.path),[])

    def test_right_click_rename_custom_watch_persists_and_remains_removable(self):
        app=self.app
        app.user_watch_name.set('Map trigger')
        app.user_watch_address.set('0x8015C574')
        app.user_watch_type.set('u8')
        app.add_custom_watch()
        with patch('practice.ui_extension.simpledialog.askstring',return_value='Trigger flag'):
            app.rename_live_watch('Custom: Map trigger')
        self.assertEqual([w.name for w in load_watches(self.path)],['Trigger flag'])
        self.assertTrue(app.watch_tree.exists('Custom: Trigger flag'))
        self.assertFalse(app.watch_tree.exists('Custom: Map trigger'))
        app.watch_tree.selection_set('Custom: Trigger flag')
        app.remove_custom_watch()
        self.assertEqual(load_watches(self.path),[])

    def test_built_in_alias_persists_without_changing_original_id(self):
        app=self.app
        _,ram=TestCheckpoint().sample()
        app.mem=ram
        app.current=ram.snapshot()
        app.refresh_inspector(app.current)
        self.assertTrue(app.watch_tree.exists('Ryo'))
        with patch('practice.ui_extension.simpledialog.askstring',return_value='Cash'):
            app.rename_live_watch('Ryo')
        self.assertEqual(app.watch_tree.item('Ryo','text'),'Cash')
        self.assertEqual(load_watch_names(Path(self.tmp.name)/'watch_names.json'),{'Ryo':'Cash'})
        self.assertIn('Ryo',[w.name for w in app.watch_rows])
        self.assertEqual(app.quick_watch_tree.item('Ryo','values')[0],'Cash')
        app.filter_text.set('Cash')
        self.assertTrue(app.watch_tree.exists('Ryo'))
        with patch('practice.ui_extension.simpledialog.askstring',return_value=''):
            app.rename_live_watch('Ryo')
        self.assertEqual(app.watch_tree.item('Ryo','text'),'Ryo')
        self.assertEqual(load_watch_names(Path(self.tmp.name)/'watch_names.json'),{})

    def test_context_menu_selects_actual_clicked_row_not_previous_selection(self):
        app=self.app
        _,ram=TestCheckpoint().sample()
        app.mem=ram
        app.current=ram.snapshot()
        app.refresh_inspector(app.current)
        app.watch_tree.selection_set('Lives')
        event=SimpleNamespace(y=11,x_root=40,y_root=50)
        with patch.object(app.watch_tree,'identify_row',return_value='Ryo'), \
             patch.object(app.watch_context_menu,'tk_popup'):
            self.assertEqual(app.open_live_watch_menu(event),'break')
        self.assertEqual(app.watch_tree.selection(),('Ryo',))
        self.assertEqual(app.watch_context_menu.entrycget(0,'label'),'Freeze value')
        self.assertEqual(app.watch_context_menu.entrycget(1,'label'),'Rename field…')

    def test_state_discovery_adds_watch(self):
        app=self.app
        app.state_probe_table.insert('','end',iid='0',values=(
            '0x8015C574','game_data','00','01','01','yes','boolean'))
        app.state_probe_table.selection_set('0')
        app.watch_state_probe_candidate()
        self.assertEqual(app.custom_watches[0].address,0x8015C574)
        self.assertEqual(app.notebook.select(),str(app.live_memory_tab))

if __name__ == '__main__': unittest.main()
