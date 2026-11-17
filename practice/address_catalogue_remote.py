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
    CATALOGUE_FORMAT, DISCOVERY_FORMAT, MAX_ENTRIES, MAX_SERIALIZED,
    _entry, validate_entry, validate_catalogue, search_entries, consolidate_entries,
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
    merged["entries"] = consolidate_entries(records.values())
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


# Canonical full-registry refresh, independent of toolkit software updates.
# Retain the older discovery-manifest reader for legacy caches/agent tools.
CANONICAL_PATH = "practice/data/address_catalogue_v1.json"
CATALOGUE_CACHE_FILE = practice_data_dir() / "address_catalogue_full_cache.json"
CATALOGUE_CACHE_INFO = practice_data_dir() / "address_catalogue_sync_info.json"
CANONICAL_MAX_BYTES = 5_000_000


def canonical_url(branch="main"):
    if not ALLOWED_BRANCH.fullmatch(branch):
        raise ValueError("Invalid official registry branch")
    return f"{OFFICIAL_HOST}/{branch}/{CANONICAL_PATH}"


def load_cached_catalogue(path=CATALOGUE_CACHE_FILE):
    try:
        file = Path(path)
        if file.stat().st_size > CANONICAL_MAX_BYTES:
            raise ValueError("Oversized registry cache")
        return validate_catalogue(json.loads(file.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError, UnicodeError, json.JSONDecodeError):
        return None


def load_catalogue_cache_info(path=CATALOGUE_CACHE_INFO):
    try:
        info = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(info, dict):
            return {}
        return {
            k: info[k] for k in (
                "version", "last_sync", "upstream_revision", "source_branch",
                "added", "updated", "disputed")
            if k in info and isinstance(info[k], (str, int))
        }
    except (OSError, ValueError, TypeError, UnicodeError):
        return {}


def merge_remote_metadata(local, remote):
    """Catalogue contains reference data, not runtime address permissions.

    Existing toolkit editor mappings are preserved from the *bundled* trusted
    registry. Remote description/evidence may change; entirely new records are
    visible and optionally readable if the validated decoder supports them.
    """
    validate_catalogue(local)
    validate_catalogue(remote)
    records = {r["id"]: dict(r) for r in local["entries"]}
    added = updated = 0
    IMMUTABLE = (
        "address", "region", "revision", "width", "mask", "data_type",
        "signed", "endian", "category", "control", "live_readable",
        "counterpart")
    for entry in remote["entries"]:
        item = dict(entry)
        current = records.get(item["id"])
        if current is None:
            # A remote entry can reference a *built-in* control name but must
            # not acquire that binding. All user actions remain explicit.
            item["control"] = None
            records[item["id"]] = item
            added += 1
        else:
            for key in IMMUTABLE:
                item[key] = current.get(key)
            if item != current:
                updated += 1
            records[item["id"]] = item
    merged = dict(local)
    merged["entries"] = sorted(
        records.values(), key=lambda x: (
            x["region"], x["address"], x.get("mask") or "", x["id"]))
    merged["sources"] = sorted(set(
        s for row in merged["entries"] for s in row["sources"]))
    merged["version"] = max(
        local.get("version", 1), remote.get("version", 1))
    validate_catalogue(merged)
    return merged, {
        "added": added, "updated": updated,
        "disputed": sum(
            row["confidence"] in ("disputed", "conflict")
            for row in merged["entries"])
    }


def refresh_canonical_catalogue(*, branch="main", opener=None,
                                cache_path=CATALOGUE_CACHE_FILE,
                                info_path=CATALOGUE_CACHE_INFO):
    """Nonblocking caller contract; performs only one official, bounded GET."""
    url = canonical_url(branch)
    request = urllib.request.Request(
        url, headers={"User-Agent": "Goemon-AddressRegistry-ReadOnly/1",
                      "Accept": "application/json"})
    if opener is None:
        opener = urllib.request.urlopen
    response = opener(request, timeout=15)
    try:
        if response.geturl() != url:
            raise ValueError("Unexpected registry redirect")
        blob = response.read(CANONICAL_MAX_BYTES + 1)
    finally:
        response.close()
    if len(blob) > CANONICAL_MAX_BYTES:
        raise ValueError("Remote registry exceeds metadata size limit")
    remote = validate_catalogue(json.loads(blob.decode("utf-8")))
    info = {
        "version": remote.get("version", 1),
        "last_sync": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "upstream_revision": hashlib.sha256(blob).hexdigest()[:12],
        "source_branch": branch,
    }
    cache = Path(cache_path)
    cache.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache.with_name(cache.name + ".tmp")
    temporary.write_bytes(blob)
    temporary.replace(cache)
    metadata = Path(info_path)
    metadata.parent.mkdir(parents=True, exist_ok=True)
    temporary_info = metadata.with_name(metadata.name + ".tmp")
    temporary_info.write_text(
        json.dumps(info, indent=2) + "\n", encoding="utf-8")
    temporary_info.replace(metadata)
    return remote, info
