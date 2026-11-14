"""Read-only Japanese status tab for verified external-Mupen RDRAM attachment."""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from practice.japanese_fields import JAPAN_FIELDS, FIELD_GROUPS, read_japan_fields


class JapaneseFieldsUi:
    def build_japanese_fields_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        self.jp_fields_tab = tab
        notebook.add(tab, text='Japan Live (read-only)')
        ttk.Label(tab, text='Japanese GameShark address leads — read-only').pack(
            anchor='w', pady=(0, 5))
        ttk.Label(
            tab, text='Published Japanese cheat addresses; most have not been tested'
            ' against live Japanese gameplay. No memory writes, freezes or USA'
            ' pointer translations are enabled.', wraplength=960,
        ).pack(anchor='w', pady=(0, 8))
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill='x', pady=(0, 6))
        self.jp_fields_caption = tk.StringVar(value='Connect to Japanese Mupen64Plus RAM.')
        ttk.Label(toolbar, textvariable=self.jp_fields_caption).pack(side='left')
        ttk.Button(toolbar, text='Refresh values',
                   command=lambda: self.refresh_japan_fields(force=True)).pack(side='right')
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
        for group in FIELD_GROUPS:
            group_id = 'jp_group_' + group.lower().replace(' ', '_')
            tree.insert('', 'end', iid=group_id, text=group, open=True)
            for field in JAPAN_FIELDS:
                if field.group == group:
                    tree.insert(group_id, 'end', iid='jp_field_' + field.key,
                                text=field.label,
                                values=(f'0x{field.address:08X}', '—', '—', 'External lead'))
        ttk.Label(
            tab, text='Sources: GameHacking.org NG5J; TCRF Japanese debug menu.'
            ' Values remain externally sourced until checked during play.',
            wraplength=950,
        ).pack(anchor='w', pady=(6, 0))
        self._jp_last_field_poll = 0.0

    def clear_japan_field_values(self):
        self._jp_last_field_poll = 0.0
        if not hasattr(self, 'jp_fields_tree'):
            return
        for field in JAPAN_FIELDS:
            iid = 'jp_field_' + field.key
            self.jp_fields_tree.set(iid, 'value', '—')
            self.jp_fields_tree.set(iid, 'raw', '—')
            self.jp_fields_tree.set(iid, 'status', 'External lead')
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
        errors = 0
        for field in JAPAN_FIELDS:
            reading = results[field.key]
            iid = 'jp_field_' + field.key
            self.jp_fields_tree.set(iid, 'value', reading.value)
            self.jp_fields_tree.set(iid, 'raw', reading.raw)
            self.jp_fields_tree.set(iid, 'status', reading.status)
            errors += reading.status.startswith('READ ERROR')
        self.jp_fields_caption.set(
            f'{len(JAPAN_FIELDS)} Japanese field leads; {errors} read errors;'
            ' auto-refresh every 0.75 s.'
        )
