import tkinter as tk
import unittest
from practice.room_actor_ui import RoomActorBrowser
from tests.test_room_actors import atlas_fixture

class DialogTest(unittest.TestCase):
    def test_render_and_filter_and_stage_selection(self):
        root=tk.Tk();root.withdraw()
        try:
            dialog=RoomActorBrowser(root, atlas_fixture(), 353)
            self.assertIn('4 ROM placements',dialog.status.get())
            self.assertEqual(len(dialog.table.get_children()),4)
            dialog.query.set('0x321')
            self.assertEqual(len(dialog.table.get_children()),3)
            dialog.refresh(atlas_fixture(), 352)
            self.assertEqual(len(dialog.table.get_children()),0)
            dialog.refresh(None, 353)
            self.assertIn('No actor atlas', dialog.status.get())
            dialog.window.destroy()
        finally:root.destroy()

if __name__=='__main__':unittest.main()
