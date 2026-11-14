"""Goemon Practice Toolkit v0.11.17 — host UI for US Goemon.

Observes original-game RDRAM state and manages position bookmarks, gameplay diagnostics
and experimental logical progression checkpoints. Memory writes
are enabled by default; --read-only disables writes and game input. This is not a savestate
and is not an in-game N64 ROM patch.
"""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import time
import tkinter as tk
import platform
import ctypes
import queue
import threading
from tkinter import ttk, messagebox, filedialog
import sys

from autosplitter.process_discovery import find_pid
from autosplitter.memory import HostProcess, Rdram, discover_rdram
from practice.checkpoints import (capture_checkpoint, restore_checkpoint,
                                  load_checkpoint_file, save_checkpoint_file)
from practice.value_freezes_ui import ValueFreezesMixin
from practice.live_speed_ui import LiveSpeedMixin
from practice.ui_extension import InspectorMixin
from practice.paths import resource_root, practice_data_dir
from practice.theme import apply_theme, PALETTE
from practice.unlocks_ui import UnlocksMixin
from practice.state_discovery_ui import StateDiscoveryMixin
from practice.value_search_ui import ValueSearchMixin
from practice.event_sessions_ui import EventSessionsMixin
from practice.story_progress_ui import StoryProgressMixin
from practice.state_discovery import measured_velocity
from practice.experimental_controls import stage_reload_trial
from practice.entrances import checkpoint_spawn
from practice.linux_pid_access import ptrace_scope, change_ptrace_scope, external_pid_hint
from practice.checkpoints import MAP_ADDR, _ensure_capture_safe, validate_checkpoint
from practice.native_character import (
    prepare_character_swap, undo_character_preparation,
    ready_after_native_swap, press_native_c_down, IDLE_ACTIONS,
)

ROOT = resource_root()
BOOKMARKS_FILE = practice_data_dir() / "bookmarks.json"
CHECKPOINTS_FILE = practice_data_dir() / "checkpoints.json"


ASSETS_DIR = ROOT / "assets"
APP_ICON_ICO = ASSETS_DIR / "goemon_tools_logo.ico"
APP_ICON_PNG = ASSETS_DIR / "goemon_tools_logo.png"
HEADER_LOGO_PNG = ASSETS_DIR / "goemon_tools_logo_small.png"


def configure_window_branding(root: tk.Tk) -> None:
    """Apply a real app identity/icon when available.

    On Windows this improves the taskbar entry so the toolkit shows its own
    icon rather than a generic Python one when launched from the source tree.
    The helper is best-effort and silently falls back if the assets or Win32
    APIs are unavailable.
    """
    try:
        if platform.system() == "Windows":
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "JakeArnold.GoemonSpeedrunTools"
                )
            except Exception:
                pass
            if APP_ICON_ICO.exists():
                try:
                    root.iconbitmap(default=str(APP_ICON_ICO))
                    return
                except Exception:
                    pass
        if APP_ICON_PNG.exists():
            try:
                icon_image = tk.PhotoImage(file=str(APP_ICON_PNG))
                root._goemon_icon_image = icon_image
                root.iconphoto(True, icon_image)
            except Exception:
                pass
    except Exception:
        pass


class Toolkit(LiveSpeedMixin, ValueFreezesMixin, StoryProgressMixin, EventSessionsMixin, ValueSearchMixin, StateDiscoveryMixin, UnlocksMixin, InspectorMixin):
    def __init__(self, root, args):
        args = apply_access_mode(args)
        self.root, self.args = root, args
        root.title("Goemon Practice Toolkit v0.11.17 · USA N64")
        root.geometry("1390x900")
        root.minsize(1100, 730)
        apply_theme(root)
        configure_window_branding(root)
        root.attributes("-topmost", False)
        self.mem, self.process = None, None
        self.game_pid = None
        self._connect_queue = queue.SimpleQueue()
        self._connecting = False
        self._linux_scope_queue = queue.SimpleQueue()
        self._linux_scope_changing = False
        self._linux_prior_scope = None
        self.pending_restore = None
        self.native_key_release = None
        self.last, self.last_t = None, None
        self.observed_velocity = None
        self.current = None
        self.bookmarks = json.loads(BOOKMARKS_FILE.read_text()) if BOOKMARKS_FILE.exists() else []
        self.checkpoints = load_checkpoint_file(CHECKPOINTS_FILE)
        self.status = tk.StringVar(value="Disconnected. Start US Goemon in Recomp or Project64, then Connect.")
        self.connection_target = tk.StringVar(value='auto')
        self.pid_text = tk.StringVar(value=str(args.pid) if args.pid else '')
        self.pos_text = tk.StringVar(value="X: —    Y: —    Z: —")
        self.speed_text = tk.StringVar(value="Speed: —")
        self.misc_text = tk.StringVar(value="Character: —   Action: —   Loading: —")
        # Branded header and first-page dashboard mirror the README concept.
        header = ttk.Frame(root, style='Header.TFrame', padding=(20, 12))
        header.pack(fill='x')
        if HEADER_LOGO_PNG.exists():
            try:
                self.header_icon = tk.PhotoImage(file=str(HEADER_LOGO_PNG))
                tk.Label(header, image=self.header_icon, bg=PALETTE['surface']).pack(side='left', padx=(0, 14))
            except tk.TclError:
                pass
        brand = ttk.Frame(header, style='Header.TFrame')
        brand.pack(side='left')
        ttk.Label(brand, text='Goemon Speedrun Tools', style='Header.TLabel').pack(anchor='w')
        ttk.Label(brand, text='PRACTICE TOOLKIT  /  SCENE BROWSER  /  LIVE MEMORY',
                  style='HeaderSub.TLabel').pack(anchor='w', pady=(4, 0))
        ttk.Label(header, text='v0.11.17  |  US Goemon · Recomp / Project64',
                  style='HeaderSub.TLabel').pack(side='right', padx=8)

        self.notebook = notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=8, pady=(0, 5))
        dashboard = ttk.Frame(notebook)
        notebook.add(dashboard, text='Dashboard')
        dash_canvas = tk.Canvas(dashboard, background=PALETTE['background'],
                                borderwidth=0, highlightthickness=0)
        dash_scroll = ttk.Scrollbar(dashboard, orient='vertical', command=dash_canvas.yview)
        dash_scroll.pack(side='right', fill='y')
        dash_canvas.pack(side='left', fill='both', expand=True)
        dash_canvas.configure(yscrollcommand=dash_scroll.set)
        frm = ttk.Frame(dash_canvas, padding=12)
        dash_window = dash_canvas.create_window((0, 0), window=frm, anchor='nw')
        frm.bind('<Configure>', lambda _e: dash_canvas.configure(scrollregion=dash_canvas.bbox('all')))
        dash_canvas.bind('<Configure>', lambda e: dash_canvas.itemconfigure(dash_window, width=e.width))
        frm.columnconfigure(0, weight=4, minsize=395)
        frm.columnconfigure(1, weight=6, minsize=475)
        frm.rowconfigure(0, weight=1)
        left = ttk.Frame(frm)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 7))
        right = ttk.Frame(frm)
        right.grid(row=0, column=1, sticky='nsew', padx=(7, 0))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        connection = ttk.LabelFrame(left, text=' Connection ', padding=12)
        connection.pack(fill='x', pady=(0, 10))
        ttk.Label(connection, textvariable=self.status, style='Card.TLabel',
                  wraplength=410).pack(anchor='w', pady=(0, 7))
        ttk.Combobox(connection, textvariable=self.connection_target, state='readonly',
                     values=('auto', 'recomp', 'project64')).pack(fill='x', pady=(0, 7))
        pid_row=ttk.Frame(connection);pid_row.pack(fill='x',pady=(0,7))
        ttk.Label(pid_row,text='PID (optional)').pack(side='left')
        ttk.Entry(pid_row,textvariable=self.pid_text,width=14).pack(side='left',padx=6)
        self.connect_button = ttk.Button(connection, text='Connect to game',
                   style='Accent.TButton', command=self.connect)
        self.connect_button.pack(fill='x', pady=(0, 7))
        if sys.platform == 'linux':
            ttk.Button(connection, text='Launch native Linux recomp',
                       command=self.launch_linux_recomp).pack(fill='x', pady=(0, 7))
            linux_access=ttk.Frame(connection)
            linux_access.pack(fill='x',pady=(0,7))
            self.linux_attach_btn=ttk.Button(
                linux_access,text='Permit connection to existing Linux PID',
                command=self.enable_linux_external_pid)
            self.linux_attach_btn.pack(side='left')
            self.linux_restore_btn=ttk.Button(
                linux_access,text='Restore original PID protection',
                command=self.restore_linux_pid_protection)
            self.linux_restore_btn.pack(side='left',padx=7)
            self.linux_restore_btn.state(['disabled'])
            ttk.Label(connection,text='Existing Linux game processes may require an OS '
                      'ptrace permission change. This affects other processes until restored.',
                      style='CardMuted.TLabel',wraplength=420).pack(anchor='w',pady=(0,7))
        ttk.Label(connection, textvariable=self.pos_text, style='AccentValue.TLabel').pack(anchor='w')
        ttk.Label(connection, textvariable=self.speed_text, style='CardMuted.TLabel').pack(anchor='w')
        ttk.Label(connection, textvariable=self.misc_text, style='CardMuted.TLabel',
                  wraplength=420).pack(anchor='w')

        self.build_live_speed_controls(left)

        checkpoints = ttk.LabelFrame(left, text=' Checkpoints and bookmarks ', padding=12)
        checkpoints.pack(fill='x', pady=(0, 10))
        ttk.Label(checkpoints, text='Name for the next saved checkpoint',
                  style='CardMuted.TLabel').pack(anchor='w')
        self.bookmark_name = ttk.Entry(checkpoints)
        self.bookmark_name.insert(0, 'Practice checkpoint')
        self.bookmark_name.pack(fill='x', pady=(4, 8))
        ttk.Label(checkpoints, text='Position bookmarks', style='Card.TLabel').pack(anchor='w')
        self.bookmarks_box = ttk.Combobox(checkpoints, state='readonly', values=self.bookmark_labels())
        self.bookmarks_box.pack(fill='x', pady=4)
        row = ttk.Frame(checkpoints, style='Card.TFrame')
        row.pack(fill='x', pady=(2, 8))
        ttk.Button(row, text='Save position', command=self.save_bookmark,
                   style='Accent.TButton').pack(side='left', fill='x', expand=True)
        self.teleport_btn = ttk.Button(row, text='Restore position', command=self.restore_bookmark)
        self.teleport_btn.pack(side='left', fill='x', expand=True, padx=(8, 0))
        if not args.enable_teleport:
            self.teleport_btn.state(['disabled'])
        ttk.Label(checkpoints, text='Logical checkpoints (experimental)',
                  style='Card.TLabel').pack(anchor='w', pady=(2, 0))
        self.checkpoints_box = ttk.Combobox(checkpoints, state='readonly', values=self.checkpoint_labels())
        self.checkpoints_box.pack(fill='x', pady=4)
        state_buttons = ttk.Frame(checkpoints, style='Card.TFrame')
        state_buttons.pack(fill='x', pady=(2, 5))
        ttk.Button(state_buttons, text='Capture checkpoint', command=self.capture_full_checkpoint,
                   style='Gold.TButton').pack(side='left', expand=True, fill='x')
        self.restore_state_btn = ttk.Button(state_buttons, text='Restore (experimental)',
                                            command=self.restore_full_checkpoint)
        self.restore_state_btn.pack(side='left', expand=True, fill='x', padx=(8, 0))
        if not args.enable_state_restore:
            self.restore_state_btn.state(['disabled'])
        self.cancel_restore_btn = ttk.Button(checkpoints, text='Cancel pending checkpoint restore',
                                             command=self.cancel_pending_restore)
        self.cancel_restore_btn.pack(fill='x', pady=(3, 0))
        self.cancel_restore_btn.state(['disabled'])

        scene_card = ttk.LabelFrame(right, text=' Scene browser ', padding=10)
        scene_card.grid(row=0, column=0, sticky='nsew', pady=(0, 6))
        scene_card.columnconfigure(0, weight=1)
        scene_card.rowconfigure(1, weight=1)
        self.quick_scene_filter = tk.StringVar()
        ttk.Entry(scene_card, textvariable=self.quick_scene_filter).grid(row=0, column=0,
                                                                sticky='ew', pady=(0, 7))
        self.quick_scene_filter.trace_add('write', lambda *_: self.draw_quick_scenes())
        scene_columns = ('map', 'name', 'category')
        self.quick_scene_tree = ttk.Treeview(scene_card, columns=scene_columns,
                                             show='headings', height=7, selectmode='browse')
        for col, label, width in [('map', 'ID', 70), ('name', 'Area / scene', 245),
                                  ('category', 'Category', 85)]:
            self.quick_scene_tree.heading(col, text=label)
            self.quick_scene_tree.column(col, width=width, stretch=(col == 'name'))
        self.quick_scene_tree.grid(row=1, column=0, sticky='nsew')
        scene_scroll = ttk.Scrollbar(scene_card, orient='vertical', command=self.quick_scene_tree.yview)
        scene_scroll.grid(row=1, column=1, sticky='ns')
        self.quick_scene_tree.configure(yscrollcommand=scene_scroll.set)
        # Single-click selects; double-click uses the same guarded reload as the full browser.
        self.quick_scene_tree.bind('<<TreeviewSelect>>', self.choose_quick_scene)
        self.quick_scene_tree.bind('<Double-1>', self.activate_quick_scene)
        footer = ttk.Frame(scene_card, style='Card.TFrame')
        footer.grid(row=2, column=0, sticky='ew', pady=(7, 0))
        ttk.Label(footer, text='Double-click an area to reload (experimental).',
                  style='CardMuted.TLabel').pack(side='left')
        ttk.Button(footer, text='Full scene browser', command=self.open_full_scene_tab).pack(side='right')

        memory_card = ttk.LabelFrame(right, text=' Live memory (read-only preview) ', padding=10)
        memory_card.grid(row=1, column=0, sticky='nsew', pady=(6, 0))
        memory_card.columnconfigure(0, weight=1)
        memory_card.rowconfigure(1, weight=1)
        ttk.Label(memory_card, text='Live values from the original N64 guest RAM',
                  style='CardMuted.TLabel').grid(row=0, column=0, sticky='w', pady=(0, 6))
        memory_columns = ('field', 'addr', 'hex')
        self.quick_watch_tree = ttk.Treeview(memory_card, columns=memory_columns,
                                            show='headings', height=7)
        for col, label, width in [('field', 'Field', 185), ('addr', 'N64 address', 112),
                                  ('hex', 'Hex', 120)]:
            self.quick_watch_tree.heading(col, text=label)
            self.quick_watch_tree.column(col, width=width, stretch=(col == 'field'))
        self.quick_watch_tree.grid(row=1, column=0, sticky='nsew')
        watch_scroll = ttk.Scrollbar(memory_card, orient='vertical', command=self.quick_watch_tree.yview)
        watch_scroll.grid(row=1, column=1, sticky='ns')
        self.quick_watch_tree.configure(yscrollcommand=watch_scroll.set)
        self.quick_watch_tree.tag_configure('changed', background=PALETTE['changed'])
        preview_footer = ttk.Frame(memory_card, style='Card.TFrame')
        preview_footer.grid(row=2, column=0, sticky='ew', pady=(7, 0))
        ttk.Label(preview_footer, text='Edit guarded fields in the full Live memory tab.',
                  style='CardMuted.TLabel').pack(side='left')
        ttk.Button(preview_footer, text='Open live memory', command=self.open_live_memory_tab).pack(side='right')
        self.draw_quick_scenes()
        self.build_inspector_tabs(notebook)
        # Show blocked requests and reload progress without opening the Scene Browser tab.
        ttk.Label(scene_card, textvariable=self.scene_status, wraplength=420,
                  style='CardMuted.TLabel').grid(row=3, column=0, columnspan=2,
                                                  sticky='ew', pady=(4, 0))
        self.build_value_freezes_tab(notebook)
        self.build_value_search_tab(notebook)
        self.build_state_discovery_tab(notebook)
        self.build_event_sessions_tab(notebook)
        self.build_unlock_tabs(notebook)
        self.build_story_progress_tab(notebook)
        # Toolkit-local F1; it does not register a system-wide/game hotkey.
        root.bind_all('<F1>', self._on_f1_open_memory, add='+')
        statusbar = ttk.Frame(root, style='Header.TFrame', padding=(16, 5))
        statusbar.pack(fill='x')
        ttk.Label(statusbar, text='EXPERIMENTAL PRACTICE ONLY  •  Never use for submitted runs',
                  style='HeaderSub.TLabel').pack(side='left')
        ttk.Label(statusbar, text=('READ ONLY' if getattr(args, 'read_only', False) else 'Memory writes enabled') + '  •  Experimental entrance reload',
                  style='HeaderSub.TLabel').pack(side='right')
        root.after(100,self.tick)

    def draw_quick_scenes(self):
        """Keep the dashboard scene catalog searchable, without guest writes."""
        from practice.scenes import SCENES
        query = self.quick_scene_filter.get().strip().lower()
        selected = self.quick_scene_tree.selection()
        self.quick_scene_tree.delete(*self.quick_scene_tree.get_children())
        for map_id, name in sorted(SCENES.items()):
            if query not in f'{map_id} {map_id:03X} {name}'.lower():
                continue
            category = 'SIRO' if map_id < 300 else ('DOUCHU' if map_id < 350 else 'MACHI / OTHER')
            self.quick_scene_tree.insert('', 'end', iid=str(map_id), values=(map_id, name, category))
        for entry in selected:
            if self.quick_scene_tree.exists(entry):
                self.quick_scene_tree.selection_set(entry)

    def choose_quick_scene(self, event=None):
        """Synchronise dashboard selection to the full browser, never mutate RAM."""
        selection = self.quick_scene_tree.selection()
        if not selection or not hasattr(self, 'scene_options'):
            return
        map_id = int(selection[0])
        for index, (candidate, _) in enumerate(self.scene_options):
            if candidate == map_id:
                self.scene_list.selection_clear(0, 'end')
                self.scene_list.selection_set(index)
                self.scene_list.see(index)
                self.select_scene()
                return
        # The full browser may have its own filter; reset it before synchronising.
        self.scene_filter.set('')
        for index, (candidate, _) in enumerate(self.scene_options):
            if candidate == map_id:
                self.scene_list.selection_set(index)
                self.scene_list.see(index)
                self.select_scene()
                break

    def activate_quick_scene(self, event=None):
        """Double-click the clicked dashboard row and reload without changing tabs."""
        if event is not None:
            row = self.quick_scene_tree.identify_row(event.y)
            if not row:
                return 'break'
            self.quick_scene_tree.selection_set(row)
        selection = self.quick_scene_tree.selection()
        if not selection:
            return 'break'
        target = int(selection[0])
        self.choose_quick_scene()
        chosen = self.scene_list.curselection()
        if not chosen or self.scene_options[chosen[0]][0] != target:
            self.scene_status.set(f'Could not select stage {target} in the Scene Browser.')
            return 'break'
        self.activate_selected_scene()
        return 'break'

    def open_full_scene_tab(self, event=None):
        self.choose_quick_scene()
        self.notebook.select(self.scene_tab)

    def open_live_memory_tab(self):
        self.notebook.select(self.live_memory_tab)

    def _on_f1_open_memory(self, _event=None):
        """Jump to the Live Memory / debug hex editor from any toolkit widget."""
        self.open_live_memory_tab()
        return 'break'

    def refresh_quick_watch(self):
        """Reflect real inspector samples; a disconnected session remains empty."""
        if not self.mem or not self.watch_rows:
            self.quick_watch_tree.delete(*self.quick_watch_tree.get_children())
            return
        priority = ('Map ID', 'Character', 'Current health (units)', 'Ryo',
                    'Lives', 'Pending destination', 'Exit request (not warp)',
                    'Native menu entry pointer', 'X', 'Y', 'Z')
        rows = {row.name: row for row in self.watch_rows}
        old = {row_id: self.quick_watch_tree.item(row_id, 'values') for row_id
               in self.quick_watch_tree.get_children()}
        self.quick_watch_tree.delete(*self.quick_watch_tree.get_children())
        for name in priority:
            value = rows.get(name)
            if not value or value.addr is None:
                continue
            fields = (self.display_watch_name(name), f'0x{value.addr:08X}', value.raw)
            tag = ('changed',) if name in old and tuple(old[name]) != fields else ()
            self.quick_watch_tree.insert('', 'end', iid=name, values=fields, tags=tag)

    def bookmark_labels(self):
        return [f"{i+1}. {x['name']} ({x['x']:.1f}, {x['y']:.1f}, {x['z']:.1f})" for i,x in enumerate(self.bookmarks)]

    def launch_linux_recomp(self):
        """Launch a user-selected native Linux build as our child for ptrace access.

        Selecting an executable does not modify game memory and is available in
        read-only mode. Flatpak sandbox boundaries may block memory access.
        """
        if sys.platform != 'linux':
            return
        selected = filedialog.askopenfilename(
            title='Select native Linux Goemon64Recompiled executable')
        if not selected:
            return
        try:
            binary = Path(selected).resolve(strict=True)
            if not binary.is_file() or not os.access(binary, os.X_OK):
                raise ValueError('Select a locally executable native Linux game binary')
            process = subprocess.Popen([str(binary)], cwd=str(binary.parent))
            self._linux_game_process = process
            self.pid_text.set(str(process.pid))
            self.connection_target.set('recomp')
            self.status.set(f'Launched native Linux game PID {process.pid}; connect once started.')
        except (OSError, ValueError) as exc:
            self.status.set(f'Linux recomp launch failed: {exc}')

    def _begin_linux_scope_change(self, value):
        """Authenticate outside the UI thread; never run Tk calls in a worker."""
        if self._linux_scope_changing:
            return
        self._linux_scope_changing=True
        self.linux_attach_btn.state(['disabled'])
        self.linux_restore_btn.state(['disabled'])
        self.status.set('Requesting OS authorization for Linux PID permission change...')
        def work():
            try:
                changed=change_ptrace_scope(value)
                self._linux_scope_queue.put(('ok',value,changed))
            except (OSError,ValueError,PermissionError,subprocess.TimeoutExpired) as exc:
                self._linux_scope_queue.put(('error',value,str(exc)))
        threading.Thread(target=work,name='GoemonLinuxPIDPermissions',daemon=True).start()
        self.root.after(100,self._poll_linux_scope_change)

    def enable_linux_external_pid(self):
        if sys.platform!='linux' or self._linux_scope_changing:
            return
        existing=ptrace_scope()
        if existing is None:
            self.status.set('Yama ptrace_scope is unavailable; check process permissions and sandbox settings.')
            return
        if existing == 0:
            self.status.set('Linux already permits normal same-user PID attachment. Connect using the game PID.')
            return
        if existing not in (1,2):
            self.status.set(f'ptrace_scope={existing} cannot be changed by this control.')
            return
        if not messagebox.askyesno(
            'Change Linux process access',
            f'Current kernel.yama.ptrace_scope={existing}. Setting it to 0 permits '
            'other same-user processes to inspect one another until restored or rebooted. '
            'Administrator authentication is required. Allow this temporary system-wide change?',
            parent=self.root):
            return
        self._linux_prior_scope=existing
        self._begin_linux_scope_change(0)

    def restore_linux_pid_protection(self):
        if sys.platform!='linux' or self._linux_scope_changing:
            return
        original=self._linux_prior_scope
        if original not in (1,2):
            self.status.set('No earlier PID protection level was recorded by this toolkit session.')
            return
        self._begin_linux_scope_change(original)

    def _poll_linux_scope_change(self):
        try:
            result=self._linux_scope_queue.get_nowait()
        except queue.Empty:
            self.root.after(100,self._poll_linux_scope_change)
            return
        self._linux_scope_changing=False
        self.linux_attach_btn.state(['!disabled'])
        if result[0]=='error':
            self.status.set('Linux PID permission change failed: '+result[2])
        elif result[1]==0:
            self.status.set('Linux external-PID access enabled for this boot. '
                            'Connect to the existing game PID; restore protection when finished.')
        else:
            self._linux_prior_scope=None
            self.status.set('Previous Linux PID protection restored.')
        if self._linux_prior_scope in (1,2) and ptrace_scope()==0:
            self.linux_restore_btn.state(['!disabled'])
        else:
            self.linux_restore_btn.state(['disabled'])

    def connect(self):
        """Start expensive process discovery in a worker, not Tk's event loop.

        Only the UI thread may touch Tk widgets. Workers own the new process
        handle until the UI takes it from the completion queue.
        """
        if self._connecting:
            return
        try:
            pid_hint = int(self.pid_text.get().strip()) if self.pid_text.get().strip() else None
            if pid_hint is not None and pid_hint <= 0:raise ValueError()
        except ValueError:
            self.status.set('Enter a valid positive PID, or leave it blank for automatic selection.')
            return
        # Complete all old-session freeze writes before closing the RAM handle.
        with self.value_freezes.guard:
            self.stop_all_freezes()
            self.cancel_pending_restore(quiet=True)
            self.pending_direct_warp = None
            self.pending_native_warp = None
            self._connecting = True
            self.connect_button.state(['disabled'])
            self.status.set('Connecting to '+(f'PID {pid_hint}' if pid_hint else 'detected game')+
                            ': discovering Goemon RAM...')
            self.mem = None
            self.current = None
            self.game_pid = None
            self.last, self.last_t = None, None
            previous = self.process
            self.process = None
            if previous is not None:
                try:
                    previous.close()
                except OSError:
                    pass
        opts = (pid_hint, self.args.base, self.args.endian,
                bool(self.args.enable_teleport or self.args.enable_state_restore or
                     self.args.enable_debug_menu or self.args.enable_scene_warp or
                     self.args.enable_hex_edit), self.connection_target.get())
        thread = threading.Thread(target=self._connect_worker, args=(opts,), daemon=True,
                                  name='GoemonRdramDiscovery')
        thread.start()
        self.root.after(50, self._poll_connect_results)

    def _connect_worker(self, opts):
        """No Tk calls here; even errors are returned through the queue."""
        pid_hint, base_hint, endian_hint, writable, target = opts
        process = None
        try:
            pid = pid_hint or find_pid(target)
            process = HostProcess(pid, writable=writable)
            if sys.platform == 'linux':
                # Fail immediately for a correct PID blocked by Linux Yama.
                # Discovery otherwise scans large readable-map ranges before
                # reporting that every process_vm_readv was denied.
                for start, size in process.regions():
                    if size < 1:
                        continue
                    try:
                        process.read(start, 1)
                    except PermissionError:
                        raise
                    except OSError:
                        continue  # Some readable maps cannot be copied by readv.
                    break
            if base_hint:
                base, endian = int(base_hint, 0) if isinstance(base_hint, str) else int(base_hint), (
                    'wordswapped' if endian_hint == 'auto' else endian_hint)
            else:
                base, endian = discover_rdram(process, endian_hint)
            candidate = Rdram(process, base, endian)
            sample = candidate.snapshot_for_monitoring()
            self._connect_queue.put(('ok', pid, process, candidate, sample, base, endian))
        except Exception as exc:
            if process is not None:
                try:
                    process.close()
                except Exception:
                    pass
            if sys.platform == 'linux' and isinstance(exc, PermissionError):
                from practice.linux_pid_access import external_pid_hint
                detail=external_pid_hint(pid if 'pid' in locals() else pid_hint or 'unknown')
                self._connect_queue.put(('error',f'{exc} {detail}'))
            else:
                self._connect_queue.put(('error', str(exc)))

    def _poll_connect_results(self):
        if not self._connecting:
            return
        try:
            result = self._connect_queue.get_nowait()
        except queue.Empty:
            self.root.after(50, self._poll_connect_results)
            return
        self._connecting = False
        self.connect_button.state(['!disabled'])
        if result[0] == 'ok':
            _, pid, process, candidate, sample, base, endian = result
            with self.value_freezes.guard:
                self.process, self.mem, self.game_pid, self.current = process, candidate, pid, sample
            if sample['x'] is None or sample['action'] is None:
                self.status.set(f'Connected PID {pid}, RAM 0x{base:X}, format {endian}; player unavailable. Memory watches remain available.')
            else:self.status.set(f'Validated PID {pid}, RAM 0x{base:X}, format {endian}. Move to verify updates.')
        else:
            with self.value_freezes.guard:
                self.process = self.mem = self.current = None
                self.game_pid = None
            self.pos_text.set('X: —    Y: —    Z: —')
            self.speed_text.set('Speed: —')
            self.misc_text.set('Character: —    Action: —    Loading: —')
            self.status.set(f'Connection failed: {result[1]}')

    def tick(self):
        if self.mem:
            try:
                now=time.monotonic()
                # During scene reload (state 0x0C), debug menus, and other
                # transitions the player object can be temporarily absent.
                # Keep the connection and read-only polling alive until gameplay.
                state=self.mem.u8(0x800C7A94)
                self.refresh_native_watch(now)
                self.poll_direct_warp(now)
                if self.pending_restore and self.pending_restore.get('phase') == 'warp':
                    self.poll_pending_restore(None, now)
                if state!=13:
                    self.current=None
                    self.last=self.last_t=None
                    self.observed_velocity=None
                    self.pos_text.set('X: —    Y: —    Z: —')
                    self.speed_text.set('Speed: —')
                    self.misc_text.set('Player unavailable in this scene')
                    self.refresh_inspector({})
                    self.refresh_unlocks()
                    self.poll_native_warp_menu(now)
                    self.root.after(170,self.tick)
                    return
                self.poll_native_warp_menu(now)
                s=self.mem.snapshot_for_monitoring()
                if s.get("player_unavailable_reason"):
                    # Impact and title/transition scenes need not expose the
                    # ordinary character, task, position, or action fields.
                    # Keep the same validated RDRAM handle for global watches.
                    self.current = None
                    self.last = self.last_t = None
                    self.observed_velocity = None
                    self.pos_text.set('X: —    Y: —    Z: —')
                    self.speed_text.set('Speed: —')
                    self.misc_text.set('Normal player unavailable; global memory is still connected')
                    self.status.set(
                        f'Connected PID {self.game_pid}; normal player unavailable: '
                        f'{s["player_unavailable_reason"]}')
                    self.cancel_pending_restore(quiet=True)
                    self.pending_direct_warp = None
                    self.pending_native_warp = None
                    self.refresh_inspector({})
                    self.refresh_unlocks()
                    self.root.after(170, self.tick)
                    return
                if self.status.get().startswith(f'Connected PID {self.game_pid}; normal player unavailable:'):
                    self.status.set(f'Connected PID {self.game_pid}; normal player restored.')
                now=time.monotonic()
                self.observed_velocity = None
                if s["x"] is not None:
                    self.pos_text.set(f"X: {s['x']:10.2f}    Y: {s['y']:10.2f}    Z: {s['z']:10.2f}")
                    if self.last is not None and self.last_t is not None and s["player_ptr"]==self.last["player_ptr"]:
                        dt=now-self.last_t
                        if dt>0:
                            velocity=measured_velocity(s,self.last,dt)
                            if velocity is not None:
                                self.observed_velocity = velocity
                                vx,vy,vz=velocity
                                magnitude=math.sqrt(vx*vx+vy*vy+vz*vz)
                                self.speed_text.set(f"Observed XYZ: ({vx:.1f}, {vy:.1f}, {vz:.1f}) u/s  |  speed: {magnitude:.1f} (derived)")
                    self.last, self.last_t=s,now
                else:
                    self.last=self.last_t=None
                    self.pos_text.set('X: —    Y: —    Z: —')
                    self.speed_text.set('Speed: —')
                self.misc_text.set(f"Character: {s['character']}    Action: {s['action']}    Loading: {s['loading']}")
                self.current=s
                self.refresh_inspector(s)
                self.refresh_unlocks()
                self.refresh_checkpoint_diff()
                if self.pending_restore and self.pending_restore.get('phase') != 'warp':
                    self.poll_pending_restore(s, now)
            except (OSError,ValueError) as e:
                self.status.set(f"Memory read failed: {e}")
                self.cancel_pending_restore(quiet=True)
                self.mem=None
        if not self.mem:
            self.refresh_unlocks(force=True)
        self.root.after(170,self.tick)

    def save_bookmark(self):
        s=self.current
        if not s or s["x"] is None:
            messagebox.showerror("Not connected","Read a valid player position first")
            return
        entry={"name":self.bookmark_name.get() or "Checkpoint",
               "x":s["x"],"y":s["y"],"z":s["z"],"character":s["character"],
               "action":s["action"],
               "map_id":self.mem.u16(0x800C7AB2) if self.mem else None}
        self.bookmarks.append(entry)
        BOOKMARKS_FILE.write_text(json.dumps(self.bookmarks,indent=2)+"\n")
        self.bookmarks_box["values"]=self.bookmark_labels()
        self.bookmarks_box.current(len(self.bookmarks)-1)
        self.status.set(f"Saved bookmark: {entry['name']}")

    def restore_bookmark(self):
        idx=self.bookmarks_box.current()
        if not self.args.enable_teleport or idx<0 or not self.mem or not self.current:
            return
        b=self.bookmarks[idx]
        if self.current["loading"] or self.current["x"] is None:
            messagebox.showerror("Blocked","Restore only in stable gameplay")
            return
        if self.current["character"]!=b["character"]:
            messagebox.showerror("Blocked","Bookmark character doesn't match the active character")
            return
        if b.get("map_id") is None:
            messagebox.showerror("Blocked","Legacy bookmark has no recorded map ID. Recapture this bookmark in v0.4 before restoring.")
            return
        if self.mem.u16(0x800C7AB2)!=b["map_id"]:
            messagebox.showerror("Blocked","Bookmark map differs. Use the original debug menu to reach that map first.")
            return
        if not messagebox.askyesno("Practice teleport",
                "This writes N64 object coordinates and can softlock, crash, or corrupt game state. "
                "It does not restore the full scene or physics state. Use only within the same room. Continue?"):
            return
        try:
            obj=self.current["player_ptr"]
            if not obj: raise ValueError("No player object")
            for i,k in enumerate(("x","y","z")):
                self.mem.write_f32(obj+8+i*4,float(b[k]))
            self.status.set(f"Moved to saved coordinates: {b['name']} (practice mode only)")
        except Exception as e:
            messagebox.showerror("Teleport failed",str(e))

    def checkpoint_labels(self):
        labels=[]
        for i, cp in enumerate(self.checkpoints):
            p=cp["payload"]
            stats=p["summary"]
            labels.append(f"{i+1}. {p['name']} (map {p['map_id']}, {stats['health']}/{stats['max_health']} HP, {stats['ryo']} Ryo, {stats['lives']} lives)")
        return labels

    def capture_full_checkpoint(self):
        if not self.mem or not self.current:
            messagebox.showerror("Not connected","Connect to the game first")
            return
        try:
            cp=capture_checkpoint(self.mem,self.bookmark_name.get())
            self.checkpoints.append(cp)
            save_checkpoint_file(CHECKPOINTS_FILE,self.checkpoints)
            self.checkpoints_box["values"]=self.checkpoint_labels()
            self.checkpoints_box.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_options()
            self.diff_cp.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_diff(force=True)
            self.status.set("Captured original N64 progress flags, stats, unlocks and position. Experimental in-room restore available.")
        except Exception as e:
            messagebox.showerror("Checkpoint capture blocked",str(e))

    def _restore_now(self, checkpoint):
        """Original logical restore; the game has already finished any native swap."""
        summary=restore_checkpoint(self.mem,checkpoint)
        self.last=None
        self.last_t=None
        p=checkpoint['payload']
        self.status.set(f"Restored logical checkpoint: {p['name']} | "
                        f"{summary['health']}/{summary['max_health']} HP, "
                        f"{summary['ryo']} Ryo, {summary['lives']} lives. Verify in-game.")
        self.refresh_checkpoint_diff(force=True)

    def _release_native_key(self):
        release=self.native_key_release
        self.native_key_release=None
        if release is not None:
            try:release()
            except Exception:pass

    def cancel_pending_restore(self, quiet=False):
        pending=self.pending_restore
        self.pending_restore=None
        self._release_native_key()
        if getattr(self,'cancel_restore_btn',None):self.cancel_restore_btn.state(['disabled'])
        if getattr(self,'restore_state_btn',None) and self.args.enable_state_restore:
            self.restore_state_btn.state(['!disabled'])
        if pending and self.mem:
            try:
                note=undo_character_preparation(self.mem,pending.get('party_patch'),
                                                pending['checkpoint']['payload']['character'])
                if not quiet:self.status.set('Checkpoint restore cancelled; '+note)
            except (OSError,ValueError) as exc:
                if not quiet:self.status.set(f'Cancelled; temporary party state could not be reverted: {exc}')
        elif pending and not quiet:
            self.status.set('Checkpoint restore cancelled')

    def _request_native_character_swap(self, pending, now):
        if getattr(self.args, 'read_only', False):
            return
        # Optional host adapter for the *original game's* C-Down switch. Never
        # modify the global/per-task character ID or bypass its model loader.
        pending['last_press']=now
        pending['attempts']+=1
        try:
            self.native_key_release=press_native_c_down(self.game_pid)
            self.root.after(180,self._release_native_key)
            self.status.set(f"Native C-Down sent ({pending['attempts']}/4); "
                            f"waiting for game to rebuild character {pending['target']}.")
        except (OSError,RuntimeError) as exc:
            pending['manual_only']=True
            self.status.set(f"Automatic C-Down unavailable: {exc}. "
                            f"Switch to character {pending['target']} in-game; restore will finish automatically.")

    def _finish_pending_restore(self, checkpoint):
        self._restore_now(checkpoint)
        self.pending_restore = None
        self.cancel_restore_btn.state(['disabled'])
        self.restore_state_btn.state(['!disabled'])

    def _arm_character_restore(self, checkpoint, now):
        """After the correct scene is loaded, swap using the native C-Down path."""
        patch = prepare_character_swap(self.mem, checkpoint)
        p = checkpoint['payload']
        self.pending_restore = dict(checkpoint=checkpoint, target=p['character'],
            party_patch=patch, phase='character', started=now,
            last_press=0.0, attempts=0, stable=0, manual_only=False)
        self.restore_state_btn.state(['disabled'])
        self.cancel_restore_btn.state(['!disabled'])
        self.status.set(f'Saved map loaded; switching natively to character {p["character"]}.')

    def _poll_cross_area_restore(self, pending, now):
        """Do not write saved coordinates until target scene has finished loading."""
        p = pending['checkpoint']['payload']
        if now-pending['started'] > 30:
            self.cancel_pending_restore(quiet=True)
            self.status.set('Checkpoint warp timed out. No checkpoint bytes/coordinates restored.')
            return
        current_map = self.mem.u16(MAP_ADDR)
        state = self.mem.u8(0x800C7A94)
        if current_map != p['map_id']:
            # Other map IDs during transition are possible. If ordinary
            # gameplay has resumed on the wrong map, stop rather than write.
            if now-pending['started'] > 2 and state == 13 and current_map != pending['source_map']:
                self.cancel_pending_restore(quiet=True)
                self.status.set(f'Checkpoint warp reached map {current_map}, not saved map {p["map_id"]}; cancelled.')
            return
        if state != 13:
            pending['stable'] = 0
            return
        try:
            snap = _ensure_capture_safe(self.mem)
        except (ValueError, OSError):
            pending['stable'] = 0  # Normal while the new map initializes.
            return
        if snap.get('action') not in IDLE_ACTIONS:
            pending['stable'] = 0
            return
        if snap['player_ptr'] != pending.get('stable_player'):
            pending['stable_player'] = snap['player_ptr']
            pending['stable'] = 0
        pending['stable'] += 1
        # Map ID can be committed before the actor has finished loading.
        if now - pending['started'] < 0.75 or pending['stable'] < 3:
            return
        try:
            if snap['character'] != p['character']:
                self._arm_character_restore(pending['checkpoint'], now)
            else:
                self._finish_pending_restore(pending['checkpoint'])
        except Exception as exc:
            # A partial multi-region write is NEVER retried automatically.
            self.cancel_pending_restore(quiet=True)
            self.status.set(f'Cross-area checkpoint write failed: {exc}; no automatic retry.')

    def poll_pending_restore(self, snapshot, now=None):
        """Two-stage cross-area restore; existing native character swap stays intact."""
        pending=self.pending_restore
        if not pending or not self.mem:return
        if now is None:now=time.monotonic()
        if pending.get('phase') == 'warp':
            self._poll_cross_area_restore(pending,now)
            return
        if now-pending['started']>45:
            self.cancel_pending_restore()
            self.status.set('Character swap timed out after 45 seconds; checkpoint not restored.')
            return
        try:
            p=pending['checkpoint']['payload']
            if self.mem.u16(MAP_ADDR)!=p['map_id']:
                self.cancel_pending_restore()
                self.status.set('Map changed during character swap. Restore cancelled to avoid writing into wrong scene.')
                return
            if snapshot['character']==pending['target']:
                if ready_after_native_swap(self.mem,pending['checkpoint']):
                    pending['stable']+=1
                    if pending['stable']>=3:
                        try:
                            self._finish_pending_restore(pending['checkpoint'])
                        except Exception as exc:
                            self.cancel_pending_restore(quiet=True)
                            self.status.set(f'Native swap completed, but checkpoint write failed: {exc}')
                            messagebox.showerror('Logical restore failed',str(exc))
                        return
                else:
                    pending['stable']=0
                    self.status.set(f"Character {pending['target']} selected; "
                                    'waiting for native model/texture swap to finish.')
                return
            pending['stable']=0
            if snapshot['action'] not in IDLE_ACTIONS or snapshot['loading']:
                self.status.set('Waiting for character-swap animation / ordinary gameplay to finish.')
                return
            if (not pending['manual_only'] and pending['attempts']<4 and
                    now-pending['last_press']>=2.0 and self.native_key_release is None):
                self._request_native_character_swap(pending,now)
            elif pending['attempts']>=4:
                pending['manual_only']=True
                self.status.set('Could not reach saved character automatically. '
                                f"Switch to character {pending['target']} in-game; restore is armed.")
        except (OSError,ValueError) as exc:
            pending['stable']=0
            self.status.set(f'Waiting for safe native character state: {exc}')

    def restore_full_checkpoint(self):
        i=self.checkpoints_box.current()
        if not self.args.enable_state_restore or i<0 or not self.mem or not self.current:return
        if self.pending_restore:
            self.status.set('A checkpoint restore is already pending; cancel it first.')
            return
        if self.pending_direct_warp or self.pending_native_warp:
            self.status.set('Finish or cancel the scene request before restoring a checkpoint.')
            return
        cp=self.checkpoints[i]
        p=cp['payload']
        try:
            validate_checkpoint(cp)
            before=_ensure_capture_safe(self.mem)
            current_map=self.mem.u16(MAP_ADDR)
        except Exception as exc:
            messagebox.showerror('Logical restore failed',str(exc))
            return
        cross_area=current_map != p['map_id']
        message=('Reload the game into saved map ' + str(p['map_id']) + ', then restore saved XYZ, rotation, resources and progression?'
                 if cross_area else 'Restore saved XYZ, rotation, resources and progression in this map?')
        if not messagebox.askyesno('EXPERIMENTAL checkpoint restore (practice only)',
             message + '\n\nIf the saved character differs, the toolkit will use native C-Down or wait for manual switching.'
             '\nThis is NOT a native savestate: actors, active scripts, physics and camera are not restored.'
             '\nSaved entrance coordinates are staged before reload. The transition remains experimental; use a backup save. Continue?'):
            return
        try:
            if cross_area:
                # The saved map is known to exist because we captured it in
                # a stable game session. Stage native pending coordinates before
                # reload; restore exact float XYZ only after the new player is ready.
                stage_reload_trial(self.mem,p['map_id'],{p['map_id']:'Checkpoint saved map'},spawn=checkpoint_spawn(cp))
                self.pending_restore=dict(checkpoint=cp, target=p['character'],
                    phase='warp',source_map=current_map,source_player=before['player_ptr'],
                    party_patch=None,started=time.monotonic(),stable=0,stable_player=None)
                self.restore_state_btn.state(['disabled'])
                self.cancel_restore_btn.state(['!disabled'])
                self.status.set(f'Reloading map {p["map_id"]} for checkpoint; waiting for stable gameplay.')
            elif before['character']==p['character']:
                self._restore_now(cp)
            else:
                self._arm_character_restore(cp,time.monotonic())
                self.poll_pending_restore(before)
        except Exception as exc:
            self.cancel_pending_restore(quiet=True)
            messagebox.showerror('Logical restore failed',str(exc))



PRACTICE_OPTIONS = ('enable_teleport', 'enable_state_restore', 'enable_debug_menu', 'enable_hex_edit')


def apply_access_mode(args):
    """Practice controls are write-enabled unless explicitly read-only."""
    if getattr(args, 'read_only', False):
        for name in (*PRACTICE_OPTIONS, 'enable_scene_warp'):
            setattr(args, name, False)
    return args


def parse_args(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pid",type=int)
    ap.add_argument("--base",help="RDRAM host base 0x...; bypasses experimental auto-discovery")
    ap.add_argument("--endian",choices=["auto","wordswapped","big"],default="auto")
    ap.add_argument("--read-only",action="store_true",help="Disable game writes and game input; overrides all enable flags")
    ap.add_argument("--linux-enable-writes",action="store_true",
                    help=argparse.SUPPRESS)  # Deprecated no-op; writes already enabled
    ap.add_argument("--enable-teleport",action="store_true",default=True,help="Write game coordinates (enabled by default)")
    ap.add_argument("--enable-state-restore",action="store_true",default=True,help="Restore logical checkpoints (enabled by default)")
    ap.add_argument("--enable-debug-menu",action="store_true",default=True,help="Allow original debug menu (enabled by default)")
    ap.add_argument("--enable-hex-edit",action="store_true",default=True,help="Allow raw hex editing (enabled by default)")
    ap.add_argument("--enable-scene-warp",action="store_true",help="DISABLED: v0.9.7 direct scene writes triggered title screen; never used")
    return apply_access_mode(ap.parse_args(argv))


def main(argv=None):
    args=parse_args(argv)
    root=tk.Tk(); app=Toolkit(root,args)
    try:
        root.mainloop()
    finally:
        app._stop_freeze_worker()
        app.stop_transition_trace()
        app.cancel_pending_restore(quiet=True)
        if getattr(app,'native_key_release',None):app._release_debug_key()
        if app.process: app.process.close()

if __name__=="__main__": main()
