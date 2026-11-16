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
    candidate_total: int | None = None


def documents_dir(*, platform_name=None, home=None, environ=None):
    custom_location = home is not None or environ is not None
    platform_name = sys.platform if platform_name is None else platform_name
    env = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    if platform_name == "win32" and not custom_location:
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
    if platform_name == "win32":
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



def working_investigations_dir(region):
    """Private, resumable A/B/C working data; not an exported report."""
    if region not in REGIONS:
        raise ValueError("Unknown investigation region")
    return reports_root() / ".working" / REGIONS[region]


def safe_slug(value):
    label = unicodedata.normalize("NFKD", str(value))
    ascii_label = label.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_label).strip("-")[:64].rstrip("-") or "research"



def readable_report_name(title):
    """Keep an experiment recognisable in GNOME Files and Windows Explorer."""
    name = unicodedata.normalize("NFC", str(title or ""))
    # Windows-reserved characters and control bytes must never enter a path.
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " - ", name)
    name = re.sub(r"\s+", " ", name).strip(" .-")
    name = re.sub(r"(?:\s*-\s*){2,}", " - ", name)
    name = name[:64].rstrip(" .-") or "Untitled investigation"
    if re.fullmatch(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])", name):
        name = "Report - " + name
    return name


def _run_stamp(when):
    return when.strftime("%Y-%m-%d %H-%M-%S UTC")


def _create_run_folder(parent, when):
    """A timestamp is a subfolder, not part of the experiment's label."""
    base_name = _run_stamp(when)
    for suffix in range(1, 1000):
        name = base_name if suffix == 1 else f"{base_name} ({suffix})"
        folder = parent / name
        try:
            folder.mkdir()
            return folder
        except FileExistsError:
            continue
    raise RuntimeError("No unused report run folder could be allocated")

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
    base = (Path(root) if root is not None else reports_root()) / REGIONS[region]
    experiment = base / readable_report_name(title)
    experiment.mkdir(parents=True, exist_ok=True)
    folder = _create_run_folder(experiment, when)
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
              "| Address | Type | Initial | Previous | Value | Raw hex |",
              "| --- | --- | --- | --- | --- | --- |"]
    for row in rows[:50]:
        columns = [str(row.get(key, "")).replace("|", r"\|").replace("\n", " ")
                   for key in ("address", "kind", "initial", "previous", "value", "hex")]
        notes.append("| " + " | ".join(columns) + " |")
    if len(rows) > 50:
        notes += ["", "Additional exported rows are in candidates.csv."]
    with (folder / "candidates.csv").open("w", encoding="utf-8",
                                           newline="") as output:
        writer = csv.DictWriter(
            output, fieldnames=("address", "kind", "initial", "previous", "value", "hex"),
            extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})
    (folder / "session.json").write_text(
        json.dumps({"manifest": manifest, "candidates": list(rows),
                    "evidence": {"value_type": value_type, "snapshots": sample_count}},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "summary.md").write_text("\n".join(notes) + "\n",
                                       encoding="utf-8")
    # The manifest is written last; partial reports are excluded from the index.
    (folder / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return folder



DISCOVERY_KINDS = {
    "value-search": "Value search",
    "memory-comparison": "Memory changes",
    "flag-investigation": "Repeated flag changes",
    "damage-events": "Automatic damage recording",
}


def create_discovery_report(*, region, title, kind, candidates, evidence,
                            candidate_total=None, metadata=None, notes=(),
                            root=None, timestamp=None):
    """Write the same four portable files for every research workflow.

    session.json contains the complete *available* structured evidence.
    candidates.csv contains every supplied candidate, not just a table preview.
    Guest-memory dumps are intentionally not duplicated into exported files.
    """
    if region not in REGIONS or kind not in DISCOVERY_KINDS:
        raise ValueError("Unknown game region or discovery report type")
    if not isinstance(candidates, (list, tuple)) or not isinstance(evidence, dict):
        raise ValueError("Candidates must be a list and evidence must be a mapping")
    total = len(candidates) if candidate_total is None else candidate_total
    if type(total) is not int or total < len(candidates):
        raise ValueError("Total candidates cannot be smaller than exported rows")
    title = str(title or "").strip() or DISCOVERY_KINDS[kind]
    when = timestamp or datetime.now(timezone.utc)
    if when.tzinfo is None:
        raise ValueError("Report timestamp must have a timezone")
    when = when.astimezone(timezone.utc)
    meta = dict(metadata or {})
    # Confirm serialisability *before* creating report folders.
    fields = sorted({key for row in candidates for key in row})
    preferred = ("address", "kind", "type", "region", "before", "after",
                 "initial", "previous", "value", "mask", "direction",
                 "score", "hits", "returns", "support", "hex")
    fields = [key for key in preferred if key in fields] + [
        key for key in fields if key not in preferred]
    if not fields:
        fields = ["address", "kind"]
    manifest = {
        "schema": SCHEMA,
        "kind": kind,
        "title": title,
        "region": REGIONS[region],
        "created_utc": when.isoformat().replace("+00:00", "Z"),
        "candidate_total": total,
        "candidate_exported": len(candidates),
        "candidate_truncated": total > len(candidates),
        "instruction_access_tracing": False,
        "evidence": "game-memory-observations-only",
        "metadata": meta,
        "notes": list(notes),
        "files": ["summary.md", "candidates.csv", "session.json", "manifest.json"],
    }
    document = {"manifest": manifest, "candidates": list(candidates),
                "evidence": evidence}
    serialised = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    title_md = title.replace("\n", " ").replace("\r", " ")
    lines = [
        f"# {title_md}", "",
        f"**Research method:** {DISCOVERY_KINDS[kind]}",
        f"**Region:** {REGIONS[region]}",
        f"**Date (UTC):** {manifest['created_utc']}",
        f"**Candidate addresses/entries:** {total:,}",
        f"**Candidates exported:** {len(candidates):,}", "",
        "The report records memory observations, not original MIPS "
        "instruction-access traces. Candidate field meanings and "
        "write safety are unverified.", ""
    ]
    if total > len(candidates):
        lines += [f"**Coverage limitation:** {total - len(candidates):,} "
                  "candidates were omitted by the underlying analyzer's "
                  "result limit.", ""]
    if meta:
        lines += ["## Investigation details", ""]
        for key, value in meta.items():
            rendered = (json.dumps(value, ensure_ascii=False)
                        if isinstance(value, (dict, list)) else str(value))
            lines.append(f"- **{key.replace('_', ' ').capitalize()}:** {rendered}")
        lines.append("")
    if notes:
        lines += ["## Evidence limitations", ""]
        lines += [f"- {str(note)}" for note in notes]
        lines.append("")
    lines += ["## Candidate preview", "",
              "| " + " | ".join(fields[:8]) + " |",
              "| " + " | ".join(["---"] * min(len(fields), 8)) + " |"]
    for row in candidates[:50]:
        def cell(value):
            value = (json.dumps(value, ensure_ascii=False)
                     if isinstance(value, (dict, list)) else str(value))
            return value.replace("|", r"\|").replace("\n", " ")
        lines.append("| " + " | ".join(cell(row.get(k, "")) for k in fields[:8]) + " |")
    if len(candidates) > 50:
        lines += ["", f"The remaining {len(candidates)-50:,} exported candidates "
                  "are in candidates.csv and session.json."]
    region_root = (Path(root) if root is not None else reports_root()) / REGIONS[region]
    experiment = region_root / readable_report_name(title)
    experiment.mkdir(parents=True, exist_ok=True)
    folder = _create_run_folder(experiment, when)
    try:
        with (folder / "candidates.csv").open("w", newline="",
                                              encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields,
                                    extrasaction="ignore")
            writer.writeheader()
            for row in candidates:
                writer.writerow({
                    k: json.dumps(row.get(k), ensure_ascii=False)
                       if isinstance(row.get(k), (dict, list))
                       else row.get(k, "")
                    for k in fields
                })
        (folder / "session.json").write_text(serialised, encoding="utf-8")
        (folder / "summary.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8")
        (folder / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
    except Exception:
        # The manifest is always committed last: a partial report won't index.
        (folder / "manifest.json").unlink(missing_ok=True)
        raise
    return folder


def list_reports(*, root=None, legacy_dir=None):
    root = Path(root) if root is not None else reports_root()
    items = []
    for region in ("USA", "JP"):
        parent = root / region
        if not parent.is_dir():
            continue
        for entry in parent.iterdir():
            if not entry.is_dir() or entry.is_symlink():
                continue
            # Both v0.11.32 flat timestamp folders and readable experiment/run
            # subfolders are indexed. Existing report paths are never moved.
            run_folders = ([entry] if (entry / "manifest.json").is_file()
                           else (child for child in entry.iterdir()
                                 if child.is_dir() and not child.is_symlink()))
            for folder in run_folders:
                try:
                    meta = json.loads((folder / "manifest.json").read_text(
                        encoding="utf-8"))
                    if meta.get("schema") != SCHEMA or meta.get("region") != region:
                        continue
                    items.append(ReportEntry(
                        folder, meta.get("title") or entry.name, region,
                        meta.get("created_utc", ""), meta.get("kind", "research"),
                        candidate_total=meta.get("candidate_total")))
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



def organise_report_folder(folder, *, root=None):
    """Explicitly rename a v0.11.32 flat folder without rewriting its files.

    This operation moves an existing report; callers must obtain user consent.
    Files outside the configured reports root are not accepted.
    """
    folder = Path(folder)
    base = Path(root) if root is not None else reports_root()
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Select a completed, non-symlink report folder")
    manifest_path = folder / "manifest.json"
    try:
        meta = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError("The selected folder has no valid report manifest") from exc
    region = meta.get("region")
    if meta.get("schema") != SCHEMA or region not in ("USA", "JP"):
        raise ValueError("The selected report has an unsupported manifest")
    region_dir = (base / region).resolve()
    # Already in the new two-level structure? Keep the location unchanged.
    if folder.resolve().parent.parent == region_dir:
        return folder
    if folder.resolve().parent != region_dir:
        raise ValueError("The selected report is outside its region directory")
    created = meta.get("created_utc", "")
    try:
        when = datetime.fromisoformat(created.replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise ValueError("Timezone missing")
        when = when.astimezone(timezone.utc)
    except (TypeError, AttributeError, ValueError) as exc:
        raise ValueError("The report does not have a valid UTC timestamp") from exc
    experiment = base / region / readable_report_name(meta.get("title"))
    experiment.mkdir(parents=True, exist_ok=True)
    stem = _run_stamp(when)
    for counter in range(1, 1000):
        name = stem if counter == 1 else f"{stem} ({counter})"
        target = experiment / name
        if target.exists():
            continue
        folder.rename(target)
        return target
    raise RuntimeError("No unused name for the selected report")

def export_report_zip(folder):
    folder = Path(folder)
    if not folder.is_dir() or not (folder / "manifest.json").is_file():
        raise ValueError("Select a completed research report")
    try:
        info = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        title = readable_report_name(info.get("title") or "Investigation")
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError("Invalid report manifest") from exc
    # Export names remain meaningful outside the experiment directory.
    archive = folder.parent / f"{title} - {folder.name}.zip"
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
