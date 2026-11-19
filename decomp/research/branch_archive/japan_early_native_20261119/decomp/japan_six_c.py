"""Stage the sixth exact Japanese N64 IDO C function at ROM 0x13B70.

Keep original mnsg and USA configurations untouched; refuse unexpected changes.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import japan_five_c as five

SOURCE_FILE = Path('src/jp_camera_13B70.c')
SOURCE_LOCAL = Path(__file__).resolve().parent / 'japan_matching/jp_camera_13B70.c'
SPLAT_CONFIG = Path('config/japan_0/splat_six_c.local.yaml')
BEFORE = '    - [0x140D0, asm, wave_uty]'
AFTER = ('    - [0x13B70, c, jp_camera_13B70]\n'
         '    - [0x13B90, asm, main_13B90]\n' + BEFORE)
FUNCTION_NAME = 'func_80012F70_13B70'
ROM_OFFSET = 0x13B70
VMA = 0x80012F70
SIZE = 32


def render_config(five_c_config: str) -> str:
    if five_c_config.count(BEFORE) != 1:
        raise ValueError('Expected unique Japanese wave_uty segment boundary')
    if ('    - [0x12D60, c, jp_motion_12D60]' not in five_c_config or
            '    - [0x16DF0, c, jp_bit_array]' not in five_c_config or
            '    - [0x38620, c, jp_main_38620]' not in five_c_config):
        raise ValueError('Previously verified Japanese C units are missing')
    if '[0x13B70,' in five_c_config or '[0x13B90,' in five_c_config:
        raise ValueError('Sixth Japanese C segment has already been inserted')
    return five_c_config.replace(BEFORE, AFTER, 1)


def stage_config(checkout: Path) -> Path:
    parent = five.stage_config(checkout)
    rendered = render_config(parent.read_text(encoding='utf-8'))
    target = checkout / SPLAT_CONFIG
    if target.exists() and target.read_text(encoding='utf-8') != rendered:
        raise FileExistsError(f'Refusing to overwrite modified Japanese Splat stage: {target}')
    target.write_text(rendered, encoding='utf-8')
    return target


def install_source(checkout: Path) -> Path:
    expected = SOURCE_LOCAL.read_bytes()
    target = checkout / SOURCE_FILE
    if target.exists():
        previous = target.read_bytes()
        if previous == expected:
            return target
        stub = (b'#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/'
                b'jp_camera_13B70/func_80012F70_13B70.s")')
        if previous.count(b'#pragma GLOBAL_ASM') != 1 or stub not in previous:
            raise FileExistsError('Refusing to overwrite edited Japanese C source')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(expected)
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('stage-config', 'install-source'))
    parser.add_argument('checkout', type=Path)
    args = parser.parse_args(argv)
    checkout = args.checkout.resolve(strict=True)
    result = stage_config(checkout) if args.command == 'stage-config' else install_source(checkout)
    print(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
