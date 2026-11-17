"""Dashboard-facing update check and one-click installation.

All Git and network operations happen on a worker. Tk state is accessed only
on its own thread. A successful update requests normal toolkit shutdown so
freeze workers and emulator handles close before relaunching the new code.
"""
from __future__ import annotations

from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk

from practice.updater import check_for_updates, install_update, UpdateError


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class UpdaterMixin:
    def build_update_controls(self, parent):
        card = ttk.LabelFrame(parent, text=' Toolkit updates ', padding=10)
        card.pack(fill='x', pady=(0, 6))
        self.update_status = tk.StringVar(
            value='Check for new toolkit code on the main GitHub branch.')
        ttk.Label(card, textvariable=self.update_status, style='CardMuted.TLabel',
                  wraplength=410).pack(anchor='w', pady=(0, 7))
        self.update_button = ttk.Button(
            card, text='Check for updates', command=self.on_update_button)
        self.update_button.pack(fill='x')
        self._update_ready = None
        self._update_busy = False
        self._update_queue = queue.SimpleQueue()
        self._restart_after_update = False
        self.update_card = card

    def on_update_button(self):
        if self._update_busy:
            return
        installing = self._update_ready is not None
        checked = self._update_ready
        self._update_busy = True
        self.update_button.state(['disabled'])
        self.update_status.set(
            'Installing checked update...' if installing else
            'Checking canonical GitHub main for updates...')
        def work():
            try:
                if installing:
                    result = install_update(PROJECT_ROOT, checked)
                else:
                    result = check_for_updates(PROJECT_ROOT)
                self._update_queue.put((installing, result, None))
            except (UpdateError, OSError, ValueError) as exc:
                self._update_queue.put((installing, None, str(exc)))
        threading.Thread(
            target=work, name='GoemonToolkitUpdater', daemon=True).start()
        self.root.after(100, self._poll_update_result)

    def _poll_update_result(self):
        try:
            installing, result, error = self._update_queue.get_nowait()
        except queue.Empty:
            try:
                if self.root.winfo_exists():
                    self.root.after(100, self._poll_update_result)
            except tk.TclError:
                pass
            return
        self._handle_update_result(installing, result, error)

    def _handle_update_result(self, installing, result, error):
        """Single Tk-thread result handler; deterministic under GUI tests."""
        self._update_busy = False
        if error:
            self._update_ready = None
            self.update_status.set('Update unavailable: ' + error)
            self.update_button.configure(text='Check for updates')
            self.update_button.state(['!disabled'])
            return
        if installing:
            self._update_ready = None
            self.update_status.set(
                f'Updated to main {result[:9]}; restarting toolkit.')
            self.update_button.configure(text='Restarting...')
            self.update_button.state(['disabled'])
            self._restart_after_update = True
            self.root.after(100, self.root.destroy)
            return
        if result.state == 'available':
            self._update_ready = result
            self.update_status.set(
                result.message + ' Install it and restart the toolkit.')
            self.update_button.configure(text='Install update and restart')
        else:
            self._update_ready = None
            self.update_status.set(result.message)
            self.update_button.configure(text='Check for updates')
        self.update_button.state(['!disabled'])
