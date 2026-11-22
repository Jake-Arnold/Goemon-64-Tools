#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$(mktemp -d)}"
mkdir -p "$OUT"
for CC in gcc clang; do
  "$CC" -std=gnu11 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all -I"$ROOT/tests/host" -Wall -Wextra -Werror \
    "$ROOT/tests/test_float5.c" "$ROOT"/source/*.c -o "$OUT/float5-$CC"
  ASAN_OPTIONS=detect_leaks=1 "$OUT/float5-$CC"
done
