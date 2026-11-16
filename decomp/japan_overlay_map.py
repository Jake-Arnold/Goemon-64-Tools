"""Generate candidate USA-to-Japan mappings within individual executable overlays.

Each code section's ROM and VRAM layout comes from the exact upstream Splat
configuration, never a global delta. Candidates require unique full-length
normalized MIPS matches. Does not build a playable Japanese recompilation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import struct
import tomllib

import yaml

from decomp.japan_function_map import (
    SIGNATURE_WORDS, _informative, _signature, japan_signature_index,
    normalized_instruction, read_verified_rom, SHA1,
)


@dataclass(frozen=True)
class TextSection:
    name: str
    rom: int
    vram: int
    end: int

    def words(self, rom_bytes: bytes) -> tuple[int, ...]:
        if not 0 <= self.rom < self.end <= len(rom_bytes):
            raise ValueError(f"Invalid text bounds: {self.name}")
        if (self.end - self.rom) % 4 or self.rom % 4 or self.vram % 4:
            raise ValueError(f"Unaligned text section: {self.name}")
        return struct.unpack_from(f">{(self.end-self.rom)//4}I", rom_bytes, self.rom)


CODE_TYPES = frozenset(("asm", "hasm", "c"))


def splat_text_sections(path: Path, region: str) -> dict[str, TextSection]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or doc.get("sha1") != SHA1[region]:
        raise ValueError(f"{region} Splat yaml does not match decompressed ROM SHA-1")
    segments = doc.get("segments")
    if not isinstance(segments, list):
        raise ValueError("Missing Splat segments")
    sections = {}
    for segment in segments:
        if not isinstance(segment, dict) or segment.get("type") != "code":
            continue
        name = segment.get("name")
        if not isinstance(name, str) or not (name in ("entry", "main") or name.startswith("file_")):
            continue
        start, vram = segment.get("start"), segment.get("vram")
        if type(start) is not int or type(vram) is not int:
            raise ValueError(f"Missing ROM/VRAM address for {name}")
        subsegments = segment.get("subsegments") or []
        first = next((x for x in subsegments if isinstance(x, list) and len(x) >= 2), None)
        if first is None or first[1] not in CODE_TYPES:
            continue  # Data-only files aren't MIPS code.
        end = next((item[0] for item in subsegments
                    if isinstance(item, list) and len(item) >= 2
                    and type(item[0]) is int and item[0] > start
                    and item[1] not in CODE_TYPES), None)
        if end is None:
            continue  # No explicit code/data boundary; do not guess.
        if name in sections or end <= start:
            raise ValueError(f"Invalid/duplicate Splat code section: {name}")
        sections[name] = TextSection("."+name, start, vram, end)
    return {section.name: section for section in sections.values()}


def original_symbols(path: Path) -> dict[str, tuple[dict, list[dict]]]:
    doc = tomllib.loads(path.read_text(encoding="utf-8"))
    result = {}
    for section in doc.get("section", []):
        name = section.get("name")
        if name in result:
            raise ValueError(f"Duplicate original symbol section: {name}")
        result[name] = (section, section.get("functions", []))
    return result


def map_sections(us_rom: bytes, jp_rom: bytes, us_splat: Path, jp_splat: Path,
                 us_syms: Path) -> dict:
    us_sections = splat_text_sections(us_splat, "usa")
    jp_sections = splat_text_sections(jp_splat, "japan_0")
    us_symbols = original_symbols(us_syms)
    result, summaries, totals = [], [], defaultdict(int)
    for name in sorted(us_sections, key=lambda x: (x != ".main", x)):
        us_sec, jp_sec, symbol_entry = us_sections[name], jp_sections.get(name), us_symbols.get(name)
        if jp_sec is None or symbol_entry is None:
            continue
        doc, functions = symbol_entry
        if (doc["rom"], doc["vram"]) != (us_sec.rom, us_sec.vram):
            raise ValueError(f"Symbol/Splat address disagreement in {name}")
        a, b = us_sec.words(us_rom), jp_sec.words(jp_rom)
        jp_index = japan_signature_index(b)
        matches, counts = [], defaultdict(int)
        for fn in functions:
            counts["symbol_functions"] += 1
            addr, size = fn["vram"], fn["size"]
            if type(addr) is not int or type(size) is not int or addr % 4 or size % 4 or size < 4:
                raise ValueError(f"Invalid original symbol in {name}")
            us_pos, word_count = (addr-us_sec.vram)//4, size//4
            if us_pos < 0 or us_pos + word_count > len(a):
                counts["outside_executable"] += 1
                continue
            if word_count < SIGNATURE_WORDS:
                counts["too_small"] += 1
                continue
            sig = _signature(a, us_pos)
            if not _informative(sig):
                counts["weak_signature"] += 1
                continue
            positions = jp_index.get(sig, [])
            if len(positions) != 1:
                counts["ambiguous_or_missing"] += 1
                continue
            jp_pos = positions[0]
            if jp_pos + word_count > len(b):
                counts["outside_japan_executable"] += 1
                continue
            if (tuple(map(normalized_instruction, a[us_pos:us_pos+word_count])) !=
                    tuple(map(normalized_instruction, b[jp_pos:jp_pos+word_count]))):
                counts["prologue_only"] += 1
                continue
            exact = sum(x == y for x, y in zip(
                a[us_pos:us_pos+word_count], b[jp_pos:jp_pos+word_count]))
            counts["fully_matching_structure"] += 1
            matches.append({
                "section": name, "usa_name": fn["name"],
                "usa_vram": f"0x{addr:08X}",
                "japan_vram": f"0x{jp_sec.vram+jp_pos*4:08X}",
                "usa_rom": f"0x{us_sec.rom+us_pos*4:X}",
                "japan_rom": f"0x{jp_sec.rom+jp_pos*4:X}",
                "size": size, "exact_instruction_words": exact,
                "total_instruction_words": word_count,
            })
        reverse = defaultdict(list)
        for item in matches:
            reverse[item["japan_vram"]].append(item)
        collisions = {addr for addr, items in reverse.items() if len(items) > 1}
        counts["collisions"] = len(collisions)
        matches = [m for m in matches if m["japan_vram"] not in collisions]
        counts["unambiguous_full_shape_matches"] = len(matches)
        result.extend(matches)
        for key, value in counts.items():
            totals[key] += value
        summaries.append({
            "section": name, "us_code_rom": f"0x{us_sec.rom:X}",
            "jp_code_rom": f"0x{jp_sec.rom:X}", "counts": dict(counts),
        })
    return {
        "format": "goemon-japan-overlay-structural-map-v1",
        "sha1": dict(SHA1),
        "warnings": [
            "Not a complete Japanese N64Recomp symbol table or playable port.",
            "Full structural equality masks I-format immediate and JAL target operands.",
            "Check dynamic behaviour and machine-code details before porting patches.",
        ],
        "totals": dict(totals), "sections": summaries,
        "mappings": sorted(result, key=lambda m: (m["section"], int(m["usa_vram"], 16))),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("usa_decompressed", type=Path)
    ap.add_argument("japan_decompressed", type=Path)
    ap.add_argument("--us-splat", type=Path, required=True)
    ap.add_argument("--jp-splat", type=Path, required=True)
    ap.add_argument("--us-symbols", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    result = map_sections(
        read_verified_rom(args.usa_decompressed, "usa"),
        read_verified_rom(args.japan_decompressed, "japan_0"),
        args.us_splat, args.jp_splat, args.us_symbols)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(f"{len(result['sections'])} executable sections; "
          f"{result['totals'].get('unambiguous_full_shape_matches', 0)} full-shape mappings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
