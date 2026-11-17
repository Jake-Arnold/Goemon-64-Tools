"""Compare verified USA/Japan Goemon 64 ROMs without exporting game data.

The result maps byte-identical ROM spans; it is not a guest RAM address mapper,
proof of function equivalence, or a runnable Japanese recompilation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROM_SIZE = 16 * 1024 * 1024
ROM_SHA1 = {
    "USA": "df8083a54296b8c151917c5333e1c85f014a2a66",
    "Japan": "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b",
}
ROM_GAME_CODES = {"USA": b"NG5E", "Japan": b"NG5J"}


def normalize_byte_order(data: bytes) -> bytes:
    """Return canonical big-endian .z64 bytes; reject unknown headers."""
    if len(data) % 4:
        raise ValueError("ROM length must be divisible by four")
    signature = data[:4]
    if signature == b"\x80\x37\x12\x40":
        return data
    if signature == b"\x37\x80\x40\x12":  # .v64 (16-bit swapped)
        out = bytearray(len(data))
        out[::2], out[1::2] = data[1::2], data[::2]
        return bytes(out)
    if signature == b"\x40\x12\x37\x80":  # .n64 (32-bit swapped)
        out = bytearray(len(data))
        for offset in range(4):
            out[offset::4] = data[3 - offset::4]
        return bytes(out)
    raise ValueError(f"Unrecognised N64 ROM byte order ({signature.hex()})")


def identify_rom(data: bytes) -> tuple[str, bytes]:
    """Require the exact verified retail ROM; no broad header-only acceptance."""
    rom = normalize_byte_order(data)
    if len(rom) != ROM_SIZE:
        raise ValueError(f"Unsupported ROM size: {len(rom)} bytes")
    digest = hashlib.sha1(rom).hexdigest()
    for region, expected in ROM_SHA1.items():
        if digest == expected:
            if rom[0x3B:0x3F] != ROM_GAME_CODES[region] or rom[0x3F] != 0:
                raise ValueError("ROM hash matched but header was unexpected")
            return region, rom
    raise ValueError(f"Unsupported ROM SHA-1: {digest}")


def _distinct_anchor(chunk: bytes) -> bool:
    return chunk.count(0) <= len(chunk) // 2 and chunk.count(255) <= len(chunk) // 2 and len(set(chunk)) >= 12


def matching_rom_spans(usa: bytes, japan: bytes, *, anchor_size: int = 128,
                       stride: int = 16, min_span: int = 128) -> list[dict[str, int]]:
    """Find unambiguously anchored, exactly equal ROM intervals (not approximate code)."""
    if not (anchor_size >= 16 and stride > 0 and min_span >= anchor_size):
        raise ValueError("Invalid anchor size, stride, or minimum span")
    # Only uniquely occurring anchors can establish an unambiguous mapping.
    candidates: dict[bytes, list[int]] = defaultdict(list)
    for pos in range(0, len(japan) - anchor_size + 1, stride):
        piece = japan[pos:pos + anchor_size]
        if _distinct_anchor(piece):
            candidates[hashlib.blake2b(piece, digest_size=12).digest()].append(pos)
    by_delta: dict[int, list[int]] = defaultdict(list)
    for usa_pos in range(0, len(usa) - anchor_size + 1, stride):
        piece = usa[usa_pos:usa_pos + anchor_size]
        if not _distinct_anchor(piece):
            continue
        positions = candidates.get(hashlib.blake2b(piece, digest_size=12).digest(), ())
        if len(positions) == 1 and japan[positions[0]:positions[0] + anchor_size] == piece:
            jp_pos = positions[0]
            by_delta[jp_pos - usa_pos].append(jp_pos)

    spans = []
    for delta, positions in by_delta.items():
        positions.sort()
        start = end = None
        for jp_pos in positions:
            if end is not None and jp_pos <= end and japan[end:jp_pos + anchor_size] == usa[end - delta:jp_pos + anchor_size - delta]:
                end = max(end, jp_pos + anchor_size)
            else:
                if start is not None and end - start >= min_span:
                    spans.append((start - delta, start, end - start))
                start, end = jp_pos, jp_pos + anchor_size
        if start is not None and end - start >= min_span:
            spans.append((start - delta, start, end - start))

    # Overlapping candidate mappings may come from repeated content. Prefer
    # longer disjoint spans, never claim two mappings for the same source range.
    selected: list[tuple[int, int, int]] = []
    for us, jp, size in sorted(spans, key=lambda x: (-x[2], x[0], x[1])):
        if any(us < a + n and a < us + size or jp < b + n and b < jp + size
               for a, b, n in selected):
            continue
        if usa[us:us + size] != japan[jp:jp + size]:
            raise AssertionError("Inexact match escaped verification")
        selected.append((us, jp, size))
    selected.sort()
    return [{"usa_offset": us, "japan_offset": jp, "length": size}
            for us, jp, size in selected]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("usa_rom", type=Path)
    parser.add_argument("japan_rom", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON report, no game data")
    args = parser.parse_args(argv)
    us_region, usa = identify_rom(args.usa_rom.read_bytes())
    jp_region, japan = identify_rom(args.japan_rom.read_bytes())
    if (us_region, jp_region) != ("USA", "Japan"):
        parser.error("Expected the USA ROM first and Japanese ROM second")
    spans = matching_rom_spans(usa, japan)
    count = sum(x["length"] for x in spans)
    report = {
        "format": "goemon-regional-exact-spans-v1",
        "roms": {"usa": {"sha1": ROM_SHA1["USA"], "game_code": "NG5E"},
                 "japan": {"sha1": ROM_SHA1["Japan"], "game_code": "NG5J"}},
        "proven_exact_bytes": count,
        "proven_exact_fraction": round(count / ROM_SIZE, 6),
        "spans": spans,
        "warning": "Exact ROM spans only. Does not map RAM or prove Japanese recomp compatibility.",
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Verified USA NG5E and Japan NG5J; {len(spans)} exact spans, "
          f"{count:,}/{ROM_SIZE:,} bytes ({count / ROM_SIZE:.1%})")
    if not args.output:
        print("Use --output to save the non-ROM JSON mapping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
