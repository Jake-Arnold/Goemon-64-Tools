"""Read-only, zero-persistence USA Project64 Object graphics snapshot interpreter."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from practice.model_object_probe import parse_snapshot_hex, interpret_usa_object_graphics


class ModelObjectProbeDialog:
    def __init__(self, parent):
        self.window=tk.Toplevel(parent)
        self.window.title('Original-USA Project64 object graphics trace (research only)')
        self.window.geometry('730x610')
        self.window.minsize(580,430)
        frame=ttk.Frame(self.window,padding=10)
        frame.pack(fill='both',expand=True)
        ttk.Label(frame,wraplength=690,text=(
            'Set a USA execution breakpoint at 0x80018CA0. Its a1 register is an '
            'Object*; in the Project64 memory viewer copy exactly 0x68 bytes '
            'starting at that address. Paste only the bytes (not row addresses). '
            'No game memory is written and the snapshot is never saved.')).pack(anchor='w')
        ttk.Label(frame,text='Object header bytes (104, big-endian):').pack(anchor='w',pady=(8,0))
        self.raw=tk.Text(frame,height=7,wrap='word')
        self.raw.pack(fill='x')
        ttk.Button(frame,text='Interpret source-backed object layout',command=self.decode).pack(anchor='w',pady=8)
        self.status=tk.StringVar(value='USA source-derived layout only. This is not a verified actor identity.')
        ttk.Label(frame,textvariable=self.status,wraplength=690).pack(anchor='w')
        self.result=tk.Text(frame,height=14,wrap='word',state='disabled')
        self.result.pack(fill='both',expand=True,pady=(8,0))

    def decode(self):
        try:
            data=parse_snapshot_hex(self.raw.get('1.0','end'))
            result=interpret_usa_object_graphics(data)
        except ValueError as exc:
            self.status.set('Invalid input: '+str(exc))
            return
        rows=[f'Object.graphics_1 (+0x2C): {result["graphics_1"]}',
              f'Object.graphics_2 (+0x30): {result["graphics_2"]}',
              'Object.overlay_info[6] (+0x34; 8 bytes each):']
        for o in result['overlays']:
            flag='ROM-table-range' if o['plausible_rom_file_id'] else 'unverified/outside known file-ID range'
            rows.append(f'  [{o["index"]}] file={o["file_id_hex"]}, VRAM={o["vram_addr"]}, '
                        f'unknown_2={o["unknown_2"]}; {flag}')
        rows.append('Not a confirmed actor→model map. Verify this object against the paused rendering call and RT64 draw calls.')
        self.result.configure(state='normal')
        self.result.delete('1.0','end')
        self.result.insert('1.0','\n'.join(rows))
        self.result.configure(state='disabled')
        self.status.set('104 bytes interpreted read-only; no snapshot persisted. Correlate the original a1 register and drawing call manually.')
