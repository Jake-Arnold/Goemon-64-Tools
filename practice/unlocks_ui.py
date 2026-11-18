"""One-click unlock controls for original N64 guest RAM."""
from __future__ import annotations
import time
import tkinter as tk
from tkinter import ttk

from practice.theme import PALETTE
from practice.unlocks import UNLOCKS, GROUPS, Unlock, read_unlock, write_unlock, normalize_unlock_value, unlock_all_known
from practice.hex_edit import parse_hex
from practice.story_progress import write_story_value
from practice.unlock_flag_catalog import (
    flags_for_region, read_flag_bytes, write_japan_crosswalk_flag,
)
from practice.region_unlocks import (
    japan_unlock_lead, japan_unlock_all_targets,
    japan_unlock_wire_value, japan_unlock_display_value,
)

# Small folders retain individual ttk buttons. Large groups use a single
# Treeview with clickable per-flag Off/On cells instead of hundreds of widgets.
_FLAG_FOLDER_EAGER_LIMIT = 12
_FLAG_FOLDER_BATCH_SIZE = 4

class UnlocksMixin:
    def build_unlock_tabs(self, notebook) -> None:
        self.unlock_status = tk.StringVar(value='Connect to US Goemon in Recomp or Project64 to read and change flags.')
        self.unlock_intro_text = tk.StringVar(value=
            'Click any value to write it immediately to the original N64 RAM. '
            'The game may not refresh its inventory until an area or menu reload.')
        self.unlock_all_hint = tk.StringVar(value=
            'One-time edit; does not set story completion flags.')
        self.unlock_address_labels = {}
        self.unlock_count_buttons = {}
        self.unlock_row_widgets = {}
        self.unlock_count_inputs = {}
        self.unlock_count_entries = {}
        self.unlock_last_poll = 0.0

        tab = ttk.Frame(notebook, padding=10)
        notebook.insert(1, tab, text='Unlocks')
        self.unlock_tab = tab
        intro = ttk.Frame(tab)
        intro.pack(fill='x', pady=(0, 8))
        self.usa_unlock_intro = intro
        ttk.Label(intro, text='Unlocks', font=('Segoe UI Semibold', 16),
                  foreground=PALETTE['gold']).pack(anchor='w')
        self.unlock_sections = ttk.Notebook(tab)
        self.unlock_sections.pack(fill='both', expand=True)
        self.unlock_items_page = ttk.Frame(self.unlock_sections, padding=(0, 5))
        self.unlock_flags_page = ttk.Frame(self.unlock_sections, padding=(0, 5))
        self.unlock_sections.add(self.unlock_items_page, text='Items & equipment')
        self.unlock_sections.add(self.unlock_flags_page, text='Story & event flags')
        ttk.Label(
            self.unlock_items_page, textvariable=self.unlock_intro_text,
            style='Muted.TLabel', wraplength=1050).pack(
                anchor='w', pady=(1, 5))
        self.unlock_status_label = ttk.Label(
            self.unlock_items_page, textvariable=self.unlock_status,
            style='Muted.TLabel', wraplength=1050)
        self.unlock_status_label.pack(fill='x', pady=(0, 5))
        all_bar = ttk.Frame(self.unlock_items_page)
        all_bar.pack(fill='x', pady=(0, 8))
        self.usa_unlock_all_bar = all_bar
        self.unlock_all_button = ttk.Button(
            all_bar, text='Unlock all mapped items, weapons and abilities',
            command=self.unlock_all_items)
        self.unlock_all_button.pack(side='left')
        if not self.args.enable_hex_edit:
            self.unlock_all_button.state(['disabled'])
        ttk.Label(all_bar, textvariable=self.unlock_all_hint,
                  style='Muted.TLabel').pack(side='left', padx=8)
        shell = ttk.Frame(self.unlock_items_page)
        shell.pack(fill='both', expand=True)
        self.usa_unlock_shell = shell
        canvas = tk.Canvas(shell, bg=PALETTE['background'], highlightthickness=0)
        scroll = ttk.Scrollbar(shell, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        body = ttk.Frame(canvas, padding=(2, 0, 8, 12))
        win = canvas.create_window((0, 0), window=body, anchor='nw')
        body.bind('<Configure>', lambda _e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfigure(win, width=e.width))
        body.columnconfigure(0, weight=1)

        for row_index, group in enumerate(GROUPS):
            card = ttk.LabelFrame(body, text=f' {group} ', padding=(10, 7))
            card.grid(row=row_index, column=0, sticky='ew', pady=(3, 8))
            card.columnconfigure(0, weight=1)
            for i, item in enumerate(x for x in UNLOCKS if x.group == group):
                ttk.Label(card, text=item.label, style='Card.TLabel').grid(row=i, column=0,
                               sticky='w', pady=3)
                address_label = ttk.Label(
                    card, text=f'{item.address:08X}', style='CardMuted.TLabel',
                    font=('Consolas', 9))
                address_label.grid(row=i, column=1, sticky='w', padx=(12, 8))
                self.unlock_address_labels[item.address] = address_label
                state = ttk.Label(card, text='—', style='Card.TLabel', width=7, font=('Consolas', 10))
                state.grid(row=i, column=2, sticky='w', padx=(4, 14))
                buttons = ttk.Frame(card, style='Card.TFrame')
                buttons.grid(row=i, column=3, sticky='e', pady=2)
                controls = {}
                for value, label in zip(item.values, item.levels):
                    button = ttk.Button(buttons, text=f'{label} [{value:02X}]',
                        command=lambda field=item, v=value: self.set_unlock(field, v),
                        width=max(10, len(label)+6))
                    button.pack(side='left', padx=(3, 0))
                    if not self.args.enable_hex_edit:button.state(['disabled'])
                    controls[value] = button
                if item.quantity:
                    entry_var=tk.StringVar(value='00')
                    entry=ttk.Entry(buttons,textvariable=entry_var,width=5,font=('Consolas',10))
                    entry.pack(side='left',padx=(8,2))
                    count_button=ttk.Button(buttons,text='Set hex count',
                               command=lambda field=item, var=entry_var: self.set_unlock_hex(field,var.get()))
                    count_button.pack(side='left')
                    if not self.args.enable_hex_edit:count_button.state(['disabled'])
                    self.unlock_count_inputs[item.address]=entry_var
                    self.unlock_count_entries[item.address]=entry
                    self.unlock_count_buttons[item.address]=count_button
                self.unlock_row_widgets[item.address] = (state, controls)

        # Tk mouse-wheel events target the child under the pointer rather than
        # the parent Canvas. Bind only Unlocks descendants, so scrolling other
        # tabs and editable controls is not hijacked by a global binding.
        self.unlock_canvas = canvas
        def wheel(event):
            if getattr(event, 'num', None) in (4, 5):
                steps = -1 if event.num == 4 else 1
            else:
                delta = getattr(event, 'delta', 0)
                if not delta:
                    return 'break'
                steps = -max(1, abs(delta) // 120) if delta > 0 else max(1, abs(delta) // 120)
            canvas.yview_scroll(steps, 'units')
            return 'break'
        self._unlock_wheel = wheel

        def bind_wheel(widget):
            for sequence in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                widget.bind(sequence, wheel, add='+')
            for child in widget.winfo_children():
                bind_wheel(child)
        bind_wheel(canvas)
        bind_wheel(body)
        # Linux/X11 sends Button-4/5 or touchpad wheel events to whichever
        # descendant is under the pointer. Dynamic Tk children and themed
        # controls can bypass a widget's own binding. Route them at root
        # level only when the pointer is inside this Items canvas.
        def route_items_wheel(event):
            # Tk's window manager can lag behind notebook selection during
            # tests, deiconify and resize. Route by actual selected pages,
            # then verify widget ancestry, not by winfo_ismapped().
            if (self.notebook.select() != str(self.unlock_tab) or
                    self.unlock_sections.select() != str(self.unlock_items_page)):
                return None
            widget = getattr(event, 'widget', None)
            while widget is not None:
                if str(widget) == str(canvas):
                    return wheel(event)
                widget = getattr(widget, 'master', None)
            return None
        self._unlock_global_wheel = route_items_wheel
        for sequence in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
            self.root.bind_all(sequence, route_items_wheel, add='+')
        self.unlock_canvas.bind(
            '<Configure>',
            lambda event: (
                canvas.itemconfigure(win, width=event.width),
                canvas.configure(scrollregion=canvas.bbox('all'))))
        self.root.after_idle(
            lambda: canvas.winfo_exists() and canvas.configure(
                scrollregion=canvas.bbox('all')))

        # Keep the Items canvas separate from the Flags canvas. Reassigning
        # a local named "canvas" here causes Tk's earlier wheel/geometry
        # closures to capture the *wrong* canvas (the original scroll bug).
        # Flag controls are individual on/off buttons beside every flag.
        # Build rows lazily when this page opens to keep GUI startup fast.
        flags_page = self.unlock_flags_page
        ttk.Label(flags_page, text='Story and event flags',
                  font=('Segoe UI Semibold', 14),
                  foreground=PALETTE['gold']).pack(anchor='w')
        ttk.Label(
            flags_page,
            text=('On / Off edits only the selected bit. Japanese candidate '
                  'addresses are editable for testing.'),
            style='Muted.TLabel', wraplength=1000).pack(
                anchor='w', pady=(1, 6))
        search_bar = ttk.Frame(flags_page)
        search_bar.pack(fill='x', pady=(0, 6))
        ttk.Label(search_bar, text='Find flag:').pack(side='left')
        self.unlock_flag_query = tk.StringVar()
        ttk.Entry(search_bar, textvariable=self.unlock_flag_query,
                  width=42).pack(side='left', padx=(6, 10))
        self.unlock_flag_counter = tk.StringVar()
        ttk.Label(search_bar, textvariable=self.unlock_flag_counter,
                  style='Muted.TLabel').pack(side='left')
        filters = ttk.Frame(flags_page)
        filters.pack(fill='x', pady=(0, 6))
        ttk.Label(filters, text='Type').pack(side='left', padx=(0, 5))
        self.unlock_flag_type = tk.StringVar(value='All types')
        self.unlock_flag_type_box = ttk.Combobox(
            filters, textvariable=self.unlock_flag_type, state='readonly',
            width=29, values=('All types',))
        self.unlock_flag_type_box.pack(side='left', padx=(0, 14))
        ttk.Label(filters, text='Subtype').pack(side='left', padx=(0, 5))
        self.unlock_flag_subtype = tk.StringVar(value='All subtypes')
        self.unlock_flag_subtype_box = ttk.Combobox(
            filters, textvariable=self.unlock_flag_subtype, state='readonly',
            width=29, values=('All subtypes',))
        self.unlock_flag_subtype_box.pack(side='left')
        self.unlock_flag_type_box.bind(
            '<<ComboboxSelected>>', self.on_unlock_flag_type_changed)
        self.unlock_flag_subtype_box.bind(
            '<<ComboboxSelected>>', lambda _e: self.filter_unlock_flags())

        flag_shell = ttk.Frame(flags_page)
        flag_shell.pack(fill='both', expand=True)
        flag_canvas = tk.Canvas(
            flag_shell, bg=PALETTE['background'], highlightthickness=0)
        scroll = ttk.Scrollbar(
            flag_shell, orient='vertical', command=flag_canvas.yview)
        flag_canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        flag_canvas.pack(side='left', fill='both', expand=True)
        body = ttk.Frame(flag_canvas, padding=(2, 0, 6, 8))
        window = flag_canvas.create_window((0, 0), window=body, anchor='nw')
        body.bind(
            '<Configure>',
            lambda _e: flag_canvas.configure(scrollregion=flag_canvas.bbox('all')))
        flag_canvas.bind(
            '<Configure>',
            lambda e: flag_canvas.itemconfigure(window, width=e.width))
        body.columnconfigure(0, weight=1)
        self.unlock_flag_canvas = flag_canvas
        self.unlock_flag_body = body
        self.unlock_flag_widgets = {}
        self.unlock_flag_sections = {}
        self._unlock_flag_pending = {}
        self._unlock_flag_jobs = {}
        self._unlock_flag_treeviews = {}
        self._unlock_flag_tree_by_key = {}
        self._unlock_flag_tree_cache = {}
        self._unlock_flag_tree_buttons = {}

        self.unlock_flag_detail = tk.StringVar(
            value='Click a flag name for full mapping evidence.')
        ttk.Label(
            flags_page, textvariable=self.unlock_flag_detail,
            style='Muted.TLabel', wraplength=1000).pack(
                anchor='w', pady=(6, 2))
        self.unlock_flag_feedback = tk.StringVar(value='')
        ttk.Label(
            flags_page, textvariable=self.unlock_flag_feedback,
            style='Muted.TLabel', wraplength=1000).pack(
                anchor='w', pady=(0, 3))
        self.unlock_flag_rows = {}
        self.unlock_flag_snapshot = {}
        self.unlock_flag_last_poll = 0.0
        self.unlock_flag_region = None
        self.unlock_flag_query.trace_add(
            'write', lambda *_: self.filter_unlock_flags())
        self.unlock_sections.bind(
            '<<NotebookTabChanged>>', self.on_unlock_section_changed)
        self.configure_unlock_flag_region()


    def _japan_unlock_controls_ready(self):
        """Source-backed Japanese fields write by default once RAM is attached."""
        return bool(
            self.active_version.key == 'japan'
            and self.jp_rdram is not None
            and getattr(self, 'game_pid', None) is not None
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus', 'recomp')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() in ('auto', self.jp_backend)
            and not getattr(self, '_connecting', False)
            and not getattr(self.args, 'read_only', False))

    def configure_unlock_region(self):
        """Retain the exact USA layout; swap address/read/write providers only."""
        japan = self.active_version.key == 'japan'
        usa_writable = bool(
            not japan and getattr(self.args, 'enable_hex_edit', False)
            and not getattr(self.args, 'read_only', False))
        self.unlock_intro_text.set(
            'Japan-0: 33/34 unlocks reported working in live gameplay. '
            'Only Sasuke battery 1 remains unverified (marked ?). '
            'Individual edits are immediate.'
            if japan else
            'Click any value to write it immediately to the original N64 RAM. '
            'The game may not refresh its inventory until an area or menu reload.')
        self.unlock_all_hint.set(
            'Japan: Unlock All writes all 33 live-tested entries; '
            'the unverified Sasuke battery byte is skipped.'
            if japan else
            'One-time edit; does not set story completion flags.')
        self.unlock_all_button.configure(
            text=(f'Unlock all mapped Japanese entries '
                  f'({len(japan_unlock_all_targets())})'
                  if japan else 'Unlock all mapped items, weapons and abilities'))
        self.unlock_all_button.state(
            ['!disabled'] if (self._japan_unlock_controls_ready()
                              if japan else usa_writable) else ['disabled'])
        for item in UNLOCKS:
            lead = japan_unlock_lead(item) if japan else item
            address = (
                'unknown' if lead is None else
                f'{lead.address:08X} ?' if japan and not lead.user_verified
                else f'{lead.address:08X}'
            )
            self.unlock_address_labels[item.address].configure(text=address)
            _state, controls = self.unlock_row_widgets[item.address]
            for value, button in controls.items():
                # Chain Pipe remains USA On [02] but is Japan On [01].
                wire = japan_unlock_wire_value(item, value) if japan else value
                label = item.levels[item.values.index(value)]
                button.configure(text=f'{label} [{wire:02X}]')
                button.state(['!disabled'] if usa_writable else ['disabled'])
            if item.quantity:
                self.unlock_count_buttons[item.address].state(
                    ['!disabled'] if usa_writable else ['disabled'])
                self.unlock_count_entries[item.address].configure(
                    state='normal' if usa_writable or not japan else 'disabled')
        self.unlock_last_poll = 0.0
        self.configure_unlock_flag_region()
        self.unlock_status.set(
            ('Japan-0: 33 of 34 entries user-verified; Sasuke battery 1 '
             'remains unverified. Connect to verified Japanese RAM to edit; '
             'automatic backend selection is supported.' if not self._japan_unlock_controls_ready()
             else 'Japan-0 unlock edits available on verified connection; '
                  'Sasuke battery 1 remains unverified.')
            if japan else
            'Connect to US Goemon in Recomp or Project64 to read and change flags.')
        self.refresh_unlocks(force=True)

    def refresh_japan_unlocks(self, *, force=False):
        """Read Japanese leads only; never substitute USA guest addresses."""
        if self.active_version.key != 'japan':
            return
        now = time.monotonic()
        if not force and now - self.unlock_last_poll < 0.8:
            return
        self.unlock_last_poll = now
        can_write = self._japan_unlock_controls_ready()
        self.unlock_all_button.state(
            ['!disabled'] if can_write else ['disabled'])
        for item in UNLOCKS:
            label, controls = self.unlock_row_widgets[item.address]
            lead = japan_unlock_lead(item)
            raw = None
            if lead is not None and self.jp_rdram is not None:
                try:
                    guest = self.jp_rdram.read_guest(lead.address, lead.width)
                    if len(guest) != lead.width:
                        raise OSError('Short Japanese unlock field read')
                    raw = int.from_bytes(guest, 'big')
                except (OSError, ValueError, PermissionError, RuntimeError):
                    pass
            display = (
                japan_unlock_display_value(item, raw) if raw is not None else None)
            label.configure(
                text=('unknown' if lead is None else
                      '—' if raw is None else f'0x{raw:02X}'),
                foreground=(PALETTE['teal'] if display is not None
                            and (display in item.values or item.quantity)
                            else PALETTE['warning']))
            for value, button in controls.items():
                button.state(
                    ['!disabled'] if can_write and lead is not None
                    else ['disabled'])
                button.configure(
                    style='Gold.TButton' if display is not None and display == value
                    else 'TButton')
            if item.quantity:
                self.unlock_count_buttons[item.address].state(
                    ['!disabled'] if can_write and lead is not None
                    else ['disabled'])
                self.unlock_count_entries[item.address].configure(
                    state='normal' if can_write and lead is not None
                    else 'disabled')
                if raw is not None:
                    try:
                        focused_path = str(self.root.tk.call('focus'))
                    except tk.TclError:
                        focused_path = ''
                    if focused_path != str(self.unlock_count_entries[item.address]):
                        self.unlock_count_inputs[item.address].set(f'{raw:02X}')
        self.refresh_unlock_flags(force=force)

    def unlock_all_items(self):
        if self.active_version.key == 'japan':
            try:
                changed, total = self.apply_japan_unlocks(japan_unlock_all_targets())
                self.unlock_status.set(
                    f'Japan-0: {changed} changed / {total} mapped entries. '
                    'Only Sasuke battery 1 skipped (not live-verified).')
                self.refresh_unlocks(force=True)
            except (OSError, ValueError, RuntimeError, PermissionError) as exc:
                self.unlock_status.set(f'Japanese unlock-all failed: {exc}')
            return
        if self.mem is None:
            self.unlock_status.set('Connect to a game before unlocking items.')
            return
        if getattr(self.args, 'read_only', False) or not self.args.enable_hex_edit:
            self.unlock_status.set('Unlock all blocked in read-only mode.')
            return
        from practice.checkpoints import _ensure_capture_safe
        try:
            with self.value_freezes.guard:
                _ensure_capture_safe(self.mem)
                for lock in self.value_freezes.locks.values():
                    if any(lock.address <= item.address < lock.address + len(lock.value)
                           for item in UNLOCKS):
                        raise ValueError('Stop overlapping freezes before unlocking items')
                changed, total = unlock_all_known(self.mem)
            self.unlock_status.set(f'Unlock all: {changed} changed / {total} entries checked. '
                                   'Story flags untouched. Some changes require a scene refresh.')
            self.last_inspect_at = 0.0
            self.refresh_unlocks(force=True)
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.unlock_status.set(f'Unlock all stopped: {exc}. Previous writes may remain.')

    def set_unlock(self, unlock: Unlock, value: int) -> None:
        """One click = regional single-byte write; never reuse another ROM address."""
        if self.active_version.key == 'japan':
            lead = japan_unlock_lead(unlock)
            if lead is None:
                self.unlock_status.set(
                    f'{unlock.label}: Japanese address unknown; no write.')
                return
            try:
                actual = normalize_unlock_value(unlock, value)
                changed, _ = self.apply_japan_unlocks(((unlock, actual),))
                self.unlock_status.set(
                    f'Japan-0 {unlock.label}: '
                    f'0x{japan_unlock_wire_value(unlock, actual):02X} '
                    + ('[live-verified] ' if lead.user_verified else
                       '[UNVERIFIED battery candidate] ')
                    + ('(written)' if changed else '(unchanged)'))
                self.refresh_unlocks(force=True)
            except (OSError, ValueError, RuntimeError, PermissionError) as exc:
                self.unlock_status.set(
                    f'Japan-0 {unlock.label}: write failed — {exc}')
            return
        if not self.mem:
            self.unlock_status.set('Disconnected. Connect before editing unlocks.')
            return
        if not getattr(self.args, 'enable_hex_edit', False):
            self.unlock_status.set('Memory writing disabled. Start with --enable-hex-edit or Run.bat.')
            return
        try:
            old = read_unlock(self.mem, unlock)
            actual = normalize_unlock_value(unlock, value)
            changed = write_unlock(self.mem, unlock, actual)
            suffix = ' (clamped)' if actual != value else ''
            self.unlock_status.set(f'{unlock.label}: 0x{old:02X} → 0x{actual:02X}' + suffix +
                                   (' (verified)' if changed else ' (unchanged)'))
            if changed:
                self.append_event(f'USER FLAG WRITE 0x{unlock.address:08X} {unlock.label}: {old:02X} -> {value:02X}')
                self.last_inspect_at = 0.0
            self.refresh_unlocks(force=True)
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.unlock_status.set(f'{unlock.label}: write failed — {exc}')

    def set_unlock_hex(self, field: Unlock, text: str) -> None:
        """Fish counts are actual quantities, not boolean acquired flags."""
        try:
            if not field.quantity:
                raise ValueError('Only count fields support arbitrary 00..FF hex')
            target=parse_hex(text,1)[0]
            self.set_unlock(field, normalize_unlock_value(field, target))
        except ValueError as exc:
            self.unlock_status.set(f'{field.label}: invalid count — {exc}')

    def refresh_unlocks(self, *, force=False) -> None:
        """Refresh region-specific values without reusing USA addresses."""
        if self.active_version.key == 'japan':
            self.refresh_japan_unlocks(force=force)
            return
        now = time.monotonic()
        if not force and now - self.unlock_last_poll < 0.5:
            return
        self.unlock_last_poll = now
        values = {}
        # Retain v0.11.50 visible-tab optimisation. Folder actions still
        # request an explicit forced refresh after an actual bit edit.
        if force:
            self.refresh_story_progress()
        # Tk's 'focus' returns the widget path directly. root.focus_get() calls
        # _nametowidget() and raises KeyError('popdown') for some ttk dropdowns
        # (observed on Python 3.14 / Windows).
        try:
            focused_path = str(self.root.tk.call('focus'))
        except tk.TclError:
            focused_path = ''
        for field in UNLOCKS:
            state, controls = self.unlock_row_widgets[field.address]
            try:
                raw = read_unlock(self.mem, field) if self.mem else None
            except (OSError, ValueError):
                raw = None
            values[field.address] = raw
            if field.quantity and raw is not None:
                var=self.unlock_count_inputs.get(field.address)
                # Refresh the input unless the user is actively typing into it.
                entry = self.unlock_count_entries.get(field.address)
                if var is not None and (entry is None or focused_path != str(entry)):
                    var.set(f'{raw:02X}')
            state.configure(text='—' if raw is None else f'0x{raw:02X}',
                            foreground=PALETTE['teal'] if (raw in field.values or (field.quantity and raw is not None)) else PALETTE['warning'])
            for value, button in controls.items():
                button.configure(style='Gold.TButton' if raw == value else 'TButton')
        self.refresh_unlock_flags(force=force)

    def on_unlock_section_changed(self, _event=None):
        if self.unlock_sections.select() == str(self.unlock_flags_page):
            self._ensure_unlock_flag_widgets()
            self.filter_unlock_flags()
            self.refresh_unlock_flags(force=True)

    def _ensure_unlock_flag_widgets(self):
        """Build inexpensive, initially collapsed type/subtype folders only.

        Hundreds of nested ttk controls are expensive to create. A folder's
        individual On/Off rows are built on its first explicit expansion.
        """
        if (self.unlock_sections.select() != str(self.unlock_flags_page)
                or self.unlock_flag_sections):
            return
        parent = self.unlock_flag_body
        canvas = self.unlock_flag_canvas
        self.unlock_flag_section_rows = {}
        for flag in self.unlock_flag_rows.values():
            self.unlock_flag_section_rows.setdefault(
                (flag.group, flag.subtype), []).append(flag)
        self.unlock_flag_section_bodies = {}
        self.unlock_flag_section_buttons = {}
        self.unlock_flag_expanded = set()
        self.unlock_flag_auto_expanded = set()

        def wheel(event):
            if getattr(event, 'num', None) in (4, 5):
                delta = -1 if event.num == 4 else 1
            else:
                motion = getattr(event, 'delta', 0)
                delta = (-max(1, abs(motion) // 120) if motion > 0 else
                         max(1, abs(motion) // 120) if motion < 0 else 0)
            if delta:
                canvas.yview_scroll(delta, 'units')
            return 'break'

        self._unlock_flag_wheel = wheel
        def bind_wheel(widget):
            for sequence in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                widget.bind(sequence, wheel, add='+')

        for index, (section, flags) in enumerate(
                self.unlock_flag_section_rows.items()):
            header = ttk.Frame(
                parent, style='FlagGroup.TFrame', padding=(7, 3))
            header.grid(row=index * 2, column=0, sticky='ew', pady=(3, 1))
            header.columnconfigure(0, weight=1)
            button = ttk.Button(
                header,
                text=f'▸ {section[0]} / {section[1]}  ({len(flags)})',
                command=lambda key=section:
                    self.toggle_unlock_flag_section(key))
            button.grid(row=0, column=0, sticky='ew')
            content = ttk.Frame(parent, style='FlagGroup.TFrame')
            content.grid(row=index * 2 + 1, column=0, sticky='ew')
            content.columnconfigure(0, weight=1)
            content.grid_remove()
            self.unlock_flag_sections[section] = header
            self.unlock_flag_section_bodies[section] = content
            self.unlock_flag_section_buttons[section] = button
            bind_wheel(header)
            bind_wheel(button)
            bind_wheel(content)

    def _set_unlock_flag_section_expanded(
            self, section, expanded, *, automatic=False):
        """Open/close a folder without populating any other folder."""
        if section not in self.unlock_flag_sections:
            return
        if expanded:
            if section not in self.unlock_flag_expanded:
                content = self.unlock_flag_section_bodies[section]
                self.unlock_flag_expanded.add(section)
                content.grid()
                if automatic:
                    matching = {
                        flag.key for flag in self.unlock_flag_section_rows[section]
                        if getattr(self, '_unlock_flag_match_cache', {}).get(
                            flag.key, False)}
                    self._build_unlock_flag_section_rows(
                        section, only_keys=matching)
                else:
                    self._build_unlock_flag_section_rows(section)
            if automatic:
                self.unlock_flag_auto_expanded.add(section)
            else:
                self.unlock_flag_auto_expanded.discard(section)
        else:
            self._cancel_unlock_flag_batch(section)
            self.unlock_flag_expanded.discard(section)
            self.unlock_flag_auto_expanded.discard(section)
            self.unlock_flag_section_bodies[section].grid_remove()
        button = self.unlock_flag_section_buttons[section]
        flags = self.unlock_flag_section_rows[section]
        button.configure(
            text=(('▾ ' if expanded else '▸ ') + section[0] + ' / ' +
                  section[1] + f'  ({len(flags)})'))
        self.unlock_flag_canvas.configure(
            scrollregion=self.unlock_flag_canvas.bbox('all'))

    def toggle_unlock_flag_section(self, section):
        if section not in self.unlock_flag_sections:
            return
        self._set_unlock_flag_section_expanded(
            section, section not in self.unlock_flag_expanded)
        self.filter_unlock_flags()
        self.refresh_unlock_flags(force=True)

    def _cancel_unlock_flag_batch(self, section):
        """Stop deferred row construction for a closed or invalidated folder."""
        self._unlock_flag_pending.pop(section, None)
        job = self._unlock_flag_jobs.pop(section, None)
        if job is not None:
            try:
                self.root.after_cancel(job)
            except tk.TclError:
                pass

    def _build_unlock_flag_section_rows(self, section, *, only_keys=None):
        """Keep small-folder buttons; use one Treeview for large folders.

        Rendering hundreds of labels, frames and buttons synchronously blocks
        Tk's event loop. The first four rows of a large folder are available
        immediately; subsequent batches yield to paint and input events.
        """
        if section not in self.unlock_flag_expanded:
            return
        if len(self.unlock_flag_section_rows[section]) > _FLAG_FOLDER_EAGER_LIMIT:
            self._ensure_unlock_flag_tree(section)
            return
        missing = [
            (index, flag)
            for index, flag in enumerate(self.unlock_flag_section_rows[section])
            if (flag.key not in self.unlock_flag_widgets and
                (only_keys is None or flag.key in only_keys))
        ]
        if self._unlock_flag_pending.get(section) == missing:
            return
        self._cancel_unlock_flag_batch(section)
        if not missing:
            return
        if (len(self.unlock_flag_section_rows[section]) <= _FLAG_FOLDER_EAGER_LIMIT
                or only_keys is not None and len(missing) <= _FLAG_FOLDER_EAGER_LIMIT):
            for index, flag in missing:
                self._create_unlock_flag_row(section, index, flag)
        else:
            self._unlock_flag_pending[section] = missing
            self._populate_unlock_flag_batch(section)

    def _populate_unlock_flag_batch(self, section):
        """Consume at most one small batch, then give Tk time to draw."""
        job = self._unlock_flag_jobs.pop(section, None)
        if job is not None:
            try:
                self.root.after_cancel(job)
            except tk.TclError:
                pass
        pending = self._unlock_flag_pending.get(section)
        if not pending or section not in self.unlock_flag_expanded:
            self._unlock_flag_pending.pop(section, None)
            return
        batch = pending[:_FLAG_FOLDER_BATCH_SIZE]
        del pending[:_FLAG_FOLDER_BATCH_SIZE]
        for index, flag in batch:
            self._create_unlock_flag_row(section, index, flag)
        if pending:
            self._unlock_flag_jobs[section] = self.root.after(
                1, lambda key=section: self._populate_unlock_flag_batch(key))
        else:
            self._unlock_flag_pending.pop(section, None)

    def _ensure_unlock_flag_tree(self, section):
        """Build one bounded Treeview for a large folder, not 8+ Tk widgets/bit.

        Every flag remains directly addressable through its own Off/On cells.
        Only the exact clicked cell can request a single-bit checked write.
        No per-row frames, buttons, geometry recalculations or wheel binds.
        """
        if section in self._unlock_flag_treeviews:
            return
        flags = self.unlock_flag_section_rows[section]
        body = self.unlock_flag_section_bodies[section]
        holder = ttk.Frame(body, style='FlagRow.TFrame', padding=5)
        holder.grid(row=0, column=0, sticky='ew')
        holder.columnconfigure(0, weight=1)
        ttk.Label(
            holder,
            text='Select a flag or click its Off / On cell to edit that bit. '
                 'Candidate mappings are not verified gameplay events.',
            style='FlagMeta.TLabel').grid(row=0, column=0, sticky='w')
        columns = ('flag', 'address', 'value', 'off', 'on')
        table = ttk.Treeview(
            holder, columns=columns, show='headings', selectmode='browse',
            height=min(14, len(flags)))
        for key, title, width, stretch in (
                ('flag', 'Named flag', 315, True),
                ('address', 'Address · mask', 155, False),
                ('value', 'State', 65, False),
                ('off', 'Off', 55, False),
                ('on', 'On', 55, False)):
            table.heading(key, text=title)
            table.column(key, width=width, minwidth=width,
                         stretch=stretch, anchor='w' if key == 'flag' else 'center')
        scrollbar = ttk.Scrollbar(holder, orient='vertical',
                                  command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.grid(row=1, column=0, sticky='nsew')
        scrollbar.grid(row=1, column=1, sticky='ns')
        toolbar = ttk.Frame(holder, style='FlagRow.TFrame')
        toolbar.grid(row=2, column=0, sticky='w', pady=(4, 0))
        off = ttk.Button(toolbar, text='Off selected',
                         command=lambda key=section:
                             self._activate_unlock_flag_tree_selection(key, 'Clear'))
        on = ttk.Button(toolbar, text='On selected',
                        command=lambda key=section:
                            self._activate_unlock_flag_tree_selection(key, 'Set'))
        off.pack(side='left')
        on.pack(side='left', padx=(6, 0))
        off.state(['disabled'])
        on.state(['disabled'])
        self._unlock_flag_treeviews[section] = table
        self._unlock_flag_tree_buttons[section] = (off, on)
        for flag in flags:
            self._unlock_flag_tree_by_key[flag.key] = table
            table.insert('', 'end', iid=flag.key,
                         values=(flag.label,
                                 f'0x{flag.address:08X} · 0x{flag.mask:02X}',
                                 '—', '—', '—'))
            self._update_unlock_flag_tree_row(flag, self.unlock_flag_snapshot)

        def clicked(event):
            if table.identify_region(event.x, event.y) != 'cell':
                return
            key = table.identify_row(event.y)
            column = table.identify_column(event.x)
            if not key:
                return
            if column in ('#4', '#5'):
                self._activate_unlock_flag_tree_cell(
                    section, key, 'Clear' if column == '#4' else 'Set')
            else:
                self.show_unlock_flag_detail(key)

        def selected(_event=None):
            item = table.selection()
            if item:
                self.show_unlock_flag_detail(item[0])
            self._refresh_unlock_flag_tree_selection(section)

        table.bind('<ButtonRelease-1>', clicked, add='+')
        table.bind('<<TreeviewSelect>>', selected, add='+')
        self._sync_unlock_flag_tree_filter(
            section, getattr(self, '_unlock_flag_match_cache', {}))
        self._refresh_unlock_flag_tree_selection(section)

    def _sync_unlock_flag_tree_filter(self, section, matches):
        """Detach filtered rows; keep their records and widget cached."""
        tree = self._unlock_flag_treeviews.get(section)
        if tree is None:
            return
        wanted = [
            flag.key for flag in self.unlock_flag_section_rows[section]
            if matches.get(flag.key, True)]
        if tuple(tree.get_children()) == tuple(wanted):
            return
        allowed = set(wanted)
        for key in tuple(tree.get_children()):
            if key not in allowed:
                tree.detach(key)
        for index, key in enumerate(wanted):
            # move also reattaches a detached item, without rebuilding it.
            tree.move(key, '', index)

    def _activate_unlock_flag_tree_selection(self, section, action):
        tree = self._unlock_flag_treeviews.get(section)
        if tree is None:
            return
        chosen = tree.selection()
        if chosen:
            self._activate_unlock_flag_tree_cell(section, chosen[0], action)

    def _activate_unlock_flag_tree_cell(self, section, key, action):
        """Apply a click only to an existing, visible, writable flag row."""
        tree = self._unlock_flag_treeviews.get(section)
        flag = self.unlock_flag_rows.get(key)
        if (tree is None or flag is None or
                section not in self.unlock_flag_expanded or
                (flag.group, flag.subtype) != section or
                key not in tree.get_children() or
                action not in ('Set', 'Clear')):
            return
        if (self.unlock_flag_snapshot.get(key) is None or
                not self._can_write_unlock_flag(flag)):
            self.unlock_flag_feedback.set(
                'Flag write blocked: connect a writable game memory reader.')
            return
        self.set_unlock_flag(key, action)

    def _update_unlock_flag_tree_row(self, flag, values):
        table = self._unlock_flag_tree_by_key.get(flag.key)
        if table is None:
            return
        raw = values.get(flag.key)
        state = ('—' if raw is None else
                 'On' if raw & flag.mask else 'Off')
        writable = bool(raw is not None and self._can_write_unlock_flag(flag))
        stamp = (state, writable)
        if self._unlock_flag_tree_cache.get(flag.key) == stamp:
            return
        self._unlock_flag_tree_cache[flag.key] = stamp
        table.item(
            flag.key, values=(
                flag.label,
                f'0x{flag.address:08X} · 0x{flag.mask:02X}',
                state,
                'Off' if writable else '—',
                'On' if writable else '—'))

    def _refresh_unlock_flag_tree_selection(self, section):
        table = self._unlock_flag_treeviews.get(section)
        if table is None:
            return
        chosen = table.selection()
        key = chosen[0] if chosen else None
        flag = self.unlock_flag_rows.get(key)
        enabled = bool(
            flag is not None and
            self.unlock_flag_snapshot.get(key) is not None and
            self._can_write_unlock_flag(flag) and
            key in table.get_children())
        for button in self._unlock_flag_tree_buttons[section]:
            button.state(['!disabled'] if enabled else ['disabled'])

    def _create_unlock_flag_row(self, section, index, flag):
        """One row; use the most recent cached event bank without re-reading it."""
        parent = self.unlock_flag_section_bodies[section]
        wheel = self._unlock_flag_wheel
        frame = ttk.Frame(
            parent, style='FlagRow.TFrame', padding=(10, 5))
        frame.grid(row=index, column=0, sticky='ew', pady=(0, 2))
        frame.columnconfigure(0, weight=1)
        name = ttk.Label(
            frame, text=flag.label, style='FlagName.TLabel',
            wraplength=520)
        name.grid(row=0, column=0, sticky='w', pady=(1, 0))
        address = ttk.Label(
            frame, text=f'{flag.address:08X} · {flag.mask:02X}',
            style='FlagAddress.TLabel')
        address.grid(row=0, column=1, padx=(8, 10), sticky='w')
        value = tk.StringVar(value='—')
        shown = ttk.Label(
            frame, textvariable=value, style='FlagState.TLabel',
            width=7)
        shown.grid(row=0, column=2, padx=(0, 6), sticky='w')
        controls = ttk.Frame(frame, style='FlagRow.TFrame')
        controls.grid(row=0, column=3, sticky='e')
        off = ttk.Button(
            controls, text='Off', width=5, style='Flag.TButton',
            command=lambda key=flag.key: self.set_unlock_flag(key, 'Clear'))
        on = ttk.Button(
            controls, text='On', width=5, style='Flag.TButton',
            command=lambda key=flag.key: self.set_unlock_flag(key, 'Set'))
        off.pack(side='left')
        on.pack(side='left', padx=(5, 0))
        off.state(['disabled'])
        on.state(['disabled'])
        source = ttk.Label(
            frame, text=f'{flag.source} · {flag.group} / {flag.subtype}',
            style='FlagMeta.TLabel')
        source.grid(row=1, column=0, columnspan=4,
                    sticky='w', pady=(1, 0))
        for label in (name, source, address):
            label.bind(
                '<Button-1>',
                lambda _event, key=flag.key:
                    self.show_unlock_flag_detail(key))
        self.unlock_flag_widgets[flag.key] = {
            'frame': frame, 'state': value,
            'state_label': shown, 'off': off, 'on': on}
        for widget in (
                frame, name, address, shown, controls, off, on, source):
            for sequence in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                widget.bind(sequence, wheel, add='+')
        self._update_unlock_flag_row(flag, self.unlock_flag_snapshot)

    def show_unlock_flag_detail(self, key):
        flag = self.unlock_flag_rows.get(key)
        if flag:
            self.unlock_flag_detail.set(
                f'{flag.label} — {flag.evidence}. '
                'Use On/Off beside this flag to change its masked bit.')

    def configure_unlock_flag_region(self):
        """Rebuild per-flag controls with the correct regional addresses."""
        region = self.active_version.key
        if self.unlock_flag_region == region:
            return
        for section in tuple(self._unlock_flag_pending):
            self._cancel_unlock_flag_batch(section)
        for widgets in self.unlock_flag_widgets.values():
            widgets['frame'].destroy()
        for header in self.unlock_flag_sections.values():
            header.destroy()
        for body in getattr(self, 'unlock_flag_section_bodies', {}).values():
            body.destroy()
        self.unlock_flag_widgets = {}
        self.unlock_flag_sections = {}
        self._unlock_flag_treeviews = {}
        self._unlock_flag_tree_by_key = {}
        self._unlock_flag_tree_cache = {}
        self._unlock_flag_tree_buttons = {}
        self.unlock_flag_section_rows = {}
        self.unlock_flag_section_bodies = {}
        self.unlock_flag_section_buttons = {}
        self.unlock_flag_expanded = set()
        self.unlock_flag_auto_expanded = set()
        self.unlock_flag_region = region
        self.unlock_flag_rows = {
            flag.key: flag for flag in flags_for_region(region)}
        self.unlock_flag_snapshot = {}
        self.unlock_flag_last_poll = 0.0
        self.unlock_flag_feedback.set('')
        self.unlock_flag_detail.set(
            'Click a flag name for full mapping evidence.')
        categories = tuple(dict.fromkeys(
            flag.group for flag in self.unlock_flag_rows.values()))
        self.unlock_flag_type_box.configure(
            values=('All types',) + categories)
        if self.unlock_flag_type.get() not in ('All types',) + categories:
            self.unlock_flag_type.set('All types')
        self._refresh_unlock_flag_subtypes()
        self._ensure_unlock_flag_widgets()
        self.filter_unlock_flags()

    def _refresh_unlock_flag_subtypes(self):
        """Only list subtypes within the selected type."""
        selected_type = self.unlock_flag_type.get()
        subtypes = tuple(dict.fromkeys(
            flag.subtype for flag in self.unlock_flag_rows.values()
            if selected_type == 'All types' or flag.group == selected_type))
        values = ('All subtypes',) + subtypes
        self.unlock_flag_subtype_box.configure(values=values)
        if self.unlock_flag_subtype.get() not in values:
            self.unlock_flag_subtype.set('All subtypes')

    def on_unlock_flag_type_changed(self, _event=None):
        self.unlock_flag_subtype.set('All subtypes')
        self._refresh_unlock_flag_subtypes()
        self.filter_unlock_flags()

    def filter_unlock_flags(self):
        """Filter collapsed folders; text searches reveal matching rows."""
        query = self.unlock_flag_query.get().strip().casefold()
        selected_type = self.unlock_flag_type.get()
        selected_subtype = self.unlock_flag_subtype.get()
        visible = 0
        section_matches = {}
        row_matches = {}
        for flag in self.unlock_flag_rows.values():
            text = ' '.join((
                flag.label, flag.group, flag.subtype, flag.source,
                flag.evidence, f'0x{flag.address:08X}',
                f'0x{flag.mask:02X}'))
            match = (query in text.casefold()
                     and (selected_type == 'All types'
                          or flag.group == selected_type)
                     and (selected_subtype == 'All subtypes'
                          or flag.subtype == selected_subtype))
            row_matches[flag.key] = match
            if match:
                visible += 1
                section_matches[(flag.group, flag.subtype)] = True
        self._unlock_flag_match_cache = row_matches
        if query:
            for section in section_matches:
                if section in self.unlock_flag_sections:
                    if section not in self.unlock_flag_expanded:
                        self._set_unlock_flag_section_expanded(
                            section, True, automatic=True)
                    else:
                        self._build_unlock_flag_section_rows(
                            section, only_keys={
                                flag.key for flag in
                                self.unlock_flag_section_rows[section]
                                if row_matches[flag.key]})
        else:
            for section in tuple(self.unlock_flag_auto_expanded):
                self._set_unlock_flag_section_expanded(section, False)
            # A manually expanded folder may have been only partly built
            # while a search or type filter was active.
            for section in section_matches:
                if section in self.unlock_flag_expanded:
                    self._build_unlock_flag_section_rows(section)
        for section in tuple(self._unlock_flag_pending):
            if section not in section_matches:
                self._cancel_unlock_flag_batch(section)
        for section in tuple(self._unlock_flag_treeviews):
            self._sync_unlock_flag_tree_filter(section, row_matches)
            self._refresh_unlock_flag_tree_selection(section)
        for flag in self.unlock_flag_rows.values():
            widgets = self.unlock_flag_widgets.get(flag.key)
            if widgets is not None:
                if row_matches[flag.key]:
                    if widgets['frame'].winfo_manager() != 'grid':
                        widgets['frame'].grid()
                elif widgets['frame'].winfo_manager() == 'grid':
                    widgets['frame'].grid_remove()
        for section, header in self.unlock_flag_sections.items():
            body = self.unlock_flag_section_bodies[section]
            if section_matches.get(section):
                if header.winfo_manager() != 'grid':
                    header.grid()
                if section in self.unlock_flag_expanded:
                    if body.winfo_manager() != 'grid':
                        body.grid()
                elif body.winfo_manager() == 'grid':
                    body.grid_remove()
            else:
                if header.winfo_manager() == 'grid':
                    header.grid_remove()
                if body.winfo_manager() == 'grid':
                    body.grid_remove()
        self.unlock_flag_counter.set(
            f'{visible} / {len(self.unlock_flag_rows)} named bits')
        if self.unlock_flag_sections:
            self.unlock_flag_canvas.configure(
                scrollregion=self.unlock_flag_canvas.bbox('all'))

    def _can_write_unlock_flag(self, flag):
        if flag is None:
            return False
        # Evidence/provenance is never a write gate for mapped crosswalk bits.
        if self.active_version.key == 'japan':
            return self._japan_unlock_controls_ready()
        return bool(
            self.mem is not None and
            getattr(self.args, 'enable_hex_edit', False) and
            not getattr(self.args, 'read_only', False))

    def refresh_unlock_flags(self, *, force=False):
        """Read the one event bank and refresh every visible on/off control."""
        if not force and self.unlock_sections.select() != str(self.unlock_flags_page):
            return
        now = time.monotonic()
        if not force and now - self.unlock_flag_last_poll < 0.7:
            return
        self.unlock_flag_last_poll = now
        region = self.active_version.key
        if region != self.unlock_flag_region:
            self.configure_unlock_flag_region()
        self._ensure_unlock_flag_widgets()
        reader = self.jp_rdram if region == 'japan' else self.mem
        try:
            values = read_flag_bytes(
                reader, region, self.unlock_flag_rows.values())
            if reader is None:
                self.unlock_flag_feedback.set(
                    'Disconnected. Connect to the game to enable On/Off.')
            elif self.unlock_flag_feedback.get().startswith(
                    ('Disconnected', 'Flag bank unavailable')):
                self.unlock_flag_feedback.set('Live event flags connected.')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            values = {}
            self.unlock_flag_feedback.set(f'Flag bank unavailable: {exc}')
        self.unlock_flag_snapshot = values
        for flag in self.unlock_flag_rows.values():
            self._update_unlock_flag_row(flag, values)
        for section in self._unlock_flag_treeviews:
            self._refresh_unlock_flag_tree_selection(section)

    def _update_unlock_flag_row(self, flag, values):
        """Update a constructed row only when its effective state changes."""
        widgets = self.unlock_flag_widgets.get(flag.key)
        if widgets is None:
            self._update_unlock_flag_tree_row(flag, values)
            return
        raw = values.get(flag.key)
        state = ('—' if raw is None else
                 'On' if raw & flag.mask else 'Off')
        enabled = bool(raw is not None and self._can_write_unlock_flag(flag))
        stamp = (state, enabled)
        if widgets.get('last_update') == stamp:
            return
        widgets['last_update'] = stamp
        widgets['state'].set(state)
        widgets['state_label'].configure(
            foreground=(PALETTE['teal'] if state == 'On'
                        else PALETTE['warning'] if state == 'Off'
                        else PALETTE['muted']))
        for target, button in (
                ('Off', widgets['off']), ('On', widgets['on'])):
            button.state(['!disabled'] if enabled else ['disabled'])
            button.configure(
                style=('FlagOn.TButton' if target == 'On'
                       else 'FlagOff.TButton')
                if raw is not None and state == target
                else 'Flag.TButton')

    def set_unlock_flag(self, key, target):
        """One-click per-row On/Off; only the requested bit may change."""
        flag = self.unlock_flag_rows.get(key)
        try:
            if flag is None:
                raise ValueError('The selected flag is not mapped in this region')
            if not self._can_write_unlock_flag(flag):
                raise PermissionError(
                    'Connect with memory writes enabled; read-only mode blocks editing')
            expected = self.unlock_flag_snapshot.get(flag.key)
            if expected is None:
                raise RuntimeError('Displayed flag byte unavailable; refresh first')
            if self.active_version.key == 'japan':
                changed = write_japan_crosswalk_flag(
                    self.write_japan_raw_bytes, flag, target, expected)
            else:
                # Reuse Story Progress masked CAS to preserve adjacent bits.
                with self.value_freezes.guard:
                    if any(lock.address <= flag.address < lock.address + len(lock.value)
                           for lock in self.value_freezes.locks.values()):
                        raise RuntimeError('Stop the overlapping freeze before editing')
                    changed = write_story_value(
                        self.mem, flag.key, target, bytes((expected,)))
            state = 'On' if target == 'Set' else 'Off'
            self.unlock_status.set(
                f'{flag.label}: {state}' +
                (' (written)' if changed else ' (unchanged)'))
            self.unlock_flag_feedback.set(
                f'{flag.label}: {state}' +
                (' written' if changed else ' unchanged'))
            if changed:
                self.append_event(
                    f'USER EVENT BIT {self.active_version.key.upper()} '
                    f'0x{flag.address:08X} mask 0x{flag.mask:02X}: {target}')
                self.last_inspect_at = 0.0
            self.refresh_unlock_flags(force=True)
            self.refresh_story_progress()
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.unlock_status.set(
                f'{flag.label if flag else "Event flag"}: blocked — {exc}')
            self.unlock_flag_feedback.set(str(exc))
            self.refresh_unlock_flags(force=True)
