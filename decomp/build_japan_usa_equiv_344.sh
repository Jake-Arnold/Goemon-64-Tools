#!/usr/bin/env bash
# Rebuild original Japanese rev-0 with 39+290+4+11 matching-C functions.
# ROMs, extracted assembly and native build products stay in the private checkout.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_usa_equiv_344.sh <fresh pinned mnsg> <dependencies> <runtime>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
host_python=$(command -v python3)
bash "$repo/decomp/build_japan_switch_333.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_usa_equivalent_eleven "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-8}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.equiv344.retail.z64" \
  --report "$checkout/build/japan_0/equiv344-proof.json"
echo 'Japanese 344-C exact expanded + retail ROM, original ELF identities and relocations: PASS'
