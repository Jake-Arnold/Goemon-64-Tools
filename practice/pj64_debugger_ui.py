"""PJ64-like guest-RAM debugger panel integrated with the toolkit's Tk UI.

No emulator PC/register API exists in the uninstrumented native recomp.
The CPU panel says so explicitly instead of inventing breakpoints or steps.
"""
from __future__ import annotations

import json
import queue
import re
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from practice.pj64_debugger import (DebuggerSession, disassembly, guest_address,
                                    hex_bytes, memory_rows, search_guest)
from practice.theme import PALETTE


class PJ64DebuggerMixin:
    def build_pj64_debugger_tab(self, notebook):
        self.debug_session = DebuggerSession()
        self.debug_last_refresh = 0.0
        self.debug_search_busy = False
        self.debug_search_queue = queue.SimpleQueue()
        self.debug_selected_read = None
        tab = ttk.Frame(notebook, padding=8)
        notebook.add(tab, text='Debugger')
        self.pj64_debugger_tab = tab
        self.debug_status = tk.StringVar(value='Connect to a game for RDRAM inspection. CPU execution hooks unavailable.')
        ttk.Label(tab, textvariable=self.debug_status, style='Muted.TLabel').pack(anchor='w', pady=(0, 5))
        pages = ttk.Notebook(tab)
        pages.pack(fill='both', expand=True)
        self.debug_pages = pages
        self._build_debug_memory_page(pages)
        self._build_debug_disasm_page(pages)
        self._build_debug_watch_page(pages)
        self._build_debug_cpu_page(pages)

    def _build_debug_memory_page(self, pages):
        page = ttk.Frame(pages, padding=6)
        pages.add(page, text='Memory viewer')
        row = ttk.Frame(page); row.pack(fill='x', pady=3)
        ttk.Label(row, text='Guest address (hex)').pack(side='left')
        self.debug_memory_addr = tk.StringVar(value='0x80000000')
        ttk.Entry(row, textvariable=self.debug_memory_addr, width=16).pack(side='left', padx=5)
        ttk.Button(row, text='Go / Refresh', command=self.debug_refresh_memory).pack(side='left', padx=3)
        self.debug_auto = tk.BooleanVar(value=True)
        ttk.Checkbutton(row, text='Auto refresh (500 ms)', variable=self.debug_auto).pack(side='left', padx=8)
        frame = ttk.Frame(page);frame.pack(fill='both', expand=True, pady=3)
        self.debug_memory_tree=ttk.Treeview(frame, columns=('bytes','ascii'),show='tree headings',height=13)
        for key, caption, width in (('#0','N64 address',130),('bytes','Big-endian guest bytes',540),('ascii','ASCII',190)):
            self.debug_memory_tree.heading(key,text=caption)
            self.debug_memory_tree.column(key,width=width,stretch=key=='bytes')
        self.debug_memory_tree.pack(side='left',fill='both',expand=True)
        scroll=ttk.Scrollbar(frame,orient='vertical',command=self.debug_memory_tree.yview)
        scroll.pack(side='right',fill='y');self.debug_memory_tree.configure(yscrollcommand=scroll.set)
        self.debug_memory_tree.bind('<<TreeviewSelect>>',self._debug_memory_selected)
        edit=ttk.LabelFrame(page,text='Guarded raw memory edit (not atomic against running game)',padding=6)
        edit.pack(fill='x',pady=5)
        r=ttk.Frame(edit);r.pack(fill='x')
        ttk.Label(r,text='Address').pack(side='left')
        self.debug_write_addr=tk.StringVar(value='0x8015C5E8')
        ttk.Entry(r,textvariable=self.debug_write_addr,width=14).pack(side='left',padx=4)
        ttk.Label(r,text='Width').pack(side='left')
        self.debug_write_width=tk.StringVar(value='4')
        ttk.Combobox(r,textvariable=self.debug_write_width,values=('1','2','4','8'),state='readonly',width=3).pack(side='left',padx=4)
        ttk.Button(r,text='Read original',command=self.debug_read_target).pack(side='left',padx=4)
        ttk.Label(r,text='Read').pack(side='left')
        self.debug_original=tk.StringVar(value='—')
        ttk.Label(r,textvariable=self.debug_original,font=('Consolas',10)).pack(side='left',padx=4)
        ttk.Label(r,text='New hex').pack(side='left')
        self.debug_new_bytes=tk.StringVar()
        ttk.Entry(r,textvariable=self.debug_new_bytes,width=19).pack(side='left',padx=4)
        self.debug_write_button=ttk.Button(r,text='Write and verify',command=self.debug_write_target)
        self.debug_write_button.pack(side='left',padx=4)
        if not self.args.enable_hex_edit:self.debug_write_button.state(['disabled'])
        ttk.Label(edit,text='Read original before writing. Writes compare current RAM against the read value; transitions may still race. '
                       'Never use this as a scene warp or CPU patch.',style='Muted.TLabel').pack(anchor='w',pady=(5,0))
        search=ttk.LabelFrame(page,text='Find exact guest-RAM bytes',padding=6)
        search.pack(fill='x')
        r=ttk.Frame(search);r.pack(fill='x')
        self.debug_search_text=tk.StringVar(value='00 00 00 0D')
        ttk.Entry(r,textvariable=self.debug_search_text,width=26).pack(side='left')
        self.debug_search_mode=tk.StringVar(value='Hex')
        ttk.Combobox(r,textvariable=self.debug_search_mode,values=('Hex','ASCII'),state='readonly',width=6).pack(side='left',padx=5)
        ttk.Label(r,text='From').pack(side='left')
        self.debug_search_start=tk.StringVar(value='0x80000000')
        ttk.Entry(r,textvariable=self.debug_search_start,width=14).pack(side='left',padx=4)
        ttk.Label(r,text='Bytes (hex)').pack(side='left')
        self.debug_search_length=tk.StringVar(value='0x400000')
        ttk.Entry(r,textvariable=self.debug_search_length,width=12).pack(side='left',padx=4)
        self.debug_search_button=ttk.Button(r,text='Find',command=self.debug_start_search)
        self.debug_search_button.pack(side='left',padx=3)
        self.debug_hits=tk.Listbox(search,height=3,exportselection=False,font=('Consolas',10),
                                    background=PALETTE['surface'],foreground=PALETTE['foreground'],
                                    selectbackground=PALETTE['red'])
        self.debug_hits.pack(fill='x',pady=(4,0))
        self.debug_hits.bind('<Double-1>',self._debug_hit_selected)

    def _build_debug_disasm_page(self,pages):
        page=ttk.Frame(pages,padding=6); pages.add(page,text='MIPS disassembly')
        bar=ttk.Frame(page);bar.pack(fill='x',pady=4)
        ttk.Label(bar,text='Code address').pack(side='left')
        self.debug_code_addr=tk.StringVar(value='0x80010000')
        ttk.Entry(bar,textvariable=self.debug_code_addr,width=16).pack(side='left',padx=5)
        ttk.Button(bar,text='Disassemble 64 words',command=self.debug_refresh_disasm).pack(side='left',padx=5)
        ttk.Label(page,text='Decodes the original MIPS words stored in guest RDRAM, NOT the native host instruction stream. '
                       'Unknown encodings remain .word.',style='Muted.TLabel').pack(anchor='w',pady=5)
        frame=ttk.Frame(page);frame.pack(fill='both',expand=True)
        tree=ttk.Treeview(frame,columns=('opcode','mnemonic'),show='tree headings')
        self.debug_disasm_tree=tree
        for key,caption,width in (('#0','N64 address',145),('opcode','Word',120),('mnemonic','MIPS III (static)',580)):
            tree.heading(key,text=caption);tree.column(key,width=width,stretch=key=='mnemonic')
        tree.pack(side='left',fill='both',expand=True)
        sb=ttk.Scrollbar(frame,orient='vertical',command=tree.yview)
        sb.pack(side='right',fill='y');tree.configure(yscrollcommand=sb.set)
        tree.bind('<Double-1>',self._debug_disasm_selected)

    def _build_debug_watch_page(self,pages):
        page=ttk.Frame(pages,padding=6);pages.add(page,text='Change watches / trace')
        row=ttk.Frame(page);row.pack(fill='x',pady=4)
        ttk.Label(row,text='Guest address').pack(side='left')
        self.debug_watch_addr=tk.StringVar(value='0x801C77E0')
        ttk.Entry(row,textvariable=self.debug_watch_addr,width=16).pack(side='left',padx=5)
        ttk.Label(row,text='Width').pack(side='left')
        self.debug_watch_width=tk.StringVar(value='4')
        ttk.Combobox(row,textvariable=self.debug_watch_width,values=('1','2','4','8'),state='readonly',width=3).pack(side='left',padx=4)
        ttk.Button(row,text='Watch',command=self.debug_add_watch).pack(side='left',padx=4)
        ttk.Button(row,text='Remove selected',command=self.debug_remove_watch).pack(side='left',padx=4)
        ttk.Button(row,text='Sample now',command=self.debug_poll_watches).pack(side='left',padx=4)
        ttk.Button(row,text='Export events JSON',command=self.debug_export_events).pack(side='left',padx=4)
        ttk.Label(page,text='Polling detects value changes (up to 64 addresses, 500 most recent events). '
                       'It cannot identify the writing MIPS instruction or stop execution. '
                       'Events and watches reset on reconnect.',style='Muted.TLabel').pack(anchor='w',pady=5)
        self.debug_watch_tree=ttk.Treeview(page,columns=('width','last'),show='tree headings',height=7)
        for key,title,width in (('#0','Guest address',190),('width','Bytes',70),('last','Last observed hex',270)):
            self.debug_watch_tree.heading(key,text=title);self.debug_watch_tree.column(key,width=width,stretch=key=='last')
        self.debug_watch_tree.pack(fill='x',pady=4)
        text_frame=ttk.Frame(page);text_frame.pack(fill='both',expand=True,pady=4)
        self.debug_events=tk.Text(text_frame,wrap='none',height=10,font=('Consolas',10),state='disabled',
                                  background=PALETTE['surface'],foreground=PALETTE['foreground'])
        self.debug_events.pack(side='left',fill='both',expand=True)
        sb=ttk.Scrollbar(text_frame,orient='vertical',command=self.debug_events.yview)
        sb.pack(side='right',fill='y');self.debug_events.configure(yscrollcommand=sb.set)

    def _build_debug_cpu_page(self,pages):
        page=ttk.Frame(pages,padding=14);pages.add(page,text='CPU / breakpoints')
        ttk.Label(page,text='NATIVE RECOMP — CPU EXECUTION NOT INSTRUMENTED',
                  font=('Consolas',13,'bold')).pack(anchor='w',pady=(5,13))
        for text in (
            'Program counter / current guest instruction: UNAVAILABLE',
            'MIPS GPR / FPR / HI / LO / COP0 registers: UNAVAILABLE',
            'Execution breakpoints, read/write hardware traps: UNAVAILABLE',
            'Single MIPS instruction step / step over / step out: UNAVAILABLE',
            'Instruction-by-instruction execution trace: UNAVAILABLE',
        ):
            ttk.Label(page,text=text,font=('Consolas',10)).pack(anchor='w',pady=6)
        ttk.Label(page,text='The native recomp translates MIPS code into host instructions. Its process RAM '
                       'does not contain a reconstructible live MIPS PC or register file. Genuine execution '
                       'debugging requires an instrumented recomp build exposing guest register snapshots, '
                       'per-instruction checkpoints, pause/continue/step and breakpoint hit notifications. '
                       'This tab deliberately does not provide fake controls.',wraplength=880).pack(anchor='w',pady=20)

    def reset_debugger_session(self):
        if not hasattr(self,'debug_session'):return
        self.debug_session.attach(None)
        self.debug_selected_read=None
        if hasattr(self,'debug_original'): self.debug_original.set('—')
        if hasattr(self,'debug_watch_tree'):self._debug_draw_watches()
        if hasattr(self,'debug_events'):self._debug_draw_events()
        self.debug_last_refresh=0.0

    def _debug_connected(self):
        ram=getattr(self,'mem',None)
        if ram is None:raise RuntimeError('Connect to a running game first')
        self.debug_session.attach(ram)
        return ram

    def _debug_error(self, exc):
        self.debug_status.set(f'Debugger: {exc}')

    def debug_refresh_memory(self):
        try:
            ram=self._debug_connected()
            address=guest_address(self.debug_memory_addr.get())
            rows=memory_rows(ram,address,16)
            selection=self.debug_memory_tree.selection()
            previous=selection[0] if selection else None
            tree=self.debug_memory_tree
            for child in tree.get_children():tree.delete(child)
            for addr,raw,asc in rows:
                tree.insert('', 'end', iid=f'{addr:08X}',text=f'{addr:08X}',values=(raw,asc))
            if previous and tree.exists(previous):tree.selection_set(previous)
            self.debug_status.set(f'Memory: {len(rows)*16} guest bytes from 0x{rows[0][0]:08X} (PID {self.game_pid})')
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)

    def _debug_memory_selected(self,_event=None):
        selected=self.debug_memory_tree.selection()
        if selected:self.debug_write_addr.set(f'0x{int(selected[0],16):08X}')

    def debug_read_target(self):
        try:
            ram=self._debug_connected()
            width=int(self.debug_write_width.get())
            if width not in (1,2,4,8):raise ValueError('Width must be 1/2/4/8')
            address=guest_address(self.debug_write_addr.get(),width)
            data=ram.read_guest(address,width)
            if len(data)!=width:raise OSError('Incomplete RAM read')
            self.debug_selected_read=(ram,address,data)
            self.debug_original.set(data.hex().upper())
            self.debug_new_bytes.set(data.hex().upper())
            self.debug_status.set(f'Read 0x{address:08X}; write requires unchanged original bytes')
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)

    def debug_write_target(self):
        try:
            ram=self._debug_connected()
            if not self.args.enable_hex_edit:raise PermissionError('Read-only mode')
            width=int(self.debug_write_width.get())
            address=guest_address(self.debug_write_addr.get(),width)
            before=self.debug_selected_read
            if before is None or before[0] is not ram or before[1]!=address or len(before[2])!=width:
                raise RuntimeError('Read this exact address and width before writing')
            new=hex_bytes(self.debug_new_bytes.get())
            if len(new)!=width:raise ValueError('Hex value does not match selected width')
            if not messagebox.askyesno('Write raw guest RAM',
                    f'Write 0x{address:08X}: {before[2].hex().upper()} → {new.hex().upper()}?\n'
                    'This can corrupt gameplay or crash the recomp.',parent=self.root):return
            changed=self.debug_session.write(address,before[2],new,writable=True)
            self.debug_selected_read=None
            self.debug_original.set('—')
            self.debug_status.set('Verified write' if changed else 'No change needed')
            self.debug_refresh_memory()
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:self._debug_error(exc)

    def debug_refresh_disasm(self):
        try:
            ram=self._debug_connected()
            address=guest_address(self.debug_code_addr.get(),4,alignment=4)
            rows=disassembly(ram,address,64)
            tree=self.debug_disasm_tree
            for child in tree.get_children():tree.delete(child)
            for addr,word,op in rows:tree.insert('', 'end', iid=f'{addr:08X}',text=f'{addr:08X}',values=(word,op))
            self.debug_status.set(f'Disassembled {len(rows)} original guest words at 0x{address:08X}; static only')
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)

    def _debug_disasm_selected(self,_event=None):
        selection=self.debug_disasm_tree.selection()
        if selection:
            self.debug_memory_addr.set('0x'+selection[0]);self.debug_pages.select(0)
            self.debug_refresh_memory()

    def debug_add_watch(self):
        try:
            ram=self._debug_connected()
            width=int(self.debug_watch_width.get())
            addr=guest_address(self.debug_watch_addr.get(),width)
            self.debug_session.add_watch(addr,width)
            self._debug_draw_watches()
            self.debug_status.set(f'Polling change watch 0x{addr:08X} ({width} bytes); not a CPU breakpoint')
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)

    def debug_remove_watch(self):
        selection=self.debug_watch_tree.selection()
        if selection:
            self.debug_session.remove_watch(int(selection[0],16));self._debug_draw_watches()

    def _debug_draw_watches(self):
        tree=self.debug_watch_tree
        for item in tree.get_children():tree.delete(item)
        for addr,data in self.debug_session.watches.items():
            tree.insert('', 'end', iid=f'{addr:08X}',text=f'{addr:08X}',
                        values=(len(data),data.hex().upper()))

    def debug_poll_watches(self):
        try:
            self._debug_connected()
            changed=self.debug_session.poll()
            if changed:self._debug_draw_watches();self._debug_draw_events()
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)

    def _debug_draw_events(self):
        text=self.debug_events
        text.configure(state='normal');text.delete('1.0','end')
        for event in self.debug_session.events[-100:]:
            text.insert('end',f'{event.timestamp}  0x{event.address:08X}  {event.before} -> {event.after}\n')
        text.configure(state='disabled');text.see('end')

    def debug_export_events(self):
        if not self.debug_session.events:
            self.debug_status.set('No change events to export');return
        path=filedialog.asksaveasfilename(parent=self.root,defaultextension='.json',
               filetypes=[('JSON','*.json')],title='Export debugger change events')
        if not path:return
        try:
            payload={'format':'goemon-pj64-memory-events-v1',
                     'note':'Polling change observations; no executing instruction/CPU registers',
                     'events':[e.export() for e in self.debug_session.events]}
            with open(path,'w',encoding='utf-8') as f:json.dump(payload,f,indent=2)
            self.debug_status.set(f'Exported {len(self.debug_session.events)} change events')
        except OSError as exc:self._debug_error(exc)

    def debug_start_search(self):
        if self.debug_search_busy:return
        try:
            ram=self._debug_connected()
            pattern=(hex_bytes(self.debug_search_text.get()) if self.debug_search_mode.get()=='Hex'
                     else self.debug_search_text.get().encode('ascii','strict'))
            if not pattern or len(pattern)>256:raise ValueError('Pattern size must be 1..256 bytes')
            start=guest_address(self.debug_search_start.get())
            n=self.debug_search_length.get().strip()
            if not re.fullmatch(r'(?:0[xX])?[0-9a-fA-F]{1,8}',n):raise ValueError('Enter hex byte length')
            length=int(n[2:] if n.lower().startswith('0x') else n,16)
            guest_address(start,length)
            self.debug_hits.delete(0,'end')
            self.debug_search_busy=True;self.debug_search_button.state(['disabled'])
            self.debug_status.set('Scanning guest RDRAM in a background read-only worker…')
            def work():
                try:self.debug_search_queue.put((ram,search_guest(ram,pattern,start,length,limit=256),None))
                except (OSError,ValueError,RuntimeError) as exc:self.debug_search_queue.put((ram,None,str(exc)))
            threading.Thread(target=work,daemon=True,name='GoemonDebuggerSearch').start()
            self.root.after(80,self._debug_poll_search)
        except (OSError,ValueError,RuntimeError,UnicodeEncodeError) as exc:self._debug_error(exc)

    def _debug_poll_search(self):
        try:ram,hits,error=self.debug_search_queue.get_nowait()
        except queue.Empty:
            self.root.after(80,self._debug_poll_search);return
        self.debug_search_busy=False;self.debug_search_button.state(['!disabled'])
        if ram is not self.mem:
            self.debug_status.set('Discarded scan results from disconnected session');return
        if error:self.debug_status.set(f'Search failed: {error}');return
        for addr in hits:self.debug_hits.insert('end',f'0x{addr:08X}')
        self.debug_status.set(f'Found {len(hits)} address(es)' + (' (limit 256)' if len(hits)==256 else ''))

    def _debug_hit_selected(self,_event=None):
        selected=self.debug_hits.curselection()
        if selected:
            self.debug_memory_addr.set(self.debug_hits.get(selected[0]));self.debug_refresh_memory()

    def poll_pj64_debugger(self, now: float):
        """Called from existing Tk tick: no CPU state guesses or background UI access."""
        if not hasattr(self,'debug_session'):return
        if self.debug_session.ram is not self.mem:
            self.debug_session.attach(self.mem)
            self.debug_selected_read=None
            self.debug_original.set('—')
            self._debug_draw_watches();self._debug_draw_events()
            self.debug_last_refresh=0.0
        if self.mem is None or now-self.debug_last_refresh < .5:return
        self.debug_last_refresh=now
        try:
            self.debug_poll_watches()
            if self.notebook.select()==str(self.pj64_debugger_tab):
                if self.debug_auto.get() and self.debug_pages.index('current')==0:self.debug_refresh_memory()
                # Avoid auto-disassembling: ROM code is static and expensive to render.
        except (OSError,ValueError,RuntimeError) as exc:self._debug_error(exc)
