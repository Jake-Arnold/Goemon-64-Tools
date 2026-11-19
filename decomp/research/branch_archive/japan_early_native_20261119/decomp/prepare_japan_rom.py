"""Prepare a verified Japanese Goemon revision-0 ROM for the pinned mnsg build.

Input may be .z64, 16-bit-swapped (.v64 / many .n64), or 32-bit-swapped.
The original file is never edited; output must be a new .z64 file.
Neither ROM contents nor extracted game assets belong in Git.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import struct
import tempfile

ROM_SIZE = 16 * 1024 * 1024
JAPAN_SHA1 = "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b"
JAPAN_GAME_CODE = b"NG5J"
JAPAN_CRC = (0x832C168B, 0x56A2CDAE)
MAGIC_Z64 = b"\x80\x37\x12\x40"
MAGIC_V64 = b"\x37\x80\x40\x12"
MAGIC_N64 = b"\x40\x12\x37\x80"


def normalize_rom(data: bytes) -> tuple[bytes, str]:
    """Return canonical big-endian bytes and original ROM byte order."""
    if len(data) != ROM_SIZE:
        raise ValueError(f"Expected {ROM_SIZE} bytes; got {len(data)}")
    signature = data[:4]
    if signature == MAGIC_Z64:
        return data, "z64"
    if signature == MAGIC_V64:
        out = bytearray(len(data))
        out[::2] = data[1::2]
        out[1::2] = data[::2]
        return bytes(out), "v64-16bit-swapped"
    if signature == MAGIC_N64:
        out = bytearray(len(data))
        for i in range(4):
            out[i::4] = data[3 - i::4]
        return bytes(out), "n64-32bit-swapped"
    raise ValueError(f"Unrecognized Nintendo 64 ROM header {signature.hex()}")


def verify_japan_rom(data: bytes) -> tuple[bytes, dict[str, object]]:
    """Accept only the exact Japanese revision-0 retail cartridge."""
    canonical, original_order = normalize_rom(data)
    if canonical[0x3B:0x3F] != JAPAN_GAME_CODE or canonical[0x3F] != 0:
        raise ValueError("Not Japanese Goemon revision 0 (NG5J, revision 0)")
    if struct.unpack_from(">II", canonical, 0x10) != JAPAN_CRC:
        raise ValueError("Unexpected Japanese Goemon cartridge CRCs")
    actual_sha1 = hashlib.sha1(canonical).hexdigest()
    if actual_sha1 != JAPAN_SHA1:
        raise ValueError(f"Wrong or modified Japanese ROM (SHA-1 {actual_sha1})")
    return canonical, {
        "region": "japan_0",
        "input_byte_order": original_order,
        "size": len(canonical),
        "sha1": actual_sha1,
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }


def prepare(source: Path, destination: Path) -> dict[str, object]:
    """Write a new canonical .z64 atomically; refuse to replace existing files."""
    source, destination = Path(source), Path(destination)
    if destination.suffix.lower() != ".z64":
        raise ValueError("Output must end in .z64")
    if source.resolve() == destination.resolve():
        raise ValueError("Refusing to overwrite the original ROM")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Output already exists: {destination}")
    canonical, report = verify_japan_rom(source.read_bytes())
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=destination.parent, prefix=".japan-rom-",
            suffix=".tmp", delete=False,
        ) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(canonical)
            tmp.flush()
            os.fsync(tmp.fileno())
        # Hard-link creation is atomic and fails if the output already exists.
        os.link(tmp_path, destination, follow_symlinks=False)
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original Japanese Goemon ROM")
    parser.add_argument("destination", type=Path, help="New config/japan_0/baserom.z64")
    args = parser.parse_args(argv)
    report = prepare(args.source, args.destination)
    print("Verified Japanese Goemon revision 0; "
          f"input={report['input_byte_order']}, canonical SHA-1={report['sha1']}")
    print(f"Wrote new canonical file: {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
