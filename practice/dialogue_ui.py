"""Offline USA dialogue browser/editor embedded in the existing toolkit."""
from __future__ import annotations

from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from practice.dialogue_rom import (
    export_index, extract_dialogue, load_usa_image, save_patched_image,
    validate_flexible_replacement, encode_text, decode_tokens,
)
from practice.dialogue_repack import load_usa_retail, save_retail_rom
from practice.dialogue_layout import (
    font_widths_from_rom, inspect_layout, wrap_plain_dialogue, CONTROL_NOTES, NOOP_TOKENS,
)


class DialogueMixin:
    def build_dialogue_tab(self, notebook: ttk.Notebook) -> None:
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Dialogue')
        self.dialogue_tab = tab
        self.dialogue_path = None
        self.dialogue_retail_path = None
        self.dialogue_build_queue = queue.SimpleQueue()
        self.dialogue_build_running = False
        self.dialogue_records = []
        self.dialogue_by_key = {}
        self.dialogue_staged = {}
        self.dialogue_filtered = []
        self.dialogue_status = tk.StringVar(value=(
            'Select the original, decompressed USA 32 MiB ROM. No game connection required.'))
        self.dialogue_query = tk.StringVar()
        self.dialogue_selected_key = None
        self.dialogue_font_widths = None
        self.dialogue_line_break_approved = set()
        self.dialogue_layout_mode = tk.StringVar(value='Measure only')
        self.dialogue_width_limit = tk.StringVar(value='')
        self.dialogue_line_limit = tk.StringVar(value='')
        self.dialogue_layout_summary = tk.StringVar(value=(
            'Font widths are loaded from the verified USA ROM; window bounds are not yet known.'))

        top = ttk.Frame(tab)
        top.pack(fill='x', pady=(0, 7))
        ttk.Button(top, text='Open decompressed USA ROM',
                   command=self._dialogue_open).pack(side='left', padx=(0, 8))
        ttk.Button(top, text='Select original retail USA ROM',
                   command=self._dialogue_open_retail).pack(side='left', padx=(0, 8))
        ttk.Button(top, text='Export index (JSON/CSV)',
                   command=self._dialogue_export).pack(side='left', padx=(0, 8))
        ttk.Button(top, text='Build decompressed',
                   command=self._dialogue_build).pack(side='left', padx=(0, 8))
        self.dialogue_retail_build_button = ttk.Button(
            top, text='Build retail .z64', command=self._dialogue_build_retail)
        self.dialogue_retail_build_button.pack(side='left')
        ttk.Label(tab, textvariable=self.dialogue_status, wraplength=1050).pack(
            anchor='w', fill='x', pady=(0, 7))
        search = ttk.Frame(tab)
        search.pack(fill='x', pady=(0, 6))
        ttk.Label(search, text='Search text / resource ID').pack(side='left', padx=(0, 8))
        ttk.Entry(search, textvariable=self.dialogue_query).pack(side='left', fill='x', expand=True)
        self.dialogue_query.trace_add('write', lambda *_: self._dialogue_filter())

        splitter = ttk.Panedwindow(tab, orient='vertical')
        splitter.pack(fill='both', expand=True)
        listing = ttk.Frame(splitter)
        splitter.add(listing, weight=3)
        cols = ('resource', 'offset', 'references', 'text')
        tree = ttk.Treeview(listing, columns=cols, show='headings', selectmode='browse', height=13)
        self.dialogue_tree = tree
        for col, title, width, stretch in (
            ('resource', 'Resource', 90, False),
            ('offset', 'Offset', 105, False),
            ('references', 'Refs', 65, False),
            ('text', 'Decoded text (candidate)', 740, True),
        ):
            tree.heading(col, text=title)
            tree.column(col, width=width, stretch=stretch)
        scroll = ttk.Scrollbar(listing, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        tree.bind('<<TreeviewSelect>>', self._dialogue_select)

        editor = ttk.LabelFrame(splitter, text=' Selected record — length-changing text edits ', padding=8)
        splitter.add(editor, weight=2)
        self.dialogue_record_info = tk.StringVar(value='Select a record to inspect it.')
        ttk.Label(editor, textvariable=self.dialogue_record_info).pack(anchor='w')
        text_row = ttk.Frame(editor)
        text_row.pack(fill='both', expand=True, pady=(5, 5))
        self.dialogue_editor = tk.Text(text_row, wrap='word', height=6, undo=True)
        text_scroll = ttk.Scrollbar(text_row, orient='vertical', command=self.dialogue_editor.yview)
        self.dialogue_editor.configure(yscrollcommand=text_scroll.set)
        self.dialogue_editor.pack(side='left', fill='both', expand=True)
        text_scroll.pack(side='right', fill='y')
        self.dialogue_editor.bind('<KeyRelease>', lambda _event: self._dialogue_analyze(), add='+')

        layout = ttk.LabelFrame(editor, text=' Font width / layout diagnostics ', padding=6)
        layout.pack(fill='x', pady=(0, 5))
        layout_row = ttk.Frame(layout)
        layout_row.pack(fill='x')
        ttk.Label(layout_row, text='Window profile').pack(side='left', padx=(0, 5))
        self.dialogue_mode_selector = ttk.Combobox(
            layout_row, textvariable=self.dialogue_layout_mode,
            values=('Measure only', 'Single-line (manual cap)', 'Multi-line (manual cap)'),
            state='readonly', width=28)
        self.dialogue_mode_selector.pack(side='left', padx=(0, 12))
        ttk.Label(layout_row, text='Max glyph width (units)').pack(side='left')
        ttk.Entry(layout_row, textvariable=self.dialogue_width_limit, width=7).pack(
            side='left', padx=(5, 12))
        ttk.Label(layout_row, text='Max lines').pack(side='left')
        ttk.Entry(layout_row, textvariable=self.dialogue_line_limit, width=5).pack(
            side='left', padx=(5, 8))
        self.dialogue_wrap_button = ttk.Button(layout_row, text='Wrap to manual limits',
                                               command=self._dialogue_wrap)
        self.dialogue_wrap_button.pack(side='left', padx=(4, 0))
        ttk.Label(layout, textvariable=self.dialogue_layout_summary,
                  wraplength=1050).pack(anchor='w', fill='x', pady=(5, 0))
        for var in (self.dialogue_layout_mode, self.dialogue_width_limit,
                    self.dialogue_line_limit):
            var.trace_add('write', lambda *_: self._dialogue_analyze())
        actions = ttk.Frame(editor)
        actions.pack(fill='x')
        ttk.Button(actions, text='Stage edited record', command=self._dialogue_stage).pack(side='left')
        ttk.Button(actions, text='Revert selected', command=self._dialogue_revert).pack(
            side='left', padx=7)
        ttk.Label(editor, text=(
            'Static script references are candidates, not proven reachable conversations. '
            'Original controls must remain ordered. Only the explicit multi-line Wrap action '
            'can approve added -60 line breaks. Caps are user-supplied, not known game bounds. '
            'Longer/shorter records are relocated within their original resource, '
            'with script operands and resource tables updated. Retail output needs '
            'the original USA cartridge and the optional lzkn64 Python package. '
            'Control-code placement can change visible formatting; test in emulator.'),
            wraplength=1000).pack(fill='x', anchor='w', pady=(7, 0))

    def _dialogue_open(self) -> None:
        path = filedialog.askopenfilename(
            title='Select decompressed USA ROM (32 MiB)',
            filetypes=[('Nintendo 64 ROM', '*.z64 *.n64'), ('All files', '*.*')])
        if not path:
            return
        try:
            image = load_usa_image(path)
            records = extract_dialogue(image)
            widths = font_widths_from_rom(image)
        except (OSError, ValueError) as exc:
            messagebox.showerror('Dialogue ROM rejected', str(exc), parent=self.dialogue_tab)
            return
        self.dialogue_path = Path(path)
        self.dialogue_font_widths = widths
        self.dialogue_line_break_approved.clear()
        self.dialogue_records = records
        self.dialogue_by_key = {record.key: record for record in records}
        self.dialogue_staged.clear()
        self.dialogue_selected_key = None
        self.dialogue_query.set('')
        self._dialogue_filter()
        self.dialogue_status.set(
            f'{len(records)} unique statically referenced records indexed from '
            f'{len({r.resource_id for r in records})} resources. No edits staged.')

    def _dialogue_open_retail(self) -> None:
        path = filedialog.askopenfilename(
            title='Select original USA retail ROM (16 MiB)',
            filetypes=[('Nintendo 64 ROM', '*.z64 *.n64'), ('All files', '*.*')])
        if not path:
            return
        try:
            load_usa_retail(path)
        except (OSError, ValueError) as exc:
            messagebox.showerror('Retail ROM rejected', str(exc), parent=self.dialogue_tab)
            return
        self.dialogue_retail_path = Path(path)
        self.dialogue_status.set('Original 16 MiB USA cartridge verified for retail rebuilding.')

    def _dialogue_filter(self) -> None:
        if not hasattr(self, 'dialogue_tree'):
            return
        query = self.dialogue_query.get().strip().casefold()
        tree = self.dialogue_tree
        for item in tree.get_children():
            tree.delete(item)
        filtered = [r for r in self.dialogue_records
                    if not query or query in r.text.casefold() or query in str(r.resource_id)
                    or query in f'0x{r.text_offset:x}']
        self.dialogue_filtered = filtered
        for record in filtered[:800]:
            preview = self.dialogue_staged.get(record.key, record.text)
            tree.insert('', 'end', iid=record.key, values=(
                record.resource_id, f'0x{record.text_offset:X}',
                len(record.references), preview.replace('\n', ' / ')[:200]))
        if self.dialogue_records:
            self.dialogue_status.set(
                f'{len(filtered)} matching records (first {min(800, len(filtered))} shown); '
                f'{len(self.dialogue_staged)} staged edits. Select a row to inspect/edit.')

    def _dialogue_select(self, _event=None) -> None:
        chosen = self.dialogue_tree.selection()
        if not chosen:
            return
        key = chosen[0]
        record = self.dialogue_by_key.get(key)
        if record is None:
            return
        self.dialogue_selected_key = key
        self.dialogue_record_info.set(
            f'ID {record.resource_id} | text +0x{record.text_offset:X} | '
            f'ROM +0x{record.image_offset:X} | '
            f'commands: {", ".join(f"+0x{x:X}" for x in record.references[:12])}'
            f'{" ..." if len(record.references) > 12 else ""} | '
            f'{len(record.tokens)} tokens')
        self.dialogue_editor.delete('1.0', 'end')
        self.dialogue_editor.insert('1.0', self.dialogue_staged.get(key, record.text))
        self._dialogue_analyze()

    def _dialogue_limits(self):
        mode = self.dialogue_layout_mode.get()
        if mode == 'Measure only':
            return None, None
        width_text = self.dialogue_width_limit.get().strip()
        line_text = self.dialogue_line_limit.get().strip()
        if not width_text:
            return None, 1 if mode.startswith('Single-line') else None
        width = int(width_text)
        if mode.startswith('Single-line'):
            return width, 1
        return width, int(line_text) if line_text else None

    def _dialogue_analyze(self) -> None:
        key = getattr(self, 'dialogue_selected_key', None)
        widths = getattr(self, 'dialogue_font_widths', None)
        if not key or key not in self.dialogue_by_key or widths is None:
            self.dialogue_layout_summary.set(
                'Select a record in the verified USA ROM to inspect its glyph widths.')
            return
        try:
            before = inspect_layout(self.dialogue_by_key[key].tokens, widths)
            tokens = encode_text(self.dialogue_editor.get('1.0', 'end-1c'))
            maximum, line_count = self._dialogue_limits()
            after = inspect_layout(tokens, widths, max_width=maximum,
                                   max_lines=line_count)
            controls = tuple(dict.fromkeys(t for t in tokens if t < 0))
            control_info = '; '.join(
                f'{code}: {CONTROL_NOTES.get(code, "unmapped/no-op" if code in NOOP_TOKENS else "unknown")}'
                for code in controls[:5])
            if len(controls) > 5:
                control_info += f'; +{len(controls) - 5} more'
            summary = (f'Original peak {before.longest_line} units; '
                       f'edited peak {after.longest_line} units; '
                       f'edited lines {len(after.line_widths)}; '
                       f'peak glyph entries {after.glyphs_since_clear_max}/120.')
            if after.messages:
                summary += '  WARNING: ' + '; '.join(after.messages)
            elif maximum is None:
                summary += '  No user window-width cap set; overflow cannot be excluded.'
            else:
                summary += '  Within user cap only; real window bounds unverified.'
            if control_info:
                summary += '  Controls: ' + control_info
            self.dialogue_layout_summary.set(summary)
        except ValueError as exc:
            self.dialogue_layout_summary.set(f'Width analysis unavailable: {exc}')

    def _dialogue_wrap(self) -> None:
        key = self.dialogue_selected_key
        if key not in self.dialogue_by_key:
            return
        if self.dialogue_layout_mode.get() != 'Multi-line (manual cap)':
            messagebox.showerror('Multi-line profile required',
                                 'Choose Multi-line (manual cap); one-line area names must not be wrapped automatically.',
                                 parent=self.dialogue_tab)
            return
        if self.dialogue_font_widths is None:
            messagebox.showerror('No verified font table',
                                 'Open the original USA decompressed ROM first.',
                                 parent=self.dialogue_tab)
            return
        record = self.dialogue_by_key[key]
        original = self.dialogue_editor.get('1.0', 'end-1c')
        try:
            maximum, lines = self._dialogue_limits()
            if maximum is None or lines is None:
                raise ValueError('Enter both the manually chosen width and maximum lines')
            source_tokens = validate_flexible_replacement(
                record, original,
                allow_added_line_breaks=key in self.dialogue_line_break_approved)
            wrapped = wrap_plain_dialogue(source_tokens, self.dialogue_font_widths,
                                          max_width=maximum, max_lines=lines)
            text = decode_tokens(wrapped)
            validate_flexible_replacement(record, text, allow_added_line_breaks=True)
        except ValueError as exc:
            messagebox.showerror('Cannot auto-wrap this record', str(exc),
                                 parent=self.dialogue_tab)
            return
        if wrapped != source_tokens:
            self.dialogue_line_break_approved.add(key)
        self.dialogue_editor.delete('1.0', 'end')
        self.dialogue_editor.insert('1.0', text)
        self._dialogue_analyze()

    def _dialogue_stage(self) -> None:
        key = self.dialogue_selected_key
        if key is None or key not in self.dialogue_by_key:
            return
        record = self.dialogue_by_key[key]
        # Tk Text always appends a final newline; end-1c excludes only that.
        replacement = self.dialogue_editor.get('1.0', 'end-1c')
        try:
            tokens = validate_flexible_replacement(
                record, replacement,
                allow_added_line_breaks=key in self.dialogue_line_break_approved)
        except ValueError as exc:
            messagebox.showerror('Invalid text edit', str(exc), parent=self.dialogue_tab)
            return
        if tokens == record.tokens:
            self.dialogue_staged.pop(key, None)
        else:
            self.dialogue_staged[key] = replacement
        self._dialogue_filter()
        self._dialogue_analyze()

    def _dialogue_revert(self) -> None:
        key = self.dialogue_selected_key
        if key is None or key not in self.dialogue_by_key:
            return
        self.dialogue_staged.pop(key, None)
        self.dialogue_line_break_approved.discard(key)
        self.dialogue_editor.delete('1.0', 'end')
        self.dialogue_editor.insert('1.0', self.dialogue_by_key[key].text)
        self._dialogue_filter()
        self._dialogue_analyze()

    def _dialogue_export(self) -> None:
        if not self.dialogue_records:
            return
        path = filedialog.asksaveasfilename(
            title='Export indexed dialogue', defaultextension='.json',
            filetypes=[('JSON index', '*.json'), ('CSV table', '*.csv')])
        if not path:
            return
        try:
            export_index(self.dialogue_records, path)
        except (OSError, ValueError) as exc:
            messagebox.showerror('Export failed', str(exc), parent=self.dialogue_tab)
            return
        self.dialogue_status.set(f'Exported {len(self.dialogue_records)} records to {path}')

    def _dialogue_build(self) -> None:
        if self.dialogue_path is None or not self.dialogue_staged:
            messagebox.showinfo('Nothing to build', 'Load a ROM and stage at least one edit.',
                                parent=self.dialogue_tab)
            return
        path = filedialog.asksaveasfilename(
            title='Write patched decompressed USA ROM', defaultextension='.z64',
            filetypes=[('Nintendo 64 ROM', '*.z64')],
            initialfile='goemon-usa-dialogue-patched.decompressed.z64')
        if not path:
            return
        try:
            digest = save_patched_image(
                self.dialogue_path, path, self.dialogue_records, self.dialogue_staged,
                allow_line_breaks_for=frozenset(self.dialogue_line_break_approved))
        except (OSError, ValueError) as exc:
            messagebox.showerror('ROM build rejected', str(exc), parent=self.dialogue_tab)
            return
        self.dialogue_status.set(
            f'Wrote patched 32 MiB decompressed image: {path} (SHA-1 {digest}). '
            'Boot/display of this particular text change has not been verified.')

    def _dialogue_build_retail(self) -> None:
        if self.dialogue_build_running:
            return
        if self.dialogue_path is None or not self.dialogue_staged:
            messagebox.showinfo('Nothing to build', 'Load the decompressed USA ROM and stage an edit.',
                                parent=self.dialogue_tab)
            return
        if self.dialogue_retail_path is None:
            messagebox.showinfo('Retail ROM required',
                                'First select the unmodified USA 16 MiB retail ROM.',
                                parent=self.dialogue_tab)
            return
        path = filedialog.asksaveasfilename(
            title='Build patched 16 MiB retail USA ROM', defaultextension='.z64',
            filetypes=[('Nintendo 64 ROM', '*.z64')],
            initialfile='goemon-usa-dialogue-hack.z64')
        if not path:
            return
        self.dialogue_build_running = True
        self.dialogue_retail_build_button.state(['disabled'])
        self.dialogue_status.set('Compressing 1,312 resources and rebuilding the retail ROM...')
        self.root.after(100, self._dialogue_poll_retail_build)
        worker = threading.Thread(
            target=self._dialogue_retail_worker,
            args=(self.dialogue_path, self.dialogue_retail_path, Path(path),
                  list(self.dialogue_records), dict(self.dialogue_staged),
                  frozenset(self.dialogue_line_break_approved)),
            daemon=True)
        worker.start()

    def _dialogue_retail_worker(self, source, retail, destination, records, staged,
                                allowed_breaks=frozenset()) -> None:
        try:
            sha1 = save_retail_rom(source, retail, destination, records, staged,
                                   allow_line_breaks_for=allowed_breaks)
            self.dialogue_build_queue.put((True, str(destination), sha1))
        except Exception as exc:
            self.dialogue_build_queue.put((False, str(exc), ''))

    def _dialogue_poll_retail_build(self) -> None:
        if not self.dialogue_build_running:
            return
        try:
            success, detail, sha1 = self.dialogue_build_queue.get_nowait()
        except queue.Empty:
            self.root.after(100, self._dialogue_poll_retail_build)
            return
        self.dialogue_build_running = False
        self.dialogue_retail_build_button.state(['!disabled'])
        if success:
            self.dialogue_status.set(
                f'Built 16 MiB retail .z64: {detail} | SHA-1 {sha1}. '
                'Test modified dialogue in Project64/Mupen64Plus.')
        else:
            self.dialogue_status.set('Retail ROM build rejected; source files were not modified.')
            messagebox.showerror('Retail ROM build failed', detail,
                                 parent=self.dialogue_tab)
