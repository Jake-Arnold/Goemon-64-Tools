#!/usr/bin/env python3
"""Minimal 5-line JSON IDO 5.3 candidate checker for fast Executor workers.

Compiles a candidate.c against an authenticated pristine Splat reference using
authentic SGI IDO 5.3, checks exact bytes + exact named relocations + empty
non-text sections, and prints a compact JSON summary (never raw build logs).
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

from decomp.consolidated_batch_promotion import FLAGS, exact, glitch, jp55, probe, rels


def _text_bytes(obj: Path) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".bin") as tmp:
        subprocess.run(
            ["mips-linux-gnu-objcopy", "-O", "binary", "-j", ".text", str(obj), tmp.name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return Path(tmp.name).read_bytes()


def _disasm_lines(obj: Path) -> list[str]:
    out = subprocess.check_output(["mips-linux-gnu-objdump", "-d", str(obj)], text=True)
    return [line.strip() for line in out.splitlines() if re.match(r"^\s*[0-9a-f]+:\s+[0-9a-f]{8}\s+", line)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--pristine", type=Path, required=True)
    parser.add_argument("--flags", choices=("O2", "O1", "O2g3"), default="O2")
    args = parser.parse_args()

    pkt = json.loads(args.packet.read_text())
    region = pkt["region"]
    name = pkt["name"]
    off = int(pkt["rom_offset"], 16)
    vma = int(pkt["vma"], 16)
    size = int(pkt["original_bytes"])
    owner = pkt["owner"]

    flags = list(FLAGS)
    if args.flags == "O1":
        flags = [("-O1" if x == "-O2" else x) for x in FLAGS]
    elif args.flags == "O2g3":
        flags = list(FLAGS) + ["-g3"]

    rom_path = args.pristine / f"config/{region}/baserom.decompressed.z64"
    with rom_path.open("rb") as rf:
        rf.seek(off)
        orig_bytes = rf.read(size)

    with tempfile.TemporaryDirectory(prefix=f"chk_{name}_") as td:
        w = Path(td)
        owner_path = args.pristine / f"asm/{region}" / owner
        raw = owner_path.read_text()
        ms = list(jp55.BLOCK.finditer(raw))
        m = [x for x in ms if x["name"] == name][0]
        header = raw[: ms[0].start()]
        header = header if ".include" in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
        ref_s = w / f"{name}.ref.s"
        ref_o = w / f"{name}.ref.o"
        ref_s.write_text(header + raw[m.start() : m.end()] + "\n")
        subprocess.run(
            ["mips-linux-gnu-as", "-EB", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-Iinclude", "-I.", "-o", str(ref_o), str(ref_s)],
            cwd=args.snapshot,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        cand_o = w / "candidate.o"
        cc = args.snapshot / "tools/ido-5.3/cc"
        res = subprocess.run(
            [str(cc), *flags, "-I" + str(args.candidate.resolve().parent), "-o", str(cand_o), str(args.candidate.resolve())],
            cwd=args.snapshot,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if res.returncode != 0 or not cand_o.is_file():
            print(json.dumps({"name": name, "exact": False, "stage": "compile_error", "error": res.stdout.strip()[:400]}))
            return

        ref_rels = rels(ref_o)
        cand_rels = rels(cand_o)
        f_meta = {"name": name, "rom_offset": off, "vma": vma, "original_bytes": size, "relocation_count": len(ref_rels)}

        nontext_ok = True
        nontext_err = ""
        try:
            glitch.check_nontext(cand_o)
        except Exception as exc:
            nontext_ok = False
            nontext_err = str(exc)

        is_exact = bool(exact(cand_o, ref_o, f_meta)) and nontext_ok
        if is_exact:
            print(json.dumps({
                "name": name,
                "exact": True,
                "flags": args.flags,
                "original_bytes": size,
                "relocation_count": len(ref_rels),
                "source_sha256": hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
            }))
            return

        cand_bytes = _text_bytes(cand_o)
        # Strip trailing zero padding from cand_bytes for fair word comparison if > size
        n_orig = len(orig_bytes) // 4
        n_cand = len(cand_bytes) // 4
        first_idx = None
        diff_words = abs(n_orig - n_cand)
        for i in range(min(n_orig, n_cand)):
            if orig_bytes[4 * i : 4 * i + 4] != cand_bytes[4 * i : 4 * i + 4]:
                diff_words += 1
                if first_idx is None:
                    first_idx = i

        ref_dis = _disasm_lines(ref_o)
        cand_dis = _disasm_lines(cand_o)
        win_start = max(0, (first_idx or 0) - 2)
        print(json.dumps({
            "name": name,
            "exact": False,
            "diff_words": diff_words,
            "orig_bytes": len(orig_bytes),
            "cand_bytes": len(cand_bytes),
            "first_diff_offset": f"+0x{4*first_idx:X}" if first_idx is not None else "size_or_reloc",
            "nontext_ok": nontext_ok,
            "nontext_err": nontext_err,
            "relocs_match": cand_rels == ref_rels,
            "reloc_counts": [len(ref_rels), len(cand_rels)],
            "orig_window": ref_dis[win_start : win_start + 8],
            "cand_window": cand_dis[win_start : win_start + 8],
        }, indent=2))


if __name__ == "__main__":
    main()
