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
        # Deterministic UI tests exercise the same poll under the freeze guard.
        # The actual 10 ms background thread is covered separately.
        self._start_patch=patch.object(self.app,'_ensure_freeze_worker')
        self._start_patch.start()

    def tearDown(self):
        self._start_patch.stop()
        self.root.destroy()

    def test_ui_poll_does_not_perform_game_writes(self):
        app=self.app
        app.raw_address.set('8015C63B');app.raw_width.set('1');app.raw_value.set('10')
        app.freeze_raw_value()
        with patch.object(self.process,'write',side_effect=AssertionError('Tk must not write RAM')):
            app.poll_value_freezes()
        self.assertTrue(app.value_freezes.active())

    def test_defaults_inactive_raw_freeze_stop_and_health_toggle(self):
        app=self.app
        self.assertFalse(app.freeze_health.get());self.assertFalse(app.value_freezes.locks)
        app.raw_address.set('8015C63B');app.raw_width.set('1');app.raw_value.set('10')
        app.freeze_raw_value();app._freeze_poll_once();app.poll_value_freezes()
        self.assertEqual(app.mem.u8(0x8015C63B),16)
        self.assertEqual(len(app.freeze_tree.get_children()),1)
        app.freeze_tree.selection_set(str(0x8015C63B));app.stop_selected_freeze()
        self.assertFalse(app.value_freezes.locks)
        app.freeze_health.set(True);app.toggle_freeze_health();app._freeze_poll_once();app.poll_value_freezes()
        self.assertEqual(app.mem.u32(0x8015C5E4),10)
        app.stop_all_freezes();self.assertFalse(app.freeze_health.get())

    def test_context_menu_freeze_unfreeze_uses_clicked_watch_and_fresh_value(self):
        app=self.app
        app.current=app.mem.snapshot()
        app.refresh_inspector(app.current)
        app.watch_tree.selection_set('Lives')
        app.mem.write_guest(0x8015C5E8,(321).to_bytes(4,'big'))
        with patch.object(app.watch_tree,'identify_row',return_value='Ryo'), \
             patch.object(app.watch_context_menu,'tk_popup'):
            app.open_live_watch_menu(SimpleNamespace(y=11,x_root=15,y_root=20))
        self.assertEqual(app.watch_tree.selection(),('Ryo',))
        app.watch_context_menu.invoke(0)
        self.assertEqual(app.value_freezes.locks[0x8015C5E8].value,(321).to_bytes(4,'big'))
        self.assertEqual(app.value_freezes.locks[0x8015C5E8].label,'Ryo')
        with patch.object(app.watch_tree,'identify_row',return_value='Ryo'), \
             patch.object(app.watch_context_menu,'tk_popup'):
            app.open_live_watch_menu(SimpleNamespace(y=11,x_root=15,y_root=20))
        self.assertEqual(app.watch_context_menu.entrycget(0,'label'),'Unfreeze value')
        app.watch_context_menu.invoke(0)
        self.assertNotIn(0x8015C5E8,app.value_freezes.locks)

    def test_no_address_cannot_freeze_and_read_only_blocks_context(self):
        app=self.app
        app.watch_rows=[SimpleNamespace(name='Derived',addr=None,raw='—')]
        app.draw_watches()
        with patch.object(app.watch_tree,'identify_row',return_value='Derived'), \
             patch.object(app.watch_context_menu,'tk_popup'):
            app.open_live_watch_menu(SimpleNamespace(y=11,x_root=15,y_root=20))
        self.assertEqual(app.watch_context_menu.entrycget(0,'state'),'disabled')
        app.args.read_only=True
        app.watch_rows=[SimpleNamespace(name='Ryo',addr=0x8015C5E8,raw='0x00000000')]
        app.freeze_watch_by_id('Ryo')
        self.assertFalse(app.value_freezes.locks)
        self.assertIn('read-only',app.freeze_status.get())

    def test_read_only_blocks_both_entry_paths_and_disconnect_clears_controls(self):
        app=self.app;app.freeze_health.set(True);app.toggle_freeze_health()
        app.mem=None;app._freeze_poll_once();app.poll_value_freezes()
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
        with patch.object(app.mem,'write_guest',side_effect=AssertionError('Changed connection')):app._freeze_poll_once()
        app.poll_value_freezes()
        self.assertFalse(app.value_freezes.locks)
        self.assertFalse(app.freeze_tree.get_children())
