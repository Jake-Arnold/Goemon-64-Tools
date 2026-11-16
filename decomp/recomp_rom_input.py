"""Build hash-verified decompressed USA/Japan Goemon recompilation inputs.

Requires the user's original cartridge ROM locally; no game content is bundled.
The emitted 32 MiB image is input for N64Recomp, not a playable PC port.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import struct

from practice.entrances import canonical_rom, decompress_block

REGIONS = {
    "usa": (b"NG5E", "df8083a54296b8c151917c5333e1c85f014a2a66", "6ea0ed71032ce08fc2745f412d84936382197494"),
    "japan_0": (b"NG5J", "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b", "6f8745fecc3a5e7d4918c7a73353eb0726116ded"),
}
SIGNATURE = b"Nisitenma-Ichigo"
FILE_POINTERS = 1312
MAX_SIZE = 0x4000000


def checksum_6102(data: bytes | bytearray) -> tuple[int, int]:
    """CIC-6102 header checksum, used by both tested retail revisions."""
    t1 = t2 = t3 = t4 = t5 = t6 = 0xF8CA4DDC
    for p in range(0x1000, 0x101000, 4):
        word = struct.unpack_from(">I", data, p)[0]
        shift = word & 31
        rotated = ((word << shift) | (word >> (32 - shift))) & 0xFFFFFFFF if shift else word
        summed = (t6 + word) & 0xFFFFFFFF
        if summed < t6:
            t4 = (t4 + 1) & 0xFFFFFFFF
        t6 = summed
        t3 ^= word
        t5 = (t5 + rotated) & 0xFFFFFFFF
        t2 ^= rotated if t2 > word else (t6 ^ word)
        t1 = (t1 + (t5 ^ word)) & 0xFFFFFFFF
    return t6 ^ t4 ^ t3, t5 ^ t2 ^ t1


def expand(retail: bytes, region: str) -> tuple[bytes, dict]:
    try:
        header, retail_sha, expanded_sha = REGIONS[region]
    except KeyError as exc:
        raise ValueError("Unsupported region") from exc
    if len(retail) != 0x1000000:
        raise ValueError("Expected an exact 16 MiB cartridge image")
    data = canonical_rom(retail)
    if data[0x3B:0x3F] != header or data[0x3F] != 0 or hashlib.sha1(data).hexdigest() != retail_sha:
        raise ValueError("Wrong ROM region/revision, or modified retail ROM")
    signature = data.find(SIGNATURE)
    if signature < 0 or data.find(SIGNATURE, signature + 1) != -1:
        raise ValueError("Missing or ambiguous file table")
    table = signature + len(SIGNATURE)
    pointers = struct.unpack_from(f">{FILE_POINTERS}I", data, table)
    destination = pointers[0] & 0x7FFFFFFF
    if not table + 4 * FILE_POINTERS <= destination < len(data):
        raise ValueError("Invalid first file offset")
    output = bytearray(MAX_SIZE)
    output[:len(data)] = data
    populated = compressed_count = 0
    for i in range(FILE_POINTERS - 1):
        begin, end = pointers[i] & 0x7FFFFFFF, pointers[i + 1] & 0x7FFFFFFF
        if begin > end or end > len(data):
            raise ValueError(f"Bad file-table entry {i + 1}")
        if begin == end:
            unpacked = b""
        else:
            compressed = bool(pointers[i] & 0x80000000)
            unpacked = decompress_block(data[begin:end]) if compressed else data[begin:end]
            populated += 1
            compressed_count += compressed
        padded = (len(unpacked) + 15) & ~15
        if destination + padded > MAX_SIZE:
            raise ValueError("Expanded ROM exceeds 64 MiB")
        output[destination:destination + len(unpacked)] = unpacked
        struct.pack_into(">I", output, table + i * 4, destination)
        destination += padded
        struct.pack_into(">I", output, table + (i + 1) * 4, destination)
    size = 1 << (destination - 1).bit_length()
    if not 0x101000 <= size <= MAX_SIZE:
        raise ValueError("Invalid decompressed ROM size")
    output = output[:size]
    struct.pack_into(">II", output, 0x10, *checksum_6102(output))
    sha1 = hashlib.sha1(output).hexdigest()
    if sha1 != expanded_sha:
        raise ValueError(f"Decompressed SHA-1 mismatch: {sha1}; expected {expanded_sha}")
    return bytes(output), {"region": region, "sha1": sha1, "file_table": table,
                           "populated_files": populated, "compressed_files": compressed_count,
                           "size": size, "last_file_end": destination}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--region", choices=tuple(REGIONS), default="japan_0")
    args = parser.parse_args(argv)
    if args.rom.resolve() == args.output.resolve():
        parser.error("Never overwrite the original cartridge ROM")
    data, details = expand(args.rom.read_bytes(), args.region)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    from tempfile import NamedTemporaryFile
    import os
    path = None
    try:
        with NamedTemporaryFile(dir=args.output.parent, prefix=".expanded-", delete=False) as out:
            path = Path(out.name)
            out.write(data)
        os.replace(path, args.output)
    finally:
        if path is not None:
            path.unlink(missing_ok=True)
    print(f"{details['region']}: {details['size']} bytes, SHA-1 {details['sha1']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
