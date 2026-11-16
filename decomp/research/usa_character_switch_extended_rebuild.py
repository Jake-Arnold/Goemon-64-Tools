"""Extend the verified four-function USA file_11 scratch build with nine wrappers.

Run only on a separately staged four-function checkout from
usa_character_switch_rebuild.py. The source checkout must have the pinned
upstream HEAD and the verified original decompressed USA ROM.

Phases: prepare; regenerate pinned Splat + make; trim; make again; verify.
Original source/ROM are never modified. The only edits are to a scratch
checkout and its generated objects. Do not claim central decomp.verify proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import shutil
import subprocess

from decomp.research.trim_elf32_mips_text import trim_text_section

PIN = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
REFERENCE_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
SPLAT_PREVIOUS = "    - [0x5995E8, asm]\n    - [0x5B8500, data]"
SPLAT_EXTENDED = ("    - [0x5995E8, asm]\n"
                  "    - [0x599918, c, character_switch_wrappers]\n"
                  "    - [0x599A38, asm]\n"
                  "    - [0x5B8500, data]")
OLD_LINKER = ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)"
NEW_LINKER = ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)"
SIZES = {
    "build/usa/asm/usa/587370.s.o": 0x12078,
    "build/usa/src/character_switch_entry.c.o": 0x34,
    "build/usa/asm/usa/59941C.s.o": 0xB4,
    "build/usa/src/character_switch_sync.c.o": 0x94,
    "build/usa/src/character_switch_alt.c.o": 0x84,
    "build/usa/asm/usa/5995E8.s.o": 0x330,
    "build/usa/src/character_switch_wrappers.c.o": 0x120,
    "build/usa/asm/usa/599A38.s.o": 0x1EAC8,
}


def pinned_checkout(checkout: Path) -> bytes:
    if not (checkout / "Makefile").is_file():
        raise ValueError("Expected pinned upstream mnsg checkout")
    rev = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if rev != PIN:
        raise ValueError("Incorrect upstream commit")
    rom = (checkout / "config/usa/baserom.decompressed.z64").read_bytes()
    if len(rom) != 0x2000000 or hashlib.sha1(rom).hexdigest() != REFERENCE_SHA1:
        raise ValueError("Original USA decompressed ROM identity mismatch")
    return rom


def prepare(checkout: Path) -> None:
    path = checkout / "config/usa/splat.yaml"
    contents = path.read_text()
    if contents.count(SPLAT_PREVIOUS) != 1 or "character_switch_alt" not in contents:
        raise ValueError("Four-function Splat stage is missing or already extended")
    source = checkout / "src/character_switch_wrappers.c"
    if source.exists():
        raise ValueError("Refusing to overwrite an existing source")
    implementation = Path(__file__).with_name("usa_character_switch_actor_wrappers.c")
    if not implementation.is_file():
        raise ValueError("Missing candidate source")
    shutil.copyfile(implementation, source)
    path.write_text(contents.replace(SPLAT_PREVIOUS, SPLAT_EXTENDED))
    print("Extended staged file_11 layout; regenerate Splat, then run first USA make")


def trim(checkout: Path) -> None:
    script = checkout / ".splat/usa/mnsg.ld"
    layout = script.read_text()
    if layout.count(OLD_LINKER) != 1:
        raise ValueError("Expected generated SUBALIGN(16) file_11 linker layout")
    staged = []
    for name, size in SIZES.items():
        path = checkout / name
        staged.append((path, trim_text_section(path.read_bytes(), size)))
    # Validate all new objects before modifying the scratch build.
    for path, data in staged:
        path.write_bytes(data)
    script.write_text(layout.replace(OLD_LINKER, NEW_LINKER))
    print("Trimmed eight chunks while retaining their original MIPS ELF relocs")


def verify(checkout: Path, reference: bytes) -> None:
    candidate = (checkout / "build/usa/mnsg.z64").read_bytes()
    if candidate != reference or hashlib.sha1(candidate).hexdigest() != REFERENCE_SHA1:
        raise ValueError("Extended build failed exact 32 MiB ROM check")
    print(f"FULL USA ROM MATCH: 33,554,432 bytes SHA-1 {REFERENCE_SHA1}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checkout", type=Path, required=True)
    ap.add_argument("--phase", choices=("prepare", "trim", "verify"), required=True)
    ns = ap.parse_args(argv)
    checkout = ns.checkout.resolve()
    reference = pinned_checkout(checkout)
    {"prepare": prepare, "trim": trim, "verify": lambda c: verify(c, reference)}[ns.phase](checkout)


if __name__ == "__main__":
    main()