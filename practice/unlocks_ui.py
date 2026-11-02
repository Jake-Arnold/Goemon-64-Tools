"""One-click unlock controls and optional original-game PNG sprite gallery.

The application intentionally does not redistribute copyrighted game graphics.
Users can add exported original sprite PNGs named by the field slug.
"""
from __future__ import annotations
import shutil
import webbrowser
import time
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from practice.paths import practice_data_dir, resource_root
from practice.theme import PALETTE
from practice.unlocks import UNLOCKS, GROUPS, Unlock, read_unlock, write_unlock, normalize_unlock_value
from practice.hex_edit import parse_hex

SPRITE_DIR = practice_data_dir() / 'sprites'
BUNDLED_SPRITE_DIR = resource_root() / 'assets' / 'item_sprites'
SPRITE_SHEET_URL = 'https://www.spriters-resource.com/nintendo_64/mysticalninjastarringgoemon/asset/123088/'


class UnlocksMixin:
    def build_unlock_tabs(self, notebook) -> None:
        self.unlock_status = tk.StringVar(value='Connect to US Goemon64Recomp to read and change flags.')
        self.unlock_row_widgets = {}
        self.unlock_count_inputs = {}
        self.unlock_sprites = {}
        self.unlock_last_poll = 0.0
        self.sprite_gallery_items = {}
        self.sprite_photos = []

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
                self.unlock_row_widgets[item.address] = (state, controls)

        sprite_tab = ttk.Frame(notebook, padding=10)
        notebook.insert(2, sprite_tab, text='Sprites')
        self.sprite_tab = sprite_tab
        ttk.Label(sprite_tab, text='Original-game item sprites', font=('Segoe UI Semibold', 16),
                  foreground=PALETTE['gold']).pack(anchor='w')
        ttk.Label(sprite_tab, text='Uses bundled crops from your provided inventory sheet and can also load local PNG overrides from the sprite folder.',
                  style='Muted.TLabel', wraplength=1000).pack(anchor='w', pady=5)
        tools = ttk.Frame(sprite_tab)
        tools.pack(fill='x', pady=(0, 8))
        ttk.Button(tools, text='Import original PNGs from folder',
                   command=self.import_unlock_sprites, style='Gold.TButton').pack(side='left')
        ttk.Button(tools, text='Refresh sprites', command=self.populate_unlock_sprites).pack(side='left', padx=7)
        ttk.Button(tools, text='Open original sprite sheet reference',
                   command=lambda: webbrowser.open(SPRITE_SHEET_URL)).pack(side='left', padx=7)
        self.sprite_status = tk.StringVar(value=f'Looking for artwork in {SPRITE_DIR}')
        ttk.Label(sprite_tab, textvariable=self.sprite_status, style='Muted.TLabel',
                  wraplength=950).pack(anchor='w', pady=(0, 7))
        host = ttk.Frame(sprite_tab)
        host.pack(fill='both', expand=True)
        self.sprite_canvas = tk.Canvas(host, bg=PALETTE['background'], highlightthickness=0)
        bar = ttk.Scrollbar(host, orient='vertical', command=self.sprite_canvas.yview)
        self.sprite_canvas.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        self.sprite_canvas.pack(side='left', fill='both', expand=True)
        self.sprite_body = ttk.Frame(self.sprite_canvas, padding=(3, 4, 12, 18))
        self.sprite_window = self.sprite_canvas.create_window((0, 0),
                                    window=self.sprite_body, anchor='nw')
        self.sprite_body.bind('<Configure>', lambda _e: self.sprite_canvas.configure(
                                   scrollregion=self.sprite_canvas.bbox('all')))
        self.sprite_canvas.bind('<Configure>', lambda e: self.sprite_canvas.itemconfigure(
                                    self.sprite_window, width=e.width))
        self.populate_unlock_sprites()

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
                if var is not None and not (isinstance(self.root.focus_get(),ttk.Entry) and
                        self.root.focus_get().cget('textvariable')==str(var)):
                    var.set(f'{raw:02X}')
            state.configure(text='—' if raw is None else f'0x{raw:02X}',
                            foreground=PALETTE['teal'] if (raw in field.values or (field.quantity and raw is not None)) else PALETTE['warning'])
            for value, button in controls.items():
                button.configure(style='Gold.TButton' if raw == value else 'TButton')
        for field, (state_label, button) in self.sprite_gallery_items.items():
            raw = values.get(field.address)
            state_label.configure(text='—' if raw is None else f'0x{raw:02X}')
            button.configure(text='Disconnected' if raw is None else
                ('Set to 1' if field.quantity and raw == 0 else ('Set to 0' if field.quantity else ('Set ON' if raw not in field.values or raw == field.values[0] else 'Set OFF'))))

    def _sprite_path(self, field: Unlock) -> Path | None:
        for base in (SPRITE_DIR, BUNDLED_SPRITE_DIR):
            file = base / f'{field.slug}.png'
            if file.is_file():
                return file
        return None

    def populate_unlock_sprites(self) -> None:
        for child in self.sprite_body.winfo_children():
            child.destroy()
        self.sprite_gallery_items = {}
        self.sprite_photos = []
        found = 0
        for column in range(4):
            self.sprite_body.columnconfigure(column, weight=1, uniform='sprites')
        for i, field in enumerate(UNLOCKS):
            card = ttk.LabelFrame(self.sprite_body, text=f' {field.group} ', padding=10)
            card.grid(row=i//4, column=i%4, sticky='nsew', padx=5, pady=6)
            icon = self._sprite_path(field)
            picture = tk.Frame(card, width=90, height=78, bg=PALETTE['surface_alt'])
            picture.pack(pady=4)
            picture.pack_propagate(False)
            if icon is not None:
                try:
                    image = tk.PhotoImage(file=str(icon))
                    scale = max(1, (max(image.width(), image.height()) + 75)//76)
                    if scale > 1:
                        image = image.subsample(scale, scale)
                    self.sprite_photos.append(image)
                    tk.Label(picture, image=image, bg=PALETTE['surface_alt']).pack(expand=True)
                    found += 1
                except tk.TclError:
                    tk.Label(picture, text='INVALID PNG', fg=PALETTE['warning'],
                             bg=PALETTE['surface_alt']).pack(expand=True)
            else:
                tk.Label(picture, text='NO SPRITE\nIMPORTED', fg=PALETTE['muted'],
                         bg=PALETTE['surface_alt'], font=('Segoe UI', 9)).pack(expand=True)
            ttk.Label(card, text=field.label, style='Card.TLabel',
                      wraplength=175).pack(anchor='center', pady=(2, 3))
            status = ttk.Label(card, text='—', style='Card.TLabel', font=('Consolas', 10))
            status.pack()
            button = ttk.Button(card, text='Set ON / OFF', command=lambda u=field: self.toggle_sprite_unlock(u))
            button.pack(fill='x', pady=(5, 0))
            self.sprite_gallery_items[field] = (status, button)
        self.sprite_status.set(f'{found}/{len(UNLOCKS)} sprite images available. '
            f'Local overrides live in {SPRITE_DIR}; bundled defaults come from {BUNDLED_SPRITE_DIR}.')
        self.refresh_unlocks(force=True)

    def toggle_sprite_unlock(self, field: Unlock) -> None:
        if not self.mem:
            self.unlock_status.set('Disconnected. Connect before editing unlocks.')
            return
        try:
            current = read_unlock(self.mem, field)
        except (OSError, ValueError) as exc:
            self.unlock_status.set(str(exc))
            return
        # A single button alternates 0 and the first available acquired level.
        self.set_unlock(field, field.values[0] if current != field.values[0] else field.values[1])

    def import_unlock_sprites(self) -> None:
        source = filedialog.askdirectory(parent=self.root,
            title='Choose a folder containing original Goemon item PNGs')
        if not source:
            return
        src_dir = Path(source)
        SPRITE_DIR.mkdir(parents=True, exist_ok=True)
        imported = 0
        for field in UNLOCKS:
            candidates = [p for p in src_dir.iterdir() if p.is_file() and
                          p.suffix.lower()=='.png' and p.stem.lower()==field.slug]
            if not candidates:
                continue
            src = candidates[0]
            dst = SPRITE_DIR / (field.slug + '.png')
            if src.resolve() != dst.resolve():
                shutil.copyfile(src, dst)
            imported += 1
        self.populate_unlock_sprites()
        self.sprite_status.set(f'Imported {imported} matched PNGs. '
                               f'Filename format: <field_slug>.png. Folder: {SPRITE_DIR}')
