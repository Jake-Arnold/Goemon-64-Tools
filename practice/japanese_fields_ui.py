"""Read-only Japanese status tab for verified external-Mupen RDRAM attachment."""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from practice.japanese_fields import JAPAN_FIELDS, FIELD_GROUPS, read_japan_fields
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES, RUNTIME_OBSERVED_SCENE_KEYS,
    read_japan_scene_probes, compare_guest_readings,
)
from practice.scenes import SCENES

ALL_JAPAN_READS = JAPAN_FIELDS + JAPAN_SCENE_PROBES



class JapaneseFieldsUi:
    def build_japanese_fields_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        self.jp_fields_tab = tab
        notebook.add(tab, text='Japan Live (read-only)')
        ttk.Label(tab, text='Japan Live: cheat-backed values and experimental scene probes (read-only)').pack(
            anchor='w', pady=(0, 5))
        ttk.Label(
            tab, text='The 58 cheat-backed values are externally sourced. The 10 scene'
            ' fields are unverified JP address hypotheses based on a limited'
            ' region displacement. Baseline comparison records byte changes'
            ' only: no cheats, writes or automatic warps.', wraplength=960,
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
                                        'OBSERVED: one JP transition'
                                        if field.key in RUNTIME_OBSERVED_SCENE_KEYS
                                        else ('UNVERIFIED: offset candidate'
                                              if field in JAPAN_SCENE_PROBES else 'External lead')))
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

    def _japan_reader_identity(self):
        return (getattr(self, 'game_pid', None), self.jp_rdram.base,
                self.jp_rdram.endian)

    def capture_japan_baseline(self):
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            self.jp_fields_caption.set('Connect to Japanese Mupen64Plus before capturing.')
            return
        self._jp_compare_on = False
        self.refresh_japan_fields(force=True)
        self._jp_baseline = dict(self._jp_last_readings)
        self._jp_baseline_identity = self._japan_reader_identity()
        self._jp_last_changes = ()
        self.jp_fields_caption.set(
            f'Baseline captured for {len(ALL_JAPAN_READS)} read-only fields. '
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
        lines = [
            'Japan-0 Mupen64Plus read-only RAM comparison',
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
                iid, 'status', 'OBSERVED: one JP transition'
                if field.key in RUNTIME_OBSERVED_SCENE_KEYS
                else ('UNVERIFIED: offset candidate'
                      if field in JAPAN_SCENE_PROBES else 'External lead'))
        self._jp_last_readings = {}
        self._jp_baseline = None
        self._jp_baseline_identity = None
        self._jp_compare_on = False
        self._jp_last_changes = ()
        self.jp_fields_caption.set('Connect to Japanese Mupen64Plus RAM.')

    def refresh_japan_fields(self, force=False):
        """At most 1.3 UI reads/s unless manually refreshed; never writes RAM."""
        if self.active_version.key != 'japan' or self.jp_rdram is None:
            return
        now = time.monotonic()
        if not force and now - self._jp_last_field_poll < 0.75:
            return
        self._jp_last_field_poll = now
        results = read_japan_fields(self.jp_rdram)
        results.update(read_japan_scene_probes(self.jp_rdram))
        self._jp_last_readings = results
        changes = ()
        if self._jp_compare_on and self._jp_baseline is not None:
            if self._jp_baseline_identity != self._japan_reader_identity():
                self._jp_compare_on = False
                self._jp_baseline = None
            else:
                changes = compare_guest_readings(
                    self._jp_baseline, results, (field.key for field in ALL_JAPAN_READS))
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
        comparison = (f'; {len(changes)} changed from baseline'
                      if self._jp_compare_on else '')
        self.jp_fields_caption.set(
            f'{len(JAPAN_FIELDS)} Japanese cheat leads + '
            f'{len(JAPAN_SCENE_PROBES)} scene candidates; {errors} read errors'
            f'{comparison}; refresh 0.75 s.'
        )
