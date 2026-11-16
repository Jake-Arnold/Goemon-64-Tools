"""Find tentative USA-to-Japan *direct JAL* function entrypoints per overlay.

No imported USA symbol table is required for this pass. The output is a list
of unique 16-instruction anchor candidates, NOT a complete function map or a
Japanese recompilation. ROMs and Splat configs must match pinned SHA-1s.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from decomp.japan_function_map import (
    SIGNATURE_WORDS, _informative, _signature, japan_signature_index,
    read_verified_rom, SHA1,
)
from decomp.japan_overlay_map import splat_text_sections


def jal_target(instruction: int, pc: int) -> int | None:
    """Resolve the MIPS JAL upper-PC nibble, including 0x08000000 overlays."""
    if instruction >> 26 != 3:
        return None
    return ((pc + 4) & 0xF0000000) | ((instruction & 0x03FFFFFF) << 2)


def direct_targets(words: tuple[int, ...], base_vram: int) -> tuple[set[int], int]:
    """Return distinct in-section direct call target positions and JAL count."""
    found: set[int] = set()
    site_count = 0
    end = base_vram + len(words) * 4
    for i, ins in enumerate(words):
        target = jal_target(ins, base_vram + i * 4)
        if target is None:
            continue
        site_count += 1
        if base_vram <= target < end and target % 4 == 0:
            found.add((target - base_vram) // 4)
    return found, site_count


def map_jal_overlays(us: bytes, jp: bytes, us_splat: Path, jp_splat: Path) -> dict:
    us_sects = splat_text_sections(us_splat, "usa")
    jp_sects = splat_text_sections(jp_splat, "japan_0")
    mappings, sections, totals = [], [], Counter()
    for name in sorted(us_sects, key=lambda x: (x != ".main", x)):
        a, b = us_sects[name], jp_sects.get(name)
        if b is None:
            continue
        uswords = a.words(us)
        jpwords = b.words(jp)
        jpindex = japan_signature_index(jpwords)
        positions, num_jal = direct_targets(uswords, a.vram)
        counts = Counter(jal_instructions=num_jal, distinct_within_section=len(positions))
        possible = []
        for pos in sorted(positions):
            if pos + SIGNATURE_WORDS > len(uswords):
                counts["near_code_end"] += 1
                continue
            signature = _signature(uswords, pos)
            if not _informative(signature):
                counts["uninformative"] += 1
                continue
            candidates = jpindex.get(signature, [])
            if len(candidates) != 1:
                counts["ambiguous_or_absent"] += 1
                continue
            target = candidates[0]
            counts["unique_anchor"] += 1
            usa16, jp16 = uswords[pos:pos + SIGNATURE_WORDS], jpwords[target:target + SIGNATURE_WORDS]
            possible.append({
                "section": name,
                "usa_vram": f"0x{a.vram+pos*4:08X}",
                "japan_vram": f"0x{b.vram+target*4:08X}",
                "usa_rom": f"0x{a.rom+pos*4:X}",
                "japan_rom": f"0x{b.rom+target*4:X}",
                "signature_words": SIGNATURE_WORDS,
                "exact_words": sum(x == y for x, y in zip(usa16, jp16)),
            })
        reverse = defaultdict(list)
        for entry in possible:
            reverse[entry["japan_vram"]].append(entry)
        bad = {addr for addr, entries in reverse.items() if len(entries) > 1}
        counts["destination_collisions"] = len(bad)
        accepted = [entry for entry in possible if entry["japan_vram"] not in bad]
        counts["unambiguous_starts"] = len(accepted)
        mappings.extend(accepted)
        totals.update(counts)
        sections.append({
            "section": name,
            "usa_rom": f"0x{a.rom:X}",
            "japan_rom": f"0x{b.rom:X}",
            "usa_vram": f"0x{a.vram:X}",
            "japan_vram": f"0x{b.vram:X}",
            "counts": dict(counts),
        })
    return {
        "format": "goemon-japan-overlay-direct-jal-anchors-v1",
        "sha1": dict(SHA1),
        "signature_words": SIGNATURE_WORDS,
        "warnings": [
            "Direct-JAL target addresses only: indirect calls, tail calls, internal data and uncalled functions omitted.",
            "Full function size and semantics are unknown. An anchor is not safe as an N64Recomp symbol.",
            "Immediate and jump operands are masked and must be audited before porting patches.",
            "Overlays with identical runtime addresses are intentionally scoped by file/section identity.",
        ],
        "totals": dict(totals),
        "sections": sections,
        "mappings": sorted(mappings, key=lambda x: (x["section"], int(x["usa_rom"], 16))),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("usa_decompressed", type=Path)
    ap.add_argument("japan_decompressed", type=Path)
    ap.add_argument("--us-splat", type=Path, required=True)
    ap.add_argument("--jp-splat", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    report = map_jal_overlays(
        read_verified_rom(args.usa_decompressed, "usa"),
        read_verified_rom(args.japan_decompressed, "japan_0"),
        args.us_splat, args.jp_splat,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{len(report['sections'])} sections, {report['totals'].get('unambiguous_starts', 0)} "
          "unambiguous call-target anchors (NOT complete function matches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
