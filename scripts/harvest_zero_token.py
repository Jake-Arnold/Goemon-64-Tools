#!/usr/bin/env python3
"""Zero-token multi-core CPU harvester for Mystical Ninja / Ganbare Goemon 64.

Sweeps remaining ASM functions in verified USA and/or Japan snapshots using
m2c (-t mips-ido-c) + authentic SGI IDO 5.3 + independent pristine Splat
reference comparison (exact instruction bytes + exact named relocations + empty
non-text sections). Auto-generates verified altered-source negative controls for
every exact hit and emits compact 4-8 KB executor task packets for near-misses.

Zero LLM tokens are consumed while scanning thousands of functions.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from decomp import inventory, task_packet
from decomp.consolidated_batch_promotion import FLAGS, exact, glitch, jp55, probe, rels, stage

M2C_TYPES_H = """#ifndef JP_M2C_TYPES_H
#define JP_M2C_TYPES_H
typedef float f32; typedef double f64; typedef signed int M2C_UNK; typedef signed char M2C_UNK8; typedef signed short M2C_UNK16; typedef signed int M2C_UNK32; typedef signed long long M2C_UNK64; typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef long long s64; typedef unsigned long long u64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8*)(expr)+(offset)))
#define M2C_BITWISE(type,expr) ((type)(expr))
#define M2C_LWL(expr) (expr)
#define M2C_FIRST3BYTES(expr) (expr)
#define M2C_UNALIGNED32(expr) (expr)
#define M2C_ERROR(desc) (0)
#define M2C_TRAP_IF(cond) (0)
#define M2C_BREAK() (0)
#define M2C_SYNC() (0)
#define GLUE_F64(a,b) (0.0)
#define MULT_HI(a,b) (0)
#define MULTU_HI(a,b) (0)
#define DMULT_HI(a,b) (0)
#define DMULTU_HI(a,b) (0)
#define CLZ(x) (0)
#define REVERSE_BITS(x) (0)
#define ROTATE_RIGHT(x,shift) (0)
#define ARM_RRX(x,carry) (0)
#define BSWAP32(x) (0)
#define BSWAP16(x) (0)
#define BSWAP16X2(x) (0)
#define M2C_CARRY 0
#define M2C_OVERFLOW(a) (0)
#endif
#ifndef NULL
#define NULL ((void *)0)
#endif
"""

FUNC_NAME_RE = re.compile(r"^func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)$")
DECL_CALL_RE = re.compile(r"^(\s*(?:void|s8|u8|s16|u16|s32|u32|s64|u64|f32|f64|M2C_UNK\w*|void \*)\s+)(func_[0-9A-Fa-f_]+)\([^;]*\);\s*/\*\s*extern\s*\*/$", re.M)


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _read_text_bytes(obj: Path) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".bin") as tmp:
        subprocess.run(
            ["mips-linux-gnu-objcopy", "-O", "binary", "-j", ".text", str(obj), tmp.name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return Path(tmp.name).read_bytes()


def _word_diff(obj: Path, orig: bytes) -> tuple[int, str]:
    cand = _read_text_bytes(obj)
    n_orig = len(orig) // 4
    n_cand = len(cand) // 4
    common = min(n_orig, n_cand)
    diffs = abs(n_orig - n_cand)
    first = ""
    for i in range(common):
        w0 = orig[4 * i : 4 * i + 4]
        w1 = cand[4 * i : 4 * i + 4]
        if w0 != w1:
            diffs += 1
            if not first:
                first = f"word +0x{4*i:X}: orig={w0.hex()} cand={w1.hex()} (orig_bytes={len(orig)} cand_bytes={len(cand)})"
    if not first and n_orig != n_cand:
        first = f"size mismatch: orig_bytes={len(orig)} cand_bytes={len(cand)}"
    return diffs, first


def _make_negative(code: str, name: str) -> list[str]:
    """Generate deterministic C89-safe compiling altered-source negative control candidates."""
    variants: list[str] = []
    last_brace = code.rfind("}")
    if last_brace > 0:
        variants.append(code[:last_brace] + "\n    *(volatile s32 *)0x80000000 = 1;\n" + code[last_brace:])
    fn_m = re.search(rf"\b{re.escape(name)}\s*\([^)]*\)\s*\{{", code)
    if fn_m:
        body_start = fn_m.end()
        ret_m = re.search(r"\breturn\b", code[body_start:])
        if ret_m:
            pos = body_start + ret_m.start()
            variants.append(code[:pos] + "{ *(volatile s32 *)0x80000000 = 1; } " + code[pos:])
    hex_m = re.search(r"\b0x([1-9A-Fa-f][0-9A-Fa-f]*)\b", code)
    if hex_m:
        val = int(hex_m.group(1), 16)
        variants.append(code[: hex_m.start()] + f"0x{val + 1:X}" + code[hex_m.end() :])
    return variants


def _clean_m2c_source(raw: str) -> str:
    return '#include "m2c_types.h"\n' + raw


def _fix_void_ptr_arith(src: str) -> str:
    # IDO 5.3 rejects pointer arithmetic on `void *`; use `u8 *` for byte-offset arithmetic.
    out = re.sub(r"\bextern void \*", "extern u8 *", src)
    out = re.sub(r"\(void \*\)", "(u8 *)", out)
    out = re.sub(r"(?m)^(\s*)void \*(\w+)", r"\1u8 *\2", out)
    return out


def _discover_targets(region: str, snapshot: Path, pristine: Path, max_bytes: int, min_bytes: int) -> list[dict]:
    elf = snapshot / f"build/{region}/mnsg.elf"
    txt = subprocess.check_output(["mips-linux-gnu-readelf", "-Ws", str(elf)], text=True)
    funcs, markers = inventory.parse_inventory_symbols(txt)
    remaining = sorted(markers & set(funcs))

    # Build owner map by scanning pristine asm/<region>/**/*.s
    asm_root = pristine / f"asm/{region}"
    owner_by_name: dict[str, str] = {}
    for s_file in asm_root.rglob("*.s"):
        rel = s_file.relative_to(asm_root).as_posix()
        if rel.startswith("data/"):
            continue
        content = s_file.read_text(errors="ignore")
        for m in jp55.BLOCK.finditer(content):
            fn = m["name"]
            if fn not in owner_by_name:
                owner_by_name[fn] = rel

    targets: list[dict] = []
    for name in remaining:
        m = FUNC_NAME_RE.match(name)
        if not m:
            continue
        size = funcs[name]["size"]
        if size < min_bytes or size > max_bytes:
            continue
        owner = owner_by_name.get(name)
        if not owner:
            continue
        vma = int(m.group(1), 16)
        rom_offset = int(m.group(2), 16)
        targets.append({
            "region": region,
            "name": name,
            "vma": vma,
            "rom_offset": rom_offset,
            "original_bytes": size,
            "owner": owner,
        })
    targets.sort(key=lambda t: (t["original_bytes"], t["rom_offset"]))
    return targets


def _probe_one(task: dict) -> dict:
    region = task["region"]
    name = task["name"]
    off = task["rom_offset"]
    vma = task["vma"]
    size = task["original_bytes"]
    owner_rel = task["owner"]
    pristine = Path(task["pristine"])
    snapshot = Path(task["snapshot"])
    m2c_py = Path(task["m2c_py"])
    rom_path = Path(task["rom_path"])
    flag_kind = task.get("flag_kind", "O2")
    flags = list(FLAGS)
    nonstd = False
    if flag_kind == "O2g3":
        flags = list(FLAGS) + ["-g3"]
        nonstd = True
    elif flag_kind == "O1":
        flags = [("-O1" if x == "-O2" else x) for x in FLAGS]
        nonstd = True

    with tempfile.TemporaryDirectory(prefix=f"h_{name}_") as td:
        w = Path(td)
        owner_path = pristine / f"asm/{region}" / owner_rel
        with rom_path.open("rb") as rf:
            rf.seek(off)
            orig_bytes = rf.read(size)

        try:
            probe.get_original_splat_lines(owner_path, name, off, vma, size, orig_bytes)
        except Exception as exc:
            return {"name": name, "status": "skip_splat", "error": str(exc)}

        raw = owner_path.read_text()
        ms = list(jp55.BLOCK.finditer(raw))
        matches = [m for m in ms if m["name"] == name]
        if len(matches) != 1:
            return {"name": name, "status": "skip_boundary"}
        blk = raw[matches[0].start() : matches[0].end()] + "\n"
        # Skip jump-table / float literal pool functions on Pass-1 pure m2c (handled separately)
        if ".word" in blk or "jtbl_" in blk:
            return {"name": name, "status": "skip_jtbl"}

        header = raw[: ms[0].start()]
        header = header if ".include" in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
        ref_s = w / f"{name}.ref.s"
        ref_o = w / f"{name}.ref.o"
        ref_s.write_text(header + blk)
        as_res = subprocess.run(
            ["mips-linux-gnu-as", "-EB", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-Iinclude", "-I.", "-o", str(ref_o), str(ref_s)],
            cwd=snapshot,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if as_res.returncode != 0:
            return {"name": name, "status": "skip_as"}

        # Run m2c with --valid-syntax for IDO 5.3 C89 compatibility
        m2c_s = w / f"{name}.m2c.s"
        m2c_s.write_text(blk)
        m2c_res = subprocess.run(
            [sys.executable, str(m2c_py), "-t", "mips-ido-c", "--valid-syntax", "--globals", "used", "-f", name, str(m2c_s)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
        if m2c_res.returncode != 0 or not m2c_res.stdout.strip():
            return {"name": name, "status": "m2c_fail"}

        cand_src = _clean_m2c_source(m2c_res.stdout)
        (w / "m2c_types.h").write_text(M2C_TYPES_H)
        cand_c = w / "candidate.c"
        cand_o = w / "candidate.o"
        cand_c.write_text(cand_src)

        cc = snapshot / "tools/ido-5.3/cc"
        cc_res = subprocess.run(
            [str(cc), *flags, "-I" + str(w), "-o", str(cand_o), str(cand_c)],
            cwd=snapshot,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=20,
        )
        if cc_res.returncode != 0 and "Unacceptable operand of" in cc_res.stdout:
            alt_src = _fix_void_ptr_arith(cand_src)
            if alt_src != cand_src:
                cand_src = alt_src
                cand_c.write_text(cand_src)
                cc_res = subprocess.run(
                    [str(cc), *flags, "-I" + str(w), "-o", str(cand_o), str(cand_c)],
                    cwd=snapshot,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=20,
                )
        if cc_res.returncode != 0 or not cand_o.is_file():
            return {"name": name, "status": "compile_fail"}

        rel_count = len(rels(ref_o))
        f_meta = {"name": name, "rom_offset": off, "vma": vma, "original_bytes": size, "relocation_count": rel_count}
        is_exact = False
        try:
            if exact(cand_o, ref_o, f_meta):
                glitch.check_nontext(cand_o)
                if nonstd:
                    def_o = w / "default.o"
                    dr = subprocess.run(
                        [str(cc), *FLAGS, "-I" + str(w), "-o", str(def_o), str(cand_c)],
                        cwd=snapshot,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=20,
                    )
                    if dr.returncode == 0 and def_o.is_file() and exact(def_o, ref_o, f_meta):
                        return {"name": name, "status": "default_also_exact"}
                is_exact = True
        except Exception:
            is_exact = False

        if is_exact:
            # Generate and verify altered-source negative control
            neg_src = None
            for idx, v in enumerate(_make_negative(cand_src, name)):
                neg_c = w / f"neg_{idx}.c"
                neg_o = w / f"neg_{idx}.o"
                neg_c.write_text(v)
                nr = subprocess.run(
                    [str(cc), *flags, "-I" + str(w), "-o", str(neg_o), str(neg_c)],
                    cwd=snapshot,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=20,
                )
                if nr.returncode == 0 and neg_o.is_file():
                    try:
                        if not exact(neg_o, ref_o, f_meta):
                            neg_src = v
                            break
                    except Exception:
                        neg_src = v
                        break
            if neg_src is None:
                return {"name": name, "status": "neg_fail"}
            return {
                "status": "EXACT",
                "region": region,
                "name": name,
                "rom_offset": off,
                "vma": vma,
                "original_bytes": size,
                "owner": owner_rel,
                "code_sha256": _sha(orig_bytes),
                "relocation_count": rel_count,
                "candidate_c": cand_src,
                "negative_c": neg_src,
            }

        # Check if near-miss (<= 6 differing words) for executor task-packet export
        try:
            diff_words, first_diff = _word_diff(cand_o, orig_bytes)
        except Exception:
            return {"name": name, "status": "diff_err"}
        if 1 <= diff_words <= 6:
            return {
                "status": "NEAR_MISS",
                "region": region,
                "name": name,
                "rom_offset": off,
                "vma": vma,
                "original_bytes": size,
                "owner": owner_rel,
                "diff_words": diff_words,
                "first_mismatch": first_diff,
                "asm": blk,
                "m2c_draft": cand_src,
            }
        return {"name": name, "status": "mismatch", "diff_words": diff_words}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", choices=("usa", "japan_0"), required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--pristine", type=Path, required=True)
    parser.add_argument("--m2c", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="Output directory (e.g. decomp/research/harvest_... or scratch)")
    parser.add_argument("--repo-rel-out", default="", help="Path relative to repo root for include_dir (optional)")
    parser.add_argument("--min-bytes", type=int, default=8)
    parser.add_argument("--max-bytes", type=int, default=256)
    parser.add_argument("--limit", type=int, default=0, help="0 = scan all matching targets")
    parser.add_argument("--workers", type=int, default=14)
    parser.add_argument("--max-packets", type=int, default=50, help="Max near-miss executor task packets to write")
    parser.add_argument("--flags", choices=("O2", "O2g3", "O1"), default="O2")
    args = parser.parse_args()

    flag_list = list(FLAGS)
    nonstd = False
    if args.flags == "O2g3":
        flag_list = list(FLAGS) + ["-g3"]
        nonstd = True
    elif args.flags == "O1":
        flag_list = [("-O1" if x == "-O2" else x) for x in FLAGS]
        nonstd = True

    rom_path = args.pristine / f"config/{args.region}/baserom.decompressed.z64"
    targets = _discover_targets(args.region, args.snapshot, args.pristine, args.max_bytes, args.min_bytes)
    if args.limit > 0:
        targets = targets[: args.limit]

    ledger_sha = _sha((REPO_ROOT / "decomp/COMPILER_QUIRKS.md").read_bytes())
    hdr_sha = _sha(M2C_TYPES_H.encode())

    tasks = [
        {
            **t,
            "pristine": str(args.pristine.resolve()),
            "snapshot": str(args.snapshot.resolve()),
            "m2c_py": str(args.m2c.resolve()),
            "rom_path": str(rom_path.resolve()),
            "flag_kind": args.flags,
        }
        for t in targets
    ]

    stats: dict[str, int] = {}
    exact_hits: list[dict] = []
    near_misses: list[dict] = []

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(_probe_one, t) for t in tasks]
        for fut in as_completed(futs):
            res = fut.result()
            st = res["status"]
            stats[st] = stats.get(st, 0) + 1
            if st == "EXACT":
                exact_hits.append(res)
            elif st == "NEAR_MISS":
                near_misses.append(res)

    exact_hits.sort(key=lambda r: r["rom_offset"])
    near_misses.sort(key=lambda r: (r["diff_words"], r["original_bytes"], r["rom_offset"]))

    args.out.mkdir(parents=True, exist_ok=True)
    candidates_manifest: list[dict] = []
    rel_base = args.repo_rel_out.rstrip("/") if args.repo_rel_out else args.out.as_posix()

    for hit in exact_hits:
        n = hit["name"]
        sdir = args.out / "sources" / args.region / n
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "m2c_types.h").write_text(M2C_TYPES_H)
        (sdir / "candidate.c").write_text(hit["candidate_c"])
        (sdir / "negative.c").write_text(hit["negative_c"])
        candidates_manifest.append({
            "region": args.region,
            "name": n,
            "rom_offset": hit["rom_offset"],
            "vma": hit["vma"],
            "original_bytes": hit["original_bytes"],
            "owner": hit["owner"],
            "code_sha256": hit["code_sha256"],
            "source_sha256": _sha(hit["candidate_c"].encode()),
            "negative_sha256": _sha(hit["negative_c"].encode()),
            "flags": flag_list,
            "nonstandard_sdk_flags": nonstd,
            "relocation_count": hit["relocation_count"],
            "include_dir": f"{rel_base}/sources/{args.region}/{n}",
            "compiler_quirk_outcome": "NO_NEW_COMPILER_FINDING",
            "ledger_sha256": ledger_sha,
            "source": f"sources/{args.region}/{n}/candidate.c",
            "negative_source": f"sources/{args.region}/{n}/negative.c",
            "origin": f"zero-token m2c+IDO ({args.flags}) CPU harvester",
            "headers_sha256": {"m2c_types.h": hdr_sha},
        })

    (args.out / f"{args.region}-candidates.json").write_text(json.dumps(candidates_manifest, indent=2) + "\n")

    # Export top near-miss minimal task packets for cheap executors
    pkt_dir = args.out / "task_packets" / args.region
    pkt_dir.mkdir(parents=True, exist_ok=True)
    for nm in near_misses[: args.max_packets]:
        pkt = task_packet.build_task_packet(
            region=args.region,
            name=nm["name"],
            rom_offset=nm["rom_offset"],
            vma=nm["vma"],
            size=nm["original_bytes"],
            owner=nm["owner"],
            asm_text=nm["asm"],
            m2c_draft=nm["m2c_draft"],
            first_mismatch=nm["first_mismatch"],
            diff_words=nm["diff_words"],
            flags=FLAGS,
        )
        (pkt_dir / f"{nm['name']}.json").write_text(json.dumps(pkt, indent=2) + "\n")

    summary = {
        "region": args.region,
        "scanned": len(tasks),
        "exact_hits": len(exact_hits),
        "exact_bytes": sum(h["original_bytes"] for h in exact_hits),
        "near_misses_total": len(near_misses),
        "task_packets_written": min(len(near_misses), args.max_packets),
        "breakdown": stats,
    }
    (args.out / f"{args.region}-harvest-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
