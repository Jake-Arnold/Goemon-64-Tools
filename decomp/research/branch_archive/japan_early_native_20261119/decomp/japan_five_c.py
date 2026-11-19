"""An exact fifth Japanese C function: motion/parameter setting at ROM 0x12D60.

The original upstream mnsg Splat configuration and USA decomp are not modified.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from . import japan_four_c as four

SOURCE_FILE = Path('src/jp_motion_12D60.c')
SOURCE_LOCAL = Path(__file__).resolve().parent / 'japan_matching/jp_motion_12D60.c'
SPLAT_CONFIG = Path('config/japan_0/splat_five_c.local.yaml')
BEFORE = '    - [0x122F0, asm, main_122F0]'
AFTER = BEFORE + '\n    - [0x12D60, c, jp_motion_12D60]\n    - [0x12D80, asm, main_12D80]'
FUNCTION_NAME = 'func_80012160_12D60'
ROM_OFFSET = 0x12D60
VMA = 0x80012160
SIZE = 32


def render_config(four_c_config: str) -> str:
    if four_c_config.count(BEFORE) != 1:
        raise ValueError('Expected unique Japanese main_122F0 assembly segment')
    if '    - [0x16DF0, c, jp_bit_array]' not in four_c_config or '    - [0x38620, c, jp_main_38620]' not in four_c_config:
        raise ValueError('Existing Japanese matching-C units are absent')
    if '[0x12D60,' in four_c_config:
        raise ValueError('Fifth Japanese C segment is already inserted')
    return four_c_config.replace(BEFORE, AFTER, 1)


def stage_config(checkout: Path) -> Path:
    previous = four.stage_config(checkout)
    content = render_config(previous.read_text(encoding='utf-8'))
    target = checkout / SPLAT_CONFIG
    if target.exists() and target.read_text(encoding='utf-8') != content:
        raise FileExistsError(f'Refusing changed Japanese Splat config: {target}')
    target.write_text(content, encoding='utf-8')
    return target


def install_source(checkout: Path) -> Path:
    data = SOURCE_LOCAL.read_bytes()
    target = checkout / SOURCE_FILE
    if target.exists():
        old = target.read_bytes()
        if old == data:
            return target
        stub = b'#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_motion_12D60/func_80012160_12D60.s")'
        if old.count(b'#pragma GLOBAL_ASM') != 1 or stub not in old:
            raise FileExistsError('Refusing to overwrite modified Japanese C source')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return target


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['stage-config','install-source'])
    p.add_argument('checkout', type=Path)
    args=p.parse_args(argv)
    root=args.checkout.resolve(strict=True)
    print(stage_config(root) if args.command == 'stage-config' else install_source(root))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
