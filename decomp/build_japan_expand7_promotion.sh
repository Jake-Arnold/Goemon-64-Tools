#!/usr/bin/env bash
# Full original-ROM Japanese JP2314 replay, requires fresh pinned upstream and private user ROM.
set -euo pipefail
if (( $# != 3 )); then echo 'Usage: build_japan_expand7_promotion.sh <fresh pinned mnsg> <deps> <runtime>' >&2;exit 2;fi
checkout=$(realpath "$1");deps=$(realpath "$2");runtime=$(realpath "$3")
repo=$(cd "$(dirname "$0")/.." && pwd)
[[ "$(git -C "$checkout" rev-parse HEAD)" == 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]] || { echo 'Wrong pinned original upstream' >&2;exit 1; }
[[ ! -e "$checkout/build/japan_0/mnsg.z64" ]] || { echo 'Checkout must begin unbuilt' >&2;exit 1; }
export PATH="$deps/bin:$PATH" LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH python3 -m "decomp.$1" "${@:2}")
bash "$repo/decomp/build_japan_retry10_promotion.sh" "$checkout" "$deps" "$runtime"
before=$(mktemp -d -t goemon-JP2307-before-expand7-XXXXXXXX)
trap 'rm -rf -- "$before"' EXIT
mkdir -p "$before/build/japan_0"
cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" "$before/build/japan_0/"
run japan_expand7_promotion stage --checkout "$checkout"
run japan_expand7_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_expand7_promotion verify --checkout "$checkout" --base "$before"
(cd "$checkout"; env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" LD_LIBRARY_PATH="$runtime/lib" "$runtime/python/bin/python3.12" tools/rommy.py compress --input build/japan_0/mnsg.z64 --output build/japan_0/mnsg.expand7.retail.z64 --manifest config/japan_0/rommy.yaml --pad --verify > /dev/null)
cmp "$checkout/build/japan_0/mnsg.expand7.retail.z64" "$checkout/config/japan_0/baserom.z64" || { echo 'Retail ROM mismatch' >&2;exit 1; }
run local_ci
printf '%s\n' 'JP2314 native full-ROM/ELF/relocations/inventory/retail and full local CI PASS'
