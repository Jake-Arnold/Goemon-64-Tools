"""Graphical tests for the bounded, reusable real-button flag viewport."""
import tkinter as tk
import unittest
from collections import namedtuple
from tkinter import ttk

from practice.virtual_flag_list import VirtualFlagList

Flag = namedtuple('Flag', 'key label address mask source group subtype')


class VirtualFlagListTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(str(exc))
        self.root.geometry('1000x650+0+0')
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)
        self.actions, self.toggles, self.details = [], [], []
        self.view = VirtualFlagList(
            self.frame, on_toggle=self.toggles.append,
            on_write=lambda key, target: self.actions.append((key, target)),
            on_detail=self.details.append,
            can_write=lambda flag: flag.key not in ('0', '1'))
        self.flags = [
            Flag(str(i), f'Flag {i}', 0x8015C600 + i // 8, 1 << (i % 8),
                 'research', 'Dolls', 'Unsorted')
            for i in range(450)]
        self.section = ('Dolls', 'Unsorted')
        self.sections = {self.section: self.flags}
        self.view.rebuild(self.sections, {self.section}, {})
        self.view.set_values({flag.key: 0 for flag in self.flags})
        self.root.update()

    def tearDown(self):
        if getattr(self, 'root', None) is not None:
            self.root.destroy()

    def test_450_logical_flags_do_not_create_450_button_rows(self):
        self.assertEqual(len(self.view.rows), 451)
        self.assertLess(self.view.widget_count, 25)
        self.assertTrue(self.view.scroll_to_key('400'))
        self.root.update()
        self.assertIn('400', self.view.visible_flags)
        self.assertLess(self.view.widget_count, 25)
        self.view.visible_flags['400']['on'].invoke()
        self.assertEqual(self.actions, [('400', 'Set')])
        self.assertTrue(self.view.scroll_to_key('0'))
        self.root.update()
        self.assertIn('disabled', self.view.visible_flags['0']['on'].state())

    def test_collapse_filter_and_actual_on_off_buttons(self):
        self.view.rebuild(self.sections, set(), {'10': True})
        self.assertEqual(len(self.view.rows), 1)
        self.assertEqual(len(self.view.visible_flags), 0)
        self.view._header_pool[0]['button'].invoke()
        self.assertEqual(self.toggles, [self.section])
        self.view.rebuild(
            self.sections, {self.section},
            {str(i): i == 10 for i in range(450)})
        self.root.update()
        self.assertIn('10', self.view.visible_flags)
        self.view.visible_flags['10']['off'].invoke()
        self.assertEqual(self.actions, [('10', 'Clear')])

    def test_same_key_cross_region_repaint_updates_address_and_source(self):
        self.assertTrue(self.view.scroll_to_key('120'))
        self.root.update()
        same_key = Flag('120', 'JP flag', 0x80161DFC, 0x40,
                        'JP offset candidate', 'Dolls', 'Unsorted')
        self.view.rebuild(
            {self.section: [same_key]}, {self.section}, {},
            reset_scroll=True)
        self.view.set_values({'120': 0})
        self.root.update()
        row = self.view.visible_flags['120']
        self.assertIn('80161DFC', row['address'].cget('text'))
        self.assertEqual(row['name'].cget('text'), 'JP flag')
        self.assertIn('JP offset', row['source'].cget('text'))

    def test_rebinding_discards_stale_key_and_region(self):
        self.assertTrue(self.view.scroll_to_key('120'))
        self.root.update()
        slot = self.view.visible_flags['120']
        callback = slot['on'].invoke
        replacement = Flag('new', 'New', 0x8016C000, 0x80,
                           'JP', 'Dolls', 'Unsorted')
        self.view.rebuild(
            {self.section: [replacement]}, {self.section}, {},
            reset_scroll=True)
        self.view.set_values({'new': 0})
        self.root.update()
        callback()
        self.assertNotIn(('120', 'Set'), self.actions)
        self.assertIn('new', self.view.visible_flags)
        self.view.visible_flags['new']['on'].invoke()
        self.assertIn(('new', 'Set'), self.actions)


if __name__ == '__main__':
    unittest.main()
