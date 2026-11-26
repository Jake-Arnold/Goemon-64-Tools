#!/usr/bin/env bash
# Native macOS research interface. The native core runs in a child process.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ -x .venv/bin/python ]]; then
    exec .venv/bin/python -m practice.mupen_native_ui "$@"
fi
exec python3 -m practice.mupen_native_ui "$@"
