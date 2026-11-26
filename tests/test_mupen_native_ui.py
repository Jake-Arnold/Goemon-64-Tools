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
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.settings=Path(self.temp.name)/'native-inspector.json'
        self.ui=NativeFrameUi(self.root,settings_path=self.settings);self.root.withdraw()
    def tearDown(self):
        if hasattr(self,'ui'):self.ui.close()
    def test_automatic_build_populates_input_and_preserves_manual_choice(self):
        from concurrent.futures import Future
        from practice.mupen_native_ui import default_input_path
        ui=self.ui; f=Future()
        with patch('practice.mupen_native_ui.request_input_build',return_value=f):
            ui._request_default_build()
            self.assertIn('Preparing',ui.status.get());self.assertEqual(ui.paths['input'].get(),'')
            f.set_result(default_input_path());ui._poll_input_build()
            self.assertEqual(ui.paths['input'].get(),str(default_input_path()))
            g=Future();ui.build_future=g;ui.paths['input'].set('/custom/plugin.so')
            g.set_result(default_input_path());ui._poll_input_build()
            self.assertEqual(ui.paths['input'].get(),'/custom/plugin.so')
            ui.paths['input'].set('');bad=Future();ui.build_future=bad
            bad.set_exception(RuntimeError('SDK missing'));ui._poll_input_build()
            self.assertIn('SDK missing',ui.status.get());self.assertEqual(ui.paths['input'].get(),'')

    def test_status_poll_does_not_drop_user_input(self):
        ui=self.ui; stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.control('status');ui.x.set('80');ui.control('hold');ui.x.set('0')
        self.assertEqual(ui.pending[1]['input']['x'],80)
        ui.busy=False;ui.inflight=None;ui.drain()
        sent=[json.loads(x) for x in stream.getvalue().splitlines()]
        self.assertEqual(sent,[{'op':'status'},{'op':'hold','input':dict(NEUTRAL,x=80)}])
        ui.process=None
    def test_managed_attachment_metadata_and_paused_edit_guard(self):
        ui=self.ui;owner=SimpleNamespace(pid=123,poll=lambda:None)
        ui.process=owner;ui.session_rom=Path('/tmp/original.z64')
        metadata=dict(pid=123,base=0x10000,size=0x400000,region='japan')
        ui.managed_ram=metadata
        self.assertEqual(ui.managed_attachment(),(owner,0x10000,ui.session_rom))
        for fields in (dict(pid=124),dict(region='usa'),dict(size=0x800000),dict(base=3)):
            ui.managed_ram=dict(metadata,**fields);self.assertIsNone(ui.managed_attachment())
        ui.managed_ram=metadata;ui.report=dict(state=2,recording=False)
        self.assertFalse(ui.manual_edits_paused());ui.report['state']=3
        self.assertTrue(ui.manual_edits_paused());ui.inflight='step'
        self.assertFalse(ui.manual_edits_paused());ui.inflight=None;ui.pending=('physical',{})
        self.assertFalse(ui.manual_edits_paused());ui.pending=None
        ui.report['recording']=True;self.assertFalse(ui.manual_edits_paused())
        owner.poll=lambda:0;self.assertIsNone(ui.managed_attachment());ui.process=None

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

    def test_locate_player_populates_editor_and_shows_read_diagnostics(self):
        ui=self.ui;stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.report=dict(region='japan',state=3,recording=False,rows=[],watches=[])
        ui.locate_player();self.assertEqual(json.loads(stream.getvalue()),dict(op='locate_player',replace_trace=False))
        r=dict(ui.report,serial=1,error='',player_base=0x8016F780,player_text='pre_callback u32 8016F788',
               ram_reader='native 2.6.0 words',watch_errors={'raw_x':'Core RDRAM pointer unavailable'})
        ui.events.put((ui.generation,'report',dict(ok=True,report=r)));ui.drain()
        self.assertIn('pre_callback u32 8016F788',ui.watches.get('1.0','end'))
        self.assertIn('task 0x8016F780',ui.status.get());self.assertIn('Core RDRAM pointer unavailable',ui.status.get())
        ui.process=None

    def test_long_timeline_sends_600_frames(self):
        ui=self.ui;stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.n.set('600');ui.timeline.insert('1.0','14 CU 0 0');ui.step()
        sent=json.loads(stream.getvalue());self.assertEqual(len(sent['inputs']),600)
        self.assertEqual(sent['inputs'][13]['buttons'],8);ui.process=None

    def test_editor_persistence_and_stale_locator_not_applied_at_launch(self):
        ui=self.ui;w='pre_callback u32 8016F788'
        ui.watches.insert('1.0',w);ui.located_text=w
        ui.timeline.insert('1.0','1-120 - 80 0');ui.n.set('600')
        ui.save_editor_settings();ui.close()
        self.root=tk.Tk();self.root.withdraw();self.ui=ui=NativeFrameUi(self.root,settings_path=self.settings)
        self.assertEqual(ui.watches.get('1.0','end-1c'),w)
        self.assertEqual(ui.timeline.get('1.0','end-1c'),'1-120 - 80 0')
        self.assertEqual(ui.n.get(),'600');self.assertEqual(ui.located_text,w)
        for k,v in ui.paths.items():v.set('/tmp/custom-'+k)
        proc=SimpleNamespace(stdin=io.StringIO(),stdout=[],wait=lambda:0)
        with patch('practice.mupen_native_ui.subprocess.Popen',return_value=proc) as launch:
            ui.start();args=launch.call_args.args[0]
            self.assertEqual(args[args.index('--watches')+1],'')
        ui.process=None
        stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream);ui.busy=False;ui.inflight=None
        ui.report=dict(region='japan',state=3,recording=False,rows=[],watches=[])
        ui.apply_watches();self.assertEqual(json.loads(stream.getvalue())['op'],'locate_player');ui.process=None

    def test_editor_autosave_and_bad_settings(self):
        from practice.native_inspector_preferences import load_editor_preferences
        ui=self.ui;ui.watches.insert('1.0','value u32 80001000');ui.timeline.insert('1.0','1-60 - 80 0')
        ui.n.set('60');self.root.update()
        done=tk.BooleanVar(value=False);self.root.after(450,lambda:done.set(True));self.root.wait_variable(done)
        self.assertEqual(load_editor_preferences(self.settings)['steps'],'60')
        self.settings.write_text('{bad json');self.assertEqual(load_editor_preferences(self.settings),{})
        self.settings.write_text(json.dumps(dict(format='goemon-native-inspector-v1',watches='x'*8193,timeline='',steps='1')))
        self.assertEqual(load_editor_preferences(self.settings),{})

    def test_copy_original_rows_during_incremental_render_and_append(self):
        ui=self.ui;w=dict(name='action',kind='u8',address=0x80001000)
        def row(i):return dict(serial=i+1,frame=i,polls=1,buttons=0,x=0,y=0,action=i%256)
        ui.report=dict(watches=[w],rows=[row(i) for i in range(600)]);ui.render()
        self.assertEqual(len(ui.table.get_children()),100);self.assertIsNotNone(ui.render_job)
        ui.select_all_trace();ui.copy_trace(selected=True)
        clip=self.root.clipboard_get().splitlines()
        self.assertEqual(len(clip),601);self.assertEqual(clip[0],'serial\tframe\tpolls\tbuttons\tx\ty\taction')
        self.assertEqual(clip[-1].split('\t')[:2],['600','599'])
        previous=ui.table.get_children();ui.report=dict(watches=[w],rows=[row(i) for i in range(650)]);ui.render()
        self.assertEqual(ui.table.get_children()[:100],previous)
        while ui.render_cursor<650:
            ui._cancel_render();ui._render_chunk()
        self.assertEqual(len(ui.table.get_children()),650);self.assertEqual(len(ui.table.selection()),650)
        ui.trace_select_all=False;ui.table.selection_set('17');ui.copy_trace(selected=True)
        self.assertEqual(self.root.clipboard_get().splitlines()[1].split('\t')[:2],['18','17'])
        ui.report=dict(watches=[w],rows=[]);ui.render();self.assertEqual(len(ui.table.get_children()),0)

    def test_full_trace_large_table_is_chunked(self):
        ui=self.ui;watches=[dict(name=f'w{i}',kind='u32',address=0x80001000+i*4) for i in range(24)]
        rows=[dict(serial=i+1,frame=i,polls=1,buttons=0,x=0,y=0,**{w['name']:i for w in watches}) for i in range(3600)]
        ui.report=dict(watches=watches,rows=rows);ui.render()
        self.assertEqual(ui.render_cursor,100)
        ui.copy_trace();self.assertEqual(len(self.root.clipboard_get().splitlines()),3601)
        while ui.render_cursor<len(rows):ui._cancel_render();ui._render_chunk()
        self.assertEqual(len(ui.table.get_children()),3600)

    def test_single_step_ignores_timeline_and_progress_keeps_busy(self):
        ui=self.ui;stream=io.StringIO();ui.process=SimpleNamespace(stdin=stream)
        ui.timeline.insert('1.0','2-120 - 80 0');ui.buttons['CU'].set(True);ui.step(1)
        self.assertEqual(json.loads(stream.getvalue())['inputs'],[dict(NEUTRAL,buttons=8)])
        ui.events.put((ui.generation,'report',dict(progress=dict(done=1,total=1))))
        ui.drain();self.assertTrue(ui.busy);self.assertEqual(ui.inflight,'step');self.assertIn('1/1',ui.status.get());ui.process=None

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
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.settings_patch=patch('practice.mupen_native_ui.inspector_preferences_path',return_value=Path(self.temp.name)/'native-inspector.json')
        self.settings_patch.start();self.addCleanup(self.settings_patch.stop)

    def tearDown(self):
        try:
            # The stub also builds the unrelated Project64 polling page.
            # Cancel its timers before destroying this isolated Tk interpreter.
            for timer in self.root.tk.call('after','info'):
                self.root.after_cancel(timer)
            self.root.destroy()
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
            for name in ('mupen64plus-video-rice.so','mupen64plus-audio-sdl.so','mupen64plus-rsp-hle.so','mupen64plus-input-sdl.so'):(plugins/name).touch()
            (p/'share'/'games'/'mupen64plus').mkdir(parents=True)
            with patch('practice.mupen_native_ui.sysconfig.get_config_var',return_value='x86_64-linux-gnu'):
                found=discover_prefix(p)
            self.assertEqual(found['core'],str(lib/'libmupen64plus.so.2'))
            self.assertEqual(found['gfx'],str(plugins/'mupen64plus-video-rice.so'))
            self.assertTrue({'audio','rsp','data','physical_input'}<=found.keys())
            self.assertEqual(found['data'],str(p/'share'/'games'/'mupen64plus'))

if __name__=='__main__':unittest.main()
