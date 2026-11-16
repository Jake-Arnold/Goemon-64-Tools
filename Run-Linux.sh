#!/usr/bin/env bash
# Unified Goemon Practice Toolkit launcher. Choose USA/Japan in the Dashboard.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ -x .venv/bin/python ]]; then
    exec .venv/bin/python -m practice.toolkit "$@"
fi
exec python3 -m practice.toolkit "$@"
