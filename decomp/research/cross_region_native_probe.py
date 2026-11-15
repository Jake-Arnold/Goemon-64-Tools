"""Proof of isolated original-address IDO codegen for US/JP switch helpers.

Strictly read-only against private verified, decompressed 32 MiB ROMs. Never
exports instructions or ROM material, only outcome metadata/hashes. Does NOT
replace linked-overlay relocation checking or full-ROM verification.
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
        "sha1": "6ea0ed71032ce08fc2745f412d84936382197494",
        "calls": {
            "character_reader": ("SELECT_READER", "func_801DD500_599410", 0x801DD500, 0x599410, 12),
            "character_wrapper": ("SELECT_WRAPPER", "func_801DD4D8_5993E8", 0x801DD4D8, 0x5993E8, 40),
            "character_sync": ("SELECT_SYNC", "func_801DD5C0_5994D0", 0x801DD5C0, 0x5994D0, 148),
        },
        "symbols": {
            "func_801DD5C0_5994D0": 0x801DD5C0,
            "D_8015C5DC_15D1DC": 0x8015C5DC,
            "func_801E0944_59C854": 0x801E0944,
            "func_8003522C_35E2C": 0x8003522C,
        },
    },
    "japan": {
        "sha1": "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
        "calls": {
            "character_reader": ("SELECT_READER", "func_801E28B0_59E880", 0x801E28B0, 0x59E880, 12),
            "character_wrapper": ("SELECT_WRAPPER", "func_801E2888_59E858", 0x801E2888, 0x59E858, 40),
            "character_sync": ("SELECT_SYNC", "func_801E2970_59E940", 0x801E2970, 0x59E940, 148),
        },
        "symbols": {
            "func_801E2970_59E940": 0x801E2970,
            "D_80161DCC_1629CC": 0x80161DCC,
            "func_801E5B5C_5A1B2C": 0x801E5B5C,
            "func_80034E9C_35A9C": 0x80034E9C,
        },
    },
}


def verified_rom(path: Path, region: str) -> bytes:
    data = path.read_bytes()
    if len(data) != 0x2000000 or hashlib.sha1(data).hexdigest() != REGIONS[region]["sha1"]:
        raise ValueError(f"Invalid expanded {region} ROM")
    return data


def compare_native(reference: bytes, compiled: bytes, offset: int, length: int) -> dict:
    if offset < 0 or length < 1 or offset + length > len(reference):
        raise ValueError("Invalid reference ROM offset / length")
    if len(compiled) < length:
        raise ValueError("Compiled function is shorter than original")
    actual = compiled[:length]
    target = reference[offset:offset + length]
    equal = sum(actual[i:i+4] == target[i:i+4] for i in range(0, length, 4))
    return {
        "original_bytes": length,
        "equal_instruction_words": equal,
        "instruction_words": length // 4,
        "exact": target == actual,
        "candidate_sha256": hashlib.sha256(actual).hexdigest(),
        "reference_sha256": hashlib.sha256(target).hexdigest(),
    }


def native_probe(rom: bytes, region: str, source: Path, cc: Path, ld: Path, objcopy: Path) -> dict:
    info = REGIONS[region]
    results = {}
    with tempfile.TemporaryDirectory(prefix=f"goemon-{region}-native-") as tmp:
        directory = Path(tmp)
        for kind, (selection, function, vma, offset, size) in info["calls"].items():
            obj, elf, out = directory / "candidate.o", directory / "candidate.elf", directory / "candidate.bin"
            script = directory / "link.ld"
            symbols = "\n".join(f"{sym} = 0x{address:08X};" for sym, address in info["symbols"].items())
            script.write_text(
                "OUTPUT_ARCH(mips)\n" + f"ENTRY({function})\n" + symbols + "\n" +
                f"SECTIONS {{ . = 0x{vma:08X}; .text : {{ *(.text) }} /DISCARD/ : {{ *(.comment) *(.note*) }} }}\n"
            )
            subprocess.run([str(cc), "-G", "0", "-non_shared", "-Xfullwarn", "-Xcpluscomm",
                            "-O2", "-mips2", "-c", f"-DREGION_{'USA' if region == 'usa' else 'JAPAN'}",
                            f"-D{selection}", "-o", str(obj), str(source)],
                           check=True, capture_output=True, text=True)
            subprocess.run([str(ld), "-T", str(script), "--no-check-sections", "-o", str(elf), str(obj)],
                           check=True, capture_output=True, text=True)
            subprocess.run([str(objcopy), "-j", ".text", "-O", "binary", str(elf), str(out)],
                           check=True, capture_output=True, text=True)
            results[kind] = {"function": function, "original_vma": f"0x{vma:08X}",
                             "rom_offset": f"0x{offset:X}",
                             **compare_native(rom, out.read_bytes(), offset, size)}
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usa", type=Path, required=True)
    parser.add_argument("--japan", type=Path, required=True)
    parser.add_argument("--cc", type=Path, required=True)
    parser.add_argument("--ld", type=Path, required=True)
    parser.add_argument("--objcopy", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, default=Path(__file__).with_name("character_switch_native_candidates.c"))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    result = {"format": "goemon-isolated-character-switch-ido-proof-v1",
              "scope": "isolated original-address native C compilation/link; not full ROM",
              "regions": {}}
    for region in ("usa", "japan"):
        rom = verified_rom(getattr(args, region), region)
        result["regions"][region] = native_probe(rom, region, args.candidate, args.cc, args.ld, args.objcopy)
    result["all_six_exact"] = all(row["exact"] for reg in result["regions"].values() for row in reg.values())
    text = json.dumps(result, indent=2) + "\n"
    if args.report:
        args.report.write_text(text)
    else:
        print(text, end="")
    return 0 if result["all_six_exact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())