"""Read-only dialog for static ROM actor placements in the selected USA scene."""
import tkinter as tk
from tkinter import ttk

from practice.room_actors import actors_for_stage
from practice.scenes import SCENES, unidentified_scene_name


class RoomActorBrowser:
    def __init__(self, parent, atlas, stage=None):
        self.window = tk.Toplevel(parent)
        self.window.title('USA room actor placements (ROM only)')
        self.window.geometry('1100x620')
        self.window.minsize(720, 350)
        self.atlas = atlas
        self.stage = stage
        shell = ttk.Frame(self.window, padding=10)
        shell.pack(fill='both', expand=True)
        self.status = tk.StringVar()
        ttk.Label(shell, textvariable=self.status, wraplength=950).pack(anchor='w', pady=(0, 8))
        row = ttk.Frame(shell)
        row.pack(fill='x', pady=(0, 8))
        ttk.Label(row, text='Filter actor ID/name:').pack(side='left')
        self.query = tk.StringVar()
        ttk.Entry(row, textvariable=self.query, width=30).pack(side='left', padx=8)
        self.query.trace_add('write', lambda *_: self.redraw())
        columns = ('actor', 'name', 'confidence', 'definition', 'record', 'group', 'cells')
        frame = ttk.Frame(shell)
        frame.pack(fill='both', expand=True)
        self.table = ttk.Treeview(frame, columns=columns, show='headings')
        for key, title, width in (
            ('actor', 'Actor ID', 90), ('name', 'Type / name', 210),
            ('confidence', 'Label provenance', 145), ('definition', 'Definition', 95),
            ('record', 'Record offset', 105), ('group', 'Group offset', 100),
            ('cells', 'Spatial grid cells', 170),
        ):
            self.table.heading(key, text=title)
            self.table.column(key, width=width, stretch=key in ('name', 'cells'))
        self.table.pack(side='left', fill='both', expand=True)
        yscroll = ttk.Scrollbar(frame, orient='vertical', command=self.table.yview)
        yscroll.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=yscroll.set)
        ttk.Label(shell, text='Static ROM placements only. Grid cells are room-placement references, not RAM addresses. A placement may be despawned, conditional or outside the loaded part of the scene. This viewer never writes memory.', wraplength=1000).pack(anchor='w', pady=(8, 0))
        self.redraw()

    def refresh(self, atlas, stage):
        self.atlas, self.stage = atlas, stage
        self.redraw()

    def redraw(self):
        self.table.delete(*self.table.get_children())
        if self.atlas is None:
            self.status.set('No actor atlas loaded. Use Scene browser → Load original USA ROM to extract static placements.')
            return
        if self.stage is None:
            self.status.set('Select a room in Scene browser. This window follows the selected room.')
            return
        rows = actors_for_stage(self.atlas, self.stage)
        search = self.query.get().strip().lower()
        shown = 0
        for p in rows:
            actor = f'0x{p["actor_id"]:03X}'
            if search and search not in actor.lower() and search not in p['name'].lower():
                continue
            cells = ', '.join('base' if n == -1 else str(n) for n in p['cells'])
            self.table.insert('', 'end', values=(
                actor, p['name'], p['name_source'], p['definition'],
                f'0x{p["record_offset"]:04X}', f'0x{p["group_offset"]:04X}', cells))
            shown += 1
        name = SCENES.get(self.stage, unidentified_scene_name(self.stage))
        self.status.set(f'Stage {self.stage} — {name}: {len(rows)} ROM placements; showing {shown}. Not a live actor list.')
