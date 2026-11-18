#!/usr/bin/env bash
# Exact original Japanese 329-C build; never stores/commits proprietary ROM bytes.
# Requires fresh pinned upstream mnsg checkout with a private JP retail ROM.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_noop_port_329.sh <fresh-pinned-upstream> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
host_python=$(command -v python3)
readelf=$(command -v readelf)
if [[ -z "$readelf" ]]; then echo 'Host readelf required' >&2; exit 1; fi
scratchbin=$(mktemp -d)
trap 'rm -rf "$scratchbin"' EXIT
ln -s "$readelf" "$scratchbin/mips-linux-gnu-readelf"
export PATH="$scratchbin:$PATH"
# The legacy 39-C builder authenticates pinned sources, both ROM images,
# all baseline C objects, original ELF functions and all semantic relocations.
bash "$repo/decomp/build_japan_thirtynine_c.sh" "$checkout" "$deps" "$runtime"
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_noop_port "$@")
run stage --checkout "$checkout"
run build --checkout "$checkout" --deps "$deps" --runtime "$runtime" --jobs "${GOEMON_JOBS:-8}"
run verify --checkout "$checkout" --deps "$deps" --runtime "$runtime" \
  --retail "$checkout/build/japan_0/mnsg.noop-port-329.retail.z64" \
  --readelf "$readelf" --report "$checkout/build/japan_0/noop-port-329-proof.json"
echo 'JAPAN 329-C exact 32 MiB + exact 16 MiB + 7376 ELF functions + 80747 relocations PASS'
