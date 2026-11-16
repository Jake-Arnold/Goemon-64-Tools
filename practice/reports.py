"""Portable, evidence-labelled reports for USA and Japanese research."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
import uuid
from zipfile import ZipFile, ZIP_DEFLATED

SCHEMA = "goemon-discovery-report-v1"
REGIONS = {"usa": "USA", "japan": "JP"}
EXPORT_FILES = ("manifest.json", "summary.md", "session.json",
                "candidates.csv", "accesses.csv")


@dataclass(frozen=True)
class ReportEntry:
    path: Path
    title: str
    region: str
    created: str
    kind: str
    legacy: bool = False


def documents_dir(*, platform_name=None, home=None, environ=None):
    platform_name = sys.platform if platform_name is None else platform_name
    env = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    if platform_name == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as key:
                raw, _ = winreg.QueryValueEx(key, "Personal")
            expanded = os.path.expandvars(raw)
            if expanded and "%" not in expanded:
                return Path(expanded).expanduser()
        except (ImportError, OSError, ValueError):
            pass
        return Path(env.get("USERPROFILE") or home) / "Documents"
    raw = env.get("XDG_DOCUMENTS_DIR", "")
    if not raw:
        try:
            cfg = (home / ".config" / "user-dirs.dirs").read_text(encoding="utf-8")
            match = re.search(r'^XDG_DOCUMENTS_DIR="([^"]+)"', cfg, re.M)
            raw = match.group(1) if match else ""
        except OSError:
            pass
    if raw:
        path = raw.replace("$HOME", str(home)).replace(chr(36) + "{HOME}", str(home))
        candidate = Path(path).expanduser()
        if candidate.is_absolute():
            return candidate
    return home / "Documents"


def reports_root():
    override = os.environ.get("GOEMON_REPORTS_DIR")
    return (Path(override).expanduser() if override else
            documents_dir() / "Goemon Practice Toolkit" / "Reports")


def safe_slug(value):
    label = unicodedata.normalize("NFKD", str(value))
    ascii_label = label.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_label).strip("-")[:64].rstrip("-") or "research"


def create_value_search_report(*, region, title, rows, total_count,
                               value_type, sample_count, timestamp=None,
                               root=None):
    if region not in REGIONS:
        raise ValueError("A report must belong to USA or Japan")
    if not isinstance(rows, (list, tuple)) or not 0 <= len(rows) <= total_count:
        raise ValueError("Invalid result list or candidate count")
    when = timestamp or datetime.now(timezone.utc)
    if when.tzinfo is None:
        raise ValueError("Report timestamp must include a timezone")
    when = when.astimezone(timezone.utc)
    stamp = when.strftime("%Y-%m-%d_%H%M%SZ")
    base = (Path(root) if root is not None else reports_root()) / REGIONS[region]
    base.mkdir(parents=True, exist_ok=True)
    for _ in range(12):
        folder = base / (stamp + "__" + safe_slug(title) +
                         "__" + uuid.uuid4().hex[:8])
        try:
            folder.mkdir()
            break
        except FileExistsError:
            continue
    else:
        raise RuntimeError("Could not allocate a unique report directory")
    manifest = {
        "schema": SCHEMA, "kind": "value-search",
        "title": title.strip() or "Value search",
        "region": REGIONS[region],
        "created_utc": when.isoformat().replace("+00:00", "Z"),
        "candidate_total": total_count,
        "candidate_exported": len(rows),
        "candidate_truncated": len(rows) < total_count,
        "value_type": value_type, "snapshots": sample_count,
        "instruction_access_tracing": False,
        "evidence": "memory-snapshot-only",
    }
    notes = [
        "# " + manifest["title"], "",
        "**Region:** " + manifest["region"],
        "**Date (UTC):** " + manifest["created_utc"],
        "**Value type:** " + value_type,
        "**Snapshots:** " + str(sample_count),
        "**Total candidates:** " + str(total_count),
        "**Exported rows:** " + str(len(rows)), "",
        "Read-only game RAM value search. These are unverified candidate"
        " addresses. No original MIPS instruction reads/writes were traced.",
    ]
    if manifest["candidate_truncated"]:
        notes += ["", "**Coverage warning:** Only the displayed candidate"
                  " rows are exported. Narrow the search for a complete list."]
    notes += ["", "## Candidate preview", "",
              "| Address | Type | Value | Raw hex |",
              "| --- | --- | --- | --- |"]
    for row in rows[:50]:
        columns = [str(row.get(key, "")).replace("|", r"\|").replace("\n", " ")
                   for key in ("address", "kind", "value", "hex")]
        notes.append("| " + " | ".join(columns) + " |")
    if len(rows) > 50:
        notes += ["", "Additional exported rows are in candidates.csv."]
    with (folder / "candidates.csv").open("w", encoding="utf-8",
                                           newline="") as output:
        writer = csv.DictWriter(
            output, fieldnames=("address", "kind", "value", "hex"),
            extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})
    (folder / "session.json").write_text(
        json.dumps({"manifest": manifest, "candidates": list(rows)},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "summary.md").write_text("\n".join(notes) + "\n",
                                       encoding="utf-8")
    # The manifest is written last; partial reports are excluded from the index.
    (folder / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return folder


def list_reports(*, root=None, legacy_dir=None):
    root = Path(root) if root is not None else reports_root()
    items = []
    for region in ("USA", "JP"):
        parent = root / region
        if not parent.is_dir():
            continue
        for folder in parent.iterdir():
            if not folder.is_dir():
                continue
            try:
                meta = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
                if meta.get("schema") != SCHEMA or meta.get("region") != region:
                    continue
                items.append(ReportEntry(
                    folder, meta.get("title") or folder.name, region,
                    meta.get("created_utc", ""), meta.get("kind", "research")))
            except (OSError, ValueError, TypeError):
                continue
    if legacy_dir is None:
        from practice.paths import practice_data_dir
        legacy_dir = practice_data_dir() / "diagnostics"
    legacy = Path(legacy_dir)
    if legacy.is_dir():
        for file in legacy.glob("*.json"):
            if file.is_file():
                stamp = datetime.fromtimestamp(
                    file.stat().st_mtime, timezone.utc).isoformat()
                items.append(ReportEntry(
                    file, file.stem.replace("_", " "), "Legacy",
                    stamp, "legacy-json", True))
    return sorted(items, key=lambda item: item.created, reverse=True)


def export_report_zip(folder):
    folder = Path(folder)
    if not folder.is_dir() or not (folder / "manifest.json").is_file():
        raise ValueError("Select a completed research report")
    archive = folder.with_suffix(".zip")
    with ZipFile(archive, "w", ZIP_DEFLATED) as output:
        for name in EXPORT_FILES:
            path = folder / name
            if path.is_file():
                output.write(path, arcname=folder.name + "/" + name)
    return archive


def open_in_file_manager(path):
    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(str(path))
    if sys.platform == "win32":
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif sys.platform.startswith("linux"):
        subprocess.Popen(["xdg-open", str(path)], start_new_session=True)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)], start_new_session=True)
    else:
        raise OSError("Unsupported desktop file opener")
