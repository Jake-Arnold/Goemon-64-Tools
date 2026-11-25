"""Value-freeze controls; user activation only, no persistent enabled state."""
import tkinter as tk
import queue
from tkinter import ttk

from practice.checkpoints import _ensure_capture_safe
from practice.hex_edit import parse_hex, watch_scalar_width
from practice.custom_watches import regional_watches
from practice.value_freezes import FastFreezeWorker
from practice.japan_value_freezes import RegionalValueFreezes, stable_japan_gameplay


class ValueFreezesMixin:
    def build_value_freezes_tab(self, notebook):
        self.value_freezes = RegionalValueFreezes(self._open_japan_freeze_writer)
        self._freeze_worker_messages = queue.SimpleQueue()
        self._freeze_worker = FastFreezeWorker(
            self.value_freezes, self._freeze_worker_connection, self._freeze_worker_messages)
        self.root.bind('<Destroy>', self._freeze_root_destroy, add='+')
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text='Value freezes')
        self.value_freezes_tab = tab
        ttk.Label(tab, text='Freeze values during gameplay', font=('Segoe UI Semibold',16)).pack(anchor='w')
        ttk.Label(tab, text='Checks active values every 10 ms (best effort, not frame-perfect); skips menus, loading, pause and scripts. '
                  'Only writes changed values. Locks are session-only and stop on reconnect or failure. '
                  'Raw targets are fixed guest addresses; actor addresses can be reused after scene changes.',
                  wraplength=1050).pack(anchor='w', pady=6)
        self.freeze_health = tk.BooleanVar(value=False)
        self.enemy_pass_through = tk.BooleanVar(value=False)
        self.god_mode_var = tk.BooleanVar(value=False)
        self.freeze_health_button = ttk.Checkbutton(tab, text='Keep health at current maximum',
            variable=self.freeze_health, command=self.toggle_freeze_health)
        self.freeze_health_button.pack(anchor='w', pady=5)
        self.god_mode_button = ttk.Checkbutton(
            tab, text='God Mode — full health, 99 lives, 9,999 Ryo',
            variable=self.god_mode_var, command=self.toggle_god_mode)
        self.god_mode_button.pack(anchor='w', pady=5)
        ttk.Label(tab, text='Resource protection only; no enemy collision or item unlock changes. '
                  'Stops enforcing resources when unchecked.', wraplength=1050).pack(anchor='w')
        self.enemy_pass_through_button = ttk.Checkbutton(
            tab, text='Pass through enemies (experimental; player task +0x30 = 6)',
            variable=self.enemy_pass_through, command=self.toggle_enemy_pass_through)
        self.enemy_pass_through_button.pack(anchor='w', pady=4)
        ttk.Label(tab, text='Uses the live player-task pointer every 10 ms, even after actor relocation. '
                  'Enemy-body collision only; damage, walls and scripted contacts are not guaranteed to be disabled. '
                  'Turning off stops writes and lets the game restore its own state.',
                  wraplength=1050).pack(anchor='w', pady=(0, 5))
        row = ttk.Frame(tab); row.pack(fill='x', pady=5)
        for title, variable, width in [('Guest address (hex)',self.raw_address,14),
                                       ('Bytes',self.raw_width,3),('Target hex',self.raw_value,20)]:
            ttk.Label(row, text=title).pack(side='left', padx=4)
            if variable is self.raw_width:
                ttk.Combobox(row,textvariable=variable,values=('1','2','4','8'),state='readonly',width=width).pack(side='left')
            else:ttk.Entry(row,textvariable=variable,width=width).pack(side='left')
        self.freeze_raw_button = ttk.Button(row,text='Freeze raw hex',command=self.freeze_raw_value)
        self.freeze_raw_button.pack(side='left',padx=6)
        ttk.Button(tab,text='Freeze selected Live memory watch at its current value',command=self.freeze_selected_watch).pack(anchor='w')
        self.freeze_status = tk.StringVar(value='No active freezes.')
        ttk.Label(tab,textvariable=self.freeze_status,wraplength=1050).pack(anchor='w',pady=6)
        self.freeze_tree = ttk.Treeview(tab,columns=('address','bytes','target'),show='tree headings',height=12)
        self.freeze_tree.heading('#0',text='Name')
        for name,title in [('address','Guest address'),('bytes','Bytes'),('target','Frozen hex')]:
            self.freeze_tree.heading(name,text=title)
        self.freeze_tree.pack(fill='both',expand=True)
        row=ttk.Frame(tab);row.pack(fill='x',pady=6)
        ttk.Button(row,text='Stop selected',command=self.stop_selected_freeze).pack(side='left')
        ttk.Button(row,text='Stop all freezes',command=self.stop_all_freezes).pack(side='left',padx=6)
        if not self.args.enable_hex_edit:
            self.freeze_health_button.state(['disabled']);self.freeze_raw_button.state(['disabled'])
            self.enemy_pass_through_button.state(['disabled'])
            self.god_mode_button.state(['disabled'])
        self.root.after(150,self.poll_value_freezes)

    def freeze_token(self):
        if self.active_version.key == 'japan':
            reader = self.jp_rdram
            return ('japan', self.game_pid, id(reader),
                    getattr(reader, 'base', None),
                    getattr(reader, 'endian', None),
                    getattr(reader, 'rdram_size', None),
                    self.jp_backend)
        return (self.game_pid, id(self.mem), getattr(self.mem, 'base', None),
                getattr(self.mem, 'endian', None))

    def _freeze_worker_connection(self):
        """Worker reads only plain Python attributes, never Tk variables."""
        if self.active_version.key == 'japan':
            connected = (
                self.jp_rdram is not None and self.game_pid is not None
                and self.jp_backend in ('project64', 'mupen64plus', 'recomp')
                and not self._connecting
                and not getattr(self.args, 'read_only', False)
                and getattr(self.args, 'enable_hex_edit', True))
            return self.jp_rdram, self.freeze_token(), bool(connected)
        return (self.mem, self.freeze_token(),
                not getattr(self.args,'read_only',False) and self.args.enable_hex_edit)

    def _ensure_freeze_worker(self):
        self._freeze_worker.start()

    def _stop_freeze_worker(self):
        self._freeze_worker.stop()

    def _freeze_root_destroy(self, event):
        if event.widget is self.root:
            self._stop_freeze_worker()

    def _freeze_poll_once(self):
        """Explicit synchronous diagnostic and test hook."""
        with self.value_freezes.guard:
            ram,token,writable=self._freeze_worker_connection()
            return self.value_freezes.poll(ram,token,writable=writable)

    def require_freeze_access(self, raw=False):
        if self.active_version.key == 'japan':
            if not raw:
                raise PermissionError('USA health, God Mode and task freezes are not Japan-0 compatible')
            if (self.jp_rdram is None or self.game_pid is None or self._connecting
                    or self.jp_backend not in ('project64', 'mupen64plus', 'recomp')
                    or self.connection_target.get() != self.jp_backend):
                raise RuntimeError('Connect to Japanese RAM before freezing')
            if (getattr(self.args, 'read_only', False)
                    or not getattr(self.args, 'enable_hex_edit', True)):
                raise PermissionError('Value freezing disabled by --read-only')
            if stable_japan_gameplay(self.jp_rdram) is None:
                raise ValueError('Freeze requires stable Japanese gameplay')
            return
        if not self.mem:raise ValueError('Connect to a game first')
        if getattr(self.args,'read_only',False) or not self.args.enable_hex_edit:
            raise PermissionError('Value freezing is disabled in read-only mode')
        _ensure_capture_safe(self.mem)

    def toggle_freeze_health(self):
        try:
            if self.freeze_health.get():
                self.require_freeze_access()
                self.value_freezes.enable_health(self.freeze_token())
                self._ensure_freeze_worker()
            else:self.value_freezes.disable_health()
            self.freeze_status.set('Maximum-health freeze '+('enabled.' if self.freeze_health.get() else 'stopped.'))
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:
            self.freeze_health.set(False);self.freeze_status.set(str(exc))

    def toggle_god_mode(self):
        try:
            if self.god_mode_var.get():
                self.require_freeze_access()
                self.value_freezes.enable_god_mode(self.freeze_token())
                self._ensure_freeze_worker()
            else:
                self.value_freezes.disable_god_mode()
            self.freeze_status.set('God Mode ' + ('enabled.' if self.god_mode_var.get()
                                                    else 'disabled; resources not restored.'))
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.god_mode_var.set(False)
            self.freeze_status.set(f'God Mode blocked: {exc}')

    def toggle_enemy_pass_through(self):
        try:
            if self.enemy_pass_through.get():
                self.require_freeze_access()
                self.value_freezes.enable_enemy_pass_through(self.freeze_token())
                self._ensure_freeze_worker()
            else:
                self.value_freezes.disable_enemy_pass_through()
            self.freeze_status.set('Enemy pass-through ' +
                ('enabled; target follows the live player task.' if self.enemy_pass_through.get()
                 else 'disabled; game controls player state.'))
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.enemy_pass_through.set(False)
            self.freeze_status.set(f'Enemy pass-through blocked: {exc}')

    def _freeze_feedback(self, message, *, inspector=False):
        self.draw_value_freezes()
        self.freeze_status.set(message)
        if inspector:
            self.inspector_status.set(message)

    def _register_raw_freeze(self, address, value, label='Raw value'):
        # Callers have already checked regional access. The lock book and worker
        # still enforce the existing session identity and gameplay policy.
        self.value_freezes.add(self.freeze_token(), address, value, label)
        self._ensure_freeze_worker()

    def toggle_live_watch_freeze(self, row_id):
        watch = next((w for w in self.watch_rows if w.name == row_id), None)
        if watch is None or watch.addr is None:
            self.inspector_status.set('No fixed guest address for this field.')
            return
        if self.value_freezes.get(watch.addr) is not None:
            self.value_freezes.remove(watch.addr)
            self._freeze_feedback(f'Unfroze {self.display_watch_name(row_id)}.', inspector=True)
        else:
            self.freeze_watch_by_id(row_id)

    def freeze_raw_value(self):
        try:
            self.require_freeze_access(raw=True)
            address=int(self.raw_address.get().strip(),16)
            value=parse_hex(self.raw_value.get(),int(self.raw_width.get()))
            self._register_raw_freeze(address, value)
            self._freeze_feedback('Raw freeze armed; checking every 10 ms.')
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:self.freeze_status.set(str(exc))

    def freeze_selected_watch(self):
        selected=self.watch_tree.selection()
        if not selected:
            self.freeze_status.set('Select a watch in Live memory first.')
            return
        self.freeze_watch_by_id(selected[0])

    def freeze_watch_by_id(self, row_id):
        """Use the same fresh-read and gameplay guards for context-menu freezing."""
        try:
            self.require_freeze_access(raw=True)
            watch=next((w for w in self.watch_rows if w.name==row_id),None)
            if watch is None:
                raise ValueError('Selected watch is no longer available')
            if watch.addr is None:
                raise ValueError('Selected watch has no fixed guest address')
            region = self.active_version.key
            japan = region == 'japan'
            try:
                width = watch_scalar_width(watch, regional_watches(self, region), region=region)
            except ValueError as exc:
                raise ValueError('No supported scalar width for this watch') from exc
            # Always fetch current game RAM bytes instead of freezing a stale table value.
            ram=self.jp_rdram if japan else self.mem
            value=ram.read_guest(watch.addr,width)
            label=self.display_watch_name(watch.name)
            self._register_raw_freeze(watch.addr, value, label)
            self._freeze_feedback(f'Freeze armed: {label} (0x{watch.addr:08X}).', inspector=True)
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:
            self.freeze_status.set(f'Freeze blocked: {exc}')
            self.inspector_status.set(self.freeze_status.get())

    def draw_value_freezes(self):
        self.freeze_tree.delete(*self.freeze_tree.get_children())
        for lock in self.value_freezes.snapshot():
            self.freeze_tree.insert('','end',iid=str(lock.address),text=lock.label,
                values=(f'0x{lock.address:08X}',len(lock.value),lock.value.hex().upper()))

    def stop_selected_freeze(self):
        for selected in self.freeze_tree.selection():self.value_freezes.remove(int(selected))
        self._freeze_feedback('Selected freezes stopped.')

    def stop_all_freezes(self):
        self.value_freezes.clear();self.freeze_health.set(False)
        self.enemy_pass_through.set(False)
        self.god_mode_var.set(False)
        self._freeze_feedback('All freezes stopped.')

    def poll_value_freezes(self):
        """UI status refresh only; fast game-memory checks run independently."""
        last=None
        while True:
            try:
                last=self._freeze_worker_messages.get_nowait()
            except queue.Empty:
                break
        active=self.value_freezes.active()
        # Discard stale status messages queued before a manual stop or new lock.
        if last is not None and not (
                (last.startswith('Active:') and not active) or
                (last.startswith('Freezes stopped') and active)):
            self.freeze_status.set(last)
        # Also reconcile tables when a test/connection clears locks without
        # passing through the background worker's message queue.
        if not active and self.freeze_tree.get_children():
            self.draw_value_freezes()
        self.freeze_health.set(self.value_freezes.keep_health)
        self.enemy_pass_through.set(self.value_freezes.enemy_pass_through)
        self.god_mode_var.set(self.value_freezes.god_mode)
        self.root.after(150,self.poll_value_freezes)
