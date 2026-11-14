"""Original-VMA isolated IDO probes for two file_12 dialogue callbacks.

This cannot establish original translation-unit ownership, relocation parity,
or a full-ROM C promotion. Private inputs and generated files stay outside Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from .probe import Elf32

ROOT = Path(__file__).resolve().parent
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ROM_SIZE = 33_554_432
ROM_START = 0x5C8770
TEXT_END = 0x5E3C90
ROM_END = 0x5F6840
VMA_START = 0x8020D2A0
TEXT_SHA256 = "50365292dbd8cdf7a407114cb88c1807c39bf024e0f5fd4807d192357aad3131"
DATA_SHA256 = "7780f27b76e25d4cd777eb8c35e870e242dcb33675a1214349518d7326397fc4"
SPECS = (
    ("func_80222034_5DD504", "file12_dialogue_copy.c", 0x80222034, 0x5DD504, 20,
     {"D_8015C5E8": 0x8015C5E8, "D_801C7750_1C8350": 0x801C7750}),
    ("func_80222168_5DD638", "file12_dialogue_call.c", 0x80222168, 0x5DD638, 36,
     {"D_801C7743": 0x801C7743, "func_801DCD48_598C58": 0x801DCD48}),
)


def verify_layout(config: str, rom: bytes) -> None:
    if len(rom) != ROM_SIZE or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError("wrong decompressed USA ROM length or SHA-1")
    if not re.search(r"(?m)^sha1: " + ROM_SHA1 + r"\s*$", config):
        raise ValueError("wrong Splat reference SHA-1")
    headings = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", config))
    names = [m.group(1) for m in headings]
    if names.count("file_12") != 1 or names.count("file_13") != 1:
        raise ValueError("missing or duplicate file_12/file_13 segment")
    at = names.index("file_12")
    if names[at + 1] != "file_13":
        raise ValueError("file_12 next segment changed")
    block = config[headings[at].end():headings[at + 1].start()]
    lines = tuple(line.strip() for line in block.splitlines() if line.strip())
    expected = ("type: code", "start: 0x5C8770", "vram: 0x8020D2A0",
                "bss_size: 0xE0", "subalign: 16", "overlay: yes",
                "exclusive_ram_id: static_overlay_2", "subsegments:",
                "- [0x5C8770, asm]", "- [0x5E3C90, data]")
    if lines != expected:
        raise ValueError("file_12 section layout changed")
    next_block = config[headings[at + 1].end():headings[at + 2].start()]
    if "start: 0x5F6840" not in next_block:
        raise ValueError("file_12 ROM end changed")
    if (hashlib.sha256(rom[ROM_START:TEXT_END]).hexdigest() != TEXT_SHA256 or
            hashlib.sha256(rom[TEXT_END:ROM_END]).hexdigest() != DATA_SHA256):
        raise ValueError("file_12 reference section hash changed")


def check_function(elf_bytes: bytes, name: str, vma: int, expected: bytes) -> dict:
    elf = Elf32(elf_bytes)
    symbol = elf.function(name)
    if symbol.value != vma or symbol.size != len(expected):
        raise ValueError("wrong linked function VMA or symbol size")
    actual = elf.code(symbol)
    offsets = [i for i in range(0, len(expected), 4)
               if actual[i:i + 4] != expected[i:i + 4]]
    section = elf.payload(symbol.section)
    section_vma = elf.sections[symbol.section][3]
    tail = section[symbol.value - section_vma + symbol.size:]
    if len(tail) > 12 or any(tail):
        raise ValueError("unexpected isolated .text after function")
    return {"function": name, "original_vma": f"0x{vma:08X}",
            "function_bytes": len(expected), "exact_function_bytes": not offsets,
            "first_mismatch": f"+0x{offsets[0]:X}" if offsets else None,
            "original_sha256": hashlib.sha256(expected).hexdigest(),
            "candidate_sha256": hashlib.sha256(actual).hexdigest(),
            "trailing_zero_alignment_bytes": len(tail)}


def run(rom_path: Path, config_path: Path, ido: Path, linker: str) -> list[dict]:
    rom = rom_path.read_bytes()
    verify_layout(config_path.read_text(encoding="utf-8"), rom)
    result = []
    with tempfile.TemporaryDirectory(prefix="goemon-file12-") as temporary:
        work = Path(temporary)
        for name, file, vma, offset, size, globals_map in SPECS:
            if offset != ROM_START + vma - VMA_START or offset + size > TEXT_END:
                raise ValueError("file_12 function ROM/VMA mapping changed")
            source = ROOT / "candidates" / file
            obj, elf, script = (work / n for n in ("probe.o", "probe.elf", "probe.ld"))
            script.write_text("OUTPUT_ARCH(mips)\n" +
                              "".join(f"{key} = 0x{value:08X};\n"
                                      for key, value in globals_map.items()) +
                              f"SECTIONS {{ .text 0x{vma:08X} : SUBALIGN(4) {{ *(.text) }} }}\n")
            subprocess.run([str(ido), "-c", "-O2", "-mips2", "-G", "0",
                            "-non_shared", str(source), "-o", str(obj)],
                           check=True, capture_output=True)
            subprocess.run([linker, "-m", "elf32btsmip", "-T", str(script),
                            str(obj), "-o", str(elf)], check=True, capture_output=True)
            item = check_function(elf.read_bytes(), name, vma, rom[offset:offset + size])
            item["original_rom_offset"] = f"0x{offset:X}"
            item["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
            result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--splat", type=Path, required=True)
    parser.add_argument("--ido", type=Path, required=True)
    parser.add_argument("--linker", default="mips-linux-gnu-ld")
    args = parser.parse_args()
    result = run(args.rom, args.splat, args.ido, args.linker)
    print(json.dumps({"file_12_original_layout_verified": True,
                      "isolated_results": result, "whole_unit_proof": "NOT_RUN",
                      "full_rom_proof": "NOT_RUN", "new_promotions": 0}, indent=2))
    return 0 if all(row["exact_function_bytes"] for row in result) else 1


if __name__ == "__main__":
    raise SystemExit(main())
