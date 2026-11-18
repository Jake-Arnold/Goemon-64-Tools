"""Read the project-wide canonical guest-data registry without duplicating it.

This is a metadata-only decomp research tool. The authoritative catalogue
lives at practice/data/address_catalogue_v1.json on toolkit main. The caller
provides a local snapshot; this module never fetches code, opens ROM files or
writes game memory. Matching-C source/ELF identity remains independent.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class RegistryView:
    entries: tuple[dict, ...]
    index: dict[str, dict]

    def lookup(self, field_id: str) -> dict:
        try:
            return self.index[field_id]
        except KeyError as exc:
            raise KeyError(f"Unknown canonical memory field: {field_id}") from exc

    def flag_counts(self) -> dict[str, int]:
        counts = Counter(row["region"] for row in self.entries
                         if row["category"] == "saved_event_bit")
        return {"usa": counts["usa"], "japan": counts["japan"]}


def validate_bidirectional_flags(entries) -> None:
    """Reject incomplete declared bit pairs; never invent a ROM counterpart."""
    by_location = {
        (row["region"], row["address"], row.get("mask"))
        for row in entries if row["category"] == "saved_event_bit"
    }
    for row in entries:
        if (row["category"] != "saved_event_bit"
                or row["region"] not in ("usa", "japan")):
            continue
        other = row.get("counterpart")
        if other is None and row.get("crosswalk_status") == "unresolved":
            continue
        paired_region = "japan" if row["region"] == "usa" else "usa"
        if not other or (paired_region, other, row.get("mask")) not in by_location:
            raise ValueError(f"{row['id']}: missing reciprocal saved-event pair")


def load_canonical_registry(path: str | Path) -> RegistryView:
    """Load a reviewed snapshot from main and check ID and flag-pair integrity."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("format") != "goemon-address-catalogue-v1":
        raise ValueError("Not the canonical Goemon address-catalogue format")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Empty or invalid canonical memory catalogue")
    by_id = {}
    for row in entries:
        if (not isinstance(row, dict) or
                not all(isinstance(row.get(k), str) for k in (
                    "id", "region", "address", "category"))):
            raise ValueError("Invalid canonical memory record")
        for key in (row["id"], *row.get("id_aliases", ())):
            if key in by_id:
                raise ValueError(f"Duplicate canonical ID/alias: {key}")
            by_id[key] = row
    validate_bidirectional_flags(entries)
    return RegistryView(tuple(entries), by_id)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path,
                        help="Local copy of main:practice/data/address_catalogue_v1.json")
    parser.add_argument("--field", help="Stable field ID or registry alias")
    args = parser.parse_args(argv)
    data = load_canonical_registry(args.catalogue)
    if args.field:
        print(json.dumps(data.lookup(args.field), sort_keys=True, indent=2))
    else:
        print(json.dumps({"total": len(data.entries),
                          "saved_event_flags": data.flag_counts()},
                         sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
