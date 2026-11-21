#!/usr/bin/env bash
# Fail-closed complete Japanese original-ROM 14-function IDO native replay from JP2289.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_retry29_promotion.sh <clean pinned mnsg> <deps> <runtime>' >&2
  exit 2
fi
checkout=$(realpath "$1"); deps=$(realpath "$2"); runtime=$(realpath "$3")
repo=$(cd "$(dirname "$0")/.." && pwd)
[[ "$(git -C "$checkout" rev-parse HEAD)" == '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee' ]] || {
  echo 'Wrong upstream mnsg revision' >&2; exit 1;
}
[[ ! -e "$checkout/build/japan_0/mnsg.z64" ]] || {
  echo 'Checkout must start unbuilt' >&2; exit 1;
}
export PATH="$deps/bin:$PATH" LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH python3 -m "decomp.$1" "${@:2}")
# Rebuild the complete prior canonical JP2289 chain, without reusing stale ELF inputs.
bash "$repo/decomp/build_japan_tiny7_promotion.sh" "$checkout" "$deps" "$runtime"
baseline=$(mktemp -d -t jp2289-before-retry29-XXXXXXXX)
trap 'rm -rf -- "$baseline"' EXIT
mkdir -p "$baseline/build/japan_0"
cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" "$baseline/build/japan_0/"
run japan_retry29_promotion stage --checkout "$checkout"
run japan_retry29_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_retry29_promotion verify --checkout "$checkout" --base "$baseline"
(cd "$checkout"; env PYTHONHOME="$runtime/python"   PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" LD_LIBRARY_PATH="$runtime/lib"   "$runtime/python/bin/python3.12" tools/rommy.py compress   --input build/japan_0/mnsg.z64 --output build/japan_0/mnsg.retry29.retail.z64   --manifest config/japan_0/rommy.yaml --pad --verify)
cmp -s "$checkout/build/japan_0/mnsg.retry29.retail.z64"   "$checkout/config/japan_0/baserom.z64" || { echo 'Japan retail ROM differs' >&2;exit 1; }
run local_ci
printf '%s\n' 'JP2303 complete original-ROM, retail, ELF, semantic relocations, inventory and full CI PASS'
