"""Generate and audit the canonical toolkit address registry.

The versioned JSON registry is the runtime source of truth. Legacy Python
address declarations are *inputs for reconciliation only*, not live lookup
tables. New research manifests import automatically; conflicting legacy
changes fail --check instead of silently overwriting a reviewed address.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from practice.address_catalogue import (
    SNAPSHOT, DATA_DIR, audit_catalogue, build_catalogue, serialize,
    validate_catalogue, _read_json,
)

AUDIT = DATA_DIR / "address_catalogue_audit.json"
CANONICAL_FIELDS = ("address", "region", "width", "data_type", "mask",
                    "category", "counterpart")
DERIVED_PREFIXES = ("research:", "external:", "japanese:", "crosswalk:",
                    "story:", "unlock:", "inspector:", "native_debug:")
SOURCE_ONLY_TYPES = ("research:", "external:")


def synchronise(existing=None):
    declarations = build_catalogue()
    if existing is None:
        return declarations, [], len(declarations["entries"])
    validate_catalogue(existing)
    current = {r["id"]: r for r in existing["entries"]}
    generated = {r["id"]: r for r in declarations["entries"]}
    conflicts = []
    added = 0
    for key, row in generated.items():
        if key not in current:
            current[key] = row
            added += 1
            continue
        prior = current[key]
        diffs = [k for k in CANONICAL_FIELDS if prior.get(k) != row.get(k)]
        if diffs and not key.startswith(SOURCE_ONLY_TYPES):
            conflicts.append({"id": key, "fields": diffs,
                              "registry": {k: prior.get(k) for k in diffs},
                              "declaration": {k: row.get(k) for k in diffs}})
        # Research discovery manifests are authoritative on their own IDs:
        # refreshed labels/evidence/decoder classifications may change only
        # after passing schema checks. Never accept remote writer permissions.
        if key.startswith(SOURCE_ONLY_TYPES):
            row["control"] = prior.get("control")
            current[key] = row
        else:
            prior["sources"] = sorted(set(
                prior.get("sources", ()) + row.get("sources", ())))
            prior["aliases"] = list(dict.fromkeys(
                prior.get("aliases", ()) + row.get("aliases", ())))
            prior["id_aliases"] = list(dict.fromkeys(
                prior.get("id_aliases", ()) + row.get("id_aliases", ())))
    out = dict(existing)
    out["entries"] = sorted(current.values(), key=lambda r: (
        r["region"], int(r["address"], 16), r.get("mask") or "", r["id"]))
    out["sources"] = sorted(set(s for r in out["entries"]
                                for s in r["sources"]))
    validate_catalogue(out)
    return out, conflicts, added


def write_or_check(*, check=False):
    existing = _read_json(SNAPSHOT) if SNAPSHOT.is_file() else None
    result, conflicts, added = synchronise(existing)
    if conflicts:
        print(json.dumps({"conflicts": conflicts}, indent=2), file=sys.stderr)
        raise ValueError("Registry/source conflict: review and update the "
                         "canonical registry manifest deliberately")
    registry_bytes = serialize(result)
    audit_bytes = (json.dumps(audit_catalogue(result),
                             indent=2, sort_keys=True) + "\n").encode("utf-8")
    if check:
        if existing is None or SNAPSHOT.read_bytes() != registry_bytes:
            raise ValueError("Address registry is outdated; run "
                             "python -m scripts.sync_address_catalogue --write")
        if not AUDIT.is_file() or AUDIT.read_bytes() != audit_bytes:
            raise ValueError("Address audit is outdated; regenerate")
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SNAPSHOT.write_bytes(registry_bytes)
        AUDIT.write_bytes(audit_bytes)
    print(f"Registry: {len(result['entries'])} fields, "
          f"{added} new, {audit_catalogue(result)['live_readable']} readable, "
          f"{len(conflicts)} conflicts; mode={'check' if check else 'write'}")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        write_or_check(check=args.check)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Address catalogue sync failed: {exc}\n")


if __name__ == "__main__":
    main()
