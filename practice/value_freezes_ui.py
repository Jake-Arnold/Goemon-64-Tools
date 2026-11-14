"""Value-freeze controls; user activation only, no persistent enabled state."""
import tkinter as tk
import queue
from tkinter import ttk

from practice.checkpoints import _ensure_capture_safe
from practice.hex_edit import parse_hex, get_policy
from practice.value_freezes import ValueFreezes, FastFreezeWorker


class ValueFreezesMixin:
    def build_value_freezes_tab(self, notebook):
        self.value_freezes = ValueFreezes()
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
        self.freeze_health_button = ttk.Checkbutton(tab, text='Keep health at current maximum',
            variable=self.freeze_health, command=self.toggle_freeze_health)
        self.freeze_health_button.pack(anchor='w', pady=5)
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
        self.root.after(150,self.poll_value_freezes)

    def freeze_token(self):
        return (self.game_pid,id(self.mem),getattr(self.mem,'base',None),getattr(self.mem,'endian',None))

    def _freeze_worker_connection(self):
        """Plain Python attributes only; never read Tk variables from worker."""
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

    def freeze_raw_value(self):
        try:
            self.require_freeze_access(raw=True)
            address=int(self.raw_address.get().strip(),16)
            value=parse_hex(self.raw_value.get(),int(self.raw_width.get()))
            self.value_freezes.add(self.freeze_token(),address,value)
            self._ensure_freeze_worker()
            self.draw_value_freezes();self.freeze_status.set('Raw freeze armed; checking every 10 ms.')
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
            spec=next((s for s in self.custom_watches if s.row_name==watch.name),None)
            policy=get_policy(watch.addr)
            raw_text=watch.raw.removeprefix('0x').removeprefix('0X').strip()
            width=(spec.width if spec else policy.width if policy else
                   len(raw_text)//2 if len(raw_text) in (2,4,8,16) and
                   all(c in '0123456789abcdefABCDEF' for c in raw_text) else 0)
            if width not in (1,2,4,8):
                raise ValueError('No supported scalar width for this watch')
            # Always fetch current game RAM bytes instead of freezing a stale table value.
            value=self.mem.read_guest(watch.addr,width)
            label=self.display_watch_name(watch.name)
            self.value_freezes.add(self.freeze_token(),watch.addr,value,label)
            self._ensure_freeze_worker()
            self.draw_value_freezes()
            self.freeze_status.set(f'Freeze armed: {label} (0x{watch.addr:08X}).')
            self.inspector_status.set(self.freeze_status.get())
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
        self.draw_value_freezes();self.freeze_status.set('Selected freezes stopped.')

    def stop_all_freezes(self):
        self.value_freezes.clear();self.freeze_health.set(False)
        self.draw_value_freezes();self.freeze_status.set('All freezes stopped.')

    def poll_value_freezes(self):
        """UI status refresh only; fast game-memory checks run independently."""
        last=None
        while True:
            try:
                last=self._freeze_worker_messages.get_nowait()
            except queue.Empty:
                break
        if last is not None:
            self.freeze_status.set(last)
            if not self.value_freezes.active():
                self.draw_value_freezes()
        self.freeze_health.set(self.value_freezes.keep_health)
        self.root.after(150,self.poll_value_freezes)
