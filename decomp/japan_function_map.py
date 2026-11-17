"""Relocation-tolerant, candidate-only USA-to-Japan Goemon main-code map.

Exact verified 32 MiB decompressed images required. MIPS immediate/jump
operands are masked, so a match is NOT evidence of equivalent game behaviour.
No ROM or assets are exported. Use --us-symbols for full-function checks.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import struct
import tomllib
from typing import Any

ROM_SIZE = 0x2000000
SHA1 = {
    "usa": "6ea0ed71032ce08fc2745f412d84936382197494",
    "japan_0": "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
}
MAIN_START = 0x1050
MAIN_END = {"usa": 0x531B0, "japan_0": 0x53430}
MAIN_VRAM = 0x80000450
SIGNATURE_WORDS = 16


def read_verified_rom(path: Path, region: str) -> bytes:
    if region not in SHA1:
        raise ValueError(f"Unsupported region: {region}")
    data = path.read_bytes()
    if len(data) != ROM_SIZE:
        raise ValueError(f"{region} requires a 32 MiB decompressed image")
    if data[:4] != bytes.fromhex("80371240"):
        raise ValueError("Decompressed ROM must have canonical .z64 byte order")
    digest = hashlib.sha1(data).hexdigest()
    if digest != SHA1[region]:
        raise ValueError(f"{region} decompressed SHA-1 mismatch: {digest}")
    return data


def normalized_instruction(word: int) -> int:
    """Preserve opcode/register/funct bits; remove immediates and J/JAL target.

    R-format instructions preserve every bit; COP opcodes retain all bits
    except coprocessor branches. I-format masks all 16 immediate bits.
    """
    op = word >> 26
    if op in (2, 3):
        return word & 0xFC000000
    if op in (0, 0x1C, 0x1F):
        return word
    if op in (0x10, 0x11, 0x12, 0x13):
        return word & 0xFFFF0000 if ((word >> 21) & 31) == 8 else word
    return word & 0xFFFF0000


def main_words(rom: bytes, region: str) -> tuple[int, ...]:
    first, last = MAIN_START, MAIN_END[region]
    return struct.unpack_from(f">{(last-first)//4}I", rom, first)


def _signature(words: tuple[int, ...], pos: int,
               count: int = SIGNATURE_WORDS) -> tuple[int, ...]:
    return tuple(map(normalized_instruction, words[pos:pos + count]))


def _informative(signature: tuple[int, ...]) -> bool:
    return (len(signature) == SIGNATURE_WORDS and
            signature.count(0) < 4 and len(set(signature)) >= 7)


def japan_signature_index(words: tuple[int, ...]) -> dict[tuple[int, ...], list[int]]:
    result = defaultdict(list)
    for pos in range(len(words) - SIGNATURE_WORDS + 1):
        signature = _signature(words, pos)
        if _informative(signature):
            result[signature].append(pos)
    return result


def jal_entrypoints(words: tuple[int, ...]) -> list[int]:
    """Only MIPS JAL targets within this main code; ignores indirect calls."""
    found = set()
    for word in words:
        if word >> 26 != 3:
            continue
        target = 0x80000000 | ((word & 0x03FFFFFF) << 2)
        pos = (target - MAIN_VRAM) // 4
        if MAIN_VRAM <= target < MAIN_VRAM + len(words)*4 and target % 4 == 0:
            found.add(pos)
    return sorted(found)


def symbol_entrypoints(path: Path) -> list[tuple[int, int, str]]:
    """Read original USA N64Recomp .main function bounds, not guessed sizes."""
    doc: dict[str, Any] = tomllib.loads(path.read_text(encoding="utf-8"))
    sections = [x for x in doc.get("section", []) if x.get("name") == ".main"]
    if len(sections) != 1:
        raise ValueError("Expected exactly one original N64Recomp .main section")
    result, seen = [], set()
    for fn in sections[0].get("functions", []):
        addr, size, name = fn["vram"], fn["size"], fn["name"]
        if type(addr) is not int or type(size) is not int or not isinstance(name, str):
            raise ValueError("Invalid N64Recomp function entry")
        if size < 4 or size % 4 or addr % 4:
            raise ValueError(f"Invalid function range for {name}")
        if not (MAIN_VRAM <= addr and addr + size <= MAIN_VRAM + MAIN_END["usa"] - MAIN_START):
            continue
        pos = (addr - MAIN_VRAM) // 4
        if pos in seen:
            raise ValueError(f"Duplicate USA symbol start {name}")
        seen.add(pos)
        result.append((pos, size // 4, name))
    return sorted(result)


def compare_main_code(usa: bytes, japan: bytes, us_symbols: Path | None = None) -> dict:
    us, jp = main_words(usa, "usa"), main_words(japan, "japan_0")
    index = japan_signature_index(jp)
    entries = (symbol_entrypoints(us_symbols) if us_symbols else
               [(p, None, f"direct_jal_0x{MAIN_VRAM+p*4:08X}")
                for p in jal_entrypoints(us)])
    mapped, stats = [], defaultdict(int)
    for us_pos, size_words, name in entries:
        stats["candidates"] += 1
        if us_pos + SIGNATURE_WORDS > len(us):
            stats["outside_main"] += 1
            continue
        signature = _signature(us, us_pos)
        if not _informative(signature):
            stats["noninformative"] += 1
            continue
        locations = index.get(signature, [])
        if len(locations) != 1:
            stats["no_unique_start"] += 1
            continue
        jp_pos = locations[0]
        if size_words is not None and jp_pos + size_words > len(jp):
            stats["out_of_bounds"] += 1
            continue
        full_shape = size_words is not None and (
            tuple(map(normalized_instruction, us[us_pos:us_pos+size_words])) ==
            tuple(map(normalized_instruction, jp[jp_pos:jp_pos+size_words])))
        compared = size_words or SIGNATURE_WORDS
        exact = sum(a == b for a, b in zip(us[us_pos:us_pos+compared],
                                         jp[jp_pos:jp_pos+compared]))
        stats["unique_start"] += 1
        if full_shape:
            stats["full_structural_match"] += 1
        item = {
            "usa_vram": f"0x{MAIN_VRAM+us_pos*4:08X}",
            "japan_vram": f"0x{MAIN_VRAM+jp_pos*4:08X}",
            "usa_rom": f"0x{MAIN_START+us_pos*4:X}",
            "japan_rom": f"0x{MAIN_START+jp_pos*4:X}",
            "name": name,
            "kind": "full_structure_match" if full_shape else "start_anchor_only",
            "compared_instructions": compared,
            "exact_instructions": exact,
        }
        if size_words is not None:
            item["usa_size"] = size_words*4
        mapped.append(item)
    reverse = defaultdict(list)
    for item in mapped:
        reverse[item["japan_vram"]].append(item)
    duplicates = {addr for addr, items in reverse.items() if len(items) > 1}
    stats["collision_candidates"] = len(duplicates)
    mapped = [m for m in mapped if m["japan_vram"] not in duplicates]
    mapped.sort(key=lambda x: int(x["usa_vram"], 16))
    stats["unambiguous_mappings"] = len(mapped)
    return {
        "format": "goemon-japan-structural-function-candidates-v1",
        "sources": dict(SHA1),
        "mode": "us_symbol_bounds" if us_symbols else "direct_jal_starts",
        "signature_instructions": SIGNATURE_WORDS,
        "stats": dict(stats),
        "warnings": [
            "NOT a runnable Japanese N64Recomp symbol table.",
            "Immediate operands are masked; full structure does not prove semantics.",
            "Indirect-only functions and ambiguous matches are excluded.",
            "ROM/VRAM code addresses cannot translate toolkit runtime RAM fields.",
        ],
        "mappings": mapped,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("usa_decompressed", type=Path)
    ap.add_argument("japan_decompressed", type=Path)
    ap.add_argument("--us-symbols", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    result = compare_main_code(
        read_verified_rom(args.usa_decompressed, "usa"),
        read_verified_rom(args.japan_decompressed, "japan_0"),
        args.us_symbols)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["stats"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
