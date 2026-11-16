"""Report library, file-manager shortcuts and portable export."""
from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from practice.reports import (
    list_reports, reports_root, export_report_zip, open_in_file_manager,
    organise_report_folder,
)


class ReportsMixin:
    def build_reports_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text="Reports")
        self.reports_tab = tab
        ttk.Label(tab, text="Research reports",
                  font=("Segoe UI Semibold", 16)).pack(anchor="w", pady=(0, 5))
        ttk.Label(
            tab, text="Completed USA and Japanese investigations, with"
            " direct access to your Documents folder. Older diagnostic JSON"
            " files are listed without moving or deleting them.",
            wraplength=1060).pack(anchor="w", pady=(0, 9))
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", pady=(0, 7))
        for caption, action in (
            ("Refresh", self.refresh_reports),
            ("Open report", self.open_selected_report),
            ("Open containing folder", self.open_selected_report_folder),
            ("Open Reports Folder", self.open_reports_folder),
            ("Copy path", self.copy_selected_report_path),
            ("Tidy folder name", self.organise_selected_report),
            ("Export ZIP", self.zip_selected_report),
        ):
            ttk.Button(toolbar, text=caption, command=action).pack(
                side="left", padx=(0, 7))
        self.report_status = tk.StringVar(value="Reports are ready.")
        ttk.Label(tab, textvariable=self.report_status,
                  wraplength=1060).pack(anchor="w", pady=(0, 7))
        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame,
                            columns=("region", "created", "kind", "candidates"),
                            show="tree headings", selectmode="browse", height=18)
        for column, caption, width in (
            ("#0", "Experiment name", 440),
            ("region", "Region", 85),
            ("created", "Created (UTC)", 165),
            ("kind", "Research type", 145),
            ("candidates", "Candidates", 115),
        ):
            tree.heading(column, text=caption)
            tree.column(column, width=width,
                        stretch=column == "#0")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        tree.bind("<Double-1>", lambda _event: self.open_selected_report())
        tree.bind("<<TreeviewSelect>>", self._on_report_selected)
        self.reports_tree = tree
        self.report_detail = tk.StringVar(value="Select a report to see its location.")
        ttk.Label(tab, textvariable=self.report_detail, wraplength=1050).pack(
            anchor="w", pady=(8, 0))
        self._reports_rows = ()
        self.refresh_reports()

    def refresh_reports(self, select_path=None):
        try:
            items = list_reports()
            self._reports_rows = items
            self.reports_tree.delete(*self.reports_tree.get_children())
            for idx, item in enumerate(items):
                kind_name = {
                    "value-search": "Value search",
                    "legacy-json": "Legacy JSON",
                }.get(item.kind, item.kind.replace("-", " ").title())
                self.reports_tree.insert(
                    "", "end", iid=str(idx), text=item.title,
                    values=(item.region,
                            item.created[:16].replace("T", " "),
                            kind_name,
                            item.candidate_total if item.candidate_total is not None else "—"))
                if select_path and item.path == Path(select_path):
                    self.reports_tree.selection_set(str(idx))
                    self.reports_tree.see(str(idx))
            self.report_status.set(
                f"{len(items)} saved report(s). Double-click to open; "
                "use Open Reports Folder to browse files.")
            self._on_report_selected()
        except (OSError, ValueError) as exc:
            self.report_status.set(f"Unable to list reports: {exc}")

    def _on_report_selected(self, _event=None):
        selected = self.reports_tree.selection()
        if selected:
            item = self._reports_rows[int(selected[0])]
            self.report_detail.set(f"Selected folder: {item.path}")
        else:
            self.report_detail.set("Select a report to see its location.")

    def _selected_report(self):
        selected = self.reports_tree.selection()
        if not selected:
            raise ValueError("Select a report first")
        return self._reports_rows[int(selected[0])]

    def _report_action(self, callback):
        try:
            result = callback()
            if result is not None:
                self.report_status.set(str(result))
        except (OSError, ValueError, IndexError) as exc:
            self.report_status.set(f"Report action failed: {exc}")

    def open_reports_folder(self):
        def action():
            root = reports_root()
            root.mkdir(parents=True, exist_ok=True)
            open_in_file_manager(root)
            return "Opened the Reports folder."
        self._report_action(action)

    def open_selected_report(self):
        def action():
            item = self._selected_report()
            target = item.path if item.legacy else item.path / "summary.md"
            open_in_file_manager(target)
            return f"Opened report: {item.title}"
        self._report_action(action)

    def open_selected_report_folder(self):
        def action():
            item = self._selected_report()
            target = item.path.parent if item.legacy else item.path
            open_in_file_manager(target)
            return f"Opened folder for: {item.title}"
        self._report_action(action)

    def copy_selected_report_path(self):
        def action():
            item = self._selected_report()
            self.root.clipboard_clear()
            self.root.clipboard_append(str(item.path))
            return f"Copied the path for: {item.title}"
        self._report_action(action)


    def organise_selected_report(self):
        """Offer a reversible-looking but path-changing operation explicitly."""
        def action():
            item = self._selected_report()
            if item.legacy:
                raise ValueError("Historical diagnostic JSON stays in its original location")
            if item.path.parent.name in ("USA", "JP"):
                confirmed = messagebox.askyesno(
                    "Use readable report folders?",
                    "Move this report into a folder named after its experiment? "
                    "Its contents will be preserved, but existing links to "
                    "the old folder path will need updating.",
                    parent=self.root)
                if not confirmed:
                    return None
            target = organise_report_folder(item.path)
            self.refresh_reports(select_path=target)
            return ("Folder is already organised." if target == item.path else
                    f"Organised: {item.title}")
        self._report_action(action)

    def zip_selected_report(self):
        def action():
            item = self._selected_report()
            if item.legacy:
                raise ValueError("Legacy reports are already individual JSON files")
            export_report_zip(item.path)
            return f"Exported ZIP for: {item.title}"
        self._report_action(action)
