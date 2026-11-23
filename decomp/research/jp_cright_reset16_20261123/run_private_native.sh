#!/usr/bin/env bash
# Reconstruct a new *private* JP2371 combined build from authenticated JP2370.
# Does not modify existing JP2370 checkout, source repo or original ROM bytes.
set -euo pipefail
if [ "$#" -ne 5 ];then
  echo "Usage: $0 JP2370_ACCEPTED JP2371_NEW_SCRATCH DEPS_DIR RUNTIME_DIR DECOMP_REPO_SOURCE" >&2
  exit 2
fi
BASE="$(realpath "$1")"
CAND="$2"
DEPS="$(realpath "$3")"
RUNTIME="$(realpath "$4")"
SRC="$(realpath "$5")"
ROOT="$(cd "$(dirname "$0")" && pwd)"
if [ -e "$CAND" ];then echo "Refusing existing candidate directory" >&2;exit 2;fi
if [ "$BASE" = "$CAND" ];then echo "Baseline cannot equal candidate" >&2;exit 2;fi
if [ ! -f "$BASE/build/japan_0/mnsg.z64" ];then echo "Missing accepted JP2370 ELF+ROM" >&2;exit 2;fi
mkdir -p "$(dirname "$CAND")"
cp -a --reflink=auto "$BASE" "$CAND"
export PATH="$DEPS/bin:$PATH"
export LD_LIBRARY_PATH="$RUNTIME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="$SRC"
if ! printf '%s  %s\n' '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0' "$CAND/tools/ido-5.3/cc" | sha256sum --check --status;then
  echo "Original IDO 5.3 compiler hash mismatches" >&2;exit 2
fi
python3 "$ROOT/stage_and_verify.py" stage --checkout "$CAND"
(
  cd "$CAND"
  make VERSION=japan_0 -j1 build/japan_0/src/jpcright_resetmixed.c.o
)
python3 "$ROOT/stage_and_verify.py" repair --checkout "$CAND"
(
  cd "$CAND"
  mips-linux-gnu-ld -T .splat/japan_0/mnsg.ld -Map build/japan_0/mnsg.map \
    -T .splat/japan_0/undefined_syms_auto.ld \
    -T .splat/japan_0/undefined_funcs_auto.ld \
    --no-check-sections --emit-relocs -o build/japan_0/mnsg.elf
  mips-linux-gnu-objcopy -O binary --pad-to=0x2000000 --gap-fill=0x00 \
    build/japan_0/mnsg.elf build/japan_0/mnsg.z64
)
python3 "$ROOT/stage_and_verify.py" verify --baseline "$BASE" --candidate "$CAND" \
 --report "$CAND/build/japan_0/cright-reset16-combined-proof.json"
