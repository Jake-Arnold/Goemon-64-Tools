"""Shared, searchable offline-first address catalogue inside Live Memory.

Only the selected row is read on request. Remote metadata refresh and guest
reads run off the Tk thread. This page never writes any game-memory bytes.
"""
from __future__ import annotations

from collections import Counter
import json
import queue
import threading
import tkinter as tk
from tkinter import ttk

from practice.address_registry import load_registry
from practice.address_catalogue import (
    audit_catalogue, decode_read, search_entries, validate_catalogue,
)
from practice.address_catalogue_remote import (
    load_cached_discoveries, merge_remote_catalogue,
    refresh_address_discoveries,
)
from practice.custom_watches import FORMATS


class AddressCatalogueUI:
    def build_address_catalogue_page(self, parent):
        self.address_catalogue_page = parent
        self.catalogue_status = tk.StringVar(value="Loading bundled memory registry...")
        self.catalogue_query = tk.StringVar(value="")
        self.catalogue_region = tk.StringVar(value="all")
        self.catalogue_evidence = tk.StringVar(value="all")
        self.catalogue_category = tk.StringVar(value="all")
        self.catalogue_type = tk.StringVar(value="all")
        self.catalogue_selected = tk.StringVar(value="No address selected")
        self.catalogue_busy = False
        self.catalogue_events = queue.SimpleQueue()
        self.catalogue_sort = ("address", False)
        self.catalogue_remote_info = {}
        self.catalogue_loaded = False
        self.catalogue_rows = {}
        self.catalogue_payload = None

        header = ttk.Frame(parent)
        header.pack(fill="x", pady=(0, 6))
        ttk.Label(header, text="Memory Address Catalogue",
                  font=("Segoe UI Semibold", 15)).pack(side="left")
        ttk.Button(header, text="Refresh Address Catalogue",
                   command=self.refresh_address_catalogue).pack(
                       side="right")
        ttk.Label(parent, textvariable=self.catalogue_status,
                  style="Muted.TLabel", wraplength=1050).pack(
                      anchor="w", pady=(0, 6))

        search = ttk.Frame(parent)
        search.pack(fill="x", pady=(0, 6))
        ttk.Label(search, text="Search address, name, field ID, evidence:").pack(
            side="left")
        ttk.Entry(search, textvariable=self.catalogue_query,
                  width=56).pack(side="left", fill="x", expand=True,
                                 padx=(8, 0))
        filters = ttk.Frame(parent)
        filters.pack(fill="x", pady=(0, 8))
        self.catalogue_filters = {}
        for label, state, width in (
                ("Region", self.catalogue_region, 12),
                ("Evidence", self.catalogue_evidence, 21),
                ("Category", self.catalogue_category, 22),
                ("Type", self.catalogue_type, 12)):
            ttk.Label(filters, text=label).pack(side="left", padx=(0, 4))
            widget = ttk.Combobox(
                filters, textvariable=state, state="readonly",
                values=("all",), width=width)
            widget.pack(side="left", padx=(0, 12))
            widget.bind("<<ComboboxSelected>>",
                        lambda _e: self.filter_address_catalogue())
            self.catalogue_filters[label] = widget
        result_frame = ttk.Frame(parent)
        result_frame.pack(fill="both", expand=True)
        names = ("address", "region", "category", "type", "evidence", "control")
        table = ttk.Treeview(
            result_frame, columns=names, show="tree headings",
            selectmode="browse", height=15)
        table.heading("#0", text="Field / research entry",
                      command=lambda: self.sort_address_catalogue("name"))
        table.column("#0", width=275, stretch=True)
        for key, label, width in (
                ("address", "Guest address", 115),
                ("region", "Region", 67),
                ("category", "Category", 126),
                ("type", "Decode", 76),
                ("evidence", "Evidence", 150),
                ("control", "Existing control", 170)):
            table.heading(
                key, text=label,
                command=lambda sort_key=key:
                self.sort_address_catalogue(sort_key))
            table.column(key, width=width, stretch=key in ("category", "control"))
        vertical = ttk.Scrollbar(result_frame, command=table.yview)
        table.configure(yscrollcommand=vertical.set)
        vertical.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        table.bind("<<TreeviewSelect>>", self.select_catalogue_address)
        self.catalogue_tree = table

        button_row = ttk.Frame(parent)
        button_row.pack(fill="x", pady=(6, 4))
        for caption, action in (
                ("Copy address", self.copy_catalogue_address),
                ("Copy address + mask", self.copy_catalogue_address_mask),
                ("Add to Live watches", self.add_catalogue_watch),
                ("Inspect live value", self.inspect_catalogue_address),
                ("Open existing control", self.open_catalogue_control)):
            ttk.Button(button_row, text=caption,
                       command=action).pack(side="left", padx=(0, 7))
        ttk.Label(parent, textvariable=self.catalogue_selected,
                  style="Muted.TLabel", wraplength=1080).pack(
                      anchor="w", pady=(0, 3))

        detail_frame = ttk.Frame(parent)
        detail_frame.pack(fill="x")
        detail = tk.Text(
            detail_frame, height=7, wrap="word", state="disabled",
            background="#1a1d23", foreground="#f3eee5",
            selectbackground="#784f28", font=("Consolas", 10))
        detail_scroll = ttk.Scrollbar(detail_frame, command=detail.yview)
        detail.configure(yscrollcommand=detail_scroll.set)
        detail.pack(side="left", fill="both", expand=True)
        detail_scroll.pack(side="right", fill="y")
        self.catalogue_detail = detail
        for var in (
                self.catalogue_query, self.catalogue_region,
                self.catalogue_category, self.catalogue_evidence,
                self.catalogue_type):
            var.trace_add("write", lambda *_:
                          self.filter_address_catalogue())

    def show_address_catalogue(self, _event=None):
        if self.catalogue_loaded:
            return
        try:
            local = load_registry()[0]
            validate_catalogue(local)
            cached = load_cached_discoveries()
            if cached:
                local, self.catalogue_remote_info = merge_remote_catalogue(
                    local, cached)
            self.catalogue_payload = local
            self.catalogue_rows = {row["id"]: row for row in local["entries"]}
            for name, key in (
                    ("Evidence", "confidence"),
                    ("Category", "category"),
                    ("Type", "data_type")):
                options = sorted(set(
                    str(r.get(key) or "unknown") for r in local["entries"]))
                self.catalogue_filters[name].configure(values=("all", *options))
            self.catalogue_filters["Region"].configure(
                values=("all", "usa", "japan", "unknown"))
            self.catalogue_loaded = True
            self.filter_address_catalogue()
        except (OSError, ValueError, KeyError, TypeError) as exc:
            self.catalogue_status.set(f"Unable to open address registry: {exc}")

    def _selected_catalogue_entry(self):
        selected = self.catalogue_tree.selection()
        if len(selected) != 1:
            return None
        return self.catalogue_rows.get(selected[0])

    def _catalogue_matches(self):
        if self.catalogue_payload is None:
            return []
        q = self.catalogue_query.get().strip()
        matches = search_entries(
            self.catalogue_payload, q,
            region=self.catalogue_region.get(),
            evidence=self.catalogue_evidence.get(),
            category=self.catalogue_category.get(),
            data_type=("all" if self.catalogue_type.get() == "all"
                       else None if self.catalogue_type.get() == "unknown"
                       else self.catalogue_type.get()))
        key, reversed_order = self.catalogue_sort
        def sorting(record):
            if key == "name":
                return record["name"].casefold()
            if key == "address":
                return (record["address"], record["region"])
            return str(record.get(
                {"type": "data_type", "evidence": "confidence",
                 "control": "control"}.get(key, key)) or "").casefold()
        return sorted(matches, key=sorting, reverse=reversed_order)

    def filter_address_catalogue(self):
        if not self.catalogue_loaded:
            return
        rows = self._catalogue_matches()
        table = self.catalogue_tree
        selected = table.selection()
        table.delete(*table.get_children())
        for row in rows:
            table.insert(
                "", "end", iid=row["id"], text=row["name"],
                values=(row["address"], row["region"],
                        row["category"], row.get("data_type") or "—",
                        row["confidence"], row.get("control") or "—"))
        if selected and table.exists(selected[0]):
            table.selection_set(selected[0])
        audit = audit_catalogue(self.catalogue_payload)
        sync = self.catalogue_remote_info
        extra = (f"; last sync {sync['last_sync']}"
                 if sync.get("last_sync") else "; bundled/offline")
        self.catalogue_status.set(
            f"Registry v{self.catalogue_payload['version']} · "
            f"{len(rows)} / {audit['total_records']} entries · "
            f"{audit['live_readable']} readable · "
            f"{audit['disputed']} disputed · "
            f"{sync.get('upstream_revision', 'bundled')}{extra}")

    def sort_address_catalogue(self, key):
        old_key, reversed_order = self.catalogue_sort
        self.catalogue_sort = (key, not reversed_order if old_key == key else False)
        self.filter_address_catalogue()

    def _show_catalogue_detail(self, message):
        widget = self.catalogue_detail
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", message)
        widget.configure(state="disabled")

    def select_catalogue_address(self, _event=None):
        row = self._selected_catalogue_entry()
        if not row:
            self.catalogue_selected.set("Select an address for details or a live read.")
            return
        address = int(row["address"], 16)
        width = row.get("width") or 1
        overlaps = [
            r for r in self.catalogue_payload["entries"]
            if r["id"] != row["id"] and r["region"] == row["region"]
            and int(r["address"], 16) < address + width
            and address < int(r["address"], 16) + (r.get("width") or 1)
        ][:15]
        related = (", ".join(
            f"{r['name']} ({r['address']}, {r.get('mask') or 'word'})"
            for r in overlaps) or "none")
        meta = {
            "id": row["id"], "aliases": row.get("aliases", []),
            "source_ids": row.get("id_aliases", []),
            "name": row["name"], "address": row["address"],
            "region": row["region"], "revision": row.get("revision"),
            "category": row["category"], "owner": row.get("owner"),
            "data_type": row.get("data_type"), "width": row.get("width"),
            "mask": row.get("mask"), "endian": row.get("endian"),
            "counterpart": row.get("counterpart"),
            "confidence": row["confidence"], "live_readable": row["live_readable"],
            "control": row.get("control"), "context": row.get("context"),
            "evidence": row.get("evidence"), "sources": row.get("sources"),
            "mips_refs": row.get("mips_refs"),
            "discovered": row.get("discovered"), "updated": row.get("updated"),
            "source_revision": row.get("source_revision"),
            "overlapping_or_related_fields": related,
        }
        self.catalogue_selected.set(
            f"{row['name']} · {row['address']} "
            f"{'& ' + row['mask'] if row.get('mask') else ''} "
            f"· {row['confidence']}")
        self._show_catalogue_detail(
            json.dumps(meta, indent=2, ensure_ascii=False))

    def _copy_catalogue(self, include_mask=False):
        row = self._selected_catalogue_entry()
        if not row:
            self.catalogue_selected.set("Select a field first.")
            return
        value = row["address"]
        if include_mask and row.get("mask"):
            value += f" & {row['mask']}"
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.catalogue_selected.set(f"Copied {value}")

    def copy_catalogue_address(self):
        self._copy_catalogue()

    def copy_catalogue_address_mask(self):
        self._copy_catalogue(include_mask=True)

    def add_catalogue_watch(self):
        row = self._selected_catalogue_entry()
        if not row:
            self.catalogue_selected.set("Select a field first.")
            return
        kind = row.get("data_type")
        if not row["live_readable"] or kind not in FORMATS:
            self.catalogue_selected.set(
                "This entry is research-only, dynamic/unsupported or has no decoder.")
            return
        if row["region"] != self.active_version.key:
            self.catalogue_selected.set(
                "Select the same game region before adding the address to watches.")
            return
        self.user_watch_address.set(row["address"])
        self.user_watch_type.set(kind)
        self.user_watch_name.set(row["name"][:64])
        self.add_custom_watch()
        self.catalogue_selected.set(self.inspector_status.get())

    def inspect_catalogue_address(self):
        row = self._selected_catalogue_entry()
        if not row:
            self.catalogue_selected.set("Select a field first.")
            return
        if not row["live_readable"]:
            self.catalogue_selected.set(
                "No live read: code VMA, external lead, unknown width or unsafe lifetime.")
            return
        if row["region"] != self.active_version.key:
            self.catalogue_selected.set(
                "Region mismatch: select the corresponding USA or Japan game.")
            return
        ram = self.mem if row["region"] == "usa" else self.jp_rdram
        if ram is None:
            self.catalogue_selected.set("Disconnected: address remains indexed offline.")
            return
        if self.catalogue_busy:
            return
        self.catalogue_busy = True
        self.catalogue_selected.set("Reading one selected guest-memory field...")
        def job():
            try:
                value, raw = decode_read(ram, row)
                self.catalogue_events.put(("read", row["id"], (value, raw), None))
            except (OSError, ValueError, PermissionError, RuntimeError) as exc:
                self.catalogue_events.put(("read", row["id"], None, str(exc)))
        threading.Thread(target=job, daemon=True,
                         name="GoemonCatalogueLiveRead").start()
        self.root.after(80, self._poll_catalogue_worker)

    def open_catalogue_control(self):
        row = self._selected_catalogue_entry()
        if not row:
            return
        control = row.get("control") or ""
        if control.startswith("Unlocks / Story"):
            self.notebook.select(self.unlock_tab)
            self.unlock_sections.select(self.unlock_flags_page)
            self.unlock_flag_query.set(row["name"])
        elif control.startswith("Unlocks / Items"):
            self.notebook.select(self.unlock_tab)
            self.unlock_sections.select(self.unlock_items_page)
        elif control.startswith("Story Progress"):
            self.notebook.select(self.story_progress_tab)
            self.story_filter.set(row["name"])
        elif control.startswith("Live memory"):
            self.live_memory_sections.select(self.live_watches_page)
        else:
            self.catalogue_selected.set(
                "No directly linked editor; research-only catalogue entry.")

    def refresh_address_catalogue(self):
        if self.catalogue_busy:
            return
        self.show_address_catalogue()
        if not self.catalogue_loaded:
            return
        self.catalogue_busy = True
        self.catalogue_selected.set("Checking official repository for metadata...")
        def job():
            try:
                remote, info = refresh_address_discoveries(branch="main")
                # Baseline metadata is canonical. Remote is descriptive only.
                local = load_registry()[0]
                merged, counts = merge_remote_catalogue(local, remote)
                self.catalogue_events.put(
                    ("refresh", None, (merged, dict(info, **counts)), None))
            except (OSError, ValueError, RuntimeError) as exc:
                self.catalogue_events.put(
                    ("refresh", None, None, str(exc)))
        threading.Thread(
            target=job, daemon=True, name="GoemonCatalogueRefresh").start()
        self.root.after(80, self._poll_catalogue_worker)

    def _poll_catalogue_worker(self):
        try:
            kind, selected, outcome, error = self.catalogue_events.get_nowait()
        except queue.Empty:
            try:
                if self.root.winfo_exists():
                    self.root.after(80, self._poll_catalogue_worker)
            except tk.TclError:
                pass
            return
        self.catalogue_busy = False
        if error:
            self.catalogue_selected.set(
                "Catalogue operation unavailable: " + error)
            return
        if kind == "refresh":
            self.catalogue_payload, self.catalogue_remote_info = outcome
            self.catalogue_rows = {
                r["id"]: r for r in self.catalogue_payload["entries"]}
            self.filter_address_catalogue()
            self.catalogue_selected.set(
                f"Metadata refreshed: {self.catalogue_remote_info['added']} "
                f"added, {self.catalogue_remote_info['updated']} updated, "
                f"{self.catalogue_remote_info['disputed']} disputed.")
        elif kind == "read":
            row = self.catalogue_rows.get(selected)
            if row is None or self._selected_catalogue_entry() is not row:
                return
            value, raw = outcome
            self.catalogue_selected.set(
                f"{row['name']}: {value} · raw {raw} (read-only inspection)")
