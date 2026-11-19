#!/usr/bin/env bash
# Reproduce 39+290+4 Japanese original-address matching C from a fresh pinned checkout.
# Never commit private ROMs, extracted assembly, .o, ELF, linker scripts or images.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_switch_333.sh <fresh pinned mnsg> <dependencies> <runtime>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
host_python=$(command -v python3)
bash "$repo/decomp/build_japan_noop_port_329.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_character_switch_four "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-8}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.switch333.retail.z64" \
  --report "$checkout/build/japan_0/switch333-proof.json"
echo 'Japanese 333-C exact expanded+retail ROM, all ELF functions and semantic relocations: PASS'
