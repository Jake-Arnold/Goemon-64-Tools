import tkinter as tk
import unittest
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
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
            with tempfile.TemporaryDirectory() as folder:
                rom=Path(folder)/'dummy.z64'
                rom.write_bytes(b'fake')
                window.rom_path=rom
                window.player_choices.current(1)
                report=dict(region='japan_0',slot=1,file_id=0x124,segment=9,
                    start=0x2448,end=0x2610,triangles=1,commands=3,warnings=[])
                with patch('practice.model_research_ui.extract_player_fragment',return_value=(report,window.mesh)) as mocked:
                    window.preview_player_fragment()
                    limit=time.monotonic()+2
                    while window.loading and time.monotonic()<limit:
                        root.update()
                        time.sleep(0.01)
                    self.assertFalse(window.loading)
                    mocked.assert_called_once_with(b'fake','japan_0',1)
                    self.assertEqual(window.file_id.get(),'0x124')
                    self.assertEqual(window.segment.get(),'0x9')
                    self.assertIn('Verified player resource table',window.status.get())
                    self.assertIn('NOT linked to selected NPC actor',window.status.get())
            window.window.destroy()
        finally:
            root.destroy()

if __name__=='__main__':unittest.main()
