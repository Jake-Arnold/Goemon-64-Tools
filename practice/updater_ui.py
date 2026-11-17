"""Dashboard updater with a user-selected stable, test or release target.

Git calls run on a worker; only the main Tk thread changes Tk widgets.
Installing a version triggers normal toolkit shutdown and relaunch.
"""
from __future__ import annotations

from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk

from practice.updater import (
    UpdateError, VersionTarget, check_for_updates, detect_installed_target,
    install_update, list_available_versions,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class UpdaterMixin:
    def build_update_controls(self, parent):
        card = ttk.LabelFrame(parent, text=' Toolkit updates and versions ', padding=6)
        card.pack(fill='x', pady=(0, 6))
        self.update_status = tk.StringVar(
            value='Choose a stable, test or tagged version. No automatic changes at startup.')
        ttk.Label(card, textvariable=self.update_status, style='CardMuted.TLabel',
                  wraplength=410).pack(anchor='w', pady=(0, 3))
        target_row = ttk.Frame(card)
        target_row.pack(fill='x', pady=(0, 3))
        self.update_target_choice = tk.StringVar(value='Load available versions')
        self.update_version_box = ttk.Combobox(
            target_row, textvariable=self.update_target_choice, state='disabled',
            values=(), width=30)
        self.update_version_box.pack(side='left', fill='x', expand=True)
        self.update_version_box.bind(
            '<<ComboboxSelected>>', self.on_update_target_selected)
        self.update_refresh_button = ttk.Button(
            target_row, text='Refresh versions', command=self.on_refresh_versions)
        self.update_refresh_button.pack(side='left', padx=(7, 0))
        self.update_button = ttk.Button(
            card, text='Check for updates', command=self.on_update_button)
        self.update_button.pack(fill='x')

        self._update_targets = {}
        self._update_ready = None
        self._update_busy = False
        self._update_queue = queue.SimpleQueue()
        self._restart_after_update = False
        self.update_card = card

    def _set_update_busy(self, busy):
        self._update_busy = busy
        self.update_button.state(['disabled'] if busy else ['!disabled'])
        self.update_refresh_button.state(
            ['disabled'] if busy else ['!disabled'])
        self.update_version_box.configure(
            state='disabled' if busy or not self._update_targets else 'readonly')

    def _start_update_work(self, operation, selected=None, checked=None):
        if self._update_busy:
            return
        self._set_update_busy(True)
        if operation == 'list':
            self.update_status.set('Loading toolkit branches and release tags from GitHub...')
        elif operation in ('catalog_check', 'check'):
            self.update_status.set('Checking selected GitHub version...')
        else:
            self.update_status.set('Installing selected version...')
        def work():
            try:
                if operation in ('list', 'catalog_check'):
                    targets = list_available_versions(PROJECT_ROOT)
                    detected = detect_installed_target(PROJECT_ROOT, targets)
                    result = (targets, detected)
                    if operation == 'catalog_check':
                        target = detected or next(t for t in targets
                                                  if t.kind == 'branch'
                                                  and t.name == 'main')
                        result = (targets, detected,
                                  check_for_updates(PROJECT_ROOT, target))
                elif operation == 'check':
                    result = check_for_updates(PROJECT_ROOT, selected)
                else:
                    result = install_update(PROJECT_ROOT, checked)
                self._update_queue.put((operation, result, None))
            except (UpdateError, OSError, ValueError) as exc:
                self._update_queue.put((operation, None, str(exc)))
        threading.Thread(
            target=work, name='GoemonToolkitVersionManager',
            daemon=True).start()
        self.root.after(100, self._poll_update_result)

    def on_refresh_versions(self):
        self._start_update_work('list')

    def on_update_button(self):
        if self._update_busy:
            return
        if self._update_ready is not None:
            self._start_update_work('install', checked=self._update_ready)
        elif not self._update_targets:
            self._start_update_work('catalog_check')
        else:
            selected = self._update_targets.get(self.update_target_choice.get())
            if selected is None:
                self.update_status.set('Select a version from the list.')
                return
            self._start_update_work('check', selected=selected)

    def on_update_target_selected(self, _event=None):
        if self._update_busy:
            return
        self._update_ready = None
        self.update_button.configure(text='Check for updates')
        target = self._update_targets.get(self.update_target_choice.get())
        self.update_status.set(
            ('Selected ' + target.label + '. Check before installing.')
            if target else 'Select a version from the list.')

    def _poll_update_result(self):
        try:
            operation, result, error = self._update_queue.get_nowait()
        except queue.Empty:
            try:
                if self.root.winfo_exists():
                    self.root.after(100, self._poll_update_result)
            except tk.TclError:
                pass
            return
        if operation in ('list', 'catalog_check'):
            self._handle_catalog_result(operation, result, error)
        else:
            self._handle_update_result(operation == 'install', result, error)

    def _handle_catalog_result(self, operation, result, error):
        self._set_update_busy(False)
        if error:
            self._update_ready = None
            self.update_button.configure(text='Check for updates')
            self.update_status.set('Version list unavailable: ' + error)
            return
        targets, detected = result[:2]
        old_label = self.update_target_choice.get()
        self._update_targets = {target.label: target for target in targets}
        self.update_version_box.configure(values=tuple(self._update_targets))
        if old_label in self._update_targets:
            chosen = self._update_targets[old_label]
        else:
            chosen = detected or next(
                t for t in targets if t.kind == 'branch' and t.name == 'main')
        self.update_target_choice.set(chosen.label)
        self._update_ready = None
        self.update_button.configure(text='Check for updates')
        self._set_update_busy(False)
        self.update_status.set(
            f'{len(targets)} versions available. Selected {chosen.label}.')
        if operation == 'catalog_check':
            # The initial Check button selects the installed version or main.
            # Avoid displaying a checked update for a different selection.
            status = result[2]
            if (chosen.kind == status.target_kind
                    and chosen.name == status.branch):
                self._handle_update_result(False, status, None)

    def _handle_update_result(self, installing, result, error):
        """Single Tk-thread result handler; deterministic under GUI tests."""
        self._set_update_busy(False)
        if error:
            self._update_ready = None
            self.update_status.set('Update unavailable: ' + error)
            self.update_button.configure(text='Check for updates')
            return
        if installing:
            self._update_ready = None
            self.update_status.set(
                f'Installed selected version {result[:9]}; restarting toolkit.')
            self.update_button.configure(text='Restarting...')
            self._set_update_busy(True)
            self._restart_after_update = True
            self.root.after(100, self.root.destroy)
            return
        if result.state in ('available', 'switch'):
            self._update_ready = result
            self.update_status.set(
                result.message + ' Install and restart to apply.')
            self.update_button.configure(
                text=('Switch version and restart'
                      if result.state == 'switch' else
                      'Install update and restart'))
        else:
            self._update_ready = None
            self.update_status.set(result.message)
            self.update_button.configure(text='Check for updates')
        self._set_update_busy(False)
