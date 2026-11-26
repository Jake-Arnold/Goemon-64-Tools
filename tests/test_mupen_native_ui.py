"""Headless UI tests; no emulator process is launched."""
import io
import json
from pathlib import Path
import tempfile
import sys
import sysconfig
import tkinter as tk
from tkinter import ttk
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from practice.mupen_native_ui import NativeFrameUi, discover_prefix
from practice.mupen_native import NEUTRAL
from practice.pj64_debugger_ui import PJ64DebuggerMixin


class NativeUiTests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.ui=NativeFrameUi(self.root);self.root.withdraw()
    def tearDown(self):
        if hasattr(self,'ui'):self.ui.close()
    def test_status_poll_does_not_drop_user_input(self):
        ui=self.ui; stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.control('status');ui.x.set('80');ui.control('hold');ui.x.set('0')
        self.assertEqual(ui.pending[1]['input']['x'],80)
        ui.busy=False;ui.inflight=None;ui.drain()
        sent=[json.loads(x) for x in stream.getvalue().splitlines()]
        self.assertEqual(sent,[{'op':'status'},{'op':'hold','input':dict(NEUTRAL,x=80)}])
        ui.process=None
    def test_apply_watches_preserves_session_and_requires_confirmation(self):
        ui=self.ui;stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.report=dict(state=3,recording=False,rows=[{'frame':1}],watches=[])
        ui.watches.insert('1.0','new s16 80001000')
        with patch('practice.mupen_native_ui.messagebox.askyesno',return_value=False):ui.apply_watches()
        self.assertEqual(stream.getvalue(),'')
        with patch('practice.mupen_native_ui.messagebox.askyesno',return_value=True):ui.apply_watches()
        sent=json.loads(stream.getvalue());self.assertEqual(sent['op'],'watches');self.assertTrue(sent['replace_trace']);self.assertIn('new s16',sent['text'])
        ui.process=None
    def test_japan_preset_and_comparison_invalidation(self):
        ui=self.ui;ui.controller_preset();self.assertIn('@research:controller_japan_raw_x',ui.watches.get('1.0','end'))
        ui.report=dict(watches=[],rows=[]);ui.reference={'rows':[]};ui.generation=1
        ui.events.put((1,'report',{'ok':True,'report':dict(watches=[dict(name='raw_x')],rows=[],region='japan',state=3,serial=1,recording=False,error='')}))
        ui.drain();self.assertIsNone(ui.reference)
    def test_mini_unlock_confirmation_and_command(self):
        ui=self.ui;stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.report=dict(state=3,recording=False,rows=[],capabilities=dict(mini_unlock=True))
        with patch('practice.mupen_native_ui.messagebox.askyesno',return_value=False):ui.unlock_mini()
        self.assertEqual(stream.getvalue(),'')
        with patch('practice.mupen_native_ui.messagebox.askyesno',return_value=True):ui.unlock_mini()
        self.assertEqual(json.loads(stream.getvalue()),dict(op='unlock_mini',confirm=True));ui.process=None

    def test_rows_compare(self):
        ui=self.ui; w=dict(name='action',kind='u16',address=0x80001000)
        def row(i,v):return dict(serial=i,frame=i,polls=1,buttons=0,x=0,y=0,action=v)
        ui.report={'watches':[w],'rows':[row(1,13),row(2,143)]};ui.render()
        self.assertIn('changed',ui.table.item(ui.table.get_children()[1],'tags'))
        ui.reference={'rows':[row(1,13),row(2,0)]};ui.render()
        self.assertIn('different',ui.table.item(ui.table.get_children()[1],'tags'))
    def test_homebrew_prefix_selection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);lib=p/'lib'/'mupen64plus';lib.mkdir(parents=True)
            for file in ('libmupen64plus.dylib','mupen64plus-video-rice.dylib','mupen64plus-audio-sdl.dylib','mupen64plus-rsp-hle.dylib'):(lib/file).touch()
            (p/'share'/'mupen64plus').mkdir(parents=True)
            self.assertTrue({'core','gfx','audio','rsp','data'}<=discover_prefix(p).keys())

class EmbeddedNativeUiTests(unittest.TestCase):
    def setUp(self):
        try:self.root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        self.root.withdraw()

    def tearDown(self):
        try:self.root.destroy()
        except tk.TclError:pass

    def test_embedded_panel_does_not_change_root_and_shutdown_closes_pipe(self):
        self.root.title('Toolkit title')
        parent=ttk.Frame(self.root);parent.pack()
        ui=NativeFrameUi(self.root,parent=parent)
        self.assertEqual(self.root.title(),'Toolkit title')
        self.assertEqual(ui.body.master,parent)
        stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        timers=(ui.drain_id,ui.poll_id)
        parent.destroy()
        self.assertTrue(ui.closed);self.assertTrue(stream.closed)
        self.assertTrue(self.root.winfo_exists())
        self.assertTrue(all(t not in self.root.tk.call('after','info') for t in timers))
        ui.shutdown()

    def test_unified_backend_routing_keeps_one_session(self):
        class Stub(PJ64DebuggerMixin):pass
        app=Stub();app.root=self.root
        app.args=SimpleNamespace(read_only=False,enable_hex_edit=False)
        app.active_version=SimpleNamespace(key='japan');app.jp_backend='mupen64plus'
        app.connection_target=tk.StringVar(value='auto')
        app.verified_rom_path=Path('/tmp/verified-rom.z64')
        app.notebook=ttk.Notebook(self.root);app.notebook.pack()
        app.notebook.add(ttk.Frame(app.notebook),text='Dashboard')
        with patch('practice.pj64_debugger_ui.sys.platform','linux'), patch.object(NativeFrameUi,'find_installation'), patch('practice.mupen_native_ui.subprocess.Popen') as launch:
            app.build_pj64_debugger_tab(app.notebook)
            self.assertIsNone(app.native_frame_ui)
            app.open_frame_inspector()
            ui=app.native_frame_ui
            self.assertEqual(app.notebook.select(),str(app.frame_inspector_tab))
            self.assertEqual(app.frame_backend_pages.select(),str(app.frame_native_page))
            self.assertEqual(ui.paths['rom'].get(),'/tmp/verified-rom.z64')
            self.assertEqual(ui.body.master,app.frame_native_page)
            stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
            ui.watches.insert('1.0','action u8 8016F84C')
            app.open_frame_inspector('project64')
            self.assertEqual(app.frame_backend_pages.select(),app.frame_project64_page)
            app._sync_frame_backend()
            self.assertEqual(app.frame_backend_pages.select(),app.frame_project64_page)
            app.open_frame_inspector('mupen64plus')
            self.assertIs(app.native_frame_ui,ui)
            self.assertIn('action u8',ui.watches.get('1.0','end'))
            self.assertFalse(stream.closed);launch.assert_not_called()
            app.shutdown_frame_inspector();self.assertTrue(stream.closed)

    def test_linux_multiarch_discovery(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);lib=p/'lib'/'x86_64-linux-gnu';plugins=lib/'mupen64plus';plugins.mkdir(parents=True)
            (lib/'libmupen64plus.so.2').touch()
            for name in ('mupen64plus-video-rice.so','mupen64plus-audio-sdl.so','mupen64plus-rsp-hle.so'):(plugins/name).touch()
            (p/'share'/'games'/'mupen64plus').mkdir(parents=True)
            with patch('practice.mupen_native_ui.sysconfig.get_config_var',return_value='x86_64-linux-gnu'):
                found=discover_prefix(p)
            self.assertEqual(found['core'],str(lib/'libmupen64plus.so.2'))
            self.assertEqual(found['gfx'],str(plugins/'mupen64plus-video-rice.so'))
            self.assertTrue({'audio','rsp','data'}<=found.keys())
            self.assertEqual(found['data'],str(p/'share'/'games'/'mupen64plus'))

if __name__=='__main__':unittest.main()
