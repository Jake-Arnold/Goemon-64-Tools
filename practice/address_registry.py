"""Runtime authority for all known Goemon game addresses and bit masks.

This module only reads the reviewed versioned JSON registry. It never imports
the legacy discovery modules, contacts the network or opens game memory.
Importing it from Unlocks, Story Progress and Live Memory is cycle-safe.
"""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path


CATALOGUE_FILE = Path(__file__).with_name("data") / "address_catalogue_v1.json"
MAX_BYTES = 6_000_000
ADDRESS_MIN = 0x80000000
ADDRESS_MAX = 0x80800000


@lru_cache(maxsize=1)
def load_registry():
    if not CATALOGUE_FILE.is_file():
        raise RuntimeError(
            "Canonical memory-address catalogue is missing: "
            "run python -m scripts.sync_address_catalogue --write")
    if CATALOGUE_FILE.stat().st_size > MAX_BYTES:
        raise ValueError("Canonical address catalogue is too large")
    data = json.loads(CATALOGUE_FILE.read_text(encoding="utf-8"))
    if (data.get("format") != "goemon-address-catalogue-v1" or
            not isinstance(data.get("entries"), list)):
        raise ValueError("Unsupported canonical address catalogue")
    rows = {}
    by_id = {}
    for row in data["entries"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError("Invalid address catalogue record")
        key = row["id"]
        if key in by_id:
            raise ValueError(f"Duplicate authoritative field: {key}")
        if not isinstance(row.get("address"), str):
            raise ValueError(f"{key}: address missing")
        try:
            int(row["address"], 16)
        except ValueError as exc:
            raise ValueError(f"{key}: invalid address") from exc
        aliases = row.get("id_aliases", ())
        if not isinstance(aliases, list) and aliases != ():
            raise ValueError(f"{key}: invalid ID aliases")
        for alias in (key, *aliases):
            if alias in by_id:
                raise ValueError(f"Ambiguous registry field/alias: {alias}")
            by_id[alias] = row
        rows[key] = row
    if not rows:
        raise ValueError("Canonical registry contains no addresses")
    return data, by_id


def lookup(field_id):
    """Return the canonical record by stable ID, including source aliases."""
    _, by_id = load_registry()
    try:
        return by_id[field_id]
    except KeyError as exc:
        raise KeyError(f"Field not registered: {field_id}") from exc


def guest_address(field_id, *, region=None, width=None):
    """Use one source of truth for a known guest RAM address."""
    row = lookup(field_id)
    if region is not None and row.get("region") != region:
        raise ValueError(f"{field_id}: incorrect game region")
    address = int(row["address"], 16)
    if (not ADDRESS_MIN <= address < ADDRESS_MAX or
            row["category"] in (
                "code_vma", "rom_offset", "overlay_patch",
                "cheat_format", "external_cheat_lead", "research_reference")):
        raise ValueError(f"{field_id}: not a fixed guest-data location")
    if width is not None and row.get("width") != width:
        raise ValueError(f"{field_id}: unexpected read width")
    return address


def guest_bit(field_id, *, region=None):
    row = lookup(field_id)
    address = guest_address(field_id, region=region, width=1)
    mask = row.get("mask")
    if not isinstance(mask, str):
        raise ValueError(f"{field_id}: not a registered bit")
    mask = int(mask, 16)
    if mask <= 0 or mask >= 256 or mask.bit_count() != 1:
        raise ValueError(f"{field_id}: invalid single-bit flag")
    return address, mask


def registry_records():
    """Immutable caller expectation: do not mutate returned records."""
    return tuple(load_registry()[0]["entries"])


def reload_registry():
    """Explicit local refresh only, after sync/check or a toolkit update."""
    load_registry.cache_clear()
    return len(registry_records())
