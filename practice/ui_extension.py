"""Live inspector, diagnostics and opt-in direct gameplay warp trial (v0.9.7)."""
from __future__ import annotations
import json
import queue
import threading
from datetime import datetime, timezone
from dataclasses import replace
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
from practice.watch_names import load_watch_names, save_watch_names, validate_watch_label
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
WATCH_NAMES_PATH = practice_data_dir() / "watch_names.json"

class InspectorMixin(EntranceMixin):
    def build_inspector_tabs(self, notebook):
        self.init_entrances()
        self.watch_previous={}
        self.watch_rows=[]
        self.custom_watch_load_error=None
        try:
            self.custom_watches=load_watches(CUSTOM_WATCHES_PATH)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            self.custom_watches=[]
            self.custom_watch_load_error=str(exc)
        self.watch_aliases={}
        self.watch_alias_load_error=None
        try:
            self.watch_aliases=load_watch_names(WATCH_NAMES_PATH)
        except (OSError,ValueError,TypeError) as exc:
            self.watch_alias_load_error=str(exc)
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
        self.scene_status=tk.StringVar(value='Double-click an area to request an experimental entrance reload. Requires a connected game, a resolved ROM entrance and write access.')
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
                  'Double-click its Hex cell to edit.',
                  style='Muted.TLabel').pack(anchor='w',pady=(4,0))
        if self.custom_watch_load_error:
            ttk.Label(watch_tools,text='Existing custom watch file could not be read: '+self.custom_watch_load_error,
                      style='Muted.TLabel').pack(anchor='w')
        if self.watch_alias_load_error:
            ttk.Label(watch_tools,text='Saved field names could not be read: '+self.watch_alias_load_error,
                      style='Muted.TLabel').pack(anchor='w')
        ttk.Label(inspector,text='Right-click a Live memory row to freeze/unfreeze its current value or rename the field. Names persist; freezes do not. Double-click the Hex cell to edit. Writes are enabled unless launched with --read-only.').pack(anchor='w')
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
        ttk.Button(manual,text='Freeze raw hex',command=self.freeze_raw_value).pack(side='left',padx=6)
        ttk.Button(manual,text='Manage freezes / max health',command=lambda:self.notebook.select(self.value_freezes_tab)).pack(side='left')
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
        self.watch_context_menu=tk.Menu(self.watch_tree,tearoff=False)
        self.watch_tree.bind('<Button-3>',self.open_live_watch_menu)
        self.watch_tree.bind('<Control-Button-1>',self.open_live_watch_menu)
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
        self.scene_instruction=ttk.Label(
            scenes,text='Single-click selects; double-click requests the '
                        'version-specific native scene warp.')
        self.scene_instruction.pack(anchor='w')
        character_line=ttk.Frame(scenes);character_line.pack(fill='x',pady=4)
        self.scene_character_line=character_line
        ttk.Label(character_line,text='Target character:').pack(side='left')
        self.scene_character=ttk.Combobox(character_line,state='readonly',width=30,
               values=('0 - Goemon','1 - Ebisumaru','2 - Sasuke (inferred)','3 - Yae (inferred)'))
        self.scene_character.current(0)
        self.scene_character.pack(side='left',padx=8)
        self.scene_character_note = ttk.Label(
            character_line,
            text='Keep current by default; alternate character is staged before reload (experimental).')
        self.scene_character_note.pack(side='left')
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
        self.scene_transition_note=ttk.Label(
            scenes, text='USA experimental entrance reload with actor and XYZ '
                         'checks. Japan uses the native debug-menu category/stage '
                         'and A input instead of direct scene ID writes.',
            wraplength=950)
        self.scene_transition_note.pack(anchor='w',pady=3)
        self.experimental_warp_btn=ttk.Button(scenes,text='Warp to selected scene',
            command=self.try_reload_warp,style='Gold.TButton')
        self.experimental_warp_btn.pack(fill='x',pady=4)
        if not self.args.enable_hex_edit:self.experimental_warp_btn.state(['disabled'])
        ttk.Label(scenes,textvariable=self.scene_status,wraplength=950).pack(anchor='w',pady=8)
        self.native_debug_btn=ttk.Button(scenes,text='Instead OPEN original debug menu (manual selection)',command=self.enter_debug_menu)
        self.native_debug_btn.pack(fill='x',pady=5)
        if not self.args.enable_debug_menu:self.native_debug_btn.state(['disabled'])
        self.scene_footer_note=ttk.Label(
            scenes,text='USA reload uses the selected entrance; Japan uses its '
                        'native debug menu to load the chosen room.',
            wraplength=950)
        self.scene_footer_note.pack(anchor='w')

    def configure_scene_browser_region(self):
        """One browser with two explicit, separately validated warp backends."""
        japan = self.active_version.key == 'japan'
        if japan:
            self.scene_instruction.configure(
                text='JAPAN: single-click selects; double-click immediately '
                     'requests the selected room using the same 0x0C area '
                     'reload mechanism as USA. No debug menu is opened.')
            self.scene_character.configure(values=(
                'Keep current character',
                'Goemon', 'Ebisumaru', 'Sasuke', 'Yae'))
            self.scene_character.current(0)
            self.scene_character_line.pack(fill='x', pady=4,
                                           after=self.scene_instruction)
            self.entrance_box.pack_forget()
            self.scene_transition_note.configure(
                text='Japan-0: stage the pending destination at '
                     '0x800CD490, then request native area reload 0x0C at '
                     '0x800CD284. No input injection; verify loaded scene.')
            self.experimental_warp_btn.configure(
                text='Warp to selected Japanese scene')
            self.native_debug_btn.configure(
                text='Open ORIGINAL debug menu (manual only)')
            enabled = bool(
                (getattr(self.args, 'enable_japan_scene_writes', False)
                 or getattr(self.args, 'enable_japan_debug_menu_writes', False))
                and not getattr(self.args, 'read_only', False))
            self.scene_footer_note.configure(
                text='Scene Browser instantly triggers Japan-0 native reload '
                     '(0x0C). If cached USA reference entrance data exists, '
                     'use it when unambiguous. No active-map or exit-bit writes.')
        else:
            self.scene_instruction.configure(
                text='USA: single-click selects; double-click uses the '
                     'selected entrance reload. Manual debug menu is separate.')
            self.scene_character.configure(values=(
                '0 - Goemon','1 - Ebisumaru','2 - Sasuke (inferred)','3 - Yae (inferred)'))
            self.scene_character.current(0)
            self.scene_character_line.pack(fill='x', pady=4,
                                           after=self.scene_instruction)
            self.entrance_box.pack(fill='x', pady=4,
                                   after=self.scene_character_line)
            self.scene_transition_note.configure(
                text='USA experimental native entrance reload with verified '
                     'spawn and character checks.')
            self.experimental_warp_btn.configure(
                text='Warp to selected USA entrance')
            self.native_debug_btn.configure(
                text='Open original debug menu (manual only)')
            enabled = bool(getattr(self.args, 'enable_hex_edit', False)
                           and getattr(self.args, 'enable_teleport', False)
                           and not getattr(self.args, 'read_only', False))
            self.scene_footer_note.configure(
                text='USA and Japan both use native 0x0C area reloads, '
                     'with independent region-specific addresses.')
        self.experimental_warp_btn.state(
            ['!disabled'] if enabled else ['disabled'])
        manual = bool(
            (getattr(self.args, 'enable_japan_debug_menu_writes', False)
             if japan else getattr(self.args, 'enable_debug_menu', False))
            and not getattr(self.args, 'read_only', False))
        self.native_debug_btn.state(
            ['!disabled'] if manual else ['disabled'])
        self.draw_scene_list()
        self.scene_status.set(
            'Japan-0: select a room and double-click for a native warp.'
            if japan else 'USA: select a room and double-click for '
                          'the experimental entrance reload.')

    def refresh_checkpoint_options(self):
        if not hasattr(self,'diff_cp'):return
        labels=self.checkpoint_labels()
        self.diff_cp['values']=labels
        if labels and self.diff_cp.current()<0:self.diff_cp.current(len(labels)-1)

    def add_custom_watch(self):
        if self.active_version.key == 'japan':
            if self.add_japan_custom_watch_from_search(
                    self.user_watch_address.get(),
                    self.user_watch_type.get(),
                    label=self.user_watch_name.get()):
                self.refresh_inspector({})
                self.inspector_status.set(
                    'Japan-only typed custom watch saved; read-only.')
            else:
                self.inspector_status.set(self.jp_custom_watch_status.get())
            return
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
        if self.active_version.key == 'japan':
            selected = set(self.watch_tree.selection())
            found = next(
                (item for item in self.jp_custom_watches
                 if item.row_name in selected), None)
            if found is None:
                self.inspector_status.set('Select a Japanese custom watch first.')
                return
            updated = [item for item in self.jp_custom_watches if item != found]
            try:
                save_watches(self.jp_watch_path, updated)
            except (OSError, ValueError) as exc:
                self.inspector_status.set(f'Japan watch removal failed: {exc}')
                return
            self.jp_custom_watches = updated
            if self.jp_fields_tree.exists(self._jp_custom_iid(found)):
                self.jp_fields_tree.delete(self._jp_custom_iid(found))
            self._jp_reset_comparison()
            self.refresh_japan_fields(force=True)
            self.refresh_inspector({})
            self.inspector_status.set(f'Removed Japan-only watch: {found.name}')
            return
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

    def display_watch_name(self, row_id):
        """An alias changes presentation only; the stable row ID remains original."""
        return self.watch_aliases.get(row_id, row_id)

    def open_live_watch_menu(self, event):
        """Right-click acts on the row under the pointer, never a previous selection."""
        row_id=self.watch_tree.identify_row(event.y)
        watch=next((w for w in self.watch_rows if w.name==row_id),None)
        if not row_id or not self.watch_tree.exists(row_id) or watch is None:
            return 'break'
        self.watch_tree.selection_set(row_id)
        self.watch_tree.focus(row_id)
        menu=self.watch_context_menu
        menu.delete(0,'end')
        active=(watch.addr is not None and self.value_freezes.get(watch.addr) is not None)
        menu.add_command(label='Unfreeze value' if active else 'Freeze value',
                         state='normal' if (self.active_version.key != 'japan'
                              and watch.addr is not None
                              and not getattr(self.args,'read_only',False))
                              else 'disabled',
                         command=lambda row_id=row_id:self.toggle_live_watch_freeze(row_id))
        menu.add_command(label='Rename field…',
                         command=lambda row_id=row_id:self.rename_live_watch(row_id))
        try:
            menu.tk_popup(event.x_root,event.y_root)
        finally:
            menu.grab_release()
        return 'break'

    def toggle_live_watch_freeze(self, row_id):
        watch=next((w for w in self.watch_rows if w.name==row_id),None)
        if watch is None or watch.addr is None:
            self.inspector_status.set('No fixed guest address for this field.')
            return
        if self.value_freezes.get(watch.addr) is not None:
            self.value_freezes.remove(watch.addr)
            self.draw_value_freezes()
            self.freeze_status.set(f'Unfroze {self.display_watch_name(row_id)}.')
            self.inspector_status.set(self.freeze_status.get())
        else:
            self.freeze_watch_by_id(row_id)

    def rename_live_watch(self, row_id):
        """Rename a custom watch definition, or persist a built-in display alias."""
        watch=next((w for w in self.watch_rows if w.name==row_id),None)
        if watch is None:
            self.inspector_status.set('This Live Memory field is no longer available.')
            return
        spec=next((s for s in self.custom_watches if s.row_name==row_id),None)
        previous=self.display_watch_name(row_id)
        proposed=simpledialog.askstring(
            'Rename Live Memory field',
            ('New custom watch name (1–64 characters):' if spec else
             'New display name (1–64 characters; blank restores original):'),
            initialvalue=spec.name if spec else previous,parent=self.root)
        if proposed is None:
            return
        try:
            if spec is not None:
                renamed=make_watch(proposed,spec.address,spec.kind)
                new_id=renamed.row_name
                if new_id==row_id:
                    return
                changed=[renamed if s.row_name==row_id else s for s in self.custom_watches]
                save_watches(CUSTOM_WATCHES_PATH,changed)
                self.custom_watches=changed
                self.watch_rows=[replace(w,name=new_id) if w.name==row_id else w for w in self.watch_rows]
                if row_id in self.watch_previous:
                    self.watch_previous[new_id]=self.watch_previous.pop(row_id)
                new_label=new_id
            else:
                new_label=validate_watch_label(proposed) if proposed.strip() else row_id
                aliases=dict(self.watch_aliases)
                if new_label==row_id:
                    aliases.pop(row_id,None)
                else:
                    aliases[row_id]=new_label
                save_watch_names(WATCH_NAMES_PATH,aliases)
                self.watch_aliases=aliases
                new_id=row_id
            # Keep an already-active lock's label consistent with the renamed field.
            if watch.addr is not None:
                lock=self.value_freezes.get(watch.addr)
                if lock is not None and lock.label==previous:
                    self.value_freezes.rename_lock(watch.addr,previous,new_label)
                    self.draw_value_freezes()
            self.draw_watches()
            if not self.watch_tree.exists(new_id):
                self.filter_text.set('')
            if self.watch_tree.exists(new_id):
                self.watch_tree.selection_set(new_id)
                self.watch_tree.see(new_id)
            self.inspector_status.set(f'Field renamed: {previous} → {new_label}.')
        except (ValueError,OSError,TypeError) as exc:
            self.inspector_status.set(f'Rename failed: {exc}')

    def write_raw_hex(self):
        """Write explicitly entered guest bytes on a writable USA connection."""
        if self.active_version.key == 'japan':
            self.inspector_status.set(
                'Japanese raw writes require a verified region-specific control; '
                'generic USA raw editor is disabled.')
            return
        if not self.mem:
            self.inspector_status.set('Connect to the game first.')
            return
        if getattr(self.args,'read_only',False) or not getattr(self.args,'enable_hex_edit',False):
            self.inspector_status.set('Memory writes are disabled in read-only mode.')
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
        """Never apply USA hex policies to Japanese live addresses."""
        if self.active_version.key == 'japan':
            self.inspector_status.set(
                'Japan Live is read-only; use a verified Japanese write control.')
            return
        if self.watch_tree.identify_region(event.x,event.y)!='cell':return
        if self.watch_tree.identify_column(event.x)!='#3':return
        row_id=self.watch_tree.identify_row(event.y)
        if not row_id or not self.mem:return
        if getattr(self.args,'read_only',False) or not getattr(self.args,'enable_hex_edit',False):
            messagebox.showwarning('Read-only mode','Memory editing is disabled by --read-only.')
            return
        watch=next((w for w in self.watch_rows if w.name==row_id),None)
        if watch is None or watch.addr is None:return
        policy=get_policy(watch.addr)
        spec=next((v for v in self.custom_watches if v.row_name==watch.name),None)
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
                +'\nRaw memory write (game values can change concurrently).'
                +'\nNew hex value:',initialvalue=original_hex,parent=self.root)
            if new_string is None:return
            proposed=parse_hex(new_string,width)
            if proposed==original:return
            did_write=checked_write(self.mem,watch.addr,original,proposed,
                     allow_advanced=True,raw_override=True)
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
            display=self.display_watch_name(w.name)
            if filt and filt not in (' '.join((w.name,display,w.value,w.raw,w.source,
                                   f'0x{w.addr:08X}' if w.addr is not None else ''))).lower():
                continue
            mark=(w.name,w.raw)
            tag = 'invalid' if w.status in ('CHECK','ERROR') else ('changed' if w.name in self.watch_previous and self.watch_previous[w.name]!=w.raw else '')
            self.watch_tree.insert('', 'end',iid=w.name,text=display,
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
        if self.active_version.key == 'japan':
            if self.jp_rdram is None:
                self.watch_rows=[]
                self.draw_watches()
                self.scene_live.set('Current map: —')
                self.inspector_status.set('Connect to Japan-0 RDRAM for shared Live Memory.')
                return
            import time
            now=time.monotonic()
            if now-self.last_inspect_at < 0.30:
                return
            self.last_inspect_at=now
            from practice.region_views import japan_live_watches
            try:
                rows=japan_live_watches(self.jp_rdram, self.jp_custom_watches)
                changed=sum(
                    1 for row in rows
                    if row.name in self.watch_previous
                    and self.watch_previous[row.name] != row.raw)
                self.watch_rows=rows
                self.draw_watches()
                self.watch_previous={row.name:row.raw for row in rows}
                scene=int.from_bytes(
                    self.jp_rdram.read_guest(0x800CD2A2, 2), 'big')
                self.scene_live.set(
                    f'Current map: 0x{scene:03X} '
                    f'{self.scene_catalog().get(scene, "unmapped")}')
                self.inspector_status.set(
                    f'Japan-0: {len(rows)} source-backed/custom fields; '
                    f'{changed} changed; USA-only address policies disabled.')
            except (OSError, RuntimeError, ValueError) as exc:
                self.inspector_status.set(f'Japan live inspector failed: {exc}')
            return
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
        if self.active_version.key == 'japan':
            chosen=self.scene_list.curselection()
            if not chosen:
                self.scene_status.set('Select a Japanese scene first.')
                return
            destination,_name=self.scene_options[chosen[0]]
            self.start_japan_native_scene_warp(destination=destination)
            return
        if getattr(self.args,'read_only',False):
            self.scene_status.set('Read-only mode: scene requests are disabled.')
            return
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
        if not getattr(self.args,'enable_hex_edit',False):
            self.scene_status.set('Memory writes disabled; scene reload was not sent.')
            return
        try:spawn=self.selected_scene_spawn(dest)
        except ValueError as exc:
            self.scene_status.set(str(exc));return
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
        if getattr(self.args,'read_only',False) or not self.args.enable_teleport or not self.args.enable_hex_edit:
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
        """Keep the historical entry point; use the validated entrance-reload path."""
        chosen=self.scene_list.curselection()
        if not chosen or self.scene_options[chosen[0]][0]!=mid:
            self.scene_status.set('Scene selection changed; reload was not sent.')
            return
        self.try_reload_warp()

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
        """Shared scene selection; the active ROM decides which backend runs."""
        chosen=self.scene_list.curselection()
        if not chosen:return
        mid,name=self.scene_options[chosen[0]]
        self.scene_selected=mid
        if self.active_version.key == 'japan':
            try:
                self.scene_status.set(
                    f'Japan-0 selected 0x{mid:03X} {name}. '
                    'Double-click for immediate 0x0C area reload; '
                    'no debug menu or N64 A key required.')
                self.show_japan_debug_target()
            except (ValueError, RuntimeError) as exc:
                self.scene_status.set(f'Japanese scene selection unavailable: {exc}')
            return
        self.refresh_entrance_choices(mid)
        try:
            target=native_debug_selection(mid,self.scene_catalog())
            self.scene_status.set(
                f'Selected {mid}: {name}. Native debug index: {target["label"]}. '
                'Double-click requests the guarded experimental entrance reload; the manual debug menu is a separate button.')
        except ValueError as e:
            self.scene_status.set(str(e))

    def activate_selected_scene(self,event=None):
        """Request a guarded reload for the row actually double-clicked."""
        if event is not None:
            index=self.scene_list.nearest(event.y)
            bounds=self.scene_list.bbox(index)
            if bounds is None or not (bounds[1] <= event.y < bounds[1]+bounds[3]):
                return 'break'
            self.scene_list.selection_clear(0,'end')
            self.scene_list.selection_set(index)
            self.scene_list.activate(index)
            self.select_scene()
        chosen=self.scene_list.curselection()
        if not chosen:return 'break'
        mid,name=self.scene_options[chosen[0]]
        self.request_direct_scene(mid,name)
        return 'break'

    def open_debug_for_selected_scene(self,event=None):
        """Open manual native menu for active ROM; never invoke a warp."""
        if self.active_version.key == 'japan':
            self.open_japan_debug_for_selected_scene()
            return
        if getattr(self.args,'read_only',False):
            self.scene_status.set('Read-only mode: debug-menu requests are disabled.')
            return
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
        """Explicit manual menu fallback only, never the double-click action."""
        if self.active_version.key == 'japan':
            self.open_japan_debug_for_selected_scene()
            return
        if getattr(self.args, 'read_only', False):
            self.scene_status.set('Read-only mode: debug-menu entry disabled.')
            return
        if self.mem is None or not self.args.enable_debug_menu:
            self.scene_status.set('Connect to the game before opening the debug menu.')
            return
        if self.pending_direct_warp or self.pending_restore or self.pending_native_warp:
            self.scene_status.set('Complete or cancel the pending scene request first.')
            return
        try:
            with self.value_freezes.guard:
                open_native_debug_menu(self.mem)
            self.scene_status.set('Original debug menu opened. Choose a destination in the game.')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.scene_status.set('Native debug menu entry blocked: ' + str(exc))

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
