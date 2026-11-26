#!/usr/bin/env python3
"""Zero-token cross-region mechanical porter (USA accepted C <-> Japan remaining ASM).

Finds remaining ASM functions in the target region whose normalized MIPS
instruction fingerprint matches an ALREADY accepted matching-C function in the
donor region, maps every relocated symbol 1-to-1 positionally between donor and
target pristine Splat assembly, ports the donor C source, compiles with
authentic SGI IDO 5.3, verifies exact object bytes + exact named relocations +
empty non-text sections, and generates verified altered-source negative controls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from decomp import inventory
from decomp.consolidated_batch_promotion import FLAGS, exact, glitch, jp55, probe, rels

FUNC_NAME_RE = re.compile(r"^func_([0-9A-Fa-f]{8})_([0-9A-Fa-f]+)$")
SYM_REF_RE = re.compile(r"\b((?:func|D|jtbl)_[0-9A-Fa-f]{4,8}(?:_[0-9A-Fa-f]+)?|[A-Za-z_][A-Za-z0-9_]*)\b")
ASM_INST_SYM_RE = re.compile(r"(?:%hi\(|%lo\(|jal\s+|j\s+|la\s+\$\w+,\s*)([A-Za-z_.$][A-Za-z0-9_.$]*)")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _norm_fp(raw: bytes) -> tuple[int, str]:
    norm = bytearray()
    for i in range(0, len(raw), 4):
        w = int.from_bytes(raw[i : i + 4], "big")
        op = (w >> 26) & 0x3F
        if op in (2, 3):  # j, jal
            w &= 0xFC000000
        elif op == 0x0F:  # lui
            w &= 0xFFFF0000
        elif op in (0x09, 0x0D, 0x20, 0x21, 0x23, 0x24, 0x25, 0x28, 0x29, 0x2B, 0x31, 0x39):
            imm = w & 0xFFFF
            if 0x1000 <= imm <= 0xF000:
                w &= 0xFFFF0000
        norm.extend(w.to_bytes(4, "big"))
    return (len(raw), hashlib.sha256(norm).hexdigest()[:20])


def _extract_single_function_unit(raw_c: str, fn_name: str) -> str | None:
    """Extract preamble (includes/typedefs/externs/macros) + one function body from a C file."""
    # Find function definition start
    pat = re.compile(rf"(?m)^([A-Za-z_][A-Za-z0-9_\s\*]*?\b{re.escape(fn_name)}\s*\([^;{{}}]*\)\s*\{{)")
    m = pat.search(raw_c)
    if not m:
        return None
    # Brace-match the function body
    start = m.start()
    brace_start = raw_c.find("{", m.start())
    depth = 0
    end = -1
    for i in range(brace_start, len(raw_c)):
        ch = raw_c[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end < 0:
        return None
    func_body = raw_c[start:end]

    # Extract preamble: everything before the FIRST function definition in the file
    first_fn = re.search(r"(?m)^(?:static\s+)?(?:void|s8|u8|s16|u16|s32|u32|s64|u64|f32|f64|int|char|short|long|unsigned|signed|M2C_UNK\w*|Gfx|OS\w+)\s+\**\w+\s*\([^;{}]*\)\s*\{", raw_c)
    preamble = raw_c[: first_fn.start()] if first_fn else ""
    # Strip GLOBAL_ASM blocks from preamble if any
    preamble = re.sub(r"GLOBAL_ASM\([^)]*\)", "", preamble)
    return preamble.rstrip() + "\n\n" + func_body + "\n"


def _extract_reloc_syms(asm_block: str) -> list[str]:
    syms: list[str] = []
    for line in asm_block.splitlines():
        if line.strip().startswith(("glabel ", "endlabel ", "nonmatching ", ".L")):
            continue
        for m in ASM_INST_SYM_RE.finditer(line):
            s = m.group(1)
            if not s.startswith("."):
                syms.append(s)
    return syms


def _index_donor_c_sources(repo_root: Path, donor_region: str) -> dict[str, Path]:
    """Map donor function name -> accepted C file path in repo."""
    sources: dict[str, Path] = {}
    decomp_dir = repo_root / "decomp"
    # Scan all candidate.c / *.c under decomp/research and decomp/
    for c_file in sorted(decomp_dir.rglob("*.c")):
        if c_file.name == "negative.c" or "test_" in c_file.name:
            continue
        # Fast path: parent dir name matches func_...
        parent = c_file.parent.name
        if FUNC_NAME_RE.match(parent) and c_file.name == "candidate.c":
            # Prefer region-matching paths
            parts = c_file.as_posix()
            if donor_region == "japan_0" and ("/usa/" in parts):
                continue
            if donor_region == "usa" and ("/japan_0/" in parts or "/japan_" in parts):
                continue
            sources.setdefault(parent, c_file)
            continue
        # Otherwise check function definitions inside file
        txt = c_file.read_text(errors="ignore")
        for m in re.finditer(r"\b(func_[0-9A-Fa-f]{8}_[0-9A-Fa-f]+)\s*\(", txt):
            fn = m.group(1)
            # Make sure it's a definition (followed by ) { somewhere nearby)
            tail = txt[m.end() : m.end() + 250]
            if ")" in tail and "{" in tail.split(";", 1)[0]:
                sources.setdefault(fn, c_file)
    return sources


def _build_owner_map(pristine: Path, region: str) -> dict[str, str]:
    asm_root = pristine / f"asm/{region}"
    owners: dict[str, str] = {}
    for s_file in asm_root.rglob("*.s"):
        rel = s_file.relative_to(asm_root).as_posix()
        if rel.startswith("data/"):
            continue
        txt = s_file.read_text(errors="ignore")
        for m in jp55.BLOCK.finditer(txt):
            owners.setdefault(m["name"], rel)
    return owners


def _get_asm_block(pristine: Path, region: str, owner_rel: str, name: str) -> tuple[str, str] | None:
    path = pristine / f"asm/{region}" / owner_rel
    if not path.is_file():
        return None
    raw = path.read_text()
    ms = list(jp55.BLOCK.finditer(raw))
    matches = [m for m in ms if m["name"] == name]
    if len(matches) != 1:
        return None
    header = raw[: ms[0].start()]
    header = header if ".include" in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
    return header, raw[matches[0].start() : matches[0].end()] + "\n"


def _make_negative(code: str, name: str) -> list[str]:
    variants: list[str] = []
    # 1. Replace `return ` with `return 1 + ` or add a volatile store before the final closing brace (C89-safe!)
    last_brace = code.rfind("}")
    if last_brace > 0:
        variants.append(code[:last_brace] + "\n    *(volatile int *)0x80000000 = 1;\n" + code[last_brace:])
    # 2. Wrap a statement right after the first `;` inside the function body (after declarations!)
    fn_m = re.search(rf"\b{re.escape(name)}\s*\([^)]*\)\s*\{{", code)
    if fn_m:
        body_start = fn_m.end()
        # Insert before first `return` if present
        ret_m = re.search(r"\breturn\b", code[body_start:])
        if ret_m:
            pos = body_start + ret_m.start()
            variants.append(code[:pos] + "{ *(volatile int *)0x80000000 = 1; } " + code[pos:])
    # 3. Tweak a hex constant if present
    hex_m = re.search(r"\b0x([1-9A-Fa-f][0-9A-Fa-f]*)\b", code)
    if hex_m:
        val = int(hex_m.group(1), 16)
        variants.append(code[: hex_m.start()] + f"0x{val + 1:X}" + code[hex_m.end() :])
    return variants


def port_direction(
    *,
    donor_region: str,
    donor_snap: Path,
    donor_prist: Path,
    target_region: str,
    target_snap: Path,
    target_prist: Path,
    out_dir: Path,
    repo_rel_out: str,
) -> dict:
    def parse_elf(region: str, snap: Path, prist: Path):
        txt = subprocess.check_output(["mips-linux-gnu-readelf", "-Ws", str(snap / f"build/{region}/mnsg.elf")], text=True)
        funcs, markers = inventory.parse_inventory_symbols(txt)
        asm_set = markers & set(funcs)
        c_set = set(funcs) - asm_set
        rom = (prist / f"config/{region}/baserom.decompressed.z64").read_bytes()
        fps_c: dict[tuple[int, str], list[tuple[str, int, int, int]]] = {}
        fps_asm: dict[tuple[int, str], list[tuple[str, int, int, int]]] = {}
        for name, info in funcs.items():
            m = FUNC_NAME_RE.match(name)
            if not m:
                continue
            vma = int(m.group(1), 16)
            off = int(m.group(2), 16)
            sz = info["size"]
            if sz < 8:
                continue
            fp = _norm_fp(rom[off : off + sz])
            row = (name, vma, off, sz)
            if name in c_set:
                fps_c.setdefault(fp, []).append(row)
            else:
                fps_asm.setdefault(fp, []).append(row)
        return fps_c, fps_asm, rom

    donor_c, _, _ = parse_elf(donor_region, donor_snap, donor_prist)
    _, target_asm, target_rom = parse_elf(target_region, target_snap, target_prist)

    donor_sources = _index_donor_c_sources(REPO_ROOT, donor_region)
    donor_owners = _build_owner_map(donor_prist, donor_region)
    target_owners = _build_owner_map(target_prist, target_region)
    ledger_sha = _sha((REPO_ROOT / "decomp/COMPILER_QUIRKS.md").read_bytes())

    pairs: list[tuple[tuple[str, int, int, int], tuple[str, int, int, int]]] = []
    for fp, t_list in target_asm.items():
        if fp not in donor_c:
            continue
        d_row = donor_c[fp][0]
        for t_row in t_list:
            pairs.append((d_row, t_row))

    stats: dict[str, int] = {"pairs_found": len(pairs)}
    manifest: list[dict] = []
    cc = target_snap / "tools/ido-5.3/cc"

    for (d_name, d_vma, d_off, d_sz), (t_name, t_vma, t_off, t_sz) in sorted(pairs, key=lambda x: x[1][2]):
        d_src_path = donor_sources.get(d_name)
        if not d_src_path:
            stats["no_donor_source"] = stats.get("no_donor_source", 0) + 1
            continue
        d_owner = donor_owners.get(d_name)
        t_owner = target_owners.get(t_name)
        if not d_owner or not t_owner:
            stats["no_owner"] = stats.get("no_owner", 0) + 1
            continue
        d_blk_pair = _get_asm_block(donor_prist, donor_region, d_owner, d_name)
        t_blk_pair = _get_asm_block(target_prist, target_region, t_owner, t_name)
        if not d_blk_pair or not t_blk_pair:
            stats["no_asm"] = stats.get("no_asm", 0) + 1
            continue
        _, d_blk = d_blk_pair
        t_hdr, t_blk = t_blk_pair

        d_syms = _extract_reloc_syms(d_blk)
        t_syms = _extract_reloc_syms(t_blk)
        if len(d_syms) != len(t_syms):
            stats["sym_len_mismatch"] = stats.get("sym_len_mismatch", 0) + 1
            continue

        sym_map = {d_name: t_name}
        conflict = False
        for ds, ts in zip(d_syms, t_syms):
            if ds in sym_map and sym_map[ds] != ts:
                conflict = True
                break
            sym_map[ds] = ts
        if conflict:
            stats["sym_conflict"] = stats.get("sym_conflict", 0) + 1
            continue

        # Rewrite donor C source using whole-word replacement
        raw_c = d_src_path.read_text()
        fn_defs = re.findall(r"\b(func_[0-9A-Fa-f]{8}_[0-9A-Fa-f]+)\s*\([^;]*\)\s*\{", raw_c)
        if len(set(fn_defs)) == 1 and d_name in fn_defs:
            unit_c = raw_c
        else:
            unit_c = _extract_single_function_unit(raw_c, d_name)
            if not unit_c:
                stats["extract_fail"] = stats.get("extract_fail", 0) + 1
                continue

        def _repl(m: re.Match) -> str:
            return sym_map.get(m.group(0), m.group(0))

        ported_c = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", _repl, unit_c)
        orig_bytes = target_rom[t_off : t_off + t_sz]

        with tempfile.TemporaryDirectory(prefix=f"xp_{t_name}_") as td:
            w = Path(td)
            # Copy any sibling headers referenced by #include "..." from donor dir or decomp/
            hdrs: dict[str, str] = {}
            inc_names = set(re.findall(r'#include\s+"([^"]+)"', ported_c))
            for h_name in sorted(inc_names):
                for search_dir in (d_src_path.parent, REPO_ROOT / "decomp"):
                    cand_h = search_dir / h_name
                    if cand_h.is_file():
                        h_txt = cand_h.read_text()
                        h_txt_ported = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", _repl, h_txt)
                        (w / Path(h_name).name).write_text(h_txt_ported)
                        hdrs[Path(h_name).name] = _sha(h_txt_ported.encode())
                        break

            ref_s = w / f"{t_name}.ref.s"
            ref_o = w / f"{t_name}.ref.o"
            ref_s.write_text(t_hdr + t_blk)
            if subprocess.run(
                ["mips-linux-gnu-as", "-EB", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-Iinclude", "-I.", "-o", str(ref_o), str(ref_s)],
                cwd=target_snap,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode != 0:
                stats["as_fail"] = stats.get("as_fail", 0) + 1
                continue

            cand_c = w / "candidate.c"
            cand_o = w / "candidate.o"
            cand_c.write_text(ported_c)
            if subprocess.run(
                [str(cc), *FLAGS, "-I" + str(w), "-o", str(cand_o), str(cand_c)],
                cwd=target_snap,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode != 0:
                stats["compile_fail"] = stats.get("compile_fail", 0) + 1
                continue

            rel_count = len(rels(ref_o))
            f_meta = {"name": t_name, "rom_offset": t_off, "vma": t_vma, "original_bytes": t_sz, "relocation_count": rel_count}
            try:
                probe.get_original_splat_lines(target_prist / f"asm/{target_region}" / t_owner, t_name, t_off, t_vma, t_sz, orig_bytes)
                ok = exact(cand_o, ref_o, f_meta)
                if ok:
                    glitch.check_nontext(cand_o)
            except Exception:
                ok = False

            if not ok:
                stats["not_exact"] = stats.get("not_exact", 0) + 1
                continue

            neg_src = None
            for idx, v in enumerate(_make_negative(ported_c, t_name)):
                neg_c = w / f"neg_{idx}.c"
                neg_o = w / f"neg_{idx}.o"
                neg_c.write_text(v)
                if subprocess.run(
                    [str(cc), *FLAGS, "-I" + str(w), "-o", str(neg_o), str(neg_c)],
                    cwd=target_snap,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode == 0:
                    try:
                        if not exact(neg_o, ref_o, f_meta):
                            neg_src = v
                            break
                    except Exception:
                        neg_src = v
                        break
            if neg_src is None:
                stats["neg_fail"] = stats.get("neg_fail", 0) + 1
                continue

            # Write ready-to-promote source folder!
            sdir = out_dir / "sources" / target_region / t_name
            sdir.mkdir(parents=True, exist_ok=True)
            for h_name in hdrs:
                (sdir / h_name).write_text((w / h_name).read_text())
            (sdir / "candidate.c").write_text(ported_c)
            (sdir / "negative.c").write_text(neg_src)
            rel_base = repo_rel_out.rstrip("/") if repo_rel_out else out_dir.as_posix()
            manifest.append({
                "region": target_region,
                "name": t_name,
                "rom_offset": t_off,
                "vma": t_vma,
                "original_bytes": t_sz,
                "owner": t_owner,
                "code_sha256": _sha(orig_bytes),
                "source_sha256": _sha(ported_c.encode()),
                "negative_sha256": _sha(neg_src.encode()),
                "flags": FLAGS,
                "nonstandard_sdk_flags": False,
                "relocation_count": rel_count,
                "include_dir": f"{rel_base}/sources/{target_region}/{t_name}",
                "compiler_quirk_outcome": "NO_NEW_COMPILER_FINDING",
                "ledger_sha256": ledger_sha,
                "source": f"sources/{target_region}/{t_name}/candidate.c",
                "negative_source": f"sources/{target_region}/{t_name}/negative.c",
                "origin": f"zero-token cross-region port from {donor_region}:{d_name}",
                "headers_sha256": hdrs,
            })
            stats["EXACT"] = stats.get("EXACT", 0) + 1

    out_dir.mkdir(parents=True, exist_ok=True)
    if manifest:
        (out_dir / f"{target_region}-candidates.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return {
        "target_region": target_region,
        "donor_region": donor_region,
        "exact_hits": len(manifest),
        "exact_bytes": sum(m["original_bytes"] for m in manifest),
        "stats": stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usa-snapshot", type=Path, required=True)
    parser.add_argument("--usa-pristine", type=Path, required=True)
    parser.add_argument("--jp-snapshot", type=Path, required=True)
    parser.add_argument("--jp-pristine", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repo-rel-out", default="")
    args = parser.parse_args()

    jp_res = port_direction(
        donor_region="usa",
        donor_snap=args.usa_snapshot,
        donor_prist=args.usa_pristine,
        target_region="japan_0",
        target_snap=args.jp_snapshot,
        target_prist=args.jp_pristine,
        out_dir=args.out,
        repo_rel_out=args.repo_rel_out,
    )
    usa_res = port_direction(
        donor_region="japan_0",
        donor_snap=args.jp_snapshot,
        donor_prist=args.jp_pristine,
        target_region="usa",
        target_snap=args.usa_snapshot,
        target_prist=args.usa_pristine,
        out_dir=args.out,
        repo_rel_out=args.repo_rel_out,
    )
    print(json.dumps({"usa": usa_res, "japan_0": jp_res}, indent=2))


if __name__ == "__main__":
    main()
