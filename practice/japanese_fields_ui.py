"""Japanese live watches with isolated, explicitly guarded experiment controls."""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from practice.japanese_fields import JAPAN_FIELDS, read_japan_fields
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES,
    read_japan_scene_probes, compare_guest_readings,
)
from practice.scenes import SCENES
from practice.custom_watches import (make_watch,
    append_watch, load_watches, save_watches, read_watch)
from practice.paths import practice_data_dir
from practice.japanese_position import (
    JAPAN_OEDO_SOUTH_ENTRANCE, read_japan_position,
)
from practice.japanese_debug_warp import (
    debug_menu_selection_hint,
)

ALL_JAPAN_READS = JAPAN_FIELDS + JAPAN_SCENE_PROBES



class JapaneseFieldsUi:
    def initialize_japanese_controls(self):
        """Initialize regional state and the shared Scene Browser XYZ editor."""
        self.jp_fields_caption = tk.StringVar(value='Connect to Japanese native recomp / Project64 / Mupen64Plus RAM.')
        self.jp_pos_x, self.jp_pos_y, self.jp_pos_z = (
            tk.StringVar(value=str(value)) for value in JAPAN_OEDO_SOUTH_ENTRANCE)
        self.jp_position_result = tk.StringVar(
            value='Position reads require Japanese RAM connection. '
                  'Writes default on after connection, unless --read-only.')
        if hasattr(self, 'scene_tab'):
            self.jp_scene_position_frame = ttk.LabelFrame(
                self.scene_tab, text='Japan · Goemon position (experimental)',
                padding=7)
            ttk.Label(
                self.jp_scene_position_frame,
                text=('Verified Goemon XYZ only in Oedo South (0x161). '
                      'Reading is safe; applying values changes guest RAM '
                      'only after the existing safety confirmation.'),
                wraplength=920).pack(anchor='w', pady=(0, 4))
            pos_row = ttk.Frame(self.jp_scene_position_frame)
            pos_row.pack(fill='x')
            for axis, value in zip(
                    ('X', 'Y', 'Z'),
                    (self.jp_pos_x, self.jp_pos_y, self.jp_pos_z)):
                ttk.Label(pos_row, text=axis).pack(
                    side='left', padx=(0, 3))
                ttk.Entry(pos_row, textvariable=value, width=12).pack(
                    side='left', padx=(0, 12))
            ttk.Button(pos_row, text='Read current',
                       command=self.refresh_japan_position).pack(
                           side='left', padx=(0, 6))
            ttk.Button(pos_row, text='Oedo South preset',
                       command=self.use_japan_oedo_entrance).pack(
                           side='left', padx=(0, 6))
            self.jp_scene_position_apply_button = ttk.Button(
                pos_row, text='Apply XYZ (confirm)',
                command=self.move_japan_oedo_xyz)
            self.jp_scene_position_apply_button.pack(side='left')
            self.jp_scene_position_apply_button.state(['disabled'])
            ttk.Label(self.jp_scene_position_frame,
                      textvariable=self.jp_position_result,
                      wraplength=920).pack(anchor='w', pady=(5, 0))

        self.jp_debug_controls_enabled = False
        self.jp_debug_result = tk.StringVar(value=(
            'Scene Browser double-click stages the Japan pending scene '
            '(0x800CD490) and requests native area reload 0x0C '
            '(0x800CD284). No debug menu or keyboard A input. '
            'The manual debug button is separate. '
            'Instant reload requires --enable-japan-scene-writes '
            '(native debug and scene writes are enabled by default).'))
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
        self._jp_last_field_poll = 0.0
        self._jp_last_readings = {}
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()

    @staticmethod
    def _jp_custom_key(watch):
        return 'custom:' + watch.name.casefold()

    def _jp_reset_comparison(self):
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()

    def add_japan_custom_watch(self, name, address, kind):
        if self.active_version.key != 'japan':
            self.jp_custom_watch_status.set('Japanese watch editing requires Japan mode.')
            return False
        try:
            watch = make_watch(name, address, kind)
            updated = append_watch(self.jp_custom_watches, watch)
            save_watches(self.jp_watch_path, updated)
        except (OSError, ValueError, TypeError) as exc:
            self.jp_custom_watch_status.set(f'Cannot add Japanese watch: {exc}')
            return False
        self.jp_custom_watches = updated
        self._jp_reset_comparison()
        self.refresh_japan_fields(force=True)
        self.jp_custom_watch_status.set(
            f'Added read-only Japanese candidate: {watch.name} '
            f'(0x{watch.address:08X}, {watch.kind}).')
        return True

    def add_japan_custom_watch_from_search(self, address, kind, label=None):
        return self.add_japan_custom_watch(label or f'Value Search {address}', address, kind)

    def remove_japan_custom_watch(self, name=None):
        if self.active_version.key != 'japan':
            self.jp_custom_watch_status.set('Japanese watch editing requires Japan mode.')
            return False
        watch = next((w for w in self.jp_custom_watches if w.name == name), None)
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
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus', 'recomp')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() in ('auto', self.jp_backend)
            and bool(getattr(getattr(self, 'args', None),
                             'enable_japan_position_writes', False))
            and not bool(getattr(getattr(self, 'args', None),
                                 'read_only', False))
        )
        if hasattr(self, 'jp_scene_position_apply_button'):
            self.jp_scene_position_apply_button.state(
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
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus', 'recomp')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() in ('auto', self.jp_backend)
            and not bool(getattr(getattr(self, 'args', None),
                                 'read_only', False))
            and not bool(getattr(self, '_connecting', False))
        )
        self.jp_debug_controls_enabled = enabled

    def refresh_japan_party_controls(self):
        """Retained as a legacy refresh entrypoint for XYZ/debug guards.

        The Sasuke/Yae buttons now live only in the shared Unlocks tab.
        """
        self.refresh_japan_position_controls()
        self.refresh_japan_debug_controls()

    def _japan_reader_identity(self):
        return (getattr(self, 'game_pid', None),
                getattr(self, 'jp_backend', None), self.jp_rdram.base,
                self.jp_rdram.endian, id(self.jp_rdram))

    def capture_japan_baseline(self):
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            self.jp_fields_caption.set('Connect to Japanese game RDRAM before capturing.')
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
            'Japan-0 read-only guest RAM comparison',
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
        root = self.scene_tab.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append('\n'.join(lines))
        self.jp_fields_caption.set(f'Copied {len(self._jp_last_changes)} raw-byte changes.')

    def clear_japan_field_values(self):
        self._jp_last_field_poll = 0.0
        self._jp_last_readings = {}
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()
        self.jp_fields_caption.set('Connect to Japanese recomp / Project64 / Mupen64Plus RAM.')
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
        errors = sum(reading.status.startswith('READ ERROR')
                     or reading.status == 'ERROR' for reading in results.values())
        comparison = (f'; {len(changes)} changed from baseline'
                      if self._jp_compare_on else '')
        self.jp_fields_caption.set(
            f'{len(JAPAN_FIELDS)} Japanese cheat leads + '
            f'{len(JAPAN_SCENE_PROBES)} scene candidates + '
            f'{len(self.jp_custom_watches)} custom watches; {errors} read errors'
            f'{comparison}; refresh 0.75 s.'
        )
