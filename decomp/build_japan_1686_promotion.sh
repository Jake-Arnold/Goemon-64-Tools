#!/usr/bin/env bash
# Full original-ROM proof gate for Japan-0 432 + 1686 matching-C functions.
# The user supplies private ROM, IDO and MIPS build toolchain locally.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_1686_promotion.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
if [[ ! -x "$deps/bin/mips-linux-gnu-readelf" ]]; then
  if ! command -v readelf >/dev/null; then
    echo 'System ELF readelf required to inspect original MIPS relocations' >&2
    exit 1
  fi
  ln -s "$(command -v readelf)" "$deps/bin/mips-linux-gnu-readelf"
fi
export GOEMON_JOBS="${GOEMON_JOBS:-8}"
# The source branch is frozen at the expected JP432 prerequisite; all old stages
# are independently built and verified before new C can be staged.
bash "$repo/decomp/build_japan_usa_main_432.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.japan_1686_promotion "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "$GOEMON_JOBS"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime"
(cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m decomp.local_ci)
echo 'Japan-0 original 432 + 1686 C: full ROM, ELF/relocations/inventory, full local CI PASS'
