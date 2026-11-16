#!/usr/bin/env python3
"""Export the read-only source-qualified USA/JP crosswalk as CSV.

Usage: python3 scripts/export_region_memory_crosswalk.py > crosswalk.csv
Never contacts a running emulator or writes game memory.
"""
from __future__ import annotations

import csv
import sys

from practice.region_memory_crosswalk import CROSS_REGION_FIELDS


def rows():
    for field in CROSS_REGION_FIELDS:
        yield {
            "key": field.key,
            "group": field.group,
            "label": field.label,
            "usa": f"0x{field.usa:08X}",
            "jp": f"0x{field.japan:08X}",
            "width_bytes": field.width,
            "mask": f"0x{field.mask:02X}" if field.mask is not None else "",
            "status": field.evidence,
            "delta_exception": "yes" if field.is_exception else "no",
            "notes": field.note,
        }


def main():
    writer = csv.DictWriter(sys.stdout, fieldnames=[
        "key", "group", "label", "usa", "jp", "width_bytes",
        "mask", "status", "delta_exception", "notes",
    ])
    writer.writeheader()
    writer.writerows(rows())


if __name__ == "__main__":
    main()
