"""Scratch-only stage and proof of three USA character-switch C functions.

This is a bounded reproduction of a complete 32 MiB USA ROM comparison, not
an automatic edit to the production Goemon decomp manifest. It requires a
scratch checkout of the exact pinned upstream mnsg source and the verified
USA decompressed ROM. Only writes under the explicitly passed checkout.

Run --phase prepare; regenerate Splat, build, run --phase trim, rebuild, then
--phase verify. See the accompanying research report for exact commands.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess

from decomp.research.trim_elf32_mips_text import trim_text_section

UPSTREAM_COMMIT = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
USA_ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
SPLAT_OLD = "    - [0x587370, asm]\n    - [0x5B8500, data]"
SPLAT_NEW = "    - [0x587370, asm]\n    - [0x5993E8, c, character_switch_entry]\n    - [0x59941C, asm]\n    - [0x5994D0, c, character_switch_sync]\n    - [0x599564, asm]\n    - [0x5B8500, data]"
CHUNKS = {
    "build/usa/asm/usa/587370.s.o": 0x12078,
    "build/usa/src/character_switch_entry.c.o": 0x34,
    "build/usa/asm/usa/59941C.s.o": 0xB4,
    "build/usa/src/character_switch_sync.c.o": 0x94,
    "build/usa/asm/usa/599564.s.o": 0x1EF9C,
}


def verify_source(checkout: Path):
    if not (checkout / "Makefile").is_file():
        raise ValueError("Not an upstream mnsg checkout")
    result = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                            check=True, capture_output=True, text=True)
    if result.stdout.strip() != UPSTREAM_COMMIT:
        raise ValueError("Upstream checkout is not the pinned commit")
    rom = checkout / "config/usa/baserom.decompressed.z64"
    if not rom.is_file() or rom.stat().st_size != 0x2000000 or hashlib.sha1(rom.read_bytes()).hexdigest() != USA_ROM_SHA1:
        raise ValueError("USA decompressed ROM identity failed")
    return rom


def prepare(checkout: Path):
    config = checkout / "config/usa/splat.yaml"
    data = config.read_text(encoding="utf-8")
    if data.count(SPLAT_OLD) != 1:
        raise ValueError("Expected pristine file_11 Splat layout (do not patch twice)")
    for name in ("character_switch_entry", "character_switch_sync"):
        destination = checkout / "src" / (name + ".c")
        if destination.exists():
            raise ValueError(f"Refusing to overwrite existing {destination}")
    candidates = Path(__file__).resolve().parent
    for name in ("character_switch_entry", "character_switch_sync"):
        shutil.copyfile(candidates / ("usa_" + name + ".c"), checkout / "src" / (name + ".c"))
    config.write_text(data.replace(SPLAT_OLD, SPLAT_NEW), encoding="utf-8")
    print("Prepared original file_11 island; now run pinned Splat and the first USA build")


def trim(checkout: Path):
    script = checkout / ".splat/usa/mnsg.ld"
    s = script.read_text()
    old = ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)"
    if s.count(old) != 1:
        raise ValueError("Expected staged file_11 linker script")
    revisions = []
    for object_path, length in CHUNKS.items():
        path = checkout / object_path
        revisions.append((path, trim_text_section(path.read_bytes(), length)))
    # Everything validated before any file changes.
    for path, data in revisions:
        path.write_bytes(data)
    script.write_text(s.replace(old, ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)"))
    print("Adjusted five original-code/IDO chunks with .rel.text preserved")


def verify(checkout: Path, reference: Path):
    original = reference.read_bytes()
    actual = (checkout / "build/usa/mnsg.z64").read_bytes()
    if actual != original or hashlib.sha1(actual).hexdigest() != USA_ROM_SHA1:
        raise ValueError("Full USA 32 MiB exact-ROM proof failed")
    print(f"FULL USA ROM MATCH: 33,554,432 bytes SHA-1 {USA_ROM_SHA1}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--phase", choices=["prepare", "trim", "verify"], required=True)
    args = parser.parse_args(argv)
    checkout = args.checkout.resolve()
    reference = verify_source(checkout)
    {"prepare": prepare, "trim": trim, "verify": lambda c: verify(c, reference)}[args.phase](checkout)


if __name__ == "__main__":
    main()