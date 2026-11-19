"""Stage three original-address Japanese mode setters after the six-C baseline.

The upstream Splat config and existing USA source files remain unchanged.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from . import japan_six_c as six

SOURCE_FILE = Path("src/jp_mode_flags.c")
SOURCE_LOCAL = Path(__file__).resolve().parent / "japan_matching/jp_mode_flags.c"
SPLAT_CONFIG = Path("config/japan_0/splat_nine_c.local.yaml")
BEFORE = "    - [0x37870, asm, main_37870]"
AFTER = (BEFORE + "\n"
         "    - [0x378D0, c, jp_mode_flags]\n"
         "    - [0x37900, asm, main_37900]")
FUNCTIONS = (
    ("func_80036CD0_378D0", 0x378D0, 0x80036CD0, 16),
    ("func_80036CE0_378E0", 0x378E0, 0x80036CE0, 16),
    ("func_80036CF0_378F0", 0x378F0, 0x80036CF0, 16),
)


def render_config(previous: str) -> str:
    if previous.count(BEFORE) != 1:
        raise ValueError("Expected original Japanese warp segment boundary")
    required = (
        "[0x12D60, c, jp_motion_12D60]",
        "[0x13B70, c, jp_camera_13B70]",
        "[0x16DF0, c, jp_bit_array]",
        "[0x38620, c, jp_main_38620]",
    )
    if not all(s in previous for s in required):
        raise ValueError("Verified six-C Japanese baseline not present")
    if "[0x378D0," in previous or "[0x37900," in previous:
        raise ValueError("Mode setter source section already staged")
    return previous.replace(BEFORE, AFTER, 1)


def stage_config(checkout: Path) -> Path:
    previous = six.stage_config(checkout)
    rendered = render_config(previous.read_text(encoding="utf-8"))
    target = checkout / SPLAT_CONFIG
    if target.exists() and target.read_text(encoding="utf-8") != rendered:
        raise FileExistsError("Refusing modified nine-C Splat config")
    target.write_text(rendered, encoding="utf-8")
    return target


def install_source(checkout: Path) -> Path:
    expected = SOURCE_LOCAL.read_bytes()
    target = checkout / SOURCE_FILE
    if target.exists():
        original = target.read_bytes()
        if original == expected:
            return target
        stubs = [
            ("asm/japan_0/nonmatchings/jp_mode_flags/" + name + ".s").encode()
            for name, _rom, _vma, _size in FUNCTIONS
        ]
        if original.count(b"#pragma GLOBAL_ASM") != 3 or any(stub not in original for stub in stubs):
            raise FileExistsError("Refusing to replace edited Japanese C source")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(expected)
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage-config", "install-source"))
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args(argv)
    root = args.checkout.resolve(strict=True)
    output = stage_config(root) if args.command == "stage-config" else install_source(root)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
