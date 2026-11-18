"""Bounded, region-neutral Tk row recycler for large story-flag catalogues.

Only viewport rows own actual ttk Off/On buttons. Rows above/below the
viewport remain pure model data; no nested scrollbar or Treeview is created.
"""
from __future__ import annotations

from bisect import bisect_right
import tkinter as tk
from tkinter import ttk

from practice.theme import PALETTE

FLAG_HEIGHT = 68
HEADER_HEIGHT = 42
OVERSCAN = 2


class VirtualFlagList:
    """A fixed-size pool of real ttk controls backed by a virtual scroll area."""

    def __init__(self, parent, *, on_toggle, on_write, on_detail, can_write):
        self.canvas = tk.Canvas(parent, background=PALETTE['background'],
                                highlightthickness=0, takefocus=True)
        self.scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.on_toggle = on_toggle
        self.on_write = on_write
        self.on_detail = on_detail
        self.can_write = can_write
        self.sections = {}
        self.rows = []
        self.starts = [0]
        self._flag_pool = []
        self._header_pool = []
        self.visible_flags = {}
        self.values = {}
        self._rendering = False
        self._last_size = (0, 0)
        self.canvas.bind('<Configure>', self._on_resize)
        self.canvas.bind('<Up>', lambda _e: self._scroll_key(-1))
        self.canvas.bind('<Down>', lambda _e: self._scroll_key(1))
        self.canvas.bind('<Prior>', lambda _e: self._scroll_pages(-1))
        self.canvas.bind('<Next>', lambda _e: self._scroll_pages(1))
        self.canvas.bind('<Home>', lambda _e: self._scroll_absolute(0))
        self.canvas.bind('<End>', lambda _e: self._scroll_absolute(1))

    def _scroll_key(self, step):
        self.yview('scroll', step, 'units')
        return 'break'

    def _scroll_pages(self, step):
        self.yview('scroll', step, 'pages')
        return 'break'

    def _scroll_absolute(self, fraction):
        self.yview('moveto', fraction)
        return 'break'

    def handle_wheel(self, event):
        if getattr(event, 'num', 0) in (4, 5):
            step = -1 if event.num == 4 else 1
        else:
            delta = getattr(event, 'delta', 0)
            if not delta:
                return 'break'
            step = -max(1, abs(delta) // 120) if delta > 0 else max(1, abs(delta) // 120)
        self.yview('scroll', step, 'units')
        return 'break'

    def yview(self, *args):
        result = self.canvas.yview(*args)
        self.render()
        return result

    def _on_resize(self, _event):
        self.render()

    def rebuild(self, sections, expanded, matches, *, reset_scroll=False):
        """Recompute the logical list; widget count depends only on viewport."""
        self.sections = sections
        self._expanded = frozenset(expanded)
        rows = []
        starts = [0]
        for section, flags in sections.items():
            selected = [flag for flag in flags if matches.get(flag.key, True)]
            if not selected:
                continue
            rows.append(('header', section, len(selected)))
            starts.append(starts[-1] + HEADER_HEIGHT)
            if section in expanded:
                for flag in selected:
                    rows.append(('flag', flag))
                    starts.append(starts[-1] + FLAG_HEIGHT)
        self.rows = rows
        self.starts = starts
        self.canvas.configure(scrollregion=(0, 0, 1, max(1, starts[-1])))
        if reset_scroll:
            self.canvas.yview_moveto(0)
        self.render()

    def set_values(self, values):
        self.values = values
        self.render()

    def _new_flag_slot(self):
        frame = ttk.Frame(self.canvas, padding=(10, 5), style='FlagRow.TFrame')
        frame.columnconfigure(0, weight=1)
        name = ttk.Label(frame, style='FlagName.TLabel', wraplength=500)
        name.grid(row=0, column=0, sticky='w')
        address = ttk.Label(frame, style='FlagAddress.TLabel')
        address.grid(row=0, column=1, sticky='w', padx=(8, 10))
        state_var = tk.StringVar(value='—')
        state = ttk.Label(frame, textvariable=state_var, style='FlagState.TLabel', width=6)
        state.grid(row=0, column=2, sticky='w', padx=(0, 6))
        controls = ttk.Frame(frame, style='FlagRow.TFrame')
        controls.grid(row=0, column=3, sticky='e')
        slot = dict(frame=frame, name=name, address=address, state=state_var,
                    state_label=state, key=None, epoch=0, last_update=None)
        off = ttk.Button(controls, text='Off', width=5, style='Flag.TButton',
                         command=lambda item=slot: self._activate(item, 'Clear'))
        on = ttk.Button(controls, text='On', width=5, style='Flag.TButton',
                        command=lambda item=slot: self._activate(item, 'Set'))
        off.pack(side='left')
        on.pack(side='left', padx=(5, 0))
        slot['off'] = off
        slot['on'] = on
        source = ttk.Label(frame, style='FlagMeta.TLabel')
        source.grid(row=1, column=0, columnspan=4, sticky='w', pady=(2, 0))
        slot['source'] = source
        for label in (name, address, source):
            label.bind('<Button-1>', lambda _e, item=slot: self._detail(item))
        slot['window'] = self.canvas.create_window(0, 0, anchor='nw', window=frame,
                                                   height=FLAG_HEIGHT, state='hidden')
        self._flag_pool.append(slot)
        return slot

    def _new_header_slot(self):
        frame = ttk.Frame(self.canvas, padding=(7, 3), style='FlagGroup.TFrame')
        slot = {'frame': frame, 'section': None}
        button = ttk.Button(frame, command=lambda item=slot: self._toggle(item))
        button.pack(fill='x', expand=True)
        slot['button'] = button
        slot['window'] = self.canvas.create_window(0, 0, anchor='nw', window=frame,
                                                   height=HEADER_HEIGHT, state='hidden')
        self._header_pool.append(slot)
        return slot

    def _activate(self, slot, target):
        key = slot['key']
        if key is None or self.visible_flags.get(key) is not slot:
            return
        flag = next((row[1] for row in self.rows
                     if row[0] == 'flag' and row[1].key == key), None)
        if flag is None or self.values.get(key) is None or not self.can_write(flag):
            return
        self.on_write(key, target)

    def _detail(self, slot):
        key = slot['key']
        if key is not None and self.visible_flags.get(key) is slot:
            self.on_detail(key)

    def _toggle(self, slot):
        if slot['section'] is not None:
            self.on_toggle(slot['section'])

    def render(self):
        if self._rendering or not self.canvas.winfo_exists():
            return
        self._rendering = True
        try:
            width = max(1, self.canvas.winfo_width())
            viewport = max(1, self.canvas.winfo_height())
            top = max(0, int(self.canvas.canvasy(0)))
            begin = max(0, bisect_right(self.starts, top) - 1 - OVERSCAN)
            finish = min(len(self.rows), bisect_right(self.starts, top + viewport) + OVERSCAN)
            visible = self.rows[begin:finish]
            need_flags = sum(row[0] == 'flag' for row in visible)
            need_headers = len(visible) - need_flags
            while len(self._flag_pool) < need_flags:
                self._new_flag_slot()
            while len(self._header_pool) < need_headers:
                self._new_header_slot()
            self.visible_flags.clear()
            fpos = hpos = 0
            for index in range(begin, finish):
                row = self.rows[index]
                if row[0] == 'flag':
                    slot = self._flag_pool[fpos]
                    fpos += 1
                    flag = row[1]
                    if slot['key'] != flag.key:
                        slot['key'] = flag.key
                        slot['epoch'] += 1
                        slot['last_update'] = None
                        slot['name'].configure(text=flag.label)
                        slot['address'].configure(text=f'{flag.address:08X} · {flag.mask:02X}')
                        slot['source'].configure(text=f'{flag.source} · {flag.group} / {flag.subtype}')
                    self.visible_flags[flag.key] = slot
                    self._paint_flag(slot, flag)
                else:
                    slot = self._header_pool[hpos]
                    hpos += 1
                    section, count = row[1], row[2]
                    slot['section'] = section
                    slot['button'].configure(text=f'▾ {section[0]} / {section[1]} ({count})'
                                             if section in self._expanded else
                                             f'▸ {section[0]} / {section[1]} ({count})')
                self.canvas.coords(slot['window'], 1, self.starts[index])
                self.canvas.itemconfigure(slot['window'], state='normal',
                                          width=max(1, width - 5))
            for slot in self._flag_pool[fpos:]:
                slot['key'] = None
                slot['last_update'] = None
                self.canvas.itemconfigure(slot['window'], state='hidden')
            for slot in self._header_pool[hpos:]:
                slot['section'] = None
                self.canvas.itemconfigure(slot['window'], state='hidden')
        finally:
            self._rendering = False

    def _paint_flag(self, slot, flag):
        raw = self.values.get(flag.key)
        state = '—' if raw is None else 'On' if raw & flag.mask else 'Off'
        writable = raw is not None and self.can_write(flag)
        stamp = (flag.key, state, writable)
        if slot['last_update'] == stamp:
            return
        slot['last_update'] = stamp
        slot['state'].set(state)
        slot['state_label'].configure(foreground=(
            PALETTE['teal'] if state == 'On' else
            PALETTE['warning'] if state == 'Off' else PALETTE['muted']))
        for target, button in (('Off', slot['off']), ('On', slot['on'])):
            button.state(['!disabled'] if writable else ['disabled'])
            button.configure(style=(
                'FlagOn.TButton' if target == 'On' else 'FlagOff.TButton')
                if state == target else 'Flag.TButton')

    @property
    def widget_count(self):
        return len(self._flag_pool) + len(self._header_pool)

    def scroll_to_key(self, key):
        for index, row in enumerate(self.rows):
            if row[0] == 'flag' and row[1].key == key:
                total = max(1, self.starts[-1])
                self.yview('moveto', self.starts[index] / total)
                return key in self.visible_flags
        return False
