#!/usr/bin/env bash
# Japanese 429 matching C; original pinned IDO, exact native build and retail ROM.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_usa_main_429.sh <clean pinned upstream mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_grouped_427.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_usa_main_two "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.equiv429.retail.z64" \
  --report "$checkout/build/japan_0/main429-proof.json"
echo 'Japan 429 C: original expanded + retail ROM; 7376 ELF functions; 80747 relocations PASS'
