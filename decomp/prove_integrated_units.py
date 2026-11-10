"""Prove combined translation-unit codegen against private original ROM.

Research only: these are standalone reconstructed units, not production manifest
promotions and not the upstream 2,331-object full-ROM build. The known object
dispatcher mismatch MUST fail closed. Do not alter reference ROM or expected bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

if __package__:
    from .prove_three_wrappers import ROM_SHA1, ORIGINAL_LENGTH, verified_symbol_size_and_address
else:
    from prove_three_wrappers import ROM_SHA1, ORIGINAL_LENGTH, verified_symbol_size_and_address

ROOT = Path(__file__).resolve().parent
SPECS = (
    {
        "unit": "resource_dispatch",
        "file": "integrated_resource_dispatch_probe.c",
        "offset": 0x35AD4,
        "size": 112,
        "sha256": "112211df4914a811c3f7327164b35372f8e0fd3976e267179aec446b22fb3674",
        "symbols": (("func_80034ED4_35AD4", 0, 36),
                    ("func_80034EF8_35AF8", 36, 40),
                    ("func_80034F20_35B20", 76, 36)),
        "globals": {
            "D_8016DAB4_16E6B4": 0x8016DAB4,
            "func_80034F44_35B44": 0x80034F44,
            "func_80035044_35C44": 0x80035044,
        },
    },
    {
        "unit": "object_dispatch",
        "file": "integrated_object_dispatch_probe.c",
        "offset": 0x35C64,
        "size": 96,
        "sha256": "519d1d7cf498a599e461bc9f99d1eb3df338d661641f7ce1b8d68bd36e8ad17c",
        "symbols": (("func_80035064_35C64", 0, 48),
                    ("func_80035094_35C94", 48, 48)),
        "globals": {
            "D_8016DAB4_16E6B4": 0x8016DAB4,
            "func_800362DC_36EDC": 0x800362DC,
            "func_80035044_35C44": 0x80035044,
            "func_800350C4_35CC4": 0x800350C4,
        },
    },
    {
        "unit": "empty_menu_hook",
        "file": "integrated_empty_menu_hook_probe.c",
        "offset": 0x12758,
        "size": 256,
        "sha256": "7206359946bbffa08fd481c09f6218dd2c86ebb8115e97aad6dc82b13894dcc2",
        "symbols": (("func_80011B58_12758", 0, 8),
                    ("func_80011B60_12760", 8, 84),
                    ("func_80011BB4_127B4", 92, 80),
                    ("func_80011C04_12804", 172, 84)),
        "globals": {
            "D_801FC624_5B8534": 0x801FC624,
            "D_801FC628_5B8538": 0x801FC628,
            "D_8015C5C8_15D1C8": 0x8015C5C8,
        },
    },
)

def compare_unit(candidate: bytes, original: bytes, spec: dict) -> dict:
    """Fail closed on symbol/unit extent and reference fingerprint mismatch."""
    if len(candidate) != spec["size"] or len(original) != spec["size"]:
        raise ValueError(f'{spec["unit"]}: wrong translation-unit byte length')
    if hashlib.sha256(original).hexdigest() != spec["sha256"]:
        raise ValueError(f'{spec["unit"]}: original translation-unit SHA-256 changed')
    mismatched = [i for i, (a, b) in enumerate(zip(candidate, original)) if a != b]
    return {
        "unit": spec["unit"],
        "rom_offset": hex(spec["offset"]),
        "size": spec["size"],
        "exact_original_bytes": candidate == original,
        "mismatched_byte_count": len(mismatched),
        "mismatched_offsets": [hex(i) for i in mismatched[:24]],
        "functions": [
            {"name": name, "bytes": length,
             "exact_original_bytes": candidate[start:start+length] == original[start:start+length]}
            for name, start, length in spec["symbols"]
        ],
    }

def run(rom_path: Path, ido: Path, linker: Path, objcopy: Path, readelf: Path) -> list[dict]:
    rom = rom_path.read_bytes()
    if len(rom) != ORIGINAL_LENGTH or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('incorrect decompressed original ROM SHA-1 or size')
    result = []
    with tempfile.TemporaryDirectory(prefix="goemon-integrated-probe-") as d:
        work = Path(d)
        for spec in SPECS:
            src = ROOT / "candidates" / spec["file"]
            obj, elf, binary = (work / n for n in ("unit.o", "unit.elf", "unit.bin"))
            original_vma = spec["offset"] + 0x7FFFF400
            symbols = "".join(f"{name} = 0x{address:08X};\n" for name,address in spec["globals"].items())
            script = work / "unit.ld"
            script.write_text(
                "OUTPUT_ARCH(mips)\n" + symbols +
                f"SECTIONS {{ .text 0x{original_vma:08X} : SUBALIGN(4) {{ *(.text) }} }}\n"
            )
            subprocess.run([str(ido), "-c", "-O2", "-mips2", "-G", "0", "-non_shared",
                            str(src), "-o", str(obj)], check=True, capture_output=True)
            subprocess.run([str(linker), "-m", "elf32btsmip", "-T", str(script),
                            str(obj), "-o", str(elf)], check=True, capture_output=True)
            table = subprocess.run([str(readelf), "-Ws", str(elf)], check=True,
                                   capture_output=True, text=True).stdout
            for name, start, length in spec["symbols"]:
                verified_symbol_size_and_address(table, name, original_vma+start, length)
            subprocess.run([str(objcopy), "-O", "binary", "--only-section=.text",
                            str(elf), str(binary)], check=True, capture_output=True)
            candidate = binary.read_bytes()
            original = rom[spec["offset"]:spec["offset"] + spec["size"]]
            result.append(compare_unit(candidate, original, spec))
    return result

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rom", type=Path, required=True)
    p.add_argument("--ido", type=Path, required=True)
    p.add_argument("--linker", type=Path, default=Path("ld.lld"))
    p.add_argument("--objcopy", type=Path, default=Path("llvm-objcopy"))
    p.add_argument("--readelf", type=Path, default=Path("readelf"))
    args = p.parse_args()
    result = run(args.rom, args.ido, args.linker, args.objcopy, args.readelf)
    print(json.dumps({"full_project_rom_verified": False,
                      "new_promotions": 0, "units": result}, indent=2))
    return 0 if all(item["exact_original_bytes"] for item in result) else 1

if __name__ == "__main__":
    raise SystemExit(main())
