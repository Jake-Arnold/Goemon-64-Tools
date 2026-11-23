#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
out=${1:-/tmp/goemon-cright-tail60-host}
mkdir -p "$out"
for cc in gcc clang; do
    command -v "$cc" >/dev/null || continue
    "$cc" -g -O1 -std=gnu11 -fsanitize=address,undefined -fno-omit-frame-pointer -Wno-unused-parameter \
        "$root/source/func_80212C50_5CE1E0.c" "$root/tests/host_test.c" -o "$out/host-$cc"
    ASAN_OPTIONS=detect_leaks=0 "$out/host-$cc"
    echo "PASS $cc ASan+UBSan: 64 stage handoff cases"
done
