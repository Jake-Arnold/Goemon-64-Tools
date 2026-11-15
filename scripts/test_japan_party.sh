#!/usr/bin/env bash
# Run Japan-0 party unlock tests from the repository root.
# Read/write tests use synthetic guest RAM. They do not touch the live emulator.
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"

# Fail immediately with a clear syntax report for any practice module,
# including GUI files that might otherwise be imported late in test discovery.
"${PYTHON}" -m compileall -q practice

"${PYTHON}" -m unittest \
  tests.test_japanese_fields \
  tests.test_japanese_scene_probes \
  tests.test_japanese_party_unlock \
  tests.test_japan_party_cli \
  tests.test_japan_party_controller \
  tests.test_japan_state_comparison \
  tests.test_value_search \
  tests.test_state_discovery \
  -v

if command -v xvfb-run >/dev/null 2>&1; then
  xvfb-run -a "${PYTHON}" -m unittest \
    tests.test_japanese_fields_ui \
    tests.test_japanese_scene_probe_ui \
    tests.test_japanese_party_controls_ui \
    tests.test_japan_readonly_parity \
    tests.test_japan_state_comparison_ui \
    tests.test_value_search_ui \
    tests.test_state_discovery_ui \
    -v
elif [[ -n "${DISPLAY:-}" ]]; then
  "${PYTHON}" -m unittest \
    tests.test_japanese_fields_ui \
    tests.test_japanese_scene_probe_ui \
    tests.test_japanese_party_controls_ui \
    tests.test_japan_readonly_parity \
    tests.test_japan_state_comparison_ui \
    tests.test_value_search_ui \
    tests.test_state_discovery_ui \
    -v
else
  echo 'ERROR: Tk smoke tests need xvfb-run (sudo apt install xvfb xauth)' >&2
  exit 2
fi
