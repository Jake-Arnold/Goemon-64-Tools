#!/usr/bin/env bash
# Native-exact JP rev-0 build: 39+290+4+11+36 original-address C functions.
# Requires a clean pinned mnsg checkout, private ROM and original IDO toolchain.
# Generated ASM, ROMs, ELF objects and native compiler stay outside Git.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_usa_equiv_380.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_equiv_344.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_usa_equivalent_36 "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.equiv380.retail.z64" \
  --report "$checkout/build/japan_0/equiv380-proof.json"
echo 'Japanese 380-C: exact 32 MiB + exact retail 16 MiB, ELF identities and relocations PASS'
