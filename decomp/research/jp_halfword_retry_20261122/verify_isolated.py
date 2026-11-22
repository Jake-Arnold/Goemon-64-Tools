#!/usr/bin/env python3
"""Read-only isolated native IDO comparisons. NOT complete-ROM or G2 promotion."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import tempfile

EXPECTED_ROM_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
FUNCTIONS = [
 ('func_80219328_6A0A28', 0x6A0A28, 28),
 ('func_80222F18_68C608', 0x68C608, 28),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', type=Path, required=True, help='Original expanded 32 MiB Japan rev-0 .z64')
    ap.add_argument('--cc', type=Path, required=True, help='Pinned SGI IDO 5.3 cc executable')
    ap.add_argument('--objcopy', default='mips-linux-gnu-objcopy', help='MIPS GNU objcopy')
    args = ap.parse_args()
    orig = args.rom.read_bytes()
    assert len(orig) == 33554432 and hashlib.sha1(orig).hexdigest() == EXPECTED_ROM_SHA1, 'ROM reference mismatch'
    srcdir = Path(__file__).resolve().parent / 'src'
    with tempfile.TemporaryDirectory(prefix='goemon-jp-halfword-') as work:
        for name, off, size in FUNCTIONS:
            src = srcdir / (name + '.c')
            obj = Path(work) / (name + '.o')
            text = Path(work) / (name + '.text')
            subprocess.run([str(args.cc), '-c', '-G', '0', '-non_shared', '-O2', '-mips2', '-o', str(obj), str(src)], check=True)
            subprocess.run([args.objcopy, '-O', 'binary', '--only-section=.text', str(obj), str(text)], check=True)
            compiled = text.read_bytes()
            assert compiled[:size] == orig[off:off+size], f'{name}: first mismatch at '+str(next((i for i in range(size) if compiled[i]!=orig[off+i]), '?'))
            assert len(compiled) in (size, size+4), f'{name}: unexpected .text extent {len(compiled)}'
            print(f'PASSED_ISOLATED_NATIVE {name}: {size}/{size} bytes, offset=0x{off:X}, section={len(compiled)} bytes')
    print('NO_G2_CLAIM: combined full-ROM, ELF, relocation, inventory and local CI not run by this verifier')

if __name__ == '__main__':
    main()
