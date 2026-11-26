#!/usr/bin/env python3
"""Standalone zero-LLM native G2 batch verifier and promoter CLI.

Runs completely outside any LLM conversation loop: executes native IDO 5.3
compilation + negative controls + full 32 MiB/16 MiB ROM link + ELF/relocation/
global/inventory checks on copies of verified regional snapshots, optionally
activates the batch into decomp/batches/registry.json, and emits a compact JSON
receipt (~20 lines) to stdout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import traceback

from decomp import batch_registry as regmod
from decomp import native251_promotion as native
from decomp import usa_short72_promotion as short72
from decomp.consolidated_batch_promotion import (
    FLAGS,
    cright,
    cross,
    exact,
    glitch,
    inventory,
    jp55,
    opening,
    probe,
    splice,
    stage,
)
from decomp.research.wave194_20261125.prefix_stage import stage_with_prefix

sys.path.insert(0, str(Path(stage.ROOT) / "research" / "promo367_20261125"))
from finish367 import finish  # noqa: E402

ALLOWED_SDK_FLAGS = (
    [("-O1" if flag == "-O2" else flag) for flag in FLAGS],
    FLAGS + ["-g3"],
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _run(args: list, cwd: Path, log: Path) -> None:
    with log.open("w") as f:
        subprocess.run([str(x) for x in args], cwd=cwd, stdout=f, stderr=subprocess.STDOUT, check=True)


def run_single_region_trial(
    *,
    region: str,
    checkout: Path,
    pristine: Path,
    manifest_path: Path,
    work: Path,
    namespace: str,
    base_commit: str,
    expected_prior_elf: str,
    uv: str,
    jobs: int,
) -> dict:
    co = checkout.resolve()
    base = pristine.resolve()
    w = work.resolve()
    w.mkdir(parents=True, exist_ok=True)

    manifest_bytes = manifest_path.read_bytes()
    manifest_sha = _sha(manifest_bytes)
    rows = json.loads(manifest_bytes.decode("utf-8"))
    resolved_rows = [
        {**x, **{k: str((manifest_path.resolve().parent / x[k]).resolve()) for k in ("source", "negative_source")}}
        for x in rows
    ]

    bd = co / f"build/{region}"
    elf = bd / "mnsg.elf"
    prior = w / "prior.elf"
    rom = stage.original(co, region)
    report = w / "summary.json"
    d: dict = {
        "region": region,
        "requested": len(resolved_rows),
        "status": "RESEARCH_ONLY",
        "stage": "preflight",
        "native": [],
        "blocked": [],
        "errors": [],
    }
    _write_json(report, d)

    try:
        assert _sha(elf.read_bytes()) == expected_prior_elf, "canonical predecessor ELF hash mismatch"
        assert (bd / "mnsg.z64").read_bytes() == rom and stage.original(base, region) == rom, "canonical original ROM mismatch"
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=co, text=True).strip() == "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
        assert _sha((co / "tools/ido-5.3/cc").read_bytes()) == stage.COMPILER_SHA

        shutil.copyfile(elf, prior)
        oldtxt = subprocess.check_output(["readelf", "-Ws", str(prior)], text=True)
        _, oldmarkers = inventory.parse_inventory_symbols(oldtxt)
        targets = {x["name"] for x in resolved_rows}
        assert targets <= oldmarkers and len(targets) == len(resolved_rows), "canonical C collision or missing ASM marker"

        for x in resolved_rows:
            assert x["region"] == region
            assert x["flags"] == FLAGS or (x.get("nonstandard_sdk_flags") and x["flags"] in ALLOWED_SDK_FLAGS)
            assert _sha(Path(x["source"]).read_bytes()) == x["source_sha256"]
            assert _sha(Path(x["negative_source"]).read_bytes()) == x["negative_sha256"]
            assert _sha(rom[x["rom_offset"] : x["rom_offset"] + x["original_bytes"]]) == x["code_sha256"]

        ledger = Path(stage.ROOT) / "COMPILER_QUIRKS.md"
        ledger.read_text()
        d["ledger_sha256"] = _sha(ledger.read_bytes())
        d["prior_elf_sha256"] = expected_prior_elf
        d["stage"] = "owner_integration"
        _write_json(report, d)

        doc = stage_with_prefix(co, region, candidates=resolved_rows, namespace=namespace)
        d["blocked"] = doc["blocked"]
        d["staged"] = len(doc["functions"])
        d["fragments"] = len(doc["fragments"])
        d["parents"] = len(doc["parents"])
        _write_json(report, d)
        assert not doc["blocked"] and len(doc["functions"]) == len(resolved_rows), "active ASM staging blocked"

        ld = (co / f".splat/{region}/mnsg.ld").read_text()
        d["stage"] = "native_objects"
        _write_json(report, d)
        if doc["fragments"]:
            stage.runmake(co, region, ld, [f"build/{region}/{x['path']}.o" for x in doc["fragments"]], w / "make.log", uv, jobs)

        for f in doc["functions"]:
            n = f["name"]
            off = f["rom_offset"]
            z = f["original_bytes"]
            obj = bd / (f["staged_path"] + ".o")
            owner = base / f"asm/{region}" / f["owner"]
            rec: dict = {
                "name": n,
                "offset": off,
                "size": z,
                "source_sha256": f["source_sha256"],
                "outcome": "NO_NEW_COMPILER_FINDING",
                "prior_research_outcome": f["compiler_quirk_outcome"],
            }
            try:
                probe.get_original_splat_lines(owner, n, off, f["vma"], z, rom[off : off + z])
                raw = owner.read_text()
                ms = list(jp55.BLOCK.finditer(raw))
                matches = [m for m in ms if m["name"] == n]
                assert len(matches) == 1, "reference source boundary"
                m = matches[0]
                src = w / (n + ".ref.s")
                ref = w / (n + ".ref.o")
                header = raw[: ms[0].start()]
                header = header if ".include" in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
                src.write_text(header + raw[m.start() : m.end()] + "\n")
                _run(["mips-linux-gnu-as", "-EB", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-Iinclude", "-I.", "-o", ref, src], co, w / (n + ".as.log"))

                inc = Path(stage.ROOT).parent / f["include_dir"]
                assert inc.is_dir()
                obj.parent.mkdir(parents=True, exist_ok=True)
                _run([co / "tools/ido-5.3/cc", *f["flags"], "-I" + str(inc), "-o", obj, co / f["staged_path"]], co, w / (n + ".compile.log"))
                rec["native_exact"] = exact(obj, ref, f)
                assert rec["native_exact"], "original object instructions, relocation or extent mismatch"
                glitch.check_nontext(obj)
                cross._trim_object(obj, z, rom[off : off + z])

                bad = w / (n + ".negative.o")
                _run([co / "tools/ido-5.3/cc", *f["flags"], "-I" + str(inc), "-o", bad, Path(f["negative_source"])], co, w / (n + ".negative.log"))
                rec["negative_rejected"] = not exact(bad, ref, f)
                assert rec["negative_rejected"], "negative unexpectedly exact"

                if f.get("nonstandard_sdk_flags"):
                    default_o = w / (n + ".default.o")
                    _run([co / "tools/ido-5.3/cc", *FLAGS, "-I" + str(inc), "-o", default_o, co / f["staged_path"]], co, w / (n + ".default.log"))
                    rec["default_flags_rejected"] = not exact(default_o, ref, f)
                    assert rec["default_flags_rejected"], "default flags also exact; use standard flags"
                rec["flags"] = f["flags"]
            except (ValueError, AssertionError, KeyError, OSError, subprocess.CalledProcessError) as exc:
                rec["error"] = str(exc)
            d["native"].append(rec)
            _write_json(report, d)

        for f in doc["fragments"]:
            path = bd / (f["path"] + ".o")
            lo, hi = f["start"], f["end"]
            try:
                if f["suffix"] == ".text.archive61":
                    splice._trim_archive_asm(path, hi - lo)
                else:
                    cross._trim_object(path, hi - lo, rom[lo:hi])
            except (ValueError, AssertionError, KeyError) as exc:
                d["errors"].append({"fragment": f["path"], "error": str(exc)})
        _write_json(report, d)
        if d["errors"] or any("error" in x for x in d["native"]):
            raise ValueError("Native object or retained ASM fragment gate failed")

        finish(region, co, base, w, uv, jobs, d, doc)
        d.update(
            base_commit=base_commit,
            source_manifest_sha256=manifest_sha,
            compiler_sha256=_sha((co / "tools/ido-5.3/cc").read_bytes()),
            expanded_bytes=33554432,
        )
        _write_json(report, d)
        return d
    except Exception as exc:
        d["errors"].append({"stage": d["stage"], "error": str(exc)})
        _write_json(report, d)
        traceback.print_exc()
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--research-dir", required=True, help="Relative to decomp/, e.g. research/my_batch_20261126")
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--usa-snapshot", type=Path)
    parser.add_argument("--usa-pristine", type=Path)
    parser.add_argument("--jp-snapshot", type=Path)
    parser.add_argument("--jp-pristine", type=Path)
    parser.add_argument("--uv", default="uv")
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--activate", action="store_true", help="Write proofs and register batch in decomp/batches/registry.json")
    parser.add_argument("--date-tag", default="20261126")
    args = parser.parse_args()

    root = regmod.ROOT
    reg = regmod.load_registry(root)
    bdir = root / args.research_dir
    receipt: dict = {"batch_id": args.batch_id, "namespace": args.namespace, "regions": {}}

    entry: dict = {
        "id": args.batch_id,
        "namespace": args.namespace,
        "base_commit": args.base_commit,
        "research_dir": args.research_dir,
    }

    for region, snap, pristine in (
        ("usa", args.usa_snapshot, args.usa_pristine),
        ("japan_0", args.jp_snapshot, args.jp_pristine),
    ):
        manifest_path = bdir / f"{region}-candidates.json"
        if not manifest_path.is_file() or snap is None or pristine is None:
            continue
        prior_elf = reg[f"base_{region}"]["elf_sha256"]
        for prev_b in reg["batches"]:
            if region in prev_b:
                prior_elf = prev_b[region]["elf_sha256"]
        trial_co = args.work / f"{region}-checkout"
        if trial_co.exists():
            shutil.rmtree(trial_co)
        shutil.copytree(snap, trial_co, symlinks=True)
        trial_work = args.work / f"{region}-trial"
        if trial_work.exists():
            shutil.rmtree(trial_work)
        proof = run_single_region_trial(
            region=region,
            checkout=trial_co,
            pristine=pristine,
            manifest_path=manifest_path,
            work=trial_work,
            namespace=args.namespace,
            base_commit=args.base_commit,
            expected_prior_elf=prior_elf,
            uv=args.uv,
            jobs=args.jobs,
        )
        rows = json.loads(manifest_path.read_text())
        proof_rel = f"results/{region}_{args.batch_id}_g2_{args.date_tag}.json"
        sdk_flags = {r["name"]: r["flags"] for r in rows if r.get("nonstandard_sdk_flags")}
        entry[region] = {
            "added": len(rows),
            "bytes": sum(r["original_bytes"] for r in rows),
            "manifest_sha256": _sha(manifest_path.read_bytes()),
            "prior_elf_sha256": prior_elf,
            "elf_sha256": proof["candidate_elf_sha256"],
            "guarded_abs": sorted([x["object"], x["symbol"]] for x in proof["guarded_abs_restorations"]),
            "proof": proof_rel,
            "sdk_flags": sdk_flags,
        }
        if args.activate:
            _write_json(root / proof_rel, proof)
        receipt["regions"][region] = {
            "status": proof["status"],
            "added": len(rows),
            "bytes": sum(r["original_bytes"] for r in rows),
            "elf_sha256": proof["candidate_elf_sha256"],
            "expanded_rom_exact": proof["expanded_rom_exact"],
            "retail_exact": proof["retail_exact"],
            "guarded_abs": len(proof["guarded_abs_restorations"]),
        }

    if args.activate:
        # Freeze promo36 base ONCE on first batch activation
        if not reg["batches"]:
            if "usa" in entry:
                for kind, src in (
                    ("manifest", root / "manifest.json"),
                    ("combined", root / "results/combined.json"),
                    ("inventory", root / "results/inventory.json"),
                ):
                    dst = root / "results" / f"{kind}_3087_before_registry.json"
                    if not dst.exists():
                        shutil.copyfile(src, dst)
                reg["frozen_usa_before_registry"] = {
                    k: _sha((root / "results" / f"{k}_3087_before_registry.json").read_bytes())
                    for k in ("manifest", "combined", "inventory")
                }
                if not reg.get("predecessor_verifier_sha"):
                    reg["predecessor_verifier_sha"] = _sha((root / "verify.py").read_bytes())
            if "japan_0" in entry:
                jp_dst = root / "results/japan_0_3019_before_registry.json"
                if not jp_dst.exists():
                    shutil.copyfile(root / "regions/japan_0.json", jp_dst)
                reg["frozen_jp_before_registry_sha256"] = _sha(jp_dst.read_bytes())

        reg["batches"].append(entry)
        _write_json(root / regmod.REGISTRY_PATH, reg)

        if "usa" in entry:
            m = regmod.frozen_usa("manifest", root)
            m[regmod.KEY] = {"format": regmod.FORMAT, "batches": [b["id"] for b in regmod.usa_batches(root)]}
            _write_json(root / "manifest.json", m)
            combined, inv = regmod.usa_documents(root)
            (root / "results/combined.json").write_text(json.dumps(combined, separators=(",", ":")) + "\n")
            _write_json(root / "results/inventory.json", inv)

        if "japan_0" in entry:
            jp_m = regmod.read(root / "results/japan_0_3019_before_registry.json")
            jp_m[regmod.JP_KEY] = regmod.jp_head(root)
            _write_json(root / "regions/japan_0.json", jp_m)

        receipt["activated"] = True
        receipt["usa_totals"] = regmod.expected_totals("usa", root)
        receipt["japan_0_totals"] = regmod.expected_totals("japan_0", root)

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
