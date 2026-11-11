"""Validate explicit overlay mappings and provenance without inferring a VMA formula."""
from __future__ import annotations

import re

ROM_SIZE = 33_554_432
SHA1 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FUNCTION = re.compile(r"func_([0-9A-F]{8})_([0-9A-F]+)\Z")
SAFE_PATH = re.compile(r"[A-Za-z0-9_./-]+\Z")


def _require_keys(value: dict, expected: set[str], where: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"invalid {where} fields")


def _require_range(start: int, end: int, limit: int, where: str) -> None:
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= limit:
        raise ValueError(f"invalid {where} range")


def _require_hash(value: str, pattern: re.Pattern[str], where: str) -> None:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise ValueError(f"invalid {where} hash")


def validate_overlay_manifest(manifest: dict) -> dict:
    """Check overlay sections and function ownership using explicitly supplied addresses.

    VMA values are validated against declared section ranges. The main-segment
    ROM/VMA offset rule is deliberately absent from this schema.
    """
    _require_keys(manifest, {"format", "reference_rom_sha1", "overlays"}, "manifest")
    if manifest["format"] != "goemon-overlay-manifest-v1":
        raise ValueError("unsupported overlay manifest format")
    _require_hash(manifest["reference_rom_sha1"], SHA1, "reference ROM SHA-1")
    overlays = manifest["overlays"]
    if not isinstance(overlays, list) or not overlays:
        raise ValueError("overlay manifest must contain overlays")

    seen_ids: set[str] = set()
    seen_functions: set[str] = set()
    overlay_rom_ranges: list[tuple[int, int]] = []
    overlay_vma_ranges: list[tuple[int, int]] = []
    function_rom_ranges: list[tuple[int, int]] = []
    function_vma_ranges: list[tuple[int, int]] = []

    for overlay in overlays:
        _require_keys(overlay, {
            "id", "exclusive_ram_id", "rom_start", "rom_end", "vma_start",
            "vma_end", "alignment", "sections", "functions",
        }, "overlay")
        overlay_id = overlay["id"]
        if (not isinstance(overlay_id, str) or SAFE_PATH.fullmatch(overlay_id) is None or
                "/" in overlay_id or overlay_id in seen_ids):
            raise ValueError("invalid or duplicate overlay ID")
        seen_ids.add(overlay_id)
        if (not isinstance(overlay["exclusive_ram_id"], str) or
                SAFE_PATH.fullmatch(overlay["exclusive_ram_id"]) is None):
            raise ValueError("invalid overlay RAM ID")
        _require_range(overlay["rom_start"], overlay["rom_end"], ROM_SIZE, "overlay ROM")
        _require_range(overlay["vma_start"], overlay["vma_end"], 1 << 32, "overlay VMA")
        alignment = overlay["alignment"]
        if type(alignment) is not int or alignment < 1 or alignment & (alignment - 1):
            raise ValueError("overlay alignment must be a positive power of two")
        if overlay["rom_start"] % alignment or overlay["vma_start"] % alignment:
            raise ValueError("overlay segment alignment is not satisfied")
        overlay_rom_ranges.append((overlay["rom_start"], overlay["rom_end"]))
        overlay_vma_ranges.append((overlay["vma_start"], overlay["vma_end"]))

        sections = overlay["sections"]
        functions = overlay["functions"]
        if not isinstance(sections, list) or not sections or not isinstance(functions, list):
            raise ValueError("overlay sections and functions must be lists")
        section_ranges: dict[str, tuple[int | None, int | None, int, int]] = {}
        for section in sections:
            if not isinstance(section, dict) or "name" not in section:
                raise ValueError("invalid section fields")
            name = section["name"]
            if not isinstance(name, str) or name not in {"text", "rodata", "data", "bss"} or name in section_ranges:
                raise ValueError("invalid or duplicate overlay section")
            expected = {"name", "vma_start", "vma_end", "alignment"}
            if name == "bss":
                _require_keys(section, expected, "BSS section")
                rom_start = rom_end = None
            else:
                _require_keys(section, expected | {"rom_start", "rom_end", "sha256"}, "section")
                rom_start, rom_end = section["rom_start"], section["rom_end"]
                _require_range(rom_start, rom_end, ROM_SIZE, "section ROM")
            _require_range(section["vma_start"], section["vma_end"], 1 << 32, "section VMA")
            if (name != "bss" and rom_end - rom_start !=
                    section["vma_end"] - section["vma_start"]):
                raise ValueError("overlay section ROM and VMA extents differ")
            section_alignment = section["alignment"]
            if (type(section_alignment) is not int or section_alignment < 1 or
                    section_alignment & (section_alignment - 1)):
                raise ValueError("section alignment must be a positive power of two")
            if ((name != "bss" and rom_start % section_alignment) or
                    section["vma_start"] % section_alignment):
                raise ValueError("overlay section alignment is not satisfied")
            in_rom = (name == "bss" or
                      overlay["rom_start"] <= rom_start < rom_end <= overlay["rom_end"])
            in_vma = (overlay["vma_start"] <= section["vma_start"] <
                      section["vma_end"] <= overlay["vma_end"])
            if not (in_rom and in_vma):
                raise ValueError("overlay section lies outside its segment")
            if name != "bss":
                _require_hash(section["sha256"], SHA256, "section SHA-256")
            section_ranges[name] = (rom_start, rom_end,
                                    section["vma_start"], section["vma_end"])

        for section_name, (start, end, vma_start, vma_end) in section_ranges.items():
            for other_name, (other_start, other_end, other_vma_start, other_vma_end) in section_ranges.items():
                if section_name >= other_name:
                    continue
                if (start is not None and other_start is not None and
                        start < other_end and other_start < end):
                    raise ValueError("overlay sections overlap in ROM")
                if vma_start < other_vma_end and other_vma_start < vma_end:
                    raise ValueError("overlay sections overlap in VMA")

        for function in functions:
            _require_keys(function, {
                "name", "section", "rom_offset", "vma", "size", "source_owner",
                "source_sha256", "object_sha256", "relocation_sha256", "original_sha256",
            }, "function")
            name = function["name"]
            match = FUNCTION.fullmatch(name) if isinstance(name, str) else None
            if match is None or name in seen_functions:
                raise ValueError("invalid or duplicate overlay function")
            seen_functions.add(name)
            if (type(function["vma"]) is not int or type(function["rom_offset"]) is not int or
                    int(match.group(1), 16) != function["vma"] or
                    int(match.group(2), 16) != function["rom_offset"]):
                raise ValueError("overlay function name disagrees with explicit addresses")
            size = function["size"]
            if type(size) is not int or size <= 0 or size % 4:
                raise ValueError("invalid overlay function size")
            section_name = function["section"]
            section = section_ranges.get(section_name) if isinstance(section_name, str) else None
            if section is None or section_name != "text":
                raise ValueError("overlay function references an unknown section")
            rom_start, rom_end, vma_start, vma_end = section
            offset, address = function["rom_offset"], function["vma"]
            if (type(offset) is not int or type(address) is not int or offset % 4 or address % 4 or
                    rom_start is None or rom_end is None or
                    not (rom_start <= offset and offset + size <= rom_end and
                         vma_start <= address and address + size <= vma_end)):
                raise ValueError("overlay function lies outside its section")
            owner = function["source_owner"]
            if (not isinstance(owner, str) or SAFE_PATH.fullmatch(owner) is None or
                    ".." in owner.split("/") or owner.startswith("/")):
                raise ValueError("invalid overlay source owner")
            for field in ("source_sha256", "object_sha256", "relocation_sha256", "original_sha256"):
                _require_hash(function[field], SHA256, field)
            function_rom_ranges.append((offset, offset + size))
            function_vma_ranges.append((address, address + size))

    overlay_rom_ranges.sort()
    if any(left[1] > right[0] for left, right in zip(overlay_rom_ranges, overlay_rom_ranges[1:])):
        raise ValueError("overlay ROM segments overlap")
    overlay_vma_ranges.sort()
    if any(left[1] > right[0] for left, right in zip(overlay_vma_ranges, overlay_vma_ranges[1:])):
        raise ValueError("overlay VMA segments overlap")
    function_rom_ranges.sort()
    if any(left[1] > right[0] for left, right in zip(function_rom_ranges, function_rom_ranges[1:])):
        raise ValueError("overlay functions overlap in ROM")
    function_vma_ranges.sort()
    if any(left[1] > right[0] for left, right in zip(function_vma_ranges, function_vma_ranges[1:])):
        raise ValueError("overlay functions overlap in VMA")

    return {"overlay_count": len(overlays), "function_count": len(seen_functions),
            "proof_level": "explicit layout and provenance only"}
