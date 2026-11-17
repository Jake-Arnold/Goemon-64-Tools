"""Restricted, metadata-only upstream address discovery refresh.

Fetches one canonical GitHub JSON path, with a strict byte limit, strict
schema, no script execution and no write permissions. Invalid remote data
never replaces the last known-good cache or the bundled catalogue.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

from practice.address_catalogue import (
    DISCOVERY_FORMAT, MAX_ENTRIES, _entry, validate_entry,
    validate_catalogue, search_entries,
)
from practice.paths import practice_data_dir


OFFICIAL_HOST = "https://raw.githubusercontent.com/Jake-Arnold/Goemon-64-Tools"
OFFICIAL_PATH = "practice/data/address_discoveries_v1.json"
REMOTE_MAX_BYTES = 1_500_000
CACHE_FILE = practice_data_dir() / "address_catalogue_remote.json"
ALLOWED_BRANCH = re.compile(r"(?:main|toolkit/[0-9A-Za-z_.-]+(?:/[0-9A-Za-z_.-]+)*)\Z")


def remote_url(branch="main"):
    if not ALLOWED_BRANCH.fullmatch(branch):
        raise ValueError("Invalid official branch")
    # Branch names are allowlisted and all path components are literal.
    return f"{OFFICIAL_HOST}/{branch}/{OFFICIAL_PATH}"


def validate_discoveries(doc):
    """Reject unbounded/untyped records before trusting downloaded metadata."""
    if (not isinstance(doc, dict) or
            doc.get("format") != DISCOVERY_FORMAT or
            not isinstance(doc.get("entries"), list) or
            len(doc["entries"]) > MAX_ENTRIES):
        raise ValueError("Invalid discovery manifest format")
    unique = set()
    for entry in doc["entries"]:
        if not isinstance(entry, dict):
            raise ValueError("Discovery record must be an object")
        for key in ("id", "name", "region", "address", "category",
                    "confidence", "source"):
            if not isinstance(entry.get(key), str) or not entry[key]:
                raise ValueError(f"Discovery record missing {key}")
        if entry["id"] in unique:
            raise ValueError("Duplicate discovery ID")
        unique.add(entry["id"])
        if entry["region"] not in ("usa", "japan", "unknown"):
            raise ValueError("Invalid discovery region")
        if not re.fullmatch(r"0x[0-9A-Fa-f]{8}", entry["address"]):
            raise ValueError("Invalid discovery address")
        dtype = entry.get("data_type")
        if dtype is not None and dtype not in (
                "u8", "s8", "u16", "s16", "u32", "s32", "f32", "f64", "hex8"):
            raise ValueError("Unsupported discovered decoder")
        if entry.get("live_readable", False) and (
                entry["region"] == "unknown" or
                entry["category"] in ("code_vma", "overlay_patch",
                                      "research_reference", "rom_offset",
                                      "external_cheat_lead")):
            raise ValueError("Unsafe downloaded live-read capability")
        normalized = discovery_to_record(entry)
        validate_entry(normalized)
    return doc


def discovery_to_record(entry):
    mask = entry.get("mask")
    if mask:
        mask = int(mask, 16)
    record = _entry(
        entry["id"], entry["name"], entry["address"], entry["region"],
        entry["category"], entry.get("data_type"),
        width=entry.get("width"), mask=mask,
        confidence=entry["confidence"], evidence=entry.get("evidence", ""),
        source=entry["source"], counterpart=entry.get("counterpart"),
        context=entry.get("context", ""), owner=entry.get("owner", ""),
        control=entry.get("control"), live=entry.get("live_readable", False),
        source_revision=entry.get("source_revision", ""),
        discovered=entry.get("discovered"), updated=entry.get("updated"))
    record["mips_refs"] = entry.get("mips_refs", [])
    return record


def merge_remote_catalogue(local, remote):
    """Overlay descriptors by stable ID. A remotely supplied control cannot
    authorize an edit: only built-in, already-known control mappings are used.
    """
    validate_catalogue(local)
    validate_discoveries(remote)
    records = {entry["id"]: dict(entry) for entry in local["entries"]}
    added = updated = 0
    for item in remote["entries"]:
        row = discovery_to_record(item)
        row["control"] = records.get(row["id"], {}).get("control")
        if row["id"] not in records:
            added += 1
        elif row != records[row["id"]]:
            updated += 1
        records[row["id"]] = row
    merged = dict(local)
    merged["entries"] = sorted(records.values(), key=lambda x: (
        x["region"], x["address"], x["id"]))
    validate_catalogue(merged)
    return merged, {"added": added, "updated": updated,
                    "disputed": sum(
                        r["confidence"] in ("disputed", "conflict")
                        for r in merged["entries"])}


def load_cached_discoveries(path=CACHE_FILE):
    try:
        blob = Path(path).read_bytes()
        if len(blob) > REMOTE_MAX_BYTES:
            raise ValueError("Oversized cache")
        document = json.loads(blob)
        return validate_discoveries(document)
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError):
        return None


def refresh_address_discoveries(*, branch="main", opener=None,
                                cache_path=CACHE_FILE):
    """Network IO only. Call on a worker, never in Tk's main callback.

    Caches the last valid document atomically. Does not contact arbitrary
    URLs and does not follow redirects to another host.
    """
    url = remote_url(branch)
    request = urllib.request.Request(
        url, headers={"User-Agent": "Goemon-Metadata-ReadOnly/1",
                      "Accept": "application/json"})
    if opener is None:
        opener = urllib.request.urlopen
    response = opener(request, timeout=12)
    try:
        final_url = response.geturl()
        if final_url != url:
            raise ValueError("Unexpected metadata redirect")
        blob = response.read(REMOTE_MAX_BYTES + 1)
    finally:
        response.close()
    if len(blob) > REMOTE_MAX_BYTES:
        raise ValueError("Remote metadata exceeds 1.5 MB")
    document = json.loads(blob.decode("utf-8"))
    validate_discoveries(document)
    cache = Path(cache_path)
    cache.parent.mkdir(parents=True, exist_ok=True)
    temp = cache.with_name(cache.name + ".tmp")
    temp.write_bytes(blob)
    temp.replace(cache)
    return document, {
        "version": document.get("version", 1),
        "last_sync": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "upstream_revision": hashlib.sha256(blob).hexdigest()[:12],
        "source_branch": branch,
    }
