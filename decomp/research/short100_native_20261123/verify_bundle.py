#!/usr/bin/env python3
"""Validate the supplied source-only 100-function ZIP without original ROMs."""
import hashlib
import json
import pathlib
import stat
import sys
import zipfile
from collections import Counter

EXPECTED = "b8733ae1670e0a7345f26744b41c33c25c44f1088247000610dc32cfa9b39226"
PREFIX = "goemon-native100-20261123/"
def require(ok, message):
    if not ok:
        raise SystemExit("INVALID: " + message)
def main():
    require(len(sys.argv) == 2, "usage: python verify_bundle.py <goemon-native100-20261123.zip>")
    path = pathlib.Path(sys.argv[1])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    require(digest == EXPECTED, "archive sha256 mismatch")
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        require(len(names) == 204, "expected exactly 204 entries")
        for item in z.infolist():
            segments = item.filename.split("/")
            require(item.filename.startswith(PREFIX) and ".." not in segments and
                    not item.filename.startswith("/") and "\\" not in item.filename,
                    "unsafe archive path")
            require(not stat.S_ISLNK(item.external_attr >> 16), "symlink")
        for name in ("README.md", "manifest.json", "evidence.json", "replay.py"):
            require(PREFIX + name in names, "missing " + name)
        manifest = json.loads(z.read(PREFIX + "manifest.json"))
        evidence = json.loads(z.read(PREFIX + "evidence.json"))
        cs = manifest["candidates"]
        require(len(cs) == 100 and evidence["total_verified"] == 100, "candidate count")
        require(manifest["research_isolated_bytes"] == evidence["total_original_bytes"] == 6824,
                "original byte count")
        require(manifest["research_isolated_relocations"] == 478, "relocation count")
        require(evidence["negative_controls"] == 100 and evidence["canonical_promoted_delta"] == 0,
                "negative controls/claim count")
        require(evidence["complete_rom"] == "NOT_RUN" and evidence["full_unit"] == "NOT_RUN",
                "unexpected promotion claim")
        require(manifest["new_accepted_c_claims"] == 0, "unexpected accepted-C claim")
        owned = set()
        regions = Counter()
        groups = Counter()
        ranges = {"usa": [], "japan_0": []}
        for c in cs:
            region = c["region"]
            require(region in regions or region in ("usa", "japan_0"), "invalid region")
            key = (region, c["rom_offset"], c["vma"], c["original_bytes"])
            require(key not in owned, "duplicate function")
            owned.add(key)
            require(0 < c["original_bytes"] < 100 and c["original_bytes"] % 4 == 0,
                    "function size")
            require(c["rom_offset"] >= 0 and c["rom_offset"] + c["original_bytes"] <= 33554432,
                    "ROM bounds")
            ranges[region].append((c["rom_offset"], c["rom_offset"] + c["original_bytes"]))
            for file_key, hash_key in (
                ("source", "source_sha256"), ("negative_source", "negative_sha256")
            ):
                name = PREFIX + c[file_key]
                require(name in names, "missing source " + name)
                require(hashlib.sha256(z.read(name)).hexdigest() == c[hash_key],
                        "source checksum mismatch " + name)
            require(c["isolated_native_status"] == "PASS_EXACT_WITH_SYMBOLIC_RELOCATIONS",
                    "nonpassing native result")
            require(c["unit_gate"] == "NOT_RUN" and c["complete_rom_gate"] == "NOT_RUN",
                    "false complete unit/ROM claim")
            regions[region] += 1
            groups[str(c["family_id"])] += 1
        for region, rs in ranges.items():
            rs.sort()
            require(all(rs[i][1] <= rs[i+1][0] for i in range(len(rs)-1)),
                    "overlapping ROM ranges for " + region)
        require(regions == {"usa": 72, "japan_0": 28}, "region counts")
        require(dict(groups) == manifest["families"], "family counts")
        print("PASS: 100 checked function identities; 200 authentic source hashes;"
              " 72 USA / 28 JP; 6824 bytes; 478 relocations")
        print("Research only: native results described in evidence; no full-ROM G2")
if __name__ == "__main__":
    main()
