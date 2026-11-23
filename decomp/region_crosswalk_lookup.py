#!/usr/bin/env python3
"""Read-only original-USA/Japan function lookup from the sanitized full audit CSVs.

python3 -m decomp.region_crosswalk_lookup --audit PATH --region usa --rom 0x35EAC

No binary game data, emulator access, RAM writes or offset arithmetic.
"""
import argparse
import csv
import json
from pathlib import Path


def lookup(root, region, rom=None, name=None):
    if region not in ("usa", "japan_0"):
        raise ValueError("Unsupported game region")
    index = Path(root) / "all_14752_with_canonical_C_status.csv"
    donor_file = Path(root) / "all_583_asm_destinations_with_accepted_C_donors_ranked.csv"
    if not index.is_file() or not donor_file.is_file():
        raise FileNotFoundError("Extract the complete original-function audit ZIP first")

    with index.open(newline="") as handle:
        matches = [
            record for record in csv.DictReader(handle)
            if record["region"] == region
            and (
                int(record["original_ROM_offset"], 16) == rom
                if rom is not None else record["name"] == name
            )
        ]
    if not matches:
        return {"region": region, "status": "NOT_FOUND", "matches": []}

    with donor_file.open(newline="") as handle:
        available = {
            (row["destination_region"], int(row["destination_original_ROM_offset"], 16)): row
            for row in csv.DictReader(handle)
        }
    result = []
    for row in matches:
        entry = {
            "name": row["name"],
            "region": region,
            "original_rom_offset": row["original_ROM_offset"],
            "original_vma": row["original_VMA"],
            "original_function_bytes": int(row["size"]),
            "source_section": row["section"],
            "canonical_C_status": row["canonical_C_status"],
            "signature_class": row["classification"],
            "other_region_signature_candidates": int(row["peer_signature_count"]),
            "other_region_accepted_C_donors": int(row["accepted_C_donors_in_other_region"]),
            "top_peer": {
                "name": row["top_peer_name"],
                "original_rom_offset": row["top_peer_rom"],
            } if row["top_peer_name"] else None,
        }
        donor = available.get((region, int(row["original_ROM_offset"], 16)))
        if donor:
            entry["source_donor"] = {
                "priority": donor["priority_tier"],
                "region": donor["donor_region"],
                "name": donor["donor_accepted_C_name"],
                "rom_offset": donor["donor_original_ROM_offset"],
                "different_original_instruction_words": int(donor["region_original_word_differences"]),
                "original_native_destination_G2": donor["full_original_ROM_own_region_G2"],
            }
        result.append(entry)
    return {"region": region, "status": "FOUND", "matches": result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--region", required=True, choices=("usa", "japan_0"))
    choices = parser.add_mutually_exclusive_group(required=True)
    choices.add_argument("--rom", type=lambda text: int(text, 0))
    choices.add_argument("--name")
    args = parser.parse_args(argv)
    print(json.dumps(lookup(args.audit, args.region, args.rom, args.name), indent=2))


if __name__ == "__main__":
    main()
