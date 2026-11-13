"""Fail-closed reference and linked-ELF guard for USA overlay file_43.

This verifies pinned reference layout/bytes and optional overlay ELF provenance,
NOT candidate source ownership or a successful decomp.verify promotion. The
main segment's ROM/VMA rule must never be used for this overlay.

Inputs (including the USA Splat config and decompressed ROM) stay private.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

try:
    from .probe import Elf32
except ImportError:
    from probe import Elf32

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
# SHA-256 from the pinned-source baseline ELF recorded by G2 on 2026-11-13.
# Its report pins upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee and the
# same decompressed USA ROM identity checked above.
REFERENCE_ELF_SHA256 = "83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038"

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


def validate_reference_inputs(splat_yaml: str, reference_rom: bytes,
                              function_names: tuple[str, ...]) -> dict:
    """Validate the exact Splat/ROM pair required before overlay ELF checks.

    This binds segment order and address layout to the Splat source SHA-1,
    then binds original function claims to the 32 MiB ROM and both section
    fingerprints. A candidate ELF or full-ROM comparison must not run before
    this input contract succeeds.
    """
    layout = validate_layout(splat_yaml)
    reference = verify_reference(reference_rom, function_names)
    return {
        "input_contract": {
            "format": "goemon-overlay-reference-input-v1",
            "overlay": OVERLAY_NAME,
            "splat_source_sha1": ROM_SHA1,
            "reference_rom_bytes": ROM_BYTES,
            "reference_rom_sha1": ROM_SHA1,
            "layout": layout,
            "text_sha256": TEXT_SHA256,
            "rodata_sha256": RODATA_SHA256,
            "function_instruction_sha256": {
                name: FUNCTIONS[name][3] for name in function_names
            },
        },
        "reference_validation": reference,
    }


def _linked_file43(elf_bytes: bytes, label: str):
    """Read one linked Splat file_43 output section and its relocation table."""
    elf = Elf32(elf_bytes)
    if elf.kind != 2:
        raise ValueError(f"{label} must be a linked MIPS executable ELF")
    indices = [i for i, name in enumerate(elf.names) if name == ".file_43"]
    if len(indices) != 1:
        raise ValueError(f"{label} must contain one .file_43 output section")
    aliases = [name for name in elf.names
               if name.startswith(".file_43_") and name != ".file_43_bss"]
    if aliases:
        raise ValueError(f"{label} contains file_43 section aliases: {aliases}")
    index = indices[0]
    section = elf.sections[index]
    expected_size = ROM_END - ROM_START
    if (section[1] != 1 or section[2] != 0x7 or section[3] != VMA_START or
            section[5] != expected_size or section[8] != 16):
        raise ValueError(f"{label} .file_43 VMA, flags, type, size or alignment differs")
    section_end = section[3] + section[5]
    for other_index, other in enumerate(elf.sections):
        if (other_index == index or not (other[2] & 0x2) or other[5] == 0):
            continue
        other_name = elf.names[other_index]
        other_overlay = re.fullmatch(r"\.file_(\d+)(?:_bss)?", other_name)
        if other_overlay and other_overlay.group(1) != "43":
            # Distinct Splat overlays intentionally reuse the same RAM VMA.
            continue
        other_end = other[3] + other[5]
        if other[3] < section_end and section[3] < other_end:
            raise ValueError(f"{label} has an allocated section overlapping .file_43")
    payload = elf.payload(index)

    relocation_indices = [
        i for i, section_header in enumerate(elf.sections)
        if section_header[1] in (4, 9) and section_header[7] == index
    ]
    if (len(relocation_indices) != 1 or elf.sections[relocation_indices[0]][1] != 9 or
            elf.names[relocation_indices[0]] != ".rel.file_43"):
        raise ValueError(f"{label} must contain one .rel.file_43 relocation table")
    relocations = elf.relocations(index)
    for relocation in relocations:
        if (not section[3] <= relocation.offset < section[3] + section[5] or
                relocation.offset & 3):
            raise ValueError(f"{label} has a relocation outside aligned .file_43")
    return elf, index, section, payload, relocations


def _relocation_signature(elf: Elf32, section: tuple, relocation) -> tuple:
    symbol = relocation.symbol
    if symbol.section < len(elf.names):
        symbol_section = elf.names[symbol.section]
    else:
        symbol_section = f"SHN_{symbol.section:04X}"
    return (relocation.offset - section[3], relocation.relocation_type,
            symbol.name, symbol.value, symbol_section, symbol.kind,
            symbol.binding, relocation.addend is not None,
            relocation.addend if relocation.addend is not None else 0)


def _function_relocations(elf: Elf32, section: tuple, relocations: tuple,
                          symbol) -> tuple:
    end = symbol.value + symbol.size
    return tuple(sorted(
        _relocation_signature(elf, section, relocation)
        for relocation in relocations
        if symbol.value <= relocation.offset < end
    ))


def validate_linked_elf_provenance(splat_yaml: str, reference_rom: bytes,
                                   reference_elf: bytes, candidate_elf: bytes,
                                   function_names: tuple[str, ...]) -> dict:
    """Bind requested file_43 functions to original/candidate linked ELF data.

    This is a provenance and exact-function check only. It does not prove
    source ownership, a complete candidate ROM, or matching-C promotion.
    """
    result = validate_reference_inputs(splat_yaml, reference_rom, function_names)
    reference_sha = hashlib.sha256(reference_elf).hexdigest()
    if reference_sha != REFERENCE_ELF_SHA256:
        raise ValueError("reference linked ELF identity mismatch")
    original, original_index, original_section, original_payload, original_relocations = (
        _linked_file43(reference_elf, "reference ELF")
    )
    candidate, candidate_index, candidate_section, candidate_payload, candidate_relocations = (
        _linked_file43(candidate_elf, "candidate ELF")
    )
    expected_overlay = reference_rom[ROM_START:ROM_END]
    if original_payload != expected_overlay:
        raise ValueError("reference ELF .file_43 bytes differ from mapped original ROM")

    def reject_function_aliases(elf: Elf32, section_index: int, symbol,
                                label: str) -> None:
        start, end = symbol.value, symbol.value + symbol.size
        for other in elf.symbols:
            if (other.name == symbol.name or other.kind != 2 or
                    other.section != section_index):
                continue
            overlaps = (other.value < end and start < other.value + other.size
                        if other.size else start <= other.value < end)
            if overlaps:
                raise ValueError(f"{label} has overlapping function alias for {symbol.name}")

    function_results = []
    for name in function_names:
        vma, rom_offset, size, expected_sha = FUNCTIONS[name]
        label = re.fullmatch(r"func_([0-9A-F]{8})_([0-9A-F]+)", name)
        if (label is None or int(label.group(1), 16) != vma or
                int(label.group(2), 16) != rom_offset):
            raise ValueError(f"overlay function name disagrees with VMA/ROM mapping: {name}")
        original_symbol = original.function(name)
        candidate_symbol = candidate.function(name)
        expected_symbol = (vma, size)
        if (original_symbol.section != original_index or
                (original_symbol.value, original_symbol.size) != expected_symbol or
                original_symbol.binding not in (1, 2)):
            raise ValueError(f"reference ELF symbol/section differs for {name}")
        if (candidate_symbol.section != candidate_index or
                (candidate_symbol.value, candidate_symbol.size) != expected_symbol or
                candidate_symbol.binding not in (1, 2)):
            raise ValueError(f"candidate ELF symbol/section differs for {name}")
        reject_function_aliases(original, original_index, original_symbol, "reference ELF")
        reject_function_aliases(candidate, candidate_index, candidate_symbol, "candidate ELF")

        expected_code = reference_rom[rom_offset:rom_offset + size]
        original_code = original.code(original_symbol)
        candidate_code = candidate.code(candidate_symbol)
        if hashlib.sha256(original_code).hexdigest() != expected_sha:
            raise ValueError(f"reference ELF function bytes differ for {name}")
        if candidate_code != expected_code:
            raise ValueError(f"candidate ELF function bytes differ for {name}")

        original_relocs = _function_relocations(
            original, original_section, original_relocations, original_symbol
        )
        candidate_relocs = _function_relocations(
            candidate, candidate_section, candidate_relocations, candidate_symbol
        )
        if original_relocs != candidate_relocs:
            raise ValueError(f"candidate relocation target differs for {name}")
        function_results.append({
            "name": name,
            "section": ".file_43",
            "vma": f"0x{vma:08X}",
            "rom_offset": f"0x{rom_offset:X}",
            "bytes": size,
            "original_sha256": hashlib.sha256(original_code).hexdigest(),
            "candidate_sha256": hashlib.sha256(candidate_code).hexdigest(),
            "candidate_code_matches_original": True,
            "candidate_relocations_match_reference": True,
            "relocation_count": len(candidate_relocs),
            "relocations": [
                {
                    "section_offset": f"0x{item[0]:X}",
                    "type": item[1],
                    "symbol": item[2],
                    "symbol_vma": f"0x{item[3]:08X}",
                    "symbol_section": item[4],
                    "symbol_kind": item[5],
                    "symbol_binding": item[6],
                    "addend": item[8] if item[7] else None,
                }
                for item in candidate_relocs
            ],
        })

    # Check the complete output section after function extents so code changes
    # retain their specific diagnostic while unclaimed text/rodata bytes and
    # padding remain bound to the original ROM as well.
    if candidate_payload != expected_overlay:
        raise ValueError("candidate ELF .file_43 bytes differ from mapped original ROM")

    result["linked_elf_provenance"] = {
        "format": "goemon-file43-linked-elf-provenance-v1",
        "reference_elf_sha256": reference_sha,
        "candidate_elf_sha256": hashlib.sha256(candidate_elf).hexdigest(),
        "reference_section": {
            "name": ".file_43",
            "vma_start": f"0x{original_section[3]:08X}",
            "elf_file_offset": f"0x{original_section[4]:X}",
            "size": original_section[5],
            "sha256": hashlib.sha256(original_payload).hexdigest(),
            "relocation_count": len(original_relocations),
        },
        "candidate_section": {
            "name": ".file_43",
            "vma_start": f"0x{candidate_section[3]:08X}",
            "elf_file_offset": f"0x{candidate_section[4]:X}",
            "size": candidate_section[5],
            "sha256": hashlib.sha256(candidate_payload).hexdigest(),
            "relocation_count": len(candidate_relocations),
        },
        "functions": function_results,
        "promoted_matching_c": False,
        "proof_level": "linked overlay symbol, section, function bytes and relocation targets only",
    }
    return result


def compare_full_rom(reference_rom: bytes, candidate_rom: bytes) -> None:
    """An additional whole-ROM byte gate; this alone cannot prove source was C."""
    if len(candidate_rom) != ROM_BYTES or candidate_rom != reference_rom:
        raise ValueError("candidate full decompressed ROM differs or is incomplete")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--splat", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--reference-elf", type=Path)
    parser.add_argument("--candidate-elf", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--function", choices=tuple(FUNCTIONS), action="append", required=True)
    args = parser.parse_args()
    original = args.reference.read_bytes()
    if bool(args.reference_elf) != bool(args.candidate_elf):
        parser.error("--reference-elf and --candidate-elf must be supplied together")
    splat_yaml = args.splat.read_text(encoding="utf-8")
    if args.reference_elf:
        result = validate_linked_elf_provenance(
            splat_yaml, original, args.reference_elf.read_bytes(),
            args.candidate_elf.read_bytes(), tuple(args.function)
        )
    else:
        result = validate_reference_inputs(splat_yaml, original, tuple(args.function))
    if args.candidate:
        compare_full_rom(original, args.candidate.read_bytes())
        result["complete_rom_bytes_equal"] = True
    # No promotion claim; integration must still establish source ownership in
    # the linked ELF and run the formal decomp verification + inventory.
    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
