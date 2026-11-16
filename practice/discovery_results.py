"""Shared, region-aware discovery results UI.

All research methods use the same selection, watch, live value and report
controls. Live value reads are ordinary read-only RAM reads, NOT instruction
access tracing. No code in this module writes game RAM.
"""
from __future__ import annotations

import math
import queue
import struct
import threading
import time
import tkinter as tk
from tkinter import ttk

from practice.custom_watches import (
    FORMATS, append_watch, make_watch, save_watches,
)
from practice.value_search import GUEST_BASE


LIVE_RATE_OPTIONS = ("100 ms", "250 ms", "500 ms", "1000 ms")
LIVE_COLUMNS = (
    ("address", "N64 address", 145),
    ("type", "Type", 105),
    ("live", "Live value", 140),
    ("raw", "Live hex", 145),
)


def canonical_type(kind):
    """Select a *read type*, not a purported game-field meaning."""
    kind = str(kind or "").strip().lower()
    if kind in FORMATS:
        return kind
    if kind in ("xyz", "xyz triple candidate", "f32x3"):
        return "xyz"
    if "f32" in kind or "float" in kind:
        return "f32"
    if kind.startswith("text/"):
        return None  # Variable-length text watches need length+codec metadata.
    if kind in ("", "byte", "boolean", "boolean candidate",
                "one-bit", "one-bit candidate", "saved event flag candidate",
                "character-index byte (known alias)"):
        return "u8"
    return None


def _live_width(kind):
    if kind == "xyz":
        return 12
    return FORMATS[kind][1]


def _decode(kind, data):
    if kind == "xyz":
        xyz = struct.unpack(">fff", data)
        return "(" + ", ".join(f"{v:.5g}" for v in xyz) + ")"
    fmt, _ = FORMATS[kind]
    if fmt is None:
        return "0x" + data.hex().upper()
    decoded = struct.unpack(">" + fmt, data)[0]
    if isinstance(decoded, float):
        return f"{decoded:.7g}" if math.isfinite(decoded) else str(decoded)
    return str(decoded)


def read_live_candidates(reader, candidates):
    """Read each supported candidate, batching overlapping/nearby guest ranges.

    candidates: list of {id, address, type} dictionaries. The caller captures
    the exact process/region identity separately; none of the input is trusted
    to justify writes. Reads are limited to 4 KiB in each batch.
    """
    requested = []
    result = {}
    for candidate in candidates:
        key = candidate["id"]
        kind = canonical_type(candidate.get("type"))
        if kind is None:
            result[key] = ("Unsupported type", "—")
            continue
        try:
            addr = int(str(candidate["address"]), 16)
            width = _live_width(kind)
            if not GUEST_BASE <= addr <= 0x80800000 - width:
                raise ValueError("Not a valid guest RAM address")
            requested.append((addr, width, kind, key))
        except (ValueError, TypeError, OverflowError):
            result[key] = ("Invalid address", "—")
    requested.sort()
    groups = []
    for entry in requested:
        addr, width, kind, key = entry
        if not groups or addr + width - groups[-1][0] > 4096:
            groups.append([addr, addr + width, [entry]])
        else:
            groups[-1][1] = max(groups[-1][1], addr + width)
            groups[-1][2].append(entry)
    for start, stop, group in groups:
        try:
            data = reader.read_guest(start, stop - start)
            if len(data) != stop - start:
                raise OSError("Incomplete guest RAM read")
            for addr, width, kind, key in group:
                value = data[addr - start:addr - start + width]
                result[key] = (_decode(kind, value), "0x" + value.hex().upper())
        except (OSError, ValueError, struct.error, RuntimeError) as exc:
            for _addr, _width, _kind, key in group:
                result[key] = (f"Read failed: {exc}", "—")
    return result


def add_research_watches(owner, candidates, *, label):
    """Persist all requested numeric/XYZ watches atomically per game region.

    Return (added, duplicates). Does not change owner.watch state when saving
    fails. In standalone synthetic GUI harnesses with only add_custom_watch,
    use that public compatibility API.
    """
    if not candidates:
        raise ValueError("Select one or more candidate addresses first")
    region = getattr(getattr(owner, "active_version", None), "key", "usa")
    if region not in ("usa", "japan"):
        raise ValueError("Select USA or Japan before adding watches")
    specs = []
    for candidate in candidates:
        kind = canonical_type(candidate.get("type"))
        if kind is None:
            raise ValueError(
                f"{candidate['address']}: this candidate cannot be watched as "
                "a fixed-width numeric field")
        address = int(str(candidate["address"]), 16)
        if kind == "xyz":
            # A float triple represents three independently watched floats.
            for axis, delta in (("X", 0), ("Y", 4), ("Z", 8)):
                specs.append(make_watch(
                    f"{label} {axis} 0x{address + delta:08X}",
                    address + delta, "f32"))
        else:
            specs.append(make_watch(
                f"{label} {kind} 0x{address:08X}", address, kind))

    attr = "jp_custom_watches" if region == "japan" else "custom_watches"
    existing = getattr(owner, attr, None)
    if existing is None:
        # Scanner-only test harnesses do not model persisted watch lists.
        for spec in specs:
            if region == "japan":
                owner.add_japan_custom_watch_from_search(
                    f"0x{spec.address:08X}", spec.kind)
            else:
                owner.user_watch_name.set(spec.name)
                owner.user_watch_address.set(f"0x{spec.address:08X}")
                owner.user_watch_type.set(spec.kind)
                owner.add_custom_watch()
        return len(specs), 0

    next_watches = list(existing)
    added = []
    duplicates = 0
    for spec in specs:
        if any(w.address == spec.address and w.kind == spec.kind
               for w in next_watches):
            duplicates += 1
            continue
        next_watches = append_watch(next_watches, spec)
        added.append(spec)
    if not added:
        return 0, duplicates
    if region == "japan":
        path = owner.jp_watch_path
    else:
        from practice.ui_extension import CUSTOM_WATCHES_PATH
        path = CUSTOM_WATCHES_PATH
    save_watches(path, next_watches)
    setattr(owner, attr, next_watches)
    if region == "japan":
        for spec in added:
            owner._jp_insert_custom_watch(spec)
        owner._jp_reset_comparison()
        owner.refresh_japan_fields(force=True)
    if hasattr(owner, "refresh_inspector"):
        owner.last_inspect_at = 0.0
        owner.refresh_inspector(
            owner.current if isinstance(
                getattr(owner, "current", None), dict) else {})
    return len(added), duplicates


class DiscoveryResultsPanel:
    """Consistent controls and best-effort live values for every research tab.

    All widgets and Treeviews are owned by the Tk thread. Memory reads take
    place off-thread; stale results after reconnect/region switch are dropped.
    """

    def __init__(self, owner, tab, *, tree, status, report_name, save,
                 label, refresh=None, auto=None, interval=None,
                 external_poll=False):
        self.owner = owner
        self.root = owner.root
        self.tab = tab
        self.tree_getter = tree
        self.status = status
        self.label = label
        self.report_name = report_name
        self.save_action = save
        self.refresh_action = refresh
        self.external_poll = external_poll
        self.auto = auto if auto is not None else tk.BooleanVar(value=True)
        self.interval = interval if interval is not None else tk.StringVar(
            value="250 ms")
        self.live_status = tk.StringVar(value="No candidates yet")
        self._destroyed = False
        self._busy = False
        self._pending = queue.SimpleQueue()
        self._next_at = 0.0
        self._after = None
        self._generation = 0

        controls = ttk.LabelFrame(tab, text="Results · read-only", padding=7)
        controls.pack(fill="x", pady=(0, 7))
        first = ttk.Frame(controls)
        first.pack(fill="x", pady=(0, 5))
        ttk.Button(first, text="Watch selected",
                   command=self.watch_selected).pack(side="left", padx=(0, 6))
        ttk.Button(first, text="Select visible",
                   command=self.select_visible).pack(side="left", padx=(0, 6))
        ttk.Button(first, text="Copy address",
                   command=self.copy_address).pack(side="left", padx=(0, 6))
        ttk.Button(first, text="Refresh now",
                   command=self.refresh_now).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(first, text="Live update",
                        variable=self.auto).pack(side="left", padx=(0, 7))
        ttk.Label(first, text="Every").pack(side="left", padx=(0, 4))
        ttk.Combobox(first, textvariable=self.interval,
                     values=LIVE_RATE_OPTIONS, width=9,
                     state="readonly").pack(side="left", padx=(0, 12))
        ttk.Label(first, textvariable=self.live_status).pack(
            side="left", fill="x", expand=True)
        second = ttk.Frame(controls)
        second.pack(fill="x")
        ttk.Label(second, text="Report name").pack(side="left", padx=(0, 7))
        ttk.Entry(second, textvariable=report_name, width=37).pack(
            side="left", padx=(0, 7))
        self.save_button = ttk.Button(second, text="Save report",
                                      command=save)
        self.save_button.pack(side="left", padx=(0, 10))
        ttk.Label(second, text="Ctrl/Shift-click for multiple candidates").pack(
            side="left")

        tab.bind("<Destroy>", self._on_destroy, add="+")
        if not external_poll:
            self._after = self.root.after(150, self._tick)

    @property
    def tree(self):
        return self.tree_getter()

    def _on_destroy(self, event):
        if event.widget is not self.tab:
            return
        self._destroyed = True
        self._generation += 1
        if self._after is not None:
            try:
                self.root.after_cancel(self._after)
            except tk.TclError:
                pass
            self._after = None

    def invalidate(self):
        self._generation += 1
        self._next_at = 0.0
        self._busy = False

    def _selection(self):
        return [
            {"id": iid, "address": self.tree.set(iid, "address"),
             "type": self.tree.set(iid, "type")}
            for iid in self.tree.selection()
        ]

    def select_visible(self):
        entries = self.tree.get_children()
        if entries:
            self.tree.selection_set(entries)
        self.live_status.set(f"{len(entries)} visible row(s) selected")

    def copy_address(self):
        chosen = self._selection()
        if not chosen:
            self.live_status.set("Select a candidate first")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(chosen[0]["address"])
        self.live_status.set(f"Copied {chosen[0]['address']}")

    def watch_selected(self):
        try:
            added, duplicates = add_research_watches(
                self.owner, self._selection(), label=self.label)
            if added:
                self.live_status.set(
                    f"Added {added} watch(es) to Live Memory"
                    + (f"; {duplicates} already present" if duplicates else ""))
            else:
                self.live_status.set(
                    f"All {duplicates} selected watches already exist")
            if added and hasattr(self.owner, "notebook") and hasattr(
                    self.owner, "live_memory_tab"):
                target = self.owner.live_memory_tab
                if (getattr(getattr(self.owner, "active_version", None),
                            "key", "usa") == "japan"
                        and getattr(self.owner, "jp_custom_watches", None) is None):
                    target = getattr(self.owner, "jp_fields_tab", target)
                self.owner.notebook.select(target)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            self.live_status.set(f"Cannot watch selected candidates: {exc}")

    def refresh_now(self):
        if self.refresh_action is not None:
            self.refresh_action()
        else:
            self._next_at = 0.0
            self._request_live(force=True)

    def _attached_reader(self):
        version = getattr(getattr(self.owner, "active_version", None),
                          "key", "usa")
        reader = (getattr(self.owner, "jp_rdram", None)
                  if version == "japan" else getattr(self.owner, "mem", None))
        return reader, (version, getattr(self.owner, "game_pid", None),
                        id(reader))

    def _visible(self):
        try:
            top = self.owner.discovery_tabs
            return (self.owner.notebook.select() ==
                    str(self.owner.discovery_tab) and
                    top.select() == str(self.tab))
        except (AttributeError, tk.TclError):
            try:
                return self.owner.notebook.select() == str(self.tab)
            except (AttributeError, tk.TclError):
                return False

    def _request_live(self, *, force=False):
        if self._busy or self._destroyed or (not force and not self._visible()):
            return
        reader, identity = self._attached_reader()
        if reader is None:
            if force:
                self.live_status.set("Connect to game RAM before refreshing")
            return
        tree = self.tree
        all_ids = tree.get_children()
        visible_count = max(1, int(tree.cget("height"))) + 4
        start = max(0, min(len(all_ids) - 1,
                           int(tree.yview()[0] * len(all_ids)))) if all_ids else 0
        # Prefer selected rows (including scrolled-off selections), then rows
        # in the visible scroll viewport; never re-read a huge full result set.
        wanted = list(dict.fromkeys(
            [*tree.selection(), *all_ids[start:start + visible_count]]))
        rows = [
            {"id": iid, "address": tree.set(iid, "address"),
             "type": tree.set(iid, "type")}
            for iid in wanted[:200]
        ]
        if not rows:
            if force:
                self.live_status.set("No candidates to refresh")
            return
        self._busy = True
        self._generation += 1
        generation = self._generation
        def work():
            try:
                values = read_live_candidates(reader, rows)
                self._pending.put((generation, identity, values, None))
            except Exception as exc:
                self._pending.put((generation, identity, None, str(exc)))
        threading.Thread(
            target=work, daemon=True,
            name="GoemonDiscoveryLiveRead").start()

    def _tick(self):
        self._after = None
        if self._destroyed:
            return
        try:
            while True:
                try:
                    generation, token, values, error = self._pending.get_nowait()
                except queue.Empty:
                    break
                if generation != self._generation:
                    continue
                if token != self._attached_reader()[1]:
                    self._busy = False
                    self.live_status.set("Connection changed; reconnect to refresh")
                    continue
                self._busy = False
                if error is not None:
                    self.live_status.set(f"Refresh failed: {error}")
                    continue
                tree = self.tree
                for iid, (value, raw) in values.items():
                    if tree.exists(iid):
                        tree.set(iid, "live", value)
                        tree.set(iid, "raw", raw)
                self.live_status.set(f"Updated {len(values)} live candidate(s)")
            now = time.monotonic()
            interval_ms = int(self.interval.get().split()[0])
            if (not self._busy and self.auto.get() and self._visible()
                    and now >= self._next_at):
                self._request_live()
                self._next_at = now + interval_ms / 1000
        except (tk.TclError, AttributeError, ValueError) as exc:
            if not self._destroyed:
                self.live_status.set(f"Live update unavailable: {exc}")
        if not self._destroyed:
            self._after = self.root.after(100, self._tick)
