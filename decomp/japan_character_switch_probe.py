"""Read-only JP character-switch overlay identification from known Project64 MIPS.

Requires the verified 32 MiB Japan-0 decompressed ROM and its pinned Splat YAML.
This is a research probe, not matching C and not a ROM builder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
import struct

JP_SHA1 = "6f8745fecc3a5e7d4918c7a73353eb0726116ded"
TRACE_START = 0x801E2944
TRACE_END = 0x801E29A0
# Only instructions independently visible in the Project64 debugger trace.
# The gap at 0x801E2958..0x801E296C is deliberately not guessed.
EXPECTED = {
    0x801E2944: 0xAC590004,  # sw t9, 4(v0)
    0x801E2948: 0xAC49002C,  # sw t1, 0x2c(v0)
    0x801E294C: 0x92050060,  # lbu a1, 0x60(s0)
    0x801E2950: 0x0C078A5C,  # jal 0x801E2970
    0x801E2954: 0x02002025,  # or a0, s0, zero (delay slot)
    0x801E2970: 0x27BDFFE8,  # addiu sp, sp, -0x18
    0x801E2974: 0x00A03025,  # or a2, a1, zero
    0x801E2978: 0xAFBF0014,  # sw ra, 0x14(sp)
    0x801E297C: 0xAFA5001C,  # sw a1, 0x1c(sp)
    0x801E2980: 0xA0860060,  # sb a2, 0x60(a0)
    0x801E2984: 0x30CE00FF,  # andi t6, a2, 0xff
    0x801E2988: 0x3C018016,  # lui at, 0x8016
    0x801E298C: 0xAC2E1DCC,  # sw t6, 0x1dcc(at)
    0x801E2990: 0x8C8F005C,  # lw t7, 0x5c(a0)
    0x801E2994: 0x24020001,  # addiu v0, zero, 1
    0x801E2998: 0x44800000,  # mtc1 zero, f0
    0x801E299C: 0xA1E20069,  # sb v0, 0x69(t7)
    0x801E29A0: 0x8C98005C,  # lw t8, 0x5c(a0)
}

@dataclass(frozen=True)
class Overlay:
    name: str
    rom_start: int
    vram_start: int
    code_end: int

    def offset(self, addr: int) -> int:
        return self.rom_start + addr - self.vram_start


def candidate_overlays(layout: dict) -> list[Overlay]:
    """Identify all overlapping executable overlays without assuming file ID."""
    if layout.get("sha1") != JP_SHA1:
        raise ValueError("Japanese Splat config checksum does not identify Japan-0")
    matches = []
    for item in layout.get("segments", []):
        if not isinstance(item, dict) or item.get("type") != "code" or not item.get("overlay"):
            continue
        rom_start, vram_start = item.get("start"), item.get("vram")
        if type(rom_start) is not int or type(vram_start) is not int:
            continue
        subsegments = item.get("subsegments", [])
        # All of the trace must lie before the first non-code subsegment.
        first_noncode = next((s[0] for s in subsegments if isinstance(s, list)
                              and len(s) >= 2 and isinstance(s[0], int)
                              and s[0] > rom_start and s[1] not in ("asm", "hasm", "c")), None)
        if first_noncode is None:
            continue
        if vram_start <= TRACE_START and TRACE_END < vram_start + first_noncode - rom_start:
            matches.append(Overlay(str(item["name"]), rom_start, vram_start, first_noncode))
    return matches


def probe(rom: bytes, layout: dict) -> dict:
    """Compare exact MIPS words: no unsafe reads, guessed offsets or code export."""
    candidates = []
    for overlay in candidate_overlays(layout):
        differences = []
        for addr, expected in EXPECTED.items():
            offset = overlay.offset(addr)
            if offset < overlay.rom_start or offset + 4 > overlay.code_end or offset + 4 > len(rom):
                differences.append({"vram": f"0x{addr:08X}", "error": "out of bounds"})
                continue
            actual = struct.unpack_from(">I", rom, offset)[0]
            if actual != expected:
                differences.append({"vram": f"0x{addr:08X}", "expected": f"0x{expected:08X}",
                                    "actual": f"0x{actual:08X}"})
        candidates.append({
            "overlay": overlay.name,
            "rom_caller": f"0x{overlay.offset(0x801E2944):X}",
            "rom_callee": f"0x{overlay.offset(0x801E2970):X}",
            "checked_words": len(EXPECTED),
            "matching_words": len(EXPECTED) - len(differences),
            "matches_trace": not differences,
            "mismatches": differences,
        })
    matches = [c["overlay"] for c in candidates if c["matches_trace"]]
    return {
        "format": "goemon-japan-character-switch-trace-probe-v1",
        "japan_rom_sha1": JP_SHA1,
        "evidence": "Project64 native switch step trace 2026-11-15; partial instructions only",
        "candidate_overlays": candidates,
        "matching_overlays": matches,
        "identified_uniquely": len(matches) == 1,
        "warnings": ["A matching instruction trace is not a complete function boundary, C match or runtime proof.",
                     "No ROM bytes or extracted game code are included in this report."],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("japan_decompressed", type=Path)
    parser.add_argument("--splat", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    rom = args.japan_decompressed.read_bytes()
    if len(rom) != 0x2000000 or hashlib.sha1(rom).hexdigest() != JP_SHA1:
        parser.error("Japan-0 expanded 32 MiB ROM does not match expected SHA-1")
    try:
        import yaml
    except ImportError:
        parser.error("PyYAML is required to parse the pinned Splat configuration")
    result = probe(rom, yaml.safe_load(args.splat.read_text(encoding="utf-8")))
    out = json.dumps(result, indent=2) + "\n"
    if args.report:
        args.report.write_text(out, encoding="utf-8")
    else:
        print(out, end="")
    return 0 if result["identified_uniquely"] else 2


if __name__ == "__main__":
    raise SystemExit(main())