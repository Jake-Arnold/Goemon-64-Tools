"""Tk interface for bounded declarative debugger tracing scripts.

Uses Toolkit's existing PID -> RDRAM session and its main-loop tick. There is
no shell, eval/exec, game-memory write or assumed CPU instrumentation.
"""
from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk

from practice.scripted_trace import (MAX_SCRIPT_BYTES, PRESETS, ScriptedTracer,
                                     parse_script)
from practice.theme import PALETTE


class ScriptedTraceUiMixin:
    def _build_scripted_trace_page(self,pages):
        self.scripted_tracer=ScriptedTracer()
        self.scripted_trace_status=tk.StringVar(value='Stopped — read-only guest RAM observation')
        self.scripted_trace_preset=tk.StringVar(value='Script VM / dialogue')
        self.scripted_trace_mark=tk.StringVar(value='Start of dialogue')
        self.scripted_trace_sample_info=tk.StringVar(value='Samples: 0  /  Events: 0')
        page=ttk.Frame(pages,padding=8)
        pages.add(page,text='Scripted tracer')
        self.scripted_trace_tab=page

        hint=('Declarative JSON scripts read guest RAM without modifying gameplay. '
              'Samples are limited by the toolkit refresh loop (~170 ms); '
              'transient writes and native function calls may be missed.')
        ttk.Label(page,text=hint,style='Muted.TLabel',wraplength=1050).pack(anchor='w',pady=(0,7))
        bar=ttk.Frame(page);bar.pack(fill='x',pady=2)
        ttk.Label(bar,text='Preset').pack(side='left')
        ttk.Combobox(bar,textvariable=self.scripted_trace_preset,state='readonly',width=27,
                     values=tuple(PRESETS)).pack(side='left',padx=4)
        ttk.Button(bar,text='Load preset',command=self.scripted_trace_load_preset).pack(side='left',padx=2)
        ttk.Button(bar,text='Open script…',command=self.scripted_trace_load_file).pack(side='left',padx=2)
        ttk.Button(bar,text='Save script…',command=self.scripted_trace_save_file).pack(side='left',padx=2)

        row=ttk.Frame(page);row.pack(fill='x',pady=3)
        self.scripted_trace_start_button=ttk.Button(row,text='Start trace',command=self.scripted_trace_start,style='Gold.TButton')
        self.scripted_trace_start_button.pack(side='left')
        ttk.Button(row,text='Stop trace',command=self.scripted_trace_stop).pack(side='left',padx=3)
        ttk.Label(row,text='Marker').pack(side='left',padx=(15,3))
        ttk.Entry(row,textvariable=self.scripted_trace_mark,width=28).pack(side='left')
        ttk.Button(row,text='Mark',command=self.scripted_trace_add_mark).pack(side='left',padx=3)
        ttk.Button(row,text='Export JSON',command=lambda:self.scripted_trace_export('json')).pack(side='right',padx=2)
        ttk.Button(row,text='Export JSONL',command=lambda:self.scripted_trace_export('jsonl')).pack(side='right',padx=2)
        ttk.Label(page,textvariable=self.scripted_trace_status,wraplength=1050).pack(anchor='w',pady=3)
        ttk.Label(page,textvariable=self.scripted_trace_sample_info,style='Muted.TLabel').pack(anchor='w')

        body=ttk.Panedwindow(page,orient='horizontal');body.pack(fill='both',expand=True,pady=(4,2))
        edit_frame=ttk.LabelFrame(body,text='Trace script (read-only operations)',padding=5)
        event_frame=ttk.LabelFrame(body,text='Recent observed events',padding=5)
        body.add(edit_frame,weight=3);body.add(event_frame,weight=2)

        script_panel=ttk.Frame(edit_frame);script_panel.pack(fill='both',expand=True)
        self.scripted_trace_editor=tk.Text(script_panel,wrap='none',undo=True,font=('Consolas',10),
                         background=PALETTE['surface'],foreground=PALETTE['foreground'],
                         insertbackground=PALETTE['gold'],selectbackground=PALETTE['red'],
                         height=18)
        self.scripted_trace_editor.pack(side='left',fill='both',expand=True)
        scrollbar=ttk.Scrollbar(script_panel,orient='vertical',command=self.scripted_trace_editor.yview)
        scrollbar.pack(side='right',fill='y');self.scripted_trace_editor.configure(yscrollcommand=scrollbar.set)
        self.scripted_trace_load_preset()

        events_panel=ttk.Frame(event_frame);events_panel.pack(fill='both',expand=True)
        tree=ttk.Treeview(events_panel,columns=('sample','kind','source','value'),show='headings',height=14)
        self.scripted_trace_tree=tree
        for key,label,width in (('sample','Sample',70),('kind','Type',85),('source','Watch / trigger',160),('value','Observed',180)):
            tree.heading(key,text=label)
            tree.column(key,width=width,stretch=key in ('source','value'))
        tree.pack(side='left',fill='both',expand=True)
        sb=ttk.Scrollbar(events_panel,orient='vertical',command=tree.yview)
        sb.pack(side='right',fill='y');tree.configure(yscrollcommand=sb.set)
        ttk.Label(page,text='Exports contain only configured scalar watches, not a full RAM dump. '
                 'Function-call hooks and exact instruction timing require an instrumented native runtime.',
                  style='Muted.TLabel',wraplength=1050).pack(anchor='w',pady=3)

    def scripted_trace_load_preset(self):
        preset=PRESETS[self.scripted_trace_preset.get()]
        self.scripted_trace_editor.delete('1.0','end')
        self.scripted_trace_editor.insert('1.0',json.dumps(preset,indent=2)+'\n')
        self.scripted_trace_status.set('Preset loaded; start trace to begin live sampling')

    def scripted_trace_load_file(self):
        path=filedialog.askopenfilename(parent=self.root,title='Open guest trace script',
               filetypes=[('Trace script JSON','*.json'),('All files','*')])
        if not path:return
        try:
            source=Path(path)
            if source.stat().st_size>MAX_SCRIPT_BYTES:raise ValueError('Script exceeds 64 KiB')
            text=source.read_text(encoding='utf-8')
            spec=parse_script(text)
            self.scripted_trace_editor.delete('1.0','end')
            self.scripted_trace_editor.insert('1.0',json.dumps(spec.source,indent=2)+'\n')
            self.scripted_trace_status.set(f'Loaded {spec.name} (not running)')
        except (OSError,UnicodeError,ValueError,json.JSONDecodeError) as exc:
            self.scripted_trace_status.set(f'Load rejected: {exc}')

    def scripted_trace_save_file(self):
        try:
            spec=parse_script(self.scripted_trace_editor.get('1.0','end'))
            path=filedialog.asksaveasfilename(parent=self.root,defaultextension='.json',
                     filetypes=[('Trace script JSON','*.json')],title='Save trace script')
            if not path:return
            Path(path).write_text(json.dumps(spec.source,indent=2)+'\n',encoding='utf-8')
            self.scripted_trace_status.set(f'Saved script {spec.name}')
        except (OSError,UnicodeError,ValueError,json.JSONDecodeError) as exc:
            self.scripted_trace_status.set(f'Save rejected: {exc}')

    def scripted_trace_start(self):
        try:
            session=self._debug_attach_session()
            if session.reader is None:raise RuntimeError('Connect to a running game first')
            spec=parse_script(self.scripted_trace_editor.get('1.0','end'))
            if spec.region is not None and spec.region!=session.region:
                raise ValueError(f'Script is for {spec.region.upper()}, but {session.region.upper()} is selected')
            self.scripted_tracer.start(session.reader,spec)
            self.scripted_trace_tree.delete(*self.scripted_trace_tree.get_children())
            self.scripted_trace_status.set(f'Recording: {spec.name} | {len(spec.watches)} watches; {len(spec.triggers)} triggers')
            self._scripted_trace_draw()
        except (OSError,RuntimeError,ValueError,json.JSONDecodeError) as exc:
            self.scripted_trace_status.set(f'Trace not started: {exc}')

    def scripted_trace_stop(self):
        self.scripted_tracer.stop()
        self.scripted_trace_status.set('Stopped. Recorded events remain available for export.')
        self._scripted_trace_draw()

    def scripted_trace_add_mark(self):
        try:
            self.scripted_tracer.mark(self.scripted_trace_mark.get())
            self._scripted_trace_draw()
        except (RuntimeError,ValueError) as exc:self.scripted_trace_status.set(str(exc))

    def _scripted_trace_draw(self):
        if not hasattr(self,'scripted_trace_tree'):return
        s=self.scripted_tracer
        self.scripted_trace_sample_info.set(f'Samples: {s.sample_count}  /  Events retained: {len(s.events)}  '
                 f'/  Complete triggers: {sum(e.get("complete",False) for e in s.events if e["kind"]=="trigger")}')
        tree=self.scripted_trace_tree
        tree.delete(*tree.get_children())
        for i,event in enumerate(s.events[-120:]):
            kind=event['kind'];source=event.get('watch') or event.get('note','')
            if kind=='trigger':
                source=event['trigger'];value='captured' if event['complete'] else 'capturing post…'
            elif kind=='change':value=event['before']+' → '+event['after']
            else:value='manual marker'
            tree.insert('', 'end',iid=f'event{i}',values=(event['sample'],kind,source,value))
        if tree.get_children():tree.see(tree.get_children()[-1])

    def poll_scripted_trace(self,now:float):
        if not hasattr(self,'scripted_tracer'):return
        tracer=self.scripted_tracer
        if not tracer.running:return
        session=self._debug_region_session()
        if tracer.ram is not session.reader or (tracer.spec.region is not None and tracer.spec.region!=session.region):
            tracer.stop()
            self.scripted_trace_status.set('Trace stopped on disconnect/reconnect; events retained for export')
            self._scripted_trace_draw()
            return
        try:
            before=tracer.sample_count
            tracer.poll(now=now)
            if tracer.sample_count!=before and getattr(self,'notebook',None) is not None and self.notebook.select()==str(self.pj64_debugger_tab):
                self._scripted_trace_draw()
        except (OSError,ValueError,RuntimeError) as exc:
            tracer.stop()
            self.scripted_trace_status.set(f'Trace stopped: {exc}')
            self._scripted_trace_draw()

    def scripted_trace_reset_on_connect(self):
        if hasattr(self,'scripted_tracer') and self.scripted_tracer.running:
            self.scripted_tracer.stop()
            self.scripted_trace_status.set('Trace stopped for new connection; export prior events before restarting')
            self._scripted_trace_draw()

    def scripted_trace_export(self,format:str):
        try:
            tracer=self.scripted_tracer
            if tracer.spec is None:raise RuntimeError('No trace session to export')
            if format not in ('json','jsonl'):raise ValueError('Unknown trace export format')
            path=filedialog.asksaveasfilename(parent=self.root,defaultextension='.'+format,
                    filetypes=[('Trace JSONL','*.jsonl')] if format=='jsonl' else [('Trace JSON','*.json')],
                    title='Export script trace')
            if not path:return
            content=tracer.jsonl() if format=='jsonl' else json.dumps(tracer.document(),indent=2,allow_nan=False)+'\n'
            Path(path).write_text(content,encoding='utf-8')
            self.scripted_trace_status.set(f'Exported {len(tracer.events)} events ({format.upper()})')
        except (OSError,ValueError,RuntimeError) as exc:
            self.scripted_trace_status.set(f'Export failed: {exc}')
