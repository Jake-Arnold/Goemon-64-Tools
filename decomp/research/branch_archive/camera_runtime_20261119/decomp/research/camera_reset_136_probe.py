"""Reproduce one authentic USA camera reset matching-C function with IDO 5.3.

Research gate only: does not change the production manifest or prove full-ROM G2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

RETAIL_DECOMPRESSED_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ORIGINAL_FUNC_SHA256 = "f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a"
SOURCE_SHA256 = "9d47ba199dfd48f5707b7623f45eee5e0853110f725e08bcf4ad7c151f7450c4"
ROM_START, ROM_END = 0x5B56E4, 0x5B576C
EXPECTED_VMA = 0x801F97D4
LINKER_SCRIPT = """OUTPUT_ARCH(mips)
D_800BCCC0_BD8C0 = 0x800BCCC0;
D_8008CCC0_8D8C0 = 0x8008CCC0;
SECTIONS {
  . = 0x801F97D4;
  .text : SUBALIGN(4) { *(.text) }
  /DISCARD/ : { *(.reginfo) *(.mdebug) *(.options) *(.comment) }
}
"""


def digest(data: bytes, algo: str) -> str:
    return hashlib.new(algo, data).hexdigest()


def prove(rom: Path, compiler: Path, linker: Path, objcopy: Path, source: Path) -> dict:
    raw = rom.read_bytes()
    if len(raw) != 32 * 1024 * 1024 or digest(raw, "sha1") != RETAIL_DECOMPRESSED_SHA1:
        raise ValueError("The supplied file is not the authenticated decompressed USA ROM")
    original = raw[ROM_START:ROM_END]
    if digest(original, "sha256") != ORIGINAL_FUNC_SHA256:
        raise ValueError("Original USA function slice differs from pinned proof")
    if digest(source.read_bytes(), "sha256") != SOURCE_SHA256:
        raise ValueError("Matching-C source has changed; proof requires review")
    with tempfile.TemporaryDirectory(prefix="goemon-usa-camera-reset-") as temp:
        tmp = Path(temp)
        obj, elf, binary = (tmp / name for name in ("probe.o", "probe.elf", "probe.bin"))
        script = tmp / "linker.ld"
        script.write_text(LINKER_SCRIPT, encoding="utf-8")
        compile_args = [str(compiler), "-c", "-G", "0", "-non_shared", "-Xfullwarn",
                        "-Xcpluscomm", "-Wab,-r4300_mul", "-woff", "649,838,712",
                        "-D_LANGUAGE_C", "-D_FINALROM", "-DF3DEX_GBI", "-D__sgi",
                        "-DNDEBUG", "-O2", "-mips2", "-o", str(obj), str(source)]
        subprocess.run(compile_args, check=True, capture_output=True, text=True)
        subprocess.run([str(linker), "-m", "elf32btsmip", "-T", str(script), "-o",
                        str(elf), str(obj)], check=True, capture_output=True, text=True)
        subprocess.run([str(objcopy), "-O", "binary", "--only-section=.text",
                        str(elf), str(binary)], check=True, capture_output=True, text=True)
        compiled_text = binary.read_bytes()
        if len(compiled_text) != 144 or compiled_text[136:] != bytes(8):
            raise ValueError("Unexpected function/linker text size or trailing alignment")
        actual = compiled_text[:ROM_END-ROM_START]
        if actual != original:
            first_diff = next((i for i, (a, b) in enumerate(zip(actual, original)) if a != b), None)
            raise ValueError(f"IDO source is not matching-C; first mismatch at offset {first_diff}")
        return {
            "status": "PASS", "scope": "isolated-original-USA-VMA-native-IDO-not-central-G2",
            "function": "func_801F97D4_5B56E4", "vma": hex(EXPECTED_VMA),
            "rom_range": [hex(ROM_START), hex(ROM_END)], "matching_code_bytes": len(original),
            "matching_instructions": len(original)//4, "source_sha256": SOURCE_SHA256,
            "compiled_text_sha256": digest(actual, "sha256"),
            "decompressed_rom_sha1": RETAIL_DECOMPRESSED_SHA1,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="Authenticated decompressed 32MiB USA ROM")
    parser.add_argument("--ido", type=Path, required=True, help="Path to original IDO 5.3 cc executable")
    parser.add_argument("--ld", type=Path, required=True, help="Path to big-endian MIPS GNU ld")
    parser.add_argument("--objcopy", type=Path, required=True, help="Path to MIPS GNU objcopy")
    parser.add_argument("--source", type=Path, default=Path(__file__).with_name("camera_reset_usa_5b56e4.c"))
    args = parser.parse_args()
    print(json.dumps(prove(args.rom, args.ido, args.ld, args.objcopy, args.source), indent=2))


if __name__ == "__main__":
    main()
