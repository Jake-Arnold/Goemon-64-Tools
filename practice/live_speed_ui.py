"""Live 1x/2x control for a compatible recomp host."""
from pathlib import Path
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog
from speed.launch_recomp import launch
from speed.live_control import read_speed, request_speed, SpeedUnavailable


class LiveSpeedMixin:
    def build_live_speed_controls(self, parent):
        frame = ttk.LabelFrame(parent, text=' Game speed (recomp) ', padding=8)
        frame.pack(fill='x', pady=(0, 8))
        binary_name = 'Goemon64Recompiled' if sys.platform == 'linux' else 'Goemon64Recompiled.exe'
        default = Path.home() / 'g64-speed-build' / 'build-speed' / binary_name
        self.speed_executable = tk.StringVar(value=str(default) if default.is_file() else '')
        row = ttk.Frame(frame); row.pack(fill='x')
        ttk.Entry(row, textvariable=self.speed_executable).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text='Browse', command=self.browse_speed_executable).pack(side='left', padx=4)
        self.speed_launch_button = ttk.Button(frame, text='Launch speed-enabled recomp', command=self.launch_speed_game)
        self.speed_launch_button.pack(anchor='w', pady=(5, 0))
        speed_row = ttk.Frame(frame); speed_row.pack(anchor='w', pady=(4, 0))
        self.live_speed_enabled = tk.BooleanVar(value=False)
        self.live_speed_factor = tk.StringVar(value='2×')
        self.live_speed_button = ttk.Checkbutton(speed_row, text='Speed up', variable=self.live_speed_enabled,
                                                 command=self.toggle_live_speed, state='disabled')
        self.live_speed_button.pack(side='left')
        self.live_speed_combo = ttk.Combobox(speed_row, textvariable=self.live_speed_factor,
                                              values=('2×','3×','4×'), state='readonly', width=5)
        self.live_speed_combo.pack(side='left', padx=5)
        self.live_speed_combo.bind('<<ComboboxSelected>>', self.change_live_speed_factor)
        note = ('Requires a separately rebuilt speed-patched native Linux recomp; '
                'the stock Linux build has no live control channel.' if sys.platform == 'linux'
                else 'The local speed build uses separate portable saves. '
                     'Speed and audio behavior are experimental.')
        ttk.Label(frame, text=note, wraplength=390,
                  style='CardMuted.TLabel').pack(anchor='w')
        self.live_speed_status = tk.StringVar(value='Connect to a speed-enabled recomp to control speed.')
        ttk.Label(frame, textvariable=self.live_speed_status, wraplength=390, style='CardMuted.TLabel').pack(anchor='w')
        self._speed_pid = None
        self._speed_requested = None
        self._speed_requested_at = None
        self._speed_last_target = None
        if getattr(self.args, 'read_only', False): self.speed_launch_button.state(['disabled'])
        self.root.after(500, self.poll_live_speed)

    def browse_speed_executable(self):
        kind = [('All files', '*')] if sys.platform == 'linux' else [('Executable', '*.exe'), ('All files', '*')]
        selected = filedialog.askopenfilename(title='Choose a speed-patched recomp executable', filetypes=kind)
        if selected: self.speed_executable.set(selected)

    def launch_speed_game(self):
        if getattr(self.args, 'read_only', False):
            self.live_speed_status.set('Game launching is disabled in read-only mode.')
            return
        try:
            path = Path(self.speed_executable.get().strip())
            process = launch(path, 1)
            self._speed_pid = process.pid
            self._speed_requested = None
            self.pid_text.set(str(process.pid))
            self.connection_target.set('recomp')
            self.live_speed_status.set(f'Launched PID {process.pid}; connect after the game starts.')
        except (OSError, ValueError) as exc:
            self.live_speed_status.set(f'Could not launch speed-enabled game: {exc}')

    def change_live_speed_factor(self, _event=None):
        if self.live_speed_enabled.get(): self.toggle_live_speed()

    def toggle_live_speed(self):
        if getattr(self.args, 'read_only', False):
            self.live_speed_enabled.set(False)
            self.live_speed_status.set('Speed changes are disabled in read-only mode.')
            return
        pid = self.game_pid or self._speed_pid
        try:
            if not pid: raise SpeedUnavailable('Connect to or launch a speed-enabled recomp')
            if self.live_speed_factor.get() not in ('2×','3×','4×'):raise ValueError('Choose 2×, 3× or 4×')
            target = int(self.live_speed_factor.get()[0]) if self.live_speed_enabled.get() else 1
            request_speed(pid, target)
            self._speed_last_target = pid
            self._speed_requested = target
            self._speed_requested_at = time.monotonic()
            self.live_speed_status.set(f'PID {pid}: applying {target}×…')
        except (OSError, ValueError, SpeedUnavailable) as exc:
            self._speed_requested = None
            self.live_speed_status.set(f'Speed unavailable: {exc}')
            self.live_speed_button.state(['disabled'])

    def poll_live_speed(self):
        pid = self.game_pid or self._speed_pid
        if pid != self._speed_last_target:
            self._speed_last_target = pid
            self._speed_requested = None
            self._speed_requested_at = None
        if not pid:
            self.live_speed_button.state(['disabled'])
        else:
            try:
                state = read_speed(pid)
                if not getattr(self.args, 'read_only', False): self.live_speed_button.state(['!disabled'])
                if self._speed_requested is None or state.applied == self._speed_requested:
                    self._speed_requested = None
                    self.live_speed_enabled.set(state.applied > 1)
                    if state.applied > 1:self.live_speed_factor.set(f'{state.applied}×')
                    self.live_speed_status.set(f'PID {pid}: host reports {state.applied}×; gameplay/audio verification pending.')
                elif time.monotonic() - self._speed_requested_at > 3:
                    self._speed_requested = None
                    self.live_speed_enabled.set(state.applied > 1)
                    if state.applied > 1:self.live_speed_factor.set(f'{state.applied}×')
                    self.live_speed_status.set(f'PID {pid}: no speed acknowledgement; host reports {state.applied}×.')
                else:
                    self.live_speed_status.set(f'PID {pid}: applying {self._speed_requested}×…')
            except (OSError, ValueError, SpeedUnavailable):
                self.live_speed_button.state(['disabled'])
                self.live_speed_status.set(f'PID {pid}: live speed unavailable until a compatible recomp is running.')
        self.root.after(500, self.poll_live_speed)
