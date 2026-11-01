"""Windows GUI entry point for the PyInstaller-packaged Goemon practice toolkit."""
from __future__ import annotations
import sys

from practice.toolkit import main

# Match the source Run.bat's experimental practice opt-ins. The high-risk game
# state editor still has its separate per-session unlock; direct warp is disabled.
DEFAULT_PRACTICE_FLAGS = [
    "--enable-teleport", "--enable-state-restore",
    "--enable-debug-menu", "--enable-hex-edit",
]


if __name__ == "__main__":
    main([*DEFAULT_PRACTICE_FLAGS, *sys.argv[1:]])
