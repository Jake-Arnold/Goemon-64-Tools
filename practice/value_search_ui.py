"""Read-only Cheat Engine-style value search UI for Goemon N64 guest RAM."""
from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

from practice.reports import create_value_search_report
from practice.value_search import (
    ValueScanner, FORMATS, FILTERS, TEXT_ENCODINGS, TEXT_KIND,
    RDRAM_SIZE, DISPLAY_LIMIT,
)


class ValueSearchMixin:
    def _value_search_reader(self):
        """One region-selected *read-only* guest-RAM reader.

        Japanese Mupen RDRAM is verified independently and never assigned to
        self.mem: that would expose USA pointer and write operations.
        """
        if getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan':
            return getattr(self, 'jp_rdram', None)
        return getattr(self, 'mem', None)

    def invalidate_value_search_connection(self):
        """Discard scan identity on ROM/PID/RDRAM changes and savestate loads."""
        self.value_scan_generation += 1
        self.value_scan_memory = None
        # A worker may still be using the previous scanner: let its stale
        # response be discarded by _value_search_poll instead of racing clear().
        if not self.value_scan_busy:
            self.value_scanner.clear()
        self.value_search_tree.delete(*self.value_search_tree.get_children())
        self.value_search_status.set('Connection changed; start a new read-only scan.')

    def build_value_search_tab(self, notebook):
        self.value_search_size = RDRAM_SIZE
        self.value_scanner = ValueScanner()
        self.value_scan_memory = None
        self.value_scan_busy = False
        self.value_scan_queue = queue.SimpleQueue()
        self.value_scan_generation = 0
        self._value_search_auto_after = None
        self._value_search_poll_after = None
        self._value_search_next_refresh = 0.0
        self.root.bind('<Destroy>', self._value_search_on_destroy, add='+')

        self.value_search_status = tk.StringVar(
            value='Connect to USA or Japan, then start a scan. Searches never write game RAM.')
        self.value_search_type = tk.StringVar(value='u16')
        self.value_search_value = tk.StringVar(value='950')
        self.value_search_encoding = tk.StringVar(value='ASCII')
        self.value_search_filter = tk.StringVar(value='Decreased')
        self.value_filter_value = tk.StringVar(value='')
        self.value_search_compare = tk.StringVar(value='Previous')
        self.value_search_unaligned = tk.BooleanVar(value=False)
        self.value_search_autorefresh = tk.BooleanVar(value=True)
        self.value_search_refresh_ms = tk.StringVar(value='250 ms')
        self.value_report_name = tk.StringVar(value='Memory value search')

        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Value search')
        self.value_search_tab = tab
        ttk.Label(tab, text='Find addresses by value or game action',
                  font=('Segoe UI Semibold', 16)).pack(anchor='w', pady=(0, 5))
        ttk.Label(tab, text=(
            'Start a scan, change something in-game, then filter the surviving '
            'addresses. Initial = the first snapshot; Previous = the last filter '
            'snapshot; Live = the latest displayed reading.'),
            wraplength=1050).pack(anchor='w', pady=(0, 7))

        startbox = ttk.LabelFrame(tab, text='1 · Start a new scan', padding=7)
        startbox.pack(fill='x', pady=(0, 7))
        row = ttk.Frame(startbox)
        row.pack(fill='x')
        ttk.Label(row, text='Data type').pack(side='left', padx=(0, 4))
        typebox = ttk.Combobox(
            row, textvariable=self.value_search_type,
            values=(*FORMATS.keys(), 'Text'), state='readonly', width=9)
        typebox.pack(side='left', padx=(0, 10))
        typebox.bind('<<ComboboxSelected>>', lambda _event: self._value_search_kind_changed())
        ttk.Label(row, text='Starting value / text').pack(side='left', padx=(0, 4))
        ttk.Entry(row, textvariable=self.value_search_value, width=21).pack(
            side='left', padx=(0, 10))
        ttk.Label(row, text='Text encoding').pack(side='left', padx=(0, 4))
        self.value_search_encoding_widget = ttk.Combobox(
            row, textvariable=self.value_search_encoding,
            values=tuple(TEXT_ENCODINGS), state='disabled', width=11)
        self.value_search_encoding_widget.pack(side='left', padx=(0, 10))
        ttk.Button(row, text='Start exact search',
                   command=lambda: self._value_start('exact')).pack(
                       side='left', padx=(0, 5))
        self.value_unknown_button = ttk.Button(
            row, text='Start unknown search',
            command=lambda: self._value_start('unknown'))
        self.value_unknown_button.pack(side='left')
        options = ttk.Frame(startbox)
        options.pack(fill='x', pady=(4, 0))
        ttk.Checkbutton(options, text='Include unaligned addresses (slower)',
                        variable=self.value_search_unaligned).pack(side='left')
        ttk.Label(options, text=(
            'Text searches match literal bytes (ASCII, Shift-JIS or UTF-8); '
            'custom in-game character encodings may not match.'),
            wraplength=780).pack(side='left', padx=(14, 0))

        refine = ttk.LabelFrame(tab, text='2 · Narrow the current results', padding=7)
        refine.pack(fill='x', pady=(0, 7))
        row2 = ttk.Frame(refine)
        row2.pack(fill='x')
        ttk.Label(row2, text='Keep addresses where value is').pack(
            side='left', padx=(0, 5))
        filterbox = ttk.Combobox(
            row2, textvariable=self.value_search_filter, values=FILTERS,
            state='readonly', width=11)
        filterbox.pack(side='left', padx=(0, 9))
        filterbox.bind('<<ComboboxSelected>>',
                       lambda _event: self._value_search_filter_changed())
        ttk.Label(row2, text='Compared with').pack(side='left', padx=(0, 5))
        ttk.Combobox(row2, textvariable=self.value_search_compare,
                     values=('Previous', 'Initial'), state='readonly',
                     width=10).pack(side='left', padx=(0, 9))
        ttk.Label(row2, text='Filter value (Exact only)').pack(
            side='left', padx=(0, 5))
        self.value_filter_entry = ttk.Entry(
            row2, textvariable=self.value_filter_value, width=16)
        self.value_filter_entry.pack(side='left', padx=(0, 9))
        ttk.Button(row2, text='Apply filter',
                   command=lambda: self._value_start('filter')).pack(side='left')
        ttk.Label(refine, text=(
            'Exact uses the Filter value above, never the Starting value. '
            'Increased/Decreased/Changed/Unchanged compare against Initial '
            'or Previous. Filtering narrows results permanently until New scan.'),
            wraplength=1050).pack(anchor='w', pady=(4, 0))
        self._value_search_filter_changed()

        toolbar = ttk.Frame(tab)
        toolbar.pack(fill='x', pady=(0, 6))
        ttk.Button(toolbar, text='Refresh values now',
                   command=lambda: self._value_start('refresh')).pack(
                       side='left', padx=(0, 8))
        ttk.Checkbutton(toolbar, text='Live refresh',
                        variable=self.value_search_autorefresh).pack(
                            side='left', padx=(0, 6))
        ttk.Label(toolbar, text='Every').pack(side='left', padx=(0, 4))
        ttk.Combobox(toolbar, textvariable=self.value_search_refresh_ms,
                     values=('100 ms', '250 ms', '500 ms', '1000 ms'),
                     state='readonly', width=9).pack(side='left', padx=(0, 15))
        ttk.Button(toolbar, text='Select all visible',
                   command=self.select_all_value_results).pack(
                       side='left', padx=(0, 7))
        ttk.Button(toolbar, text='Watch selected addresses',
                   command=self.watch_value_search_candidate).pack(
                       side='left', padx=(0, 7))
        ttk.Button(toolbar, text='Clear scan',
                   command=self.clear_value_search).pack(side='left')

        exports = ttk.Frame(tab)
        exports.pack(fill='x', pady=(0, 7))
        ttk.Label(exports, text='Report name').pack(side='left', padx=(0, 5))
        ttk.Entry(exports, textvariable=self.value_report_name, width=35).pack(
            side='left', padx=(0, 7))
        ttk.Button(exports, text='Save candidate report',
                   command=self.export_value_search_report).pack(side='left')
        ttk.Label(exports, text='Ctrl/Shift-click to select multiple rows').pack(
            side='left', padx=(16, 0))
        ttk.Label(tab, textvariable=self.value_search_status,
                  wraplength=1070).pack(fill='x', pady=(0, 7))

        frame = ttk.Frame(tab)
        frame.pack(fill='both', expand=True)
        columns = ('address', 'type', 'initial', 'previous', 'value', 'hex')
        self.value_search_tree = ttk.Treeview(
            frame, columns=columns, show='headings',
            selectmode='extended', height=16)
        for key, title, width in (
            ('address', 'N64 address', 155),
            ('type', 'Data type', 105),
            ('initial', 'Initial', 130),
            ('previous', 'Previous', 130),
            ('value', 'Live', 145),
            ('hex', 'Raw hex', 170),
        ):
            self.value_search_tree.heading(key, text=title)
            self.value_search_tree.column(
                key, width=width, anchor='w', stretch=(key == 'value'))
        scrollbar = ttk.Scrollbar(
            frame, orient='vertical', command=self.value_search_tree.yview)
        self.value_search_tree.configure(yscrollcommand=scrollbar.set)
        self.value_search_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        ttk.Label(tab, text=(
            'Up to 200 candidates are shown at once. Live refresh samples '
            'visible addresses only; full RAM is read when starting or '
            'filtering. A value match is not proof of what the address does.'),
            wraplength=1080).pack(anchor='w', pady=(7, 0))

        self._value_search_auto_after = self.root.after(
            125, self._value_search_auto_tick)

    def _value_search_kind_changed(self):
        text_mode = self.value_search_type.get() == 'Text'
        self.value_search_encoding_widget.configure(
            state='readonly' if text_mode else 'disabled')
        self.value_unknown_button.state(
            ['disabled'] if text_mode else ['!disabled'])
        self._value_search_filter_changed()

    def _value_search_filter_changed(self):
        exact = self.value_search_filter.get() == 'Exact'
        self.value_filter_entry.configure(state='normal' if exact else 'disabled')

    def select_all_value_results(self):
        rows = self.value_search_tree.get_children()
        if rows:
            self.value_search_tree.selection_set(rows)
            self.value_search_status.set(
                f'{len(rows)} visible addresses selected. '
                'Watch selected addresses adds numeric values to Live Memory.')

    def _value_search_on_destroy(self, event):
        """Stop callbacks owned by this Tk root, not by another test window."""
        if event.widget is not self.root:
            return
        for attribute in ('_value_search_auto_after',
                          '_value_search_poll_after'):
            job = getattr(self, attribute, None)
            setattr(self, attribute, None)
            if job is not None:
                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass  # Tcl interpreter is already disposing of widgets.

    def _value_start(self, action):
        if self.value_scan_busy:
            self.value_search_status.set('A RAM read is already running.')
            return
        mem = self._value_search_reader()
        if mem is None:
            self.value_search_status.set('Connect to a running game first.')
            return
        if action in ('filter', 'refresh') and (self.value_scanner.previous is None or
                                                self.value_scan_memory is not mem):
            self.value_search_status.set('Start a new search for this game connection first.')
            return
        kind = self.value_search_type.get()
        number = self.value_search_value.get()
        filter_mode = self.value_search_filter.get()
        include_unaligned = self.value_search_unaligned.get()
        # Project64 may expose only an unexpanded 4 MiB RDRAM mapping.
        # Keep USA and synthetic test scanner sizes unchanged.
        scan_size = (getattr(mem, 'rdram_size', self.value_search_size)
                     if getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan'
                     else self.value_search_size)
        self.value_scan_busy = True
        self.value_search_status.set('Reading game RAM; UI remains responsive...')
        generation = self.value_scan_generation

        def worker():
            try:
                scanner = self.value_scanner
                if action in ('exact', 'unknown'):
                    scanner = ValueScanner(size=scan_size,
                                           aligned=not include_unaligned)
                    if action == 'exact':
                        scanner.start_exact(mem, kind, number)
                    else:
                        scanner.start_unknown(mem, kind)
                    rows = scanner.rows(DISPLAY_LIMIT)
                elif action == 'filter':
                    scanner.filter(mem, filter_mode, number)
                    rows = scanner.rows(DISPLAY_LIMIT)
                elif action == 'refresh':
                    rows = scanner.rows(DISPLAY_LIMIT, ram=mem)
                else:
                    raise ValueError('Invalid value-search operation')
                self.value_scan_queue.put((generation, mem, action, scanner, rows, None))
            except Exception as exc:  # Report worker failure instead of leaving UI permanently busy.
                self.value_scan_queue.put((generation, mem, action, None, None, str(exc)))

        # The RDRAM reader can be slow; never scan 8 MiB on the Tk event loop.
        threading.Thread(target=worker, daemon=True, name='GoemonReadOnlyValueSearch').start()
        self._value_search_poll_after = self.root.after(
            70, self._value_search_poll)

    def _value_search_poll(self):
        self._value_search_poll_after = None
        try:
            result = self.value_scan_queue.get_nowait()
        except queue.Empty:
            self._value_search_poll_after = self.root.after(
                70, self._value_search_poll)
            return
        generation, mem, action, scanner, rows, error = result
        self.value_scan_busy = False
        if generation != self.value_scan_generation or mem is not self._value_search_reader():
            self.value_search_status.set('Game connection changed; start a new scan.')
            self.value_scanner.clear()
            self.value_scan_memory = None
            self.value_search_tree.delete(*self.value_search_tree.get_children())
            return
        if error is not None:
            self.value_search_status.set(f'Value search failed: {error}')
            return
        if action in ('exact', 'unknown'):
            self.value_scanner = scanner
            self.value_scan_memory = mem
        selected = self.value_search_tree.selection()
        selected_id = selected[0] if selected else None
        self.value_search_tree.delete(*self.value_search_tree.get_children())
        for row in rows:
            address = f'0x{row["address"]:08X}'
            self.value_search_tree.insert('', 'end', iid=address,
                values=(address, row['kind'], row['value'], row['hex']))
        if selected_id and self.value_search_tree.exists(selected_id):
            self.value_search_tree.selection_set(selected_id)
        label = 'Live preview' if action == 'refresh' else 'Search updated'
        self.value_search_status.set(
            f'{label}: {self.value_scanner.count:,} candidates; '
            f'showing {len(rows):,}. Type {self.value_scanner.kind}; '
            f'{self.value_scanner.samples} snapshot(s). '
            'No game memory was modified.')

    def export_value_search_report(self):
        """Save the current *displayed* snapshot; never claim a full trace."""
        if self.value_scan_busy or self.value_scanner.previous is None:
            self.value_search_status.set(
                'Run a scan and let it finish before saving a report.')
            return
        try:
            displayed = []
            for row in self.value_scanner.rows(DISPLAY_LIMIT):
                displayed.append({
                    'address': f'0x{row["address"]:08X}',
                    'kind': row['kind'], 'value': row['value'],
                    'hex': row['hex'],
                })
            region = getattr(getattr(self, 'active_version', None),
                             'key', 'usa')
            folder = create_value_search_report(
                region=region,
                title=self.value_report_name.get() or 'Memory value search',
                rows=displayed, total_count=self.value_scanner.count,
                value_type=self.value_scanner.kind,
                sample_count=self.value_scanner.samples)
            self.value_search_status.set(
                f'Saved {len(displayed)}/{self.value_scanner.count} '
                f'candidate rows to {folder}. View them in Reports.')
            if hasattr(self, 'refresh_reports'):
                self.refresh_reports(select_path=folder)
        except (OSError, ValueError, TypeError) as exc:
            self.value_search_status.set(f'Report export failed: {exc}')

    def _value_search_tab_visible(self):
        # Standalone scanner tests may attach the tab directly to the root.
        if self.notebook.select() == str(self.value_search_tab):
            return True
        discovery = getattr(self, 'discovery_tab', None)
        tabs = getattr(self, 'discovery_tabs', None)
        return bool(discovery is not None and tabs is not None and
                    self.notebook.select() == str(discovery) and
                    tabs.select() == str(self.value_search_tab))

    def _value_search_auto_tick(self):
        self._value_search_auto_after = None
        if (self.value_search_autorefresh.get() and not self.value_scan_busy and
                self.value_scanner.previous is not None and self._value_search_reader() is self.value_scan_memory and
                self._value_search_tab_visible()):
            self._value_start('refresh')
        self._value_search_auto_after = self.root.after(
            1800, self._value_search_auto_tick)

    def clear_value_search(self):
        if self.value_scan_busy:
            self.value_search_status.set('Current scan must finish before clearing.')
            return
        self.value_scan_generation += 1
        self.value_scanner.clear()
        self.value_scan_memory = None
        self.value_search_tree.delete(*self.value_search_tree.get_children())
        self.value_search_status.set('Cleared candidate set; game memory unchanged.')

    def watch_value_search_candidate(self):
        selected = self.value_search_tree.selection()
        if not selected:
            self.value_search_status.set('Select a surviving address first.')
            return
        addr = selected[0]
        kind = self.value_scanner.kind
        if kind is None:
            return
        if getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan':
            if self.add_japan_custom_watch_from_search(addr, kind):
                self.notebook.select(self.jp_fields_tab)
            else:
                self.value_search_status.set(self.jp_custom_watch_status.get())
            return
        self.user_watch_name.set(f'Value Search {addr}')
        self.user_watch_address.set(addr)
        self.user_watch_type.set(kind)
        self.add_custom_watch()
        self.notebook.select(self.live_memory_tab)
