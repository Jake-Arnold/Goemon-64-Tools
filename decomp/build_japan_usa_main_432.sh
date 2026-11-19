#!/usr/bin/env bash
# Original-ID0 Japanese 432-function matching-C rebuild, no game assets committed.
set -euo pipefail
if (( $# != 3 )); then
 echo 'Usage: build_japan_usa_main_432.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2; exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_main_429.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_usa_main_three "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" --retail "$checkout/build/japan_0/mnsg.equiv432.retail.z64" --report "$checkout/build/japan_0/main432-proof.json"
echo 'Japan 432 C: original expanded/retail ROM, ELF FUNC and semantic relocations PASS'
