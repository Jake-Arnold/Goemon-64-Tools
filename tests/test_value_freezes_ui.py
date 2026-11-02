import tkinter as tk
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from practice.toolkit import Toolkit,parse_args
from tests import test_checkpoint


class ValueFreezeUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw();self.app=Toolkit(self.root,parse_args([]))
        self.process,self.app.mem=test_checkpoint.TestCheckpoint().sample()
        self.app.game_pid=123

    def tearDown(self):
        self.root.destroy()

    def test_defaults_inactive_raw_freeze_stop_and_health_toggle(self):
        app=self.app
        self.assertFalse(app.freeze_health.get());self.assertFalse(app.value_freezes.locks)
        app.raw_address.set('8015C63B');app.raw_width.set('1');app.raw_value.set('10')
        app.freeze_raw_value();app.poll_value_freezes()
        self.assertEqual(app.mem.u8(0x8015C63B),16)
        self.assertEqual(len(app.freeze_tree.get_children()),1)
        app.freeze_tree.selection_set(str(0x8015C63B));app.stop_selected_freeze()
        self.assertFalse(app.value_freezes.locks)
        app.freeze_health.set(True);app.toggle_freeze_health();app.poll_value_freezes()
        self.assertEqual(app.mem.u32(0x8015C5E4),10)
        app.stop_all_freezes();self.assertFalse(app.freeze_health.get())

    def test_read_only_blocks_both_entry_paths_and_disconnect_clears_controls(self):
        app=self.app;app.freeze_health.set(True);app.toggle_freeze_health()
        app.mem=None;app.poll_value_freezes()
        self.assertFalse(app.freeze_health.get())
        _,app.mem=test_checkpoint.TestCheckpoint().sample();app.args.read_only=True
        with patch.object(app.mem,'write_guest',side_effect=AssertionError('Read only')):
            app.freeze_health.set(True);app.toggle_freeze_health();app.freeze_raw_value()
        self.assertFalse(app.value_freezes.keep_health);self.assertFalse(app.value_freezes.locks)

    def test_selected_watch_is_fresh_and_connection_change_never_reuses_lock(self):
        app=self.app
        app.watch_rows=[SimpleNamespace(name='Freeze test',addr=0x8015C5E8,raw='0xFFFFFFFF')]
        app.watch_tree.insert('','end',iid='Freeze test');app.watch_tree.selection_set('Freeze test')
        app.freeze_selected_watch()
        self.assertEqual(app.value_freezes.locks[0x8015C5E8].value,(100).to_bytes(4,'big'))
        app.game_pid=999
        with patch.object(app.mem,'write_guest',side_effect=AssertionError('Changed connection')):app.poll_value_freezes()
        self.assertFalse(app.value_freezes.locks)
        self.assertFalse(app.freeze_tree.get_children())
