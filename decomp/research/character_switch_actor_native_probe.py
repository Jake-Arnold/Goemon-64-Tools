"""Original VMA matching-C probe for nine USA/Japan file_11 actor wrappers.

Checks authentic 32 MiB ROM hashes, compiles all nine candidate functions
in their original source order using original IDO 5.3, links at the genuine
VMA and compares every 32-byte function. No copyrighted game bytes emitted.
This is isolated original-address proof, not an entire overlay/full-ROM gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

REGIONS = {
    "usa": {
        "rom_sha1": "6ea0ed71032ce08fc2745f412d84936382197494",
        "vma": 0x801DDA08,
        "offset": 0x599918,
        "functions": [f"func_{0x801DDA08 + 0x20 * n:08X}_{0x599918 + 0x20 * n:X}" for n in range(9)],
        "symbols": {
            "func_801E1B60_59DA70": 0x801E1B60,
            "func_801E7CC4_5A3BD4": 0x801E7CC4,
            "func_801E15D0_59D4E0": 0x801E15D0,
        },
    },
    "japan": {
        "rom_sha1": "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
        "vma": 0x801E2DB8,
        "offset": 0x59ED88,
        "functions": [f"func_{0x801E2DB8 + 0x20 * n:08X}_{0x59ED88 + 0x20 * n:X}" for n in range(9)],
        "symbols": {
            "func_801E6DA8_5A2D78": 0x801E6DA8,
            "func_801ECDEC_5A8DBC": 0x801ECDEC,
            "func_801E67F0_5A27C0": 0x801E67F0,
        },
    },
}

SINGLE_SIZE = 0x20
COUNT = 9
TOTAL = SINGLE_SIZE * COUNT


def check_original_rom(path: Path, region: str) -> bytes:
    content = path.read_bytes()
    if len(content) != 0x2000000 or hashlib.sha1(content).hexdigest() != REGIONS[region]["rom_sha1"]:
        raise ValueError(f"Invalid authentic {region} 32 MiB ROM identity")
    return content


def compare(original: bytes, compiled: bytes, region: str) -> dict:
    info = REGIONS[region]
    offset = info["offset"]
    if len(compiled) != TOTAL or offset < 0 or offset + TOTAL > len(original):
        raise ValueError(f"Wrong size for {region} native wrapper proof")
    rom_bytes = original[offset:offset + TOTAL]
    functions = []
    for n, name in enumerate(info["functions"]):
        c = compiled[n * SINGLE_SIZE:(n + 1) * SINGLE_SIZE]
        r = rom_bytes[n * SINGLE_SIZE:(n + 1) * SINGLE_SIZE]
        functions.append({
            "name": name,
            "original_vma": f"0x{info['vma'] + n * SINGLE_SIZE:08X}",
            "rom_offset": f"0x{offset + n * SINGLE_SIZE:X}",
            "size": SINGLE_SIZE,
            "exact": c == r,
            "word_matches": sum(c[i:i+4] == r[i:i+4] for i in range(0, SINGLE_SIZE, 4)),
        })
    return {
        "region": region,
        "original_rom_sha1": info["rom_sha1"],
        "functions": functions,
        "matched_bytes": sum(f["size"] for f in functions if f["exact"]),
        "total_bytes": TOTAL,
        "all_exact": compiled == rom_bytes,
    }


def probe(rom: bytes, region: str, source: Path, cc: Path, ld: Path, objcopy: Path) -> dict:
    info = REGIONS[region]
    with tempfile.TemporaryDirectory(prefix=f"goemon-{region}-actor-wrap-") as directory:
        working = Path(directory)
        path_o, path_elf, path_bin = [working / x for x in ("candidate.o", "candidate.elf", "candidate.bin")]
        script = working / "link.ld"
        decls = "\n".join(f"{s} = 0x{value:08X};" for s, value in info["symbols"].items())
        script.write_text("OUTPUT_ARCH(mips)\n" + decls + "\n" +
                          f"SECTIONS {{ . = 0x{info['vma']:08X}; .text : {{ *(.text) }} " +
                          "/DISCARD/ : { *(.comment) *(.note*) } }\n")
        commands = [
            [str(cc), "-G", "0", "-non_shared", "-Xfullwarn", "-Xcpluscomm",
             "-O2", "-mips2", "-c", f"-DREGION_{region.upper()}", "-o", str(path_o), str(source)],
            [str(ld), "-T", str(script), "--no-check-sections", "-o", str(path_elf), str(path_o)],
            [str(objcopy), "-j", ".text", "-O", "binary", str(path_elf), str(path_bin)],
        ]
        for cmd in commands:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        return compare(rom, path_bin.read_bytes(), region)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--usa", type=Path, required=True)
    ap.add_argument("--japan", type=Path, required=True)
    ap.add_argument("--cc", type=Path, required=True)
    ap.add_argument("--ld", type=Path, required=True)
    ap.add_argument("--objcopy", type=Path, required=True)
    ap.add_argument("--candidate", type=Path,
                    default=Path(__file__).with_name("character_switch_actor_wrappers.c"))
    ap.add_argument("--report", type=Path)
    ns = ap.parse_args(argv)
    proof = {
        "format": "goemon-character-actor-wrappers-native-proof-v1",
        "scope": "isolated original-VMA native IDO; USA full-ROM stage separate",
        "regions": {},
    }
    for region in ("usa", "japan"):
        rom = check_original_rom(getattr(ns, region), region)
        proof["regions"][region] = probe(rom, region, ns.candidate, ns.cc, ns.ld, ns.objcopy)
    proof["all_exact"] = all(x["all_exact"] for x in proof["regions"].values())
    report = json.dumps(proof, indent=2) + "\n"
    if ns.report:
        ns.report.write_text(report)
    else:
        print(report, end="")
    return 0 if proof["all_exact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())