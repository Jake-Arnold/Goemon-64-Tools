"""Read-only, damage-triggered event capture tab for the practice toolkit."""
from __future__ import annotations

from datetime import datetime
import json
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

from practice.damage_event_capture import (
    DamageRecorder, candidate_report, event_timeline, export_report,
)
from practice.reports import create_discovery_report, DISCOVERY_KINDS


class DamageEventCaptureMixin:
    def build_damage_event_capture_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Record damage")
        self.damage_capture_tab = tab
        self.damage_recorder = None
        self.damage_capture_worker = None
        self.damage_capture_stop = None
        self.damage_capture_queue = queue.SimpleQueue()
        self.damage_capture_generation = 0
        self.damage_capture_rows = []
        self.damage_capture_ranked_count = -1
        self.damage_report_name = tk.StringVar(value="Damage and invulnerability research")
        self.damage_capture_status = tk.StringVar(
            value="Stopped. Connect to a running game and start recording.")
        self.damage_capture_timeline = tk.StringVar(
            value="Select a candidate to inspect its first completed event.")

        ttk.Label(tab, text="Automatic damage-event capture",
                  font=("Segoe UI Semibold", 16)).pack(anchor="w", pady=(0, 7))
        ttk.Label(tab, text=(
            "Read-only recorder: keeps 30 pre-hit samples, detects a decrease in "
            "health, then records 3.5 seconds after the hit. Samples focused "
            "globals and player task/object memory at a best-effort 25 Hz. "
            "Repeat hits to rank candidate timers and flags. Results are "
            "correlations, not proven collision or immunity controls."),
            wraplength=1070).pack(anchor="w", pady=(0, 10))
        bar = ttk.Frame(tab)
        bar.pack(fill="x", pady=(0, 7))
        ttk.Button(bar, text="Start recording",
                   command=self.start_damage_capture).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Stop",
                   command=self.stop_damage_capture).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Clear",
                   command=self.clear_damage_capture).pack(side="left", padx=(0, 6))
        ttk.Label(bar, text="Investigation name").pack(side="left", padx=(0, 4))
        ttk.Entry(bar, textvariable=self.damage_report_name, width=27).pack(
            side="left", padx=(0, 6))
        ttk.Button(bar, text="Save report",
                   command=self.export_damage_capture).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Watch selected",
                   command=self.watch_damage_candidate).pack(side="left", padx=(0, 6))
        ttk.Label(tab, textvariable=self.damage_capture_status,
                  wraplength=1060).pack(anchor="w", pady=(0, 10))

        columns = ("address", "type", "region", "hits", "returns", "score")
        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)
        self.damage_capture_tree = ttk.Treeview(
            frame, columns=columns, show="headings", height=17)
        for key, title, width in (
            ("address", "N64 address", 165),
            ("type", "Type", 75),
            ("region", "Memory region", 165),
            ("hits", "Events changed", 135),
            ("returns", "Returned to baseline", 185),
            ("score", "Rank", 80),
        ):
            self.damage_capture_tree.heading(key, text=title)
            self.damage_capture_tree.column(
                key, width=width, anchor="w", stretch=key == "region")
        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                  command=self.damage_capture_tree.yview)
        self.damage_capture_tree.configure(yscrollcommand=scrollbar.set)
        self.damage_capture_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.damage_capture_tree.bind(
            "<<TreeviewSelect>>", self._show_damage_timeline)
        ttk.Label(tab, textvariable=self.damage_capture_timeline,
                  wraplength=1050).pack(anchor="w", pady=(8, 5))

    def start_damage_capture(self):
        japan = self.active_version.key == 'japan'
        ram = self.jp_rdram if japan else self.mem
        if ram is None:
            self.damage_capture_status.set(
                'Connect to verified Japan-0 RDRAM first.' if japan
                else 'Connect to a running USA game first.')
            return
        self.stop_damage_capture(quiet=True)
        if (self.damage_capture_worker is not None and
                self.damage_capture_worker.is_alive()):
            self.damage_capture_status.set("Previous capture is still stopping.")
            return
        self.damage_capture_generation += 1
        generation = self.damage_capture_generation
        if japan:
            from practice.japan_damage_capture import JapanDamageRecorder
            recorder = JapanDamageRecorder(ram)
        else:
            recorder = DamageRecorder(ram)
        signal = threading.Event()
        self.damage_recorder = recorder
        self.damage_capture_stop = signal
        self.damage_capture_rows = []
        self.damage_capture_ranked_count = -1
        self.damage_capture_tree.delete(*self.damage_capture_tree.get_children())
        self.damage_capture_timeline.set("Select a candidate after the first completed hit.")
        self.damage_capture_status.set(
            f"Recording {('Japan-0' if japan else 'USA')} read-only damage "
            "events. Take damage during normal gameplay; maximum eight events.")

        def worker():
            error = None
            try:
                while not signal.is_set() and not recorder.stopped:
                    # Coordinate game process access with reconnection and freezes.
                    guard = self.value_freezes.guard
                    with guard:
                        if signal.is_set():
                            break
                        recorder.sample()
                    signal.wait(0.04)
            except (OSError, ValueError, RuntimeError) as exc:
                error = str(exc)
            finally:
                recorder.stop()
                self.damage_capture_queue.put((generation, error))

        self.damage_capture_worker = threading.Thread(
            target=worker, daemon=True, name="GoemonDamageEventCapture")
        self.damage_capture_worker.start()
        self.root.after(150, lambda: self._poll_damage_capture(generation))

    def _poll_damage_capture(self, generation):
        if generation != self.damage_capture_generation:
            return
        finished = False
        error = None
        while True:
            try:
                token, message = self.damage_capture_queue.get_nowait()
            except queue.Empty:
                break
            if token == generation:
                finished = True
                error = message
        recorder = self.damage_recorder
        if recorder is None:
            return
        complete = sum(e.complete for e in recorder.events)
        if complete != self.damage_capture_ranked_count or finished:
            self._refresh_damage_capture_rows()
            self.damage_capture_ranked_count = complete
        partial = len(recorder.events) - complete
        status = (
            f"{recorder.samples} samples; {complete} complete hits; "
            f"{partial} partial; {len(self.damage_capture_rows)} ranked candidates.")
        if recorder.active is not None:
            status += " Recording post-hit window."
        if error:
            status += f" Stopped: {error}"
        elif finished or recorder.stopped:
            status += " Stopped."
        else:
            status += " Recording."
        self.damage_capture_status.set(status)
        if not finished and self.damage_capture_worker.is_alive():
            self.root.after(250, lambda: self._poll_damage_capture(generation))

    def _refresh_damage_capture_rows(self):
        if self.damage_recorder is None:
            return
        rows = candidate_report(self.damage_recorder.events)
        selected = self.damage_capture_tree.selection()
        selected_key = None
        if selected:
            values = self.damage_capture_tree.item(selected[0], "values")
            selected_key = (values[0], values[1])
        self.damage_capture_rows = rows
        self.damage_capture_tree.delete(*self.damage_capture_tree.get_children())
        for i, row in enumerate(rows):
            self.damage_capture_tree.insert("", "end", iid=str(i), values=(
                row["address"], row["type"], row["region"],
                row["hits"], row["returns"], row["score"]))
            if selected_key == (row["address"], row["type"]):
                self.damage_capture_tree.selection_set(str(i))

    def _show_damage_timeline(self, _event=None):
        selected = self.damage_capture_tree.selection()
        recorder = self.damage_recorder
        if not selected or recorder is None:
            return
        idx = int(selected[0])
        if idx >= len(self.damage_capture_rows):
            return
        row = self.damage_capture_rows[idx]
        completed = [e for e in recorder.events if e.complete]
        if not completed:
            return
        samples = event_timeline(completed[0], row)
        step = max(1, len(samples) // 12)
        preview = ", ".join(
            f"{p['t']:+.2f}s:{p['value']}" for p in samples[::step][:12])
        self.damage_capture_timeline.set(
            f"{row['address']} [{row['type']}]  {preview}")

    def stop_damage_capture(self, quiet=False):
        signal = getattr(self, "damage_capture_stop", None)
        if signal is not None:
            signal.set()
        worker = getattr(self, "damage_capture_worker", None)
        if (worker is not None and worker.is_alive() and
                worker is not threading.current_thread()):
            # No timeout: prevent the process handle from being closed
            # while an event-capture read is still in progress.
            worker.join()
        if not quiet and hasattr(self, "damage_capture_status"):
            self._refresh_damage_capture_rows()
            self.damage_capture_status.set(
                "Capture stopped. Completed events remain available.")

    def clear_damage_capture(self):
        self.stop_damage_capture(quiet=True)
        self.damage_capture_generation += 1
        self.damage_recorder = None
        self.damage_capture_rows = []
        self.damage_capture_ranked_count = -1
        self.damage_capture_tree.delete(*self.damage_capture_tree.get_children())
        self.damage_capture_timeline.set("No candidate selected.")
        self.damage_capture_status.set("Cleared. Game memory was not modified.")

    def export_damage_capture(self):
        recorder = self.damage_recorder
        if recorder is None or not recorder.events:
            self.damage_capture_status.set("Record at least one damage event first.")
            return
        if self.damage_capture_worker and self.damage_capture_worker.is_alive():
            self.damage_capture_status.set(
                "Stop recording before saving a complete, stable report.")
            return
        try:
            from practice.damage_event_capture import candidate_report
            # Keep the entire ranked candidate list in CSV/JSON. Full detailed
            # timelines are bounded to the strongest 300 due to output size.
            all_rows = candidate_report(recorder.events, limit=100000)
            report = export_report(recorder, limit=min(300, len(all_rows)))
            region = getattr(recorder, 'region', self.active_version.key)
            report['game_version'] = region
            report['hp_guest_address'] = (
                f"0x{getattr(recorder, 'hp_address', 0x8015C5E4):08X}")
            report['detailed_timeline_candidate_count'] = len(report['candidates'])
            path = create_discovery_report(
                region=region,
                title=self.damage_report_name.get(),
                kind='damage-events',
                candidates=all_rows,
                evidence={'source_report': report,
                          'ranked_candidates': all_rows,
                          'event_summaries': report.get('events', [])},
                metadata={
                    'backend': getattr(self, 'jp_backend', None) if region == 'japan' else 'usa-recomp-or-project64',
                    'sample_count': recorder.samples,
                    'recorded_events': len(recorder.events),
                    'completed_events': sum(event.complete for event in recorder.events),
                    'timelines_with_full_samples': len(report['candidates']),
                    'health_address': report['hp_guest_address'],
                    'recording_stopped': True,
                },
                notes=[
                    'The full ranked candidate list is saved.',
                    'Detailed time-series values are saved for up to the strongest 300 candidates. '
                    'The source recorder does not preserve every raw RAM snapshot for export.',
                    'Correlations around damage are not proven collision or invulnerability controls.',
                ])
            if hasattr(self, 'refresh_reports'):
                self.refresh_reports(select_path=path)
            self.damage_capture_status.set(
                f"Saved {len(all_rows):,} candidates and {len(recorder.events)} "
                "damage event(s). Open Reports to view the investigation.")
        except (OSError, ValueError, TypeError) as exc:
            self.damage_capture_status.set(f"Save report failed: {exc}")

    def watch_damage_candidate(self):
        selected = self.damage_capture_tree.selection()
        if not selected:
            self.damage_capture_status.set("Select a candidate first.")
            return
        row = self.damage_capture_rows[int(selected[0])]
        self.user_watch_name.set(f"Damage candidate {row['address']}")
        self.user_watch_address.set(row["address"])
        self.user_watch_type.set(row["type"])
        self.add_custom_watch()
        self.notebook.select(self.live_memory_tab)
