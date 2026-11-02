"""Windows GUI entry point for the PyInstaller-packaged Goemon practice toolkit."""
from __future__ import annotations
import sys

from practice.toolkit import main

# Defaults are owned by practice.toolkit.parse_args for every entry point.
DEFAULT_PRACTICE_FLAGS = []  # Compatibility for callers importing this symbol.


if __name__ == "__main__":
    main(sys.argv[1:])
