"""Japanese live watches with isolated, explicitly guarded experiment controls."""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from practice.japanese_fields import JAPAN_FIELDS, FIELD_GROUPS, read_japan_fields
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES, RUNTIME_OBSERVATION_STATUS,
    read_japan_scene_probes, compare_guest_readings,
)
from practice.scenes import SCENES
from practice.custom_watches import (FORMATS as CUSTOM_FORMATS, make_watch,
    append_watch, load_watches, save_watches, read_watch)
from practice.paths import practice_data_dir
from practice.japanese_position import (
    JAPAN_PLAYER_XYZ, JAPAN_OEDO_SOUTH_SCENE,
    JAPAN_OEDO_SOUTH_ENTRANCE, read_japan_position,
)
from practice.japanese_debug_warp import (
    debug_menu_selection_hint, get_japan_debug_context,
)

ALL_JAPAN_READS = JAPAN_FIELDS + JAPAN_SCENE_PROBES



class JapaneseFieldsUi:
    def build_japanese_fields_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        self.jp_fields_tab = tab
        notebook.add(tab, text='Japan Live / Party Test')
        ttk.Label(tab, text='Japan Live: cheat-backed values and experimental scene probes (read-only)').pack(
            anchor='w', pady=(0, 5))
        ttk.Label(
            tab, text='The 58 cheat-backed values are externally sourced. The 10 scene'
            ' research fields have mixed evidence: four scene fields are'
            ' supported by live traces, character 0/1 by both switch directions,'
            ' and the remaining fields are hypotheses. All field watches are'
            ' read-only; separately opted-in party unlocks and one Oedo South'
            ' Goemon XYZ move control can write. No automatic warps.', wraplength=960,
        ).pack(anchor='w', pady=(0, 8))
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill='x', pady=(0, 6))
        self.jp_fields_caption = tk.StringVar(value='Connect to Japanese Mupen64Plus RAM.')
        ttk.Label(toolbar, textvariable=self.jp_fields_caption).pack(side='left')
        ttk.Button(toolbar, text='Copy changes',
                   command=self.copy_japan_changes).pack(side='right', padx=(4, 0))
        ttk.Button(toolbar, text='Compare',
                   command=self.compare_japan_baseline).pack(side='right', padx=(4, 0))
        ttk.Button(toolbar, text='Capture baseline',
                   command=self.capture_japan_baseline).pack(side='right', padx=(4, 0))
        ttk.Button(toolbar, text='Refresh',
                   command=lambda: self.refresh_japan_fields(force=True)).pack(side='right', padx=(4, 0))
        research_tabs = ttk.Notebook(tab)
        self.jp_research_tabs = research_tabs
        research_tabs.pack(fill='x', pady=(0, 7))
        party = ttk.Frame(research_tabs, padding=7)
        research_tabs.add(party, text='Party unlocks')
        ttk.Label(
            party,
            text='The game builds character actors itself. These buttons only set '
                 'the Sasuke/Yae party flags from the published Japanese cheats. '
                 'Never force the character-index word directly. '
                 'Make a full emulator savestate first.',
            wraplength=960,
        ).pack(anchor='w')
        controls = ttk.Frame(party)
        controls.pack(fill='x', pady=(5, 3))
        self.jp_party_buttons = {}
        for character, label in ((2, 'Unlock Sasuke'), (3, 'Unlock Yae')):
            button = ttk.Button(
                controls, text=label,
                command=lambda cid=character: self.enable_japan_party(cid))
            button.pack(side='left', padx=(0, 6))
            self.jp_party_buttons[character] = button
            button.state(['disabled'])
        self.jp_party_result = tk.StringVar(
            value=('Opt-in enabled. Connect, create an emulator savestate, '
                   'then confirm each individual unlock.'
                   if getattr(getattr(self, 'args', None),
                              'enable_japan_party_writes', False)
                   else 'Party write option disabled by default. Restart with '
                        '--enable-japan-party-writes to use these buttons.'))
        ttk.Label(party, textvariable=self.jp_party_result,
                  wraplength=960).pack(anchor='w', pady=(4, 0))

        move = ttk.Frame(research_tabs, padding=7)
        research_tabs.add(move, text='Goemon XYZ')
        ttk.Label(
            move,
            text='Live-tested position-controlling float32 vector: '
                 'X 0x80151B10 · Y 0x80151B14 · Z 0x80151B18. '
                 'Read position is always read-only; Apply requires a separate '
                 '--enable-japan-position-writes opt-in, Goemon (0), '
                 'scene 0x161, explicit confirmation and an emulator savestate. '
                 'Not verified in other scenes or characters.',
            wraplength=960,
        ).pack(anchor='w')
        row = ttk.Frame(move)
        row.pack(fill='x', pady=(4, 3))
        self.jp_pos_x, self.jp_pos_y, self.jp_pos_z = (
            tk.StringVar(value=str(value))
            for value in JAPAN_OEDO_SOUTH_ENTRANCE)
        for axis, address, variable in zip(
                ('X', 'Y', 'Z'), JAPAN_PLAYER_XYZ,
                (self.jp_pos_x, self.jp_pos_y, self.jp_pos_z)):
            ttk.Label(row, text=f'{axis} 0x{address:08X}').pack(
                side='left', padx=(0, 4))
            ttk.Entry(row, textvariable=variable, width=12).pack(
                side='left', padx=(0, 8))
        buttons = ttk.Frame(move)
        buttons.pack(fill='x', pady=(3, 0))
        ttk.Button(
            buttons, text='Read current XYZ',
            command=self.refresh_japan_position).pack(side='left')
        ttk.Button(
            buttons, text='Use Oedo South entrance values',
            command=self.use_japan_oedo_entrance).pack(side='left', padx=(8, 0))
        self.jp_position_apply_button = ttk.Button(
            buttons, text='Apply XYZ once (confirm)',
            command=self.move_japan_oedo_xyz)
        self.jp_position_apply_button.pack(side='left', padx=(8, 0))
        self.jp_position_apply_button.state(['disabled'])
        self.jp_position_result = tk.StringVar(
            value='Position reads require Japanese RAM connection. '
                  'Writes disabled until separately opted in.')
        ttk.Label(
            move, textvariable=self.jp_position_result,
            wraplength=960).pack(anchor='w', pady=(5, 0))

        debug = ttk.Frame(research_tabs, padding=7)
        research_tabs.add(debug, text='Scene warp')
        ttk.Label(
            debug,
            text='Use the existing Scene Browser in both USA and Japan. '
                 'Double-click a room to request its immediate native '
                 '0x0C area reload. The debug menu is not involved. '
                 'The original debug button below is manual only.',
            wraplength=960).pack(anchor='w')
        row = ttk.Frame(debug)
        row.pack(fill='x', pady=(7, 4))
        ttk.Button(
            row, text='Open shared Scene Browser',
            command=self.open_full_scene_tab).pack(side='left')
        self.jp_debug_menu_button = ttk.Button(
            debug, text='Open original debug menu (manual only)',
            command=self.open_japan_debug_for_selected_scene)
        self.jp_debug_menu_button.pack(anchor='w', pady=(5, 3))
        self.jp_debug_menu_button.state(['disabled'])
        self.jp_debug_result = tk.StringVar(value=(
            'Scene Browser double-click stages the Japan pending scene '
            '(0x800CD490) and requests native area reload 0x0C '
            '(0x800CD284). No debug menu or keyboard A input. '
            'The manual debug button is separate. '
            'Instant reload requires --enable-japan-scene-writes '
            '(legacy debug-write opt-in also works).'))
        ttk.Label(debug, textvariable=self.jp_debug_result,
                  wraplength=960).pack(anchor='w', pady=(3, 0))

        # Never reuse USA's custom-watch file or promote a candidate to a write.
        self.jp_watch_path = practice_data_dir() / 'japan_0_custom_watches.json'
        try:
            self.jp_custom_watches = load_watches(self.jp_watch_path)
            watch_error = None
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.jp_custom_watches = []
            watch_error = str(exc)
        self.jp_custom_watch_status = tk.StringVar(
            value=('Unable to load Japanese watches: ' + watch_error)
                  if watch_error else 'Japan-only custom watches are read-only and unverified.')
        custom = ttk.LabelFrame(tab, text='Japan custom memory watches (read-only)', padding=6)
        custom.pack(fill='x', pady=(0, 7))
        custom_inputs = ttk.Frame(custom)
        custom_inputs.pack(fill='x')
        self.jp_watch_name = tk.StringVar(value='Japan candidate')
        self.jp_watch_address = tk.StringVar(value='0x80161DCC')
        self.jp_watch_type = tk.StringVar(value='u32')
        ttk.Label(custom_inputs, text='Name').pack(side='left')
        ttk.Entry(custom_inputs, textvariable=self.jp_watch_name,
                  width=24).pack(side='left', padx=(4, 8))
        ttk.Label(custom_inputs, text='N64 address').pack(side='left')
        ttk.Entry(custom_inputs, textvariable=self.jp_watch_address,
                  width=16).pack(side='left', padx=(4, 8))
        ttk.Label(custom_inputs, text='Type').pack(side='left')
        ttk.Combobox(custom_inputs, textvariable=self.jp_watch_type,
                     values=tuple(CUSTOM_FORMATS), state='readonly',
                     width=7).pack(side='left', padx=(4, 8))
        ttk.Button(custom_inputs, text='Add read-only watch',
                   command=self.add_japan_custom_watch).pack(side='left')
        ttk.Button(custom_inputs, text='Remove selected',
                   command=self.remove_japan_custom_watch).pack(side='left', padx=(6, 0))
        ttk.Label(custom, textvariable=self.jp_custom_watch_status,
                  wraplength=950).pack(anchor='w', pady=(4, 0))
        body = ttk.Frame(tab)
        body.pack(fill='both', expand=True)
        tree = ttk.Treeview(body, columns=('address', 'value', 'raw', 'status'),
                            show='tree headings', selectmode='browse', height=18)
        for column, title, width in (
            ('#0', 'Japanese field / group', 260),
            ('address', 'Guest RAM address', 145),
            ('value', 'Value', 150),
            ('raw', 'Raw bytes', 105),
            ('status', 'Evidence / validation', 175),
        ):
            tree.heading(column, text=title)
            tree.column(column, width=width, stretch=column in ('#0', 'status'))
        scroll = ttk.Scrollbar(body, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        self.jp_fields_tree = tree
        for group in (*FIELD_GROUPS, JAPAN_SCENE_PROBES[0].group):
            group_id = 'jp_group_' + group.lower().replace(' ', '_')
            tree.insert('', 'end', iid=group_id, text=group, open=True)
            for field in ALL_JAPAN_READS:
                if field.group == group:
                    tree.insert(group_id, 'end', iid='jp_field_' + field.key,
                                text=field.label,
                                values=(f'0x{field.address:08X}', '—', '—',
                                        RUNTIME_OBSERVATION_STATUS.get(
                                            field.key, 'UNVERIFIED: offset candidate')
                                        if field in JAPAN_SCENE_PROBES
                                        else 'External lead'))
        self.jp_custom_group_id = 'jp_group_custom_japan'
        tree.insert('', 'end', iid=self.jp_custom_group_id,
                    text='Custom JP watches (unverified)', open=True)
        for watch in self.jp_custom_watches:
            self._jp_insert_custom_watch(watch)
        ttk.Label(
            tab, text='Sources: Japanese GameHacking.org cheats; TCRF debug code;'
            ' regional-offset hypotheses for scene probes. Both Japanese wikis'
            ' supply scene-transition and Fortune Doll test cases, not memory maps.',
            wraplength=950,
        ).pack(anchor='w', pady=(6, 0))
        self._jp_last_field_poll = 0.0
        self._jp_last_readings = {}
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()

    @staticmethod
    def _jp_custom_key(watch):
        return 'custom:' + watch.name.casefold()

    @staticmethod
    def _jp_custom_iid(watch):
        return 'jp_user_' + watch.name.casefold()

    def _jp_insert_custom_watch(self, watch):
        self.jp_fields_tree.insert(
            self.jp_custom_group_id, 'end', iid=self._jp_custom_iid(watch),
            text=watch.name, values=(f'0x{watch.address:08X}', '—', '—',
                                     f'CUSTOM: {watch.kind}, unverified and read-only'))

    def _jp_reset_comparison(self):
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()

    def add_japan_custom_watch(self):
        if self.active_version.key != 'japan':
            self.jp_custom_watch_status.set('Japanese watch editing requires Japan mode.')
            return False
        try:
            watch = make_watch(self.jp_watch_name.get(), self.jp_watch_address.get(),
                               self.jp_watch_type.get())
            updated = append_watch(self.jp_custom_watches, watch)
            save_watches(self.jp_watch_path, updated)
        except (OSError, ValueError, TypeError) as exc:
            self.jp_custom_watch_status.set(f'Cannot add Japanese watch: {exc}')
            return False
        self.jp_custom_watches = updated
        self._jp_insert_custom_watch(watch)
        self._jp_reset_comparison()
        self.refresh_japan_fields(force=True)
        self.jp_custom_watch_status.set(
            f'Added read-only Japanese candidate: {watch.name} '
            f'(0x{watch.address:08X}, {watch.kind}).')
        return True

    def add_japan_custom_watch_from_search(self, address, kind, label=None):
        self.jp_watch_name.set(label or f'Value Search {address}')
        self.jp_watch_address.set(address)
        self.jp_watch_type.set(kind)
        return self.add_japan_custom_watch()

    def remove_japan_custom_watch(self):
        if self.active_version.key != 'japan':
            self.jp_custom_watch_status.set('Japanese watch editing requires Japan mode.')
            return False
        selection = self.jp_fields_tree.selection()
        if not selection:
            self.jp_custom_watch_status.set('Select a custom Japanese watch first.')
            return False
        selected = selection[0]
        watch = next((w for w in self.jp_custom_watches
                      if self._jp_custom_iid(w) == selected), None)
        if watch is None:
            self.jp_custom_watch_status.set('Only custom Japanese watches can be removed.')
            return False
        updated = [w for w in self.jp_custom_watches if w != watch]
        try:
            save_watches(self.jp_watch_path, updated)
        except (OSError, ValueError) as exc:
            self.jp_custom_watch_status.set(f'Cannot remove Japanese watch: {exc}')
            return False
        self.jp_custom_watches = updated
        self.jp_fields_tree.delete(selected)
        self._jp_reset_comparison()
        self.refresh_japan_fields(force=True)
        self.jp_custom_watch_status.set(f'Removed Japanese watch: {watch.name}')
        return True

    def use_japan_oedo_entrance(self):
        for variable, value in zip(
                (self.jp_pos_x, self.jp_pos_y, self.jp_pos_z),
                JAPAN_OEDO_SOUTH_ENTRANCE):
            variable.set(str(value))
        self.jp_position_result.set(
            'Oedo Town South entrance XYZ loaded in the inputs only; no RAM write.')

    def refresh_japan_position(self):
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            self.jp_position_result.set('Connect to verified Japan RAM for XYZ reads.')
            return
        try:
            values = read_japan_position(self.jp_rdram)
            scene = int.from_bytes(
                self.jp_rdram.read_guest(0x800CD2A2, 2), 'big')
            char = int.from_bytes(
                self.jp_rdram.read_guest(0x80161DCC, 4), 'big')
            for variable, value in zip(
                    (self.jp_pos_x, self.jp_pos_y, self.jp_pos_z), values):
                variable.set(f'{value:.6f}')
            self.jp_position_result.set(
                f'Live XYZ = ({values[0]:.3f}, {values[1]:.3f}, {values[2]:.3f}); '
                f'scene 0x{scene:03X}; character {char}; no RAM write.')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.jp_position_result.set(f'Japan XYZ read failed: {exc}')

    def refresh_japan_position_controls(self):
        enabled = (
            self.active_version.key == 'japan'
            and self.jp_rdram is not None
            and getattr(self, 'game_pid', None) is not None
            and getattr(self, 'verified_rom_path', None) is not None
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() == self.jp_backend
            and bool(getattr(getattr(self, 'args', None),
                             'enable_japan_position_writes', False))
            and not bool(getattr(getattr(self, 'args', None),
                                 'read_only', False))
        )
        self.jp_position_apply_button.state(
            ['!disabled'] if enabled else ['disabled'])

    def selected_japan_debug_scene(self):
        """Use the SAME shared scene selection for every ROM region."""
        chosen = self.scene_list.curselection()
        if not chosen:
            if getattr(self, 'scene_selected', None) is None:
                raise ValueError('Select a room in Scene Browser first')
            scene = self.scene_selected
        else:
            scene = self.scene_options[chosen[0]][0]
        debug_menu_selection_hint(scene)
        return scene

    def show_japan_debug_target(self):
        try:
            scene = self.selected_japan_debug_scene()
            category, index = debug_menu_selection_hint(scene)
            self.jp_debug_result.set(
                f'Selected 0x{scene:03X} ({SCENES[scene]}); original '
                f'debug-menu hint {category} / stage index {index} '
                '(manual fallback only). Double-click this room in Scene '
                'Browser for immediate 0x0C area reload, without the menu.')
        except (ValueError, TypeError) as exc:
            self.jp_debug_result.set(f'Select a catalogued scene: {exc}')

    def refresh_japan_debug_controls(self):
        enabled = (
            self.active_version.key == 'japan'
            and self.jp_rdram is not None
            and getattr(self, 'game_pid', None) is not None
            and getattr(self, 'verified_rom_path', None) is not None
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() == self.jp_backend
            and bool(getattr(getattr(self, 'args', None),
                             'enable_japan_debug_menu_writes', False))
            and not bool(getattr(getattr(self, 'args', None),
                                 'read_only', False))
        )
        self.jp_debug_menu_button.state(
            ['!disabled'] if enabled else ['disabled'])

    def refresh_japan_party_controls(self):
        enabled = (
            self.active_version.key == 'japan'
            and self.jp_rdram is not None
            and getattr(self, 'game_pid', None) is not None
            and (getattr(self, 'jp_backend', None) is None or
                 getattr(getattr(self, 'connection_target', None),
                         'get', lambda: None)() == self.jp_backend)
            and bool(getattr(getattr(self, 'args', None),
                             'enable_japan_party_writes', False))
            and not bool(getattr(getattr(self, 'args', None),
                                 'read_only', False))
        )
        for button in self.jp_party_buttons.values():
            button.state(['!disabled'] if enabled else ['disabled'])
        self.refresh_japan_position_controls()
        self.refresh_japan_debug_controls()

    def _japan_reader_identity(self):
        return (getattr(self, 'game_pid', None),
                getattr(self, 'jp_backend', None), self.jp_rdram.base,
                self.jp_rdram.endian, id(self.jp_rdram))

    def capture_japan_baseline(self):
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            self.jp_fields_caption.set('Connect to Japanese emulator before capturing.')
            return
        self._jp_compare_on = False
        self.refresh_japan_fields(force=True)
        self._jp_baseline = dict(self._jp_last_readings)
        self._jp_baseline_identity = self._japan_reader_identity()
        self._jp_last_changes = ()
        self.jp_fields_caption.set(
            f'Baseline captured for {len(ALL_JAPAN_READS) + len(self.jp_custom_watches)} read-only fields. '
            'Change scenes or pick up items, then Compare.')

    def compare_japan_baseline(self):
        if self.jp_rdram is None or self._jp_baseline is None:
            self.jp_fields_caption.set('Capture baseline after connecting first.')
            return
        if self._jp_baseline_identity != self._japan_reader_identity():
            self._jp_baseline = None
            self.jp_fields_caption.set('Process/RDRAM changed; capture a new baseline.')
            return
        self._jp_compare_on = True
        self.refresh_japan_fields(force=True)

    def copy_japan_changes(self):
        if not self._jp_last_changes or not self._jp_compare_on:
            self.jp_fields_caption.set('No recorded changes; Capture baseline and Compare first.')
            return
        names = {field.key: field.label for field in ALL_JAPAN_READS}
        names.update({self._jp_custom_key(w): w.name for w in self.jp_custom_watches})
        lines = [
            'Japan-0 read-only emulator RAM comparison',
            f'PID/base/endian: {self._jp_baseline_identity}',
            'Changes are observations, not verified field semantics.',
        ]
        for key, before, after in self._jp_last_changes:
            lines.append(f'{names[key]} [{key}]: {before} -> {after}')
            if key in ('scene_map', 'scene_previous', 'scene_pending'):
                before_id, after_id = int(before, 16), int(after, 16)
                before_name = SCENES.get(before_id, 'unlisted')
                after_name = SCENES.get(after_id, 'unlisted')
                lines.append(
                    f'  Scene catalogue (USA-derived; JP unconfirmed): '
                    f'{before_id} {before_name} -> {after_id} {after_name}')
        # Clipboard interaction is user-initiated and does not write game RAM.
        root = self.jp_fields_tab.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append('\n'.join(lines))
        self.jp_fields_caption.set(f'Copied {len(self._jp_last_changes)} raw-byte changes.')

    def clear_japan_field_values(self):
        self._jp_last_field_poll = 0.0
        if not hasattr(self, 'jp_fields_tree'):
            return
        for field in ALL_JAPAN_READS:
            iid = 'jp_field_' + field.key
            self.jp_fields_tree.set(iid, 'value', '—')
            self.jp_fields_tree.set(iid, 'raw', '—')
            self.jp_fields_tree.set(
                iid, 'status',
                RUNTIME_OBSERVATION_STATUS.get(
                    field.key, 'UNVERIFIED: offset candidate')
                if field in JAPAN_SCENE_PROBES else 'External lead')
        for watch in self.jp_custom_watches:
            iid = self._jp_custom_iid(watch)
            self.jp_fields_tree.set(iid, 'value', '—')
            self.jp_fields_tree.set(iid, 'raw', '—')
            self.jp_fields_tree.set(iid, 'status', 'CUSTOM: unverified, read-only')
        self._jp_last_readings = {}
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()
        self.jp_fields_caption.set('Connect to Japanese Project64/Mupen64Plus RAM.')
        self.jp_position_result.set('Disconnected; XYZ inputs are not a game write.')
        self.jp_debug_result.set('Disconnected; native debug menu not requested.')
        self.refresh_japan_party_controls()

    def refresh_japan_fields(self, force=False):
        """At most 1.3 UI reads/s unless manually refreshed; never writes RAM."""
        self.refresh_japan_party_controls()
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            return
        now = time.monotonic()
        if not force and now - self._jp_last_field_poll < 0.75:
            return
        self._jp_last_field_poll = now
        results = read_japan_fields(self.jp_rdram)
        results.update(read_japan_scene_probes(self.jp_rdram))
        for watch in self.jp_custom_watches:
            results[self._jp_custom_key(watch)] = read_watch(self.jp_rdram, watch)
        self._jp_last_readings = results
        changes = ()
        if self._jp_compare_on and self._jp_baseline is not None:
            if self._jp_baseline_identity != self._japan_reader_identity():
                self._jp_compare_on = False
                self._jp_baseline = None
            else:
                changes = compare_guest_readings(
                    self._jp_baseline, results,
                    tuple(field.key for field in ALL_JAPAN_READS) +
                    tuple(self._jp_custom_key(w) for w in self.jp_custom_watches))
        self._jp_last_changes = changes
        changed_by_key = {key: (before, after) for key, before, after in changes}
        errors = 0
        for field in ALL_JAPAN_READS:
            reading = results[field.key]
            iid = 'jp_field_' + field.key
            self.jp_fields_tree.set(iid, 'value', reading.value)
            self.jp_fields_tree.set(iid, 'raw', reading.raw)
            status = reading.status
            if field.key in changed_by_key:
                old_raw, new_raw = changed_by_key[field.key]
                status = f'CHANGED: {old_raw} -> {new_raw}'
            self.jp_fields_tree.set(iid, 'status', status)
            errors += reading.status.startswith('READ ERROR')
        for watch in self.jp_custom_watches:
            reading = results[self._jp_custom_key(watch)]
            iid = self._jp_custom_iid(watch)
            self.jp_fields_tree.set(iid, 'value', reading.value)
            self.jp_fields_tree.set(iid, 'raw', reading.raw)
            status = (f'CUSTOM: {watch.kind}, unverified'
                      if reading.status == 'CUSTOM'
                      else f'READ ERROR: {reading.value}')
            if self._jp_custom_key(watch) in changed_by_key:
                old, new = changed_by_key[self._jp_custom_key(watch)]
                status = f'CHANGED: {old} -> {new}'
            self.jp_fields_tree.set(iid, 'status', status)
            errors += reading.status == 'ERROR'
        comparison = (f'; {len(changes)} changed from baseline'
                      if self._jp_compare_on else '')
        self.jp_fields_caption.set(
            f'{len(JAPAN_FIELDS)} Japanese cheat leads + '
            f'{len(JAPAN_SCENE_PROBES)} scene candidates + '
            f'{len(self.jp_custom_watches)} custom watches; {errors} read errors'
            f'{comparison}; refresh 0.75 s.'
        )
