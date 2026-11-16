"""Fail-closed USA file_13 reference and linked-ELF checks.

file_13 is the Impact controller and HUD overlay. Its file table assigns the
overlay the reusable 0x801CB460 window. This module checks the exact ROM/VMA
mapping and complete linked section before a staged function can be counted.
"""
from __future__ import annotations

import hashlib
import re

try:
    from .probe import Elf32
except ImportError:
    from probe import Elf32

ROM_BYTES = 33_554_432
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
OVERLAY_NAME = "file_13"
OVERLAY_RAM = "static_overlay_1"
ROM_START = 0x5F6840
ROM_TEXT_END = 0x634E30
ROM_END = 0x63A2B0
VMA_START = 0x801CB460
BSS_SIZE = 0x80
TEXT_SHA256 = "1d4463ddfa36511e85d0f26a6cf4ba614bed884daa3820eb413c2b9a1e4e2f3b"
DATA_SHA256 = "4c6999139e37ce05a334ee8304d92105987f5a758039deaef53207849e3a262d"
FILE_SHA256 = "f3116027c76aad9c68dac460bfb58f4af059d0e9c6f6aff8a7e6091f19c6bd85"

FUNCTIONS = {
    "func_801D3954_5FED34": (
        0x801D3954, 0x5FED34, 40,
        "0088a46b77319aabd425930cbf8b5e2b4a3c408fc4db73f46b0fdee0414f5fcf",
    ),
    "func_801D3A44_5FEE24": (
        0x801D3A44, 0x5FEE24, 36,
        "b25fc487c5084143936a71e2fedcb1f53d5a497030af1fd2de25a196517fac7b",
    ),
}
FUNCTION_RELOCATIONS = {
    "func_801D3954_5FED34": (
        (0, 5, "D_8020EED0_63A2B0"),
        (4, 6, "D_8020EED0_63A2B0"),
    ),
    "func_801D3A44_5FEE24": (
        (0, 5, "D_8020EED0_63A2B0"),
        (4, 6, "D_8020EED0_63A2B0"),
    ),
}
FUNCTION_RELOCATION_SYMBOLS = {
    "func_801D3954_5FED34": {"D_8020EED0_63A2B0": (1, 4)},
    "func_801D3A44_5FEE24": {"D_8020EED0_63A2B0": (1, 4)},
}
FUNCTION_OBJECT_PADDING = {
    "func_801D3954_5FED34": 8,
    "func_801D3A44_5FEE24": 12,
}
APPROVED_SYMBOL_KIND_UPGRADES = {
    "D_8015C5C8_15D1C8": 1,
    "D_8015C5D8_15D1D8": 1,
    "D_8015C608_15D208": 1,
    "D_8020EED0_63A2B0": 1,
    ".L0800AD60_6BE000": 2,
}

EXPECTED_SEGMENT_LINES = (
    "type: code", "start: 0x5F6840", "vram: 0x801CB460",
    "bss_size: 0x80", "subalign: 16", "overlay: yes",
    "exclusive_ram_id: static_overlay_1", "subsegments:",
    "- [0x5F6840, asm]", "- [0x634E30, data]",
)


def validate_layout(splat_yaml: str) -> dict:
    """Accept only the pinned file_13 layout and adjacent file_14 boundary."""
    if not re.search(r"(?m)^sha1: " + ROM_SHA1 + r"\s*$", splat_yaml):
        raise ValueError("wrong source Splat reference SHA-1")
    headings = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", splat_yaml))
    names = [match.group(1) for match in headings]
    if names.count(OVERLAY_NAME) != 1 or names.count("file_14") != 1:
        raise ValueError("missing or duplicate file_13/file_14 segment")
    index = names.index(OVERLAY_NAME)
    if index + 1 >= len(names) or names[index + 1] != "file_14":
        raise ValueError("file_13 must end at neighboring file_14")
    block = splat_yaml[headings[index].end():headings[index + 1].start()]
    lines = tuple(line.strip() for line in block.splitlines() if line.strip())
    if lines != EXPECTED_SEGMENT_LINES:
        raise ValueError("file_13 VMA, ROM, BSS, overlay ID, or section split differs")
    next_block = splat_yaml[headings[index + 1].end():
                            headings[index + 2].start() if index + 2 < len(headings) else None]
    if "start: 0x63A2B0" not in next_block:
        raise ValueError("file_13 ROM end differs from file_14 start")
    if (ROM_START | ROM_TEXT_END | ROM_END | VMA_START) & 0xF:
        raise ValueError("unaligned file_13 region")
    return {
        "overlay": OVERLAY_NAME,
        "rom_start": ROM_START,
        "text_end": ROM_TEXT_END,
        "rom_end": ROM_END,
        "vma_start": VMA_START,
        "text_bytes": ROM_TEXT_END - ROM_START,
        "data_bytes": ROM_END - ROM_TEXT_END,
        "bss_size": BSS_SIZE,
        "ram_id": OVERLAY_RAM,
    }


def verify_reference(reference_rom: bytes, function_names: tuple[str, ...]) -> dict:
    if len(reference_rom) != ROM_BYTES or hashlib.sha1(reference_rom).hexdigest() != ROM_SHA1:
        raise ValueError("reference decompressed USA ROM size or SHA-1 mismatch")
    if not function_names or len(set(function_names)) != len(function_names):
        raise ValueError("empty or duplicated requested function claim")
    if (hashlib.sha256(reference_rom[ROM_START:ROM_TEXT_END]).hexdigest() != TEXT_SHA256 or
            hashlib.sha256(reference_rom[ROM_TEXT_END:ROM_END]).hexdigest() != DATA_SHA256 or
            hashlib.sha256(reference_rom[ROM_START:ROM_END]).hexdigest() != FILE_SHA256):
        raise ValueError("file_13 text/data reference hashes differ")
    validated = []
    for name in function_names:
        if name not in FUNCTIONS:
            raise ValueError("unreviewed file_13 function name")
        vma, offset, size, expected_sha = FUNCTIONS[name]
        if not (ROM_START <= offset and offset + size <= ROM_TEXT_END):
            raise ValueError("file_13 function crosses the original text boundary")
        if offset != ROM_START + (vma - VMA_START):
            raise ValueError("file_13 ROM-to-VMA mapping differs")
        if (vma & 3) or (offset & 3) or (size & 3):
            raise ValueError("unaligned original file_13 function extent")
        if hashlib.sha256(reference_rom[offset:offset + size]).hexdigest() != expected_sha:
            raise ValueError("file_13 function bytes differ from pinned reference")
        validated.append({
            "name": name, "vma": f"0x{vma:08X}",
            "rom_offset": f"0x{offset:X}", "bytes": size,
        })
    return {
        "overlay": OVERLAY_NAME,
        "reference_sha1": ROM_SHA1,
        "verified_original_functions": validated,
        "promoted_matching_c": False,
        "proof_level": "original reference mapping and original bytes only",
    }


def validate_reference_inputs(splat_yaml: str, reference_rom: bytes,
                              function_names: tuple[str, ...]) -> dict:
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
            "data_sha256": DATA_SHA256,
            "file_sha256": FILE_SHA256,
            "function_instruction_sha256": {
                name: FUNCTIONS[name][3] for name in function_names
            },
        },
        "reference_validation": reference,
    }


def normalize_relocation_metadata(original: tuple, candidate: tuple) -> dict:
    """Allow only unchanged-target ELF symbol kind upgrades from the C object."""
    if len(original) != len(candidate):
        raise ValueError("file_13 relocation table entry count changed")
    normalized = {}
    for old, new in zip(original, candidate):
        if old == new:
            continue
        if (old[:5] + old[6:] != new[:5] + new[6:] or
                old[5] != 0 or
                APPROVED_SYMBOL_KIND_UPGRADES.get(old[2]) != new[5]):
            raise ValueError("file_13 relocation target changed beyond approved symbol type upgrades")
        normalized[old[2]] = normalized.get(old[2], 0) + 1
    return {
        "symbol_kind_upgrades": normalized,
        "relocation_sites_and_targets_unchanged": True,
    }


def validate_linked_elf_provenance(splat_yaml: str, reference_rom: bytes,
                                    baseline_elf: bytes, candidate_elf: bytes,
                                    function_names: tuple[str, ...]) -> dict:
    """Prove complete file_13 bytes and relocation preservation in linked ELFs."""
    validate_reference_inputs(splat_yaml, reference_rom, function_names)
    expected_section = reference_rom[ROM_START:ROM_END]

    def inspect(elf_bytes: bytes, label: str):
        elf = Elf32(elf_bytes)
        if elf.kind != 2:
            raise ValueError(f"{label} must be a linked MIPS executable ELF")
        matches = [i for i, section_name in enumerate(elf.names)
                   if section_name == ".file_13"]
        if len(matches) != 1:
            raise ValueError(f"{label} must contain one .file_13 section")
        index = matches[0]
        section = elf.sections[index]
        if (section[1], section[2], section[3], section[5], section[8]) != (
                1, 0x7, VMA_START, ROM_END - ROM_START, 16):
            raise ValueError(f"{label} .file_13 output section layout differs")
        payload = elf.payload(index)
        if payload != expected_section:
            raise ValueError(f"{label} .file_13 bytes differ from original ROM")
        bss_matches = [i for i, section_name in enumerate(elf.names)
                       if section_name == ".file_13_bss"]
        if len(bss_matches) != 1:
            raise ValueError(f"{label} must contain one .file_13_bss section")
        bss = elf.sections[bss_matches[0]]
        if (bss[1], bss[2], bss[3], bss[5], bss[8]) != (
                8, 3, VMA_START + ROM_END - ROM_START, 0, 16):
            raise ValueError(f"{label} .file_13_bss layout differs")
        relocations = tuple(sorted(
            (item.offset, item.relocation_type, item.symbol.name,
             item.symbol.value, item.symbol.size, item.symbol.kind,
             item.symbol.binding, item.symbol.section, item.addend)
            for item in elf.relocations(index)
        ))
        return elf, index, payload, relocations

    baseline, _, _, baseline_relocations = inspect(baseline_elf, "baseline")
    candidate, candidate_index, candidate_payload, candidate_relocations = inspect(
        candidate_elf, "candidate")
    relocation_normalizations = normalize_relocation_metadata(
        baseline_relocations, candidate_relocations
    )
    function_rows = []
    for name in function_names:
        expected_vma, expected_offset, expected_size, expected_hash = FUNCTIONS[name]
        symbol = candidate.function(name)
        if (symbol.value != expected_vma or symbol.size != expected_size or
                symbol.binding != 1 or symbol.section != candidate_index):
            raise ValueError("candidate file_13 function symbol identity differs")
        code = candidate.code(symbol)
        original = reference_rom[expected_offset:expected_offset + expected_size]
        if code != original or hashlib.sha256(code).hexdigest() != expected_hash:
            raise ValueError("candidate file_13 function bytes differ from original")
        function_relocations = tuple(sorted(
            (item.offset - expected_vma, item.relocation_type, item.symbol.name)
            for item in candidate.relocations(candidate_index)
            if expected_vma <= item.offset < expected_vma + expected_size
        ))
        if function_relocations != FUNCTION_RELOCATIONS[name]:
            raise ValueError("candidate file_13 function relocation signature differs")
        function_rows.append({
            "name": name,
            "section": ".file_13",
            "vma": f"0x{expected_vma:08X}",
            "rom_offset": f"0x{expected_offset:X}",
            "bytes": expected_size,
            "original_sha256": expected_hash,
            "candidate_sha256": hashlib.sha256(code).hexdigest(),
            "candidate_code_matches_original": True,
            "candidate_relocations_match_reference": True,
            "relocation_count": len(function_relocations),
        })
    return {
        "format": "goemon-file13-linked-elf-v1",
        "overlay": OVERLAY_NAME,
        "section": ".file_13",
        "section_vma": f"0x{VMA_START:08X}",
        "section_bytes": len(candidate_payload),
        "section_sha256": FILE_SHA256,
        "section_bytes_match_original": True,
        "relocation_count": len(candidate_relocations),
        "relocation_sites_and_targets_match_baseline": True,
        "raw_relocation_metadata_identical": not relocation_normalizations["symbol_kind_upgrades"],
        "relocation_metadata_normalizations": relocation_normalizations,
        "functions": function_rows,
    }
