"""Nonblocking, local-only build of the bundled native input bridge."""
from concurrent.futures import Future
from pathlib import Path
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
_lock = threading.Lock()
_future = None


def default_input_path(root=ROOT):
    suffix = '.dylib' if sys.platform == 'darwin' else '.so'
    return root / 'build' / ('goemon_mupen_input' + suffix)


def build_default_input(root=ROOT):
    if sys.platform not in ('linux', 'darwin') or getattr(sys, 'frozen', False):
        raise RuntimeError('Native input build requires a Linux/macOS source checkout')
    try:
        result = subprocess.run(['bash', 'scripts/build_mupen_input.sh', '--if-needed'],
                                cwd=root, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f'Native input build could not run: {exc}') from exc
    path = default_input_path(root)
    if result.returncode or not path.is_file():
        detail = (result.stderr or result.stdout).strip().splitlines()[-4:]
        raise RuntimeError('Native input build failed. Install the matching Mupen64Plus SDK and a C compiler, or select a manually built plugin. ' + ' '.join(detail))
    return path


def request_input_build(*, retry=False):
    """Share one build between startup and the lazy inspector. Never install packages."""
    global _future
    with _lock:
        if (_future is None or (_future.done() and _future.exception() is None and not _future.result().is_file())
                or (retry and _future.done() and _future.exception() is not None)):
            future = _future = Future()
            def run():
                try:
                    future.set_result(build_default_input())
                except Exception as exc:
                    future.set_exception(exc)
            threading.Thread(target=run, daemon=True, name='GoemonInputBuild').start()
        return _future
