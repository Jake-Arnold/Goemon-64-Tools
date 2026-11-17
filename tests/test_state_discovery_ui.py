"""Graphical probe workflow exercised against synthetic original-game bytes."""
from __future__ import annotations
from argparse import Namespace
import tkinter as tk
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from practice.toolkit import Toolkit
from tests.test_state_discovery import Memory


class ProbeUITests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()
        self.app=Toolkit(self.root,Namespace(pid=None,base=None,endian='auto',route=None,
            enable_teleport=True,enable_state_restore=True,enable_debug_menu=True,
            enable_hex_edit=True,enable_scene_warp=False))

    def tearDown(self):
        if hasattr(self,'root'):self.root.destroy()

    def test_capture_compare_export_and_clear(self):
        app=self.app
        self.assertEqual(app.event_sections.tab(app.state_discovery_tab,'text'),'Compare memory changes')
        self.assertNotIn('State discovery', [app.notebook.tab(t,'text') for t in app.notebook.tabs()])
        mem=Memory()
        app.mem=mem
        app.current=mem.snapshot()
        app.capture_state_probe('A')
        mem.write(0x8015C7A5,b'\x01')
        app.capture_state_probe('B')
        app.compare_state_probes()
        report=app.state_report
        self.assertTrue(report)
        self.assertGreater(report['counts']['candidate_count'],0)
        with TemporaryDirectory() as tmp,patch(
            'practice.reports.reports_root',return_value=Path(tmp)):
            app.export_state_probe()
            manifests=list(Path(tmp).glob('USA/*/*/manifest.json'))
            self.assertEqual(len(manifests),1)
            self.assertEqual(__import__('json').loads(
                manifests[0].read_text())['kind'],'memory-comparison')
            self.assertTrue((manifests[0].parent/'session.json').is_file())
            self.assertIn('Saved',app.state_probe_status.get())
        app.reset_state_probes()
        self.assertIsNone(app.state_report)
        self.assertEqual(len(app.state_probe_table.get_children()),0)


    def test_capture_without_normal_player_during_impact(self):
        class ImpactMemory(Memory):
            def snapshot(self):
                raise ValueError('Invalid player object pointer 0xA4600014')
            def snapshot_for_monitoring(self):
                return {'player_ptr': None, 'task_ptr': None, 'character': None}
        app=self.app
        mem=ImpactMemory()
        mem.write(0x8015C5DC,(0xFFFFFFFF).to_bytes(4,'big'))
        app.mem=mem
        app.current=None
        app.capture_state_probe('A')
        self.assertIn('A captured',app.state_probe_status.get())
        mem.write(0x800C7AA4,b'\x04')
        app.capture_state_probe('B')
        self.assertIn('B captured',app.state_probe_status.get())
        app.compare_state_probes()
        self.assertTrue(app.state_report)
        self.assertTrue(any(row['address']=='0x800C7AA4'
                            for row in app.state_report['candidates']))

    def test_state_discovery_does_not_write_guest(self):
        class ReadOnlyMemory(Memory):
            def write_guest(self,*a):raise AssertionError('No write permitted')
        app=self.app; mem=ReadOnlyMemory();app.mem=mem;app.current=mem.snapshot()
        app.capture_state_probe('A')
        app.capture_state_probe('B')
        app.compare_state_probes()
        self.assertIn('No candidate',app.state_probe_status.get())


if __name__=='__main__':unittest.main()
