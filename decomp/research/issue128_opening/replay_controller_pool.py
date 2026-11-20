"""Rebuild the checkpoint 6 controller and its original-layout constant pool probe."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
from zipfile import ZipFile

from compare_controller import (
    NAME, ORIGINAL_TABLE, POOL_END, ROM_OFFSET, SIZE, VMA, compare, words,
)
from verify_wrappers import (
    FLAGS, IDO_SHA256, PIN, ROM_SHA1, read_section, relocations, run, symbols,
)

CHECKPOINT = "goemon_opening_controller_checkpoint6_2026-11-20"
SOURCE = f"{CHECKPOINT}/opening_controller_native_C_NONMATCHING.c"
SOURCE_SHA256 = "efce083eeefd65b25f729bc1195281172a64dc756a1203a669c31b94c5e17b56"
HEADER_SHA256 = "f84442c9b6d3ad647ba55db93a994d9c24f0a2500a82cccca99725d1e7b6221c"
POOL_VMA = 0x8022A6C8
DECLARATION = re.compile(r"^extern (f32|f64) (D_\w+_([0-9A-F]{6}));\n", re.M)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def restore_literals(source, rom):
    restored = 0
    for declaration in list(DECLARATION.finditer(source)):
        kind, name, offset = declaration.groups()
        offset = int(offset, 16)
        if not (0x694148 <= offset < 0x69417C or 0x6941A0 <= offset < POOL_END):
            continue
        if kind == "f32":
            (value,) = struct.unpack_from(">f", rom, offset)
            literal = f"{value:.16e}f"
        else:
            (value,) = struct.unpack_from(">d", rom, offset)
            literal = f"{value:.17e}"
        source = source.replace(declaration[0], "")
        source = re.sub(rf"\b{re.escape(name)}\b", literal, source)
        restored += 1
    if restored != 22:
        raise ValueError(f"Unexpected controller literal count: {restored}")
    return source


def linked_comparison(obj, original_elf, original_symbols, rom, output):
    script = output / "link.ld"
    script.write_text(
        f"SECTIONS {{ .text 0x{VMA:x} : SUBALIGN(4) {{ *(.text) }} "
        f".rodata 0x{POOL_VMA:x} : SUBALIGN(8) {{ *(.rodata) }} }}\n"
    )
    definitions = []
    for symbol in sorted({name for _, _, name in relocations(obj)} - {".rodata"}):
        (address,) = {value for value, _, _ in original_symbols[symbol]}
        definitions.append(f"--defsym={symbol}=0x{address:x}")

    linked = output / "candidate.elf"
    run("mips-linux-gnu-ld", "-EB", "-e", NAME, "-T", script, *definitions, "-o", linked, obj)
    if (VMA, SIZE, "FUNC") not in symbols(linked)[NAME]:
        raise ValueError("Linked candidate controller address or extent changed")
    original_pool = rom[ORIGINAL_TABLE:POOL_END]
    original_text = rom[ROM_OFFSET:ROM_OFFSET + SIZE]
    pool = read_section(linked, ".rodata", output / "linked.pool")[:len(original_pool)]
    text = read_section(linked, ".text", output / "linked.text")[:SIZE]
    return {
        "original_elf_sha256": sha256(original_elf.read_bytes()),
        "linked_pool_exact": original_pool == pool,
        "linked_pool_equal_bytes": sum(a == b for a, b in zip(original_pool, pool)),
        "linked_text_exact": original_text == text,
        "linked_text_equal_bytes": sum(a == b for a, b in zip(original_text, text)),
        "linked_text_equal_words": sum(a == b for a, b in zip(words(original_text), words(text))),
        "linked_text_first_mismatch": next(
            (i for i, (a, b) in enumerate(zip(original_text, text)) if a != b), None
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path, help="Built pinned original USA checkout")
    parser.add_argument("checkpoint", type=Path, help="Checkpoint 6 source ZIP")
    parser.add_argument("output", type=Path, help="New, private output directory")
    args = parser.parse_args()
    upstream = args.upstream.resolve()
    output = args.output.resolve()
    rom = (upstream / "config/usa/baserom.decompressed.z64").read_bytes()
    ido = upstream / "tools/ido-5.3/cc"
    with ZipFile(args.checkpoint) as archive:
        source = archive.read(SOURCE)
    header = (Path(__file__).resolve().parent.parent / "pending_native51_20261120"
              / "sources/research_m2c_macros.h").read_bytes()
    if (run("git", "rev-parse", "HEAD", cwd=upstream).strip() != PIN
            or len(rom) != 33554432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1
            or sha256(ido.read_bytes()) != IDO_SHA256 or sha256(source) != SOURCE_SHA256
            or sha256(header) != HEADER_SHA256):
        raise ValueError("Unexpected upstream, expanded ROM, compiler, checkpoint source or macro header")

    output.mkdir()
    (output / "m2c_macros.h").write_bytes(header)
    original_elf = upstream / "build/usa/mnsg.elf"
    original_symbols = symbols(original_elf)
    for name, code in (("checkpoint6", source.decode()),
                       ("full-pool", restore_literals(source.decode(), rom))):
        work = output / name
        work.mkdir()
        c_file = work / "controller.c"
        c_file.write_text(code)
        obj = work / "controller.o"
        run(ido, *FLAGS, f"-I{output}", "-o", obj, c_file, cwd=upstream)
        report = compare(upstream, obj, work)
        report.update(linked_comparison(obj, original_elf, original_symbols, rom, work))
        report["candidate_source_sha256"] = sha256(c_file.read_bytes())
        report["status"] = "RESEARCH_ONLY"
        (work / "report.json").write_text(json.dumps(report, indent=2) + "\n")
        print(f"{name}: {report['linked_pool_equal_bytes']}/336 pool bytes, "
              f"{report['linked_text_equal_words']}/4337 text words")


if __name__ == "__main__":
    main()
