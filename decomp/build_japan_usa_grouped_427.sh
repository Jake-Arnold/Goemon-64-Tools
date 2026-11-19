#!/usr/bin/env bash
# Original-address Japanese 427-C exact-ROM rebuild from fresh pinned upstream.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_usa_grouped_427.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_equiv_423.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_usa_grouped_four "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.equiv427.retail.z64" \
  --report "$checkout/build/japan_0/grouped427-proof.json"
echo 'Japan 427 matching C: expanded/retail original ROM, 7376 FUNC identities and 80747 relocations PASS'
