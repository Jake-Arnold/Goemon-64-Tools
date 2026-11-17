"""Canonical, read-only N64 address metadata catalogue.

Reconciles typed toolkit declarations, decomp research notes and external
lead manifests. Evidence classification is *not* a write permission.
No renderer should ever use this module to call a guest-memory writer.
"""
from __future__ import annotations

from collections import Counter
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct

CATALOGUE_FORMAT = "goemon-address-catalogue-v1"
DISCOVERY_FORMAT = "goemon-address-discoveries-v1"
DATA_DIR = Path(__file__).with_name("data")
SNAPSHOT = DATA_DIR / "address_catalogue_v1.json"
DISCOVERIES = DATA_DIR / "address_discoveries_v1.json"
EXTERNAL = DATA_DIR / "usa_external_memory_leads.json"
MENTIONS = DATA_DIR / "address_research_mentions_v1.json"
SOURCE_DATE = "2026-11-17"
SHA_PATTERN = re.compile(r"^0x[0-9A-F]{8}$")
READ_KINDS = frozenset(("u8", "s8", "u16", "s16", "u32", "s32", "f32", "f64", "hex8"))
WIDTHS = {"u8": 1, "s8": 1, "u16": 2, "s16": 2,
          "u32": 4, "s32": 4, "f32": 4, "f64": 8, "hex8": 8}
REGIONS = frozenset(("usa", "japan", "unknown"))
ROM_REVISIONS = {"usa": "NG5E-0", "japan": "NG5J-0", "unknown": "unknown"}
BLOCKED_LIVE_CATEGORIES = frozenset(
    ("code_vma", "rom_offset", "overlay_patch", "external_cheat_lead",
     "research_reference", "cheat_format", "unknown"))
MAX_ENTRIES = 15000
MAX_SERIALIZED = 5_000_000


def hexaddr(address):
    return f"0x{address:08X}" if isinstance(address, int) else "0x" + str(address).replace("0X", "0x").removeprefix("0x").upper()


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:76]


def _entry(key, name, address, region, category, data_type=None, *,
           mask=None, confidence="unknown", evidence="", source="",
           counterpart=None, context="", control=None, owner="", reader=None,
           writer=None, aliases=(), width=None, live=None, source_revision="",
           discovered=None, updated=None):
    address = hexaddr(address)
    valid_guest = bool(re.fullmatch(r"0x[0-9A-F]{8}", address)) and (
        0x80000000 <= int(address, 16) < 0x80800000)
    width = width if width is not None else WIDTHS.get(data_type)
    if live is None:
        live = (valid_guest and data_type in READ_KINDS and
                category not in BLOCKED_LIVE_CATEGORIES)
    return {
        "id": str(key), "name": str(name), "address": address,
        "region": region, "revision": ROM_REVISIONS[region],
        "category": category, "data_type": data_type, "width": width,
        "signed": None if data_type is None else data_type.startswith("s"),
        "endian": "big" if data_type in READ_KINDS else None,
        "mask": None if mask is None else f"0x{mask:X}",
        "counterpart": None if counterpart is None else hexaddr(counterpart),
        "confidence": str(confidence), "evidence": str(evidence),
        "sources": [str(source)] if source else [],
        "context": str(context), "mips_refs": [reader, writer]
        if reader or writer else [],
        "live_readable": bool(live), "control": control,
        "owner": owner or category, "aliases": list(aliases),
        "discovered": discovered, "updated": updated or SOURCE_DATE,
        "source_revision": source_revision or "toolkit declarations",
    }


def validate_entry(record):
    if not isinstance(record, dict):
        raise ValueError("Catalogue entry must be an object")
    for required in ("id", "name", "address", "region", "category",
                     "confidence", "sources", "live_readable"):
        if required not in record:
            raise ValueError(f"Address entry missing {required}")
    if not isinstance(record["id"], str) or not (0 < len(record["id"]) <= 180):
        raise ValueError("Invalid address ID")
    if not isinstance(record["name"], str) or not (0 < len(record["name"]) <= 300):
        raise ValueError(f"{record['id']}: invalid name")
    if record["region"] not in REGIONS:
        raise ValueError(f"{record['id']}: invalid region")
    address = record["address"]
    if not isinstance(address, str) or not SHA_PATTERN.fullmatch(address):
        raise ValueError(f"{record['id']}: invalid 8-digit address")
    width = record.get("width")
    if width is not None and (type(width) is not int or width not in (1, 2, 4, 8)):
        raise ValueError(f"{record['id']}: invalid width")
    if record.get("data_type") is not None and record["data_type"] not in READ_KINDS:
        raise ValueError(f"{record['id']}: unsupported decoder type")
    if record.get("data_type") in READ_KINDS and width != WIDTHS[record["data_type"]]:
        raise ValueError(f"{record['id']}: decoder width mismatch")
    mask = record.get("mask")
    if mask is not None:
        if not isinstance(mask, str) or not re.fullmatch(r"0x[0-9A-Fa-f]+", mask):
            raise ValueError(f"{record['id']}: invalid mask")
        if width is None or int(mask, 16) < 1 or int(mask, 16) >= (1 << (8 * width)):
            raise ValueError(f"{record['id']}: mask outside field width")
    if type(record["live_readable"]) is not bool:
        raise ValueError(f"{record['id']}: live_readable must be a boolean")
    if record["live_readable"]:
        if (width is None or
                not 0x80000000 <= int(address, 16) < 0x80800000 or
                int(address, 16) + width > 0x80800000 or
                record.get("data_type") not in READ_KINDS or
                record["category"] in BLOCKED_LIVE_CATEGORIES or
                record["region"] == "unknown"):
            raise ValueError(f"{record['id']}: unsafe live-read declaration")
    if (not isinstance(record["sources"], list) or
            not all(isinstance(s, str) for s in record["sources"])):
        raise ValueError(f"{record['id']}: invalid provenance")
    return record


def validate_catalogue(payload):
    if (not isinstance(payload, dict) or
            payload.get("format") != CATALOGUE_FORMAT or
            not isinstance(payload.get("entries"), list) or
            len(payload["entries"]) > MAX_ENTRIES):
        raise ValueError("Unsupported or oversized catalogue version")
    ids = set()
    for row in payload["entries"]:
        validate_entry(row)
        if row["id"] in ids:
            raise ValueError(f"Duplicate catalogue ID: {row['id']}")
        ids.add(row["id"])
    return payload


def _read_json(path, max_bytes=MAX_SERIALIZED):
    if path.stat().st_size > max_bytes:
        raise ValueError(f"Oversized address metadata: {path.name}")
    return json.loads(path.read_text(encoding="utf-8"))



def consolidate_entries(records):
    """One display/runtime record per actual typed guest location and bit.

    Identical physical fields from the ROM crosswalk, Story Progress and
    inspector are the *same field*, not separate evidence rows. Keep every
    stable source ID as an alias so no existing control loses its lookup.
    Differently masked bits in the same byte stay independent. Untyped and
    non-game-memory research references do not merge speculatively.
    """
    def priority(row):
        key = row["id"]
        if key.startswith("story:usa:"):
            return 0
        if key.startswith("unlock:usa:"):
            return 1
        if key.startswith("crosswalk:japan:"):
            return 2
        if key.startswith("crosswalk:usa:"):
            return 3
        if key.startswith("inspector:usa:"):
            return 4
        return 5

    def identity(row):
        if (row.get("width") is None or row.get("data_type") is None or
                row["region"] not in ("usa", "japan") or
                row["category"] in BLOCKED_LIVE_CATEGORIES):
            return ("unclassified", row["id"])
        return (row["region"], row["address"],
                row["width"], row.get("mask"))

    groups = {}
    for row in records:
        groups.setdefault(identity(row), []).append(row)
    results = []
    for group in groups.values():
        group.sort(key=lambda row: (priority(row), row["id"]))
        primary = dict(group[0])
        ids = []
        names = []
        sources = []
        evidence = []
        histories = []
        refs = []
        for row in group:
            for alias in (row["id"], *row.get("id_aliases", ())):
                if alias != primary["id"] and alias not in ids:
                    ids.append(alias)
            for name in (row["name"], *row.get("aliases", ())):
                if name != primary["name"] and name not in names:
                    names.append(name)
            for source in row.get("sources", ()):
                if source not in sources:
                    sources.append(source)
            if row.get("evidence") and row["evidence"] not in evidence:
                evidence.append(row["evidence"])
            for history in row.get("confidence_sources", ()):
                if history not in histories:
                    histories.append(history)
            own = {
                "confidence": row["confidence"],
                "source_id": row["id"],
                "evidence": row.get("evidence", ""),
            }
            if own not in histories:
                histories.append(own)
            for ref in row.get("mips_refs", ()):
                if ref and ref not in refs:
                    refs.append(ref)
            if primary.get("counterpart") is None and row.get("counterpart"):
                primary["counterpart"] = row["counterpart"]
            if not primary.get("control") and row.get("control"):
                primary["control"] = row["control"]
        primary["id_aliases"] = sorted(ids)
        primary["aliases"] = names
        primary["sources"] = sorted(sources)
        primary["evidence"] = "; ".join(evidence)
        primary["confidence_sources"] = histories
        primary["mips_refs"] = refs
        results.append(primary)
    results.sort(key=lambda r: (
        r["region"], int(r["address"], 16),
        r.get("mask") or "", r["id"]))
    return results


def build_catalogue():
    """Audit legacy declarations and reviewed manifests; no RAM reads.

    Runtime consumers load the authoritative JSON snapshot, never these
    source modules. Lazy imports avoid cycles when existing UI pages resolve
    their addresses from the canonical registry.
    """
    from practice.inspector import INVENTORY
    from practice.unlocks import UNLOCKS
    from practice.story_progress import FLAGS
    from practice.japanese_fields import JAPAN_FIELDS
    from practice.japanese_scene_probes import (
        JAPAN_SCENE_PROBES, RUNTIME_OBSERVATION_STATUS)
    from practice.region_memory_crosswalk import CROSS_REGION_FIELDS
    from practice.native_debug_watch import FIELDS as DEBUG_FIELDS

    items = []
    by_id = {}
    by_location = {}

    def add(row, *, reconcile=True):
        validate_entry(row)
        if row["id"] in by_id:
            return by_id[row["id"]]
        # Merge aliases from other sources for the *same unmasked scalar*;
        # independently named bits at a byte always remain distinct entries.
        loc = (row["region"], row["address"], row.get("mask"),
               row.get("width"))
        matched = by_location.get(loc) if reconcile else None
        if matched and row["mask"] is None:
            if matched["name"] != row["name"] and row["name"] not in matched["aliases"]:
                matched["aliases"].append(row["name"])
            for s in row["sources"]:
                if s not in matched["sources"]:
                    matched["sources"].append(s)
            if row["evidence"] and row["evidence"] not in matched["evidence"]:
                matched["evidence"] += "; " + row["evidence"]
            if row.get("control") and not matched.get("control"):
                matched["control"] = row["control"]
            if row.get("counterpart") and not matched.get("counterpart"):
                matched["counterpart"] = row["counterpart"]
            if row["id"] != matched["id"]:
                aliases = matched.setdefault("id_aliases", [])
                if row["id"] not in aliases:
                    aliases.append(row["id"])
            by_id[row["id"]] = matched
            return matched
        items.append(row)
        by_id[row["id"]] = row
        by_location.setdefault(loc, row)
        return row

    for unlock in UNLOCKS:
        add(_entry(
            f"unlock:usa:{unlock.slug}", unlock.label, unlock.address,
            "usa", "inventory", "u8", mask=unlock.bit_mask,
            confidence="user_observed", source="practice/unlocks.py",
            evidence=f"Item/group: {unlock.group}; individual level semantics",
            control="Unlocks / Items & equipment", owner=unlock.group))
    for flag in FLAGS:
        add(_entry(
            f"story:usa:{flag.key}", flag.label, flag.address, "usa",
            "saved_event_bit", "u8", mask=flag.mask,
            confidence=("external_unverified" if flag.external else "research_observed"),
            source="practice/story_progress.py", evidence=flag.evidence,
            control="Unlocks / Story & event flags", owner="Story Progress"))
    for name, address, width, maximum, note in INVENTORY:
        add(_entry(
            f"inspector:usa:{_slug(name)}", name, address, "usa",
            "inventory", f"u{width * 8}", source="practice/inspector.py",
            confidence="mixed_evidence", evidence=note,
            control="Live memory", owner="Inventory"))
    for field in CROSS_REGION_FIELDS:
        for region, address, other in (
                ("usa", field.usa, field.japan),
                ("japan", field.japan, field.usa)):
            confidence = field.evidence if region == "japan" else "usa_source"
            category = ("saved_event_bit" if field.mask is not None and
                        field.key.startswith(("event:", "plasma:")) else
                        "inventory" if field.key.startswith("unlock:") else
                        "fixed_global")
            control = ("Unlocks / Story & event flags"
                       if field.key.startswith(("event:", "plasma:")) else
                       "Unlocks / Items & equipment"
                       if field.key.startswith("unlock:") else "Live memory")
            add(_entry(
                f"crosswalk:{region}:{field.key}", field.label, address,
                region, category, f"u{field.width*8}", mask=field.mask,
                source="practice/region_memory_crosswalk.py",
                confidence=confidence, evidence=field.note or field.evidence,
                counterpart=other, control=control, owner=field.group))
    for field in JAPAN_FIELDS:
        dtype = f"u{field.width*8}" if field.kind != "hex" else f"u{field.width*8}"
        add(_entry(
            f"japanese:field:{field.key}", field.label, field.address,
            "japan", "inventory" if field.group in ("Items", "Weapons and skills",
                                                "Party") else "fixed_global",
            dtype, confidence="external_unverified", source=field.source,
            evidence=f"JP external {field.group}: {field.kind}",
            control="Live memory", owner=field.group))
    for field in JAPAN_SCENE_PROBES:
        confidence = ("observed" if field.key in RUNTIME_OBSERVATION_STATUS
                      else "disputed" if field.key == "scene_pause" else
                      "offset_candidate")
        add(_entry(
            f"japanese:scene:{field.key}", field.label, field.address,
            "japan", "fixed_global", f"u{field.width * 8}",
            source="practice/japanese_scene_probes.py",
            evidence=RUNTIME_OBSERVATION_STATUS.get(field.key, field.source),
            confidence=confidence, counterpart=field.usa_reference,
            context="Original Japanese scene/gameplay; load transitions",
            owner="Engine / scene", control="Live memory"))
    for field in DEBUG_FIELDS:
        add(_entry(
            f"native_debug:{field.key}", field.label, field.address,
            "usa", "dynamic_field" if "pointer" in field.key else "fixed_global",
            f"u{field.width*8}", source="practice/native_debug_watch.py",
            evidence=field.confidence,
            confidence="research_observed",
            context="Native debug menu; hover pointer only valid while menu active"
            if "pointer" in field.key else "Game scene",
            control="Live memory", owner="Native debug menu"))

    data = _read_json(DISCOVERIES)
    if data.get("format") != DISCOVERY_FORMAT or not isinstance(data.get("entries"), list):
        raise ValueError("Invalid discovery manifest")
    for record in data["entries"]:
        row = _entry(
            record["id"], record["name"], record["address"],
            record["region"], record["category"], record.get("data_type"),
            width=record.get("width"),
            mask=int(record["mask"], 16) if record.get("mask") else None,
            counterpart=record.get("counterpart"), confidence=record["confidence"],
            evidence=record.get("evidence", ""), source=record.get("source", ""),
            context=record.get("context", ""), control=record.get("control"),
            owner=record.get("owner", ""), live=record.get("live_readable"),
            source_revision=record.get("source_revision", ""),
            discovered=record.get("discovered"), updated=record.get("updated"))
        row["mips_refs"] = list(record.get("mips_refs", []))
        add(row)
    external = _read_json(EXTERNAL)
    if external.get("format") != "goemon-usa-external-memory-leads-v1":
        raise ValueError("External lead input format changed")
    for index, lead in enumerate(external["new_usa_address_leads"]):
        address = hexaddr(lead["address"])
        category = ("code_vma" if lead["kind"] == "code_address" else
                    "overlay_patch" if lead["kind"] == "overlay_patch" else
                    "external_cheat_lead")
        record = _entry(
            f"external:usa:{index:02d}", lead["label"], address, "usa",
            category, None, confidence="external_unverified",
            evidence=lead.get("note", ""), source=(
                "research/usa_external_memory_leads.json: "
                + lead.get("source", "")), context="Original external code: "
            + "; ".join(lead.get("raw_codes", [])), live=False)
        # Xplorer64 commands are a distinct address space, never guest data.
        if address.startswith("0xA"):
            record["category"] = "cheat_format"
        add(record, reconcile=False)
        if lead["kind"] == "repeating_progress_flag":
            origin = int(lead["address"], 16)
            for slot in range(11):
                add(_entry(
                    f"external:warp_slot:{slot+1:02d}",
                    f"All-warp unlock repeat entry {slot+1}/11",
                    origin + slot*4, "usa", "external_cheat_lead", None,
                    source="research/usa_external_memory_leads.json",
                    confidence="external_unverified",
                    evidence="GameShark 50000B04 repeat; destinations unproven",
                    context="Generated byte write index from original 11x+4 code",
                    live=False), reconcile=False)
        if lead["kind"] == "size_modifier":
            origin = int(lead["address"], 16)
            for index2 in range(1,3):
                add(_entry(
                    f"external:size_vector:{index2}", f"Size modifier vector component {index2+1}",
                    origin + 4*index2, "usa", "external_cheat_lead", None,
                    source="research/usa_external_memory_leads.json",
                    confidence="external_unverified", evidence=lead.get("note", ""),
                    live=False), reconcile=False)
    # A declaration audit for source modules not yet converted into typed
    # manifests. These unclassified references remain searchable but cannot
    # be polled or edited. A new hard-coded guest address in these modules
    # creates a reproducible registry diff in --check.
    source_root = Path(__file__).resolve().parents[1]
    source_modules = (
        "practice/checkpoints.py", "practice/inspector.py",
        "practice/scene_controls.py", "practice/unlocks.py",
        "practice/region_unlocks.py", "practice/story_progress.py",
        "practice/japanese_fields.py", "practice/japanese_scene_probes.py",
        "practice/region_memory_crosswalk.py", "practice/region_views.py",
        "practice/custom_watches.py", "practice/native_debug_watch.py",
    )
    for source_module in source_modules:
        source_path = source_root / source_module
        parsed = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(parsed):
            if not (isinstance(node, ast.Constant) and
                    type(node.value) is int and
                    0x80000000 <= node.value < 0x80800000):
                continue
            addr = hexaddr(node.value)
            provenance = f"{source_module}:{node.lineno}"
            same = [row for row in items if row["address"] == addr]
            if same:
                for row in same:
                    if provenance not in row["sources"]:
                        row["sources"].append(provenance)
                continue
            add(_entry(
                f"source:unclassified:{addr}",
                f"Unclassified source address {addr}", addr,
                "unknown", "research_reference", None,
                confidence="reference_only", source=provenance,
                evidence=("Address-shaped literal in toolkit Python source; "
                          "type/width/region not independently classified"),
                context="Source-reference only; register detailed discovery manifest",
                live=False, owner="Python declaration audit"), reconcile=False)
    mentions = _read_json(MENTIONS)
    if mentions.get("format") != "goemon-address-research-mentions-v1":
        raise ValueError("Research provenance format changed")
    for item in mentions["mentions"]:
        address = item["address"]
        same = [row for row in items if row["address"] == address]
        for mention in item["mentions"]:
            source = f"{mention['path']}:{mention['line']}@{mention['branch']}"
            if same:
                for row in same:
                    if source not in row["sources"]:
                        row["sources"].append(source)
            else:
                add(_entry(
                    f"research:mention:{address}", f"Research mention at {address}",
                    address, "unknown", "research_reference", None,
                    confidence="reference_only", source=source,
                    evidence=mention["context"], live=False,
                    context="Original ROM region/type unclassified; not a live read",
                    owner="Research mentions"), reconcile=False)
                same = [items[-1]]

    records = consolidate_entries(items)
    payload = {
        "format": CATALOGUE_FORMAT,
        "version": 1,
        "generated": SOURCE_DATE,
        "sources": sorted(set(source for r in records for source in r["sources"])),
        "entries": records,
    }
    validate_catalogue(payload)
    return payload


def search_entries(payload, query="", *, region="all", evidence="all",
                   category="all", data_type="all", limit=None,
                   already_validated=False):
    """Search names, addresses, masks, aliases, provenance and descriptions."""
    if not already_validated:
        validate_catalogue(payload)
    q = str(query).strip().casefold().replace("0x", "")
    matches = []
    for row in payload["entries"]:
        if region != "all" and row["region"] != region:
            continue
        if evidence != "all" and row["confidence"] != evidence:
            continue
        if category != "all" and row["category"] != category:
            continue
        if data_type != "all" and row["data_type"] != data_type:
            continue
        text = " ".join(str(row.get(key) or "") for key in (
            "id", "name", "address", "mask", "category", "data_type",
            "confidence", "evidence", "sources", "aliases", "context",
            "counterpart", "owner", "confidence_sources", "id_aliases"))
        if q and q not in text.casefold().replace("0x", ""):
            continue
        matches.append(row)
        if limit is not None and len(matches) >= limit:
            break
    return matches


def decode_read(ram, record):
    """One bounded guest-RAM read. Never dereferences a stored pointer."""
    validate_entry(record)
    if not record["live_readable"]:
        return ("Unavailable: research/unsupported type", "—")
    width = record["width"]
    address = int(record["address"], 16)
    raw = ram.read_guest(address, width)
    if len(raw) != width:
        raise OSError("Short guest-memory read")
    kind = record["data_type"]
    if kind == "hex8":
        decoded = "0x" + raw.hex().upper()
    elif kind in ("f32", "f64"):
        decoded = str(struct.unpack(">f" if kind == "f32" else ">d", raw)[0])
    else:
        decoded = str(int.from_bytes(
            raw, "big", signed=kind.startswith("s")))
    if record.get("mask") is not None:
        decoded += f"  (bit {'On' if int.from_bytes(raw, 'big') & int(record['mask'], 16) else 'Off'})"
    return decoded, "0x" + raw.hex().upper()


def audit_catalogue(payload):
    validate_catalogue(payload)
    return {
        "format": "goemon-address-catalogue-audit-v1",
        "total_records": len(payload["entries"]),
        "unique_region_address": len({
            (r["region"], r["address"]) for r in payload["entries"]}),
        "by_region": dict(Counter(r["region"] for r in payload["entries"])),
        "by_category": dict(Counter(r["category"] for r in payload["entries"])),
        "by_confidence": dict(Counter(r["confidence"] for r in payload["entries"])),
        "live_readable": sum(r["live_readable"] for r in payload["entries"]),
        "research_only": sum(not r["live_readable"] for r in payload["entries"]),
        "unknown_width": sum(r.get("width") is None for r in payload["entries"]),
        "disputed": sum(r["confidence"] in ("disputed", "conflict")
                        for r in payload["entries"]),
        "experimental_japan_flags": sum(
            r["region"] == "japan" and
            r["category"] == "saved_event_bit" for r in payload["entries"]),
    }


def serialize(payload):
    validate_catalogue(payload)
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True,
                       indent=2) + "\n").encode("utf-8")
