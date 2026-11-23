#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 1 ]];then echo 'Usage: run_host.sh EMPTY_OUTPUT_DIR' >&2;exit 2;fi
OUT=$1
[[ ! -e "$OUT" ]] || { echo 'Output must not exist' >&2;exit 2; }
mkdir -p "$OUT"
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
for CC in gcc clang; do
  command -v "$CC" >/dev/null
  "$CC" -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer \
    "$HERE/host_timers.c" \
    "$ROOT/sources/func_80206078_630AF8.c" \
    "$ROOT/sources/func_801F72A8_621D28.c" \
    "$ROOT/sources/func_801F72D8_621D58.c" \
    -o "$OUT/jp28-$CC"
  "$OUT/jp28-$CC"
done
