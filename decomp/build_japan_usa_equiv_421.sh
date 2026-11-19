#!/usr/bin/env bash
# Exact native JP rev-0 original-address reconstruction: 39+290+4+11+36+4+37 = 421 matching C.
# Requires pinned upstream and private Japanese ROM/toolchain; no original assets are committed.
set -euo pipefail
if (( $# != 3 )); then
    echo 'Usage: build_japan_usa_equiv_421.sh <clean-pinned-mnsg> <dependencies> <runtime-additions>' >&2
    exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
bash "$repo/decomp/build_japan_usa_equiv_380.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m "decomp.$1" "${@:2}")
run japan_usa_equivalent_four_more stage --checkout "$checkout"
run japan_usa_equivalent_four_more build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run japan_usa_equivalent_four_more verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" --retail "$checkout/build/japan_0/mnsg.equiv384.retail.z64" --report "$checkout/build/japan_0/equiv384-proof.json"
run japan_usa_equivalent_thirtyseven_more stage --checkout "$checkout"
run japan_usa_equivalent_thirtyseven_more build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-4}"
run japan_usa_equivalent_thirtyseven_more verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" --retail "$checkout/build/japan_0/mnsg.equiv421.retail.z64" --report "$checkout/build/japan_0/equiv421-proof.json"
echo 'Japanese 421 C: exact expanded and retail ROM, original ELF identities and 80747 relocations PASS'
