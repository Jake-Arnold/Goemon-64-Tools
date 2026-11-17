#!/usr/bin/env python3
"""Agent/CLI: propose a USA <-> JP data address; no RAM access.

Known:
 python3 scripts/crosswalk_address.py --source usa --address 0x8015C60C --mask 0x20
 python3 scripts/crosswalk_address.py --source jp --address 0x80162057

Unknown classified static field:
 python3 scripts/crosswalk_address.py --source jp --address 0x80161E00 --kind static-global

Result is a JSON array of explicit mappings or *unverified* candidates.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from practice.region_crosswalk_agent import propose_other_region


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("usa", "jp", "japan"), required=True)
    parser.add_argument("--address", type=lambda v: int(v, 0), required=True)
    parser.add_argument("--kind", choices=("static-global", "saved-event"))
    parser.add_argument("--width", type=int, choices=(1, 2, 4), default=1)
    parser.add_argument("--mask", type=lambda v: int(v, 0))
    args = parser.parse_args(argv)
    try:
        proposals = propose_other_region(
            "japan" if args.source in ("jp", "japan") else "usa",
            args.address, kind=args.kind, width=args.width, mask=args.mask)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps([proposal.as_dict() for proposal in proposals], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
