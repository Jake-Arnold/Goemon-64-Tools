#!/usr/bin/env bash
# Authentic Japan-0 2,123 + 145 matching-C native full-ROM G2 replay.
# Requires a fresh pinned upstream checkout and user's private original ROM/tools.
# Never publishes original ASM/ROM/assets/ELF/tools. Does not touch main.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_short145_promotion.sh <fresh-pinned-mnsg> <dependencies> <runtime-additions>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
python=$(command -v python3)
export PATH="$deps/bin:$PATH"
export LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
if [[ "$(git -C "$checkout" rev-parse HEAD)" != 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]]; then
  echo 'Wrong original upstream commit' >&2; exit 1
fi
if [[ ! -e "$checkout/config/japan_0/baserom.z64" ]]; then
  echo 'Private Japanese normalized retail ROM is missing' >&2; exit 1
fi
if [[ -d "$checkout/asm/japan_0" || -d "$checkout/bin/japan_0" || -d "$checkout/build/japan_0" ]]; then
  echo 'Requires a fresh checkout; refusing to modify an existing decomp build' >&2; exit 1
fi
run() (cd "$repo"; env -u PYTHONHOME -u PYTHONPATH "$python" -m "decomp.$1" "${@:2}")
scratch=$(mktemp -d -t goemon-jp-short145-baselines-XXXXXXXX)
trap 'rm -rf -- "$scratch"' EXIT
mkdir -p "$scratch/jp2118/build/japan_0" "$scratch/jp2121/build/japan_0" "$scratch/jp2123/build/japan_0"
archive_baseline() {
  local name=$1
  cp "$checkout/build/japan_0/mnsg.elf" "$checkout/build/japan_0/mnsg.z64" \
    "$scratch/$name/build/japan_0/"
}

bash "$repo/decomp/build_japan_1686_promotion.sh" "$checkout" "$deps" "$runtime"
archive_baseline jp2118
run glitch_g2_promotion stage --checkout "$checkout" --region japan_0
run glitch_g2_promotion build --checkout "$checkout" --region japan_0 --deps "$deps" --runtime "$runtime"
run glitch_g2_promotion verify --checkout "$checkout" --region japan_0 --baseline "$scratch/jp2118"
archive_baseline jp2121
run vm_g2_promotion stage --checkout "$checkout"
run vm_g2_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run vm_g2_promotion verify --checkout "$checkout" --baseline "$scratch/jp2121"
archive_baseline jp2123
run japan_short145_promotion stage --checkout "$checkout"
run japan_short145_promotion build --checkout "$checkout" --deps "$deps" --runtime "$runtime"
run japan_short145_promotion verify --checkout "$checkout" --base "$scratch/jp2123"

# The complete 32 MiB expanded ROM already matches. Check 16 MiB retail too.
(cd "$checkout"; env PYTHONHOME="$runtime/python" PYTHONPATH="$deps/.venv/lib/python3.12/site-packages" \
  LD_LIBRARY_PATH="$runtime/lib" \
  "$runtime/python/bin/python3.12" "tools/rommy.py" compress \
    --input "$checkout/build/japan_0/mnsg.z64" \
    --output "$checkout/build/japan_0/mnsg.short145.retail.z64" \
    --manifest "config/japan_0/rommy.yaml" --pad --verify)
cmp -s "$checkout/build/japan_0/mnsg.short145.retail.z64" "$checkout/config/japan_0/baserom.z64" \
  || { echo 'FAILED_ROM: retail Japanese ROM differs' >&2; exit 1; }
run local_ci

echo 'JP 2,268 C: original expanded + retail ROM, 7376 ELF identities, 80747 relocations, inventory, full CI PASS'
