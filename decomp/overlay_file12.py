"""Fail-closed USA file_12 reference and linked-ELF checks.

The file_12 overlay combines text and data and uses its own ROM/VMA mapping.
This module verifies only a pinned reference, linked section, symbol, bytes and
relocations. It does not establish production ownership or promotion by itself.
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
OVERLAY_NAME = "file_12"
OVERLAY_RAM = "static_overlay_2"
ROM_START = 0x5C8770
ROM_TEXT_END = 0x5E3C90
ROM_END = 0x5F6840
VMA_START = 0x8020D2A0
TEXT_SHA256 = "50365292dbd8cdf7a407114cb88c1807c39bf024e0f5fd4807d192357aad3131"
DATA_SHA256 = "7780f27b76e25d4cd777eb8c35e870e242dcb33675a1214349518d7326397fc4"
REFERENCE_ELF_SHA256 = "83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038"
PINNED_SHARED_ALLOCATED_SECTION = (
    ".audio_tables", 0x800967C0, 0x4C0380, 0x3, 16,
    "1339118f55006e5d052455f76554e570ac1c25a45f65db2d283645eaadb67a1f",
)
TEXT_END_ALIAS = (
    ROM_TEXT_END - 4,
    VMA_START + ROM_TEXT_END - ROM_START - 4,
    "D_802287BC_5E3C8C",
    "func_802287BC_5E3C8C",
    "00000000",
)

FUNCTIONS = {
    "func_80222034_5DD504": (
        0x80222034, 0x5DD504, 20,
        "5ccb72181f417c5c752ed603f23e956d5824dbb8d53935fe46132f2c4dd7d9db",
    ),
    "func_80222168_5DD638": (
        0x80222168, 0x5DD638, 36,
        "2fc27981dfd6f3b7bec3855adf32d1969e5efe4a62e235c6abda6c1cfdd38c98",
    ),
}

FUNCTION_RELOCATIONS = {
    "func_80222034_5DD504": (
        (0x0, 5, "D_8015C5E8"), (0x4, 6, "D_8015C5E8"),
        (0x8, 5, "D_801C7750_1C8350"), (0x10, 6, "D_801C7750_1C8350"),
    ),
    "func_80222168_5DD638": (
        (0x8, 5, "D_801C7743"), (0xC, 4, "func_801DCD48_598C58"),
        (0x10, 6, "D_801C7743"),
    ),
}

EXPECTED_SEGMENT_LINES = (
    "type: code", "start: 0x5C8770", "vram: 0x8020D2A0",
    "bss_size: 0xE0", "subalign: 16", "overlay: yes",
    "exclusive_ram_id: static_overlay_2", "subsegments:",
    "- [0x5C8770, asm]", "- [0x5E3C90, data]",
)


def validate_layout(splat_yaml: str) -> dict:
    """Accept only the pinned file_12 segment and file_13 end boundary."""
    if not re.search(r"(?m)^sha1: " + ROM_SHA1 + r"\s*$", splat_yaml):
        raise ValueError("wrong source Splat reference SHA-1")
    headings = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", splat_yaml))
    names = [match.group(1) for match in headings]
    if names.count(OVERLAY_NAME) != 1 or names.count("file_13") != 1:
        raise ValueError("missing or duplicate file_12/file_13 segment")
    index = names.index(OVERLAY_NAME)
    if index + 1 >= len(names) or names[index + 1] != "file_13":
        raise ValueError("file_12 must end at neighboring file_13")
    block = splat_yaml[headings[index].end():headings[index + 1].start()]
    lines = tuple(line.strip() for line in block.splitlines() if line.strip())
    if lines != EXPECTED_SEGMENT_LINES:
        raise ValueError("file_12 VMA, ROM, overlay ID, or text/data split differs")
    next_block = splat_yaml[
        headings[index + 1].end():
        headings[index + 2].start() if index + 2 < len(headings) else None
    ]
    if "start: 0x5F6840" not in next_block:
        raise ValueError("file_12 ROM end differs from file_13 start")
    if (ROM_START | ROM_TEXT_END | ROM_END) & 0xF:
        raise ValueError("unaligned file_12 region")
    return {
        "overlay": OVERLAY_NAME,
        "rom_start": ROM_START,
        "text_end": ROM_TEXT_END,
        "rom_end": ROM_END,
        "vma_start": VMA_START,
        "text_bytes": ROM_TEXT_END - ROM_START,
        "data_bytes": ROM_END - ROM_TEXT_END,
        "ram_id": OVERLAY_RAM,
    }


def verify_reference(reference_rom: bytes, function_names: tuple[str, ...]) -> dict:
    if len(reference_rom) != ROM_BYTES or hashlib.sha1(reference_rom).hexdigest() != ROM_SHA1:
        raise ValueError("reference decompressed USA ROM size or SHA-1 mismatch")
    if not function_names or len(set(function_names)) != len(function_names):
        raise ValueError("empty or duplicated requested function claim")
    if (hashlib.sha256(reference_rom[ROM_START:ROM_TEXT_END]).hexdigest() != TEXT_SHA256 or
            hashlib.sha256(reference_rom[ROM_TEXT_END:ROM_END]).hexdigest() != DATA_SHA256):
        raise ValueError("file_12 text/data reference hashes differ")
    validated = []
    for name in function_names:
        if name not in FUNCTIONS:
            raise ValueError("unreviewed file_12 function name")
        vma, offset, size, expected_sha = FUNCTIONS[name]
        if not (ROM_START <= offset and offset + size <= ROM_TEXT_END):
            raise ValueError("file_12 function crosses the original text boundary")
        if offset != ROM_START + (vma - VMA_START):
            raise ValueError("file_12 ROM-to-VMA mapping differs")
        if (vma & 3) or (offset & 3) or (size & 3):
            raise ValueError("unaligned original file_12 function extent")
        if hashlib.sha256(reference_rom[offset:offset + size]).hexdigest() != expected_sha:
            raise ValueError("file_12 function bytes differ from pinned reference")
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
            "function_instruction_sha256": {
                name: FUNCTIONS[name][3] for name in function_names
            },
        },
        "reference_validation": reference,
    }


def _linked_file12(elf_bytes: bytes, label: str):
    elf = Elf32(elf_bytes)
    if elf.kind != 2:
        raise ValueError(f"{label} must be a linked MIPS executable ELF")
    indices = [i for i, name in enumerate(elf.names) if name == ".file_12"]
    if len(indices) != 1:
        raise ValueError(f"{label} must contain one .file_12 output section")
    aliases = [name for name in elf.names
               if name.startswith(".file_12_") and name != ".file_12_bss"]
    if aliases:
        raise ValueError(f"{label} contains file_12 section aliases: {aliases}")
    index = indices[0]
    section = elf.sections[index]
    if (section[1] != 1 or section[2] != 0x7 or section[3] != VMA_START or
            section[5] != ROM_END - ROM_START or section[8] != 16):
        raise ValueError(f"{label} .file_12 VMA, flags, extent, or alignment differs")
    section_end = section[3] + section[5]
    for other_index, other in enumerate(elf.sections):
        if other_index == index or not (other[2] & 0x2) or other[5] == 0:
            continue
        other_name = elf.names[other_index]
        other_overlay = re.fullmatch(r"\.file_(\d+)(?:_bss)?", other_name)
        if other_overlay and other_overlay.group(1) != "12":
            continue
        other_end = other[3] + other[5]
        if other[3] < section_end and section[3] < other_end:
            shared_name, shared_vma, shared_size, shared_flags, shared_align, shared_sha = (
                PINNED_SHARED_ALLOCATED_SECTION
            )
            if other_name == shared_name:
                if (other[1], other[2], other[3], other[5], other[8]) != (
                        1, shared_flags, shared_vma, shared_size, shared_align):
                    raise ValueError(f"{label} shared audio table section layout differs")
                if hashlib.sha256(elf.payload(other_index)).hexdigest() != shared_sha:
                    raise ValueError(f"{label} shared audio table section bytes differ")
                continue
            raise ValueError(f"{label} has an allocated section overlapping .file_12")
    payload = elf.payload(index)
    relocation_indices = [
        i for i, candidate in enumerate(elf.sections)
        if candidate[1] in (4, 9) and candidate[7] == index
    ]
    if (len(relocation_indices) != 1 or
            elf.sections[relocation_indices[0]][1] != 9 or
            elf.names[relocation_indices[0]] != ".rel.file_12"):
        raise ValueError(f"{label} must contain one .rel.file_12 relocation table")
    relocations = elf.relocations(index)
    if any(not section[3] <= item.offset < section[3] + section[5] or item.offset & 3
           for item in relocations):
        raise ValueError(f"{label} has a relocation outside aligned .file_12")
    return elf, index, section, payload, relocations


def _relocation_signature(elf: Elf32, section: tuple, relocation,
                          *, normalize_symbol_metadata=False) -> tuple:
    symbol = relocation.symbol
    symbol_section = (elf.names[symbol.section] if symbol.section < len(elf.names)
                      else f"SHN_{symbol.section:04X}")
    symbol_kind = symbol.kind
    if normalize_symbol_metadata:
        tail_vma, _, tail_alias, _, _ = TEXT_END_ALIAS
        expected_tail_vma = VMA_START + tail_vma - ROM_START
        if (symbol.name == tail_alias and symbol.value == expected_tail_vma and
                symbol_section in ("SHN_FFF1", ".file_12")):
            symbol_section = "FILE12_TEXT_END_ALIAS"
        # The output linker records global C data declarations as STT_OBJECT,
        # while the original assembly referenced the same globals as STT_NOTYPE.
        # Symbol name, address, section, binding and relocation type remain exact.
        if symbol_kind in (0, 1):
            symbol_kind = 0
    return (
        relocation.offset - section[3], relocation.relocation_type,
        symbol.name, symbol.value, symbol_section, symbol_kind, symbol.binding,
        relocation.addend is not None,
        relocation.addend if relocation.addend is not None else 0,
    )


def _section_relocations(elf: Elf32, section: tuple, relocations: tuple,
                         *, normalize_symbol_metadata=True) -> tuple:
    return tuple(sorted(_relocation_signature(
        elf, section, item, normalize_symbol_metadata=normalize_symbol_metadata
    )
                        for item in relocations))


def _function_relocations(elf: Elf32, section: tuple, relocations: tuple,
                          symbol, *, normalize_symbol_metadata=True) -> tuple:
    end = symbol.value + symbol.size
    return tuple(sorted(
        (item.offset - symbol.value, *_relocation_signature(
            elf, section, item,
            normalize_symbol_metadata=normalize_symbol_metadata
        )[1:])
        for item in relocations
        if symbol.value <= item.offset < end
    ))


def _relocation_metadata_normalizations(original_signatures: tuple,
                                        candidate_signatures: tuple) -> dict:
    if len(original_signatures) != len(candidate_signatures):
        raise ValueError("file_12 relocation table entry count changed")
    notype_to_object = 0
    tail_alias_section = 0
    tail_vma, _, tail_alias, _, _ = TEXT_END_ALIAS
    expected_tail_vma = VMA_START + tail_vma - ROM_START
    for original, candidate in zip(original_signatures, candidate_signatures):
        if original == candidate:
            continue
        without_kind = original[:5] + original[6:]
        candidate_without_kind = candidate[:5] + candidate[6:]
        if (without_kind == candidate_without_kind and
                {original[5], candidate[5]} == {0, 1}):
            notype_to_object += 1
            continue
        original_without_section = original[:4] + original[5:]
        candidate_without_section = candidate[:4] + candidate[5:]
        if (original_without_section == candidate_without_section and
                original[2] == tail_alias and original[3] == expected_tail_vma and
                original[4] in ("SHN_FFF1", ".file_12") and
                candidate[4] in ("SHN_FFF1", ".file_12")):
            tail_alias_section += 1
            continue
        raise ValueError("file_12 relocation target metadata changed beyond approved aliases")
    return {
        "notype_to_object_data_symbols": notype_to_object,
        "absolute_to_overlay_tail_alias": tail_alias_section,
        "rule": (
            "Preserve relocation offset, type, symbol name, resolved VMA, binding and addend; "
            "normalize STT_NOTYPE/STT_OBJECT for the same data symbol and the pinned "
            "0x5E3C8C zero-size file_12 tail alias section representation."
        ),
    }


def validate_linked_elf_provenance(splat_yaml: str, reference_rom: bytes,
                                   reference_elf: bytes, candidate_elf: bytes,
                                   function_names: tuple[str, ...]) -> dict:
    """Bind requested file_12 functions and the entire output section to ROM."""
    result = validate_reference_inputs(splat_yaml, reference_rom, function_names)
    reference_sha = hashlib.sha256(reference_elf).hexdigest()
    if reference_sha != REFERENCE_ELF_SHA256:
        raise ValueError("reference linked ELF identity mismatch")
    original, original_index, original_section, original_payload, original_relocations = (
        _linked_file12(reference_elf, "reference ELF")
    )
    candidate, candidate_index, candidate_section, candidate_payload, candidate_relocations = (
        _linked_file12(candidate_elf, "candidate ELF")
    )
    expected_overlay = reference_rom[ROM_START:ROM_END]
    if original_payload != expected_overlay:
        raise ValueError("reference ELF .file_12 bytes differ from mapped original ROM")

    def reject_function_aliases(elf: Elf32, section_index: int, symbol,
                                label: str) -> None:
        start, end = symbol.value, symbol.value + symbol.size
        for other in elf.symbols:
            if other.name == symbol.name or other.kind != 2 or other.section != section_index:
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
            raise ValueError(f"file_12 function name disagrees with VMA/ROM mapping: {name}")
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
        candidate_relocs_raw = _function_relocations(
            candidate, candidate_section, candidate_relocations, candidate_symbol,
            normalize_symbol_metadata=False,
        )
        if original_relocs != candidate_relocs:
            raise ValueError(f"candidate relocation target differs for {name}")
        expected_relocations = FUNCTION_RELOCATIONS[name]
        observed_relocations = tuple(
            (item[0], item[1], item[2]) for item in candidate_relocs
        )
        if observed_relocations != expected_relocations:
            raise ValueError(f"candidate relocation signature differs for {name}")
        function_results.append({
            "name": name, "section": ".file_12",
            "vma": f"0x{vma:08X}", "rom_offset": f"0x{rom_offset:X}",
            "bytes": size,
            "original_sha256": hashlib.sha256(original_code).hexdigest(),
            "candidate_sha256": hashlib.sha256(candidate_code).hexdigest(),
            "candidate_code_matches_original": True,
            "candidate_relocations_match_reference": True,
            "relocation_count": len(candidate_relocs),
            "relocations": [
                {"section_offset": f"0x{item[0]:X}", "type": item[1],
                 "symbol": item[2], "symbol_vma": f"0x{item[3]:08X}",
                 "symbol_section": item[4], "symbol_kind": item[5],
                 "symbol_binding": item[6], "addend": item[8] if item[7] else None}
                for item in candidate_relocs_raw
            ],
        })

    if candidate_payload != expected_overlay:
        raise ValueError("candidate ELF .file_12 bytes differ from mapped original ROM")
    original_section_relocs_raw = _section_relocations(
        original, original_section, original_relocations,
        normalize_symbol_metadata=False,
    )
    candidate_section_relocs_raw = _section_relocations(
        candidate, candidate_section, candidate_relocations,
        normalize_symbol_metadata=False,
    )
    relocation_normalizations = _relocation_metadata_normalizations(
        original_section_relocs_raw, candidate_section_relocs_raw
    )
    original_section_relocs = _section_relocations(
        original, original_section, original_relocations
    )
    candidate_section_relocs = _section_relocations(
        candidate, candidate_section, candidate_relocations
    )
    if original_section_relocs != candidate_section_relocs:
        raise ValueError("candidate .file_12 relocation table differs from original")

    original_rel_index = original.names.index(".rel.file_12")
    candidate_rel_index = candidate.names.index(".rel.file_12")
    original_rel_payload = original.payload(original_rel_index)
    candidate_rel_payload = candidate.payload(candidate_rel_index)

    result["linked_elf_provenance"] = {
        "format": "goemon-file12-linked-elf-provenance-v1",
        "reference_elf_sha256": reference_sha,
        "candidate_elf_sha256": hashlib.sha256(candidate_elf).hexdigest(),
        "reference_section": {
            "name": ".file_12", "vma_start": f"0x{original_section[3]:08X}",
            "elf_file_offset": f"0x{original_section[4]:X}",
            "size": original_section[5],
            "sha256": hashlib.sha256(original_payload).hexdigest(),
            "relocation_count": len(original_relocations),
        },
        "candidate_section": {
            "name": ".file_12", "vma_start": f"0x{candidate_section[3]:08X}",
            "elf_file_offset": f"0x{candidate_section[4]:X}",
            "size": candidate_section[5],
            "sha256": hashlib.sha256(candidate_payload).hexdigest(),
            "relocation_count": len(candidate_relocations),
        },
        "functions": function_results,
        "full_section_relocations_match": True,
        "full_section_relocations_semantically_match": True,
        "raw_relocation_section_bytes_identical": original_rel_payload == candidate_rel_payload,
        "reference_raw_relocation_sha256": hashlib.sha256(original_rel_payload).hexdigest(),
        "candidate_raw_relocation_sha256": hashlib.sha256(candidate_rel_payload).hexdigest(),
        "relocation_symbol_metadata_normalizations": relocation_normalizations,
        "promoted_matching_c": False,
        "proof_level": (
            "linked overlay symbol, whole section bytes, function bytes and semantic "
            "relocation targets; raw symbol-index section bytes are reported separately"
        ),
    }
    return result


def compare_full_rom(reference_rom: bytes, candidate_rom: bytes) -> None:
    if len(candidate_rom) != ROM_BYTES or candidate_rom != reference_rom:
        raise ValueError("candidate full decompressed ROM differs or is incomplete")
