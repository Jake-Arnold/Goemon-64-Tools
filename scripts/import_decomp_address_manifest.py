"""Import metadata-only research from the separate decomp branch.

The source file is an externally staged, versioned *data* manifest. Its
contents are schema-validated and can never authorize writes or merge decomp
code into the toolkit. Conflicting addresses create explicit disputed leads
instead of silently overwriting the reviewed canonical fields.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from practice.address_catalogue import DISCOVERIES
from practice.address_catalogue_remote import validate_discoveries


def import_upstream(local, upstream, *, upstream_revision):
    validate_discoveries(local)
    validate_discoveries(upstream)
    records = {row["id"]: dict(row) for row in local["entries"]}
    added = updated = disputed = 0
    for candidate in upstream["entries"]:
        if not candidate["id"].startswith(("decomp:", "research:")):
            raise ValueError("Decomp manifest may register only decomp:/research: IDs")
        if not str(candidate["source"]).startswith("decomp/"):
            raise ValueError("Decomp discovery needs an explicit decomp/ source")
        incoming = dict(candidate)
        incoming["control"] = None
        incoming["source_revision"] = upstream_revision
        old = records.get(incoming["id"])
        if old is None:
            records[incoming["id"]] = incoming
            added += 1
            continue
        identity = ("address", "region", "width", "mask", "category")
        if any(old.get(key) != incoming.get(key) for key in identity):
            # Keep both, with an ID unique to this revision + address. A
            # conflict must be reviewable, not treated as new verification.
            safe_revision = re.sub(r"[^a-z0-9]", "", upstream_revision.lower())[:12]
            dispute_key = (
                f"decomp:conflict:{incoming['id']}:{safe_revision}:"
                + incoming["address"].removeprefix("0x").lower())
            incoming["id"] = dispute_key
            incoming["confidence"] = "disputed"
            incoming["evidence"] = (
                "Conflicts with canonical " + old["id"] + " at "
                + old["address"] + ". " + incoming.get("evidence", ""))
            incoming["live_readable"] = False
            records[dispute_key] = incoming
            disputed += 1
            continue
        # Existing registry identity wins on evidence status and decoding
        # unless a human deliberately promotes the reviewed record.
        old["source_revision"] = upstream_revision
        old_evidence = old.get("evidence", "")
        incoming_evidence = incoming.get("evidence", "")
        if incoming_evidence and incoming_evidence not in old_evidence:
            old["evidence"] = (
                old_evidence + "; " + incoming_evidence).strip("; ")
            updated += 1
    merged = dict(local)
    merged["entries"] = sorted(records.values(), key=lambda r: r["id"])
    validate_discoveries(merged)
    return merged, {"added": added, "updated": updated,
                    "disputed": disputed}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", required=True, type=Path,
                        help="Previously fetched decomp branch manifest JSON")
    parser.add_argument("--revision", required=True,
                        help="Exact source branch commit or recorded revision")
    parser.add_argument("--output", type=Path, default=DISCOVERIES)
    args = parser.parse_args(argv)
    current = json.loads(DISCOVERIES.read_text(encoding="utf-8"))
    incoming = json.loads(args.upstream.read_text(encoding="utf-8"))
    merged, summary = import_upstream(
        current, incoming, upstream_revision=args.revision)
    target = args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
