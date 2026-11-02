"""Tk interface for read-only, user-labelled A/B/C N64 state probes."""
from __future__ import annotations

from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from practice.paths import diagnostics_dir
from practice.state_discovery import PROBE_ACTIONS, capture_state, compare_captures
from practice.theme import PALETTE


class StateDiscoveryMixin:
    def build_state_discovery_tab(self, notebook):
        tab=ttk.Frame(notebook,padding=10)
        notebook.add(tab,text='State discovery')
        self.state_discovery_tab=tab
        self.state_captures={}
        self.state_report=None
        ttk.Label(tab,text='Discover original N64 memory fields',font=('Segoe UI Semibold',16),
                  foreground=PALETTE['gold']).pack(anchor='w',pady=(2,6))
        ttk.Label(tab,text='Capture A (before), B (after) and optionally C (returned to the original state). '
                  'Only observed values are reported: no addresses are assumed to represent the requested flag.',
                  style='Muted.TLabel',wraplength=1080).pack(anchor='w',pady=(0,9))
        row=ttk.Frame(tab);row.pack(fill='x',pady=(0,6))
        ttk.Label(row,text='Test:').pack(side='left',padx=(0,6))
        self.state_probe_kind=tk.StringVar(value='Map displayed')
        selector=ttk.Combobox(row,textvariable=self.state_probe_kind,values=list(PROBE_ACTIONS),
                              width=26,state='readonly')
        selector.pack(side='left')
        ttk.Label(row,text='Memory range:').pack(side='left',padx=(18,5))
        self.state_probe_scope=tk.StringVar(value='focused')
        ttk.Combobox(row,textvariable=self.state_probe_scope,values=('focused','wide'),
                     width=10,state='readonly').pack(side='left')
        self.state_probe_instruction=tk.StringVar(value=PROBE_ACTIONS[self.state_probe_kind.get()])
        selector.bind('<<ComboboxSelected>>',lambda _e:self.state_probe_instruction.set(PROBE_ACTIONS[self.state_probe_kind.get()]))
        ttk.Label(tab,textvariable=self.state_probe_instruction,style='Muted.TLabel',
                  wraplength=1100).pack(anchor='w',pady=(0,6))
        ttk.Label(tab,text='Focused: nearby game globals + player task/object. Wide: original 4 MiB N64 RAM; '
                  'takes longer and captures some unrelated changing bytes. Use the same range for A/B/C.',
                  style='Muted.TLabel',wraplength=1080).pack(anchor='w',pady=(0,8))
        row=ttk.Frame(tab);row.pack(fill='x',pady=(0,9))
        for stage,caption in (('A','Capture A: Before'),('B','Capture B: After'),('C','Capture C: Reverted')):
            ttk.Button(row,text=caption,command=lambda s=stage:self.capture_state_probe(s)).pack(side='left',padx=(0,7))
        ttk.Button(row,text='Compare',style='Gold.TButton',command=self.compare_state_probes).pack(side='left',padx=8)
        ttk.Button(row,text='Export comparison JSON',command=self.export_state_probe).pack(side='left',padx=(0,7))
        ttk.Button(row,text='Clear',command=self.reset_state_probes).pack(side='left')
        self.state_probe_status=tk.StringVar(value='No captures. Select a test and connect to the game.')
        ttk.Label(tab,textvariable=self.state_probe_status,wraplength=1060).pack(anchor='w',pady=(0,10))
        headings=('address','region','before','after','bitmask','returned','kind')
        frame=ttk.Frame(tab);frame.pack(fill='both',expand=True)
        self.state_probe_table=ttk.Treeview(frame,columns=headings,show='headings',height=15)
        for key,heading,width in (
                ('address','Guest address',150),('region','Region',135),
                ('before','A: before',95),('after','B: after',95),
                ('bitmask','XOR mask',85),('returned','C matched A?',125),
                ('kind','Potential type',150)):
            self.state_probe_table.heading(key,text=heading)
            self.state_probe_table.column(key,width=width,stretch=key=='region')
        bar=ttk.Scrollbar(frame,orient='vertical',command=self.state_probe_table.yview)
        self.state_probe_table.configure(yscrollcommand=bar.set)
        self.state_probe_table.pack(side='left',fill='both',expand=True)
        bar.pack(side='right',fill='y')
        row=ttk.Frame(tab);row.pack(fill='x',pady=7)
        ttk.Button(row,text='Copy selected address',command=self.copy_state_probe_address).pack(side='left')
        ttk.Button(row,text='Watch selected address',command=self.watch_state_probe_candidate,
                   style='Gold.TButton').pack(side='left',padx=(8,0))
        ttk.Label(row,text='A/B changes alone are hypotheses. For persistent storyline flags, A/B is sufficient. '
                  'Player-task float values are not proven velocity.',style='Muted.TLabel',
                  wraplength=850).pack(side='left',padx=(15,0))

    def capture_state_probe(self,stage):
        if not self.mem:
            self.state_probe_status.set('Connect to Goemon64Recomp before capturing memory.')
            return
        try:
            scope=self.state_probe_scope.get()
            label=self.state_probe_kind.get()+' '+stage
            capture=capture_state(self.mem,label,scope=scope,
                                  snapshot=self.current if isinstance(self.current,dict) else None)
            self.state_captures[stage]=capture
            self.state_report=None
            regions=', '.join(r.name for r in capture.regions)
            self.state_probe_status.set(f'{stage} captured for character {capture.character}, '
                                        f'map {capture.map_id}; {regions}. '
                                        f'A/B/C captured: {", ".join(sorted(self.state_captures))}')
        except (OSError,ValueError,RuntimeError) as exc:
            self.state_probe_status.set(f'{stage} capture failed: {exc}')

    def compare_state_probes(self):
        if 'A' not in self.state_captures or 'B' not in self.state_captures:
            self.state_probe_status.set('Capture A and B first.')
            return
        try:
            report=compare_captures(self.state_captures['A'],self.state_captures['B'],
                                    self.state_captures.get('C'))
            self.state_report=report
            self.state_probe_table.delete(*self.state_probe_table.get_children())
            for i,row in enumerate(report['candidates']):
                self.state_probe_table.insert('','end',iid=str(i),values=(
                    row['address'],row['region'],row['before'],row['after'],
                    row['xor_mask'],'yes' if row['reverted'] else '—',row['kind']))
            counts=report['counts']
            event_count=len(report.get('event_flag_changes',[]))
            self.state_probe_status.set(f"Compared {counts['regions_compared']} regions; "
                f"{counts['observed_changes']} byte changes; "
                f"{counts['candidate_count']} candidates (showing {counts['reported_candidates']}); "
                f"{event_count} changed saved event-flag bytes. "
                'No candidate has been validated as an actual game flag.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.state_probe_status.set(f'Comparison failed: {exc}')

    def export_state_probe(self):
        if not self.state_report:
            self.state_probe_status.set('Compare A and B before exporting.')
            return
        try:
            path=diagnostics_dir()/('state_probe_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
            path.write_text(json.dumps(self.state_report,indent=2)+'\n',encoding='utf-8')
            self.state_probe_status.set(f'Exported comparison to {path}')
        except OSError as exc:
            self.state_probe_status.set(f'Export failed: {exc}')

    def copy_state_probe_address(self):
        chosen=self.state_probe_table.selection()
        if not chosen:
            self.state_probe_status.set('Select a candidate row first.')
            return
        addr=self.state_probe_table.item(chosen[0],'values')[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(addr)
        self.state_probe_status.set(f'Copied candidate address {addr}; not confirmed or enabled for editing.')

    def watch_state_probe_candidate(self):
        chosen=self.state_probe_table.selection()
        if not chosen:
            self.state_probe_status.set('Select a candidate before adding it to Live Memory.')
            return
        row=self.state_probe_table.item(chosen[0],'values')
        address=row[0]
        kind='f32' if row[6]=='f32 candidate' else 'u8'
        self.user_watch_name.set(f'{self.state_probe_kind.get()} {address}')
        self.user_watch_address.set(address)
        self.user_watch_type.set(kind)
        self.add_custom_watch()
        self.notebook.select(self.live_memory_tab)

    def reset_state_probes(self):
        self.state_captures={}
        self.state_report=None
        self.state_probe_table.delete(*self.state_probe_table.get_children())
        self.state_probe_status.set('Captures cleared; no game memory was written.')
