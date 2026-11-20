"""Verify issue #128 wrappers against local original file_18 build inputs."""

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory

PIN = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
RETAIL_SHA1 = "df8083a54296b8c151917c5333e1c85f014a2a66"
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
IDO_SHA256 = "76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0"
OWNER_ROM = 0x676C80
CANDIDATES = {
    "func_8020D818_6771F8": (0x8020D818, 0x6771F8, 52),
    "func_8020D870_677250": (0x8020D870, 0x677250, 32),
    "func_8020D890_677270": (0x8020D890, 0x677270, 52),
    "func_8020D8C4_6772A4": (0x8020D8C4, 0x6772A4, 32),
    "func_8020D92C_67730C": (0x8020D92C, 0x67730C, 32),
    "func_8020D978_677358": (0x8020D978, 0x677358, 32),
}
FLAGS = (
    "-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include "
    "-Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 "
    "-D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2"
).split()


def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True)


def symbols(path):
    result = {}
    for line in run("mips-linux-gnu-readelf", "-Ws", path).splitlines():
        fields = line.split()
        if len(fields) == 8 and fields[0][:-1].isdigit() and fields[6] != "UND":
            result.setdefault(fields[7], set()).add(
                (int(fields[1], 16), int(fields[2], 0), fields[3])
            )
    return result


def relocations(path, section=".rel.text"):
    text = False
    result = []
    expected_count = 0
    for line in run("mips-linux-gnu-readelf", "-Wr", path).splitlines():
        if line.startswith("Relocation section "):
            text = line.startswith(f"Relocation section '{section}' ")
            if text:
                expected_count = int(line.split()[-2])
        if text:
            row = re.fullmatch(r"\s*([\da-f]+)\s+[\da-f]+\s+(R_MIPS_\w+)\s+[\da-f]+\s+(\S+)\s*", line)
            if row:
                offset, kind, symbol = row.groups()
                result.append((int(offset, 16), kind, symbol))
    if len(result) != expected_count:
        raise ValueError(f"{path}: could not read every {section} relocation")
    return result


def region_relocations(rows, start, size):
    return Counter((offset - start, kind, sym) for offset, kind, sym in rows
                   if start <= offset < start + size)


def read_section(obj, section, dest):
    run("mips-linux-gnu-objcopy", "--dump-section", f"{section}={dest}", obj,
        dest.with_name(dest.name + ".copy.o"))
    return dest.read_bytes()


def extract_text(obj, dest):
    return read_section(obj, ".text", dest)


def verify(upstream, scratch):
    config = upstream / "config/usa"
    retail = (config / "baserom.z64").read_bytes()
    rom = (config / "baserom.decompressed.z64").read_bytes()
    ido = upstream / "tools/ido-5.3/cc"
    if (run("git", "rev-parse", "HEAD", cwd=upstream).strip() != PIN
            or len(retail) != 16777216 or hashlib.sha1(retail).hexdigest() != RETAIL_SHA1
            or len(rom) != 33554432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1
            or hashlib.sha256(ido.read_bytes()).hexdigest() != IDO_SHA256):
        raise ValueError("Pinned source, USA ROM or IDO digest does not match")

    source = Path(__file__).with_name("opening_setups.c").resolve()
    baseline = upstream / "build/usa"
    old_obj = baseline / "asm/usa/676C80.s.o"
    new_obj = scratch / "wrappers.o"
    run(ido, *FLAGS, "-o", new_obj, source, cwd=upstream)

    old_symbols = symbols(old_obj)
    new_symbols = symbols(new_obj)
    linked_symbols = symbols(baseline / "mnsg.elf")
    old_relocs, new_relocs = relocations(old_obj), relocations(new_obj)
    old_code = extract_text(old_obj, scratch / "original.text")
    new_code = extract_text(new_obj, scratch / "candidate.text")
    externs = sorted({sym for _, _, sym in new_relocs})
    definitions = []
    for sym in externs:
        (address,) = {value for value, _, _ in linked_symbols[sym]}
        definitions.append(f"--defsym={sym}=0x{address:x}")

    for name, (vma, offset, size) in CANDIDATES.items():
        start = offset - OWNER_ROM
        (candidate,) = new_symbols[name]
        pos, actual_size, kind = candidate
        if ((start, size, "FUNC") not in old_symbols[name]
                or (vma, size, "FUNC") not in linked_symbols[name]
                or (actual_size, kind) != (size, "FUNC")):
            raise ValueError(f"{name}: function address or size mismatch")
        if old_code[start:start + size] != new_code[pos:pos + size]:
            raise ValueError(f"{name}: relocatable text differs")
        expected = region_relocations(old_relocs, start, size)
        if expected != region_relocations(new_relocs, pos, size):
            raise ValueError(f"{name}: relocation tuples differ")
        linked = scratch / "wrappers.elf"
        script = scratch / "wrapper.ld"
        script.write_text(
            f"SECTIONS {{ .text 0x{vma - pos:x} : SUBALIGN(4) {{ *(.text) }} }}\n"
        )
        run("mips-linux-gnu-ld", "-EB", "-e", name, "-T", script,
            *definitions, "-o", linked, new_obj)
        if (vma, size, "FUNC") not in symbols(linked)[name]:
            raise ValueError(f"{name}: linked address or size mismatch")
        actual = extract_text(linked, scratch / "linked.text")[pos:pos + size]
        if actual != rom[offset:offset + size]:
            raise ValueError(f"{name}: original ROM bytes differ")
        print(f"{name} {size} bytes {sum(expected.values())} relocations "
              f"sha256={hashlib.sha256(actual).hexdigest()} PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path, help="Built pinned original USA checkout")
    args = parser.parse_args()
    with TemporaryDirectory(prefix="goemon-opening-wrappers-") as tmp:
        verify(args.upstream.resolve(), Path(tmp))


if __name__ == "__main__":
    main()
