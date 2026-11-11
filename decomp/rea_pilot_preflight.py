"""Read-only Goemon/REA MIPS ELF admission preflight.

This deliberately does NOT assert REA provider support. Only REA itself can
admit an ELF after checking ABI records and provider/toolchain availability.
No contents are written or uploaded; stdout contains metadata only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

ARCH_NAMES = {
    0x00000000: "MIPS-I",
    0x10000000: "MIPS-II",
    0x20000000: "MIPS-III",
    0x30000000: "MIPS-IV",
    0x40000000: "MIPS-V",
    0x50000000: "MIPS32",
    0x60000000: "MIPS64",
    0x70000000: "MIPS32r2",
    0x80000000: "MIPS64r2",
}
POSSIBLE_REA_ARCHES = {0x00000000, 0x50000000, 0x70000000}


def classify_header(header: bytes, length: int) -> dict:
    """Classify only the conservative MIPS-ELF prerequisites, not full admission."""
    if header[:4] != b"\x7fELF":
        return {"format": "non-ELF", "rea_mips_lane": "NOT_APPLICABLE",
                "reason": "REA raw-binary Ghidra mode does not list MIPS; a Z64 ROM is not a MIPS ELF"}
    if len(header) < 52:
        return {"format": "ELF", "rea_mips_lane": "MALFORMED",
                "reason": "ELF header shorter than ELF32 header"}
    elf_class, elf_data = header[4], header[5]
    if elf_class != 1:
        return {"format": "ELF", "elf_class": elf_class,
                "rea_mips_lane": "UNSUPPORTED_ELF_CLASS",
                "reason": "REA MIPS lane requires ELF32"}
    if elf_data not in (1, 2):
        return {"format": "ELF32", "rea_mips_lane": "MALFORMED",
                "reason": "unrecognized ELF data encoding"}
    endian = "little" if elf_data == 1 else "big"
    prefix = "<" if elf_data == 1 else ">"
    e_type, e_machine = struct.unpack_from(prefix + "HH", header, 16)
    e_flags = struct.unpack_from(prefix + "I", header, 36)[0]
    e_ehsize = struct.unpack_from(prefix + "H", header, 40)[0]
    e_phoff, e_shoff = struct.unpack_from(prefix + "II", header, 28)
    e_phentsize, e_phnum, e_shentsize, e_shnum = struct.unpack_from(prefix + "HHHH", header, 42)
    arch_flag = e_flags & 0xF0000000
    facts = {"format": "ELF32", "byte_order": endian, "e_type": e_type,
             "e_machine": e_machine, "e_flags": f"0x{e_flags:08x}",
             "mips_arch_flag": f"0x{arch_flag:08x}",
             "mips_arch_name": ARCH_NAMES.get(arch_flag, "unknown")}
    if e_ehsize < 52 or any(off and (off > length or off + count * entsize > length)
                               for off, count, entsize in (
                                   (e_phoff, e_phnum, e_phentsize),
                                   (e_shoff, e_shnum, e_shentsize))):
        return {**facts, "rea_mips_lane": "MALFORMED",
                "reason": "ELF header size or declared table extent invalid"}
    if e_machine != 8:
        return {**facts, "rea_mips_lane": "NOT_MIPS",
                "reason": "ELF e_machine is not EM_MIPS"}
    if e_type not in (1, 2):
        return {**facts, "rea_mips_lane": "UNSUPPORTED_ELF_TYPE",
                "reason": "REA standard MIPS lane documents ET_REL or ET_EXEC"}
    if arch_flag not in POSSIBLE_REA_ARCHES:
        return {**facts, "rea_mips_lane": "UNSUPPORTED_DECLARED_ISA",
                "reason": "REA standard MIPS ELF admission does not document this declared ISA"}
    return {**facts, "rea_mips_lane": "POSSIBLE_REQUIRES_OFFICIAL_REA_ADMISSION",
            "reason": "e_flags ISA is potentially eligible; ABI/FP flags and records, loader, provider and language must still be verified by REA"}


def inspect(path: Path) -> dict:
    if not path.is_file():
        raise ValueError("target must be a readable regular file")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        header = stream.read(64)
        digest.update(header)
        size += len(header)
        while data := stream.read(1024 * 1024):
            digest.update(data)
            size += len(data)
    return {"schema": "goemon-rea-preflight-v1", "target_basename": path.name,
            "size_bytes": size, "sha256": digest.hexdigest(),
            **classify_header(header, size),
            "provider_executed": False, "full_rom_verification": False,
            "private_data_exported": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path, help="local, privately built candidate ELF; never a ROM upload")
    parser.add_argument("--strict", action="store_true",
                        help="return nonzero unless header is potentially eligible")
    args = parser.parse_args(argv)
    try:
        result = inspect(args.elf)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return int(args.strict and result["rea_mips_lane"] != "POSSIBLE_REQUIRES_OFFICIAL_REA_ADMISSION") * 2


if __name__ == "__main__":
    raise SystemExit(main())
