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

    def test_traced_pj64_four_part_preview_without_actor_binding(self):
        root=tk.Tk();root.withdraw()
        try:
            dialog=ModelResearchDialog(root,region='usa',stage=353,actor_id=0x82)
            self.assertIn('4-part skeleton',dialog.trace_button.cget('text'))
            with tempfile.TemporaryDirectory() as folder:
                rom=Path(folder)/'rom.z64';rom.write_bytes(b'test')
                dialog.rom_path=rom
                mesh=MeshProbe(triangles=(((0,0,0),(10,0,0),(0,10,0)),),
                               rgb=((190,80,120),),commands=12,vertex_loads=1,
                               opcodes=(),warnings=('part transforms omitted',),ended=True)
                report=dict(roots=['0x090047F8']*4,file_id=0x120,segment=9,
                            triangles=84,commands=152,warnings=[])
                with patch('practice.model_research_ui.extract_traced_player_limb_bundle',
                           return_value=(report,mesh)) as mocked:
                    dialog.preview_traced_skeleton()
                    limit=time.monotonic()+2
                    while dialog.loading and time.monotonic()<limit:
                        root.update()
                        time.sleep(0.01)
                    self.assertFalse(dialog.loading)
                    mocked.assert_called_once_with(b'test','usa')
                    self.assertEqual(dialog.file_id.get(),'0x120')
                    self.assertEqual(dialog.start.get(),'')
                    self.assertEqual(dialog.end.get(),'')
                    self.assertEqual(dialog.segment.get(),'0x9')
                    self.assertIn('84 triangles',dialog.status.get())
                    self.assertIn('NOT an NPC actor-ID mapping',dialog.status.get())
            dialog.window.destroy()
        finally:root.destroy()


    def test_source_linked_rig_and_channel_table(self):
        root=tk.Tk();root.withdraw()
        try:
            dialog=ModelResearchDialog(root,region='usa',stage=353,actor_id=0x82)
            self.assertIn('Goemon weapon fragment',dialog.player_choices['values'][0])
            with tempfile.TemporaryDirectory() as folder:
                rom=Path(folder)/'rom.z64';rom.write_bytes(b'synthetic')
                dialog.rom_path=rom
                mesh=MeshProbe(triangles=(((0,0,0),(1,0,0),(0,1,0)),),
                               rgb=((80,150,110),),commands=0,vertex_loads=0,
                               opcodes=(),warnings=(),ended=True)
                raw=dict(kind='animation_channel',offset=0x6c8)
                immediate=dict(kind='immediate',value=1.0)
                node=dict(index=0,source_offset=0x2a518,graphics_pointer='0x00000000',
                          triangles=0,scale=[immediate]*3,rotation=[raw]*3,
                          translation=[raw]*3,right=1,left=0)
                report=dict(node_count=14,mesh_node_count=13,triangles=460,
                            immediate_scale_count=42,unresolved_rotation_channels=39,
                            unresolved_translation_channels=27,nodes=[node]*14)
                with patch('practice.model_research_ui.reconstruct_traced_rig',return_value=(report,mesh)) as mocked:
                    dialog.preview_linked_rig()
                    deadline=time.monotonic()+3
                    while dialog.loading and time.monotonic()<deadline:
                        root.update()
                        time.sleep(.01)
                    self.assertFalse(dialog.loading)
                    mocked.assert_called_once_with(b'synthetic','usa')
                self.assertIn('460 triangles',dialog.status.get())
                self.assertIn('39 rotation',dialog.status.get())
                self.assertIn('no pose',dialog.status.get())
                self.assertEqual(dialog.file_id.get(),'0x120')
                self.assertEqual(dialog.segment.get(),'0x09')
                child=dialog.inspect_rig_channels()
                self.assertIsNotNone(child)
                self.assertEqual(len(child.winfo_children()[0].winfo_children()[-1].get_children()),14)
                child.destroy()
            dialog.window.destroy()
        finally:
            root.destroy()


if __name__=='__main__':unittest.main()
