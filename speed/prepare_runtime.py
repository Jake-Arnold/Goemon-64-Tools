"""Prepare a pinned N64ModernRuntime checkout for a fixed startup speed.

This modifies the explicitly supplied clean checkout. It does not build or launch
an executable. The speed is chosen by GOEMON_SPEED_MULTIPLIER at process start.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

PIN = 'fc4592a31414daf0040c19907e0b1976b2e48a67'
BEFORE = 'constexpr uint32_t speed_multiplier = 1;'
AFTER = 'const uint32_t speed_multiplier = goemon_speed::startup_multiplier();'
INCLUDE = '#include "ultramodern/ultra64.h"'
HEADER = Path(__file__).resolve().parent / 'startup_multiplier.h'


def prepare_runtime(root: Path) -> None:
    root = root.resolve(strict=True)
    revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != PIN:
        raise ValueError('Runtime checkout is not at the verified commit')
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=all'], text=True)
    if dirty.strip():
        raise ValueError('Runtime checkout has local changes; use a clean isolated checkout')
    source = root / 'ultramodern/src/timer.cpp'
    installed_header = root / 'ultramodern/src/goemon_startup_multiplier.h'
    if installed_header.exists():
        raise ValueError('Runtime speed header already exists')
    data = source.read_text(encoding='utf-8')
    counter = 'constexpr uint32_t counter_per_ms = 46\'875 * speed_multiplier;'
    if data.count(BEFORE) != 1 or data.count(INCLUDE) != 1 or data.count(counter) != 1:
        raise ValueError('Runtime timing source differs from the expected pinned layout')
    changed = data.replace(INCLUDE, INCLUDE+'\n#include "goemon_startup_multiplier.h"', 1)
    changed = changed.replace(BEFORE, AFTER, 1)
    changed = changed.replace(counter, 'const uint32_t counter_per_ms = 46\'875 * speed_multiplier;', 1)
    header_data = HEADER.read_bytes()
    # Create exclusively so an existing local file is never overwritten.
    with installed_header.open('xb') as handle:
        handle.write(header_data)
    temp_path = None
    try:
        # Publish the modified source atomically; never truncate the original.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=source.parent, prefix='.goemon-speed-',
                                         suffix='.tmp', delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(changed)
        os.chmod(temp_path, source.stat().st_mode)
        os.replace(temp_path, source)
    except Exception:
        if temp_path is not None:temp_path.unlink(missing_ok=True)
        installed_header.unlink(missing_ok=True)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runtime', type=Path, help='Clean isolated pinned N64ModernRuntime checkout')
    args = parser.parse_args(argv)
    prepare_runtime(args.runtime)
    print('Prepared startup-speed runtime; rebuild the recomp before use.')


if __name__ == '__main__':
    main()
