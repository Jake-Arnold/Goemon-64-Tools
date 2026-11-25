"""Tk controls for an explicitly installed Project64 debugger script."""
import queue
import secrets
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from practice.pj64_frame_control import BUTTONS, controller_input, export_script, parse_inputs, request


class PJ64FrameUiMixin:
    def _build_pj64_frame_page(self, pages):
        page = ttk.Frame(pages, padding=10)
        pages.add(page, text='Frame control (PJ64)')
        ttk.Label(page, text='Experimental: controller polls are not game frames. Optional execution PC needs live validation.', wraplength=850).pack(anchor='w')
        self.frame_status = tk.StringVar(value='Export and run the companion script in Project64; then Refresh.')
        self.frame_port = tk.StringVar(value='47651')
        self.frame_token = tk.StringVar(value=secrets.token_hex(16))
        self.frame_pc = tk.StringVar()
        self.frame_region = tk.StringVar(value='usa')
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
        self.frame_timeline=tk.Text(page,height=6,width=65); self.frame_timeline.pack(fill='both',expand=True)
        if getattr(self.args,'read_only',False):
            for b in self.frame_controls:b.state(['disabled'])
            self.frame_status.set('Frame control disabled in read-only mode.')
        page.after(100,self._frame_drain)

    def _frame_export(self):
        if getattr(self.args,'read_only',False): return
        try:
            source=export_script(self.frame_region.get(),int(self.frame_port.get()),self.frame_token.get(),self.frame_pc.get())
            path=filedialog.asksaveasfilename(defaultextension='.js',initialfile='goemon_frame_bridge.js',filetypes=[('JavaScript','*.js')])
            if path: Path(path).write_text(source,encoding='utf-8'); self.frame_status.set('Run exported script from Project64 Debugger > Scripts; use Interpreter core.')
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
        try: port=int(self.frame_port.get()); token=self.frame_token.get(); region=self.frame_region.get(); pc=int(self.frame_pc.get().strip() or '0',16)
        except ValueError as exc:self.frame_status.set(str(exc));return
        self.frame_busy=True
        def work():
            try:
                # Verify the selected endpoint/region before sending any control command.
                s=request(port,token,'status')
                if s.get('region')!=region or s.get('pc')!=pc:raise ValueError('Script region or execution hook does not match this panel')
                if op!='status':s=request(port,token,op,**fields)
                self.frame_results.put((s,None))
            except (OSError,ValueError,TypeError,KeyError) as exc:self.frame_results.put((None,str(exc)))
        threading.Thread(target=work,daemon=True,name='PJ64FrameBridge').start()

    def _frame_drain(self):
        try:s,error=self.frame_results.get_nowait()
        except queue.Empty:pass
        else:
            self.frame_busy=False; self.frame_last=s
            if error:self.frame_status.set(error)
            else:
                state='Paused at boundary' if s.get('ready') else 'Pending' if s.get('pending') else 'Running / not synchronized'
                self.frame_status.set(f"{s['mode']} | {state} | step {s['count']} | P1 polls {s['polls']} | {s.get('error') or ('ROM header CRC matched' if s['valid'] else 'Wrong ROM')}")
        if self.frame_last and self.frame_last.get('pending') and not self.frame_busy:self._frame_request('status')
        self.root.after(150,self._frame_drain)
