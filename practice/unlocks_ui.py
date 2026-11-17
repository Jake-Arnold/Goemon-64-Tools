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
        ttk.Label(intro, text='Unlocks, weapons and upgrades', font=('Segoe UI Semibold', 16),
                  foreground=PALETTE['gold']).pack(anchor='w')
        ttk.Label(intro, textvariable=self.unlock_intro_text,
                  style='Muted.TLabel', wraplength=1050).pack(anchor='w', pady=(4, 0))
        self.unlock_status_label = ttk.Label(tab, textvariable=self.unlock_status)
        self.unlock_status_label.pack(fill='x', pady=(0, 8))
        self.unlock_sections = ttk.Notebook(tab)
        self.unlock_sections.pack(fill='both', expand=True)
        self.unlock_items_page = ttk.Frame(self.unlock_sections, padding=(0, 5))
        self.unlock_flags_page = ttk.Frame(self.unlock_sections, padding=(0, 5))
        self.unlock_sections.add(self.unlock_items_page, text='Items & equipment')
        self.unlock_sections.add(self.unlock_flags_page, text='Story & event flags')
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

        # The second page uses a single searchable table instead of repeating
        # dozens of per-row controls. The original 34 item buttons are intact.
        flags_page = self.unlock_flags_page
        ttk.Label(flags_page, text='Story and event flags',
                  font=('Segoe UI Semibold', 14),
                  foreground=PALETTE['gold']).pack(anchor='w')
        ttk.Label(
            flags_page,
            text=('Each named saved event is one masked bit. Set/Clear edits '
                  'only that bit, not neighbouring flags or Start-menu items. '
                  'Japanese crosswalk candidates can also be Set/Cleared for live '
                  'testing. Editing a flag does not replay the cutscene or reward.'),
            style='Muted.TLabel', wraplength=1000).pack(anchor='w', pady=(3, 8))
        search_bar = ttk.Frame(flags_page)
        search_bar.pack(fill='x', pady=(0, 6))
        ttk.Label(search_bar, text='Find flag:').pack(side='left')
        self.unlock_flag_query = tk.StringVar()
        ttk.Entry(search_bar, textvariable=self.unlock_flag_query,
                  width=42).pack(side='left', padx=(6, 10))
        self.unlock_flag_counter = tk.StringVar()
        ttk.Label(search_bar, textvariable=self.unlock_flag_counter,
                  style='Muted.TLabel').pack(side='left')
        tree_shell = ttk.Frame(flags_page)
        tree_shell.pack(fill='both', expand=True)
        columns = ('group', 'address', 'mask', 'value', 'source')
        tree = ttk.Treeview(
            tree_shell, columns=columns, show='tree headings', height=15,
            selectmode='browse')
        tree.heading('#0', text='Flag')
        tree.column('#0', width=290, stretch=True)
        for key, title, width in (
            ('group', 'Group', 135), ('address', 'JP / USA address', 130),
            ('mask', 'Mask', 65), ('value', 'Observed', 130),
            ('source', 'Mapping status', 155)):
            tree.heading(key, text=title)
            tree.column(key, width=width, stretch=key == 'group')
        tree.pack(side='left', fill='both', expand=True)
        vertical = ttk.Scrollbar(tree_shell, orient='vertical',
                                 command=tree.yview)
        vertical.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vertical.set)
        self.unlock_flag_tree = tree
        self.unlock_flag_detail = tk.StringVar(
            value='Select a mapped bit to see its evidence.')
        ttk.Label(flags_page, textvariable=self.unlock_flag_detail,
                  style='Muted.TLabel', wraplength=1000).pack(
                      anchor='w', pady=(8, 6))
        actions = ttk.Frame(flags_page)
        actions.pack(fill='x')
        self.unlock_flag_set = ttk.Button(
            actions, text='Set / On',
            command=lambda: self.set_unlock_flag('Set'))
        self.unlock_flag_clear = ttk.Button(
            actions, text='Clear / Off',
            command=lambda: self.set_unlock_flag('Clear'))
        self.unlock_flag_set.pack(side='left')
        self.unlock_flag_clear.pack(side='left', padx=(8, 0))
        self.unlock_flag_set.state(['disabled'])
        self.unlock_flag_clear.state(['disabled'])
        self.unlock_flag_feedback = tk.StringVar(value='')
        ttk.Label(actions, textvariable=self.unlock_flag_feedback,
                  style='Muted.TLabel').pack(side='left', padx=(12, 0))
        self.unlock_flag_rows = {}
        self.unlock_flag_snapshot = {}
        self.unlock_flag_last_poll = 0.0
        self.unlock_flag_region = None
        self.unlock_flag_query.trace_add(
            'write', lambda *_: self.filter_unlock_flags())
        self.unlock_flag_tree.bind(
            '<<TreeviewSelect>>', self.select_unlock_flag)
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
            self.refresh_unlock_flags(force=True)

    def configure_unlock_flag_region(self):
        """Repopulate the same UI with source-qualified addresses on switch."""
        region = self.active_version.key
        if self.unlock_flag_region == region:
            return
        self.unlock_flag_region = region
        self.unlock_flag_rows = {flag.key: flag for flag in flags_for_region(region)}
        self.unlock_flag_snapshot = {}
        self.unlock_flag_last_poll = 0.0
        self.unlock_flag_tree.delete(*self.unlock_flag_tree.get_children())
        for flag in self.unlock_flag_rows.values():
            self.unlock_flag_tree.insert(
                '', 'end', iid=flag.key, text=flag.label,
                values=(flag.group, f'0x{flag.address:08X}',
                        f'0x{flag.mask:02X}', '—', flag.source))
        self.unlock_flag_feedback.set('')
        self.filter_unlock_flags()
        self.select_unlock_flag()

    def filter_unlock_flags(self):
        """Filter by name, memory address, group, or provenance."""
        query = self.unlock_flag_query.get().strip().casefold()
        visible = []
        table = self.unlock_flag_tree
        for flag in self.unlock_flag_rows.values():
            item = table.item(flag.key)
            text = ' '.join((
                flag.label, flag.group, flag.source, flag.evidence,
                *(str(value) for value in item['values'])))
            if query in text.casefold():
                visible.append(flag.key)
        wanted = set(visible)
        for key in table.get_children():
            if key not in wanted:
                table.detach(key)
        for position, key in enumerate(visible):
            table.move(key, '', position)
        self.unlock_flag_counter.set(
            f'{len(visible)} / {len(self.unlock_flag_rows)} named bits')
        self.select_unlock_flag()

    def _can_write_unlock_flag(self, flag):
        if flag is None or not flag.editable:
            return False
        if self.active_version.key == 'japan':
            return self._japan_unlock_controls_ready()
        return bool(
            self.mem is not None and
            getattr(self.args, 'enable_hex_edit', False) and
            not getattr(self.args, 'read_only', False))

    def select_unlock_flag(self, _event=None):
        table = self.unlock_flag_tree
        selected = table.selection()
        flag = self.unlock_flag_rows.get(selected[0]) if len(selected) == 1 else None
        if flag is not None and flag.key not in table.get_children():
            flag = None
        raw = self.unlock_flag_snapshot.get(flag.key) if flag else None
        enabled = bool(
            flag and raw is not None and self._can_write_unlock_flag(flag))
        for button in (self.unlock_flag_set, self.unlock_flag_clear):
            button.state(['!disabled'] if enabled else ['disabled'])
        if flag is None:
            self.unlock_flag_detail.set('Select a named bit to see its evidence.')
            return
        limitation = (
            ('JP user-confirmed; Set/Clear available.'
             if flag.source == 'JP user-confirmed' else
             'JP offset candidate; Set/Clear available for testing. Verify the effect in-game.')
            if self.active_version.key == 'japan' else
            'USA mapped bit; Set/Clear available.')
        self.unlock_flag_detail.set(
            f'{flag.label} — {flag.evidence}. {limitation}')

    def refresh_unlock_flags(self, *, force=False):
        """Read the one saved-event bank, only while the Flags page is visible."""
        if not force and self.unlock_sections.select() != str(self.unlock_flags_page):
            return
        now = time.monotonic()
        if not force and now - self.unlock_flag_last_poll < 0.7:
            return
        self.unlock_flag_last_poll = now
        region = self.active_version.key
        if region != self.unlock_flag_region:
            self.configure_unlock_flag_region()
        reader = self.jp_rdram if region == 'japan' else self.mem
        try:
            values = read_flag_bytes(reader, region,
                                     self.unlock_flag_rows.values())
            self.unlock_flag_feedback.set('' if reader is not None else 'Disconnected.')
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            values = {}
            self.unlock_flag_feedback.set(f'Flag bank unavailable: {exc}')
        self.unlock_flag_snapshot = values
        for flag in self.unlock_flag_rows.values():
            raw = values.get(flag.key)
            state = ('—' if raw is None else
                     'Set' if raw & flag.mask else 'Clear')
            if raw is not None and region == 'japan' and flag.source == 'JP offset candidate':
                state += ' (candidate)'
            self.unlock_flag_tree.set(flag.key, 'value', state)
        self.select_unlock_flag()

    def set_unlock_flag(self, target):
        """Explicit masked bit edit for mapped USA and JP event fields."""
        table = self.unlock_flag_tree
        selected = table.selection()
        flag = self.unlock_flag_rows.get(selected[0]) if len(selected) == 1 else None
        try:
            if flag is None or flag.key not in table.get_children():
                raise ValueError('Select one visible named flag first')
            if not self._can_write_unlock_flag(flag):
                raise PermissionError('Connect with memory writes enabled; read-only mode blocks editing')
            expected = self.unlock_flag_snapshot.get(flag.key)
            if expected is None:
                raise RuntimeError('Displayed flag byte unavailable; refresh first')
            if self.active_version.key == 'japan':
                changed = write_japan_crosswalk_flag(
                    self.write_japan_raw_bytes, flag, target, expected)
            else:
                # Reuse the existing Story Progress masked CAS writer.
                # A stale byte, game transition, or invalid target fails closed.
                with self.value_freezes.guard:
                    if any(lock.address <= flag.address < lock.address + len(lock.value)
                           for lock in self.value_freezes.locks.values()):
                        raise RuntimeError('Stop the overlapping freeze before editing')
                    changed = write_story_value(
                        self.mem, flag.key, target, bytes((expected,)))
            self.unlock_status.set(
                f'{flag.label}: {target}' +
                (' (written)' if changed else ' (unchanged)'))
            if changed:
                self.append_event(
                    f'USER EVENT BIT {self.active_version.key.upper()} '
                    f'0x{flag.address:08X} mask 0x{flag.mask:02X}: {target}')
                self.last_inspect_at = 0.0
            self.refresh_unlock_flags(force=True)
            self.refresh_story_progress()
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.unlock_status.set(f'{flag.label if flag else "Event flag"}: blocked — {exc}')
            self.unlock_flag_feedback.set(str(exc))
            self.refresh_unlock_flags(force=True)
