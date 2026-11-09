"""Fail-closed original-ROM layout guard for USA overlay file_43.

This verifies *reference layout and bytes*, NOT linker provenance, C ownership,
reconstructed functions, or a successful decomp.verify promotion. The main
segment's ROM/VMA rule must never be used for this overlay.

Inputs (including the USA Splat config and decompressed ROM) stay private.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

ROM_BYTES = 33_554_432
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
OVERLAY_NAME = "file_43"
OVERLAY_RAM = "tlb_overlay"
ROM_START = 0x6F34E0
ROM_TEXT_END = 0x6F9CE0
ROM_END = 0x6FB200
VMA_START = 0x08000000
TEXT_SHA256 = "77fa512adb309eac78ad05109746bdc0541a92995446929b1d9b7bf4a10c2b07"
RODATA_SHA256 = "6d5a1d659e1432a882d5c492ae7fc9dbc03cdfc9a284d5c95483dc429f50afb8"

# All extents/hash values are from the independently SHA-verified 32 MiB USA ROM.
# The key initializer's isolated linked match is NOT whole-ROM C proof.
FUNCTIONS = {
    "func_080001BC_6F369C": (0x080001BC, 0x6F369C, 96,
                              "21679e650f47538d001cc7ede7f84feaede2715ce8a016b5fb81bce7b10e2484"),
    "func_08006490_6F9970": (0x08006490, 0x6F9970, 140,
                              "c96aa2507f3322508dafcfd47894d90cd26ec626b6ec4b304d0d2252a53d19e0"),
}
EXPECTED_SEGMENT_LINES = (
    "type: code", "start: 0x6F34E0", "vram: 0x8000000",
    "subalign: 16", "overlay: yes", "exclusive_ram_id: tlb_overlay",
    "subsegments:", "- [0x6F34E0, asm, file_43]",
    "- [0x6F9CE0, rodata, file_43]",
)


def validate_layout(splat_yaml: str) -> dict:
    """Accept only the pinned file_43 section layout, without YAML dependencies."""
    if not re.search(r"(?m)^sha1: " + ROM_SHA1 + r"\s*$", splat_yaml):
        raise ValueError("wrong source Splat reference SHA-1")
    # Recognize only top-level segment headings. Do not silently accept an
    # additional overlay of the same name or a changed section sequence.
    matches = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", splat_yaml))
    names = [match.group(1) for match in matches]
    if names.count(OVERLAY_NAME) != 1 or names.count("file_44") != 1:
        raise ValueError("missing or duplicate overlay segment ID")
    index = names.index(OVERLAY_NAME)
    if index + 1 >= len(names) or names[index + 1] != "file_44":
        raise ValueError("overlay section must end at neighboring file_44")
    block = splat_yaml[matches[index].end():matches[index + 1].start()]
    lines = tuple(line.strip() for line in block.splitlines() if line.strip())
    if lines != EXPECTED_SEGMENT_LINES:
        raise ValueError("file_43 VMA, ROM, permissions, or section layout differs")
    after = splat_yaml[matches[index + 1].end():matches[index + 2].start() if index + 2 < len(matches) else None]
    next_lines = tuple(line.strip() for line in after.splitlines() if line.strip())
    if "start: 0x6FB200" not in next_lines:
        raise ValueError("file_43 ROM end overlaps or leaves a gap before file_44")
    if (ROM_START | ROM_TEXT_END | ROM_END) & 0xF:
        raise ValueError("unaligned overlay region")
    return {"overlay": OVERLAY_NAME, "rom_start": ROM_START,
            "text_end": ROM_TEXT_END, "rom_end": ROM_END, "vma_start": VMA_START,
            "text_bytes": ROM_TEXT_END-ROM_START,
            "rodata_bytes": ROM_END-ROM_TEXT_END}


def verify_reference(reference_rom: bytes, function_names: tuple[str, ...]) -> dict:
    if len(reference_rom) != ROM_BYTES or hashlib.sha1(reference_rom).hexdigest() != ROM_SHA1:
        raise ValueError("reference decompressed USA ROM size or SHA-1 mismatch")
    if not function_names or len(set(function_names)) != len(function_names):
        raise ValueError("empty or duplicated requested function claim")
    if (hashlib.sha256(reference_rom[ROM_START:ROM_TEXT_END]).hexdigest() != TEXT_SHA256 or
        hashlib.sha256(reference_rom[ROM_TEXT_END:ROM_END]).hexdigest() != RODATA_SHA256):
        raise ValueError("file_43 text/rodata reference hashes differ")
    validated = []
    for name in function_names:
        if name not in FUNCTIONS:
            raise ValueError("unreviewed overlay function name")
        vma, offset, size, expected_sha = FUNCTIONS[name]
        if not (ROM_START <= offset and offset + size <= ROM_TEXT_END):
            raise ValueError("overlay function crosses original text section boundary")
        if offset != ROM_START + (vma - VMA_START):
            raise ValueError("overlay ROM-to-VMA mapping differs")
        if (vma & 3) or (offset & 3) or (size & 3):
            raise ValueError("unaligned original function extent")
        if hashlib.sha256(reference_rom[offset:offset+size]).hexdigest() != expected_sha:
            raise ValueError("function instruction bytes differ from pinned reference")
        validated.append({"name": name, "vma": f"0x{vma:08X}",
                          "rom_offset": f"0x{offset:X}", "bytes": size})
    return {"overlay": OVERLAY_NAME, "reference_sha1": ROM_SHA1,
            "verified_original_functions": validated,
            "promoted_matching_c": False,
            "proof_level": "original reference mapping and original bytes only"}


def compare_full_rom(reference_rom: bytes, candidate_rom: bytes) -> None:
    """An additional whole-ROM byte gate; this alone cannot prove source was C."""
    if len(candidate_rom) != ROM_BYTES or candidate_rom != reference_rom:
        raise ValueError("candidate full decompressed ROM differs or is incomplete")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--splat", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--function", choices=tuple(FUNCTIONS), action="append", required=True)
    args = parser.parse_args()
    validate_layout(args.splat.read_text(encoding="utf-8"))
    original = args.reference.read_bytes()
    result = verify_reference(original, tuple(args.function))
    if args.candidate:
        compare_full_rom(original, args.candidate.read_bytes())
        result["complete_rom_bytes_equal"] = True
    # No promotion claim; integration must still establish source ownership in
    # the linked ELF and run the formal decomp verification + inventory.
    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
