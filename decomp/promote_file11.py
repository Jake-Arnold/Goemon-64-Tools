"""Fail-closed orchestrator for promoting USA file_11 C after *central* G2.

Does not modify the checked-in manifest, combined proof or inventory. It emits a
promotion review bundle only after a fresh complete `decomp.verify` run and
`decomp.inventory` both pass. Original ROMs and ELF files stay outside the repo.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

try:
    from . import overlay_file11
    from .research import usa_file11_noop_groups
except ImportError:
    import overlay_file11
    from research import usa_file11_noop_groups

STAGE = {"format": "goemon-file11-character-switch-50-v2"}
ORIGINAL_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ORIGINAL_ROM_BYTES = 33_554_432
OLD_FUNCTIONS = 160
NEW_FUNCTIONS = 50
TOTAL_FUNCTIONS = 210
OLD_BYTES = 12_272
NEW_BYTES = 1_064
TOTAL_BYTES = 13_336
EXPECTED_RELOCATIONS = 8_825
EXPECTED_ENTRIES = 7_376


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_file11_names() -> set[str]:
    old = {entry[0] for entry in overlay_file11.FUNCTIONS}
    new = {name for name, _ in usa_file11_noop_groups.entries()}
    if len(old) != 13 or len(new) != 37 or len(old | new) != NEW_FUNCTIONS:
        raise ValueError("Pinned file_11 names are no longer 13+37 unique functions")
    if (sum(entry[2] for entry in overlay_file11.FUNCTIONS) + 12*len(new)) != NEW_BYTES:
        raise ValueError("Pinned file_11 reconstructed code extent changed")
    return old | new


def candidate_manifest(original: dict) -> dict:
    """Create an opt-in review manifest without changing canonical production."""
    if not isinstance(original, dict) or original.get("format") != "goemon-matching-decomp-v1":
        raise ValueError("Expected original decomp manifest format")
    if "overlay_file11_stage" in original:
        raise ValueError("Canonical manifest already contains a file_11 stage; review before rerun")
    previous = sum(len(u["functions"]) for u in original["units"])
    previous += len(original.get("existing_source_patches", []))
    previous += int(original.get("overlay_file43_stage") is not None)
    previous += len(original.get("overlay_file12_stages", []))
    previous += int(original.get("overlay_file12_stage") is not None)
    if previous != OLD_FUNCTIONS:
        raise ValueError(f"Existing manifest contains {previous} claims, not pinned {OLD_FUNCTIONS}")
    result = copy.deepcopy(original)
    result["overlay_file11_stage"] = dict(STAGE)
    return result


def verify_g2_report(proof: dict, expected_names: set[str]) -> dict:
    """Check fresh complete central verifier, not the older scratch-overlay proof."""
    if proof.get("format") != "goemon-matching-build-result-v1" or proof.get("status") != "matched":
        raise ValueError("Central verifier did not report matched status")
    if proof.get("stage") != "complete":
        raise ValueError("Central verifier did not finish its final stage")
    c = proof.get("comparison") or {}
    checks = {
        "full_rom_match": True,
        "expected_sha1": ORIGINAL_SHA1,
        "candidate_sha1": ORIGINAL_SHA1,
        "rom_size": ORIGINAL_ROM_BYTES,
        "matched_functions": TOTAL_FUNCTIONS,
        "claimed_functions": TOTAL_FUNCTIONS,
        "matched_function_bytes": TOTAL_BYTES,
    }
    for key, expected in checks.items():
        if c.get(key) != expected or type(c.get(key)) is not type(expected):
            raise ValueError(f"Central G2 comparison {key} expected {expected!r}, got {c.get(key)!r}")
    source_rows = c.get("functions")
    if not isinstance(source_rows, list) or len(source_rows) != TOTAL_FUNCTIONS:
        raise ValueError("Full G2 lacks the exact 210 function comparison rows")
    names = [x.get("name") for x in source_rows if isinstance(x, dict)]
    if len(set(names)) != TOTAL_FUNCTIONS or any(x.get("matched") is not True for x in source_rows):
        raise ValueError("G2 function rows have duplicates or unmatched entries")
    if not expected_names.issubset(names):
        raise ValueError("G2 did not include all 50 original file_11 C function names")
    stage = proof.get("overlay_file11_stage") or {}
    if stage.get("stage") != STAGE["format"]:
        raise ValueError("G2 did not use the reviewed file_11 stage")
    fields = {
        "total_overlay_c_functions": NEW_FUNCTIONS,
        "total_overlay_c_bytes": NEW_BYTES,
        "ordered_linker_objects": 12,
        "rom_bytes": ORIGINAL_ROM_BYTES,
        "rom_sha1": ORIGINAL_SHA1,
        "relocations": EXPECTED_RELOCATIONS,
    }
    for key, expected in fields.items():
        if stage.get(key) != expected:
            raise ValueError(f"Linked file_11 {key} identity differs from pinned stage")
    # The relocation multiset is already checked by stage.verify(); original
    # order is an additional deliberate invariant of this particular promotion.
    if stage.get("relocations_same_order") is True:
        if (stage.get("relocation_order_equivalence")!="identical" or
                stage.get("reordered_relocations")!=0):
            raise ValueError("File_11 identical relocation order lacks independent proof")
    elif (stage.get("relocation_order_equivalence")!="known_3_record_permutation" or
          stage.get("reordered_relocations")!=3):
        raise ValueError("Unverified file_11 relocation order change")
    pinned = {
        name: (rom, size, original_hash)
        for name, rom, size, original_hash in overlay_file11.FUNCTIONS
    }
    noop_hash = sha256(usa_file11_noop_groups.ORIGINAL_NOOP)
    pinned.update({name: (rom, 12, noop_hash)
                   for name, rom in usa_file11_noop_groups.entries()})
    if set(pinned) != expected_names:
        raise ValueError("Pinned function signatures differ from the 50 expected entries")
    by_name = {x["name"]: x for x in source_rows}
    for name, (rom, size, hash_value) in pinned.items():
        row = by_name[name]
        expected_row = {
            "size": size,
            "rom_offset": f"0x{rom:X}",
            "guest_address": f"0x{overlay_file11.VMA_START + rom - overlay_file11.ROM_START:08X}",
            "expected_sha256": hash_value,
            "candidate_sha256": hash_value,
        }
        for key, expected in expected_row.items():
            if row.get(key) != expected:
                raise ValueError(f"file_11 original identity {key} changed for {name}")
    return {"g2_functions": TOTAL_FUNCTIONS, "g2_bytes": TOTAL_BYTES,
            "file11_new_functions": NEW_FUNCTIONS, "file11_new_bytes": NEW_BYTES,
            "rom_sha1": ORIGINAL_SHA1, "file11_relocations": EXPECTED_RELOCATIONS}


def verify_inventory_report(inventory: dict) -> dict:
    if inventory.get("format") != "goemon-function-inventory-v1":
        raise ValueError("Inventory report uses an unexpected format")
    if inventory.get("decompressed_sha1") != ORIGINAL_SHA1:
        raise ValueError("Inventory is not tied to the authenticated USA ROM")
    summary = inventory.get("summary") or {}
    required = {
        "identified_function_entries": EXPECTED_ENTRIES,
        "upstream_unmarked_entries": 13,
        "newly_matching_c": TOTAL_FUNCTIONS,
        "current_unmarked_entries": 13 + TOTAL_FUNCTIONS,
        "remaining_assembly_entries": EXPECTED_ENTRIES - 13 - TOTAL_FUNCTIONS,
    }
    for key, expected in required.items():
        if summary.get(key) != expected:
            raise ValueError(f"Candidate inventory {key} expected {expected}, got {summary.get(key)}")
    return dict(required)


def write_exclusive(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:
        f.write(content)


def invoke(cmd: list[str], cwd: Path, log_path: Path) -> None:
    """Preserve logs and refuse prior report paths; never hide subprocess errors."""
    with log_path.open("x", encoding="utf-8") as log:
        subprocess.run(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, check=True)


def promote(args: argparse.Namespace) -> Path:
    source_dir = args.source_dir.resolve()
    canonical = source_dir / "manifest.json"
    if not canonical.is_file():
        raise ValueError("Missing canonical decomp/manifest.json: GitHub checkout must be local")
    if args.workdir.exists():
        raise ValueError("Fresh central G2 workdir already exists: " + str(args.workdir))
    output = args.output_dir.resolve()
    repo_root = source_dir.parent
    if output.is_relative_to(repo_root) or args.workdir.resolve().is_relative_to(repo_root):
        raise ValueError("G2 workdir and promotion proofs must be outside the tracked repository")
    if output.exists():
        raise ValueError("Review output directory already exists; never overwrite promotion proof")
    canonical_bytes = canonical.read_bytes()
    review = candidate_manifest(json.loads(canonical_bytes))
    expected_names = expected_file11_names()
    output.mkdir(parents=True)
    candidate = output / "manifest.file11-v2.review.json"
    write_exclusive(candidate, (json.dumps(review, indent=2) + "\n").encode())
    g2 = output / "full-central-g2.json"
    inv = output / "full-central-inventory.json"
    repo_root = source_dir.parent
    command = [sys.executable, "-m", "decomp.verify",
               "--upstream", str(args.upstream.resolve()),
               "--workdir", str(args.workdir.resolve()),
               "--retail-rom", str(args.retail_rom.resolve()),
               "--report", str(g2),
               "--manifest", str(candidate),
               "--source-dir", str(source_dir),
               "--uv", args.uv, "--jobs", str(args.jobs)]
    if args.baseline_cache:
        command.extend(("--baseline-cache", str(args.baseline_cache.resolve())))
    if args.binutils_root:
        command.extend(("--binutils-root", str(args.binutils_root.resolve())))
    invoke(command, repo_root, output / "central-verifier.log")
    verified = verify_g2_report(json.loads(g2.read_text()), expected_names)
    baseline = args.baseline_cache.resolve() if args.baseline_cache else args.workdir.resolve() / "baseline"
    inventory_command = [sys.executable, "-m", "decomp.inventory",
                         "--baseline", str(baseline),
                         "--candidate", str(args.workdir.resolve() / "candidate"),
                         "--report", str(inv), "--manifest", str(candidate)]
    invoke(inventory_command, repo_root, output / "central-inventory.log")
    summary = verify_inventory_report(json.loads(inv.read_text()))
    # This bundle can be reviewed and committed separately. No tracked or
    # canonical production result is changed by the tool itself.
    proof = {
        "format": "goemon-file11-central-promotion-review-v1",
        "status": "ready_for_human_review",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "canonical_manifest_sha256": sha256(canonical_bytes),
        "candidate_manifest_sha256": sha256(candidate.read_bytes()),
        "g2_report_sha256": sha256(g2.read_bytes()),
        "inventory_report_sha256": sha256(inv.read_bytes()),
        "g2": verified,
        "inventory": summary,
        "tracked_repository_files_modified": False,
    }
    write_exclusive(output / "PROMOTION_REVIEW.json", (json.dumps(proof, indent=2) + "\n").encode())
    return output


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-dir", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--upstream", type=Path, required=True)
    p.add_argument("--retail-rom", type=Path, required=True)
    p.add_argument("--workdir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--baseline-cache", type=Path)
    p.add_argument("--binutils-root", type=Path)
    p.add_argument("--uv", default="uv")
    p.add_argument("--jobs", type=int, default=2)
    a = p.parse_args(argv)
    if a.jobs <= 0:
        p.error("--jobs must be positive")
    try:
        output = promote(a)
    except (ValueError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        p.exit(1, f"file_11 promotion NOT verified: {exc}\n")
    print(f"Central 210-function G2 and inventory passed. Review candidate bundle: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())