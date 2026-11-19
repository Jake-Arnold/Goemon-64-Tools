#!/usr/bin/env bash
# Build Japanese rev-0 ROM with the exact first C and three additional bit helpers.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_four_c.sh <pinned-mnsg-checkout> <dependencies-dir> <runtime-additions-dir>' >&2
  exit 2
fi
source_root=$(realpath -- "$1")
deps=$(realpath -- "$2")
additions=$(realpath -- "$3")
repo_root=$(cd -- "$(dirname -- "$0")/.." && pwd)
py312="$additions/python/bin/python3.12"
if [[ "$(git -C "$source_root" rev-parse HEAD)" != 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]]; then
  echo 'Unexpected pinned mnsg source commit' >&2
  exit 1
fi
if [[ ! -x "$py312" || ! -d "$deps/.venv/lib/python3.12/site-packages" ]]; then
  echo 'Offline Python 3.12 runtime or site packages not available' >&2
  exit 1
fi
export PYTHONHOME="$additions/python"
export PYTHONPATH="$deps/.venv/lib/python3.12/site-packages"
export LD_LIBRARY_PATH="$additions/lib"
export PATH="$deps/bin:$PATH"
"$py312" -c 'import yaml, splat, lzkn64, spimdisasm'
mips-linux-gnu-ld --version >/dev/null
cd "$source_root"
rom=config/japan_0/baserom.z64
if [[ ! -f "$rom" || "$(sha1sum "$rom" | cut -d' ' -f1)" != 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b ]]; then
  echo 'Japanese rev-0 canonical retail ROM missing or mismatched' >&2
  exit 1
fi
expanded=config/japan_0/baserom.decompressed.z64
if [[ ! -f "$expanded" || ! -f config/japan_0/rommy.yaml ]]; then
  "$py312" tools/rommy.py decompress --input "$rom" \
    --output "$expanded" --manifest config/japan_0/rommy.yaml --pad
fi
if [[ "$(sha1sum "$expanded" | cut -d' ' -f1)" != 6f8745fecc3a5e7d4918c7a73353eb0726116ded ]]; then
  echo 'Expanded Japanese ROM SHA-1 mismatch' >&2
  exit 1
fi
host_python=$(command -v python3)
run_module() (
  cd "$repo_root"
  env -u PYTHONHOME -u PYTHONPATH "$host_python" -m "$@"
)
run_module decomp.japan_four_c stage-config "$source_root"
"$py312" "$deps/.venv/bin/splat" split config/japan_0/splat_four_c.local.yaml
run_module decomp.japan_first_c install-source "$source_root"
run_module decomp.japan_four_c install-source "$source_root"
run_module decomp.japan_asm_baseline patch-asm "$source_root"
rm -f -- build/japan_0/mnsg.elf build/japan_0/mnsg.z64
make build/japan_0/mnsg.z64 VERSION=japan_0 \
  'C_FILES=src/jp_main_38620.c src/jp_bit_array.c' PYTHON="$py312" \
  -j"$(printenv GOEMON_JOBS || echo 6)"
retail=build/japan_0/mnsg.four-c.retail.z64
rm -f -- "$retail"
"$py312" tools/rommy.py compress --input build/japan_0/mnsg.z64 \
  --output "$retail" --manifest config/japan_0/rommy.yaml --pad --verify
run_module decomp.japan_four_c verify "$source_root" \
  --retail-output "$source_root/$retail" \
  --report "$source_root/build/japan_0/four-c-proof.json"
