#!/usr/bin/env bash
# Exact Japanese original-address 24-C build with private, pinned ROM/toolchain.
# Run from any directory: bash decomp/build_japan_twentyfour_c.sh checkout deps runtime
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_eighteen_c.sh <pinned-mnsg-checkout> <dependencies-dir> <runtime-additions-dir>' >&2
  exit 2
fi
checkout=$(realpath -- "$1")
deps=$(realpath -- "$2")
runtime=$(realpath -- "$3")
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
host_python=$(command -v python3)
py="$runtime/python/bin/python3.12"
if [[ "$(git -C "$checkout" rev-parse HEAD)" != 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]]; then
  echo 'Wrong pinned original game source revision' >&2; exit 1
fi
if [[ ! -x "$py" || ! -d "$deps/.venv/lib/python3.12/site-packages" ]]; then
  echo 'Offline Python 3.12 runtime and packages are required' >&2; exit 1
fi
export PYTHONHOME="$runtime/python"
export PYTHONPATH="$deps/.venv/lib/python3.12/site-packages"
export LD_LIBRARY_PATH="$runtime/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="$deps/bin:$PATH"
"$py" -c 'import yaml,splat,lzkn64,spimdisasm'
mips-linux-gnu-ld --version >/dev/null
run_module() (
  cd "$repo"
  env -u PYTHONHOME -u PYTHONPATH "$host_python" -m "$@"
)
cd "$checkout"
if [[ ! -e config/japan_0/baserom.z64 || "$(sha1sum config/japan_0/baserom.z64 | cut -d' ' -f1)" != 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b ]]; then
  echo 'Wrong or missing original Japanese rev-0 retail ROM' >&2; exit 1
fi
if [[ -d asm/japan_0 || -d bin/japan_0 || -d build/japan_0 ]]; then
  echo 'Requires a fresh pinned mnsg checkout; will not overwrite existing generated build data' >&2; exit 1
fi
if [[ ! -f config/japan_0/baserom.decompressed.z64 || ! -f config/japan_0/rommy.yaml ]]; then
  "$py" tools/rommy.py decompress --input config/japan_0/baserom.z64 \
    --output config/japan_0/baserom.decompressed.z64 \
    --manifest config/japan_0/rommy.yaml --pad >/dev/null
fi
if [[ "$(sha1sum config/japan_0/baserom.decompressed.z64 | cut -d' ' -f1)" != 6f8745fecc3a5e7d4918c7a73353eb0726116ded ]]; then
  echo 'Expanded Japanese ROM does not match pinned original' >&2; exit 1
fi
run_module decomp.japan_eighteen_c stage "$checkout"
"$py" "$deps/.venv/bin/splat" split config/japan_0/splat_twentyfour_c.local.yaml >/dev/null
run_module decomp.japan_eighteen_c install "$checkout"
run_module decomp.japan_asm_baseline patch-asm "$checkout"
C_FILES='src/jp_bit_array.c src/jp_camera_13B70.c src/jp_main_38620.c src/jp_mode_flags.c src/jp_motion_12D60.c src/jp_state_37D1C.c src/jp_transition_37870.c src/jp_warp_37920.c src/jp_warp_37B58.c src/jp_warp_37C4C.c src/jp_warp_37C84.c src/jp_warp_37CB8.c src/jp_warp_37CE0.c src/jp_warp_call_37900.c src/jp_coord_37958.c src/jp_coord_37A24.c src/jp_state_37AF4.c src/jp_warp_37B8C.c src/jp_state_37D5C.c src/jp_compare_37EEC.c'
objects=()
for file in $C_FILES; do objects+=("build/japan_0/$file.o"); done
objects+=(build/japan_0/asm/japan_0/main_37DB8.s.o build/japan_0/asm/japan_0/main_37F20.s.o)
make -j"${GOEMON_JOBS:-8}" VERSION=japan_0 "C_FILES=$C_FILES" "${objects[@]}" >/dev/null
run_module decomp.japan_eighteen_c layout "$checkout" --report "$checkout/build/japan_0/twentyfour-layout-proof.json" --objdump "$deps/bin/mips-linux-gnu-objdump"
make -j"${GOEMON_JOBS:-8}" VERSION=japan_0 "C_FILES=$C_FILES" build/japan_0/mnsg.z64 >/dev/null
if ! cmp -s build/japan_0/mnsg.z64 config/japan_0/baserom.decompressed.z64; then
  echo 'Japanese expanded ROM differs from original' >&2; exit 1
fi
out=build/japan_0/mnsg.twentyfour-c.retail.z64
"$py" tools/rommy.py compress --input build/japan_0/mnsg.z64 \
  --output "$out" --manifest config/japan_0/rommy.yaml --pad --verify >/dev/null
if ! cmp -s "$out" config/japan_0/baserom.z64; then
  echo 'Japanese retail ROM differs from original' >&2; exit 1
fi
run_module decomp.japan_twentyfour_verify --checkout "$checkout" \
  --retail-output "$checkout/$out" --source-dir "$repo/decomp" \
  --objcopy "$deps/bin/mips-linux-gnu-objcopy" --objdump "$deps/bin/mips-linux-gnu-objdump" \
  --report "$checkout/build/japan_0/twentyfour-proof.json"
echo 'Japanese 24-C: exact source-linked 32 MiB + retail 16 MiB; strict source/ELF/verifier PASS'
