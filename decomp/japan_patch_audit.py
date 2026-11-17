"""Verify a prospective Japanese audio patch against exact original MIPS code.

An audit does not patch a ROM, game process, or recompiled executable. All
region-specific changes still require a Japanese N64Recomp symbol table and
native runtime testing. The hardcoded USA patch metadata is from upstream
Goemon64Recomp/mnsg.toml on the dev branch.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

from decomp.japan_function_map import (
    MAIN_START, MAIN_END, MAIN_VRAM, SIGNATURE_WORDS,
    _signature, normalized_instruction, read_verified_rom,
)

USA_ENTRYPOINT = 0x80038210
USA_PATCH = 0x80038290
USA_SIZE = 0x1B4  # N64Recomp original USA func_80038210_38E10 symbol bound
EXPECTED_OLD = 0x00E3082B
PATCH_WORD = 0x00E3082A


def _words(rom: bytes, region: str) -> tuple[int, ...]:
    end = MAIN_END[region]
    return struct.unpack_from(f">{(end-MAIN_START)//4}I", rom, MAIN_START)


def audit_patch(usa: bytes, japan: bytes) -> dict:
    us, jp = _words(usa, "usa"), _words(japan, "japan_0")
    first = (USA_ENTRYPOINT - MAIN_VRAM) // 4
    patch = (USA_PATCH - MAIN_VRAM) // 4
    count = USA_SIZE // 4
    if not (0 <= first < len(us) and first + count <= len(us) and first <= patch < first + count):
        raise ValueError("USA patch is outside verified main-function bounds")
    if us[patch] != EXPECTED_OLD:
        raise ValueError(f"USA original instruction changed: 0x{us[patch]:08X}")
    signature = _signature(us, first)
    locations = [pos for pos in range(len(jp) - SIGNATURE_WORDS + 1)
                 if _signature(jp, pos) == signature]
    if len(locations) != 1:
        raise ValueError(f"Japanese function anchor ambiguous or absent: {len(locations)} matches")
    jp_first = locations[0]
    if jp_first + count > len(jp):
        raise ValueError("Japanese equivalent function would extend beyond main code")
    us_fn = us[first:first+count]
    jp_fn = jp[jp_first:jp_first+count]
    jp_patch = jp_first + (patch - first)
    if jp[jp_patch] != EXPECTED_OLD:
        raise ValueError(f"Japanese original patch instruction differs: 0x{jp[jp_patch]:08X}")
    if any(normalized_instruction(a) != normalized_instruction(b)
           for a, b in zip(us_fn, jp_fn)):
        raise ValueError("Japanese function does not preserve complete normalized instruction structure")
    return {
        "type": "unapplied-japan-0-audio-patch-candidate",
        "usa_function": "func_80038210_38E10",
        "usa_function_vram": f"0x{USA_ENTRYPOINT:08X}",
        "japan_function_vram": f"0x{MAIN_VRAM+4*jp_first:08X}",
        "usa_patch_vram": f"0x{USA_PATCH:08X}",
        "japan_patch_vram": f"0x{MAIN_VRAM+4*jp_patch:08X}",
        "japan_patch_rom": f"0x{MAIN_START+4*jp_patch:X}",
        "function_bytes_checked": USA_SIZE,
        "structurally_equal_words": count,
        "exactly_equal_words": sum(a == b for a, b in zip(us_fn, jp_fn)),
        "original_instruction": f"0x{EXPECTED_OLD:08X}",
        "proposed_instruction": f"0x{PATCH_WORD:08X}",
        "status": "candidate verified against retail code; NOT applied or gameplay tested",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("usa_decompressed", type=Path)
    ap.add_argument("japan_decompressed", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    report = audit_patch(read_verified_rom(args.usa_decompressed, "usa"),
                         read_verified_rom(args.japan_decompressed, "japan_0"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(f"Japanese candidate {report['japan_patch_vram']}: "
          f"{report['structurally_equal_words']} structurally equal instructions; not applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
