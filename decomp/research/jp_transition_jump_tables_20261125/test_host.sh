#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
T=$(mktemp -d);trap 'rm -rf "$T"' EXIT
for cc in gcc clang; do
 for variant in baseline negative; do
  "$cc" -std=c99 -O2 -g -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie -Ihost -Isrc "src/func_80002EF4_3AF4_$variant.c" host/test.c -o "$T/test"
  printf '%s %s: ' "$cc" "$variant"; "$T/test"
 done
done
