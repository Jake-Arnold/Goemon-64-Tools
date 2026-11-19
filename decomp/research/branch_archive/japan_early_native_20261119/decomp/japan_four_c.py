"""Stage and prove three additional Japanese bit-array C functions.

This opt-in variant extends the separately verified first-Japanese-C baseline.
The default USA build, upstream original Splat config and private ROMs are not changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from decomp import japan_asm_baseline as baseline
from decomp import japan_first_c as first

SOURCE_FILE = Path("src/jp_bit_array.c")
SOURCE_LOCAL = Path(__file__).resolve().parent / "japan_matching/jp_bit_array.c"
SPLAT_CONFIG = Path("config/japan_0/splat_four_c.local.yaml")
NEXT_SEGMENT = "    - [0x16E70, asm, main_16E70]"
NEW_SEGMENT = "    - [0x16DF0, c, jp_bit_array] # Three matching bit-array functions\n"
ROM_OFFSET = 0x16DF0
SECTION_SIZE = 128
FUNCTIONS = (
    ("func_800161F0_16DF0", "0x800161F0", 36),
    ("func_80016214_16E14", "0x80016214", 40),
    ("func_8001623C_16E3C", "0x8001623C", 52),
)


def render_config(previous: str) -> str:
    if previous.count(NEXT_SEGMENT) != 1:
        raise ValueError("Expected unique Japanese Splat segment following bit array")
    if "    - [0x15500, asm, main_15500]" not in previous:
        raise ValueError("Expected original Japanese segment preceding bit array")
    if "[0x38620, c, jp_main_38620]" not in previous:
        raise ValueError("Missing previously verified first-C Japanese segment")
    if "[0x16DF0," in previous:
        raise ValueError("Bit-array segment has already been inserted")
    return previous.replace(NEXT_SEGMENT, NEW_SEGMENT + NEXT_SEGMENT, 1)


def stage_config(root: Path) -> Path:
    parent = first.stage_config(root)
    rendered = render_config(parent.read_text(encoding="utf-8"))
    target = root / SPLAT_CONFIG
    if target.exists() and target.read_text(encoding="utf-8") != rendered:
        raise FileExistsError(f"Refusing changed Splat configuration: {target}")
    target.write_text(rendered, encoding="utf-8")
    return target


def install_source(root: Path) -> Path:
    source = SOURCE_LOCAL.read_text(encoding="utf-8")
    target = root / SOURCE_FILE
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if existing == source:
            return target
        if (existing.count("#pragma GLOBAL_ASM") != len(FUNCTIONS)
            or any(f"asm/japan_0/nonmatchings/jp_bit_array/{name}.s" not in existing
                   for name, _vram, _size in FUNCTIONS)
            or not existing.startswith('#include "common.h"')):
            raise FileExistsError(f"Refusing to overwrite non-generated source: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    return target


def _dump_text(objcopy: str, obj: Path) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "text.bin"
        subprocess.run([objcopy, "--dump-section", f".text={dest}", str(obj)],
                       check=True, capture_output=True)
        return dest.read_bytes()


def verify(root: Path, retail_output: Path, objcopy: str = "mips-linux-gnu-objcopy",
           objdump: str = "mips-linux-gnu-objdump") -> dict:
    proof = first.verify(root, retail_output, objcopy=objcopy)
    obj = root / "build/japan_0/src/jp_bit_array.c.o"
    if not obj.is_file():
        raise FileNotFoundError(f"Missing Japanese bit-array C object: {obj}")
    data = _dump_text(objcopy, obj)
    original = (root / "config/japan_0/baserom.decompressed.z64").read_bytes()
    expected = original[ROM_OFFSET:ROM_OFFSET + SECTION_SIZE]
    if len(data) != SECTION_SIZE or data != expected:
        raise ValueError("Japanese bit-array IDO object text does not match original bytes")
    reloc = subprocess.run([objdump, "-r", "-j", ".text", str(obj)],
                           check=True, capture_output=True, text=True).stdout
    if "RELOCATION RECORDS FOR [.text]" in reloc:
        raise ValueError("Japanese bit-array object unexpectedly contains text relocations")
    proof["matching_c"] = {
        "count": 4,
        "function_bytes": 136,
        "no_op_function": first.FUNCTION_NAME,
        "bit_array_functions": [
            {"name": name, "vram": vram, "size": size,
             "rom_offset": hex(ROM_OFFSET + sum(x[2] for x in FUNCTIONS[:idx]))}
            for idx, (name, vram, size) in enumerate(FUNCTIONS)
        ],
        "bit_array_text_size": SECTION_SIZE,
        "bit_array_text_sha256": hashlib.sha256(data).hexdigest(),
        "bit_array_text_relocation_count": 0,
        "all_japanese_c_object_bytes_match": True,
        "complete_32mib_image_match": True,
        "compressed_16mib_image_match": True,
        "status": "PASS",
    }
    proof["method"] = "four Japanese native-IDO matched-C functions; all remaining original assembly"
    return proof


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for action in ("stage-config", "install-source", "verify"):
        p = subs.add_parser(action)
        p.add_argument("checkout", type=Path)
        if action == "verify":
            p.add_argument("--retail-output", type=Path, required=True)
            p.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    root = args.checkout.resolve(strict=True)
    if args.command == "stage-config":
        print(stage_config(root))
    elif args.command == "install-source":
        print(install_source(root))
    else:
        proof = verify(root, args.retail_output)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(proof, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
