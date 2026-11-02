"""One-click unlock controls for original N64 guest RAM."""
from __future__ import annotations
import time
import tkinter as tk
from tkinter import ttk

from practice.theme import PALETTE
from practice.unlocks import UNLOCKS, GROUPS, Unlock, read_unlock, write_unlock, normalize_unlock_value
from practice.hex_edit import parse_hex

class UnlocksMixin:
    def build_unlock_tabs(self, notebook) -> None:
        self.unlock_status = tk.StringVar(value='Connect to US Goemon64Recomp to read and change flags.')
        self.unlock_row_widgets = {}
        self.unlock_count_inputs = {}
        self.unlock_count_entries = {}
        self.unlock_last_poll = 0.0

        tab = ttk.Frame(notebook, padding=10)
        notebook.insert(1, tab, text='Unlocks')
        self.unlock_tab = tab
        intro = ttk.Frame(tab)
        intro.pack(fill='x', pady=(0, 8))
        ttk.Label(intro, text='Unlocks, weapons and upgrades', font=('Segoe UI Semibold', 16),
                  foreground=PALETTE['gold']).pack(anchor='w')
        ttk.Label(intro, text='Click any value to write it immediately to the original N64 RAM. '
                  'The game may not refresh its inventory until an area or menu reload.',
                  style='Muted.TLabel').pack(anchor='w', pady=(4, 0))
        ttk.Label(tab, textvariable=self.unlock_status).pack(fill='x', pady=(0, 8))

        shell = ttk.Frame(tab)
        shell.pack(fill='both', expand=True)
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
                    controls[value] = button
                if item.quantity:
                    entry_var=tk.StringVar(value='00')
                    entry=ttk.Entry(buttons,textvariable=entry_var,width=5,font=('Consolas',10))
                    entry.pack(side='left',padx=(8,2))
                    ttk.Button(buttons,text='Set hex count',
                               command=lambda field=item, var=entry_var: self.set_unlock_hex(field,var.get())).pack(side='left')
                    self.unlock_count_inputs[item.address]=entry_var
                    self.unlock_count_entries[item.address]=entry
                self.unlock_row_widgets[item.address] = (state, controls)


    def set_unlock(self, unlock: Unlock, value: int) -> None:
        """One click = one measured byte write; never confirmation dialogs."""
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
        """Refresh from live RAM, including external edits and game changes."""
        now = time.monotonic()
        if not force and now - self.unlock_last_poll < 0.5:
            return
        self.unlock_last_poll = now
        values = {}
        # Raw Tcl path avoids tkinter's _nametowidget('popdown') KeyError
        # when a ttk Combobox internal dropdown owns focus on Windows.
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
