"""Standalone or embedded UI for the native Mupen64Plus research session."""
from __future__ import annotations
import json
import shutil
from pathlib import Path
import queue
import subprocess
import sys
import sysconfig
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from practice.mupen_native import PREFIX, write_trace
from practice.mupen_input_build import default_input_path, request_input_build

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
    def __init__(self, root, *, parent=None):
        self.root=root; self.process=None; self.busy=False; self.report=None; self.reference=None
        self.events=queue.Queue(); self.generation=0; self.closed=False
        self.pending=None; self.inflight=None; self.last_render=None; self.last_error=''
        self.managed_ram=None; self.session_rom=None
        self.build_future=None
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
        ttk.Label(edit,text='Timeline: relative step, buttons (+), X, Y').grid(row=0,column=1,sticky='w')
        self.watches=tk.Text(edit,height=3,width=40);self.watches.grid(row=1,column=0,sticky='ew')
        self.timeline=tk.Text(edit,height=3,width=35);self.timeline.grid(row=1,column=1,sticky='ew')
        actions=ttk.Frame(edit);actions.grid(row=2,column=0,sticky='w')
        ttk.Button(actions,style='Inspector.TButton',text='Apply watches (paused)',command=self.apply_watches).pack(side='left')
        ttk.Button(actions,style='Inspector.TButton',text='JP controller preset',command=self.controller_preset).pack(side='left')
        grid=ttk.Frame(body);grid.pack(fill='both',expand=True);grid.rowconfigure(0,weight=1);grid.columnconfigure(0,weight=1)
        self.table=ttk.Treeview(grid,show='headings');self.table.grid(row=0,column=0,sticky='nsew')
        for orient,cmd,r,c,sticky in [('vertical',self.table.yview,0,1,'ns'),('horizontal',self.table.xview,1,0,'ew')]:
            sb=ttk.Scrollbar(grid,orient=orient,command=cmd);sb.grid(row=r,column=c,sticky=sticky);self.table.configure(**{('y' if orient=='vertical' else 'x')+'scrollcommand':sb.set})
        self.table.tag_configure('changed',background='#a45a14',foreground='white');self.table.tag_configure('different',background='#8b2635',foreground='white')
        self.drain_id=root.after(50,self.drain)
        self.poll_id=root.after(700,self.poll)

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
            args.extend(['--watches',self.watches.get('1.0','end')])
            # Keep the SDL/native core on the child process main thread.
            self.process=subprocess.Popen(args,cwd=str(Path(__file__).resolve().parents[1]),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        except (OSError,ValueError,RuntimeError) as exc:self.status.set(str(exc));return
        self.generation+=1;gen=self.generation;proc=self.process;self.busy=True;self.inflight='launch';self.pending=None;self.report=None;self.reference=None;self.last_render=None;self.last_error=''
        self.start_button.state(['disabled']); self.set_setup_visible(False); self.status.set('Starting native core…')
        def read():
            last_log=''
            for line in proc.stdout:
                if line.startswith(PREFIX):
                    try:self.events.put((gen,'report',json.loads(line[len(PREFIX):])))
                    except ValueError:pass
                elif line.strip():last_log=line.strip()
            code=proc.wait(); self.events.put((gen,'exit',f'Emulator exited ({code}). {last_log}'))
        threading.Thread(target=read,daemon=True).start()

    def default(self):
        return controller_input([name for name,var in self.buttons.items() if var.get()],int(self.x.get()),int(self.y.get()))

    def control(self,op,**fields):
        if self.closed or not self.process:return
        try:
            if op=='hold' and 'input' not in fields:fields['input']=self.default()
            if self.busy:
                if op!='status' and self.inflight=='status' and self.pending is None:
                    self.pending=(op,fields)
                elif op!='status':self.status.set('Command in progress; wait for its result')
                return
            if op!='status':self.last_error=''
            self.process.stdin.write(json.dumps(dict(op=op,**fields))+'\n');self.process.stdin.flush()
            self.busy=True;self.inflight=op
        except (OSError,ValueError) as exc:self.status.set(str(exc))

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
        self.control('watches',text=self.watches.get('1.0','end'),replace_trace=replace)

    def step(self,n=None):
        try:self.control('step',inputs=parse_inputs(self.timeline.get('1.0','end'),int(self.n.get()) if n is None else n,self.default()))
        except ValueError as exc:self.status.set(str(exc))

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
            if Path(path).stat().st_size>4000000:raise ValueError('Reference exceeds 4 MB')
            other=json.loads(Path(path).read_text())
            if any(other[k]!=self.report[k] for k in ('region','boundary','watches')) or not isinstance(other['rows'],list) or len(other['rows'])>600 or not all(isinstance(r,dict) for r in other['rows']):raise ValueError('Incompatible reference trace')
            self.reference=other;self.render()
        except (OSError,ValueError,KeyError,TypeError) as exc:self.status.set(str(exc))

    def clear_compare(self):
        self.reference=None;self.render()

    def render(self):
        if not self.report:return
        snapshot=(self.report['rows'],self.report['watches'],self.reference)
        if snapshot==self.last_render:return
        self.last_render=snapshot
        rows=self.report['rows'];ref=self.reference['rows'] if self.reference else []
        columns=['serial','frame','polls','buttons','x','y']+[w['name'] for w in self.report['watches']]
        self.table.delete(*self.table.get_children());self.table['columns']=columns
        for name in columns:self.table.heading(name,text=name);self.table.column(name,width=90)
        for i in range(max(len(rows),len(ref))):
            r=rows[i] if i<len(rows) else {};p=rows[i-1] if 0<i<len(rows) else r
            other=ref[i] if i<len(ref) else {}
            changed=any(r.get(k)!=p.get(k) for k in columns[2:]);different=self.reference is not None and (i>=len(rows) or i>=len(ref) or any(r.get(k)!=other.get(k) for k in columns[2:]))
            values=[f'{r.get(k)} / {other.get(k)}' if different and k not in ('serial','frame') and r.get(k)!=other.get(k) else r.get(k,'') for k in columns]
            self.table.insert('','end',values=values,tags=('different',) if different else ('changed',) if changed else ())

    def drain(self):
        if self.closed:return
        self._poll_input_build()
        try:
            while True:
                gen,kind,payload=self.events.get_nowait()
                if gen!=self.generation:continue
                self.busy=False;self.inflight=None
                if kind=='exit':
                    self.process=None;self.managed_ram=None;self.session_rom=None;self.pending=None;self.start_button.state(['!disabled']);self.mini_button.state(['disabled']);self.watches.configure(state='normal');self.set_setup_visible(True);self.status.set(self.last_error or payload)
                elif not payload['ok']:self.last_error=payload['error'];self.status.set(self.last_error)
                else:
                    previous=self.report;self.report=payload['report'];r=self.report
                    self.managed_ram=payload.get('managed_ram')
                    if previous and previous['watches']!=r['watches']:
                        self.reference=None;self.last_render=None
                    can_unlock=r.get('capabilities',{}).get('mini_unlock') and r['state']==3 and not r['recording']
                    self.mini_button.state(['!disabled'] if can_unlock else ['disabled'])
                    unlocked=r.get('mini_unlock')
                    notice=('Mini Ebisumaru ability granted (verified RAM readback)' if unlocked and unlocked['changed'] else 'Mini Ebisumaru ability already unlocked' if unlocked else '')
                    state={1:'Starting / stopped',2:'Running',3:'Paused'}.get(r['state'],'Unknown')
                    self.status.set(f"{r['region']} | {state} | core callback {r['serial']} | {len(r['rows'])} captured | {r.get('input_mode','scripted')} input | recording {r['recording']} | {self.last_error or r['error'] or notice}");self.render()
        except queue.Empty:pass
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
        return bool(r and r['state']==3 and not r['recording']
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
        self.closed=True
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
