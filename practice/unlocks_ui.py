"""One-click unlock controls for original N64 guest RAM."""
from __future__ import annotations
import time
import tkinter as tk
from tkinter import ttk

from practice.theme import PALETTE
from practice.unlocks import UNLOCKS, GROUPS, Unlock, read_unlock, write_unlock, normalize_unlock_value, unlock_all_known
from practice.hex_edit import parse_hex
from practice.region_unlocks import japan_unlock_lead, japan_unlock_all_targets

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
        all_bar = ttk.Frame(tab)
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
        self.unlock_status_label=ttk.Label(tab, textvariable=self.unlock_status)
        self.unlock_status_label.pack(fill='x', pady=(0, 8))
        shell = ttk.Frame(tab)
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


    def _japan_unlock_controls_ready(self):
        """Source-backed Japanese fields write by default once RAM is attached."""
        return bool(
            self.active_version.key == 'japan'
            and self.jp_rdram is not None
            and getattr(self, 'game_pid', None) is not None
            and getattr(self, 'jp_backend', None) in ('project64', 'mupen64plus')
            and getattr(getattr(self, 'connection_target', None),
                        'get', lambda: None)() == self.jp_backend
            and not getattr(self, '_connecting', False)
            and not getattr(self.args, 'read_only', False))

    def configure_unlock_region(self):
        """Retain the exact USA layout; swap address/read/write providers only."""
        japan = self.active_version.key == 'japan'
        usa_writable = bool(
            not japan and getattr(self.args, 'enable_hex_edit', False)
            and not getattr(self.args, 'read_only', False))
        self.unlock_intro_text.set(
            'Japan-0: original USA controls and grouping. Addresses shown are '
            'Japanese source-backed leads only; unknown means unmapped. '
            'Mapped fields can be changed directly; no confirmation or party guard.'
            if japan else
            'Click any value to write it immediately to the original N64 RAM. '
            'The game may not refresh its inventory until an area or menu reload.')
        self.unlock_all_hint.set(
            'Japan: writes only mapped addresses; unknown rows are skipped.'
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
            self.unlock_address_labels[item.address].configure(
                text=f'{lead.address:08X}' if lead is not None else 'unknown')
            _state, controls = self.unlock_row_widgets[item.address]
            for value, button in controls.items():
                button.state(['!disabled'] if usa_writable else ['disabled'])
            if item.quantity:
                self.unlock_count_buttons[item.address].state(
                    ['!disabled'] if usa_writable else ['disabled'])
                self.unlock_count_entries[item.address].configure(
                    state='normal' if usa_writable or not japan else 'disabled')
        self.unlock_last_poll = 0.0
        self.unlock_status.set(
            'Japan-0: 34 original unlock rows. Unknown addresses cannot be '
            'read or written; mapped items support direct writes by default.'
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
            label.configure(
                text=('unknown' if lead is None else
                      '—' if raw is None else f'0x{raw:02X}'),
                foreground=(PALETTE['teal'] if raw is not None
                            and (raw in item.values or item.quantity)
                            else PALETTE['warning']))
            for value, button in controls.items():
                button.state(
                    ['!disabled'] if can_write and lead is not None
                    else ['disabled'])
                button.configure(
                    style='Gold.TButton' if raw is not None and raw == value
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

    def unlock_all_items(self):
        if self.active_version.key == 'japan':
            try:
                changed, total = self.apply_japan_unlocks(japan_unlock_all_targets())
                self.unlock_status.set(
                    f'Japan-0: {changed} changed / {total} mapped entries. '
                    'All unknown addresses skipped.')
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
                    f'Japan-0 {unlock.label}: 0x{actual:02X} '
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
