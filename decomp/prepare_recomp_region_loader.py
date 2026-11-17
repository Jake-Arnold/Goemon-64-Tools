"""Prepare an isolated Goemon64Recomp ROM decompressor for both retail regions.

This patches only the ROM expansion helper. The USA GameEntry and generated
USA code stay unchanged. It does NOT enable Japanese gameplay: a separate
Japanese GameEntry, symbols, overlays and recompiled functions are still needed.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

RELATIVE = Path("src/game/rom_decompression.cpp")
BEFORE_CONSTANTS = """constexpr size_t FILE_TABLE_OFFSET = 0x57FD8;
constexpr uint32_t DECOMPRESSED_ROM_CRC_1 = 0x9CC11F4B;
constexpr uint32_t DECOMPRESSED_ROM_CRC_2 = 0xABAA8538;"""
AFTER_CONSTANTS = """// Source retail images checked against exact USA/Japan revision-0 SHA-1s.
// Japanese gameplay still requires a Japanese recompiled executable target.
struct GoemonRomVariant {
    size_t file_table_offset;
    uint32_t decompressed_crc1;
    uint32_t decompressed_crc2;
    uint32_t retail_crc1;
    uint32_t retail_crc2;
};
constexpr GoemonRomVariant GOEMON_USA{0x57FD8, 0x9CC11F4B, 0xABAA8538,
                                     0xFCBCCB21, 0x72903C6B};
constexpr GoemonRomVariant GOEMON_JAPAN_0{0x58258, 0x673A3EDC, 0x2491ADFC,
                                         0x832C168B, 0x56A2CDAE};"""
BEFORE_HEADER = """    if (compressed_rom[0x3B] != 'N' || compressed_rom[0x3C] != 'G' || compressed_rom[0x3D] != '5' || compressed_rom[0x3E] != 'E') {
        assert(false);
        return {};
    }"""
AFTER_HEADER = """    // Retail game ID, revision and original header CRCs select decompression.
    // These header checks are not a substitute for GameEntry's ROM hash check.
    if (compressed_rom[0x3B] != 'N' || compressed_rom[0x3C] != 'G' ||
        compressed_rom[0x3D] != '5' || compressed_rom[0x3F] != 0) {
        assert(false);
        return {};
    }
    const GoemonRomVariant* variant = nullptr;
    const uint8_t region = compressed_rom[0x3E];
    const uint32_t retail_crc1 = byteswap(*reinterpret_cast<const uint32_t*>(compressed_rom.data() + 0x10));
    const uint32_t retail_crc2 = byteswap(*reinterpret_cast<const uint32_t*>(compressed_rom.data() + 0x14));
    if (region == 'E' && retail_crc1 == GOEMON_USA.retail_crc1 && retail_crc2 == GOEMON_USA.retail_crc2) {
        variant = &GOEMON_USA;
    } else if (region == 'J' && retail_crc1 == GOEMON_JAPAN_0.retail_crc1 && retail_crc2 == GOEMON_JAPAN_0.retail_crc2) {
        variant = &GOEMON_JAPAN_0;
    }
    if (!variant || std::memcmp(compressed_rom.data() + variant->file_table_offset - 16,
                                "Nisitenma-Ichigo", 16) != 0) {
        assert(false);
        return {};
    }"""
BEFORE_EXPAND = "size_t final_size = lzkn64_decompress_rom(compressed_rom, ret, FILE_TABLE_OFFSET);"
AFTER_EXPAND = "size_t final_size = lzkn64_decompress_rom(compressed_rom, ret, variant->file_table_offset);"
BEFORE_CRC = """    *reinterpret_cast<uint32_t*>(ret.data() + 0x10) = byteswap(DECOMPRESSED_ROM_CRC_1);
    *reinterpret_cast<uint32_t*>(ret.data() + 0x14) = byteswap(DECOMPRESSED_ROM_CRC_2);"""
AFTER_CRC = """    *reinterpret_cast<uint32_t*>(ret.data() + 0x10) = byteswap(variant->decompressed_crc1);
    *reinterpret_cast<uint32_t*>(ret.data() + 0x14) = byteswap(variant->decompressed_crc2);"""


def render(source: str) -> str:
    if "GOEMON_JAPAN_0" in source:
        raise ValueError("Region ROM loader is already patched")
    for label, old, new in (
        ("constants", BEFORE_CONSTANTS, AFTER_CONSTANTS),
        ("USA-only header", BEFORE_HEADER, AFTER_HEADER),
        ("file table offset", BEFORE_EXPAND, AFTER_EXPAND),
        ("output header CRCs", BEFORE_CRC, AFTER_CRC),
    ):
        found = source.count(old)
        if found != 1:
            raise ValueError(f"Expected exactly one original {label} anchor, found {found}")
        source = source.replace(old, new, 1)
    return source


def prepare(repo: Path, dry_run: bool = False) -> Path:
    repo = repo.resolve(strict=True)
    path = repo / RELATIVE
    if not path.is_file():
        raise FileNotFoundError(f"Goemon64Recomp source missing at {path}")
    if (repo / ".git").exists():
        status = subprocess.check_output(
            ["git", "-C", str(repo), "status", "--porcelain", "--", str(RELATIVE)],
            text=True)
        if status.strip():
            raise ValueError("Refusing to patch an already-modified ROM loader")
    original = path.read_text(encoding="utf-8")
    updated = render(original)
    if dry_run:
        return path
    temp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=".goemon-region-", suffix=".tmp", delete=False
        ) as dest:
            dest.write(updated)
            temp = Path(dest.name)
        os.chmod(temp, path.stat().st_mode)
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recomp_checkout", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    result = prepare(args.recomp_checkout, dry_run=args.dry_run)
    print(f"{'Validated' if args.dry_run else 'Patched'} {result}")
    print("Japanese GameEntry and recompiled code are still missing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
