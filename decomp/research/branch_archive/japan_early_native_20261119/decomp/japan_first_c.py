"""Stage and verify the first Japanese rev-0 exact native-IDO C replacement.

Only operates on an external pinned mnsg checkout, never on cartridge data.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
from decomp import japan_asm_baseline as baseline

BASE_CONFIG = baseline.ASM_CONFIG
FIRST_CONFIG = Path("config/japan_0/splat_one_c.local.yaml")
SOURCE_FILE = Path("src/jp_main_38620.c")
SOURCE_LOCAL = Path(__file__).resolve().parent / "japan_matching/jp_main_38620.c"
SEGMENT_OLD = "[0x38620, asm, main_38620]"
SEGMENT_NEW = "[0x38620, c, jp_main_38620]"
FUNCTION_NAME = "func_80037A20_38620"
ROM_OFFSET = 0x38620
FUNCTION_SIZE = 8
OBJECT_SECTION_SIZE = 16


def render_config(asm_config: str) -> str:
    if asm_config.count(SEGMENT_OLD) != 1:
        raise ValueError("Expected exactly one Japanese original assembly segment")
    return asm_config.replace(SEGMENT_OLD, SEGMENT_NEW)


def stage_config(root: Path) -> Path:
    asm_config = baseline.stage_config(root)
    output = render_config(asm_config.read_text(encoding="utf-8"))
    target = root / FIRST_CONFIG
    if target.exists() and target.read_text(encoding="utf-8") != output:
        raise FileExistsError("Japanese single-C config has unexpected contents")
    target.write_text(output, encoding="utf-8")
    return target


def install_source(root: Path) -> Path:
    content = SOURCE_LOCAL.read_text(encoding="utf-8")
    target = root / SOURCE_FILE
    if target.exists():
        current = target.read_text(encoding="utf-8")
        if current == content:
            return target
        # Splat creates a source stub with this explicit, matching path.
        stub = '#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_main_38620/func_80037A20_38620.s")'
        if stub not in current or current.count("#pragma GLOBAL_ASM") != 1:
            raise FileExistsError("Refusing to overwrite non-Splat Japanese C source")
    target.write_text(content, encoding="utf-8")
    return target


def verify(root: Path, retail_output: Path, objcopy: str = "mips-linux-gnu-objcopy") -> dict:
    result = baseline.verify(root, retail_output)
    obj = root / "build/japan_0/src/jp_main_38620.c.o"
    if not obj.is_file():
        raise FileNotFoundError(f"Missing linked Japanese C object: {obj}")
    with tempfile.TemporaryDirectory() as d:
        extracted = Path(d) / "text.bin"
        subprocess.run([objcopy, "--dump-section", f".text={extracted}", str(obj)], check=True)
        actual = extracted.read_bytes()
    expected = (root / "config/japan_0/baserom.decompressed.z64").read_bytes()[ROM_OFFSET:ROM_OFFSET+OBJECT_SECTION_SIZE]
    if len(actual) != OBJECT_SECTION_SIZE or actual != expected:
        raise ValueError("IDO C object .text does not match original Japanese segment")
    result["method"] = "one Japanese native IDO 5.3 matching-C replacement; all remaining sections assembly"
    result["matching_c"] = {"function":FUNCTION_NAME,"rom_offset":"0x38620",
                           "vram":"0x80037A20", "function_size":FUNCTION_SIZE,
                           "object_text_size":OBJECT_SECTION_SIZE,
                           "sha256":hashlib.sha256(actual).hexdigest(),
                           "original_function_bytes_match": True,
                           "linked_full_32mib_image_match":True,
                           "recompressed_16mib_image_match":True,
                           "status":"PASS"}
    return result


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command", required=True)
    for cmd in ("stage-config","install-source","verify"):
        s=sub.add_parser(cmd)
        s.add_argument("checkout", type=Path)
        if cmd=="verify":
            s.add_argument("--retail-output", type=Path, required=True)
            s.add_argument("--report", type=Path)
    args=p.parse_args(argv)
    root=args.checkout.resolve(strict=True)
    if args.command=="stage-config":
        print(stage_config(root))
    elif args.command=="install-source":
        print(install_source(root))
    else:
        report=verify(root,args.retail_output)
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(report,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
