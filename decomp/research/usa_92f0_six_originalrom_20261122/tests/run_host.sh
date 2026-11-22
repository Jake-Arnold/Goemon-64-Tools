#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$(mktemp -d)}"
mkdir -p "$OUT"
for CC in gcc clang; do
  "$CC" -std=gnu11 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all -I"$ROOT/tests/host" -Wall -Wextra -Werror -Wno-pointer-to-int-cast \
    "$ROOT/tests/test_sources.c" "$ROOT/source/func_8000AAE8_B6E8.c" "$ROOT/source/func_8000AB30_B730.c" -o "$OUT/native-three-$CC"
  ASAN_OPTIONS=detect_leaks=1 "$OUT/native-three-$CC"
  "$CC" -std=gnu11 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all -I"$ROOT/tests/host" -Wall -Wextra -Werror "$ROOT/tests/test_a5c4.c" -o "$OUT/native-structure-$CC"
  ASAN_OPTIONS=detect_leaks=1 "$OUT/native-structure-$CC"
  "$CC" -std=gnu11 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all -fno-strict-aliasing -I"$ROOT/tests/host" -Wall -Wextra -Werror "$ROOT/tests/test_a548.c" "$ROOT/source/func_8000A5C4_B1C4.c" -o "$OUT/native-loop-$CC"
  ASAN_OPTIONS=detect_leaks=1 "$OUT/native-loop-$CC"
done
