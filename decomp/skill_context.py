"""Compact canonical Goemon decomp proof/inventory context; no ROM build.

The obsolete G64-001..100 plan was retired. This module deliberately does not
load or schedule historical G64 tasks. Latest local/published G2 batches may be
newer than the stored canonical USA combined/inventory checkpoint.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(root=ROOT):
    """Load published canonical proof metadata, not historical task packets."""
    root = Path(root)
    read = lambda path: json.loads(path.read_text(encoding="utf-8"))
    result = read(root / "results" / "combined.json")
    inventory = read(root / "results" / "inventory.json")
    comparison = result["comparison"]
    summary = inventory["summary"]
    return {"proof": {
        "status": result.get("status"),
        "full_rom_match": comparison.get("full_rom_match"),
        "matched": comparison.get("matched_functions"),
        "claimed": comparison.get("claimed_functions"),
        "bytes": comparison.get("matched_function_bytes"),
        "rom_size": comparison.get("rom_size"),
        "sha1": comparison.get("candidate_sha1"),
        "inventory_sha1": inventory.get("decompressed_sha1"),
        "c_total": summary.get("current_unmarked_entries"),
        "asm_total": summary.get("remaining_assembly_entries"),
        "identified": summary.get("identified_function_entries"),
        "new_c": summary.get("newly_matching_c"),
        "baseline_c": summary.get("upstream_unmarked_entries"),
    }}


def validate(data):
    """Fail closed on inconsistent stored proof/inventory; not a new G2 run."""
    p = data["proof"]
    errors = []
    if p["status"] != "matched" or p["full_rom_match"] is not True:
        errors.append("Recorded whole-ROM proof is not matched")
    for field in ("matched", "claimed", "bytes", "rom_size", "c_total",
                  "asm_total", "identified", "new_c", "baseline_c"):
        if type(p.get(field)) is not int or p[field] < 0:
            errors.append("Malformed or negative numeric proof field: " + field)
    if errors:
        return errors
    if p["matched"] != p["claimed"] or p["claimed"] != p["new_c"]:
        errors.append("Proof/inventory claim counts disagree")
    if p["c_total"] != p["new_c"] + p["baseline_c"]:
        errors.append("Published baseline/claimed-C partition disagrees")
    if p["c_total"] + p["asm_total"] != p["identified"]:
        errors.append("Inventory C/ASM totals disagree")
    if p["rom_size"] != 33554432:
        errors.append("Expected expanded original-ROM size is 33,554,432 bytes")
    if not isinstance(p.get("sha1"), str) or len(p["sha1"]) != 40:
        errors.append("Missing candidate ROM SHA-1")
    if p["sha1"] != p.get("inventory_sha1"):
        errors.append("Proof/inventory candidate ROM SHA-1 differs")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--status", action="store_true", help="Show stored canonical USA proof/inventory")
    mode.add_argument("--validate", action="store_true", help="Validate stored proof/inventory consistency")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = load()
    errors = validate(data)
    if errors:
        parser.error("; ".join(errors))
    if args.validate:
        result = {"status": "CONSISTENT_STORED_REPORTS",
                  "notice": "No fresh original-ROM verification performed"}
    else:
        result = {"published_canonical_proof": data["proof"],
                  "notice": "Stored USA checkpoint only; read CONTINUE.md and latest G2 reports for newer batches"}
    if args.json or args.status:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["status"] + ": " + result["notice"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
