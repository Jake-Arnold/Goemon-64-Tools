"""Goemon Practice Toolkit — USA/Japan native and emulator guest RAM.

Observes original-game RDRAM state and manages gameplay diagnostics and
experimental logical checkpoints (including saved position and orientation). Memory writes
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
import struct
from tkinter import ttk, messagebox, filedialog
import sys

from autosplitter.process_discovery import find_pid
from autosplitter.memory import HostProcess, Rdram, discover_rdram
from practice.checkpoints import (capture_checkpoint, restore_checkpoint,
                                  load_checkpoint_file, save_checkpoint_file)
from practice.native_checkpoints import (
    load_named_checkpoints, save_named_checkpoints,
    make_named_checkpoint, upsert_named_checkpoint, label_named_checkpoint,
    japan_checkpoint_summary,
)
from practice.reports_ui import ReportsMixin
from practice.value_freezes_ui import ValueFreezesMixin
from practice.damage_event_capture_ui import DamageEventCaptureMixin
from practice.ui_extension import InspectorMixin
from practice.paths import resource_root, practice_data_dir
from practice.game_versions import VERSIONS, selected_version, verify_selected_rom
from practice.region_session import active_session
from practice.version import DISPLAY_VERSION
from practice.updater_ui import UpdaterMixin
from practice.launcher_preferences import load_last_region, save_last_region
from practice.japan_auto_attach import (
    JapanProcessCandidate, list_japan_processes, connect_candidate_ram,
    describe_verified_connections, remember_verified_connection,
)
from practice.japan_native_recomp import (
    verified_japan_recomp_pid, find_japan_recomp_pid,
    discover_japan_recomp_rdram, validate_japan_recomp_writer,
)
from practice.remembered_rom import remember_verified_rom, load_remembered_rom
from practice.japan_native_scene_warp import (
    is_japan_scene_loaded, japan_scene_readiness,
)
from practice.japan_direct_scene_reload import (
    JAPAN_DIRECT_RELOAD_MODE, stage_japan_direct_reload,
)
from practice.japan_warp_spawns import (
    load_japan_spawns, save_japan_spawn, capture_current_japan_spawn,
    position_difference,
)
from practice.japan_spawn_placement import place_japan_spawn_once
from practice.scenes import SCENES
from practice.emulator_savestates import find_emulator_pid, verified_emulator_pid, send_state_command
from practice.japanese_mupen_attach import (
    verified_japan_probes, discover_japanese_mupen_rdram,
    validate_rdram_base, AmbiguousJapaneseRdram,
)
from practice.japanese_fields_ui import JapaneseFieldsUi
from practice.region_unlocks import japan_unlock_lead, write_japan_unlock
from practice.japanese_position import (
    JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE, JAPAN_SCENE_INDEX,
    JAPAN_OEDO_SOUTH_SCENE, JAPAN_CHARACTER_INDEX,
    checked_japan_xyz, read_japan_position, move_japan_goemon_oedo_south,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE, JAPAN_DEBUG_CHARACTER,
    JAPAN_NATIVE_DEBUG_MODE,
    debug_menu_selection_hint, get_japan_debug_context,
    enter_japan_native_debug_menu,
)
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
NATIVE_CHECKPOINTS_FILE = practice_data_dir() / "native-state-bookmarks.json"


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


class Toolkit(UpdaterMixin, ReportsMixin, JapaneseFieldsUi, DamageEventCaptureMixin, ValueFreezesMixin, StoryProgressMixin, EventSessionsMixin, ValueSearchMixin, StateDiscoveryMixin, UnlocksMixin, InspectorMixin):
    def __init__(self, root, args):
        args = apply_access_mode(args)
        self.root, self.args = root, args
        self.active_version = selected_version(
            getattr(args, 'game_version', 'usa') or load_last_region())
        self.game_version_choice = tk.StringVar(value=self.active_version.label)
        self.verified_rom_path = (
            load_remembered_rom('japan')
            if self.active_version.key == 'japan' else None)
        root.title(f"Goemon Practice Toolkit {DISPLAY_VERSION} · {self.active_version.label}")
        # Fit the initial window to the usable desktop instead of forcing
        # a 790px-tall viewport that hides the lower Dashboard controls.
        # Every page still scrolls on smaller monitors.
        screen_width = max(1, root.winfo_screenwidth())
        screen_height = max(1, root.winfo_screenheight())
        width = max(780, min(1480, screen_width - 80))
        height = max(600, min(950, screen_height - 100))
        left = max(0, (screen_width - width) // 2)
        top = max(0, (screen_height - height) // 3)
        root.geometry(f"{width}x{height}+{left}+{top}")
        root.minsize(min(940, width), min(620, height))
        apply_theme(root)
        configure_window_branding(root)
        root.attributes("-topmost", False)
        self.mem, self.process = None, None
        self.game_pid = None
        self.jp_rdram = None  # Region-verified Japan-0 RDRAM (recomp/emulator)
        self._connect_queue = queue.SimpleQueue()
        self._connecting = False
        self._linux_scope_queue = queue.SimpleQueue()
        self._linux_scope_changing = False
        self._linux_prior_scope = None
        self.pending_restore = None
        self.native_key_release = None
        self.jp_auto_warp = None
        self.jp_native_key_release = None
        self.jp_warp_spawns = load_japan_spawns()
        self.last, self.last_t = None, None
        self.observed_velocity = None
        self.current = None
        # Legacy position-only bookmarks are presented in the same selector but
        # never misrepresented or rewritten as full progression checkpoints.
        self.legacy_bookmarks = json.loads(BOOKMARKS_FILE.read_text()) if BOOKMARKS_FILE.exists() else []
        self.checkpoints = load_checkpoint_file(CHECKPOINTS_FILE)
        # A named native state is a local label for an emulator slot, never
        # a copy of its savestate bytes. Corrupt metadata must not prevent boot.
        try:
            self.named_native_checkpoints = load_named_checkpoints(
                NATIVE_CHECKPOINTS_FILE)
        except (OSError, ValueError):
            self.named_native_checkpoints = []
        self.status = tk.StringVar(value="Disconnected. Start USA Goemon in Recomp or Project64, then Connect.")
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
        self.version_heading = tk.StringVar(value=f'{DISPLAY_VERSION}  |  {self.active_version.label}')
        ttk.Label(header, textvariable=self.version_heading,
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
        def resize_dashboard(event):
            dash_canvas.itemconfigure(dash_window, width=event.width)
            self._arrange_dashboard(event.width)
        dash_canvas.bind('<Configure>', resize_dashboard)
        self.dashboard_canvas = dash_canvas
        self.dashboard_frame = frm
        self.dashboard_wide = None
        frm.columnconfigure(0, weight=1)
        left = ttk.Frame(frm)
        left.grid(row=0, column=0, sticky='new', padx=(6, 6))
        right = ttk.Frame(frm)
        right.grid(row=0, column=1, sticky='new', padx=(6, 6))
        self.dashboard_connection_column = left
        self.dashboard_checkpoints_column = right

        connection = ttk.LabelFrame(left, text=' Connection ', padding=10)
        connection.pack(fill='x', pady=(0, 6))
        ttk.Label(connection, textvariable=self.status, style='Card.TLabel',
                  wraplength=410).pack(anchor='w', pady=(0, 7))
        version_row = ttk.Frame(connection)
        version_row.pack(fill='x', pady=(0, 7))
        ttk.Label(version_row, text='Game version').pack(side='left', padx=(0, 8))
        self.version_selector = ttk.Combobox(
            version_row, textvariable=self.game_version_choice, state='readonly',
            values=tuple(version.label for version in VERSIONS.values()), width=23)
        self.version_selector.pack(side='left', fill='x', expand=True)
        self.version_selector.bind('<<ComboboxSelected>>', self.on_game_version_changed)
        ttk.Combobox(connection, textvariable=self.connection_target, state='readonly',
                     values=('auto', 'recomp', 'project64', 'mupen64plus')).pack(fill='x', pady=(0, 7))
        pid_row=ttk.Frame(connection);pid_row.pack(fill='x',pady=(0,7))
        ttk.Label(pid_row,text='PID (optional)').pack(side='left')
        ttk.Entry(pid_row,textvariable=self.pid_text,width=14).pack(side='left',padx=6)
        self.jp_base_row = ttk.Frame(connection)
        ttk.Label(self.jp_base_row, text='Japanese RAM base').pack(side='left')
        self.jp_base_choice = tk.StringVar(value='Auto (detect)')
        self.jp_base_selector = ttk.Combobox(
            self.jp_base_row, textvariable=self.jp_base_choice, state='readonly',
            values=('Auto (detect)',), width=31)
        self.jp_base_selector.pack(side='left', fill='x', expand=True, padx=(7, 0))
        self.jp_base_row.pack(fill='x', pady=(0, 7))
        self.jp_candidates = {}
        self.jp_candidates_pid = None
        self.jp_candidates_backend = None
        self.jp_backend = None
        self._jp_reconnect_enabled = False  # only after successful JP Auto attach
        self._jp_process_birth = None      # psutil PID creation time, prevents reuse
        self._jp_last_liveness_check = 0.0
        self._jp_last_auto_attempt = 0.0
        self.connect_button = ttk.Button(connection, text='Connect to game',
                   style='Accent.TButton', command=self.connect)
        self.connect_button.pack(fill='x', pady=(0, 7))
        if sys.platform == 'linux':
            self.launch_recomp_button = ttk.Button(
                connection, text='Launch native Linux recomp',
                command=self.launch_linux_recomp)
            self.launch_recomp_button.pack(fill='x', pady=(0, 7))
            linux_access=ttk.Frame(connection)
            linux_access.pack(fill='x',pady=(0,7))
            self.linux_attach_btn=ttk.Button(
                linux_access,text='Permit existing Linux PID',
                command=self.enable_linux_external_pid)
            self.linux_attach_btn.pack(side='left')
            self.linux_restore_btn=ttk.Button(
                linux_access,text='Restore PID protection',
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
        self.build_update_controls(left)

        state_card = ttk.LabelFrame(right, text=' Full emulator savestates ', padding=10)
        state_card.pack(fill='x', pady=(0, 6))
        ttk.Label(state_card, text='Complete states are saved by Project64 or Mupen64Plus. '
                  'Goemon64Recomp does not support full savestates.',
                  style='CardMuted.TLabel', wraplength=430).pack(anchor='w', pady=(0, 7))
        slot_row = ttk.Frame(state_card)
        slot_row.pack(fill='x', pady=(0, 7))
        ttk.Label(slot_row, text='Save slot').pack(side='left', padx=(0, 8))
        self.savestate_slot = tk.StringVar(value='0')
        self.savestate_slot_box = ttk.Combobox(
            slot_row, textvariable=self.savestate_slot, width=5, state='readonly',
            values=tuple(str(i) for i in range(10)))
        # ttk's readonly Combobox can expose an empty displayed selection on
        # certain native Windows Tk versions despite StringVar(value='0').
        # Explicitly choose index 0 so the displayed slot and backend agree.
        self.savestate_slot_box.current(0)
        self.savestate_slot_box.pack(side='left')
        native_buttons = ttk.Frame(state_card)
        native_buttons.pack(fill='x')
        self.native_save_btn = ttk.Button(native_buttons, text='Save full state',
                                          command=lambda: self.native_savestate_action('save'),
                                          style='Gold.TButton')
        self.native_save_btn.pack(side='left', fill='x', expand=True)
        self.native_load_btn = ttk.Button(native_buttons, text='Load full state',
                                          command=lambda: self.native_savestate_action('load'))
        self.native_load_btn.pack(side='left', fill='x', expand=True, padx=(8, 0))
        if getattr(args, 'read_only', False):
            self.native_save_btn.state(['disabled'])
            self.native_load_btn.state(['disabled'])

        # Japan-0 named checkpoints are references to emulator-owned full
        # save slots, NOT USA logical RAM checkpoints.
        named = ttk.Frame(state_card)
        named.pack(fill='x', pady=(7, 0))
        self.named_native_frame = named
        ttk.Label(
            named, text='Named Japanese state slots (emulator owns the saves)',
            style='CardMuted.TLabel').pack(anchor='w')
        name_row = ttk.Frame(named)
        name_row.pack(fill='x', pady=(3, 3))
        self.named_native_name = tk.StringVar(value='Practice checkpoint')
        ttk.Entry(name_row, textvariable=self.named_native_name,
                  width=26).pack(side='left', fill='x', expand=True)
        self.named_native_save_btn = ttk.Button(
            name_row, text='Save named slot',
            command=self.save_named_native_checkpoint)
        self.named_native_save_btn.pack(side='left', padx=(6, 0))
        choice_row = ttk.Frame(named)
        choice_row.pack(fill='x')
        self.named_native_choice = tk.StringVar()
        self.named_native_selector = ttk.Combobox(
            choice_row, textvariable=self.named_native_choice,
            state='readonly', width=33)
        self.named_native_selector.pack(side='left', fill='x', expand=True)
        self.named_native_load_btn = ttk.Button(
            choice_row, text='Load named slot',
            command=self.load_named_native_checkpoint)
        self.named_native_load_btn.pack(side='left', padx=(6, 0))
        self._named_native_visible = []
        self.connection_target.trace_add(
            'write', lambda *_: self.refresh_named_native_checkpoints())
        if self.active_version.key != 'japan':
            named.pack_forget()
        self.refresh_named_native_checkpoints()

        # Read-only diagnostics coexist with direct mapped Japanese unlock edits.
        jp_card = ttk.LabelFrame(right, text=' Japanese guest RAM (recomp / emulators) ', padding=10)
        self.jp_card = jp_card
        jp_card.pack(fill='x', pady=(0, 6))
        ttk.Label(jp_card, text='Verify Japan-0 ROM; select recomp, project64 (Windows or Wine/Linux) or mupen64plus, '
                  'then Connect. Only raw N64 bytes are exposed; USA pointers, '
                  'USA checkpoints and USA RAM editors remain disabled. '
                  'Mapped Japanese unlocks write directly in the shared Unlocks tab.',
                  style='CardMuted.TLabel', wraplength=420).pack(anchor='w', pady=(0, 7))
        jp_inputs = ttk.Frame(jp_card)
        jp_inputs.pack(fill='x')
        self.jp_read_address = tk.StringVar(value='0x80000450')
        self.jp_read_length = tk.StringVar(value='16')
        ttk.Label(jp_inputs, text='Address').pack(side='left')
        ttk.Entry(jp_inputs, textvariable=self.jp_read_address, width=15).pack(side='left', padx=5)
        ttk.Label(jp_inputs, text='Bytes').pack(side='left')
        ttk.Entry(jp_inputs, textvariable=self.jp_read_length, width=5).pack(side='left', padx=5)
        self.jp_read_button = ttk.Button(jp_inputs, text='Read', command=self.read_japan_rdram)
        self.jp_read_button.pack(side='left', padx=5)
        self.jp_read_button.state(['disabled'])
        self.jp_read_result = tk.StringVar(value='Japanese guest RAM is not connected.')
        ttk.Label(jp_card, textvariable=self.jp_read_result,
                  style='CardMuted.TLabel', wraplength=420).pack(anchor='w', pady=(7, 0))

        # Retain existing logical checkpoint code/data but hide its incomplete
        # snapshot controls so the dashboard presents only native full states.
        checkpoints = ttk.LabelFrame(right, text=' Legacy logical checkpoints ', padding=10)
        checkpoints.pack(fill='x', pady=(0, 6))
        ttk.Label(checkpoints, text='Includes saved position, orientation, health, lives, Ryo, items and progression.',
                  style='CardMuted.TLabel',wraplength=430).pack(anchor='w',pady=(0,7))
        ttk.Label(checkpoints, text='Name for new checkpoint',style='CardMuted.TLabel').pack(anchor='w')
        self.checkpoint_name = ttk.Entry(checkpoints)
        self.checkpoint_name.insert(0, 'Practice checkpoint')
        self.checkpoint_name.pack(fill='x', pady=(4, 8))
        ttk.Label(checkpoints, text='Saved checkpoints',style='Card.TLabel').pack(anchor='w')
        self.checkpoints_box = ttk.Combobox(checkpoints, state='readonly', values=self.checkpoint_labels())
        self.checkpoints_box.pack(fill='x', pady=4)
        state_buttons = ttk.Frame(checkpoints, style='Card.TFrame')
        state_buttons.pack(fill='x', pady=(2, 5))
        self.capture_state_btn = ttk.Button(state_buttons, text='Capture logical checkpoint',
                                            command=self.capture_full_checkpoint,style='Gold.TButton')
        self.capture_state_btn.pack(side='left', expand=True, fill='x')
        self.restore_state_btn = ttk.Button(state_buttons, text='Restore selected checkpoint',
                                            command=self.restore_full_checkpoint)
        self.restore_state_btn.pack(side='left', expand=True, fill='x', padx=(8, 0))
        if not (args.enable_state_restore or args.enable_teleport):
            self.restore_state_btn.state(['disabled'])
        self.cancel_restore_btn = ttk.Button(checkpoints, text='Cancel pending checkpoint restore',
                                             command=self.cancel_pending_restore)
        self.cancel_restore_btn.pack(fill='x', pady=(3, 0))
        self.cancel_restore_btn.state(['disabled'])
        ttk.Label(checkpoints,text='Older position bookmarks appear here as position-only; '
                  'they cannot restore health, items or progression.',style='CardMuted.TLabel',
                  wraplength=430).pack(anchor='w',pady=(6,0))
        self.legacy_checkpoint_card = checkpoints
        checkpoints.pack_forget()

        # The dedicated tabs are visible directly above; no duplicate footer is needed.
        self._arrange_dashboard(1220)
        self.build_inspector_tabs(notebook)
        self.build_value_freezes_tab(notebook)
        # Shared research workspace: preserve all scanners and event algorithms
        # while consolidating their formerly scattered top-level navigation.
        discovery = ttk.Frame(notebook, padding=7)
        notebook.add(discovery, text='Memory discovery')
        self.discovery_tab = discovery
        connection_bar = ttk.Frame(discovery)
        connection_bar.pack(fill='x', pady=(0, 7))
        self.discovery_connection_state = tk.StringVar(
            value='Checking game connection...')
        ttk.Label(connection_bar, textvariable=self.discovery_connection_state,
                  wraplength=970).pack(side='left', fill='x', expand=True)
        ttk.Button(connection_bar, text='Open connection',
                   command=lambda: self.notebook.select(
                       self.notebook.tabs()[0])).pack(side='right')
        self.discovery_tabs = ttk.Notebook(discovery)
        self.discovery_tabs.pack(fill='both', expand=True)
        # A single entry point answers "which experiment should I use?".
        # All four research modes are siblings, never nested in each other.
        discovery_home = ttk.Frame(self.discovery_tabs, padding=14)
        self.discovery_tabs.add(discovery_home, text="Start here")
        ttk.Label(discovery_home, text="What are you trying to find?",
                  font=("Segoe UI Semibold", 17)).pack(anchor="w", pady=(4, 7))
        ttk.Label(discovery_home, text=(
            "All methods work on the selected USA or Japanese game. "
            "Every method has a Save report button and exports the same "
            "four-file evidence package. None of these searches edits RAM."),
            wraplength=900).pack(anchor="w", pady=(0, 14))
        self.build_value_search_tab(self.discovery_tabs)
        self.build_state_discovery_tab(self.discovery_tabs)
        self.build_event_sessions_tab(self.discovery_tabs)
        self.build_damage_event_capture_tab(self.discovery_tabs)
        method_cards = (
            ("Find a known or unknown value",
             "Find health, Ryo, coordinates, floats, or text. Narrow matches "
             "with Exact/Changed/Unchanged filters; optionally repeat.",
             self.value_search_tab),
            ("Compare memory before and after",
             "Capture A before an action, B after, optionally C after reverting. "
             "Best for temporary values, movement, menus and scene changes.",
             self.state_discovery_tab),
            ("Find event and unlock flags",
             "Repeat an event with before/after and idle/control trials. "
             "Best for persistent story and inventory bits in a chosen 100-byte region.",
             self.event_sessions_tab),
            ("Record damage automatically",
             "Start a recording, take damage in-game, repeat the hit and "
             "rank candidate changes around the damage event.",
             self.damage_capture_tab),
        )
        for title, explanation, target in method_cards:
            card = ttk.LabelFrame(discovery_home, text=title, padding=10)
            card.pack(fill="x", pady=(0, 9))
            ttk.Label(card, text=explanation, wraplength=720).pack(
                side="left", fill="x", expand=True, padx=(0, 10))
            ttk.Button(card, text="Open tool",
                       command=lambda page=target:
                       self.discovery_tabs.select(page)).pack(side="right")
        self.build_unlock_tabs(notebook)
        self.build_story_progress_tab(notebook)
        self.build_japanese_fields_tab(notebook)
        self.build_reports_tab(notebook)
        self.status.trace_add(
            'write', lambda *_: self._refresh_discovery_connection_state())
        self.connection_target.trace_add(
            'write', lambda *_: self._refresh_discovery_connection_state())
        self._apply_game_version_ui()
        self._refresh_discovery_connection_state()
        if self.verified_rom_path is not None:
            self.status.set(
                f'Japan-0 ROM verified again from saved selection: '
                f'{self.verified_rom_path}. Connect to native recomp, Project64 or Mupen; '
                'live RAM signatures will still be checked.')
        # Toolkit-local F1; it does not register a system-wide/game hotkey.
        root.bind_all('<F1>', self._on_f1_open_memory, add='+')
        statusbar = ttk.Frame(root, style='Header.TFrame', padding=(16, 5))
        statusbar.pack(fill='x')
        ttk.Label(statusbar, text='EXPERIMENTAL PRACTICE ONLY  •  Never use for submitted runs',
                  style='HeaderSub.TLabel').pack(side='left')
        self.access_footer = tk.StringVar(
            value=('JAPAN: mapped unlock writes enabled; unknown rows skipped'
                   if self.active_version.key == 'japan'
                   and not getattr(args, 'read_only', False)
                   else 'JAPAN READ ONLY'
                   if self.active_version.key == 'japan'
                   else ('READ ONLY' if getattr(args, 'read_only', False)
                         else 'USA memory writes enabled  •  Experimental entrance reload')))
        ttk.Label(statusbar, textvariable=self.access_footer,
                  style='HeaderSub.TLabel').pack(side='right')
        # Refresh the newly visible panel once, rather than continuously
        # polling every hidden tab while the game is running.
        self.notebook.bind('<<NotebookTabChanged>>', self._on_main_tab_changed,
                           add='+')
        root.after(100,self.tick)

    def _refresh_discovery_connection_state(self):
        """Describe the actual attached memory reader, not an old UI hint."""
        if not hasattr(self, 'discovery_connection_state'):
            return
        region = getattr(self.active_version, 'key', 'usa')
        reader = (self.jp_rdram if region == 'japan'
                  else self.mem)
        pid = getattr(self, 'game_pid', None)
        if reader is None:
            state = ('No Japanese game memory attached.' if region == 'japan'
                     else 'No USA game memory attached.')
        elif not pid:
            state = ('Game RAM is present but the process identity is missing. '
                     'Reconnect from Dashboard before starting a session.')
        else:
            backend = getattr(self, 'jp_backend', None) if region == 'japan' else (
                getattr(self, 'connection_target', None).get())
            if region == 'japan' and backend not in (
                    'project64', 'mupen64plus', 'recomp'):
                state = ('Japanese RAM is attached but the detected game backend '
                         'is missing. Reconnect on Dashboard.')
            else:
                state = (f"{'JP' if region == 'japan' else 'USA'} memory attached | PID {pid} | "
                         f"Backend: {backend or 'connected'} | "
                         "Research scans use this connection.")
        self.discovery_connection_state.set(state)

    def _apply_game_version_ui(self):
        """Expose the selected version without implying a mapped Japanese RDRAM."""
        version = self.active_version
        self.root.title(f"Goemon Practice Toolkit {DISPLAY_VERSION} · {version.label}")
        self.version_heading.set(f"{DISPLAY_VERSION}  |  {version.label}")
        enabled = version.live_memory_supported
        region_active = version.key in ('usa', 'japan')
        if self.notebook.select() == str(self.jp_fields_tab):
            self.notebook.select(self.live_memory_tab)
        for tab in self.notebook.tabs()[1:]:
            if tab == str(self.jp_fields_tab):
                # Historical JP probes still supply model/backend state, but
                # the second Live Memory page is no longer user-visible.
                self.notebook.tab(tab, state='hidden')
                continue
            self.notebook.tab(
                tab, state='normal' if region_active else 'disabled')
        # The same visible scene browser and inspector follow the active ROM;
        # USA-only write controls stay individually gated.
        self.configure_scene_browser_region()
        if hasattr(self, 'scene_live'):
            self.refresh_scene_banner(force=True)
        if hasattr(self, 'catalogue_loaded'):
            self.sync_address_catalogue_region()
        if hasattr(self, 'jp_scene_position_frame'):
            if version.key == 'japan':
                self.jp_scene_position_frame.pack(
                    fill='x', pady=(5, 7), after=self.scene_character_line)
            else:
                self.jp_scene_position_frame.pack_forget()
        self.configure_unlock_region()
        # Both ROMs use the same event sessions UI. Japanese sessions
        # compare an explicitly labelled 100-byte research slice (NOT a
        # validated saved-event bank); the existing Advanced A/B/C remains.
        self.discovery_tabs.tab(self.event_sessions_tab, state='normal')
        self.discovery_tabs.tab(self.state_discovery_tab, state='normal')
        self.configure_event_region()
        self.configure_state_probe_region()
        if version.key == 'japan':
            self.jp_card.pack(fill='x', pady=(0, 6))
        else:
            self.jp_card.pack_forget()
        self.refresh_japan_party_controls()
        if version.key == 'japan':
            self.named_native_frame.pack(fill='x', pady=(7, 0))
        else:
            self.named_native_frame.pack_forget()
        self.refresh_named_native_checkpoints()
        # Japan permits fixed-address raw freezes; USA-only task-pointer /
        # health / God Mode controls remain disabled. No USA guest offsets are
        # ever used by Japanese freeze polling.
        usa_edit = bool(
            version.key == 'usa' and self.args.enable_hex_edit
            and not getattr(self.args, 'read_only', False))
        jp_edit = bool(
            version.key == 'japan'
            and getattr(self.args, 'enable_hex_edit', True)
            and not getattr(self.args, 'read_only', False))
        self.raw_write_btn.state(
            ['!disabled'] if (usa_edit or jp_edit) else ['disabled'])
        self.freeze_raw_button.state(
            ['!disabled'] if (usa_edit or jp_edit) else ['disabled'])
        for button in (self.freeze_health_button,
                       self.god_mode_button, self.enemy_pass_through_button):
            button.state(['!disabled'] if usa_edit else ['disabled'])
        if version.key == 'japan':
            self.inspector_status.set(
                'Shared Live Memory: right-click to edit or freeze fixed guest '
                'addresses; freeze pauses during transitions.')
            self.freeze_status.set(
                'Japan-0 raw freezes available during stable gameplay; '
                'USA task-pointer/health/God Mode freezes remain disabled.')
            self.refresh_story_progress()
        if hasattr(self, 'access_footer'):
            self.access_footer.set(
                'JAPAN: mapped unlock writes enabled; unknown rows skipped'
                if version.key == 'japan' and not getattr(self.args, 'read_only', False)
                else 'JAPAN READ ONLY' if version.key == 'japan'
                else ('READ ONLY' if getattr(self.args, 'read_only', False)
                      else 'USA memory writes enabled  •  Experimental entrance reload'))
        # Japan raw-memory mode has no USA-specific field interpretation.
        if version.key == 'japan':
            self.jp_base_row.pack(fill='x', before=self.connect_button, pady=(0, 7))
        else:
            self.jp_base_row.pack_forget()
        self.connect_button.state(['!disabled'])
        if hasattr(self, 'launch_recomp_button'):
            self.launch_recomp_button.state(['!disabled'] if version.key in ('usa', 'japan') else ['disabled'])
        self.capture_state_btn.state(['!disabled'] if enabled else ['disabled'])
        self.restore_state_btn.state(
            ['!disabled'] if enabled and (self.args.enable_state_restore or
                                        self.args.enable_teleport) else ['disabled'])
        if enabled:
            self.status.set('USA selected. Connect to the USA game in Recomp or Project64.')
        else:
            self.status.set(
                'Japan selected. Click Connect for automatic PID/backend/RDRAM '
                'detection; the original retail ROM is requested only once '
                'if no verified path is remembered.')

    def _clear_japan_base_choices(self):
        """Discard process-specific candidate bases when the region or ROM changes."""
        self.jp_candidates = {}
        self.jp_candidates_pid = None
        self.jp_candidates_backend = None
        self.jp_base_selector['values'] = ('Auto (detect)',)
        self.jp_base_choice.set('Auto (detect)')

    def _disconnect_for_version_change(self):
        """Stop write workers and detach before switching region interpretations."""
        # Region switching must not leave old damage candidates/live rows
        # visible under the new game's address interpretation.
        self.clear_damage_capture()
        with self.value_freezes.guard:
            self.stop_all_freezes()
            self.cancel_pending_restore(quiet=True)
            self.pending_direct_warp = None
            self.pending_native_warp = None
            self.jp_auto_warp = None
            self._release_japan_native_key()
            previous = self.process
            self.process = self.mem = self.current = self.jp_rdram = None
            self.game_pid = None
            self.jp_backend = None
            self.last = self.last_t = None
            self.observed_velocity = None
        if previous is not None:
            try:
                previous.close()
            except OSError:
                pass
        self.pos_text.set('X: —    Y: —    Z: —')
        self.speed_text.set('Speed: —')
        self.misc_text.set('Character: —    Action: —    Loading: —')
        self.clear_japan_field_values()
        if hasattr(self, 'state_discovery_tab'):
            self.reset_state_probes()
        if hasattr(self, 'value_search_tab'):
            self.invalidate_value_search_connection()
        if getattr(self, 'jp_read_button', None):
            self.jp_read_button.state(['disabled'])
            self.jp_read_result.set('Japanese guest RAM is not connected.')
        if hasattr(self, 'jp_capture_spawn_btn'):
            self.jp_capture_spawn_btn.state(['disabled'])

    def read_japan_rdram(self):
        """Read raw guest bytes without invoking any USA live-memory parser."""
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            self.jp_read_result.set('Japanese guest RAM is not connected.')
            return
        try:
            address = int(self.jp_read_address.get().strip(), 0)
            length = int(self.jp_read_length.get().strip(), 0)
            if not 1 <= length <= 64:
                raise ValueError('Read length must be between 1 and 64 bytes')
            guest = self.jp_rdram.read_guest(address, length)
            self.jp_read_result.set(f'0x{address:08X}: {guest.hex(" ").upper()}')
        except (ValueError, OSError, PermissionError) as exc:
            self.jp_read_result.set(f'RDRAM read rejected: {exc}')

    def on_game_version_changed(self, _event=None):
        """A version selection never remaps the existing USA RDRAM handle."""
        if self._connecting:
            self.game_version_choice.set(self.active_version.label)
            self.status.set('Complete the existing connection attempt before changing versions.')
            return
        version = next((item for item in VERSIONS.values()
                        if item.label == self.game_version_choice.get()), None)
        if version is None:
            self.game_version_choice.set(self.active_version.label)
            return
        if version == self.active_version:
            return
        self._jp_reconnect_enabled = False
        self._jp_process_birth = None
        self._disconnect_for_version_change()
        self._clear_japan_base_choices()
        self.active_version = version
        if version.key == 'usa' and self.connection_target.get() == 'mupen64plus':
            self.connection_target.set('auto')
        self.verified_rom_path = (
            load_remembered_rom('japan') if version.key == 'japan' else None)
        self._apply_game_version_ui()
        try:
            save_last_region(version.key)
        except OSError:
            pass  # Missing config permission does not block gameplay.
        if self.verified_rom_path is not None:
            self.status.set(
                f'Previously selected Japan-0 ROM reverified: '
                f'{self.verified_rom_path}. Live RAM connection still requires '
                'verified Japanese guest-memory signatures.')

    def _japan_writable_reader(self, host, attached):
        """Re-check native recomp PID and exact JP code probes for every writer.

        Emulator backends retain their existing attached-reader policy.
        A game update, restart or USA binary must never inherit a Japan writer.
        """
        if self.jp_backend == 'recomp':
            verified_japan_recomp_pid(self.game_pid)
            probes = verified_japan_probes(self.verified_rom_path)
            return validate_japan_recomp_writer(host, attached, probes)
        writer = Rdram(host, attached.base, attached.endian)
        writer.rdram_size = getattr(attached, 'rdram_size', 0x800000)
        return writer

    def _open_japan_freeze_writer(self, attached, token):
        """Worker-only, ephemeral Japan-0 writer; never retain across polls."""
        if (self.active_version.key != 'japan'
                or self.jp_rdram is not attached
                or token != self.freeze_token()
                or getattr(self.args, 'read_only', False)
                or self._connecting or self.game_pid is None
                or self.jp_backend not in ('project64', 'mupen64plus', 'recomp')):
            raise RuntimeError('Japanese freeze connection changed')
        host = HostProcess(self.game_pid, writable=True)
        try:
            writer = self._japan_writable_reader(host, attached)
            return host, writer
        except Exception:
            host.close()
            raise

    def write_japan_raw_bytes(self, address, data, *, expected=None):
        """Direct per-row Japanese Live Memory edit, including research fields.

        No confirmation dialogue, byte allowlist, or expensive ROM revalidation
        on every edit. Only the attached Japanese PID/base/endian are used.
        Explicit --read-only always blocks writes. A stale displayed value
        is rejected rather than blindly overwriting changes by the game.
        """
        if (self.active_version.key != 'japan'
                or getattr(self.args, 'read_only', False)
                or self._connecting or self.jp_rdram is None
                or self.game_pid is None
                or self.jp_backend not in ('project64', 'mupen64plus', 'recomp')
                or self.connection_target.get() not in ('auto', self.jp_backend)):
            raise RuntimeError('Connect Japanese RAM with writes enabled first')
        if not isinstance(data, bytes) or len(data) not in (1, 2, 4, 8):
            raise ValueError('Live Memory edit must contain 1, 2, 4, or 8 bytes')
        if expected is not None and len(expected) != len(data):
            raise ValueError('Expected and replacement byte widths differ')
        original = self.jp_rdram
        # Validate the guest address against the active 4/8 MiB reader first.
        original.read_guest(address, len(data))
        host = HostProcess(self.game_pid, writable=True)
        try:
            writer = self._japan_writable_reader(host, original)
            before = writer.read_guest(address, len(data))
            if expected is not None and before != expected:
                raise RuntimeError('RAM value changed since opening editor; retry')
            if before == data:
                return False
            writer.write_guest(address, data)
            if writer.read_guest(address, len(data)) != data:
                raise OSError('Japanese Live Memory write readback mismatch')
            return True
        finally:
            host.close()

    def apply_japan_unlocks(self, changes):
        """Direct mapped Japanese edits without consent or party-only guards.

        The ROM/RAM identity was established at Connect. Reopen a writable
        handle for this click, without rescanning the ROM or checking gameplay
        character/scene each time. Only explicitly mapped Japanese bytes may
        be written, and all unknown rows are rejected before opening a handle.
        """
        changes = tuple(changes)
        if not changes:
            return 0, 0
        if (self.active_version.key != 'japan'
                or getattr(self.args, 'read_only', False)
                or self._connecting or self.jp_rdram is None
                or self.game_pid is None
                or self.jp_backend not in ('project64', 'mupen64plus', 'recomp')
                or self.connection_target.get() not in ('auto', self.jp_backend)):
            raise RuntimeError('Connect Japanese RAM in write-enabled mode first')
        for item, _target in changes:
            if japan_unlock_lead(item) is None:
                raise ValueError(f'{item.label}: Japanese address unknown')
        host = HostProcess(self.game_pid, writable=True)
        try:
            attached = self.jp_rdram
            writable = self._japan_writable_reader(host, attached)
            changed = sum(write_japan_unlock(writable, item, target)
                          for item, target in changes)
            return changed, len(changes)
        finally:
            host.close()

    def move_japan_oedo_xyz(self):
        """User-triggered XYZ in verified Oedo South as Goemon only."""
        result_text = self.jp_position_result
        if (self.active_version.key != 'japan' or self._connecting
                or getattr(self.args, 'read_only', False)
                or not getattr(self.args, 'enable_japan_position_writes', False)
                or self.jp_rdram is None or self.game_pid is None
                or self.verified_rom_path is None):
            result_text.set('Japan position writes require a verified connection and '
                            '--enable-japan-position-writes (without --read-only).')
            return
        try:
            coords = checked_japan_xyz((
                self.jp_pos_x.get(), self.jp_pos_y.get(), self.jp_pos_z.get()))
            current = read_japan_position(self.jp_rdram)
            before = self.jp_rdram.read_guest(
                JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE)
            scene = int.from_bytes(
                self.jp_rdram.read_guest(JAPAN_SCENE_INDEX, 2), 'big')
            character = int.from_bytes(
                self.jp_rdram.read_guest(JAPAN_CHARACTER_INDEX, 4), 'big')
            if (scene != JAPAN_OEDO_SOUTH_SCENE or character != 0):
                raise RuntimeError(
                    'XYZ writes are verified only for Goemon (0) '
                    'in Oedo Town South (scene 0x161); no other scenes/characters.')
        except (ValueError, OSError, RuntimeError, PermissionError) as exc:
            result_text.set(f'Japanese XYZ write rejected: {exc}')
            return

        consent = messagebox.askyesno(
            'Move Goemon to XYZ?',
            'Experimental Japanese position write — Oedo Town South only.'
            '\n\nBack up your save; native recomp does not support full savestates.'
            f'\nCurrent XYZ: ({current[0]:.3f}, {current[1]:.3f}, {current[2]:.3f})'
            f'\nRequested XYZ: ({coords[0]:.3f}, {coords[1]:.3f}, {coords[2]:.3f})'
            '\n\nOnly the verified 12 position bytes at '
            '0x80151B10–0x80151B1B will be changed once.'
            '\nNo scene/character changes, collision bypass, or repeated freeze.',
            parent=self.root)
        if not consent:
            result_text.set('Japanese XYZ move cancelled; no RAM written.')
            return

        writable = None
        pid = self.game_pid
        original = self.jp_rdram
        try:
            target = self.jp_backend
            if target not in ('project64', 'mupen64plus', 'recomp'):
                raise RuntimeError('Japanese backend is not confirmed')
            if target == 'project64' and sys.platform not in ('win32', 'linux'):
                raise RuntimeError('Project64 position writes require Windows or Linux/Wine')
            if self.connection_target.get() not in ('auto', target):
                raise RuntimeError('Selected emulator changed; reconnect')
            check = (verified_japan_recomp_pid(pid) if target == 'recomp'
                     else verified_emulator_pid(pid, target))
            if check != (pid, target):
                raise RuntimeError('Verified Japanese process changed; reconnect')
            probes = verified_japan_probes(self.verified_rom_path)
            writable = HostProcess(pid, writable=True)
            verified = (validate_japan_recomp_writer(writable, original, probes)
                        if target == 'recomp' else validate_rdram_base(
                            writable, original.base, original.endian, probes,
                            allow_4mb=(target == 'project64')))
            if getattr(verified, 'rdram_size', 0x800000) != getattr(
                    original, 'rdram_size', 0x800000):
                raise RuntimeError('Japanese RDRAM mapping size changed; reconnect')
            # Compare independent read and write views immediately before use.
            for address, count in (
                    (JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE),
                    (JAPAN_CHARACTER_INDEX, 4),
                    (JAPAN_SCENE_INDEX, 2)):
                if verified.read_guest(address, count) != original.read_guest(address, count):
                    raise RuntimeError('Writable/read-only RAM disagreement; no XYZ write')
            if verified.read_guest(JAPAN_PLAYER_XYZ_START, 12) != before:
                raise RuntimeError('Position changed after confirmation; no XYZ write')
            outcome = move_japan_goemon_oedo_south(
                verified, coords, expected_before=before)
            if outcome.changed and original.read_guest(
                    JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE) != (
                        verified.read_guest(JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE)):
                raise RuntimeError('Read-only view did not match the verified XYZ write')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            result_text.set(f'Japanese XYZ write rejected: {exc}')
            self.status.set(f'Japanese XYZ write rejected: {exc}')
            return
        finally:
            if writable is not None:
                writable.close()
        # Refresh the displayed coordinates first; then leave the one-shot
        # operation outcome visible rather than overwriting it with a read.
        self.refresh_japan_position()
        message = (
            'Goemon moved to requested XYZ in Oedo South (verified read-back). '
            'Check the game and saved progress if movement or collision is invalid.'
            if outcome.changed else 'Goemon was already at the specified XYZ.')
        result_text.set(message)
        self.status.set(message)

    def open_japan_debug_for_selected_scene(self):
        """Unrestricted original debug-menu entry, independent of scene/actor.

        Only 0x800CD284 -> 0x0A is written, at most once. Never request a
        destination, inspect loading/cutscenes/character or inject input.
        Region/PID/ROM/RDRAM mapping validation is still mandatory.
        """
        caption = self.jp_debug_result
        if (self.active_version.key != 'japan' or self._connecting
                or getattr(self.args, 'read_only', False)
                or self.jp_rdram is None or self.game_pid is None
                or self.verified_rom_path is None):
            caption.set('Connect verified Japanese RAM with writes enabled first.')
            return
        original = self.jp_rdram
        pid = self.game_pid
        target = self.jp_backend
        writable = None
        try:
            if target not in ('project64', 'mupen64plus', 'recomp'):
                raise RuntimeError('Japanese backend not verified')
            if target == 'project64' and sys.platform not in ('win32', 'linux'):
                raise RuntimeError('Project64 debug entry requires Windows or Linux/Wine')
            if self.connection_target.get() not in ('auto', target):
                raise RuntimeError('Connection backend changed; reconnect')
            check = (verified_japan_recomp_pid(pid) if target == 'recomp'
                     else verified_emulator_pid(pid, target))
            if check != (pid, target):
                raise RuntimeError('Japanese process identity changed')
            probes = verified_japan_probes(self.verified_rom_path)
            writable = HostProcess(pid, writable=True)
            # Do not call validate_japan_recomp_context here: it deliberately
            # rejects invalid characters in ordinary gameplay and would make
            # the debug button conditional on character/actor initialization.
            verified = validate_rdram_base(
                writable, original.base, original.endian, probes,
                allow_4mb=(target == 'project64'))
            if getattr(verified, 'rdram_size', 0x800000) != getattr(
                    original, 'rdram_size', 0x800000):
                raise RuntimeError('Japanese RDRAM mapping size changed')
            result = enter_japan_native_debug_menu(verified)
        except (OSError, PermissionError, ValueError, RuntimeError) as exc:
            message = f'Original Japanese debug menu entry failed: {exc}'
            caption.set(message)
            self.status.set(message)
            return
        finally:
            if writable is not None:
                writable.close()
        message = ('Original Japanese debug mode already 0x0A; no RAM write.'
                   if not result.changed else
                   'Original Japanese debug menu requested: wrote only '
                   '0x0A to 0x800CD284; no map, actor, entrance or input changes.')
        caption.set(message)
        self.status.set(message)
        if hasattr(self, 'scene_status'):
            self.scene_status.set(message)
        # Do not initiate a second editor/renderer pass inside a RAM command.
        # Visible panels refresh on their ordinary cadence.

    def _japan_native_warp_writer(self):
        """Reverify exact Japan ROM, process identity and live RAM before each step.

        Returns a short-lived host and matching guest reader; caller closes host.
        This path is independent of USA's layout and never trusts saved PID/base.
        """
        original = self.jp_rdram
        pid = self.game_pid
        target = self.jp_backend
        if (self.active_version.key != 'japan'
                or self._connecting or original is None or pid is None
                or self.verified_rom_path is None
                or getattr(self.args, 'read_only', False)
                or not (getattr(self.args, 'enable_japan_scene_writes', False)
                        or getattr(self.args, 'enable_japan_debug_menu_writes', False))
                or target not in ('project64', 'recomp')
                or self.connection_target.get() not in ('auto', target)
                or (target == 'project64'
                    and sys.platform not in ('win32', 'linux'))):
            raise RuntimeError(
                'Instant warp requires verified Japanese Project64 or native recomp '
                'and enabled Japan scene writes (without --read-only)')
        check = (verified_japan_recomp_pid(pid) if target == 'recomp'
                 else verified_emulator_pid(pid, target))
        if check != (pid, target):
            raise RuntimeError('Japanese game PID changed; reconnect')
        probes = verified_japan_probes(self.verified_rom_path)
        handle = HostProcess(pid, writable=True)
        try:
            verified = (validate_japan_recomp_writer(handle, original, probes)
                        if target == 'recomp' else validate_rdram_base(
                            handle, original.base, original.endian, probes, allow_4mb=True))
            if getattr(verified, 'rdram_size', 0x800000) != getattr(
                    original, 'rdram_size', 0x800000):
                raise RuntimeError('Japan RAM mapping size changed; reconnect')
            for address, size in (
                    (JAPAN_DEBUG_ENGINE_MODE, 1),
                    (JAPAN_DEBUG_SCENE, 2),
                    (JAPAN_DEBUG_CHARACTER, 4)):
                if verified.read_guest(address, size) != original.read_guest(address, size):
                    raise RuntimeError('Japanese writable and read-only RAM disagree')
            return handle, verified
        except Exception:
            handle.close()
            raise

    def _release_japan_native_key(self):
        release = self.jp_native_key_release
        self.jp_native_key_release = None
        if release:
            release()

    def _finish_japan_native_warp(self, message):
        pending = self.jp_auto_warp
        self.jp_auto_warp = None
        try:
            self._release_japan_native_key()
        except (OSError, RuntimeError):
            pass
        if hasattr(self, 'jp_debug_result'):
            self.jp_debug_result.set(message)
        if hasattr(self, 'scene_status'):
            self.scene_status.set(message)
        self.status.set(message)

    def _japan_reference_entrance(self, destination, source):
        """Resolve the exact same selected USA entrance as the USA warp path.

        Both regions share EntranceMixin's cached original-USA atlas, source-
        map/default prioritization, explicit entrance chooser, XYZ/heading/mode
        and Spawn.pending_bytes encoding. No Japan-specific fallback overrides
        the user's selected original USA entrance.
        """
        return self.selected_scene_spawn(destination)

    def capture_japan_warp_spawn(self):
        """Record the current Japanese Goemon position for future room reloads.

        This is a deliberate, user-initiated capture from *the destination*
        while already visiting it. No game memory is written at capture time.
        """
        try:
            if (self.active_version.key != 'japan'
                    or self.jp_rdram is None or self.game_pid is None
                    or self._connecting or self.jp_auto_warp is not None):
                raise RuntimeError(
                    'Connect to stable Japanese gameplay without a pending warp')
            point, basis = capture_current_japan_spawn(self.jp_rdram)
            save_japan_spawn(point, basis=basis)
            self.jp_warp_spawns[point.destination] = point
            message = (
                f'Captured JP scene 0x{point.destination:03X} warp XYZ '
                f'({point.position[0]:.2f}, {point.position[1]:.2f}, '
                f'{point.position[2]:.2f}). Heading/mode: '
                + ('observed matching native pending record.'
                   if basis == 'native-pending' else
                   'UNVERIFIED defaults (0 / 0x10). Test footing.'))
            self.scene_status.set(message)
            self.status.set(message)
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            message = f'Japanese warp-point capture refused: {exc}'
            self.scene_status.set(message)
            self.status.set(message)

    def start_japan_native_scene_warp(self, destination=None):
        """Same immediate 0x0C area-reload sequence as USA Scene Browser.

        Stages Japanese pending scene/optional entrance, then requests 0x0C
        in the SAME call. Never enters debug menu, injects A or writes active
        scene/exit flag. Original debug-menu control is a separate fallback.
        """
        if self.jp_auto_warp is not None:
            self.scene_status.set('Another Japanese scene reload is pending.')
            return
        try:
            destination = (
                self.selected_japan_debug_scene()
                if destination is None else destination)
            if type(destination) is not int or destination not in SCENES:
                raise ValueError('Select a catalogued scene')
            reader = self.jp_rdram
            if reader is None:
                raise RuntimeError('Connect to verified Japan-0 RAM first')
            context = get_japan_debug_context(reader)
            from practice.japanese_debug_warp import _normal_gameplay
            _normal_gameplay(context)
            selector = getattr(self, 'scene_character', None)
            selected = selector.current() if selector is not None else 0
            target_character = selected - 1 if selected in (1, 2, 3, 4) else None
            spawn = self._japan_reference_entrance(
                destination, context[1])
            handle, writable = self._japan_native_warp_writer()
            try:
                if get_japan_debug_context(writable) != context:
                    raise RuntimeError(
                        'Japanese gameplay context changed during attachment')
                # An old XYZ freeze would otherwise rewrite the previous room's
                # coordinates after the destination reaches gameplay. Stop
                # freezes only after identity and source-context verification.
                if hasattr(self, 'value_freezes'):
                    with self.value_freezes.guard:
                        if self.value_freezes.active():
                            self.stop_all_freezes()
                outcome = stage_japan_direct_reload(
                    writable, destination, expected_context=context,
                    spawn=spawn, target_character=target_character)
            finally:
                handle.close()
            now = time.monotonic()
            self.jp_auto_warp = {
                'destination': destination, 'source': context[1],
                'character': context[2], 'pid': self.game_pid,
                'reader': reader, 'started': now, 'deadline': now + 18,
                'seen_reload': outcome.state_after_write == JAPAN_DIRECT_RELOAD_MODE,
                'stable': 0, 'spawn': spawn, 'placement_attempted': False,
                'target_character': target_character,
            }
            entrance_note = (
                f' Shared USA entrance {spawn.entrance_id}, '
                f'XYZ {tuple(round(v, 2) for v in spawn.position)}, '
                f'heading 0x{spawn.heading:X}, mode 0x{spawn.mode:X} '
                'staged in the same native 12-byte entry block as USA.')
            message = (
                f'Japan instant reload 0x{context[1]:03X} → '
                f'0x{destination:03X}: pending destination written, '
                f'engine 0x0C requested; waiting for playable scene.'
                + (f' Target character {target_character} staged experimentally.'
                   if outcome.character_staged else
                   ' Keeping the existing character.')
                + entrance_note)
            self.jp_debug_result.set(message)
            self.scene_status.set(message)
            self.status.set(message)
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            message = f'Japanese instant scene reload refused: {exc}'
            self.jp_debug_result.set(message)
            self.scene_status.set(message)
            self.status.set(message)

    def poll_japan_native_scene_warp(self, now):
        """Monitor area reload; never infer a playable actor from map ID alone.

        Stable scene/mode/loading/character data is distinct from independently
        verified player task or animation. Only the originally confirmed
        Goemon/Oedo vector is eligible for post-load position correction.
        """
        pending = self.jp_auto_warp
        if pending is None:
            return
        if (self.active_version.key != 'japan'
                or getattr(self.args, 'read_only', False)
                or self.jp_rdram is not pending['reader']
                or self.game_pid != pending['pid']
                or self.jp_backend not in ('project64', 'recomp')
                or self._connecting):
            self._finish_japan_native_warp(
                'Japan scene reload cancelled: game session changed')
            return
        if now > pending['deadline']:
            detail = pending.get('wrong_character')
            expected = (pending['target_character'] if
                        pending['target_character'] is not None else
                        pending['character'])
            suffix = (f' Expected character {expected}, last observed {detail}.'
                      if detail is not None else '')
            self._finish_japan_native_warp(
                f'Japan reload to 0x{pending["destination"]:03X} '
                'NOT confirmed before timeout; no retry was sent.' + suffix)
            return
        try:
            state = self.jp_rdram.read_guest(JAPAN_DEBUG_ENGINE_MODE, 1)[0]
            if state == JAPAN_DIRECT_RELOAD_MODE:
                pending['seen_reload'] = True
                pending['stable'] = 0
                pending['stable_character'] = None
                return
            if state == JAPAN_NATIVE_DEBUG_MODE:
                self._finish_japan_native_warp(
                    'Japan reload unexpectedly entered original debug menu; '
                    'no menu selection or A input sent.')
                return
            readiness = japan_scene_readiness(
                self.jp_rdram, pending['destination'])
            if not readiness.scene_loaded:
                pending['stable'] = 0
                pending['stable_character'] = None
                pending['last_not_ready'] = readiness.note
                return
            # An actual destination change is independent evidence of a
            # transition if the short 0x0C interval was missed by polling.
            if not (pending['seen_reload']
                    or pending['destination'] != pending['source']):
                return
            expected = (pending['target_character']
                        if pending['target_character'] is not None else
                        pending['character'])
            if readiness.character != expected:
                pending['wrong_character'] = readiness.character
                pending['stable'] = 0
                pending['stable_character'] = None
                return
            if pending.get('stable_character') != readiness.character:
                pending['stable_character'] = readiness.character
                pending['stable'] = 0
            pending['stable'] += 1
            if pending['stable'] < 3:
                return
            spawn = pending['spawn']
            character = readiness.character
            assert character is not None
            if character != 0:
                self._finish_japan_native_warp(
                    f'Japan scene 0x{pending["destination"]:03X} '
                    f'{SCENES[pending["destination"]]}: stable scene, '
                    f'character {character} detected across 3 reads; '
                    f'USA entrance {spawn.entrance_id} staged. '
                    'Playability/actor initialization is NOT confirmed '
                    'without a verified Japanese per-character actor/task '
                    'pointer; no post-load XYZ write was attempted.')
                return
            actual = read_japan_position(self.jp_rdram)
            if pending['destination'] != JAPAN_OEDO_SOUTH_SCENE:
                distance = position_difference(spawn.position, actual)
                self._finish_japan_native_warp(
                    f'Japan scene 0x{pending["destination"]:03X} '
                    f'{SCENES[pending["destination"]]}: stable Goemon state '
                    f'and plausible XYZ {actual}; source USA entrance '
                    f'{spawn.entrance_id} XYZ {spawn.position} staged. '
                    f'Difference {distance:.1f}. Actor/task not independently '
                    'verified; no post-load write because the JP Goemon XYZ '
                    'offset is only validated for Oedo South (0x161).')
                return
            before_raw = self.jp_rdram.read_guest(
                JAPAN_PLAYER_XYZ_START, JAPAN_PLAYER_XYZ_SIZE)
            expected_raw = struct.pack(
                '>fff', *checked_japan_xyz(spawn.position))
            if before_raw != expected_raw:
                # Guarded, one-shot and ONLY in the verified Oedo South scene.
                pending['placement_attempted'] = True
                handle, writer = self._japan_native_warp_writer()
                try:
                    if not is_japan_scene_loaded(writer, pending['destination']):
                        raise RuntimeError(
                            'Destination became unstable before placement')
                    place_japan_spawn_once(
                        writer, spawn, expected_before=before_raw)
                finally:
                    handle.close()
            final_xyz = read_japan_position(self.jp_rdram)
            distance = position_difference(spawn.position, final_xyz)
            target_xyz = '(' + ', '.join(f'{v:.1f}' for v in spawn.position) + ')'
            observed_xyz = '(' + ', '.join(f'{v:.1f}' for v in final_xyz) + ')'
            verdict = (f'SPAWN MISMATCH: requested {target_xyz}; '
                       f'actual {observed_xyz}; distance {distance:.1f}.'
                       if distance > 8 else
                       f'USA entrance {spawn.entrance_id}: requested '
                       f'{target_xyz}; JP actual {observed_xyz} '
                       f'(distance {distance:.1f}). '
                       'Goemon/Oedo XYZ verified; collision/actor/task '
                       'initialization still require gameplay confirmation.')
            self._finish_japan_native_warp(
                f'Japan 0x{pending["destination"]:03X} '
                f'{SCENES[pending["destination"]]}: {verdict}')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self._finish_japan_native_warp(
                f'Japan scene reload stopped: {exc}; no retry was sent.')

    def native_savestate_action(self, action):
        """Request native emulator-owned F5/F7; never claim it finished writing."""
        if getattr(self.args, 'read_only', False):
            self.status.set('Savestate input disabled by --read-only.')
            return
        if self._connecting:
            self.status.set('Finish connecting before using emulator savestates.')
            return
        target = self.connection_target.get()
        if target == 'auto' and self.active_version.key == 'japan' and self.jp_backend:
            target = self.jp_backend
        try:
            if (self.active_version.key == 'japan' and self.jp_rdram is not None
                    and target != self.jp_backend):
                raise ValueError('Selected emulator differs from connected Japan-0 process; reconnect')
            if target == 'recomp':
                raise ValueError('Goemon64Recomp cannot create complete savestates yet')
            specified = self.pid_text.get().strip()
            if specified:
                pid, kind = verified_emulator_pid(int(specified), target)
            elif self.game_pid is not None:
                pid, kind = verified_emulator_pid(self.game_pid, target)
            else:
                pid, kind = find_emulator_pid(target)
            slot = int(self.savestate_slot.get())
            # Stop asynchronous toolkit writers before the emulator snapshots
            # or restores the machine. A load invalidates cached guest pointers.
            self.stop_damage_capture(quiet=True)
            with self.value_freezes.guard:
                self.stop_all_freezes()
                self.cancel_pending_restore(quiet=True)
                self.pending_direct_warp = None
                self.pending_native_warp = None
            if action == 'load':
                self._disconnect_for_version_change()
            send_state_command(pid, kind, action, slot)
            self.status.set(f'Requested {kind} {action} in state slot {slot} (PID {pid}). '
                            'Confirm completion in the emulator.')
            return pid, kind, slot
        except (ValueError, RuntimeError, OSError) as exc:
            self.status.set(f'Full savestate unavailable: {exc}')

    def refresh_named_native_checkpoints(self):
        """Only show labels for the selected region and emulator backend."""
        if not hasattr(self, 'named_native_selector'):
            return
        region = self.active_version.key
        backend = self.connection_target.get()
        if backend == 'auto' and self.active_version.key == 'japan':
            backend = self.jp_backend
        filtered = [
            record for record in self.named_native_checkpoints
            if record['region'] == region and record['backend'] == backend
        ]
        previous = self.named_native_choice.get()
        labels = [label_named_checkpoint(record) for record in filtered]
        self._named_native_visible = filtered
        self.named_native_selector.configure(values=labels)
        self.named_native_choice.set(previous if previous in labels else
                                     labels[0] if labels else '')
        writable = (region == 'japan' and
                    backend in ('project64', 'mupen64plus') and
                    not getattr(self.args, 'read_only', False))
        self.named_native_save_btn.state(
            ['!disabled'] if writable else ['disabled'])
        self.named_native_load_btn.state(
            ['!disabled'] if writable and filtered else ['disabled'])

    def save_named_native_checkpoint(self):
        """Request an emulator full save; store only its human-readable slot label."""
        if (self.active_version.key != 'japan'
                or self.jp_rdram is None
                or self.game_pid is None
                or self.connection_target.get() not in ('auto', self.jp_backend)):
            self.status.set('Connect Japan-0 Project64/Mupen before naming a state slot.')
            return
        name = self.named_native_name.get().strip()
        if not 1 <= len(name) <= 64:
            self.status.set('Named checkpoint requires a name of 1–64 characters.')
            return
        # Capture optional observational metadata before issuing the save.
        summary = japan_checkpoint_summary(self.jp_rdram)
        dispatched = self.native_savestate_action('save')
        if dispatched is None:
            return
        _pid, backend, slot = dispatched
        record = make_named_checkpoint(
            name, 'japan', backend, slot, **summary)
        try:
            updated = upsert_named_checkpoint(
                self.named_native_checkpoints, record)
            save_named_checkpoints(NATIVE_CHECKPOINTS_FILE, updated)
            self.named_native_checkpoints = updated
            self.refresh_named_native_checkpoints()
            self.named_native_choice.set(label_named_checkpoint(record))
            self.status.set(
                f'Emulator SAVE REQUEST sent to {backend} slot {slot}; '
                f'named metadata recorded as "{name}". '
                'Confirm the actual save completed in the emulator.')
        except (OSError, ValueError) as exc:
            self.status.set(
                f'Emulator save request sent for slot {slot}, but the '
                f'checkpoint label could not be stored: {exc}')

    def load_named_native_checkpoint(self):
        """Route through existing emulator load; never restore a Japanese RAM dump."""
        selected = self.named_native_selector.current()
        if not 0 <= selected < len(self._named_native_visible):
            self.status.set('Select an existing named Japanese state slot.')
            return
        record = self._named_native_visible[selected]
        if (self.active_version.key != 'japan'
                or record['region'] != 'japan'
                or record['backend'] != (self.jp_backend if self.connection_target.get() == 'auto'
                                          else self.connection_target.get())):
            self.status.set('Named checkpoint is for another region/emulator.')
            return
        if (self.jp_rdram is None or self.game_pid is None
                or self.jp_backend != record['backend']):
            self.status.set(
                'Connect to the matching Japan-0 emulator before loading '
                'a named checkpoint.')
            return
        self.savestate_slot.set(str(record['slot']))
        dispatched = self.native_savestate_action('load')
        if dispatched is not None:
            self.status.set(
                f'Requested native {record["backend"]} load of '
                f'{record["name"]} (slot {record["slot"]}). '
                'Confirm completion in the emulator. '
                'Reconnect to read the restored Japanese RAM.')

    def verify_rom_for_version(self):
        """Pick and validate a retail ROM when first attaching Japanese RAM.

        The public dashboard no longer has a separate preliminary Verify ROM
        button. Connect invokes this picker only when no verified path exists.
        """
        selected = filedialog.askopenfilename(
            title=f'Select your original {self.active_version.label} ROM (one time)',
            filetypes=(('Nintendo 64 ROMs', '*.z64 *.n64 *.v64'),
                       ('All files', '*.*')))
        if not selected:
            self.status.set('ROM selection cancelled; no game was attached.')
            return False
        try:
            version = verify_selected_rom(selected, self.active_version.key)
        except (OSError, ValueError) as exc:
            self.verified_rom_path = None
            self.status.set(f'ROM verification failed: {exc}')
            return False
        self.verified_rom_path = Path(selected)
        remembered = False
        if version.key == 'japan':
            try:
                self.verified_rom_path = remember_verified_rom(selected, 'japan')
                remembered = True
            except (OSError, ValueError) as exc:
                # A correctly verified ROM remains valid for this session;
                # a read-only disk or corrupt registry must not disable use.
                self.status.set(f'ROM verified but preference could not be saved: {exc}')
        self._clear_japan_base_choices()
        capability = ('USA live toolkit supported' if version.live_memory_supported
                      else 'Japan-0 verified; select recomp, project64 or mupen64plus and Connect')
        self.status.set(
            f'Verified {version.label} (revision 0). {capability}. '
            + ('ROM path remembered for future sessions; file checked again '
               'before each reuse.' if remembered else ''))
        return True

    def _arrange_dashboard(self, width):
        """Place both cards above the fold at default size; stack on narrow screens."""
        wide = width >= 1080
        if self.dashboard_wide == wide:
            return
        self.dashboard_wide = wide
        self.dashboard_frame.columnconfigure(1, weight=1 if wide else 0)
        self.dashboard_checkpoints_column.grid_configure(
            row=0 if wide else 1,
            column=1 if wide else 0,
            sticky='new',
            padx=(6, 6),
            pady=(0, 0 if wide else 6),
        )

    def open_full_scene_tab(self, event=None):
        if self.active_version.key in ('usa', 'japan'):
            self.notebook.select(self.scene_tab)

    def open_live_memory_tab(self):
        if self.active_version.key in ('usa', 'japan'):
            self.notebook.select(self.live_memory_tab)

    def _on_f1_open_memory(self, _event=None):
        """Toolkit-local shortcut for the complete Live Memory tab."""
        self.open_live_memory_tab()
        return 'break'

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
            self.status.set(f'Launched {self.active_version.key.upper()} native Linux recomp PID '
                            f'{process.pid}; connect after the game ROM has booted.')
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
        if self.active_version.key == 'japan':
            self._connect_japan_emulator()
            return
        if self.connection_target.get() == 'mupen64plus':
            try:
                specified = self.pid_text.get().strip()
                pid, kind = (verified_emulator_pid(int(specified), 'mupen64plus')
                             if specified else find_emulator_pid('mupen64plus'))
                self._disconnect_for_version_change()
                self.game_pid = pid
                self.status.set(f'Mupen64Plus PID {pid} selected for full savestates. '
                                'Its RAM layout is not supported by the toolkit.')
            except (ValueError, RuntimeError, OSError) as exc:
                self.status.set(f'Mupen64Plus connection failed: {exc}')
            return
        if not self.active_version.live_memory_supported:
            self.status.set('The selected game region does not support this connection backend.')
            return
        try:
            pid_hint = int(self.pid_text.get().strip()) if self.pid_text.get().strip() else None
            if pid_hint is not None and pid_hint <= 0:raise ValueError()
        except ValueError:
            self.status.set('Enter a valid positive PID, or leave it blank for automatic selection.')
            return
        self.stop_damage_capture(quiet=True)
        # Complete all old-session freeze writes before closing the RAM handle.
        with self.value_freezes.guard:
            self.stop_all_freezes()
            self.cancel_pending_restore(quiet=True)
            self.pending_direct_warp = None
            self.pending_native_warp = None
            self._connecting = True
            self.connect_button.state(['disabled'])
            self.version_selector.state(['disabled'])
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

    def _connect_japan_emulator(self):
        """Attach Japan-0 to verified native recomp/Mupen/Project64 guest RDRAM."""
        target = self.connection_target.get()
        if target not in ('auto', 'mupen64plus', 'project64', 'recomp'):
            self.status.set('Select auto, recomp, mupen64plus or project64.')
            return
        # Project64 running under Wine has a native Linux PID and mapped
        # RDRAM, which the LinuxProcess adapter can read. Both Wine/Linux
        # and native Windows must pass the same process identity, original-ROM
        # code signatures and live-memory plausibility checks.
        if target == 'project64' and sys.platform not in ('win32', 'linux'):
            self.status.set(
                'Japanese Project64 attachment requires Windows or Linux/Wine.')
            return
        if self.verified_rom_path is None:
            # ROM bytes are used to derive code fingerprints for RDRAM
            # matching, so an unverified path cannot be bypassed.
            if not self.verify_rom_for_version():
                return
        try:
            pid_hint = int(self.pid_text.get().strip()) if self.pid_text.get().strip() else None
            if pid_hint is not None and pid_hint <= 0:
                raise ValueError()
        except ValueError:
            self.status.set('Enter a positive game PID or leave it empty.')
            return
        selected = self.jp_base_choice.get()
        candidate = self.jp_candidates.get(selected)
        if selected != 'Auto (detect)' and (
                candidate is None or (target != 'auto' and self.jp_candidates_backend != target)):
            self.status.set('The selected Japanese RAM candidate is stale; rescan.')
            return
        base_hint = candidate[0] if candidate else self.args.base
        endian = candidate[1] if candidate else self.args.endian
        selected_pid = self.jp_candidates_pid if candidate else None
        self._disconnect_for_version_change()
        self._connecting = True
        self.connect_button.state(['disabled'])
        self.version_selector.state(['disabled'])
        self.status.set(f'Checking Japanese {target} memory signatures '
                        '(three independent code probes; auto RAM layout)...')
        opts = (pid_hint, self.verified_rom_path, base_hint, endian,
                selected_pid, target)
        threading.Thread(target=self._connect_japan_worker, args=(opts,), daemon=True,
                         name='GoemonJapanRegionDiscovery').start()
        self.root.after(50, self._poll_connect_results)

    def _connect_japan_auto_worker(self, opts):
        """Select the *one* process with proven Japan-0 RDRAM, not first name.

        All candidate PID/region/3-code-probe/layout checks run in this worker,
        never on Tk's event thread. A cached executable/base is only a hint:
        code signatures and RAM context are rechecked every time.
        """
        pid_hint, rom_path, base_hint, endian, selected_pid, _ = opts
        confirmed = []
        ambiguous = []
        errors = []
        try:
            probes = verified_japan_probes(rom_path)
            if selected_pid is not None:
                if pid_hint is not None and pid_hint != selected_pid:
                    raise RuntimeError('Selected RAM candidate is for a different PID')
                pid_hint = selected_pid
            candidates = list_japan_processes(
                pid_hint=pid_hint, target='auto',
                allow_project64=(sys.platform in ('win32', 'linux')))
            base = (int(base_hint, 0) if isinstance(base_hint, str)
                    else int(base_hint) if base_hint is not None else None)
            for choice in candidates:
                process = None
                try:
                    if choice.backend == 'recomp':
                        check = verified_japan_recomp_pid(choice.pid)
                    else:
                        check = verified_emulator_pid(choice.pid, choice.backend)
                    if check != (choice.pid, choice.backend):
                        raise RuntimeError('Process identity changed during discovery')
                    process = HostProcess(choice.pid, writable=False)
                    reader, address, mode = connect_candidate_ram(
                        choice, process, probes, base_hint=base, endian=endian)
                    confirmed.append((choice, process, reader, address, mode))
                    process = None  # Owned by result list from now onward.
                except AmbiguousJapaneseRdram as exc:
                    ambiguous.append((choice, exc.candidates))
                except (OSError, PermissionError, RuntimeError, ValueError) as exc:
                    errors.append(f'PID {choice.pid} {choice.backend}: {exc}')
                finally:
                    if process is not None:
                        process.close()
            if len(confirmed) > 1:
                details = describe_verified_connections(
                    (choice.pid, choice.backend, addr, mode)
                    for choice, _, _, addr, mode in confirmed)
                raise RuntimeError(
                    'Multiple Japanese processes pass exact ROM/RDRAM verification: '
                    + details + '. Close other games or provide a PID.')
            if confirmed and ambiguous:
                raise RuntimeError(
                    'Another Japanese process contains ambiguous code-matching '
                    'RAM buffers: ' +
                    ', '.join(f'PID {c.pid} {c.backend}' for c, _ in ambiguous)
                    + '. Resolve before auto-connecting.')
            if len(confirmed) == 1:
                choice, process, reader, address, mode = confirmed.pop()
                remember_verified_connection(choice, probes, address, mode)
                self._connect_queue.put(
                    ('japan-ok', choice.pid, choice.backend,
                     process, reader, address, mode))
                return
            if len(ambiguous) == 1 and len(candidates) == 1:
                choice, rows = ambiguous[0]
                self._connect_queue.put(
                    ('japan-ambiguous', choice.pid, choice.backend, rows))
                return
            failures = ('; '.join(errors + [
                f'PID {c.pid} {c.backend}: {len(rows)} RAM candidates'
                for c, rows in ambiguous])) or 'No code-signature matches'
            raise RuntimeError(
                'No uniquely verified Japan-0 process/layout. ' + failures)
        except Exception as exc:
            message = str(exc)
            if sys.platform == 'linux' and isinstance(exc, PermissionError):
                message += ' ' + external_pid_hint(pid_hint or 'unknown')
            self._connect_queue.put(('error', message))
        finally:
            for _choice, handle, _reader, _address, _mode in confirmed:
                handle.close()

    def _connect_japan_worker(self, opts):
        """Verified ROM code probes only; no Tk or memory writes in worker."""
        pid_hint, rom_path, base_hint, endian, selected_pid, target = opts
        if target == 'auto':
            Toolkit._connect_japan_auto_worker(self, opts)
            return
        process = None
        try:
            if target == 'recomp':
                pid, kind = (verified_japan_recomp_pid(pid_hint)
                             if pid_hint else find_japan_recomp_pid())
            else:
                pid, kind = (verified_emulator_pid(pid_hint, target)
                             if pid_hint else find_emulator_pid(target))
            if kind != target:
                raise RuntimeError('Selected game process changed during discovery')

            if selected_pid is not None and pid != selected_pid:
                raise RuntimeError('Selected RAM base belongs to a different emulator PID; rescan')
            probes = verified_japan_probes(rom_path)
            process = HostProcess(pid, writable=False)
            base = (int(base_hint, 0) if isinstance(base_hint, str) else
                    int(base_hint) if base_hint is not None else None)
            # Manual backend selection and Auto use the same ROM-verified
            # candidate connector and executable-scoped layout cache.
            executable = ''
            try:
                import psutil
                executable = psutil.Process(pid).exe() or ''
            except Exception:
                # Optional executable metadata must not veto a PID whose
                # process identity and ROM signatures are otherwise valid.
                pass
            candidate = JapanProcessCandidate(pid, target, executable)
            reader, address, mode = connect_candidate_ram(
                candidate, process, probes, base_hint=base, endian=endian)
            remember_verified_connection(candidate, probes, address, mode)
            self._connect_queue.put(('japan-ok', pid, target, process, reader,
                                     address, mode))

        except AmbiguousJapaneseRdram as exc:
            if process is not None:
                try:
                    process.close()
                except OSError:
                    pass
            self._connect_queue.put(('japan-ambiguous', pid, target,
                                     exc.candidates))
        except Exception as exc:
            if process is not None:
                try:
                    process.close()
                except OSError:
                    pass
            if sys.platform == 'linux' and isinstance(exc, PermissionError):
                self._connect_queue.put(('error',f'{exc} {external_pid_hint(pid if "pid" in locals() else pid_hint or "unknown")}'))
            else:
                self._connect_queue.put(('error', str(exc)))

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
        self.version_selector.state(['!disabled', 'readonly'])
        self.connect_button.state(['!disabled'])
        if result[0] == 'japan-ambiguous':
            _, pid, target, choices = result
            self.jp_candidates_backend = target
            self.jp_candidates = {
                f'0x{base:X} ({endian})': (base, endian)
                for base, endian in choices
            }
            self.jp_candidates_pid = pid
            self.jp_base_selector['values'] = (
                'Auto (detect)', *self.jp_candidates.keys())
            self.jp_base_choice.set('Auto (detect)')
            self.jp_read_button.state(['disabled'])
            self.jp_capture_spawn_btn.state(['disabled'])
            self.jp_read_result.set(
                'Select a Japan-code-matching RAM base above, then reconnect. '
                'A match alone does not prove the copy is actively changing.')
            self.status.set(
                f'Found {len(choices)} candidate RAM buffers in Japanese {target} PID {pid}. '
                'Choose a base from the dropdown and reconnect.')
        elif result[0] == 'japan-ok':
            _, pid, target, process, reader, base, endian = result
            with self.value_freezes.guard:
                self.process, self.jp_rdram, self.game_pid = process, reader, pid
                self.jp_backend = target
                self.mem = self.current = None
            self.jp_read_button.state(['!disabled'])
            self.jp_capture_spawn_btn.state(['!disabled'])
            # Only a successful Auto attachment can arm live restart tracking.
            self._jp_reconnect_enabled = self.connection_target.get() == 'auto'
            self._jp_process_birth = None
            if self._jp_reconnect_enabled:
                try:
                    import psutil
                    self._jp_process_birth = psutil.Process(pid).create_time()
                except (psutil.NoSuchProcess, psutil.AccessDenied, OSError,
                        ImportError):
                    # Do not guess that a future process with this PID is
                    # the same binary; no automatic monitoring without proof.
                    pass
            size_mb = getattr(reader, 'rdram_size', 0x800000) // 0x100000
            self.jp_read_result.set(
                f'Japan-0 verified {size_mb} MiB RDRAM at 0x{base:X}; {endian}.')

            self.refresh_japan_fields(force=True)
            self.last_inspect_at=0.0
            self.refresh_inspector({})
            self.refresh_unlocks(force=True)
            self.refresh_story_progress()
            self.select_story_edit()
            self.notebook.select(self.scene_tab)
            self.status.set(f'Attached to Japan-0 {target} PID {pid}, '
                            f'{size_mb} MiB RAM 0x{base:X}, {endian}. '
                            'Japanese mapped writes, raw edits and freezes enabled; '
                            'USA-only player/task controls remain unavailable.')
        elif result[0] == 'ok':
            _, pid, process, candidate, sample, base, endian = result
            with self.value_freezes.guard:
                self.process, self.mem, self.game_pid, self.current = process, candidate, pid, sample
            if sample['x'] is None or sample['action'] is None:
                self.status.set(f'Connected PID {pid}, RAM 0x{base:X}, format {endian}; player unavailable. Memory watches remain available.')
            else:self.status.set(f'Validated PID {pid}, RAM 0x{base:X}, format {endian}. Move to verify updates.')
        else:
            with self.value_freezes.guard:
                self.process = self.mem = self.current = self.jp_rdram = None
                self.game_pid = None
                self.jp_backend = None
                self.jp_read_button.state(['disabled'])
                self.jp_capture_spawn_btn.state(['disabled'])
            self.pos_text.set('X: —    Y: —    Z: —')
            self.speed_text.set('Speed: —')
            self.misc_text.set('Character: —    Action: —    Loading: —')
            self.status.set(f'Connection failed: {result[1]}')

    def _watch_japan_process_restart(self, now):
        """Detect an exited/reused PID and re-run JP Auto connection safely.

        This is a throttled Tk-thread lifecycle check, not a write operation.
        Each replacement process still passes exact ROM/RDRAM verification in
        the background before any toolkit controls are re-enabled.
        """
        if (not getattr(self, '_jp_reconnect_enabled', False)
                or self.active_version.key != 'japan'
                or self.connection_target.get() != 'auto'
                or self._connecting
                or now - getattr(self, '_jp_last_liveness_check', 0) < 2):
            return
        self._jp_last_liveness_check = now
        if self.jp_rdram is None:
            # A game that is not running must not cause expensive rapid scans.
            if now - getattr(self, '_jp_last_auto_attempt', 0) < 10:
                return
            self._jp_last_auto_attempt = now
            self.pid_text.set('')
            self._clear_japan_base_choices()
            self._connect_japan_emulator()
            return
        old_birth = getattr(self, '_jp_process_birth', None)
        if old_birth is None:
            return  # No trustworthy PID identity; manual reconnect remains.
        try:
            import psutil
            current_birth = psutil.Process(self.game_pid).create_time()
        except psutil.NoSuchProcess:
            current_birth = None
        except (psutil.AccessDenied, OSError):
            return
        if current_birth == old_birth:
            return
        # All old-session handles and asynchronous freezes must be disabled
        # before scanning the new executable. A PID reused by an unrelated
        # process must never inherit the previous RDRAM mapping/writer.
        self._jp_last_auto_attempt = now
        old_pid = self.game_pid
        self._disconnect_for_version_change()
        self._jp_process_birth = None
        self.pid_text.set('')
        self._clear_japan_base_choices()
        self.status.set(
            f'Japanese client PID {old_pid} exited or restarted; '
            'discovering the new verified process automatically.')
        self._connect_japan_emulator()

    def _visible_main_panel(self):
        """One shared tab visibility policy for both regions."""
        selected = self.notebook.select()
        if selected == str(self.live_memory_tab):
            if self.live_memory_sections.select() == str(self.live_watches_page):
                return 'watches'
            return 'catalogue'
        if selected == str(self.unlock_tab):
            return 'unlocks'
        if selected == str(self.story_progress_tab):
            return 'story'
        if selected == str(self.dashboard_canvas.master):
            return 'dashboard'
        if selected == str(self.scene_tab):
            return 'scene'
        return 'other'

    def _poll_visible_panels(self, snapshot=None, *, force=False):
        """Refresh only the selected main tab, regardless of game region.

        Original guest addresses and decoding remain region-specific, but
        scheduling and Tk widget lifetime are not. No reader is required to
        browse offline metadata. Prevent hidden-page Tk rebuilds/read storms.
        """
        panel = self._visible_main_panel()
        if panel == 'watches':
            if force:
                self.last_inspect_at = 0.0
            self.refresh_inspector(snapshot or {})
        elif panel == 'unlocks':
            self.refresh_unlocks(force=force)
        elif panel == 'story':
            now = time.monotonic()
            if force or now - getattr(self, '_visible_story_last_poll', 0) >= 0.8:
                self._visible_story_last_poll = now
                self.refresh_story_progress()
        elif panel == 'dashboard':
            self.refresh_checkpoint_diff(force=force)
        elif panel == 'scene':
            self.refresh_scene_banner(force=force)
        if (self.active_version.key == 'japan'
                and panel in ('dashboard', 'scene')):
            self.refresh_japan_party_controls()

    def _on_main_tab_changed(self, _event=None):
        """Sample the selected tab once after navigation, never hidden tabs."""
        self.root.after_idle(lambda: self._poll_visible_panels(force=True))

    def _refresh_unlocks_on_reader_change(self):
        """Update offline controls once after detaching, not every UI tick.

        USA uses self.mem; Japan uses self.jp_rdram. Checking only self.mem
        incorrectly treats a *connected Japanese game* as disconnected and
        forces a full 34-item/flag redraw every 170 ms. Once detached, one
        forced refresh clears stale On/Off states and disables write buttons.
        """
        session = active_session(self)
        region, reader = session.region, session.reader
        previous = getattr(self, '_unlock_refresh_reader_token', None)
        if (previous is not None and previous[0] == region
                and previous[1] is reader):
            return
        self._unlock_refresh_reader_token = (region, reader)
        if reader is None:
            self.refresh_unlocks(force=True)
            if hasattr(self, 'scene_live'):
                self.refresh_scene_banner(force=True)

    def tick(self):
        session = active_session(self)
        if session.region == 'japan':
            self._watch_japan_process_restart(time.monotonic())
        if session.region == 'japan' and session.connected:
            self.poll_japan_native_scene_warp(time.monotonic())
            self._poll_visible_panels()
            # Compact dashboard position display is polled only when shown.
            now_jp = time.monotonic()
            if (self._visible_main_panel() == 'dashboard'
                    and now_jp - getattr(self, '_jp_position_last_poll', 0) > 0.8):
                self._jp_position_last_poll = now_jp
                try:
                    from practice.japanese_position import read_japan_position
                    from practice.japanese_debug_warp import JAPAN_DEBUG_CHARACTER
                    xyz=read_japan_position(self.jp_rdram)
                    character=int.from_bytes(
                        self.jp_rdram.read_guest(JAPAN_DEBUG_CHARACTER,4),'big')
                    self.pos_text.set(
                        f'X: {xyz[0]:10.2f}    Y: {xyz[1]:10.2f}    Z: {xyz[2]:10.2f}')
                    self.misc_text.set(
                        f'Character: {character}   Region: Japan-0')
                    self.speed_text.set(
                        'Japan: movement velocity / player task not mapped')
                except (OSError, RuntimeError, ValueError, PermissionError):
                    self.pos_text.set('X: —    Y: —    Z: —')
        if session.region == 'usa' and session.connected:
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
                    self._poll_visible_panels()
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
                    self._poll_visible_panels()
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
                self._poll_visible_panels(s)
                if self.pending_restore and self.pending_restore.get('phase') != 'warp':
                    self.poll_pending_restore(s, now)
            except (OSError,ValueError) as e:
                self.stop_damage_capture(quiet=True)
                self.status.set(f"Memory read failed: {e}")
                self.cancel_pending_restore(quiet=True)
                self.mem=None
        self._refresh_unlocks_on_reader_change()
        self.root.after(170,self.tick)

    def checkpoint_choices(self):
        """One selector for full logical checkpoints and unmodified legacy bookmarks."""
        return ([('logical', i) for i in range(len(self.checkpoints))] +
                [('position', i) for i in range(len(self.legacy_bookmarks))])

    def checkpoint_labels(self):
        labels=[]
        for n, (kind, index) in enumerate(self.checkpoint_choices(), 1):
            if kind=='logical':
                p=self.checkpoints[index]['payload']
                stats=p['summary']
                labels.append(f"{n}. {p['name']} — logical (map {p['map_id']}, "
                              f"{stats['health']}/{stats['max_health']} HP, "
                              f"{stats['ryo']} Ryo, {stats['lives']} lives; XYZ saved)")
            else:
                b=self.legacy_bookmarks[index]
                map_id=b.get('map_id')
                where=f'map {map_id}' if map_id is not None else 'map unknown'
                labels.append(f"{n}. {b.get('name','Untitled')} — legacy POSITION ONLY "
                              f"({where}; no inventory or progression)")
        return labels

    def _restore_legacy_position(self, bookmark):
        """A legacy entry restores coordinates only. Never manufacture progress data."""
        if not self.args.enable_teleport:
            self.status.set('Position-only restore disabled by current access settings.')
            return
        try:
            before=_ensure_capture_safe(self.mem)
            saved_map=bookmark.get('map_id')
            if type(saved_map) is not int or not 0 <= saved_map < 65536:
                raise ValueError('Legacy bookmark has no valid map ID; capture a new logical checkpoint.')
            if before['character'] != bookmark.get('character'):
                raise ValueError('Position-only checkpoint character differs from the active character.')
            if self.mem.u16(MAP_ADDR) != saved_map:
                raise ValueError('Position-only checkpoint requires its original map; automatic warp is unavailable.')
            xyz=tuple(float(bookmark[k]) for k in ('x','y','z'))
            if any(not math.isfinite(v) or abs(v)>=1e6 for v in xyz):
                raise ValueError('Invalid saved position coordinates')
            obj=before['player_ptr']
            if not obj or not self.mem.is_ram_pointer(obj,0x1A):
                raise ValueError('Player object unavailable')
        except (OSError,ValueError,KeyError,TypeError,OverflowError) as exc:
            messagebox.showerror('Position-only restore blocked',str(exc))
            return
        if not messagebox.askyesno('Legacy position-only checkpoint',
            'Restore XYZ only in this map? This does NOT restore inventory, health, '
            'lives, Ryo, rotation, scripts or story progress. It may disrupt gameplay. Continue?'):
            return
        try:
            with self.value_freezes.guard:
                current=_ensure_capture_safe(self.mem)
                if (current['player_ptr'] != obj or current['character'] != before['character'] or
                        self.mem.u16(MAP_ADDR) != saved_map):
                    raise ValueError('Player, character or map changed before position restore')
                encoded=struct.pack('>fff',*xyz)
                original=self.mem.read_guest(obj+0x08,12)
                try:
                    self.mem.write_guest(obj+0x08,encoded)
                    if self.mem.read_guest(obj+0x08,12)!=encoded:
                        raise OSError('Position readback mismatch')
                except Exception:
                    try:self.mem.write_guest(obj+0x08,original)
                    except Exception:pass
                    raise
            self.last=self.last_t=None
            self.status.set(f"Restored legacy position-only checkpoint: {bookmark.get('name','Untitled')} "
                            '(XYZ only; progress unchanged).')
        except (OSError,ValueError,RuntimeError) as exc:
            messagebox.showerror('Position-only restore failed',str(exc))

    def capture_full_checkpoint(self):
        if not self.mem or not self.current:
            messagebox.showerror("Not connected","Connect to the game first")
            return
        try:
            cp=capture_checkpoint(self.mem,self.checkpoint_name.get())
            self.checkpoints.append(cp)
            save_checkpoint_file(CHECKPOINTS_FILE,self.checkpoints)
            self.checkpoints_box["values"]=self.checkpoint_labels()
            self.checkpoints_box.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_options()
            self.diff_cp.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_diff(force=True)
            self.status.set("Captured logical checkpoint: XYZ, rotation, health, lives, Ryo, inventory and progression. This is not a savestate.")
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
        # main() also performs cleanup after the user has closed the Tk root.
        # Destroyed widgets still exist as Python objects, but their Tcl
        # commands no longer exist. Never abort pending-state cleanup there.
        try:
            if (getattr(self, 'cancel_restore_btn', None) is not None
                    and self.cancel_restore_btn.winfo_exists()):
                self.cancel_restore_btn.state(['disabled'])
            if (getattr(self, 'restore_state_btn', None) is not None
                    and (self.args.enable_state_restore or self.args.enable_teleport)
                    and self.restore_state_btn.winfo_exists()):
                self.restore_state_btn.state(['!disabled'])
        except tk.TclError:
            pass  # UI already destroyed; finish non-UI cleanup below.
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
        if getattr(self.args,'read_only',False):
            self.status.set('Checkpoint restore is disabled in read-only mode.')
            return
        i=self.checkpoints_box.current()
        if i<0 or not self.mem or not self.current:return
        if self.pending_restore:
            self.status.set('A checkpoint restore is already pending; cancel it first.')
            return
        if self.pending_direct_warp or self.pending_native_warp:
            self.status.set('Finish or cancel the scene request before restoring a checkpoint.')
            return
        choice=self.checkpoint_choices()
        if i>=len(choice):return
        kind, index=choice[i]
        if kind=='position':
            self._restore_legacy_position(self.legacy_bookmarks[index])
            return
        if not self.args.enable_state_restore:
            self.status.set('Logical checkpoint restoration is disabled.')
            return
        cp=self.checkpoints[index]
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
        args.enable_japan_party_writes = False
        args.enable_japan_position_writes = False
        args.enable_japan_debug_menu_writes = False
        args.enable_japan_scene_writes = False
    return args


def parse_args(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pid",type=int)
    ap.add_argument("--route", default=None, help=argparse.SUPPRESS)  # Legacy Windows launcher option
    ap.add_argument("--base",help="RDRAM host base 0x...; Japan always validates three ROM code probes")
    ap.add_argument("--endian",choices=["auto","wordswapped","byteswapped","big"],default="auto")
    ap.add_argument("--game-version", choices=tuple(VERSIONS), default=None,
                    help=argparse.SUPPRESS)  # Legacy override; select in Dashboard
    ap.add_argument("--read-only",action="store_true",help="Disable game writes and game input; overrides all enable flags")
    ap.add_argument("--enable-japan-party-writes", action="store_true", default=True,
                    help=argparse.SUPPRESS)  # Deprecated; mapped unlocks write by default
    ap.add_argument("--enable-japan-position-writes", action="store_true", default=True,
                    help="Enable Japanese XYZ actions (on by default; --read-only disables)")
    ap.add_argument("--enable-japan-debug-menu-writes", action="store_true", default=True,
                    help="Enable native Japanese debug-menu entry (on by default)")
    ap.add_argument("--enable-japan-scene-writes", action="store_true", default=True,
                    help="Enable Japanese Scene Browser instant 0x0C reload (on by default)")
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
    # Tk normalizes WM_CLASS capitalization. The instance matches the\n    # lowercase desktop filename on real Tk 8.6 / X11.
    root=tk.Tk(className='goemon-practice-toolkit'); app=Toolkit(root,args)
    try:
        root.mainloop()
    finally:
        app.stop_damage_capture(quiet=True)
        app._stop_freeze_worker()
        app.stop_transition_trace()
        app.cancel_pending_restore(quiet=True)
        if getattr(app,'native_key_release',None):app._release_debug_key()
        if getattr(app,'jp_native_key_release',None):app._release_japan_native_key()
        if app.process: app.process.close()
        if getattr(app, '_restart_after_update', False):
            # Relaunch only after normal cleanup releases game handles,
            # freezes, injected keys and Tk widgets.
            try:
                subprocess.Popen(
                    [sys.executable, '-m', 'practice.toolkit', *sys.argv[1:]],
                    cwd=str(Path(__file__).resolve().parents[1]),
                    close_fds=True,
                    start_new_session=(os.name != 'nt'))
            except OSError as exc:
                print(f'Toolkit updated but automatic restart failed: {exc}',
                      file=sys.stderr)

if __name__=="__main__": main()
