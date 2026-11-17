"""Fail-closed original-USA file_12 isolated-address native C verifier.

Compile with the pinned original IDO 5.3 and link each reconstructed C routine at
its original virtual address with GNU MIPS binutils. No original bytes are
embedded, emitted, changed or committed. No complete overlay/build claim.

Run:
python3 decomp/research/file12_spatial/verify_isolates.py \
  --rom /path/to/verified/usa/decompressed.z64 \
  --cc /path/to/mnsg/tools/ido-5.3/cc \
  --ld /path/to/mips-linux-gnu-ld \
  --objcopy /path/to/mips-linux-gnu-objcopy
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

USA_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
USA_SIZE = 33_554_432
FILE12_START_PC = 0x8020D2A0
FILE12_START_ROM = 0x5C8770


@dataclass(frozen=True)
class Isolate:
    filename: str
    symbol: str
    vma: int
    size: int
    expected_reloc_count: int
    external_addresses: tuple[tuple[str, int], ...]


ISOLATES = (
    Isolate("active_gate.c", "func_8021A644_5D5B14", 0x8021A644, 0x38, 1,
            (("func_8021A4E4_5D59B4", 0x8021A4E4),)),
    Isolate("update_dispatch.c", "func_80218E7C_5D434C", 0x80218E7C, 0xB4, 14,
            (("func_80217114_5D25E4", 0x80217114),
             ("func_80216AB8_5D1F88", 0x80216AB8),
             ("func_80224B88_5E0058", 0x80224B88),
             ("func_8021893C_5D3E0C", 0x8021893C),
             ("func_8021C444_5D7914", 0x8021C444),
             ("func_8021B808_5D6CD8", 0x8021B808),
             ("func_8021C518_5D79E8", 0x8021C518),
             ("func_8021A978_5D5E48", 0x8021A978),
             ("func_80218990_5D3E60", 0x80218990),
             ("func_8021B610_5D6AE0", 0x8021B610),
             ("func_80219F20_5D53F0", 0x80219F20),
             ("func_80218350_5D3820", 0x80218350),
             ("func_80218804_5D3CD4", 0x80218804),
             ("func_8021A328_5D57F8", 0x8021A328))),
    Isolate("state2_callback.c", "func_80218F30_5D4400", 0x80218F30, 0xB8, 10,
            (("func_80218E7C_5D434C", 0x80218E7C),
             ("func_80034ED4_35AD4", 0x80034ED4),
             ("func_80213ED0_5CF3A0", 0x80213ED0),
             ("D_8015CCBC", 0x8015CCBC),
             ("func_80034E08_35A08", 0x80034E08),
             ("func_80035244_35E44", 0x80035244))),
)


def rom_offset(vma: int) -> int:
    return FILE12_START_ROM + vma - FILE12_START_PC


def validate_image(image: bytes) -> str:
    digest = hashlib.sha1(image).hexdigest()
    if len(image) != USA_SIZE or digest != USA_SHA1:
        raise ValueError("Expected the exact original 32 MiB decompressed USA ROM")
    return digest


def check_relocations(readelf_output: str, expected: Isolate) -> None:
    entries = re.findall(r"\bR_MIPS_(26|HI16|LO16)\s+[0-9a-fA-F]+\s+(\S+)", readelf_output)
    if len(entries) != expected.expected_reloc_count:
        raise ValueError(f"{expected.symbol}: relocation count is {len(entries)}; "
                         f"expected {expected.expected_reloc_count}")
    symbols = {s for _, s in entries}
    expected_symbols = {s for s, _ in expected.external_addresses} | {expected.symbol}
    if not symbols.issubset(expected_symbols):
        raise ValueError(f"{expected.symbol}: unexpected symbol relocations {symbols - expected_symbols}")
    if not ({s for s, _ in expected.external_addresses} <= symbols):
        raise ValueError(f"{expected.symbol}: missing named external relocation")


def verify(rom: bytes, compiler: Path, linker: Path, objcopy: Path,
           readelf: Path, source_dir: Path) -> dict:
    rom_sha1 = validate_image(rom)
    checks = []
    with tempfile.TemporaryDirectory(prefix="goemon-file12-isolate-") as temp:
        scratch = Path(temp)
        for entry in ISOLATES:
            source = source_dir / entry.filename
            obj = scratch / (source.stem + ".o")
            elf = scratch / (source.stem + ".elf")
            code = scratch / (source.stem + ".bin")
            subprocess.run([str(compiler), "-c", "-G", "0", "-non_shared",
                            "-Xfullwarn", "-Xcpluscomm", "-Wab,-r4300_mul",
                            "-woff", "649,838,712", "-O2", "-mips2",
                            "-o", str(obj), str(source)], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            reloc_text = subprocess.check_output([str(readelf), "-r", str(obj)], text=True)
            check_relocations(reloc_text, entry)
            # Original functions can begin at 4-byte (not 16-byte) boundaries.
            # SUBALIGN(4) avoids spurious leading padding from ELF .text alignment.
            ldscript = scratch / (source.stem + ".ld")
            ldscript.write_text(
                "SECTIONS {\n"
                f"  . = 0x{entry.vma:X};\n"
                "  .text : SUBALIGN(4) { *(.text) }\n"
                "  .reginfo : { *(.reginfo) }\n"
                "  .mdebug : { *(.mdebug) }\n"
                "  /DISCARD/ : { *(.comment) *(.note*) }\n"
                "}\n"
            )
            linker_args = [str(linker), "-EB", "-m", "elf32btsmip",
                           "-T", str(ldscript), "-e", entry.symbol,
                           "-o", str(elf), str(obj)]
            linker_args.extend(f"--defsym={name}=0x{addr:X}"
                               for name, addr in entry.external_addresses)
            subprocess.run(linker_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run([str(objcopy), "-O", "binary", "-j", ".text", str(elf), str(code)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            candidate = code.read_bytes()
            if len(candidate) < entry.size or any(candidate[entry.size:]):
                raise ValueError(f"{entry.symbol}: unexpected extent or nonzero trailing bytes")
            actual = candidate[:entry.size]
            expected = rom[rom_offset(entry.vma):rom_offset(entry.vma) + entry.size]
            if actual != expected:
                differing = next(i for i, (a, b) in enumerate(zip(actual, expected)) if a != b)
                raise ValueError(f"{entry.symbol}: original-ROM mismatch at +0x{differing:X}")
            checks.append({"function": entry.symbol, "vma": f"0x{entry.vma:08X}",
                           "rom_start": f"0x{rom_offset(entry.vma):X}",
                           "bytes": entry.size, "relocations": entry.expected_reloc_count,
                           "sha256": hashlib.sha256(actual).hexdigest(),
                           "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    return {"status": "isolated_original_vma_code_exact", "rom_sha1": rom_sha1,
            "functions": len(checks), "matched_bytes": sum(c["bytes"] for c in checks),
            "relocations": sum(c["relocations"] for c in checks), "results": checks,
            "limitations": "No combined overlay layout, original ELF relocation multiset, or full-ROM G2 proof"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--cc", type=Path, required=True)
    parser.add_argument("--ld", type=Path, required=True)
    parser.add_argument("--objcopy", type=Path, required=True)
    parser.add_argument("--readelf", type=Path, default=Path("/usr/bin/readelf"))
    parser.add_argument("--source-dir", type=Path, default=Path(__file__).parent)
    opts = parser.parse_args()
    result = verify(opts.rom.read_bytes(), opts.cc, opts.ld, opts.objcopy,
                    opts.readelf, opts.source_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
