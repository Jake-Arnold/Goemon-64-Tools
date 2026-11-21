#!/usr/bin/env bash
# Rebuild previous JP2268, then original-region donor-template 10-function G2.
set -euo pipefail
if (( $# != 3 )); then
 echo 'Usage: build_japan_donor10_promotion.sh <fresh-pinned-mnsg> <dependencies> <runtime>' >&2;exit 2
fi
checkout=$(realpath -- "$1");deps=$(realpath -- "$2");runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
export PATH="$deps/bin:$PATH"
export LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
[[ "$(git -C "$checkout" rev-parse HEAD)" == 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]] || { echo 'Wrong pinned source' >&2;exit 1; }
[[ ! -e "$checkout/build/japan_0/mnsg.z64" ]] || { echo 'Checkout not fresh' >&2;exit 1; }
python=$(command -v python3)
run() (cd "$repo";env -u PYTHONHOME -u PYTHONPATH "$python" -m "decomp.$1" "${@:2}")
bash "$repo/decomp/build_japan_short145_promotion.sh" "$checkout" "$deps" "$runtime"
baseline=$(mktemp -d -t goemon-jp2268-baseline-XXXXXXXX)
trap 'rm -rf -- "$baseline"' EXIT
mkdir -p "$baseline/build/japan_0"
cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" "$baseline/build/japan_0/"
run japan_donor10_promotion stage --checkout "$checkout"
run japan_donor10_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_donor10_promotion verify --checkout "$checkout" --base "$baseline"
(cd "$checkout";env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" \
 LD_LIBRARY_PATH="$runtime/lib" "$runtime/python/bin/python3.12" tools/rommy.py compress \
 --input build/japan_0/mnsg.z64 --output build/japan_0/mnsg.donor10.retail.z64 \
 --manifest config/japan_0/rommy.yaml --pad --verify)
cmp -s "$checkout/build/japan_0/mnsg.donor10.retail.z64" "$checkout/config/japan_0/baserom.z64" || { echo 'Retail ROM mismatch' >&2;exit 1; }
run local_ci
echo 'JP2278: expanded/retail ROM, ELF7376, semantic relocations80747, inventory and full CI PASS'
