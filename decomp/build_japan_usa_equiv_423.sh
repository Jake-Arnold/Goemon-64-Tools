#!/usr/bin/env bash
# Japanese original-address 423-C exact ROM rebuild; all original ROM/toolchain inputs are private.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_usa_equiv_423.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_equiv_421.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_usa_equivalent_two_remaining "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.equiv423.retail.z64" \
  --report "$checkout/build/japan_0/equiv423-proof.json"
echo 'Japanese 423 C: original expanded 32MiB + retail 16MiB, 7376 ELF identities, 80747 relocations PASS'
