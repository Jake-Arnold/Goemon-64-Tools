"""Unified data-driven additive batch promoter and fail-closed validator.

Replaces one-off per-batch promotion modules for all promotions after
promo36_promotion (USA 3,087 / Japan 3,019). Every batch is declared in
decomp/batches/registry.json and must satisfy the exact same native IDO,
full-ROM, ELF, relocation, global, ownership, and strict inventory gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from . import consolidated_batch_promotion as native
from . import promo36_promotion as base_stage

ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = Path("batches/registry.json")
FORMAT = "goemon-batch-registry-v1"
KEY = "usa_batch_registry"
JP_KEY = "batch_registry_promotion"
ALLOWED_OUTCOMES = (
    "EXISTING_QUIRK_REPRODUCED",
    "EXISTING_QUIRK_NOT_APPLICABLE",
    "NEW_REPRODUCIBLE_QUIRK",
    "NO_NEW_COMPILER_FINDING",
)
ALLOWED_NONSTANDARD_FLAGS = (
    [("-O1" if flag == "-O2" else flag) for flag in native.FLAGS],
    native.FLAGS + ["-g3"],
)


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError("BatchRegistry: " + msg)


sha = base_stage.sha
read = base_stage.read
write = base_stage.write


def load_registry(root: Path = ROOT) -> dict:
    reg = read(root / REGISTRY_PATH)
    need(reg.get("format") == FORMAT, "registry format mismatch")
    need(reg.get("base_stage") == "promo36_promotion", "unexpected base stage")
    need(reg["base_usa"]["accepted_C"] == 3087 and reg["base_usa"]["accepted_original_bytes"] == 212412, "USA base drift")
    need(reg["base_japan_0"]["accepted_C"] == 3019 and reg["base_japan_0"]["accepted_original_bytes"] == 202176, "JP base drift")
    seen_ids: set[str] = set()
    seen_ns: set[str] = set()
    for b in reg.get("batches", []):
        bid = b["id"]
        ns = b["namespace"]
        need(bool(re.fullmatch(r"[a-z0-9_]+", bid)) and bid not in seen_ids, f"invalid/duplicate batch id {bid}")
        need(bool(re.fullmatch(r"[a-z0-9_]+", ns)) and ns not in seen_ns, f"invalid/duplicate namespace {ns}")
        seen_ids.add(bid)
        seen_ns.add(ns)
        need("usa" in b or "japan_0" in b, f"batch {bid} has no regions")
    return reg


def expected_totals(region: str, root: Path = ROOT) -> tuple[int, int, int]:
    """Return (accepted_C, accepted_original_bytes, remaining_assembly) from registry."""
    reg = load_registry(root)
    base = reg[f"base_{region}"]
    total_c = base["accepted_C"]
    total_bytes = base["accepted_original_bytes"]
    for b in reg["batches"]:
        cfg = b.get(region)
        if cfg:
            total_c += cfg["added"]
            total_bytes += cfg["bytes"]
    remaining = 7376 - (total_c + base["upstream_unmarked"])
    return total_c, total_bytes, remaining


def expected_usa_totals(root: Path = ROOT) -> tuple[int, int]:
    c, b, _ = expected_totals("usa", root)
    return c, b


def batch_rows(batch: dict, region: str, root: Path = ROOT, rom: bytes | None = None) -> list[dict]:
    cfg = batch[region]
    batch_dir = root / batch["research_dir"]
    manifest_path = batch_dir / f"{region}-candidates.json"
    need(sha(manifest_path.read_bytes()) == cfg["manifest_sha256"], f"{batch['id']} {region} manifest drift")
    rr = read(manifest_path)
    need((len(rr), sum(f["original_bytes"] for f in rr)) == (cfg["added"], cfg["bytes"]), f"{batch['id']} {region} count/bytes")
    names: set[str] = set()
    spans: list[tuple[int, int]] = []
    sdk_flags = cfg.get("sdk_flags", {})
    for f in rr:
        n = f["name"]
        a = f["rom_offset"]
        z = f["original_bytes"]
        v = f["vma"]
        need(
            f["region"] == region
            and n not in names
            and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", n) is not None
            and type(v) is int
            and a >= 0
            and z > 0
            and a % 4 == z % 4 == 0
            and a + z <= 33554432,
            f"identity {n}",
        )
        if n.startswith("func_"):
            need(n == f"func_{v:08X}_{a:X}", f"address/name {n}")
        expected_flags = sdk_flags.get(n, native.FLAGS)
        need(f["flags"] == expected_flags, f"flags {n}")
        if n in sdk_flags:
            need(f["flags"] in ALLOWED_NONSTANDARD_FLAGS and f.get("nonstandard_sdk_flags") is True, f"sdk flags {n}")
        else:
            need(not f.get("nonstandard_sdk_flags"), f"unexpected nonstandard flag {n}")
        need(f["compiler_quirk_outcome"] in ALLOWED_OUTCOMES, f"compiler outcome {n}")
        inc = (root.parent / f["include_dir"]).resolve()
        need(inc.is_relative_to(root.resolve()) and inc.is_dir(), f"include_dir {n}")
        for key, hkey, fname in (("source", "source_sha256", "candidate.c"), ("negative_source", "negative_sha256", "negative.c")):
            src_rel = f[key]
            need(src_rel.endswith("/" + fname) and sha((batch_dir / src_rel).read_bytes()) == f[hkey], f"source drift {n} {key}")
        if "headers_sha256" in f:
            actual_hdrs = {p.name: sha(p.read_bytes()) for p in sorted((batch_dir / f["source"]).parent.glob("*.h"))}
            need(f["headers_sha256"] == actual_hdrs, f"header drift {n}")
        need(f["source_sha256"] != f["negative_sha256"] and re.fullmatch(r"[a-f0-9]{64}", f["code_sha256"]) is not None, f"control/code {n}")
        if rom is not None:
            need(sha(rom[a : a + z]) == f["code_sha256"], f"original code mismatch {n}")
        names.add(n)
        spans.append((a, a + z))
    spans.sort()
    need(all(x[1] <= y[0] for x, y in zip(spans, spans[1:])), f"candidate overlap in {batch['id']} {region}")
    return rr


def frozen_usa(kind: str, root: Path = ROOT) -> dict:
    reg = load_registry(root)
    frozen = reg["frozen_usa_before_registry"]
    p = root / "results" / f"{kind}_3087_before_registry.json"
    need(sha(p.read_bytes()) == frozen[kind], f"frozen USA base {kind} drift")
    return read(p)


def usa_batches(root: Path = ROOT) -> list[dict]:
    return [b for b in load_registry(root)["batches"] if "usa" in b]


def jp_batches(root: Path = ROOT) -> list[dict]:
    return [b for b in load_registry(root)["batches"] if "japan_0" in b]


def claims(root: Path = ROOT) -> list[dict]:
    out: list[dict] = []
    for b in usa_batches(root):
        for f in batch_rows(b, "usa", root):
            out.append({"name": f["name"], "rom_offset": f["rom_offset"], "vma": f["vma"], "size": f["original_bytes"]})
    return out


def source_hashes(root: Path = ROOT) -> dict[str, str]:
    out: dict[str, str] = {}
    for b in usa_batches(root):
        bdir = Path(b["research_dir"])
        for f in batch_rows(b, "usa", root):
            out[str(bdir / f["source"])] = f["source_sha256"]
    return out


def predecessor(m: dict, root: Path = ROOT, rom: bytes | None = None) -> list[dict]:
    from .verify import claimed_functions

    reg = load_registry(root)
    batches = usa_batches(root)
    need(bool(batches), "usa_batch_registry active with zero registered USA batches")
    old = frozen_usa("manifest", root)
    expected_head = {"format": FORMAT, "batches": [b["id"] for b in batches]}
    need(m.get(KEY) == expected_head and old == {k: v for k, v in m.items() if k != KEY}, "USA registry manifest drift")
    before = claimed_functions(old)
    need((len(before), sum(x["size"] for x in before)) == (3087, 212412), "USA base predecessor count")
    if rom is not None:
        need(len(rom) == 33554432 and hashlib.sha1(rom).hexdigest() == reg["base_usa"]["rom_sha1"], "USA ROM mismatch")
    seen_names = {x["name"] for x in before} | set(frozen_usa("inventory", root)["summary"]["upstream_unmarked_names"])
    seen_spans = [(x["rom_offset"], x["rom_offset"] + x["size"]) for x in before]
    for b in batches:
        for f in batch_rows(b, "usa", root, rom):
            a = f["rom_offset"]
            end = a + f["original_bytes"]
            need(f["name"] not in seen_names, f"duplicate USA name {f['name']}")
            need(not any(lo < end and a < hi for lo, hi in seen_spans), f"overlapping USA span {f['name']}")
            seen_names.add(f["name"])
            seen_spans.append((a, end))
    return before


def validate_native_proof(
    batch: dict,
    region: str,
    proof: dict,
    prior_names: set[str],
    prior_elf: str,
    base_cfg: dict,
    root: Path = ROOT,
) -> dict:
    cfg = batch[region]
    fs = batch_rows(batch, region, root)
    byname = {f["name"]: f for f in fs}
    old = len(prior_names)
    n = cfg["added"]
    new = old + n
    need(not (set(byname) & prior_names), f"{batch['id']} {region} predecessor ownership collision")
    expected = {
        "region": region,
        "requested": n,
        "stage": "completed_trial",
        "base_commit": batch["base_commit"],
        "source_manifest_sha256": cfg["manifest_sha256"],
        "compiler_sha256": native.stage.COMPILER_SHA,
        "prior_elf_sha256": prior_elf,
        "candidate_elf_sha256": cfg["elf_sha256"],
        "expanded_sha1": base_cfg["rom_sha1"],
        "expanded_bytes": 33554432,
        "retail_sha1": base_cfg["retail_sha1"],
        "function_identities": 7376,
        "semantic_relocations_before": cfg.get("relocs_before", base_cfg["relocs"]),
        "semantic_relocations_after": cfg.get("relocs_after", base_cfg["relocs"]),
        "semantic_relocation_sha256": cfg.get("relocation_sha", base_cfg["relocation_sha"]),
        "stable_globals": base_cfg["globals"],
        "observed_new_ownership": n,
        "status": "PASSED_G2_LOCAL",
        "staged": n,
    }
    for k, v in expected.items():
        need(proof.get(k) == v, f"{batch['id']} {region} proof field {k}")
    for k in ("expanded_rom_exact", "retail_exact", "function_identity_exact", "globals_exact", "ownership_exact", "semantic_relocations_exact"):
        need(proof.get(k) is True, f"{batch['id']} {region} native gate {k} failed")
    for k in ("errors", "blocked", "function_removed", "function_added", "relocations_added", "relocations_removed", "globals_removed", "globals_added"):
        need(proof.get(k) == [], f"{batch['id']} {region} discrepancy {k}")
    need(proof.get("first_rom_mismatch") is None, f"{batch['id']} {region} rom mismatch")
    need(len(proof["native"]) == n and {x["name"] for x in proof["native"]} == set(byname), f"{batch['id']} {region} native records")
    for x in proof["native"]:
        f = byname[x["name"]]
        need(
            x.get("native_exact") is True
            and x.get("negative_rejected") is True
            and "error" not in x
            and (x["offset"], x["size"], x["source_sha256"], x["prior_research_outcome"])
            == (f["rom_offset"], f["original_bytes"], f["source_sha256"], f["compiler_quirk_outcome"]),
            f"{batch['id']} {region} native control {f['name']}",
        )
        if f.get("nonstandard_sdk_flags"):
            need(x.get("default_flags_rejected") is True, f"{batch['id']} {region} sdk default control {f['name']}")
    expected_abs = sorted(tuple(pair) for pair in cfg.get("guarded_abs", []))
    actual_abs = sorted((x["object"], x["symbol"]) for x in proof["guarded_abs_restorations"])
    need(actual_abs == expected_abs, f"{batch['id']} {region} guarded ABS mismatch: {actual_abs} != {expected_abs}")
    need(
        all(
            x["code_and_relocations_unchanged"] is True
            and x["st_info_bytes_changed"] == 1
            and x["compiler_outcome"] == "EXISTING_QUIRK_REPRODUCED"
            for x in proof["guarded_abs_restorations"]
        ),
        f"{batch['id']} {region} ABS metadata evidence",
    )
    inv = proof["strict_inventory"]
    need(
        (
            inv["identified_function_entries"],
            inv["upstream_unmarked_entries"],
            inv["newly_matching_c"],
            inv["current_unmarked_entries"],
            inv["remaining_assembly_entries"],
            inv["extra_positive_alias_entries"],
            inv["size_annotation_differences"],
            inv["function_entry_identity_sha256"],
        )
        == (7376, old, n, new, 7376 - new, 0, [], base_cfg["identity"]),
        f"{batch['id']} {region} strict inventory mismatch",
    )
    need(set(inv["upstream_unmarked_names"]) == prior_names and len(inv["upstream_unmarked_names"]) == old, f"{batch['id']} {region} prior names mismatch")
    return proof


def _project_usa_batch(batch: dict, proof: dict, report: dict, root: Path = ROOT) -> None:
    fs = batch_rows(batch, "usa", root)
    c = report["comparison"]
    c["functions"] += [
        {
            "name": f["name"],
            "size": f["original_bytes"],
            "guest_address": f"0x{f['vma']:08X}",
            "rom_offset": f"0x{f['rom_offset']:X}",
            "matched": True,
            "expected_sha256": f["code_sha256"],
            "candidate_sha256": f["code_sha256"],
        }
        for f in fs
    ]
    c["matched_functions"] += len(fs)
    c["claimed_functions"] += len(fs)
    c["matched_function_bytes"] += sum(f["original_bytes"] for f in fs)
    bdir = Path(batch["research_dir"])
    report["sources_sha256_lf"].update({str(bdir / f["source"]): f["source_sha256"] for f in fs})
    added_names = {f["name"] for f in fs}
    report["retained_assembly_functions"] = [n for n in report["retained_assembly_functions"] if n not in added_names]
    report.setdefault(KEY, {})[batch["id"]] = proof


def usa_documents(root: Path = ROOT) -> tuple[dict, dict]:
    from .verify import claimed_functions

    reg = load_registry(root)
    batches = usa_batches(root)
    out = frozen_usa("combined", root)
    inv = frozen_usa("inventory", root)
    prior_names = {x["name"] for x in claimed_functions(frozen_usa("manifest", root))} | set(inv["summary"]["upstream_unmarked_names"])
    prior_elf = reg["base_usa"]["elf_sha256"]
    total_c = reg["base_usa"]["accepted_C"]
    upstream = reg["base_usa"]["upstream_unmarked"]
    for b in batches:
        proof = read(root / b["usa"]["proof"])
        validate_native_proof(b, "usa", proof, prior_names, prior_elf, reg["base_usa"], root)
        _project_usa_batch(b, proof, out, root)
        prior_names |= {f["name"] for f in batch_rows(b, "usa", root)}
        prior_elf = b["usa"]["elf_sha256"]
        total_c += b["usa"]["added"]
    out["verifier_source_sha256_lf"] = sha((root / "verify.py").read_bytes())
    inv["candidate_elf_sha256"] = prior_elf
    inv["summary"].update(newly_matching_c=total_c, current_unmarked_entries=total_c + upstream, remaining_assembly_entries=7376 - (total_c + upstream))
    return out, inv


def audit_usa(root: Path, m: dict, p: dict, i: dict) -> dict:
    try:
        reg = load_registry(root)
        hist_vsha = reg.get("predecessor_verifier_sha")
        need(
            base_stage.audit_usa(root, frozen_usa("manifest", root), frozen_usa("combined", root), frozen_usa("inventory", root), historical_verifier_sha=hist_vsha)["status"] == "PASS",
            "historical USA3087 integrity",
        )
        predecessor(m, root)
        expected_out, expected_inv = usa_documents(root)
        need(
            p["status"] == "matched"
            and all(p[k] == expected_out[k] for k in ("comparison", "sources_sha256_lf", "retained_assembly_functions", "verifier_source_sha256_lf", KEY)),
            "canonical USA registry proof drift",
        )
        need(i == expected_inv, "canonical USA registry inventory drift")
        c, b, rem = expected_totals("usa", root)
        return {"status": "PASS", "accepted_C": c, "accepted_original_bytes": b, "remaining_assembly": rem, "errors": []}
    except (KeyError, ValueError, TypeError, FileNotFoundError) as exc:
        return {"status": "FAIL", "errors": [str(exc)]}


def run_native_batch(batch: dict, region: str, co: Path, pristine: Path, work: Path, uv: str = "uv", jobs: int = 4) -> dict:
    need(__debug__, "assertions required")
    from .run_promotion import run_single_region_trial

    bdir = ROOT / batch["research_dir"]
    manifest = bdir / f"{region}-candidates.json"
    proof = run_single_region_trial(
        region=region,
        checkout=co,
        pristine=pristine,
        manifest_path=manifest,
        work=work,
        namespace=batch["namespace"],
        base_commit=batch["base_commit"],
        expected_prior_elf=batch[region]["prior_elf_sha256"],
        uv=uv,
        jobs=jobs,
    )
    return proof


def apply(co: Path, base: Path, work: Path, uv: str, jobs: int, m: dict, report: dict, rom: bytes) -> None:
    predecessor(m, rom=rom)
    c = report["comparison"]
    need(c["full_rom_match"] and (c["matched_functions"], c["matched_function_bytes"]) == (3087, 212412), "fresh USA3087 predecessor report")
    reg = load_registry(ROOT)
    prior_names = {x["name"] for x in predecessor(m)} | set(frozen_usa("inventory")["summary"]["upstream_unmarked_names"])
    prior_elf = reg["base_usa"]["elf_sha256"]
    for b in usa_batches(ROOT):
        proof = run_native_batch(b, "usa", co, base, Path(work) / f"registry_{b['id']}", uv, jobs)
        validate_native_proof(b, "usa", proof, prior_names, prior_elf, reg["base_usa"], ROOT)
        _project_usa_batch(b, proof, report, ROOT)
        prior_names |= {f["name"] for f in batch_rows(b, "usa", ROOT)}
        prior_elf = b["usa"]["elf_sha256"]


def jp_head(root: Path = ROOT) -> dict:
    batches = jp_batches(root)
    c, b, rem = expected_totals("japan_0", root)
    return {
        "format": FORMAT,
        "status": "PASSED_G2_LOCAL",
        "base_original_C": 3019,
        "new_original_C": c - 3019,
        "accepted_original_C": c,
        "accepted_original_bytes": b,
        "asm_remaining": rem,
        "full_original_elf_identities": 7376,
        "registry": "decomp/" + REGISTRY_PATH.as_posix(),
        "batches": [x["id"] for x in batches],
    }


def master_predecessor(m: dict, root: Path = ROOT) -> dict:
    reg = load_registry(root)
    path = root / "results/japan_0_3019_before_registry.json"
    need(sha(path.read_bytes()) == reg["frozen_jp_before_registry_sha256"], "JP frozen predecessor fingerprint")
    old = read(path)
    need(m.get(JP_KEY) == jp_head(root) and {k: v for k, v in m.items() if k != JP_KEY} == old, "JP3019 frozen predecessor mismatch")
    return old


def validate_jp(root: Path = ROOT) -> dict:
    reg = load_registry(root)
    need(base_stage.validate_jp(root)["accepted_C"] == 3019, "historical JP3019 integrity")
    batches = jp_batches(root)
    if not batches:
        return {"status": "PASS", "accepted_C": 3019, "accepted_original_bytes": 202176, "remaining_assembly": 4357, "registered_batches": 0}
    master_predecessor(read(root / "regions/japan_0.json"), root)
    base_inv = read(root / "results" / base_stage.JP_INV)
    prior_names = set(base_inv["previous_C_names"]) | set(base_inv["new_C_names"])
    prior_elf = reg["base_japan_0"]["elf_sha256"]
    for b in batches:
        proof = read(root / b["japan_0"]["proof"])
        validate_native_proof(b, "japan_0", proof, prior_names, prior_elf, reg["base_japan_0"], root)
        prior_names |= {f["name"] for f in batch_rows(b, "japan_0", root)}
        prior_elf = b["japan_0"]["elf_sha256"]
    c, b_bytes, rem = expected_totals("japan_0", root)
    return {"status": "PASS", "accepted_C": c, "accepted_original_bytes": b_bytes, "remaining_assembly": rem, "registered_batches": len(batches)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(validate_jp(args.root), indent=2))
