#!/usr/bin/env bash
# Native original-ROM Japan donor-template wave (baseline 2278 + 4 C).
set -euo pipefail
if (( $# != 3 )); then echo 'Usage: build_japan_donor4_promotion.sh <fresh-pinned-mnsg> <deps> <runtime>' >&2;exit 2;fi
checkout=$(realpath "$1");deps=$(realpath "$2");runtime=$(realpath "$3")
repo=$(cd "$(dirname "$0")/.." && pwd)
[[ "$(git -C "$checkout" rev-parse HEAD)" == 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]] || { echo 'Wrong original mnsg pin' >&2;exit 1; }
[[ ! -e "$checkout/build/japan_0/mnsg.z64" ]] || { echo 'Checkout not fresh' >&2;exit 1; }
export PATH="$deps/bin:$PATH" LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH python3 -m "decomp.$1" "${@:2}")
bash "$repo/decomp/build_japan_donor10_promotion.sh" "$checkout" "$deps" "$runtime"
base=$(mktemp -d -t jp2278-baseline-XXXXXXXX);trap 'rm -rf -- "$base"' EXIT
mkdir -p "$base/build/japan_0"
cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" "$base/build/japan_0/"
run japan_donor4_promotion stage --checkout "$checkout"
run japan_donor4_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_donor4_promotion verify --checkout "$checkout" --base "$base"
(cd "$checkout";env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" \
 LD_LIBRARY_PATH="$runtime/lib" "$runtime/python/bin/python3.12" tools/rommy.py compress \
 --input build/japan_0/mnsg.z64 --output build/japan_0/mnsg.donor4.retail.z64 \
 --manifest config/japan_0/rommy.yaml --pad --verify)
cmp -s "$checkout/build/japan_0/mnsg.donor4.retail.z64" "$checkout/config/japan_0/baserom.z64" || { echo 'Retail ROM mismatch' >&2;exit 1; }
run local_ci
echo 'JP2282 full expanded/retail ROM, ELF7376, relocations80747 and full CI PASS'
