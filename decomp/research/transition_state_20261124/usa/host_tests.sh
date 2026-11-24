#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
for cc in gcc clang; do
  command -v "$cc" >/dev/null || continue
  "$cc" -std=c99 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie -Ihost -I. 454c.c 3cf0_selector.c host/test_transition.c -o "$work/test-$cc"
  "$work/test-$cc"
done
