"""Standalone or embedded UI for the native Mupen64Plus research session."""
from __future__ import annotations
import csv
import io
import json
import shutil
from pathlib import Path
import queue
import subprocess
import sys
import sysconfig
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from practice.mupen_native import write_trace, MAX_NATIVE_STEPS, MAX_TRACE_ROWS
from practice.native_trace_wire import TraceReader
from practice.mupen_input_build import default_input_path, request_input_build
from practice.native_inspector_preferences import (inspector_preferences_path, load_editor_preferences,
    save_editor_preferences)

JP_CONTROLLER_WATCHES = '\n'.join(f'{name} {kind} @research:controller_japan_{name}' for name,kind in (
    ('raw_x','s16'),('raw_y','s16'),('magnitude','f32'),('processed_x','f32'),
    ('processed_y','f32'),('held','u16'),('pressed','u16'),
    ('combined_magnitude','f32'),('combined_x','f32'),('combined_y','f32')))

from practice.pj64_frame_control import BUTTONS, controller_input, parse_inputs
from practice.version import DISPLAY_VERSION


def discover_prefix(prefix):
    """Search bounded library/data locations under one installation prefix."""
    prefix=Path(prefix)
    candidates={}
    # Debian/Ubuntu place the core and plugins in multiarch directories.
    libs = [prefix / "lib", prefix / "lib64"]
    multiarch = sysconfig.get_config_var("MULTIARCH")
    if multiarch:
        libs.insert(0, prefix / "lib" / multiarch)
    shares = [prefix / "share" / "mupen64plus", prefix / "share" / "games" / "mupen64plus"]
    locations = [path for lib in libs for path in (lib, lib / "mupen64plus")]
    locations += [share / "plugins" for share in shares]
    patterns={
        'core': ('libmupen64plus.dylib','libmupen64plus.2.dylib','libmupen64plus.so','libmupen64plus.so.2'),
        'gfx': ('mupen64plus-video-glide64mk2.dylib','mupen64plus-video-rice.dylib','mupen64plus-video-glide64mk2.so','mupen64plus-video-rice.so'),
        'audio': ('mupen64plus-audio-sdl.dylib','mupen64plus-audio-sdl.so'),
        'rsp': ('mupen64plus-rsp-hle.dylib','mupen64plus-rsp-hle.so'),
        'physical_input': ('mupen64plus-input-sdl.dylib','mupen64plus-input-sdl.so'),
    }
    for key,names in patterns.items():
        for name in names:
            files=[path / name for path in locations if (path / name).is_file()]
            if files:
                candidates[key]=str(files[0]);break
    for share in shares:
        if share.is_dir():
            candidates['data']=str(share);break
    for suffix in (('.dylib',) if sys.platform=='darwin' else ('.so',) if sys.platform.startswith('linux') else ('.dll',)):
        p=Path(__file__).resolve().parents[1]/'build'/('goemon_mupen_input'+suffix)
        if p.is_file():candidates['input']=str(p);break
    return candidates


class NativeFrameUi:
    def __init__(self, root, *, parent=None, settings_path=None):
        self.root=root; self.process=None; self.busy=False; self.report=None; self.reference=None
        self.events=queue.Queue(); self.generation=0; self.closed=False
        self.pending=None; self.inflight=None; self.last_render=None; self.last_error=''
        self.last_activity=0.; self.stalled=False; self.protocol_failed=False; self.recovery_path=None
        self.managed_ram=None; self.session_rom=None
        self.build_future=None
        self.settings_path=Path(settings_path) if settings_path is not None else inspector_preferences_path()
        self.settings_job=None; self.settings_last=None; self.located_text=None
        self.render_job=None; self.render_cursor=0; self.trace_select_all=False
        self.embedded=parent is not None
        if not self.embedded:
            root.title(f'Goemon Native Frame Inspector {DISPLAY_VERSION}')
            root.geometry('1050x750'); root.protocol('WM_DELETE_WINDOW', self.close)
        body=ttk.Frame(parent if self.embedded else root,padding=6); body.pack(fill='both',expand=True)
        self.body=body
        style=ttk.Style(root)
        style.configure('Inspector.TButton',padding=(5,2))
        style.configure('Inspector.TEntry',padding=(3,2))
        style.configure('Inspector.TCheckbutton',padding=1)
        body.bind('<Destroy>',self._body_destroyed,add='+')
        top=ttk.Frame(body);top.pack(fill='x')
        ttk.Label(top,text='Native core frames • managed research session').pack(side='left')
        self.setup_button=ttk.Button(top,style='Inspector.TButton',text='Hide setup',command=self.toggle_setup);self.setup_button.pack(side='right')
        setup=ttk.LabelFrame(body,text='Launch a new emulator',padding=4); setup.pack(fill='x')
        self.setup=setup
        self.setup_visible=True
        setup.columnconfigure(1,weight=1);setup.columnconfigure(4,weight=1)
        home=Path.home()/'.goemon-mupen-research'
        self.paths={key:tk.StringVar(value=str(home) if key=='config' else '') for key in ('rom','core','gfx','audio','input','rsp','data','config','physical_input')}
        for i,(key,var) in enumerate(self.paths.items()):
            r,c=divmod(i,2);c*=3
            ttk.Label(setup,text=key).grid(row=r,column=c,sticky='w')
            ttk.Entry(setup,style='Inspector.TEntry',textvariable=var,width=22).grid(row=r,column=c+1,sticky='ew')
            ttk.Button(setup,style='Inspector.TButton',text='Browse',command=lambda k=key:self.browse(k)).grid(row=r,column=c+2)
        ttk.Button(setup,style='Inspector.TButton',text='Find Mupen64Plus installation',command=self.find_installation).grid(row=5,column=0,columnspan=3,sticky='w')
        self.status=tk.StringVar(value='Select the original ROM, native core and plugins. See docs/MUPEN_NATIVE.md.')
        bar=ttk.Frame(body); bar.pack(fill='x');self.command_bar=bar
        self.start_button=ttk.Button(bar,style='Inspector.TButton',text='Launch session',command=self.start);self.start_button.pack(side='left')
        for label,op in [('Pause','pause'),('Resume neutral','resume'),('Play with controller','physical'),('Hold input','hold'),('Stop emulator','stop')]:
            ttk.Button(bar,style='Inspector.TButton',text=label,command=lambda op=op:self.control(op)).pack(side='left')
        extra=ttk.Frame(body);extra.pack(fill='x')
        for label,op in [('Record / stop','record'),('Clear trace','clear')]:
            ttk.Button(extra,style='Inspector.TButton',text=label,command=lambda op=op:self.control(op)).pack(side='left')
        self.mini_button=ttk.Button(extra,style='Inspector.TButton',text='Unlock Mini Ebisumaru (JP)',command=self.unlock_mini,state='disabled');self.mini_button.pack(side='left')
        ttk.Button(extra,style='Inspector.TButton',text='Copy trace',command=self.copy_trace).pack(side='left')
        statebar=ttk.Frame(body);statebar.pack(fill='x')
        self.slot=tk.StringVar(value='0')
        ttk.Label(statebar,text='State slot').pack(side='left')
        ttk.Spinbox(statebar,from_=0,to=9,textvariable=self.slot,width=3).pack(side='left')
        ttk.Button(statebar,style='Inspector.TButton',text='Save state (F5)',command=lambda:self.state_action('save_state')).pack(side='left')
        ttk.Button(statebar,style='Inspector.TButton',text='Load state (F7)',command=lambda:self.state_action('load_state')).pack(side='left')
        ttk.Button(statebar,style='Inspector.TButton',text='Recover latest trace',command=self.copy_recovered).pack(side='left')
        self.state_bindings=[(key,self.root.bind(key,lambda e,op=op:self.state_hotkey(e,op),add='+')) for key,op in (('<F5>','save_state'),('<F7>','load_state'))]
        ttk.Label(body,textvariable=self.status,wraplength=990).pack(anchor='w')
        row=ttk.Frame(body); row.pack(fill='x')
        self.buttons={b:tk.BooleanVar() for b in BUTTONS}
        for b,var in self.buttons.items():ttk.Checkbutton(row,style='Inspector.TCheckbutton',text=b,variable=var).pack(side='left')
        row=ttk.Frame(body);row.pack(fill='x')
        self.x=tk.StringVar(value='0');self.y=tk.StringVar(value='0');self.n=tk.StringVar(value='1')
        for name,var in [('X',self.x),('Y',self.y),('Steps',self.n)]:
            ttk.Label(row,text=name).pack(side='left');ttk.Entry(row,style='Inspector.TEntry',textvariable=var,width=5).pack(side='left')
        ttk.Button(row,style='Inspector.TButton',text='Step +1',command=lambda:self.step(1)).pack(side='left')
        ttk.Button(row,style='Inspector.TButton',text='Run timeline',command=self.step).pack(side='left')
        ttk.Button(row,style='Inspector.TButton',text='Export CSV / JSON',command=self.export).pack(side='left')
        ttk.Button(row,style='Inspector.TButton',text='Compare JSON',command=self.compare).pack(side='left')
        ttk.Button(row,style='Inspector.TButton',text='Clear comparison',command=self.clear_compare).pack(side='left')
        edit=ttk.Frame(body);edit.pack(fill='x');edit.columnconfigure(0,weight=1);edit.columnconfigure(1,weight=1)
        ttk.Label(edit,text='Watches: name type address / root->hex offset (s16 supported)').grid(row=0,column=0,sticky='w')
        ttk.Label(edit,text='Timeline: frame or range, buttons (+), X, Y').grid(row=0,column=1,sticky='w')
        self.watches=tk.Text(edit,height=3,width=40);self.watches.grid(row=1,column=0,sticky='ew')
        self.timeline=tk.Text(edit,height=3,width=35);self.timeline.grid(row=1,column=1,sticky='ew')
        self.restore_editor_settings()
        for editor in (self.watches,self.timeline):
            editor.edit_modified(False)
            editor.bind('<<Modified>>',self._editor_modified,add='+')
        self.n.trace_add('write',lambda *_:self._schedule_save())
        actions=ttk.Frame(edit);actions.grid(row=2,column=0,sticky='w')
        ttk.Button(actions,style='Inspector.TButton',text='Apply watches (paused)',command=self.apply_watches).pack(side='left')
        ttk.Button(actions,style='Inspector.TButton',text='JP controller preset',command=self.controller_preset).pack(side='left')
        ttk.Button(actions,style='Inspector.TButton',text='Locate Player (JP)',command=self.locate_player).pack(side='left')
        grid=ttk.Frame(body);grid.pack(fill='both',expand=True);grid.rowconfigure(0,weight=1);grid.columnconfigure(0,weight=1)
        self.table=ttk.Treeview(grid,show='headings');self.table.grid(row=0,column=0,sticky='nsew')
        for orient,cmd,r,c,sticky in [('vertical',self.table.yview,0,1,'ns'),('horizontal',self.table.xview,1,0,'ew')]:
            sb=ttk.Scrollbar(grid,orient=orient,command=cmd);sb.grid(row=r,column=c,sticky=sticky);self.table.configure(**{('y' if orient=='vertical' else 'x')+'scrollcommand':sb.set})
        self.table.tag_configure('changed',background='#a45a14',foreground='white');self.table.tag_configure('different',background='#8b2635',foreground='white')
        for key in ('<Control-a>','<Control-A>') + (('<Command-a>','<Command-A>') if sys.platform=='darwin' else ()):
            self.table.bind(key,self.select_all_trace)
        for key in ('<Control-c>','<Control-C>') + (('<Command-c>','<Command-C>') if sys.platform=='darwin' else ()):
            self.table.bind(key,lambda _event:self.copy_trace(selected=True))
        for key in ('<ButtonPress-1>','<Up>','<Down>','<Home>','<End>'):
            self.table.bind(key,lambda _event:setattr(self,'trace_select_all',False),add='+')
        self.drain_id=root.after(50,self.drain)
        self.poll_id=root.after(700,self.poll)

    def restore_editor_settings(self):
        values=load_editor_preferences(self.settings_path)
        if not values:return
        self.watches.insert('1.0',values['watches']);self.timeline.insert('1.0',values['timeline'])
        self.n.set(values['steps'] or '1')
        if values['located'] and values['watches'].strip():
            self.located_text=values['watches'].strip()
        self.settings_last=(values['watches'],values['timeline'],self.n.get(),bool(self.located_text))

    def _editor_modified(self,event):
        if event.widget.edit_modified():
            event.widget.edit_modified(False)
            self._schedule_save()

    def _schedule_save(self):
        if self.closed:return
        if self.settings_job is not None:self.root.after_cancel(self.settings_job)
        self.settings_job=self.root.after(350,self.save_editor_settings)

    def save_editor_settings(self):
        if self.settings_job is not None:
            self.root.after_cancel(self.settings_job);self.settings_job=None
        try:
            watches=self.watches.get('1.0','end-1c');timeline=self.timeline.get('1.0','end-1c');steps=self.n.get()
        except tk.TclError:return  # parent already destroyed its editor widgets
        located=bool(self.located_text and watches.strip()==self.located_text)
        snapshot=(watches,timeline,steps,located)
        if snapshot==self.settings_last:return
        if self.settings_last is None and snapshot==('','','1',False):return
        try:
            save_editor_preferences(self.settings_path,watches=watches,timeline=timeline,steps=steps,located=located)
            self.settings_last=snapshot
        except (OSError,ValueError) as exc:
            if not self.closed:self.status.set(f'Could not save inspector editor: {exc}')

    def set_setup_visible(self,visible):
        self.setup_visible=bool(visible)
        if visible:
            self.setup.pack(fill='x',before=self.command_bar)
        else:
            self.setup.pack_forget()
        self.setup_button.configure(text='Hide setup' if visible else 'Show setup')

    def toggle_setup(self):
        self.set_setup_visible(not self.setup_visible)

    def browse(self,key):
        path=filedialog.askdirectory() if key in ('data','config') else filedialog.askopenfilename()
        if path:self.paths[key].set(path)

    def find_installation(self):
        if self.process:return
        brew=shutil.which('brew')
        try:
            if sys.platform=='darwin':
                if not brew:raise RuntimeError('Homebrew was not found; choose installed files manually')
                result=subprocess.run([brew,'--prefix','mupen64plus'],check=True,capture_output=True,text=True,timeout=5)
                prefix=result.stdout.strip()
                if not prefix or not Path(prefix).is_dir():raise RuntimeError('Homebrew did not return an installed Mupen64Plus prefix')
                found=discover_prefix(prefix)
            elif sys.platform.startswith('linux'):
                # Choose one installation, not a mixture of plugin releases.
                choices=[discover_prefix(prefix) for prefix in ('/usr','/usr/local')]
                found=max(choices,key=lambda item:sum(k in item for k in ('core','gfx','audio','rsp','data')))
            else:
                raise RuntimeError('Select installed native libraries manually')
            for k,v in found.items():
                if k!='input' or not self.paths[k].get():self.paths[k].set(v)
            self.status.set('Detected: '+', '.join(found)+'. Physical input is optional; select stock SDL input plugin if missing.')
            if self._using_default_input():
                self._request_default_build(retry=True)

        except (OSError,subprocess.SubprocessError,RuntimeError) as exc:self.status.set(str(exc))

    def _using_default_input(self):
        path=self.paths['input'].get().strip()
        return not path or Path(path).expanduser().resolve()==default_input_path().resolve()

    def _request_default_build(self, *, retry=False):
        self.build_future=request_input_build(retry=retry)
        self._poll_input_build()

    def _poll_input_build(self):
        future=self.build_future
        if future is None:return
        if not future.done():
            if not self.process:self.status.set('Preparing bundled Mupen64Plus input plugin…')
            return
        self.build_future=None
        if self.process or not self._using_default_input():return
        try:
            self.paths['input'].set(str(future.result()))
            self.status.set('Native input plugin ready. Choose ROM and launch session.' +
                            ('' if self.paths['physical_input'].get() else ' Stock SDL input provider not found.'))
        except Exception as exc:
            self.status.set(str(exc))

    def start(self):
        if self.closed or self.process is not None:return
        try:
            if self._using_default_input():
                future=request_input_build()
                if not future.done():
                    self.build_future=future
                    self.status.set('Preparing bundled Mupen64Plus input plugin…')
                    return
                self.paths['input'].set(str(future.result()))
            paths={k:v.get().strip() for k,v in self.paths.items()}
            if any(not v for k,v in paths.items() if k!='physical_input'):
                raise ValueError('Required paths missing. Find Mupen64Plus installation and select the ROM.')
            self.managed_ram=None; self.session_rom=Path(paths['rom']).resolve()
            args=[sys.executable,'-m','practice.mupen_native']
            for key,val in paths.items():args.extend(['--'+key,val])
            self.save_editor_settings()
            watch_text=self.watches.get('1.0','end-1c')
            # A saved locator result is an editor draft, not validated in a new child.
            needs_relocate=bool(self.located_text and watch_text.strip()==self.located_text)
            args.extend(['--watches','' if needs_relocate else watch_text])
            # Keep the SDL/native core on the child process main thread.
            self.process=subprocess.Popen(args,cwd=str(Path(__file__).resolve().parents[1]),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',bufsize=1)
        except (OSError,ValueError,RuntimeError) as exc:self.status.set(str(exc));return
        self._cancel_render();self.generation+=1;gen=self.generation;proc=self.process;self.busy=True;self.inflight='launch';self.pending=None;self.report=None;self.reference=None;self.last_render=None;self.last_error='';self.trace_select_all=False
        self.last_activity=time.monotonic();self.stalled=False;self.protocol_failed=False;self.recovery_path=None
        self.start_button.state(['disabled']); self.set_setup_visible(False); self.status.set('Starting native core…' + (' Pause and locate the player again.' if needs_relocate else ''))
        last_log=['']
        def logs():
            try:
                for line in proc.stderr:
                    if line.strip():last_log[0]=line.strip()[-500:]
            except (OSError,ValueError):pass
        def read():
            reader=TraceReader(); failed=False
            try:
                for line in proc.stdout:
                    if failed:continue  # keep draining even after protocol fault
                    try:
                        value=reader.receive(line)
                        if value is not None:self.events.put((gen,'report',value))
                    except (ValueError,KeyError,TypeError) as exc:
                        failed=True;self.events.put((gen,'protocol_error',str(exc)))
                if reader.pending is not None and not failed:self.events.put((gen,'protocol_error','Incomplete final report'))
            except (OSError,ValueError) as exc:self.events.put((gen,'protocol_error',str(exc)))
            code=proc.wait(); self.events.put((gen,'exit',f'Emulator exited ({code}). {last_log[0]}'))
        threading.Thread(target=logs,daemon=True).start()
        threading.Thread(target=read,daemon=True).start()

    def default(self):
        return controller_input([name for name,var in self.buttons.items() if var.get()],int(self.x.get()),int(self.y.get()))

    def control(self,op,**fields):
        if self.closed or not self.process:return
        if self.protocol_failed or self.stalled:
            if op=='stop' and messagebox.askyesno('Stop stalled emulator?', 'Stop this managed emulator process? Unsaved gameplay may be lost; the latest trace checkpoint is retained.',parent=self.root):
                try:self.process.terminate()
                except OSError as exc:self.status.set(str(exc))
            return
        try:
            if op=='hold' and 'input' not in fields:fields['input']=self.default()
            if self.busy:
                if op!='status' and self.inflight=='status' and self.pending is None:
                    self.pending=(op,fields)
                elif op!='status':self.status.set('Command in progress; wait for its result')
                return
            if op!='status':self.last_error=''
            self.process.stdin.write(json.dumps(dict(op=op,**fields))+'\n');self.process.stdin.flush()
            self.busy=True;self.inflight=op;self.last_activity=time.monotonic();self.stalled=False
            if op=='step':self.status.set(f"Stepping 0/{len(fields['inputs'])} core frames…")
        except (OSError,ValueError) as exc:self.status.set(str(exc))

    def state_hotkey(self,event,op):
        if event.widget is self.body or str(event.widget).startswith(str(self.body)+'.'):
            self.state_action(op);return 'break'

    def state_action(self,op):
        r=self.report
        if not self.process or not r or not r.get('capabilities',{}).get('savestate_control'):
            self.status.set('Managed states require a running native core 2.6.0');return
        if r['state']!=3 or r['recording'] or r.get('state_job_pending'):
            self.status.set('Pause and stop recording before using a savestate');return
        try:
            slot=int(self.slot.get())
            if not 0<=slot<=9:raise ValueError('Choose a slot from 0 to 9')
        except ValueError as exc:self.status.set(str(exc));return
        if op=='load_state' and not messagebox.askyesno('Load savestate?', 'Restore this slot? Current gameplay and the active trace will be replaced. The latest trace checkpoint remains recoverable; reapply or relocate watches after loading.',parent=self.root):return
        self.control(op,slot=slot,confirm=True)

    def unlock_mini(self):
        r=self.report
        if not self.process or not r or not r.get('capabilities',{}).get('mini_unlock'):
            self.status.set('Mini Ebisumaru unlock requires Japan-0 and Mupen64Plus 2.6.0');return
        if r['state']!=3 or r['recording']:
            self.status.set('Pause and stop recording before unlocking');return
        if r['rows']:
            self.status.set('Export and clear the trace before unlocking');return
        if messagebox.askyesno('Unlock Mini Ebisumaru',
                'Only use this after entering normal gameplay. Advance one neutral core frame and grant the miniature ability? This changes the in-game unlock, not the active form.',parent=self.root):
            self.control('unlock_mini',confirm=True)

    def controller_preset(self):
        if self.report and self.process and self.report['region']!='japan':
            self.status.set('JP controller preset requires Japan-0');return
        if self.watches.get('1.0','end').strip() and not messagebox.askyesno(
                'Replace watch editor?', 'Replace the editor text with the Japan controller preset?',parent=self.root):return
        self.watches.delete('1.0','end');self.watches.insert('1.0',JP_CONTROLLER_WATCHES)
        self.status.set('JP controller preset loaded; apply while paused or launch Japan-0')

    def apply_watches(self):
        if not self.process:
            self.status.set('Watches will be applied when launching the session');return
        if not self.report or self.report['state']!=3 or self.report['recording']:
            self.status.set('Pause and stop recording before applying watches');return
        # No implicit deletion of a recording. An explicit confirmation is
        # required even if a status response is in flight.
        replace=False
        if self.report['rows']:
            replace=messagebox.askyesno('Replace watch set?', 'Changing watches clears the current trace. Export it first if needed. Apply and clear?',parent=self.root)
            if not replace:return
        watch_text=self.watches.get('1.0','end-1c')
        self.save_editor_settings()
        if self.located_text and watch_text.strip()==self.located_text:
            # Re-resolve the candidate instead of trusting a saved absolute address.
            self.control('locate_player',replace_trace=replace)
        else:
            self.control('watches',text=watch_text,replace_trace=replace)

    def locate_player(self):
        if not self.process or not self.report or self.report['state']!=3 or self.report['recording']:
            self.status.set('Pause and stop recording before locating the player');return
        if self.report['region']!='japan':
            self.status.set('Locate Player requires Japan-0');return
        replace=False
        if self.report['rows']:
            replace=messagebox.askyesno('Replace watch set?', 'Export the trace first. Locate Player and replace watches and clear trace?',parent=self.root)
            if not replace:return
        self.control('locate_player',replace_trace=replace)

    def step(self,n=None):
        try:
            self.save_editor_settings()
            default=self.default()
            # Single-step is independent of the retained multi-frame timeline.
            inputs=([default] if n==1 else parse_inputs(self.timeline.get('1.0','end'),int(self.n.get()) if n is None else n,default,max_count=MAX_NATIVE_STEPS))
            self.control('step',inputs=inputs)
        except ValueError as exc:self.status.set(str(exc))

    def select_all_trace(self,_event=None):
        self.trace_select_all=True
        self.table.selection_set(self.table.get_children())
        return 'break'

    def copy_recovered(self):
        try:
            if not self.recovery_path:raise ValueError('No recovery checkpoint from this session')
            path=Path(self.recovery_path)
            if path.stat().st_size>16000000:raise ValueError('Recovery checkpoint exceeds 16 MB')
            report=json.loads(path.read_text(encoding='utf-8'))
            self.copy_trace(report=report)
        except (OSError,ValueError,KeyError,TypeError) as exc:self.status.set(f'Trace recovery unavailable: {exc}')

    def copy_trace(self,selected=False,report=None):
        r=self.report if report is None else report
        if not r or not r['rows']:
            self.status.set('No captured rows to copy');return 'break'
        rows=r['rows'];columns=['serial','frame','polls','buttons','x','y']+[w['name'] for w in r['watches']]
        if selected and not self.trace_select_all:
            indices=sorted(int(i) for i in self.table.selection())
            rows=[rows[i] for i in indices if i<len(rows)]
        if not rows:
            self.status.set('No captured rows selected');return 'break'
        stream=io.StringIO();writer=csv.writer(stream,delimiter='\t',lineterminator='\n')
        writer.writerow(columns)
        writer.writerows([str(row.get(k)) if k in row else '' for k in columns] for row in rows)
        try:
            self.root.clipboard_clear();self.root.clipboard_append(stream.getvalue())
            self.status.set(f'Copied {len(rows)} captured rows as tab-separated text (original trace).')
        except tk.TclError as exc:self.status.set(f'Clipboard unavailable: {exc}')
        return 'break'

    def export(self):
        if not self.report:return
        path=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json'),('CSV','*.csv')])
        if path:
            try:write_trace(path,self.report)
            except (OSError,ValueError,KeyError) as exc:self.status.set(str(exc))

    def compare(self):
        if not self.report:return
        path=filedialog.askopenfilename(filetypes=[('JSON','*.json')])
        if not path:return
        try:
            if Path(path).stat().st_size>16000000:raise ValueError('Reference exceeds 16 MB')
            other=json.loads(Path(path).read_text())
            if any(other[k]!=self.report[k] for k in ('region','boundary','watches')) or not isinstance(other['rows'],list) or len(other['rows'])>MAX_TRACE_ROWS or not all(isinstance(r,dict) for r in other['rows']):raise ValueError('Incompatible reference trace')
            self.reference=other;self.render()
        except (OSError,ValueError,KeyError,TypeError) as exc:self.status.set(str(exc))

    def clear_compare(self):
        self.reference=None;self.render()

    def _cancel_render(self):
        if self.render_job is not None:
            self.root.after_cancel(self.render_job);self.render_job=None

    def render(self):
        if not self.report:return
        snapshot=(self.report['rows'],self.report['watches'],self.reference)
        previous=self.last_render
        if snapshot==previous:return
        self._cancel_render()
        rows,watches,ref=snapshot
        append_only=(previous is not None and previous[1]==watches and previous[2] is None
                     and ref is None and len(rows)>=len(previous[0]) and rows[:len(previous[0])]==previous[0])
        self.last_render=snapshot
        if not append_only:
            self.trace_select_all=False;self.render_cursor=0
            self.table.delete(*self.table.get_children())
            columns=['serial','frame','polls','buttons','x','y']+[w['name'] for w in watches]
            self.table['columns']=columns
            for name in columns:self.table.heading(name,text=name);self.table.column(name,width=90)
        self._render_chunk()

    def _render_chunk(self):
        self.render_job=None
        if self.closed or self.last_render is None:return
        rows,watches,reference=self.last_render;ref=reference['rows'] if reference else []
        columns=['serial','frame','polls','buttons','x','y']+[w['name'] for w in watches]
        total=max(len(rows),len(ref));end=min(total,self.render_cursor+100)
        for i in range(self.render_cursor,end):
            r=rows[i] if i<len(rows) else {};p=rows[i-1] if 0<i<len(rows) else r
            other=ref[i] if i<len(ref) else {}
            changed=any(r.get(k)!=p.get(k) for k in columns[2:]);different=reference is not None and (i>=len(rows) or i>=len(ref) or any(r.get(k)!=other.get(k) for k in columns[2:]))
            values=[f'{r.get(k)} / {other.get(k)}' if different and k not in ('serial','frame') and r.get(k)!=other.get(k) else r.get(k,'') for k in columns]
            self.table.insert('','end',iid=str(i),values=values,tags=('different',) if different else ('changed',) if changed else ())
        if self.trace_select_all and end>self.render_cursor:
            self.table.selection_add(tuple(str(i) for i in range(self.render_cursor,end)))
        self.render_cursor=end
        if end<total:self.render_job=self.root.after(1,self._render_chunk)

    def drain(self):
        if self.closed:return
        self._poll_input_build()
        try:
            while True:
                gen,kind,payload=self.events.get_nowait()
                if gen!=self.generation:continue
                if kind=='protocol_error':
                    self.protocol_failed=True;self.busy=True;self.pending=None
                    self.status.set(f'Native protocol error: {payload}. Recover latest trace or stop emulator.')
                    continue
                if self.protocol_failed and kind!='exit':continue
                self.last_activity=time.monotonic();self.stalled=False
                if kind=='report' and payload.get('progress'):
                    progress=payload['progress']
                    if self.inflight=='step':
                        if 'report' in payload:
                            self.report=payload['report'];self.recovery_path=self.report.get('recovery_path',self.recovery_path)
                            self.managed_ram=payload.get('managed_ram');self.render()
                        self.status.set(f"Stepping {progress['done']}/{progress['total']} core frames…" if progress['done']<progress['total'] else 'Final frame complete; receiving final report…')
                    continue  # progress is not command completion
                completed=self.inflight
                self.busy=False;self.inflight=None
                if kind=='exit':
                    self.process=None;self.managed_ram=None;self.session_rom=None;self.pending=None;self.protocol_failed=False;self.start_button.state(['!disabled']);self.mini_button.state(['disabled']);self.watches.configure(state='normal');self.set_setup_visible(True);self.status.set(self.last_error or payload)
                elif not payload['ok']:
                    self.last_error=payload['error']
                    if 'report' in payload:
                        previous=self.report;self.report=payload['report'];self.managed_ram=payload.get('managed_ram')
                        self.recovery_path=self.report.get('recovery_path',self.recovery_path)
                        if previous and previous['watches']!=self.report['watches']:self.reference=None;self.last_render=None
                        self.render()
                    self.status.set(self.last_error)
                else:
                    previous=self.report;self.report=payload['report'];r=self.report
                    self.managed_ram=payload.get('managed_ram')
                    self.recovery_path=r.get('recovery_path',self.recovery_path)
                    if completed=='load_state':self.reference=None;self.last_render=None
                    if completed=='locate_player' and r.get('player_text'):
                        self.located_text=r['player_text'].strip()
                        self.watches.delete('1.0','end');self.watches.insert('1.0',r['player_text'])
                        self.save_editor_settings()
                    if previous and previous['watches']!=r['watches']:
                        self.reference=None;self.last_render=None
                    can_unlock=r.get('capabilities',{}).get('mini_unlock') and r['state']==3 and not r['recording']
                    self.mini_button.state(['!disabled'] if can_unlock else ['disabled'])
                    unlocked=r.get('mini_unlock')
                    notice=('Mini Ebisumaru ability granted (verified RAM readback)' if unlocked and unlocked['changed'] else 'Mini Ebisumaru ability already unlocked' if unlocked else '')
                    state={1:'Starting / stopped',2:'Running',3:'Paused'}.get(r['state'],'Unknown')
                    errors=r.get('watch_errors',{})
                    diagnostic=(f"{len(errors)} watch(s) unavailable: "+'; '.join(f'{k}: {v}' for k,v in list(errors.items())[:2])) if errors else ''
                    player=f" | task 0x{r['player_base']:08X}" if r.get('player_base') else ''
                    if not r.get('player_base') and self.located_text and self.watches.get('1.0','end-1c').strip()==self.located_text and not diagnostic:
                        diagnostic='Saved player watches: pause and Locate Player again.'
                    job_notice=('Unacknowledged savestate job; stop and relaunch' if r.get('state_job_pending') else r.get('state_job_notice',''))
                    recovery_notice=('Trace checkpoint failed: '+r['recovery_error'] if r.get('recovery_error') else '')
                    self.status.set(f"{r['region']} | {state} | core callback {r['serial']} | {len(r['rows'])}/{MAX_TRACE_ROWS} captured | {r.get('input_mode','scripted')} input | recording {r['recording']}{player} | {r.get('ram_reader','')} | {self.last_error or r['error'] or job_notice or diagnostic or notice or recovery_notice}");self.render()
        except queue.Empty:pass
        if self.process and self.busy and not self.protocol_failed and not self.stalled and self.last_activity and time.monotonic()-self.last_activity>20:
            self.stalled=True;self.pending=None
            self.status.set(f'No native response for 20s ({self.inflight}). Recover latest trace; Stop emulator if unresponsive.')
        if self.process and not self.busy and self.pending:
            op,fields=self.pending;self.pending=None;self.control(op,**fields)
        if self.drain_id is not None:
            self.root.after_cancel(self.drain_id)
        self.drain_id=self.root.after(50,self.drain)

    def managed_attachment(self):
        """Only a live child and its own private-pipe metadata are eligible."""
        p=self.process; m=self.managed_ram
        if (p is None or not m or p.poll() is not None or not self.session_rom
                or m.get('pid')!=p.pid or m.get('region')!='japan'
                or m.get('size')!=0x400000 or type(m.get('base')) is not int
                or m['base']<=0 or m['base']%16):
            return None
        return p, m['base'], self.session_rom

    def manual_edits_paused(self):
        r=self.report
        return bool(r and r['state']==3 and not r['recording'] and not r.get('state_job_pending')
                    and not self.stalled and not self.protocol_failed
                    and self.inflight in (None,'status') and self.pending is None)

    def poll(self):
        if self.closed:return
        if self.process and not self.busy and self.pending is None:self.control('status')
        self.poll_id=self.root.after(700,self.poll)

    def _body_destroyed(self,event):
        if event.widget is self.body:self.shutdown()

    def shutdown(self):
        # Tk can destroy the parent without invoking a window protocol.
        # This is idempotent and leaves an unrelated toolkit root untouched.
        if self.closed:return
        self.save_editor_settings()
        self._cancel_render()
        self.closed=True
        for key,funcid in self.state_bindings:
            try:self.root.unbind(key,funcid)
            except tk.TclError:pass
        self.generation+=1
        self.pending=None
        for callback in (self.drain_id,self.poll_id):
            try:self.root.after_cancel(callback)
            except tk.TclError:pass
        proc,self.process=self.process,None
        if proc:
            try:proc.stdin.close()
            except (OSError,ValueError):pass
            # EOF requests normal core shutdown; do not block Tk.

    def close(self):
        self.shutdown()
        if self.embedded:self.body.destroy()
        else:self.root.destroy()


def main():
    root=tk.Tk();ui=NativeFrameUi(root);ui.find_installation();root.mainloop()

if __name__=='__main__':main()
