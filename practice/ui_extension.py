"""Live inspector, diagnostics and opt-in direct gameplay warp trial (v0.9.7)."""
from __future__ import annotations
import json
import queue
import threading
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from practice.inspector import get_watches, checkpoint_differences, Watch
from practice.hex_edit import get_policy, parse_hex, checked_write
from practice.scenes import SCENES, scene_label
from practice.scene_controls import open_native_debug_menu, open_native_debug_for_scene, native_debug_selection, request_scene_warp, assess_direct_warp
from practice.checkpoints import MAP_ADDR, STATE_ADDR
from practice.experimental_controls import stage_reload_trial
from practice.entrance_ui import EntranceMixin
from practice.scene_placement import SpawnPlacement
from practice.paths import practice_data_dir, diagnostics_dir
from practice.custom_watches import (CustomWatch, FORMATS, make_watch, append_watch,
                                     load_watches, save_watches, read_watch)
from practice.theme import PALETTE
from practice.native_character import press_native_debug_accept, ready_for_scene_spawn
from practice.native_debug_watch import FIELDS as NATIVE_WATCH_FIELDS, read_fields as read_native_watches, changed_fields as changed_native_watches, make_change_event as make_native_change_event, can_mark_state as can_mark_native_state, decode_hover_pointer
from practice.native_debug_trace import (Observation, Candidate, menu_state, take_menu_snapshot,
    find_candidates, load_profile, save_profile, calibrated_for_direct_warp,
    stage_menu_selection, candidate_report, display_candidate_indices)

from practice.native_character_cursor_scan import (
    ORDER as CHARACTER_CURSOR_ORDER, CHARACTERS as CHARACTER_CURSOR_NAMES,
    capture_cursor, find_cursor_candidates, make_cursor_report)

DEBUG_PROFILE_PATH = practice_data_dir() / "native_debug_fields.json"
CUSTOM_WATCHES_PATH = practice_data_dir() / "custom_watches.json"

class InspectorMixin(EntranceMixin):
    def build_inspector_tabs(self, notebook):
        self.init_entrances()
        self.watch_previous={}
        self.hex_advanced=tk.BooleanVar(value=bool(self.args.enable_hex_edit))
        self.watch_rows=[]
        self.custom_watch_load_error=None
        try:
            self.custom_watches=load_watches(CUSTOM_WATCHES_PATH)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            self.custom_watches=[]
            self.custom_watch_load_error=str(exc)
        self.scene_selected=None
        self.debug_observations=[]
        self.debug_candidates=[]
        self.native_watch_previous={}
        self.native_watch_current={}
        self.native_watch_events=[]
        self.native_watch_last_at=0.0
        self.debug_display_indices=[]
        self.cursor_captures=[]
        self.cursor_candidates=[]
        self.cursor_analysed=False
        self.cursor_busy=False
        self.cursor_job_results=queue.Queue()
        self.debug_profile=load_profile(DEBUG_PROFILE_PATH)
        self.pending_native_warp=None
        self.pending_direct_warp=None
        self.direct_warp_confirmed=False
        self.transition_trace=None
        self.native_key_release=None
        self.native_warp_confirmed=False
        self.warp_monitor=None
        self.warp_monitor_after=None
        self.debug_shortcut_confirmed=False
        self.diff_previous_key=None
        self.log_events=[]
        self.log_changes=tk.BooleanVar(value=False)
        self.last_inspect_at=0.0
        self.last_compare_at=0.0
        self.inspector_status=tk.StringVar(value='Connect to begin inspecting memory. Raw addresses refer to US N64 guest RAM.')
        self.scene_status=tk.StringVar(value='Direct warp disabled: v0.9.7 exits to title. Double-click does NOT write memory. Capture a normal transition to identify the loader.')
        self.compare_status=tk.StringVar(value='Capture or select a logical checkpoint to compare.')

        inspector=ttk.Frame(notebook,padding=10)
        notebook.add(inspector,text='Live memory')
        self.live_memory_tab=inspector
        ttk.Label(inspector,textvariable=self.inspector_status,wraplength=900).pack(fill='x',pady=3)
        top=ttk.Frame(inspector);top.pack(fill='x',pady=3)
        ttk.Checkbutton(top,text='Log changed values',variable=self.log_changes).pack(side='left')
        ttk.Button(top,text='Export diagnostic JSON',command=self.export_inspector).pack(side='left',padx=9)
        ttk.Label(top,text='Filter:').pack(side='left',padx=5)
        self.filter_text=tk.StringVar()
        ttk.Entry(top,textvariable=self.filter_text,width=25).pack(side='left')
        self.filter_text.trace_add('write',lambda *_:self.draw_watches())
        watch_tools=ttk.LabelFrame(inspector,text='Custom memory watches (saved across launches)',padding=6)
        watch_tools.pack(fill='x',pady=(2,6))
        custom_row=ttk.Frame(watch_tools);custom_row.pack(fill='x')
        ttk.Label(custom_row,text='Name:').pack(side='left')
        self.user_watch_name=tk.StringVar(value='Map write-trigger candidate')
        ttk.Entry(custom_row,textvariable=self.user_watch_name,width=29).pack(side='left',padx=(3,8))
        ttk.Label(custom_row,text='Address:').pack(side='left')
        self.user_watch_address=tk.StringVar(value='0x8015C574')
        ttk.Entry(custom_row,textvariable=self.user_watch_address,width=14).pack(side='left',padx=(3,8))
        ttk.Label(custom_row,text='Type:').pack(side='left')
        self.user_watch_type=tk.StringVar(value='u8')
        ttk.Combobox(custom_row,textvariable=self.user_watch_type,values=tuple(FORMATS),
                     state='readonly',width=7).pack(side='left',padx=(3,8))
        ttk.Button(custom_row,text='Add watch',command=self.add_custom_watch,
                   style='Gold.TButton').pack(side='left',padx=(0,6))
        ttk.Button(custom_row,text='Remove selected watch',command=self.remove_custom_watch).pack(side='left')
        ttk.Label(watch_tools,text='Custom values refresh with the live table. Select the custom row to remove it. '
                  'Double-click its Hex cell to edit when UNSAFE is enabled.',
                  style='Muted.TLabel').pack(anchor='w',pady=(4,0))
        if self.custom_watch_load_error:
            ttk.Label(watch_tools,text='Existing custom watch file could not be read: '+self.custom_watch_load_error,
                      style='Muted.TLabel').pack(anchor='w')
        ttk.Label(inspector,text='Double-click a HEX cell to edit. UNSAFE enables unrestricted hex values at the displayed guest address (including mapped bounds override).').pack(anchor='w')
        self.unsafe_check=ttk.Checkbutton(inspector,text='UNSAFE: enable raw guest-memory hex editing (any 1/2/4/8-byte value and address)',variable=self.hex_advanced)
        self.unsafe_check.pack(anchor='w')
        if not self.args.enable_hex_edit:self.unsafe_check.state(['disabled'])
        manual=ttk.Frame(inspector);manual.pack(fill='x',pady=(3,7))
        ttk.Label(manual,text='Raw address:').pack(side='left')
        self.raw_address=tk.StringVar(value='0x8015C717')
        ttk.Entry(manual,textvariable=self.raw_address,width=14).pack(side='left',padx=(3,10))
        ttk.Label(manual,text='Bytes:').pack(side='left')
        self.raw_width=tk.StringVar(value='1')
        ttk.Combobox(manual,textvariable=self.raw_width,values=('1','2','4','8'),state='readonly',width=3).pack(side='left',padx=(3,10))
        ttk.Label(manual,text='Hex:').pack(side='left')
        self.raw_value=tk.StringVar(value='01')
        ttk.Entry(manual,textvariable=self.raw_value,width=20).pack(side='left',padx=(3,10))
        self.raw_write_btn=ttk.Button(manual,text='Write raw hex',command=self.write_raw_hex)
        self.raw_write_btn.pack(side='left')
        if not self.args.enable_hex_edit:self.raw_write_btn.state(['disabled'])
        columns=('address','value','raw','status','source')
        frame=ttk.Frame(inspector);frame.pack(fill='both',expand=True)
        self.watch_tree=ttk.Treeview(frame,columns=columns,show='tree headings',height=22)
        self.watch_tree.heading('#0',text='Field');self.watch_tree.column('#0',width=195,stretch=True)
        for n,display,w in [('address','N64 address',120),('value','Decoded',340),('raw','Hex',85),('status','Status',75),('source','Source / confidence',235)]:
            self.watch_tree.heading(n,text=display);self.watch_tree.column(n,width=w,stretch=n in ('value','source'))
        self.watch_tree.tag_configure('changed',background='#254f49')
        self.watch_tree.tag_configure('invalid',background='#5d3030')
        scroll=ttk.Scrollbar(frame,orient='vertical',command=self.watch_tree.yview)
        self.watch_tree.configure(yscrollcommand=scroll.set)
        self.watch_tree.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
        self.watch_tree.bind('<Double-1>',self.edit_live_hex)
        ttk.Label(inspector,text='Recent raw-field changes (not definitive semantic proof). F1 opens this tab from anywhere in the toolkit.').pack(anchor='w')
        self.event_text=tk.Text(inspector,height=6,wrap='none',font=('Consolas',9),state='disabled',
                                background='#1a1d23', foreground='#f3eee5',
                                insertbackground='#edbf6b', selectbackground='#8c3030',
                                relief='flat', borderwidth=0)
        self.event_text.pack(fill='x')

        scenes=ttk.Frame(notebook,padding=10)
        notebook.add(scenes,text='Scene browser')
        self.scene_tab=scenes
        self.scene_live=tk.StringVar(value='Current map: —')
        ttk.Label(scenes,textvariable=self.scene_live,font=('Consolas',12)).pack(anchor='w',pady=4)
        ttk.Label(scenes,text='Double-click selects a stage without writing memory. Choose an entrance, then use an explicit scene request button.').pack(anchor='w')
        character_line=ttk.Frame(scenes);character_line.pack(fill='x',pady=4)
        ttk.Label(character_line,text='Target character:').pack(side='left')
        self.scene_character=ttk.Combobox(character_line,state='readonly',width=30,
               values=('0 - Goemon','1 - Ebisumaru','2 - Sasuke (inferred)','3 - Yae (inferred)'))
        self.scene_character.current(0)
        self.scene_character.pack(side='left',padx=8)
        ttk.Label(character_line,text='Experimental pre-load spawn ID, no C-Down. Native model selection unverified.').pack(side='left')
        self.build_entrance_controls(scenes)
        self.scene_filter=tk.StringVar()
        ttk.Entry(scenes,textvariable=self.scene_filter).pack(fill='x',pady=6)
        self.scene_filter.trace_add('write',lambda *_:self.draw_scene_list())
        scene_frame=ttk.Frame(scenes);scene_frame.pack(fill='both',expand=True)
        self.scene_list=tk.Listbox(scene_frame,font=('Consolas',10),exportselection=False,height=6,
                                   background='#1a1d23', foreground='#f3eee5',
                                   selectbackground='#8c3030',selectforeground='#fff',
                                   relief='flat',highlightthickness=0)
        self.scene_list.pack(side='left',fill='both',expand=True)
        sc=ttk.Scrollbar(scene_frame,orient='vertical',command=self.scene_list.yview)
        sc.pack(side='right',fill='y');self.scene_list.configure(yscrollcommand=sc.set)
        self.scene_list.bind('<<ListboxSelect>>',self.select_scene)
        self.scene_list.bind('<Double-Button-1>',self.activate_selected_scene)
        self.draw_scene_list()
        ttk.Label(scenes,text='Experimental 0x0C reload: stage the selected ROM entrance XYZ and facing before native loading, then place the loaded player after destination/character checks. Collision, camera and scene scripts still require live validation. The old exit-flag route remains disabled.',wraplength=950).pack(anchor='w',pady=3)
        self.experimental_warp_btn=ttk.Button(scenes,text='EXPERIMENT: reload at selected entrance',
            command=self.try_reload_warp,style='Gold.TButton')
        self.experimental_warp_btn.pack(fill='x',pady=4)
        if not self.args.enable_hex_edit:self.experimental_warp_btn.state(['disabled'])
        ttk.Label(scenes,textvariable=self.scene_status,wraplength=950).pack(anchor='w',pady=8)
        self.native_debug_btn=ttk.Button(scenes,text='Instead OPEN original debug menu (manual selection)',command=self.open_debug_for_selected_scene)
        self.native_debug_btn.pack(fill='x',pady=5)
        if not self.args.enable_debug_menu:self.native_debug_btn.state(['disabled'])
        ttk.Label(scenes,text='Warp destinations use the original debug-menu transition and the selected entrance coordinates.',wraplength=950).pack(anchor='w')

    def refresh_checkpoint_options(self):
        if not hasattr(self,'diff_cp'):return
        labels=self.checkpoint_labels()
        self.diff_cp['values']=labels
        if labels and self.diff_cp.current()<0:self.diff_cp.current(len(labels)-1)

    def add_custom_watch(self):
        try:
            spec=make_watch(self.user_watch_name.get(),self.user_watch_address.get(),
                            self.user_watch_type.get())
            updated=append_watch(self.custom_watches,spec)
            save_watches(CUSTOM_WATCHES_PATH,updated)
            self.custom_watches=updated
            self.inspector_status.set(f'Added {spec.row_name} at 0x{spec.address:08X} ({spec.kind}).')
            self.filter_text.set('')
            if self.mem:
                self.last_inspect_at=0.0
                self.refresh_inspector(self.current if isinstance(self.current,dict) else {})
            else:
                self.watch_rows=[*self.watch_rows, Watch(spec.row_name,spec.address,
                    'Connect to read','—','CUSTOM',f'user watch: {spec.kind}; meaning unverified')]
                self.draw_watches()
            if self.watch_tree.exists(spec.row_name):
                self.watch_tree.selection_set(spec.row_name)
                self.watch_tree.see(spec.row_name)
        except (ValueError,OSError,TypeError,KeyError) as exc:
            self.inspector_status.set(f'Add watch failed: {exc}')

    def remove_custom_watch(self):
        chosen=self.watch_tree.selection()
        names={spec.row_name for spec in self.custom_watches}
        selected=next((name for name in chosen if name in names),None)
        if selected is None:
            self.inspector_status.set('Select a Custom: row before removing it.')
            return
        updated=[spec for spec in self.custom_watches if spec.row_name!=selected]
        try:
            save_watches(CUSTOM_WATCHES_PATH,updated)
        except OSError as exc:
            self.inspector_status.set(f'Remove watch failed: {exc}')
            return
        self.custom_watches=updated
        self.watch_rows=[w for w in self.watch_rows if w.name != selected]
        self.watch_previous.pop(selected,None)
        if self.mem:
            self.last_inspect_at=0.0
            self.refresh_inspector(self.current if isinstance(self.current,dict) else {})
        else:
            self.draw_watches()
        self.inspector_status.set(f'Removed {selected}.')

    def write_raw_hex(self):
        """Write explicitly entered guest bytes; unlocked only by UNSAFE toggle."""
        if not self.mem:
            self.inspector_status.set('Connect to the game first.')
            return
        if not getattr(self.args,'enable_hex_edit',False) or not self.hex_advanced.get():
            self.inspector_status.set('Raw writes require --enable-hex-edit and the UNSAFE checkbox.')
            return
        try:
            addr=int(self.raw_address.get().strip(),16)
            width=int(self.raw_width.get())
            new=parse_hex(self.raw_value.get(),width)
            before=self.mem.read_guest(addr,width)
            changed=checked_write(self.mem,addr,before,new,allow_advanced=True,raw_override=True)
            self.append_event(f'RAW USER WRITE 0x{addr:08X}: 0x{before.hex().upper()} -> 0x{new.hex().upper()}')
            self.inspector_status.set(f'Raw write verified at 0x{addr:08X}: 0x{new.hex().upper()}'+('' if changed else ' (unchanged)'))
            self.last_inspect_at=0.0
        except (ValueError,OSError,RuntimeError,PermissionError) as exc:
            self.inspector_status.set(f'Raw write failed: {exc}')

    def edit_live_hex(self,event):
        """Launch a typed hex editor only for the clicked HEX column."""
        if self.watch_tree.identify_region(event.x,event.y)!='cell':return
        if self.watch_tree.identify_column(event.x)!='#3':return
        row_id=self.watch_tree.identify_row(event.y)
        if not row_id or not self.mem:return
        if not getattr(self.args,'enable_hex_edit',False):
            messagebox.showwarning('Hex editing off','Restart with --enable-hex-edit to opt in to memory writing.')
            return
        watch=next((w for w in self.watch_rows if w.name==row_id),None)
        if watch is None or watch.addr is None:return
        policy=get_policy(watch.addr)
        spec=next((v for v in self.custom_watches if v.row_name==watch.name),None)
        unsafe=self.hex_advanced.get()
        if spec is not None and not unsafe:
            messagebox.showwarning('Custom watch is read-only',
                'Enable UNSAFE to edit a custom guest-RAM watch.')
            return
        if policy is None and not unsafe:
            messagebox.showwarning('Read-only field','Enable UNSAFE to edit a field without a declared policy.')
            return
        if policy is not None and policy.advanced and not unsafe:
            messagebox.showwarning('Engine-state field locked','Enable UNSAFE to edit this field.')
            return
        try:
            # Unknown floats and other raw watches provide their byte width
            # through the displayed hex data, rather than a guessed policy.
            raw_text=watch.raw.removeprefix('0x').removeprefix('0X').strip()
            if spec is not None:
                width=spec.width
            elif policy is not None:
                width=policy.width
            elif len(raw_text) in (2,4,8,16) and all(c in '0123456789abcdefABCDEF' for c in raw_text):
                width=len(raw_text)//2
            else:
                raise ValueError('No valid raw width for this watch; use the raw address editor')
            original=self.mem.read_guest(watch.addr,width)
            original_hex='0x'+original.hex().upper()
            new_string=simpledialog.askstring('Edit N64 guest hex — '+watch.name,
                f'{watch.name}\n0x{watch.addr:08X} ({width} bytes; N64 big-endian)\n'
                +('UNSAFE: any raw value of this width is accepted\n' if unsafe else policy.note+'\n')
                +'\nNew hex value:',initialvalue=original_hex,parent=self.root)
            if new_string is None:return
            proposed=parse_hex(new_string,width)
            if proposed==original:return
            if not unsafe:
                value=int.from_bytes(proposed,'big')
                if policy.max_value is not None and value>policy.max_value:
                    raise ValueError(f'Value {value} exceeds maximum {policy.max_value}')
                approved=messagebox.askyesno('Confirm N64 RAM write',
                    f'{watch.name}\nBefore: {original_hex}\nAfter: 0x{proposed.hex().upper()}',
                    parent=self.root,icon='warning')
                if not approved:return
            did_write=checked_write(self.mem,watch.addr,original,proposed,
                     allow_advanced=unsafe,raw_override=unsafe)
            if did_write:
                stamp=datetime.now().strftime('%H:%M:%S')
                self.append_event(f'{stamp} USER WRITE {watch.name}: {original_hex} -> 0x{proposed.hex().upper()}')
                self.last_inspect_at=0.0
                self.refresh_inspector({} if self.mem.u8(0x800C7A94)==10 else (self.current or {}))
                self.inspector_status.set(f'Verified write: {watch.name} {original_hex} -> 0x{proposed.hex().upper()}')
        except (ValueError,OSError,RuntimeError,PermissionError) as exc:
            messagebox.showerror('Hex write blocked / failed',str(exc),parent=self.root)

    def draw_watches(self):
        filt=self.filter_text.get().lower().strip()
        chosen=self.watch_tree.selection()
        self.watch_tree.delete(*self.watch_tree.get_children())
        for w in self.watch_rows:
            if filt and filt not in (' '.join((w.name,w.value,w.raw,w.source,
                                   f'0x{w.addr:08X}' if w.addr is not None else ''))).lower():
                continue
            mark=(w.name,w.raw)
            tag = 'invalid' if w.status in ('CHECK','ERROR') else ('changed' if w.name in self.watch_previous and self.watch_previous[w.name]!=w.raw else '')
            self.watch_tree.insert('', 'end',iid=w.name,text=w.name,
                    values=(f'0x{w.addr:08X}' if w.addr is not None else '—',w.value,w.raw,w.status,w.source),tags=(tag,))
        for iid in chosen:
            if self.watch_tree.exists(iid):self.watch_tree.selection_add(iid)

    def append_event(self,line):
        self.log_events.append(line)
        self.log_events=self.log_events[-100:]
        self.event_text.configure(state='normal')
        self.event_text.delete('1.0','end')
        self.event_text.insert('end','\n'.join(self.log_events[-35:]))
        self.event_text.see('end');self.event_text.configure(state='disabled')

    def refresh_inspector(self, snapshot):
        if not self.mem:return
        import time
        now=time.monotonic()
        if now-self.last_inspect_at < 0.30:return
        self.last_inspect_at=now
        try:
            live_map=self.mem.u16(MAP_ADDR)
            self.scene_live.set('Current map: '+scene_label(live_map))
            watches=get_watches(self.mem,snapshot,SCENES)
            watches.extend(read_watch(self.mem,spec) for spec in self.custom_watches)
            observed=getattr(self, 'observed_velocity', None)
            if observed is not None:
                import math
                for name,value in zip(('Observed velocity X','Observed velocity Y','Observed velocity Z'),observed):
                    watches.append(Watch(name,None,f'{value:.3f} units/s','—','DERIVED',
                                         'Measured XYZ / elapsed real seconds; not an internal N64 velocity field'))
                speed=math.sqrt(sum(v*v for v in observed))
                watches.append(Watch('Observed velocity magnitude',None,f'{speed:.3f} units/s','—','DERIVED',
                                     'Position-difference estimate; not engine momentum or per-frame speed'))
            old=self.watch_previous
            modified=[]
            for w in watches:
                if w.name in old and old[w.name]!=w.raw:
                    modified.append((w.name,old[w.name],w.raw))
            self.watch_rows=watches
            self.draw_watches()
            self.refresh_quick_watch()
            self.watch_previous={w.name:w.raw for w in watches}
            invalid=[w.name for w in watches if w.status in ('CHECK','ERROR')]
            self.inspector_status.set(f'Map {live_map} ({SCENES.get(live_map,"unmapped")})  |  {len(watches)} fields  |  {len(invalid)} need verification  |  {len(modified)} changed this poll')
            if self.log_changes and modified:
                stamp=datetime.now().strftime('%H:%M:%S')
                for name,before,after in modified[:12]:self.append_event(f'{stamp}  {name}: {before} -> {after}')
                if len(modified)>12:self.append_event(f'{stamp}  ... +{len(modified)-12} changes')
        except (OSError,ValueError) as e:
            self.inspector_status.set(f'Inspector failed: {e}')

    def refresh_checkpoint_diff(self,force=False):
        if not hasattr(self,'diff_tree'):return
        import time
        now=time.monotonic()
        if not force and now-self.last_compare_at<1.5:return
        self.last_compare_at=now
        if not self.mem or not self.checkpoints:return
        idx=self.diff_cp.current()
        if idx<0 or idx>=len(self.checkpoints):return
        try:
            d=checkpoint_differences(self.mem,self.checkpoints[idx])
            self.compare_status.set(
                f'Map: {d["map_live"]} / saved {d["map_saved"]} ({"MATCH" if d["map_matches"] else "DIFFERENT"}); '
                f'character: {d["character_live"]} / saved {d["character_saved"]} '
                f'({"MATCH" if d["character_matches"] else "DIFFERENT"}). '
                f'Changed bytes: live={d["counts"]["live"]}, progression={d["counts"]["gamedata"]}, '
                f'header={d["counts"]["header"]}; total={d["total"]} (showing {len(d["rows"])}).')
            self.diff_tree.delete(*self.diff_tree.get_children())
            for i,(region,n64,off,old,new) in enumerate(d['rows']):
                self.diff_tree.insert('','end',iid=str(i),text=region,values=(n64,off,old,new))
        except (OSError,ValueError,TypeError) as e:
            self.compare_status.set(f'Comparison failed: {e}')

    def draw_scene_list(self):
        filt=self.scene_filter.get().lower().strip()
        self.scene_options=[(k,v) for k,v in sorted(self.scene_catalog().items()) if filt in f'{k} {k:03X} {v}'.lower()]
        self.scene_list.delete(0,'end')
        for k,v in self.scene_options:self.scene_list.insert('end',f'{k:03d} [0x{k:03X}]  {v}')

    def build_debug_calibration_tab(self,notebook):
        tab=ttk.Frame(notebook,padding=0);notebook.add(tab,text='Native menu calibration')
        shell=ttk.Frame(tab)
        shell.pack(fill='both',expand=True)
        canvas=tk.Canvas(shell,bg=PALETTE['background'],highlightthickness=0)
        scroll=ttk.Scrollbar(shell,orient='vertical',command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y')
        canvas.pack(side='left',fill='both',expand=True)
        body=ttk.Frame(canvas,padding=10)
        window=canvas.create_window((0,0),window=body,anchor='nw')
        body.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window, width=e.width))
        def _wheel(event):
            delta = -1 if event.delta < 0 else 1
            canvas.yview_scroll(-delta, 'units')
        canvas.bind_all('<MouseWheel>', _wheel, add='+')
        self.debug_calibration_canvas = canvas
        self.debug_calibration_scrollbar = scroll

        ttk.Label(body,text='ORIGINAL game debug menu: capture the FINAL scene/character highlight without entering the scene. Scanner now includes original N64 overlay memory (4 MiB). Match the toolkit scene and character, then Record.',wraplength=990).pack(anchor='w',pady=5)
        ttk.Label(body,text='Record at least 3 different scenes with the same character and 2 scenes with a second character, plus a different scene category. Each field must match 2+ comparisons before enabling automatic warp.',wraplength=990).pack(anchor='w',pady=5)
        self.debug_calibration_status=tk.StringVar(value='No native menu observations. Existing calibration: '+('ready' if calibrated_for_direct_warp(self.debug_profile) else 'incomplete'))
        ttk.Label(body,textvariable=self.debug_calibration_status,wraplength=950).pack(anchor='w',pady=8)
        watch_box=ttk.LabelFrame(body,text='LIVE READ-ONLY N64 watch (menu AND gameplay transitions)',padding=6)
        watch_box.pack(fill='x',pady=4)
        ttk.Label(watch_box,text='Read-only logging. 0x800C7E60 matched eight native-menu highlights but user also observed 0x80 persisting once the menu opened; the value is not a stable gameplay character selector. Never write it to force a spawn.',wraplength=970).pack(anchor='w')
        self.native_watch_status=tk.StringVar(value='Connect, then open original debug menu. Live values will update automatically.')
        ttk.Label(watch_box,textvariable=self.native_watch_status).pack(anchor='w',pady=(2,3))
        field_columns=('address','value','hex','previous','confidence')
        self.native_watch_tree=ttk.Treeview(watch_box,columns=field_columns,show='tree headings',height=len(NATIVE_WATCH_FIELDS))
        self.native_watch_tree.heading('#0',text='Field');self.native_watch_tree.column('#0',width=205)
        for c,title,w in [('address','N64 address',116),('value','Decimal',80),('hex','Hex',86),('previous','Previous',100),('confidence','Evidence / caution',325)]:
            self.native_watch_tree.heading(c,text=title);self.native_watch_tree.column(c,width=w,stretch=c=='confidence')
        self.native_watch_tree.tag_configure('changed',background='#254f49')
        for field in NATIVE_WATCH_FIELDS:
            self.native_watch_tree.insert('','end',iid=field.key,text=field.label,
                values=(f'0x{field.address:08X}','—','—','—',field.confidence))
        self.native_watch_tree.pack(fill='x')
        controls=ttk.Frame(watch_box);controls.pack(fill='x',pady=3)
        ttk.Label(controls,text='Manual marker:').pack(side='left')
        self.native_watch_note=tk.StringVar(value='SIRO 90 / Goemon')
        ttk.Entry(controls,textvariable=self.native_watch_note,width=29).pack(side='left',padx=4)
        ttk.Button(controls,text='Mark current state',command=self.mark_native_watch).pack(side='left',padx=4)
        ttk.Button(controls,text='Export LIVE watch log',command=self.export_native_watch).pack(side='left',padx=4)
        ttk.Button(controls,text='Clear watch history',command=self.clear_native_watch).pack(side='left',padx=4)
        ttk.Label(watch_box,text='Mark IN-GAME loaded scene while in gameplay (state 13); mark highlighted scene/character BEFORE confirming while in menu (state 10). Automatic changes now include both states and transitions.',wraplength=950).pack(anchor='w')
        tracebox=ttk.LabelFrame(body,text='REAL gameplay door transition trace — READ ONLY',padding=6)
        tracebox.pack(fill='x',pady=4)
        ttk.Label(tracebox,text='Click Start while in a playable room, then WALK THROUGH A NORMAL DOOR. Captures state, current/previous/pending map, phase, exit and loading ~50 times per second for 30 seconds. No N64 writes.',wraplength=950).pack(anchor='w')
        self.transition_status=tk.StringVar(value='Not recording.')
        buttons=ttk.Frame(tracebox);buttons.pack(fill='x',pady=3)
        ttk.Button(buttons,text='Start 30s transition trace',command=self.start_transition_trace).pack(side='left',padx=4)
        ttk.Button(buttons,text='Stop trace',command=self.stop_transition_trace).pack(side='left',padx=4)
        ttk.Button(buttons,text='Export transition JSON',command=self.export_transition_trace).pack(side='left',padx=4)
        ttk.Label(tracebox,textvariable=self.transition_status,wraplength=930).pack(anchor='w')

        row=ttk.Frame(body);row.pack(fill='x',pady=7)
        ttk.Button(row,text='Record highlighted native selection',command=self.record_native_selection).pack(side='left',padx=4)
        ttk.Button(row,text='Find candidate memory fields',command=self.analyse_debug_selection).pack(side='left',padx=4)
        ttk.Button(row,text='Use selected field',command=self.use_debug_candidate).pack(side='left',padx=4)
        ttk.Button(row,text='Export FULL candidate report',command=self.export_debug_candidates).pack(side='left',padx=4)
        self.debug_sample_list=tk.Listbox(body,height=4,font=('Consolas',10),
                                      background='#1a1d23',foreground='#f3eee5',selectbackground='#8c3030')
        self.debug_sample_list.pack(fill='x',pady=5)
        cols=('role','method','addr','width','pairs','examples')
        self.debug_candidates_tree=ttk.Treeview(body,columns=cols,show='headings',height=7)
        for col,width in (('role',110),('method',125),('addr',150),('width',65),('pairs',75),('examples',215)):
            self.debug_candidates_tree.heading(col,text=col.capitalize())
            self.debug_candidates_tree.column(col,width=width)
        self.debug_candidates_tree.pack(fill='both',expand=True)
        ttk.Label(body,text='Candidate addresses are hypotheses, not proven. Select each scene, character (and category, when necessary) field after checking the raw values and repeats. Calibration is stored locally in practice/native_debug_fields.json.',wraplength=990).pack(anchor='w',pady=5)

    def build_character_cursor_tab(self, notebook):
        tab=ttk.Frame(notebook,padding=12)
        notebook.add(tab,text='Character cursor scan')
        ttk.Label(tab,text='READ ONLY: identify the ORIGINAL debug menu character cursor. Do not press A to load a stage. Open the character list and only move its highlight between recordings.',wraplength=980).pack(anchor='w',pady=(2,6))
        ttk.Label(tab,text='Keep category, stage, loaded character and game state unchanged. Each recording takes two RDRAM snapshots ~300 ms apart in a worker thread. Do not move the highlight until capture finishes.',wraplength=980).pack(anchor='w',pady=3)
        ttk.Label(tab,text='Order: Goemon > Ebisumaru > Sasuke > Yae > Yae > Sasuke > Ebisumaru > Goemon. Repeat Yae without moving for #5.',wraplength=980).pack(anchor='w',pady=4)
        self.cursor_status=tk.StringVar(value='No character cursor captures. Open the native debug menu and highlight Goemon.')
        ttk.Label(tab,textvariable=self.cursor_status,wraplength=950).pack(anchor='w',pady=(6,6))
        row=ttk.Frame(tab);row.pack(fill='x',pady=3)
        self.cursor_capture_btn=ttk.Button(row,text='Record #1: Goemon',command=self.record_character_hover)
        self.cursor_capture_btn.pack(side='left',padx=(0,5))
        self.cursor_analyse_btn=ttk.Button(row,text='Analyse character cursor',command=self.analyse_character_cursor)
        self.cursor_analyse_btn.pack(side='left',padx=5)
        self.cursor_analyse_btn.state(['disabled'])
        self.cursor_export_btn=ttk.Button(row,text='Export FULL character report',command=self.export_character_cursor)
        self.cursor_export_btn.pack(side='left',padx=5)
        self.cursor_export_btn.state(['disabled'])
        self.cursor_reset_btn=ttk.Button(row,text='Clear cursor captures',command=self.reset_character_cursor)
        self.cursor_reset_btn.pack(side='left',padx=5)
        self.cursor_record_list=tk.Listbox(tab,height=8,font=('Consolas',10),
                                       background='#1a1d23',foreground='#f3eee5',selectbackground='#8c3030')
        self.cursor_record_list.pack(fill='x',pady=(8,7))
        headings=('addr','width','encoding','goemon','ebi','sasuke','yae')
        frame=ttk.Frame(tab);frame.pack(fill='both',expand=True)
        self.cursor_result_tree=ttk.Treeview(frame,columns=headings,show='headings',height=11)
        for key,caption,width in [('addr','N64 address',145),('width','Bytes',64),('encoding','Pattern',133),('goemon','Goemon',105),('ebi','Ebisumaru',115),('sasuke','Sasuke',105),('yae','Yae',105)]:
            self.cursor_result_tree.heading(key,text=caption)
            self.cursor_result_tree.column(key,width=width,stretch=key=='encoding')
        scroll=ttk.Scrollbar(frame,orient='vertical',command=self.cursor_result_tree.yview)
        self.cursor_result_tree.configure(yscrollcommand=scroll.set)
        self.cursor_result_tree.pack(side='left',fill='both',expand=True)
        scroll.pack(side='right',fill='y')
        ttk.Label(tab,text='Up to 250 candidates are shown here. The JSON exports ALL matches, including numeric 0..3 / 1..4, other linear encodings and repeated non-linear values. A match is not proof; no cursor memory writes are performed.',wraplength=950).pack(anchor='w',pady=5)

    def _cursor_buttons(self):
        waiting=self.cursor_busy
        n=len(self.cursor_captures)
        if n<len(CHARACTER_CURSOR_ORDER):
            self.cursor_capture_btn.configure(text=f'Record #{n+1}: {CHARACTER_CURSOR_NAMES[CHARACTER_CURSOR_ORDER[n]]}')
            self.cursor_capture_btn.state(['disabled'] if waiting else ['!disabled'])
        else:
            self.cursor_capture_btn.configure(text='All 8 character highlights recorded')
            self.cursor_capture_btn.state(['disabled'])
        self.cursor_analyse_btn.state(['disabled'] if waiting or n!=len(CHARACTER_CURSOR_ORDER) else ['!disabled'])
        self.cursor_export_btn.state(['disabled'] if waiting or not self.cursor_analysed else ['!disabled'])
        self.cursor_reset_btn.state(['disabled'] if waiting else ['!disabled'])

    def record_character_hover(self):
        if self.cursor_busy or len(self.cursor_captures)>=len(CHARACTER_CURSOR_ORDER):
            return
        if not self.mem:
            messagebox.showerror('Not connected','Connect to Goemon64Recomp first')
            return
        number=len(self.cursor_captures)
        character=CHARACTER_CURSOR_ORDER[number]
        self.cursor_busy=True
        self._cursor_buttons()
        self.cursor_status.set(f'Capturing #{number+1}: {CHARACTER_CURSOR_NAMES[character]}. Keep highlight still until complete.')
        memory=self.mem
        def work():
            try:
                result=capture_cursor(memory,character)
                self.cursor_job_results.put(('capture',number,result,None))
            except Exception as exc:
                self.cursor_job_results.put(('capture',number,None,str(exc)))
        threading.Thread(target=work,name='goemon-character-hover-capture',daemon=True).start()

    def analyse_character_cursor(self):
        if self.cursor_busy or len(self.cursor_captures)!=len(CHARACTER_CURSOR_ORDER):
            return
        self.cursor_busy=True
        self.cursor_analysed=False
        self._cursor_buttons()
        self.cursor_status.set('Analysing eight stable character highlights in worker thread. The window remains responsive.')
        copies=tuple(self.cursor_captures)
        def work():
            try:
                results=find_cursor_candidates(copies)
                self.cursor_job_results.put(('analyse',None,results,None))
            except Exception as exc:
                self.cursor_job_results.put(('analyse',None,None,str(exc)))
        threading.Thread(target=work,name='goemon-character-hover-analyser',daemon=True).start()

    def poll_cursor_jobs(self):
        try:
            while True:
                kind,number,result,error=self.cursor_job_results.get_nowait()
                self.cursor_busy=False
                if error:
                    self.cursor_status.set(f'{kind.capitalize()} failed: {error}')
                elif kind=='capture':
                    expected=CHARACTER_CURSOR_ORDER[len(self.cursor_captures)]
                    if number != len(self.cursor_captures) or result.character != expected:
                        self.cursor_status.set('Capture discarded: unexpected recording order.')
                    elif self.cursor_captures and result.context != self.cursor_captures[0].context:
                        self.cursor_status.set('Capture discarded: stage/category/active character changed. Re-enter the same character menu and repeat this highlight.')
                    else:
                        self.cursor_captures.append(result)
                        self.cursor_candidates=[]
                        self.cursor_analysed=False
                        context=result.context
                        self.cursor_record_list.insert('end',f'#{number+1} {CHARACTER_CURSOR_NAMES[result.character]:10s} | map {context["absolute_map"]} | category {context["category"]} | in-game char {context["active_character"]}')
                        left=len(CHARACTER_CURSOR_ORDER)-len(self.cursor_captures)
                        next_text=(f'Next: {CHARACTER_CURSOR_NAMES[CHARACTER_CURSOR_ORDER[len(self.cursor_captures)]]}.' if left else 'Now click Analyse character cursor.')
                        self.cursor_status.set(f'Recorded #{number+1} successfully; {left} captures remaining. {next_text}')
                elif kind=='analyse':
                    self.cursor_candidates=result
                    self.cursor_analysed=True
                    self.cursor_result_tree.delete(*self.cursor_result_tree.get_children())
                    for i,c in enumerate(result[:250]):
                        self.cursor_result_tree.insert('','end',iid=str(i),values=(c['addr'],c['width'],c['encoding'],*c['values']))
                    counts={name:sum(c['encoding']==name for c in result) for name in ('zero_based','one_based','linear','lookup')}
                    self.cursor_status.set(f'{len(result)} stable repeated matches; pattern counts {counts}. Export FULL character report. No writes made.')
                self._cursor_buttons()
        except queue.Empty:
            pass
        try:
            self.root.after(120,self.poll_cursor_jobs)
        except tk.TclError:
            pass

    def reset_character_cursor(self):
        if self.cursor_busy:
            return
        self.cursor_captures=[]
        self.cursor_candidates=[]
        self.cursor_analysed=False
        self.cursor_record_list.delete(0,'end')
        self.cursor_result_tree.delete(*self.cursor_result_tree.get_children())
        self.cursor_status.set('Character captures cleared. Highlight Goemon and begin again.')
        self._cursor_buttons()

    def export_character_cursor(self):
        if not self.cursor_analysed or self.cursor_busy:
            self.cursor_status.set('Record eight highlights and run the analysis first.')
            return
        root=diagnostics_dir()
        root.mkdir(parents=True,exist_ok=True)
        path=root/('native_character_cursor_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
        payload=make_cursor_report(self.cursor_captures,self.cursor_candidates)
        import os
        temp=path.with_suffix('.json.tmp')
        try:
            with temp.open('w',encoding='utf-8') as f:
                json.dump(payload,f,indent=2)
                f.write('\n')
            os.replace(temp,path)
            self.cursor_status.set(f'Exported ALL {len(self.cursor_candidates)} character cursor candidates: {path}')
        except OSError as exc:
            self.cursor_status.set(f'Export failed: {exc}')
            try:temp.unlink(missing_ok=True)
            except OSError:pass

    def refresh_native_watch(self, now):
        """Poll *while native menu is open*; toolkit.tick skips the player UI there."""
        if not hasattr(self,'native_watch_tree') or not self.mem or now-self.native_watch_last_at < 0.20:
            return
        self.native_watch_last_at=now
        try:
            live=read_native_watches(self.mem)
        except (OSError,ValueError) as exc:
            self.native_watch_status.set(f'Live watch unavailable: {exc}')
            return
        previous=self.native_watch_current
        changes=changed_native_watches(previous,live)
        for field in NATIVE_WATCH_FIELDS:
            v=live[field.key]
            older=previous.get(field.key)
            prev_disp='—' if older is None else str(older)
            row=self.native_watch_tree
            row.item(field.key,values=(f'0x{field.address:08X}',str(v),f'0x{v:0{field.width*2}X}',prev_disp,field.confidence),
                     tags=('changed',) if field.key in changes else ())
        self.native_watch_current=live
        state=live['state']
        state_label='DEBUG MENU' if state==10 else ('GAMEPLAY' if state==13 else f'TRANSITION/OTHER {state}')
        hover_name=decode_hover_pointer(live.get('hover_pointer',-1)) if state==10 else None
        hover_label=(f'  |  Hover candidate: {hover_name}' if hover_name else '')
        self.native_watch_status.set(f'Game state: {state_label}{hover_label}  |  {len(changes)} fields changed at last poll  |  {len(self.native_watch_events)} events retained')
        evt=make_native_change_event(previous,live,datetime.now(timezone.utc).isoformat())
        if evt:
            self.native_watch_events.append(evt)
            self.native_watch_events=self.native_watch_events[-1500:]

    def mark_native_watch(self):
        if not self.mem:
            messagebox.showerror('Not connected','Connect to the game first')
            return
        try:
            live=read_native_watches(self.mem)
            if not can_mark_native_state(live['state']):
                raise ValueError(f'Only stable gameplay (state 13) or original debug menu (state 10) may be marked; observed {live["state"]}')
            note=self.native_watch_note.get().strip()
            if not note:
                raise ValueError('Describe the currently highlighted OR loaded scene and character')
            self.native_watch_events.append({'utc':datetime.now(timezone.utc).isoformat(),
                                             'kind':'marker','label':note,'values':live})
            self.native_watch_events=self.native_watch_events[-1500:]
            self.native_watch_status.set(f'Marked "{note}" — {len(self.native_watch_events)} retained events')
        except (OSError,ValueError) as exc:
            messagebox.showerror('Cannot mark menu selection',str(exc))

    def clear_native_watch(self):
        self.native_watch_events=[]
        self.native_watch_previous={}
        self.native_watch_current={}
        self.native_watch_status.set('Live watch history cleared. Current values continue updating.')

    def export_native_watch(self):
        if not self.native_watch_events:
            messagebox.showerror('No samples','Mark game or debug-menu state before exporting')
            return
        root=diagnostics_dir()
        root.mkdir(parents=True,exist_ok=True)
        path=root/('native_watch_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
        payload={'format':'mnsg-usa-original-debug-live-watch-v1',
                 'note':'Read-only original N64 guest values. v0.9.4 logs BOTH menu and gameplay states. Candidate cursor mapping NOT verified; map-state can change while menu is open; no RAM dumps or game assets.',
                 'fields':[{'key':x.key,'label':x.label,'address':f'0x{x.address:08X}',
                            'width':x.width,'confidence':x.confidence} for x in NATIVE_WATCH_FIELDS],
                 'events':self.native_watch_events}
        path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
        self.native_watch_status.set(f'Exported {len(self.native_watch_events)} watch events to {path}')

    def record_native_selection(self):
        if not self.mem or not menu_state(self.mem):
            messagebox.showerror('Debug menu not active','Open the ORIGINAL debug menu, highlight the selected scene and character, and do not press A yet.')
            return
        chosen=self.scene_list.curselection()
        if not chosen:
            messagebox.showerror('Missing scene','Select the scene highlighted in the game using the Scene browser first.')
            return
        map_id=self.scene_options[chosen[0]][0]
        character=self.scene_character.current()
        if character<0: return
        try:
            first=take_menu_snapshot(self.mem)
        except Exception as exc:
            messagebox.showerror('Capture failed',str(exc));return
        self.debug_calibration_status.set('Capturing second menu snapshot; leave the game selection unchanged...')
        self.root.after(300,lambda:self._finish_native_observation(map_id,character,first))

    def _finish_native_observation(self,map_id,character,first):
        try:
            second=take_menu_snapshot(self.mem)
            obs=Observation(map_id,character,first,second)
            self.debug_observations.append(obs)
            stable=sum(x==y for x,y in zip(first,second))
            self.debug_sample_list.insert('end',f'#{len(self.debug_observations)} map={map_id} character={character} stable={stable}/{len(first)} bytes')
            self.debug_calibration_status.set(f'Captured {len(self.debug_observations)} observations. Now change menu selection and record again.')
        except Exception as exc:
            self.debug_calibration_status.set(f'Capture refused: {exc}')

    def analyse_debug_selection(self):
        if len(self.debug_observations)<2:
            self.debug_calibration_status.set('Capture at least two distinct native menu selections first.')
            return
        self.debug_candidates=find_candidates(self.debug_observations)
        self.debug_candidates_tree.delete(*self.debug_candidates_tree.get_children())
        self.debug_display_indices=display_candidate_indices(self.debug_candidates)
        for i, candidate_index in enumerate(self.debug_display_indices):
            c=self.debug_candidates[candidate_index]
            self.debug_candidates_tree.insert('','end',iid=str(i),values=(c.role,c.method,f'0x{c.addr:08X}',c.width,c.examples,f'{c.before} -> {c.after}'))
        self.debug_calibration_status.set(
            f'{len(self.debug_candidates)} total candidates; displaying {len(self.debug_display_indices)} ' +
            'across character, scene and category. Require 2+ matching comparisons per field; export contains ALL candidates.')

    def export_debug_candidates(self):
        if not self.debug_candidates:
            self.analyse_debug_selection()
        if not self.debug_candidates:
            self.debug_calibration_status.set('No candidates to export. Record several contrasting selections.')
            return
        root=diagnostics_dir()
        root.mkdir(parents=True,exist_ok=True)
        from datetime import datetime,timezone
        path=root/('native_menu_candidates_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
        data=candidate_report(self.debug_observations,self.debug_candidates,self.debug_profile)
        # Write to a temporary path first to avoid leaving a partial JSON report.
        import os
        temporary=path.with_suffix('.json.tmp')
        try:
            with temporary.open('w',encoding='utf-8') as f:
                json.dump(data,f,indent=2)
                f.write('\n')
            os.replace(temporary,path)
        except OSError as exc:
            try:temporary.unlink(missing_ok=True)
            except OSError:pass
            messagebox.showerror('Report export failed',str(exc))
            return
        self.debug_calibration_status.set(f'Exported ALL {len(self.debug_candidates)} candidates (no RAM dump): {path}')

    def use_debug_candidate(self):
        chosen=self.debug_candidates_tree.selection()
        if not chosen:return
        c=self.debug_candidates[self.debug_display_indices[int(chosen[0])]]
        if c.examples < 2:
            messagebox.showerror('Insufficient evidence',f'This candidate matched {c.examples} comparison(s); at least two are required before enabling native-menu memory writes. Capture more contrasting selections, then analyse again.')
            return
        if not messagebox.askyesno('Experimental learned N64 field',
                 f'Use {c.role}: {c.method} at guest 0x{c.addr:08X} ({c.width} byte(s))?\n'
                 'This is an observation-based hypothesis and can crash the game when used. Use disposable saves.'):
            return
        profile=dict(self.debug_profile)
        profile['fields']=dict(profile.get('fields',{}))
        profile['fields'][c.role]={'addr':f'0x{c.addr:08X}','width':c.width,'method':c.method,'pairs':c.examples}
        try:
            save_profile(DEBUG_PROFILE_PATH,profile)
            self.debug_profile=profile
        except Exception as exc:
            messagebox.showerror('Field incompatible',str(exc));return
        ready=calibrated_for_direct_warp(profile)
        self.debug_calibration_status.set(f'Saved {c.role} field. Native one-click menu automation: {"available (experimental)" if ready else "NOT yet calibrated"}.')

    def _save_direct_warp_diagnostics(self, pending):
        """Capture non-sensitive numeric N64 state; no raw dumps or ROM assets."""
        out=diagnostics_dir()
        out.mkdir(parents=True,exist_ok=True)
        path=out / ('direct_warp_' + pending['date_code'] + '.json')
        payload={'format':'goemon-usa-experimental-direct-warp-v1',
                 'warning':'Unverified transition fields; no claimed native warp success',
                 'destination':pending['map_id'], 'source_map':pending['from_map'],
                 'original_character':pending['character'],
                 'requested_character':pending.get('selected_character'),
                 'observed_character':pending.get('observed_character'),
                 'character_staged':pending.get('character_staged',False),
                 'status':pending['status'], 'samples':pending['events'],
                 'entrance':pending.get('entrance'),'placement':pending.get('placement_result')}
        path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
        return str(path)


    def try_reload_warp(self):
        if self.pending_direct_warp or self.pending_restore or self.pending_native_warp:
            self.scene_status.set('Another scene or checkpoint transition is pending; finish or cancel it first.')
            return
        chosen=self.scene_list.curselection()
        if not chosen:
            self.scene_status.set('Select a destination first.')
            return
        dest,name=self.scene_options[chosen[0]]
        target_character=self.scene_character.current()
        if target_character not in range(4):
            self.scene_status.set('Choose a target character 0–3 first.')
            return
        if not self.mem:
            self.scene_status.set('Connect to Goemon64Recomp first.')
            return
        if not getattr(self.args,'enable_teleport',False):
            self.scene_status.set('Position restoration is disabled; entrance reload was not sent.');return
        if not getattr(self.args,'enable_hex_edit',False) or not self.hex_advanced.get():
            self.scene_status.set('Enable Live Memory UNSAFE before experimental reloading.')
            return
        try:spawn=self.selected_scene_spawn(dest)
        except ValueError as exc:
            self.scene_status.set(str(exc));return
        if not messagebox.askyesno('Experimental entrance reload',
            f'Reload {dest} ({name}) at {spawn.label}?\n'
            f'XYZ {tuple(spawn.position)}, character {target_character}.\n'
            'The original reload remains experimental; model, collision, camera and scripts may differ from an ordinary door transition.'):
            return
        try:
            info=stage_reload_trial(self.mem,dest,self.scene_catalog(),spawn_character=target_character,spawn=spawn)
            now=__import__('time').monotonic()
            self.pending_direct_warp={
                'map_id':dest,'from_map':info['source_map'],'character':info['source_character'],
                'selected_character':target_character, 'observed_character':None,
                'phase':'loading', 'character_staged':info['character_staged'],
                'source_position':info['source_position'], 'start_at':now, 'last_message_at':now,
                'date_code':datetime.now().strftime('%Y%m%d_%H%M%S_%f'),
                'events':[], 'status':'requested_0x0C','stable':0,
                'entrance':dict(id=spawn.entrance_id,label=spawn.label,position=list(spawn.position),heading=spawn.heading,mode=spawn.mode),
                'placement':SpawnPlacement(self.mem,spawn,target_character,info['source_map'],info['player_ptr'],info['task_ptr'],now,seen_transition=True),
            }
            self.scene_status.set(f'Experimental reload sent: {info["source_map"]} → {dest}. '
                f'Entrance XYZ {tuple(spawn.position)} staged before reload; waiting to check the loaded player.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.scene_status.set(f'Reload trial failed: {exc}')

    def _finish_direct_warp(self, pending, status, summary):
        pending['status']=status
        try:
            path=self._save_direct_warp_diagnostics(pending)
            summary=f'{summary} Diagnostic: {path}'
        except OSError as exc:
            summary=f'{summary} (Could not save diagnostic: {exc})'
        self.scene_status.set(summary)
        self.pending_direct_warp=None

    def poll_direct_warp(self,now):
        """Place only the requested destination player; never repair actor IDs."""
        pending=self.pending_direct_warp
        if not pending or not self.mem:return
        if getattr(self.args,'read_only',False) or not self.args.enable_teleport or not self.args.enable_hex_edit or not self.hex_advanced.get():
            self.pending_direct_warp=None;return
        try:
            assessment=assess_direct_warp(self.mem,pending['map_id'])
            pending['events'].append({'seconds':round(now-pending['start_at'],3),**assessment})
            result=pending['placement'].poll(self.mem,now)
            if result['status']=='placed':
                pending['placement_result']=result;pending['observed_character']=result['character']
                self._finish_direct_warp(pending,'entrance_coordinates_applied',
                    f'Entrance XYZ applied in stage {pending["map_id"]}: {tuple(result["observed"])}. '
                    'Character verified; confirm footing/camera in-game.')
            else:self.scene_status.set(f'Reload requested; waiting for entrance placement ({result["reason"]}).')
        except (OSError,ValueError,RuntimeError) as exc:
            self._finish_direct_warp(pending,'placement_stopped',f'Entrance placement stopped: {exc}. No further writes.')

    def request_direct_scene(self,mid,name):
        """Double-click is selection-only; experimental writes need a dedicated button."""
        self.scene_status.set(
            f'Selected {mid} ({name}); double-click warp DISABLED, no memory writes sent. Use the explicit '
            'EXPERIMENT reload button and choose a ROM entrance after enabling UNSAFE.'
        )

    def start_transition_trace(self):
        from practice.transition_trace import TransitionTrace
        if not self.mem:
            self.transition_status.set('Connect to the game first.')
            return
        previous=getattr(self,'transition_trace',None)
        if previous and previous.thread and previous.thread.is_alive():
            self.transition_status.set('Trace is already recording.')
            return
        self.transition_trace=TransitionTrace(self.mem,duration=30.0,interval=0.02)
        self.transition_trace.start()
        self.transition_status.set('Recording 30 seconds at ~50 Hz. Walk through a normal in-game doorway.')
        self.root.after(250,self.refresh_transition_status)

    def refresh_transition_status(self):
        trace=getattr(self,'transition_trace',None)
        if trace is None:return
        if trace.thread and trace.thread.is_alive():
            self.transition_status.set('Recording real area transitions: %d samples; %d changes. Normal gameplay only.' %
                                       (trace.samples,len(trace.events)-1))
            self.root.after(250,self.refresh_transition_status)
        else:
            self.transition_status.set('Trace finished: %d samples, %d changes. Export trace to JSON.' %
                                       (trace.samples,max(0,len(trace.events)-1)))

    def stop_transition_trace(self):
        trace=getattr(self,'transition_trace',None)
        if trace is not None:
            trace.stop()
            self.refresh_transition_status()

    def export_transition_trace(self):
        trace=getattr(self,'transition_trace',None)
        if trace is None:
            self.transition_status.set('No trace to export.')
            return
        trace.stop()
        out=diagnostics_dir()
        out.mkdir(parents=True,exist_ok=True)
        path=out/('normal_transition_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
        report = trace.report()
        path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        self.transition_status.set('Exported READ-ONLY transition trace: %s (%d full samples, %d change events).' % (path, len(report.get('samples_trace', [])), len(report.get('events', []))))

    def poll_native_warp_menu(self,now):
        if getattr(self.args, 'read_only', False) or not self.args.enable_teleport:
            self.pending_native_warp=None
            return
        pending=self.pending_native_warp
        if not pending or not self.mem:return
        from practice.checkpoints import MAP_ADDR
        if now>pending['deadline']:
            self.scene_status.set(f'Native warp NOT confirmed: map {pending["map_id"]}, character {pending["character"]}. No additional writes will be made.')
            self.pending_native_warp=None
            return
        state=self.mem.u8(STATE_ADDR)
        if state==10 and not pending.get('manual') and not pending['staged'] and now>=pending['start_at']:
            try:
                info=stage_menu_selection(self.mem,self.debug_profile,pending['map_id'],pending['character'])
                pending['staged']=True
                pending['confirm_at']=now+0.36
                self.scene_status.set('Native debug menu selection staged from learned fields. Preparing to confirm using original N64 A input.')
            except Exception as exc:
                self.scene_status.set(f'Native selection failed: {exc}; complete manually in the game.')
                self.pending_native_warp=None
                return
        if state==10 and pending['staged'] and not pending['confirmed'] and now>=pending['confirm_at']:
            try:
                # If the game rewrites cursor variables each frame, our learned
                # addresses were only a mirror. Do NOT press A on a stale value.
                from practice.native_debug_trace import selection_values
                expected=selection_values(pending['map_id'])
                for field in self.debug_profile['fields'].values():
                    address=int(field['addr'],16) if isinstance(field['addr'],str) else field['addr']
                    correct=(pending['character'] if field['method']=='character_id' else expected[field['method']])
                    observed=int.from_bytes(self.mem.read_guest(address,field['width']),'big')
                    if observed!=correct:
                        raise RuntimeError(f'Original menu rewrote 0x{address:08X} ({observed} != {correct}); automatic A suppressed')
                release=press_native_debug_accept(self.game_pid)
                self.native_key_release=release
                self.root.after(130,self._release_debug_key)
                pending['confirmed']=True
                self.scene_status.set('Original debug menu A button sent. Waiting to observe loaded scene. No result assumed.')
            except Exception as exc:
                self.scene_status.set(f'Debug selection staged; press A in the game manually: {exc}')
                pending['confirmed']=True
        if pending.get('placement'):
            try:
                result=pending['placement'].poll(self.mem,now)
                if result['status']=='placed':
                    self.scene_status.set(f'Native-menu destination {pending["map_id"]}: entrance XYZ applied {tuple(result["observed"])}; confirm footing in-game.')
                    self.pending_native_warp=None
            except (OSError,ValueError,RuntimeError) as exc:
                self.scene_status.set('Native entrance placement stopped: '+str(exc))
                self.pending_native_warp=None

    def _release_debug_key(self):
        if self.native_key_release:
            try:self.native_key_release()
            finally:self.native_key_release=None

    def select_scene(self,event=None):
        """A single click only selects; never writes guest RAM."""
        chosen=self.scene_list.curselection()
        if not chosen:return
        mid,name=self.scene_options[chosen[0]]
        self.scene_selected=mid
        self.refresh_entrance_choices(mid)
        try:
            target=native_debug_selection(mid,self.scene_catalog())
            self.scene_status.set(
                f'Selected {mid}: {name}. Native debug index: {target["label"]}. '
                'Direct warp disabled; double-click will make NO guest memory writes. Separate button opens the original debug menu.')
        except ValueError as e:
            self.scene_status.set(str(e))

    def activate_selected_scene(self,event=None):
        """Double-click requests a direct gameplay scene transition, NO debug menu."""
        chosen=self.scene_list.curselection()
        if not chosen:return
        mid,name=self.scene_options[chosen[0]]
        self.request_direct_scene(mid,name)

    def open_debug_for_selected_scene(self,event=None):
        """Separate manual native menu path, intentionally not the double-click path."""
        chosen=self.scene_list.curselection()
        if not chosen:return
        mid,name=self.scene_options[chosen[0]]
        character=self.scene_character.current()
        if character<0:return
        if not self.mem or not self.args.enable_debug_menu:
            messagebox.showerror('Not connected','Connect via Run.bat first')
            return
        if not self.args.enable_teleport:
            self.scene_status.set('Position restoration is disabled; scene request was not sent.');return
        if self.pending_direct_warp or self.pending_restore or self.pending_native_warp:
            self.scene_status.set('Another scene or checkpoint request is pending.');return
        try:
            spawn=self.selected_scene_spawn(mid)
            source=self.mem.snapshot();source_map=self.mem.u16(MAP_ADDR)
        except (OSError,ValueError) as exc:
            self.scene_status.set(str(exc));return
        ready=calibrated_for_direct_warp(self.debug_profile)
        if ready and not self.native_warp_confirmed:
            if not messagebox.askyesno('Experimental native warp',
                'This uses addresses LEARNED from original debug-menu selections and then sends N64 A.\n'
                'Calibration is not proof of safety. It can crash/softlock the game. Continue on a disposable save?'):
                return
            self.native_warp_confirmed=True
        if not ready and not self.debug_shortcut_confirmed:
            if not messagebox.askyesno('Native debug menu needs calibration',
                'This build cannot safely invent the menu selection addresses.\n'
                'Open the native debug menu now for manual navigation / calibration?'):
                return
            self.debug_shortcut_confirmed=True
        try:
            result=open_native_debug_for_scene(self.mem,mid,self.scene_catalog())
            from time import monotonic
            now=monotonic();timeout=18 if ready else 90
            self.pending_native_warp={'map_id':mid,'character':character,'start_at':now+0.85,
                'deadline':now+timeout,'staged':False,'confirmed':False,'confirm_at':None,'manual':not ready,
                'placement':SpawnPlacement(self.mem,spawn,character,source_map,source['player_ptr'],source['task_ptr'],now,timeout=timeout)}
            if ready:self.scene_status.set(f'Opening native menu for stage {mid}; entrance placement is armed.')
            else:self.scene_status.set(f'Native menu opened. Manually choose {result["label"]}, character {character}; selected entrance XYZ will apply only after that destination loads.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.scene_status.set(f'Native debug entry blocked: {exc}')
            messagebox.showerror('Native debug entry failed',str(exc))

    def enter_debug_menu(self):
        """Preserve previous call-site compatibility: open with selected hint."""
        self.activate_selected_scene()

    def export_inspector(self):
        if not self.mem or not self.watch_rows:
            messagebox.showerror('No data','Connect and wait for current readings')
            return
        out=diagnostics_dir()
        out.mkdir(parents=True,exist_ok=True)
        path=out/('inspect_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
        data={'format':'goemon-inspector-usa-v1','captured_utc':datetime.now(timezone.utc).isoformat(),
              'note':'Observations; reverse-engineered source statuses. No game ROM/assets.',
              'watches':[{'name':w.name,'n64':(f'0x{w.addr:08X}' if w.addr else None),
                          'value':w.value,'raw':w.raw,'status':w.status,'source':w.source} for w in self.watch_rows],
              'changes':self.log_events}
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        self.inspector_status.set('Exported diagnostics to '+str(path))
