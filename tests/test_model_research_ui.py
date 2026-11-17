import tkinter as tk
import unittest
from practice.model_research import MeshProbe
from practice.model_research_ui import ModelResearchDialog

class ResearchViewTests(unittest.TestCase):
    def test_select_actor_without_asserting_model(self):
        root=tk.Tk();root.withdraw()
        try:
            window=ModelResearchDialog(root,region='japan_0',stage=353,actor_id=0x82,actor_name='Unknown')
            self.assertIn('japan_0',window.window.title())
            self.assertIsNone(window.rom_path)
            self.assertIsNone(window.mesh)
            self.assertEqual(window.file_id.get(),'')
            self.assertEqual(window.start.get(),'')
            self.assertEqual(window.end.get(),'')
            self.assertIn('No guessed actor resources',window.status.get())
            window.mesh=MeshProbe(triangles=(((0,0,0),(100,0,0),(0,100,0)),),rgb=((128,128,128),),commands=3,vertex_loads=1,opcodes=((4,1),),warnings=(),ended=True)
            window.window.update_idletasks()
            window.render()
            self.assertEqual(len(window.canvas.find_all()),1)
            initial=window.yaw
            class Event:pass
            press=Event();press.x=10;press.y=10
            drag=Event();drag.x=30;drag.y=15
            window.begin_drag(press)
            window.drag(drag)
            self.assertGreater(window.yaw,initial)
            window.zoom_by(1.1)
            self.assertGreater(window.zoom,1.0)
            window.window.destroy()
        finally:
            root.destroy()

if __name__=='__main__':unittest.main()
