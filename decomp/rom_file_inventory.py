"""Reproduce non-copyrighted file boundaries/sizes from the original Goemon ROMs.

No ROM bytes, decoded assets, or extracted code are included in the output.
Based on the Nisitenma-Ichigo table format parsed by pinned upstream rommy.py.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha1
from io import StringIO
from pathlib import Path
import struct
from typing import Callable

SIGNATURE = b"Nisitenma-Ichigo"
COUNT = 1311
ROM_SIZE = 16 * 1024 * 1024
SHA1 = {
    "USA": "df8083a54296b8c151917c5333e1c85f014a2a66",
    "Japan": "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b",  # normalized JP rev-0
}
COLUMNS = (
    "File", "Segment classification", "USA stored bytes", "USA expanded bytes",
    "USA compression", "USA ROM offset", "USA expanded ROM offset",
    "Japan stored bytes", "Japan expanded bytes", "Japan compression",
    "Japan ROM offset", "Japan expanded ROM offset", "JP minus USA stored bytes",
    "JP minus USA expanded bytes",
)


def normalize_rom(data: bytes) -> bytes:
    """Accept z64, v64, or n64 byte order, without guessing from extension."""
    if data[:4] == b"\x80\x37\x12\x40":
        return data
    if data[:4] == b"\x37\x80\x40\x12":
        converted = bytearray(len(data))
        converted[::2] = data[1::2]
        converted[1::2] = data[::2]
        return bytes(converted)
    if data[:4] == b"\x40\x12\x37\x80":
        return b"".join(data[i:i + 4][::-1] for i in range(0, len(data), 4))
    raise ValueError("unrecognized N64 ROM byte order")


def load_region(path: Path, region: str) -> bytes:
    data = normalize_rom(path.read_bytes())
    if len(data) != ROM_SIZE:
        raise ValueError(f"{region}: expected a 16 MiB retail ROM")
    actual = sha1(data).hexdigest()
    if actual != SHA1[region]:
        raise ValueError(f"{region}: incorrect normalized ROM SHA-1: {actual}")
    return data


def parse_file_table(data: bytes, count: int = COUNT) -> list[tuple[int, bool]]:
    """Return numbered file starts plus the non-file end boundary."""
    location = data.find(SIGNATURE)
    if location < 0 or data.find(SIGNATURE, location + 1) >= 0:
        raise ValueError("Nisitenma-Ichigo signature missing or ambiguous")
    base = location + len(SIGNATURE)
    if base + 4 * (count + 2) > len(data):
        raise ValueError("truncated file table")
    words = struct.unpack_from(f">{count + 2}I", data, base)
    if words[-1] != 0:
        raise ValueError("missing file-table terminator")
    entries = [(word & 0x7FFFFFFF, bool(word & 0x80000000)) for word in words[:-1]]
    if entries[0][0] < base + 4 * (count + 2):
        raise ValueError("file data overlaps its table")
    offsets = [offset for offset, _ in entries]
    if offsets != sorted(offsets) or offsets[-1] > len(data):
        raise ValueError("non-monotonic or out-of-bounds file offsets")
    return entries


def classification(file_id: int, stored_size: int) -> str:
    if not stored_size:
        return "Empty slot"
    if 11 <= file_id <= 23:
        return "Executable: static overlay"
    if 24 <= file_id <= 80:
        return "Executable: TLB overlay"
    return "Opaque binary/data"


def region_entries(
    data: bytes,
    decompress: Callable[[bytes], bytes],
    count: int = COUNT,
) -> list[dict[str, int | str]]:
    entries = parse_file_table(data, count)
    expanded_offset = entries[0][0]
    result = []
    for idx in range(count):
        start, compressed = entries[idx]
        end, _ = entries[idx + 1]
        stored = end - start
        if stored == 0:
            expanded = 0
            compression = "Empty"
        elif compressed:
            expanded = len(decompress(data[start:end]))
            compression = "LZKN64"
        else:
            expanded = stored
            compression = "Uncompressed"
        result.append({
            "stored": stored, "expanded": expanded, "compression": compression,
            "rom_offset": f"0x{start:08X}", "expanded_rom_offset": f"0x{expanded_offset:08X}",
        })
        expanded_offset += expanded
    return result


def build_csv(usa: list[dict[str, int | str]], japan: list[dict[str, int | str]]) -> str:
    if len(usa) != COUNT or len(japan) != COUNT:
        raise ValueError("expected exactly 1,311 file slots per region")
    buffer = StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(COLUMNS)
    for idx, (u, j) in enumerate(zip(usa, japan), start=1):
        writer.writerow((
            f"file_{idx}", classification(idx, int(u["stored"])),
            u["stored"], u["expanded"], u["compression"], u["rom_offset"],
            u["expanded_rom_offset"], j["stored"], j["expanded"],
            j["compression"], j["rom_offset"], j["expanded_rom_offset"],
            int(j["stored"]) - int(u["stored"]), int(j["expanded"]) - int(u["expanded"]),
        ))
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usa-rom", type=Path, required=True)
    parser.add_argument("--japan-rom", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("data") / "rom_file_inventory.csv")
    parser.add_argument("--check", action="store_true", help="fail if the checked-in CSV differs; do not write")
    args = parser.parse_args()
    import lzkn64  # provided by the pinned Goemon Linux decomp environment

    usa = region_entries(load_region(args.usa_rom, "USA"), lzkn64.decompress)
    jp = region_entries(load_region(args.japan_rom, "Japan"), lzkn64.decompress)
    rendered = build_csv(usa, jp)
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != rendered.encode("utf-8"):
            parser.error(f"inventory drift: {args.output}")
        print(f"PASS: {COUNT} USA/Japan entries exactly match {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered.encode("utf-8"))
        print(f"Wrote {COUNT} USA/Japan entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
