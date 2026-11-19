"""Stage Japanese warp dispatcher func_80036D00_37900 as tenth exact C.

Preserves all previous nine Japanese C functions and original USA source.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from . import japan_nine_c as nine

SOURCE_FILE = Path("src/jp_warp_call_37900.c")
SOURCE_LOCAL = Path(__file__).resolve().parent / "japan_matching/jp_warp_call_37900.c"
SPLAT_CONFIG = Path("config/japan_0/splat_ten_c.local.yaml")
BEFORE = "    - [0x37900, asm, main_37900] # Warps"
AFTER = "    - [0x37900, c, jp_warp_call_37900]\n    - [0x37920, asm, main_37920] # Warps"
FUNCTION_NAME = "func_80036D00_37900"
ROM_OFFSET = 0x37900
VMA = 0x80036D00
SIZE = 32


def render_config(previous: str) -> str:
    if previous.count(BEFORE) != 1:
        raise ValueError("Expected unique original Japanese warp segment")
    for label in (
        "[0x12D60, c, jp_motion_12D60]",
        "[0x13B70, c, jp_camera_13B70]",
        "[0x16DF0, c, jp_bit_array]",
        "[0x378D0, c, jp_mode_flags]",
        "[0x38620, c, jp_main_38620]",
    ):
        if label not in previous:
            raise ValueError("Missing previously verified nine-C source: " + label)
    if "[0x37920," in previous:
        raise ValueError("Tenth Japanese C stage already inserted")
    return previous.replace(BEFORE, AFTER, 1)


def stage_config(checkout: Path) -> Path:
    prior = nine.stage_config(checkout)
    rendered = render_config(prior.read_text(encoding="utf-8"))
    target = checkout / SPLAT_CONFIG
    if target.exists() and target.read_text(encoding="utf-8") != rendered:
        raise FileExistsError("Refusing unexpected Japanese ten-C Splat config")
    target.write_text(rendered, encoding="utf-8")
    return target


def install_source(checkout: Path) -> Path:
    expected = SOURCE_LOCAL.read_bytes()
    target = checkout / SOURCE_FILE
    if target.exists():
        previous = target.read_bytes()
        if previous == expected:
            return target
        stub = (b'asm/japan_0/nonmatchings/jp_warp_call_37900/'
                b'func_80036D00_37900.s')
        if previous.count(b"#pragma GLOBAL_ASM") != 1 or stub not in previous:
            raise FileExistsError("Refusing modified Japanese warp C source")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(expected)
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage-config", "install-source"))
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args(argv)
    root = args.checkout.resolve(strict=True)
    print(stage_config(root) if args.command == "stage-config" else install_source(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
