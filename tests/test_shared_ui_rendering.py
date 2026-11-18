"""Regression: unified toolkit tables do not rebuild unchanged Tk rows."""
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit, parse_args
from practice.inspector import Watch
from tests.test_unlocks import FakeRAM


class SharedUiRenderingTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.withdraw()
        self.app = Toolkit(self.root, parse_args([
            '--read-only', '--game-version', 'usa']))

    def tearDown(self):
        if hasattr(self, 'root'):
            for task in self.root.tk.call('after', 'info'):
                self.root.after_cancel(task)
            self.root.destroy()

    def test_live_memory_unchanged_rows_preserve_identity_and_selection(self):
        app = self.app
        app.watch_rows = [Watch('test field', 0x80000100,
                                'One', '01', 'OBSERVED', 'test')]
        app.draw_watches()
        tree = app.watch_tree
        tree.selection_set('test field')
        with patch.object(tree, 'delete',
                          side_effect=AssertionError('unexpected delete')), \
             patch.object(tree, 'insert',
                          side_effect=AssertionError('unexpected insert')), \
             patch.object(tree, 'item',
                          side_effect=AssertionError('unexpected row update')), \
             patch.object(tree, 'move',
                          side_effect=AssertionError('unexpected reorder')):
            app.draw_watches()
        self.assertEqual(tree.selection(), ('test field',))
        app.watch_rows = [Watch('test field', 0x80000100,
                                'Two', '02', 'OBSERVED', 'test')]
        app.draw_watches()
        self.assertEqual(tree.item('test field', 'values')[1], 'Two')
        self.assertEqual(tree.selection(), ('test field',))

    def test_story_progress_second_identical_sample_skips_row_updates(self):
        app = self.app
        app.mem = FakeRAM()
        app.refresh_story_progress()
        with patch.object(app.story_table, 'item',
                          side_effect=AssertionError('unchanged story row')) as changed:
            app.refresh_story_progress()
        changed.assert_not_called()


if __name__ == '__main__':
    unittest.main()
