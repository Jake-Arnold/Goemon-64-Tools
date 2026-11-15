"""One-click unlock controls for original N64 guest RAM."""
from __future__ import annotations
import time
import tkinter as tk
from tkinter import ttk

from practice.theme import PALETTE
from practice.unlocks import UNLOCKS, GROUPS, Unlock, read_unlock, write_unlock, normalize_unlock_value, unlock_all_known
from practice.hex_edit import parse_hex

class UnlocksMixin:
    def build_unlock_tabs(self, notebook) -> None:
        self.unlock_status = tk.StringVar(value='Connect to US Goemon in Recomp or Project64 to read and change flags.')
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
        ttk.Label(intro, text='Click any value to write it immediately to the original N64 RAM. '
                  'The game may not refresh its inventory until an area or menu reload.',
                  style='Muted.TLabel').pack(anchor='w', pady=(4, 0))
        all_bar = ttk.Frame(tab)
        all_bar.pack(fill='x', pady=(0, 8))
        self.usa_unlock_all_bar = all_bar
        self.unlock_all_button = ttk.Button(
            all_bar, text='Unlock all mapped items, weapons and abilities',
            command=self.unlock_all_items)
        self.unlock_all_button.pack(side='left')
        if not self.args.enable_hex_edit:
            self.unlock_all_button.state(['disabled'])
        ttk.Label(all_bar, text='One-time edit; does not set story completion flags.',
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
                ttk.Label(card, text=f'{item.address:08X}', style='CardMuted.TLabel',
                          font=('Consolas', 9)).grid(row=i, column=1, sticky='w', padx=(12, 8))
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
                self.unlock_row_widgets[item.address] = (state, controls)


        # The same Unlocks TAB renders version-specific, source-backed rows.
        # No USA addresses may be interpreted while Japan-0 is selected.
        japanese = ttk.Frame(tab, padding=(2, 4))
        self.jp_unlock_panel = japanese
        ttk.Label(
            japanese, text='Japan-0 unlocks and inventory',
            font=('Segoe UI Semibold', 16)).pack(anchor='w')
        ttk.Label(
            japanese, text='Original Japanese guest addresses from the JP '
                           'cheat catalogue. Most entries are source-backed '
                           'leads, not confirmed writing targets. The two '
                           'user-verified party unlocks use the separate '
                           'guarded Japan controller.',
            wraplength=1020).pack(anchor='w', pady=(3, 6))
        self.jp_unlock_status = tk.StringVar(
            value='Connect to verified Japan-0 RAM to read mapped unlocks.')
        ttk.Label(japanese, textvariable=self.jp_unlock_status).pack(
            fill='x', pady=(2, 5))
        buttons=ttk.Frame(japanese)
        buttons.pack(fill='x', pady=(2, 6))
        self.jp_unlock_buttons={}
        for char, name in ((2,'Unlock Sasuke'),(3,'Unlock Yae')):
            button=ttk.Button(
                buttons, text=name,
                command=lambda index=char:self.enable_japan_party(index))
            button.pack(side='left', padx=(0, 8))
            button.state(['disabled'])
            self.jp_unlock_buttons[char]=button
        from practice.region_views import japan_unlock_fields
        self.jp_unlock_fields=japan_unlock_fields()
        table=ttk.Treeview(
            japanese, columns=('address','value','raw','status'),
            show='tree headings', height=21)
        table.heading('#0',text='Japanese field')
        table.column('#0',width=340)
        for key,label,width in (
            ('address','Japan guest address',150),
            ('value','Observed',160),('raw','Raw',80),
            ('status','Evidence / status',290)):
            table.heading(key,text=label)
            table.column(key,width=width)
        scrollbar=ttk.Scrollbar(
            japanese, orient='vertical', command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.jp_unlock_table=table
        for field in self.jp_unlock_fields:
            table.insert('', 'end', iid=field.key, text=field.label,
                         values=(f'0x{field.address:08X}','—','—',
                                 'Source-backed; awaiting live read'))
        self.jp_unlock_last_poll=0.0

    def configure_unlock_region(self):
        japan=self.active_version.key=='japan'
        for widget in (self.usa_unlock_intro, self.usa_unlock_all_bar,
                       self.unlock_status_label, self.usa_unlock_shell):
            if japan:
                widget.pack_forget()
            else:
                widget.pack(fill='both' if widget is self.usa_unlock_shell
                            else 'x', expand=(widget is self.usa_unlock_shell))
        if japan:
            self.jp_unlock_panel.pack(fill='both',expand=True)
            self.refresh_japan_unlocks(force=True)
        else:
            self.jp_unlock_panel.pack_forget()
            self.refresh_unlocks(force=True)

    def refresh_japan_unlocks(self, *, force=False):
        if self.active_version.key!='japan':
            return
        now=time.monotonic()
        if not force and now-self.jp_unlock_last_poll < 0.8:
            return
        self.jp_unlock_last_poll=now
        from practice.japanese_fields import read_japan_field
        for field in self.jp_unlock_fields:
            if self.jp_rdram is None:
                value,raw,status='—','—','Disconnected'
            else:
                result=read_japan_field(self.jp_rdram,field)
                value,raw,status=result.value,result.raw,result.status
            self.jp_unlock_table.item(
                field.key,values=(f'0x{field.address:08X}',
                                  value,raw,status))
        enabled=bool(
            self.jp_rdram is not None
            and getattr(self.args,'enable_japan_party_writes',False)
            and not getattr(self.args,'read_only',False))
        for button in self.jp_unlock_buttons.values():
            button.state(['!disabled'] if enabled else ['disabled'])
        self.jp_unlock_status.set(
            f'Japan-0: {len(self.jp_unlock_fields)} mapped read-only '
            'source leads; Sasuke/Yae guarded unlocks available.'
            if self.jp_rdram is not None
            else 'Connect to verified Japan-0 RAM to read mapped unlocks.')

    def unlock_all_items(self):
        if self.active_version.key == 'japan':
            self.jp_unlock_status.set(
                'Japan-only unlock-all not mapped; USA inventory writes refused.')
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
        """One click = one measured USA byte write; never translate to Japan."""
        if self.active_version.key == 'japan':
            self.jp_unlock_status.set(
                'Japan-0: USA unlock addresses are unavailable; no writes.')
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
