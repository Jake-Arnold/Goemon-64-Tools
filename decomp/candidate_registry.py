"""Fail-closed USA/Japan matching-C candidate inventory and native-batch planner.

ROM offsets here are expanded-ROM offsets, never retail offsets or RAM crosswalks.
This module does NOT promote code or replace original MIPS/whole-ROM verification.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

EXPANDED_SIZE = 33_554_432
ROM_SHA1 = {
    "usa": "6ea0ed71032ce08fc2745f412d84936382197494",
    "japan_0": "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FUNC = re.compile(r"^func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)$")


class RegistryError(ValueError):
    """Candidate metadata or provenance is unsafe for native staging."""


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_files(repo: Path, registry: Path | None = None):
    source = registry or repo / "decomp/data/candidate_registry.json"
    with source.open(encoding="utf-8") as handle:
        candidates = json.load(handle)
    with (repo / "decomp/data/rom_file_inventory.csv").open(newline="", encoding="utf-8") as handle:
        files = list(csv.DictReader(handle))
    return candidates, files


def _int_hex(value, label: str) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9A-Fa-f]+", value):
        raise RegistryError(f"{label}: expected hex address")
    return int(value, 16)


def _source_bytes(repo: Path, source: dict, cache: dict) -> bytes:
    path = source.get("path")
    if not isinstance(path, str):
        raise RegistryError("candidate source path missing")
    rel = PurePosixPath(path)
    if rel.is_absolute() or ".." in rel.parts or not path.startswith("decomp/"):
        raise RegistryError(f"unsafe source path: {path}")
    if path not in cache:
        file = (repo / path).resolve()
        if not file.is_relative_to(repo.resolve()) or not file.is_file():
            raise RegistryError(f"candidate source missing: {path}")
        cache[path] = file.read_bytes()
    raw = cache[path]
    expected = source.get("git_blob_sha")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise RegistryError(f"missing source Git blob identity: {path}")
    if git_blob_sha(raw) != expected:
        raise RegistryError(f"source drift: {path}")
    return raw


def validate(repo: Path, registry: dict, inventory: list[dict]) -> dict:
    if registry.get("format") != "goemon-candidate-registry-v1":
        raise RegistryError("unknown candidate registry version")
    if len(inventory) != 1311 or inventory[0].get("File") != "file_1" or inventory[-1].get("File") != "file_1311":
        raise RegistryError("1,311-slot USA/Japan ROM file index missing or incorrect")
    by_file = {row["File"]: row for row in inventory}
    if len(by_file) != 1311:
        raise RegistryError("duplicate numbered ROM file slot")
    accepted = registry.get("accepted_baseline")
    if not isinstance(accepted, dict) or any(not isinstance(accepted.get(key), int) or accepted[key] < 0 for key in ("usa_functions", "japan_0_functions")):
        raise RegistryError("invalid registry production baseline")
    actual = json.loads((repo / "decomp/results/inventory.json").read_text(encoding="utf-8"))
    if actual["summary"]["newly_matching_c"] != accepted["usa_functions"]:
        raise RegistryError("USA canonical inventory changed; re-deduplicate before use")
    japan = json.loads((repo / "decomp/regions/japan_0.json").read_text(encoding="utf-8"))
    jp_total = sum(len(unit["functions"]) for unit in japan["units"])
    if jp_total != accepted["japan_0_functions"]:
        raise RegistryError("Japan canonical manifest changed; re-deduplicate before use")
    first_file = {
        "usa": int(inventory[0]["USA expanded ROM offset"], 16),
        "japan_0": int(inventory[0]["Japan expanded ROM offset"], 16),
    }
    seen = set()
    intervals = defaultdict(list)
    src_cache = {}
    counts = Counter()
    bytes_by_region = Counter()
    groups = Counter()
    rows = registry.get("candidates")
    if not isinstance(rows, list):
        raise RegistryError("missing candidate list")
    for row in rows:
        region = row.get("region")
        segment = row.get("segment")
        if region not in ROM_SHA1:
            raise RegistryError(f"unsupported region: {region}")
        if not isinstance(segment, str) or (segment != "main" and segment not in by_file):
            raise RegistryError(f"unsupported segment: {segment}")
        name = row.get("name")
        match = FUNC.fullmatch(name) if isinstance(name, str) else None
        if not match:
            raise RegistryError(f"invalid original function name: {name}")
        start = _int_hex(row.get("rom_offset"), "rom_offset")
        vma = _int_hex(row.get("vma"), "vma")
        size = row.get("size")
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0 or size % 4:
            raise RegistryError(f"invalid code length for {name}: {size}")
        if start % 4 or vma % 4 or start + size > EXPANDED_SIZE:
            raise RegistryError(f"invalid original code bounds: {name}")
        if int(match.group(1), 16) != vma or int(match.group(2), 16) != start:
            raise RegistryError(f"symbol/ROM-offset mismatch: {name}")
        hash_value = row.get("original_code_sha256")
        if not isinstance(hash_value, str) or not HEX64.fullmatch(hash_value):
            raise RegistryError(f"missing original instruction hash: {name}")
        if segment == "main":
            if start + size > first_file[region]:
                raise RegistryError(f"main executable overlaps numbered files: {name}")
        else:
            file = by_file[segment]
            field = "USA" if region == "usa" else "Japan"
            a = int(file[f"{field} expanded ROM offset"], 16)
            b = a + int(file[f"{field} expanded bytes"])
            if not file["Segment classification"].startswith("Executable:") or not a <= start < start + size <= b:
                raise RegistryError(f"candidate outside {region} {segment} expanded extent: {name}")
        key = (region, segment, start)
        if key in seen:
            raise RegistryError(f"duplicate original function identity: {name}")
        seen.add(key)
        intervals[(region, segment)].append((start, start + size, name))
        if row.get("status") != "RESEARCH_ONLY" or row.get("canonical_g2") != "NOT_RUN":
            raise RegistryError(f"unverified promotion claim: {name}")
        source = row.get("source")
        if not isinstance(source, dict):
            raise RegistryError(f"source provenance missing: {name}")
        content = _source_bytes(repo, source, src_cache)
        if name.encode() not in content:
            raise RegistryError(f"source does not identify candidate {name}")
        if not isinstance(row.get("provenance"), list) or not row["provenance"]:
            raise RegistryError(f"missing research provenance for {name}")
        counts[region] += 1
        bytes_by_region[region] += size
        groups[(region, segment)] += 1
    for key, intervals_for_section in intervals.items():
        sorted_intervals = sorted(intervals_for_section)
        for left, right in zip(sorted_intervals, sorted_intervals[1:]):
            if left[1] > right[0]:
                raise RegistryError(f"overlapping {key} candidates: {left[2]}, {right[2]}")
    totals = registry.get("expected_pending")
    if totals != {"usa_functions": counts["usa"], "usa_bytes": bytes_by_region["usa"],
                  "japan_0_functions": counts["japan_0"], "japan_0_bytes": bytes_by_region["japan_0"]}:
        raise RegistryError("pending function/byte totals do not agree with the records")
    return {"functions": dict(counts), "bytes": dict(bytes_by_region),
            "groups": {f"{r}/{s}": v for (r, s), v in sorted(groups.items())},
            "source_files_checked": len(src_cache)}


def verify_original_images(registry: dict, images: dict[str, Path]) -> dict:
    output = {}
    for region, path in images.items():
        if path is None:
            continue
        data = path.read_bytes()
        if len(data) != EXPANDED_SIZE or hashlib.sha1(data).hexdigest() != ROM_SHA1[region]:
            raise RegistryError(f"{region}: wrong original expanded-ROM SHA-1 or length")
        tested = 0
        for candidate in registry["candidates"]:
            if candidate["region"] != region:
                continue
            off = int(candidate["rom_offset"], 16)
            size = candidate["size"]
            actual = hashlib.sha256(data[off:off + size]).hexdigest()
            if actual != candidate["original_code_sha256"]:
                raise RegistryError(f"original ROM hash mismatch: {candidate['name']}")
            tested += 1
        output[region] = {"expanded_sha1": ROM_SHA1[region], "original_instruction_hashes_checked": tested}
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--usa-expanded", type=Path)
    parser.add_argument("--japan-expanded", type=Path)
    args = parser.parse_args()
    try:
        registry, inventory = load_files(args.repo, args.registry)
        result = validate(args.repo, registry, inventory)
        result["original_rom_checks"] = verify_original_images(registry, {
            "usa": args.usa_expanded, "japan_0": args.japan_expanded})
    except (RegistryError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(2, f"BLOCKED_INPUT: {exc}\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
