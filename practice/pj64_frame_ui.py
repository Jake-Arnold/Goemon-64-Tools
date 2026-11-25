"""Tk controls for an explicitly installed Project64 debugger script."""
import queue
import json
import secrets
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path

from practice.pj64_frame_control import BUTTONS, controller_input, export_script, parse_inputs, request, trace_rows, export_trace, append_trace, parse_watches, parse_trap, TRACE_COLUMNS, TRACE_METADATA


class PJ64FrameUiMixin:
    def _build_pj64_frame_page(self, pages):
        page = ttk.Frame(pages, padding=10)
        pages.add(page, text='Frame Inspector (PJ64)')
        ttk.Label(page, text='Experimental: controller polls are not game frames. Optional execution PC needs live validation.', wraplength=850).pack(anchor='w')
        self.frame_status = tk.StringVar(value='Export and run the companion script in Project64; then Refresh.')
        self.frame_port = tk.StringVar(value='47651')
        self.frame_token = tk.StringVar(value=secrets.token_hex(16))
        self.frame_pc = tk.StringVar()
        self.frame_region = tk.StringVar(value='japan' if getattr(getattr(self,'active_version',None),'key',None)=='japan' else 'usa')
        self.frame_last = None
        self.frame_busy = False
        self.frame_results = queue.SimpleQueue()
        self.frame_buttons = {name: tk.BooleanVar(value=False) for name in BUTTONS}
        setup = ttk.Frame(page); setup.pack(fill='x', pady=5)
        ttk.Combobox(setup, textvariable=self.frame_region, values=('usa', 'japan'), state='readonly', width=8).pack(side='left')
        for title, variable, width in [('Port',self.frame_port,7), ('Session token',self.frame_token,34), ('Optional update PC',self.frame_pc,12)]:
            ttk.Label(setup,text=title).pack(side='left',padx=(8,2))
            ttk.Entry(setup,textvariable=variable,width=width).pack(side='left')
        self.frame_controls = []
        row = ttk.Frame(page); row.pack(fill='x',pady=5)
        for caption, callback in [('Export script', self._frame_export), ('Refresh', lambda:self._frame_request('status')), ('Pause at boundary', lambda:self._frame_request('pause')), ('Resume', lambda:self._frame_request('resume')), ('Cancel', lambda:self._frame_request('cancel'))]:
            b=ttk.Button(row,text=caption,command=callback); b.pack(side='left',padx=2); self.frame_controls.append(b)
        ttk.Label(page,textvariable=self.frame_status,wraplength=850).pack(anchor='w',pady=5)
        buttons=ttk.LabelFrame(page,text='Default input for each selected step'); buttons.pack(fill='x',pady=5)
        for i,(name,var) in enumerate(self.frame_buttons.items()):
            ttk.Checkbutton(buttons,text=name,variable=var).grid(row=i//7,column=i%7,sticky='w',padx=5)
        self.frame_x=tk.StringVar(value='0'); self.frame_y=tk.StringVar(value='0'); self.frame_n=tk.StringVar(value='1')
        row=ttk.Frame(page); row.pack(fill='x',pady=5)
        for label,var in [('Stick X',self.frame_x),('Stick Y',self.frame_y),('Steps',self.frame_n)]:
            ttk.Label(row,text=label).pack(side='left'); ttk.Entry(row,textvariable=var,width=5).pack(side='left',padx=4)
        for n in (1,5,60):
            b=ttk.Button(row,text=f'Step +{n}',command=lambda n=n:self._frame_step(n)); b.pack(side='left',padx=2); self.frame_controls.append(b)
        b=ttk.Button(row,text='Run timeline',command=self._frame_step); b.pack(side='left',padx=2); self.frame_controls.append(b)
        ttk.Label(page,text='Optional timeline: relative step, buttons (+), X, Y. Example: 1 A 0 0; next line: 2 - 0 0.').pack(anchor='w')
        self.frame_timeline=tk.Text(page,height=4,width=65); self.frame_timeline.pack(fill='x')
        ttk.Label(page,text='Watches (one per line): name u8/u16/u32/f32 hex_address or @catalogue_id. Re-export script after editing.').pack(anchor='w')
        self.frame_watches=tk.Text(page,height=3,width=65); self.frame_watches.pack(fill='x')
        traprow=ttk.Frame(page); traprow.pack(fill='x')
        ttk.Label(traprow,text='Optional breakpoint (exec PC / write address)').pack(side='left')
        self.frame_trap=tk.StringVar(); ttk.Entry(traprow,textvariable=self.frame_trap,width=24).pack(side='left')
        row=ttk.Frame(page); row.pack(fill='x')
        ttk.Button(row,text='Export trace CSV/JSON',command=self._frame_save_trace).pack(side='left')
        ttk.Button(row,text='Compare saved JSON',command=self._frame_compare_trace).pack(side='left')
        self.frame_reference=None
        self.frame_comparison=tk.StringVar(value='Latest batch; comparison off')
        ttk.Label(page,textvariable=self.frame_comparison).pack(anchor='w')
        ttk.Button(row,text='Clear comparison',command=self._frame_clear_comparison).pack(side='left')
        self.frame_capture=None; self.frame_recording=False; self.frame_show_capture=True
        ttk.Button(row,text='Latest batch / recording',command=self._frame_switch_trace).pack(side='left')
        self.frame_record_button=ttk.Button(row,text='Record',command=self._frame_toggle_record)
        self.frame_record_button.pack(side='left'); self.frame_controls.append(self.frame_record_button)
        grid=ttk.Frame(page); grid.pack(fill='both',expand=True)
        grid.rowconfigure(0,weight=1); grid.columnconfigure(0,weight=1)
        self.frame_table=ttk.Treeview(grid,show='headings',height=8)
        self.frame_table.grid(row=0,column=0,sticky='nsew')
        scrollbar=ttk.Scrollbar(grid,orient='horizontal',command=self.frame_table.xview)
        scrollbar.grid(row=1,column=0,sticky='ew'); self.frame_table.configure(xscrollcommand=scrollbar.set)
        scrollbar=ttk.Scrollbar(grid,orient='vertical',command=self.frame_table.yview)
        scrollbar.grid(row=0,column=1,sticky='ns'); self.frame_table.configure(yscrollcommand=scrollbar.set)
        self.frame_table.tag_configure('changed',background='#a45a14',foreground='white')
        self.frame_table.tag_configure('different',background='#8b2635',foreground='white')
        if getattr(self.args,'read_only',False):
            for b in self.frame_controls:b.state(['disabled'])
            self.frame_status.set('Frame control disabled in read-only mode.')
        self.root.after(100,self._frame_drain)

    def _frame_export(self):
        if getattr(self.args,'read_only',False): return
        try:
            source=export_script(self.frame_region.get(),int(self.frame_port.get()),self.frame_token.get(),self.frame_pc.get(),self.frame_watches.get('1.0','end'),self.frame_trap.get())
            path=filedialog.asksaveasfilename(defaultextension='.js',initialfile='goemon_frame_bridge.js',filetypes=[('JavaScript','*.js')])
            if path:
                Path(path).write_text(source,encoding='utf-8')
                self._frame_stop_record(); self.frame_last=None
                self.frame_status.set('Run exported script from Project64 Debugger > Scripts; use Interpreter core.')
        except (OSError,ValueError,KeyError) as exc:self.frame_status.set(str(exc))

    def _frame_step(self,n=None):
        try:
            s=self.frame_last
            if not s or not s.get('ready'): raise ValueError('Refresh after pausing at a bridge boundary')
            default=controller_input([name for name,var in self.frame_buttons.items() if var.get()],int(self.frame_x.get()),int(self.frame_y.get()))
            inputs=parse_inputs(self.frame_timeline.get('1.0','end'),int(self.frame_n.get()) if n is None else n,default)
            self._frame_request('step',epoch=s['epoch'],count=s['count'],generation=s['generation'],inputs=inputs)
        except (ValueError,KeyError) as exc:self.frame_status.set(str(exc))

    def _frame_request(self,op,**fields):
        if self.frame_busy or getattr(self.args,'read_only',False):return
        try:
            port=int(self.frame_port.get()); token=self.frame_token.get(); region=self.frame_region.get(); pc=int(self.frame_pc.get().strip() or '0',16)
            watches=parse_watches(self.frame_watches.get('1.0','end'),region); trap=parse_trap(self.frame_trap.get(),pc)
        except (ValueError,KeyError) as exc:self.frame_status.set(str(exc));return
        if self.frame_recording and (op in ('resume','cancel','pause') or (port,token,region,pc,watches,trap)!=self.frame_record_endpoint):
            self._frame_stop_record()
        self.frame_busy=True
        def work():
            try:
                # Verify the selected endpoint/region before sending any control command.
                s=request(port,token,'status')
                if s.get('region')!=region or s.get('pc')!=pc or s.get('watches')!=watches or s.get('trap')!=trap:raise ValueError('Script region, hook, watches or breakpoint does not match this panel; re-export')
                if op!='status':s=request(port,token,op,**fields)
                self.frame_results.put((s,None))
            except (OSError,ValueError,TypeError,KeyError) as exc:self.frame_results.put((None,str(exc)))
        threading.Thread(target=work,daemon=True,name='PJ64FrameBridge').start()

    def _frame_stop_record(self):
        self.frame_recording=False; self.frame_record_button.configure(text='Record')

    def _frame_toggle_record(self):
        if getattr(self.args,'read_only',False):return
        if self.frame_recording:self._frame_stop_record();return
        if self.frame_busy or not self.frame_last or not self.frame_last.get('ready'):
            self.frame_status.set('Pause at a boundary before recording');return
        if self.frame_capture and not messagebox.askyesno('New recording','Replace the previous recording? Export it first if needed.'):
            return
        try:
            self.frame_record_endpoint=(int(self.frame_port.get()),self.frame_token.get(),self.frame_last['region'],self.frame_last['pc'],self.frame_last['watches'],self.frame_last['trap'])
        except (ValueError,KeyError) as exc:self.frame_status.set(str(exc));return
        self.frame_capture=None; self.frame_recording=True; self.frame_show_capture=True
        self.frame_record_epoch=self.frame_last['epoch']; self.frame_record_generation=self.frame_last['generation']
        self.frame_record_button.configure(text='Stop recording')

    def _frame_switch_trace(self):
        self.frame_show_capture=not self.frame_show_capture
        s=self._frame_display_trace()
        if s:self._frame_render_trace(s)

    def _frame_display_trace(self):
        return (self.frame_capture if self.frame_show_capture else None) or self.frame_last

    def _frame_save_trace(self):
        try:
            s=self._frame_display_trace()
            if not s or not s.get('trace') or self.frame_busy or self.frame_last and self.frame_last.get('pending'):
                raise ValueError('Complete a recorded step batch first')
            path=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json'),('CSV','*.csv')])
            if path: export_trace(path,s)
        except (OSError,ValueError,KeyError) as exc:self.frame_status.set(str(exc))

    def _frame_compare_trace(self):
        try:
            path=filedialog.askopenfilename(filetypes=[('Trace JSON','*.json')])
            if not path:return
            if Path(path).stat().st_size>1000000:raise ValueError('Trace exceeds size limit')
            ref=json.loads(Path(path).read_text(encoding='utf-8'))
            s=self._frame_display_trace()
            if not s or any(ref[k]!=s[k] for k in TRACE_METADATA):
                raise ValueError('Comparison requires identical region, hook and watches')
            trace_rows(ref)
            self.frame_reference=ref; self._frame_render_trace(s)
        except (OSError,ValueError,KeyError,TypeError,AttributeError,OverflowError) as exc:self.frame_status.set(str(exc))

    def _frame_clear_comparison(self):
        self.frame_reference=None
        s=self._frame_display_trace()
        if s:self._frame_render_trace(s)

    def _frame_render_trace(self,s):
        rows=trace_rows(s)
        ref=self.frame_reference
        if ref and any(ref.get(k)!=s.get(k) for k in TRACE_METADATA):ref=None
        other=trace_rows(ref) if ref else []
        columns=list(TRACE_COLUMNS)+[w['name'] for w in s.get('watches',[])]
        table=self.frame_table; table.delete(*table.get_children()); table['columns']=columns
        for name in columns:
            table.heading(name,text=name); table.column(name,width=85,stretch=True)
        first=None
        for i in range(max(len(rows),len(other))):
            row=rows[i] if i<len(rows) else {}
            previous=rows[i-1] if 0<i<len(rows) else row
            changed=any(row.get(k)!=previous.get(k) for k in columns[1:])
            different=bool(ref) and (i>=len(other) or i>=len(rows) or any(row.get(k)!=other[i].get(k) for k in columns[1:]))
            if different and first is None:first=i
            def cell(k):
                value=row.get(k)
                if ref and (i>=len(other) or i>=len(rows) or value!=other[i].get(k)):
                    return f'{value if value is not None else "—"} / {other[i].get(k) if i<len(other) else "—"}'
                if k=='buttons' and value is not None:return '+'.join(n for n,mask in BUTTONS.items() if value & mask) or '-'
                if k not in TRACE_COLUMNS and isinstance(value,int):return f'0x{value:X}'
                return '' if value is None else str(value)
            table.insert('', 'end',values=[cell(k) for k in columns],tags=('different',) if different else ('changed',) if changed else ())
        view='Recording' if self.frame_show_capture and self.frame_capture else 'Latest batch'
        compare=f'current / reference | first difference at relative row {first}' if first is not None else 'no differences' if ref else 'comparison off'
        self.frame_comparison.set(f'{view}: {len(rows)} samples | {compare}')

    def _frame_drain(self):
        try:s,error=self.frame_results.get_nowait()
        except queue.Empty:pass
        else:
            self.frame_busy=False; self.frame_last=s
            if error:self._frame_stop_record(); self.frame_status.set(error)
            else:
                record_error=''
                if self.frame_recording and s['generation']!=self.frame_record_generation and not s.get('pending'):
                    try:
                        if not s.get('trace') or s['epoch']!=self.frame_record_epoch or s.get('batchGeneration')!=s['generation'] or (not s.get('ready') and not (s.get('paused') and s.get('error'))):
                            raise ValueError('Recording interrupted; existing capture retained')
                        self.frame_capture=append_trace(self.frame_capture,s)
                        self.frame_record_generation=s['generation']
                        if s.get('error'):self._frame_stop_record()
                    except ValueError as exc:self._frame_stop_record();record_error=str(exc)
                self._frame_render_trace(self._frame_display_trace())
                state='Breakpoint' if s.get('hit') and s.get('paused') else 'Paused at boundary' if s.get('ready') else 'Pending' if s.get('pending') else 'Running / not synchronized'
                hit=s.get('hit')
                detail=f" | {hit['kind']} at PC 0x{hit['pc']:08X}, target 0x{hit['address']:08X}" if hit else ''
                self.frame_status.set(f"{s['mode']} | {state} | step {s['count']} | P1 polls {s['polls']} | {record_error or s.get('error') or ('ROM header CRC matched' if s['valid'] else 'Wrong ROM')}{detail}")
        if self.frame_last and self.frame_last.get('pending') and not self.frame_busy:self._frame_request('status')
        self.root.after(150,self._frame_drain)
