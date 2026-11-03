"""Launch a speed-enabled recomp build with a fixed startup multiplier.

The executable must be built with the startup-speed runtime patch. This launcher
requests a rate; it cannot independently verify that the executable honors it.
"""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def launch(executable: Path, multiplier: int):
    if type(multiplier) is not int or multiplier not in (1, 2, 3, 4):
        raise ValueError('Startup multiplier must be 1, 2, 3 or 4')
    executable = executable.resolve(strict=True)
    if not executable.is_file():
        raise ValueError('Choose an executable file')
    env = os.environ.copy()
    env['GOEMON_SPEED_MULTIPLIER'] = str(multiplier)
    return subprocess.Popen([str(executable)], cwd=str(executable.parent), env=env)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path, help='Recomp built with startup-speed runtime')
    parser.add_argument('--multiplier', required=True, type=int, choices=(1, 2, 3, 4))
    args = parser.parse_args(argv)
    process = launch(args.executable, args.multiplier)
    print(f'Launched PID {process.pid} with {args.multiplier}x requested; '
          'the executable must include the startup-speed runtime patch.')


if __name__ == '__main__':
    main()
