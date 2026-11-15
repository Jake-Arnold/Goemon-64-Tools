"""Read-only Cheat Engine-style value search UI for Goemon N64 guest RAM."""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import ttk

from practice.value_search import (
    ValueScanner, FORMATS, FILTERS, RDRAM_SIZE, DISPLAY_LIMIT,
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
        self.value_search_status = tk.StringVar(value='Read-only search. Connect to the game, then start an exact or unknown-value scan.')
        self.value_search_type = tk.StringVar(value='u16')
        self.value_search_value = tk.StringVar(value='950')
        self.value_search_filter = tk.StringVar(value='Decreased')
        self.value_search_unaligned = tk.BooleanVar(value=False)
        self.value_search_autorefresh = tk.BooleanVar(value=False)

        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Value search')
        self.value_search_tab = tab
        ttk.Label(tab, text='Find oil, Ryo, boss HP, timers and other unknown values',
                  font=('Segoe UI Semibold', 16)).pack(anchor='w', pady=(0, 7))
        ttk.Label(tab, text="Scans the selected N64 ROM's guest RAM (4 or 8 MiB); no player object required. "
                  'Reads only. Each filter compares a new snapshot with the previous one. '
                  'Values are unverified candidates, not named game fields.',
                  wraplength=1100).pack(anchor='w', pady=(0, 10))

        row = ttk.Frame(tab)
        row.pack(fill='x', pady=(0, 6))
        ttk.Label(row, text='Type:').pack(side='left', padx=(0, 4))
        ttk.Combobox(row, textvariable=self.value_search_type, values=tuple(FORMATS),
                     state='readonly', width=7).pack(side='left', padx=(0, 12))
        ttk.Label(row, text='Number:').pack(side='left', padx=(0, 4))
        ttk.Entry(row, textvariable=self.value_search_value, width=17).pack(side='left', padx=(0, 12))
        ttk.Button(row, text='New exact scan', command=lambda: self._value_start('exact'),
                   style='Gold.TButton').pack(side='left', padx=(0, 7))
        ttk.Button(row, text='Unknown initial value',
                   command=lambda: self._value_start('unknown')).pack(side='left', padx=(0, 7))
        ttk.Checkbutton(row, text='Include unaligned addresses (slower)',
                        variable=self.value_search_unaligned).pack(side='left')

        row2 = ttk.Frame(tab)
        row2.pack(fill='x', pady=(0, 7))
        ttk.Label(row2, text='Next filter:').pack(side='left', padx=(0, 5))
        ttk.Combobox(row2, textvariable=self.value_search_filter, values=FILTERS,
                     state='readonly', width=13).pack(side='left', padx=(0, 10))
        ttk.Button(row2, text='Filter surviving results',
                   command=lambda: self._value_start('filter'),
                   style='Gold.TButton').pack(side='left', padx=(0, 7))
        ttk.Button(row2, text='Refresh visible values',
                   command=lambda: self._value_start('refresh')).pack(side='left', padx=(0, 7))
        ttk.Checkbutton(row2, text='Auto-refresh visible values',
                        variable=self.value_search_autorefresh).pack(side='left', padx=(0, 11))
        ttk.Button(row2, text='Watch selected address',
                   command=self.watch_value_search_candidate).pack(side='left', padx=(0, 7))
        ttk.Button(row2, text='Clear', command=self.clear_value_search).pack(side='left')

        ttk.Label(tab, textvariable=self.value_search_status, wraplength=1090).pack(fill='x', pady=(0, 8))
        frame = ttk.Frame(tab)
        frame.pack(fill='both', expand=True)
        columns = ('address', 'type', 'value', 'hex')
        self.value_search_tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)
        for key, title, width in (
            ('address', 'N64 guest address', 170), ('type', 'Type', 95),
            ('value', 'Value', 160), ('hex', 'Raw big-endian hex', 190),
        ):
            self.value_search_tree.heading(key, text=title)
            self.value_search_tree.column(key, width=width, anchor='w', stretch=(key == 'value'))
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.value_search_tree.yview)
        self.value_search_tree.configure(yscrollcommand=scrollbar.set)
        self.value_search_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        ttk.Label(tab, text='Only the first 200 surviving addresses are shown. Narrow the search before adding a watch. '
                  'Integer scans use exact values; f32 matches IEEE-754 bytes. '
                  'Unknown-value scans begin with every candidate address and may take longer.',
                  wraplength=1080).pack(anchor='w', pady=(8, 0))
        self.root.after(1800, self._value_search_auto_tick)

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
        self.root.after(70, self._value_search_poll)

    def _value_search_poll(self):
        try:
            result = self.value_scan_queue.get_nowait()
        except queue.Empty:
            self.root.after(70, self._value_search_poll)
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

    def _value_search_auto_tick(self):
        if (self.value_search_autorefresh.get() and not self.value_scan_busy and
                self.value_scanner.previous is not None and self._value_search_reader() is self.value_scan_memory and
                self.notebook.select() == str(self.value_search_tab)):
            self._value_start('refresh')
        self.root.after(1800, self._value_search_auto_tick)

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
