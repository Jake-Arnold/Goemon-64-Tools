#!/usr/bin/env bash
# Full native Japan rev-0 JP55 fail-closed trial. Private ROM/toolchain remain external.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_jp55_promotion.sh <fresh pinned mnsg> <dependencies> <runtime>' >&2
  exit 2
fi
checkout=$(realpath "$1")
deps=$(realpath "$2")
runtime=$(realpath "$3")
repo=$(cd "$(dirname "$0")/.." && pwd)
[[ "$(git -C "$checkout" rev-parse HEAD)" == 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]] || {
  echo 'Wrong original pinned upstream commit' >&2; exit 1;
}
[[ ! -e "$checkout/build/japan_0/mnsg.z64" ]] || {
  echo 'Checkout must begin clean and unbuilt' >&2; exit 1;
}
export PATH="$deps/bin:$PATH" LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH python3 -m "decomp.$1" "${@:2}")

# Replay the entire previously published JP2314 baseline from the original ROM.
bash "$repo/decomp/build_japan_expand7_promotion.sh" "$checkout" "$deps" "$runtime"
base=$(mktemp -d -t goemon-JP2314-before-55-XXXXXXXX)
trap 'rm -rf -- "$base"' EXIT
mkdir -p "$base/build/japan_0"
cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" "$base/build/japan_0/"

run japan_jp55_promotion plan --checkout "$checkout"
run japan_jp55_promotion stage --checkout "$checkout"
run japan_jp55_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_jp55_promotion verify --checkout "$checkout" --base "$base"

# Native retail compression and byte-identical comparison of original private cartridge.
(
  cd "$checkout"
  env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" \
    LD_LIBRARY_PATH="$runtime/lib" "$runtime/python/bin/python3.12" tools/rommy.py compress \
    --input build/japan_0/mnsg.z64 \
    --output build/japan_0/mnsg.jp55.retail.z64 \
    --manifest config/japan_0/rommy.yaml --pad --verify >/dev/null
)
cmp "$checkout/build/japan_0/mnsg.jp55.retail.z64" "$checkout/config/japan_0/baserom.z64"
run local_ci
printf '%s\n' 'JP55 FULL ORIGINAL-ROM/ELF/RELOCATION/INVENTORY/RETAIL/LOCAL-CI GATES PASS'
