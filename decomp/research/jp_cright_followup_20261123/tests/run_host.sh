#!/bin/sh
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d);trap 'rm -rf "$tmp"' EXIT
for cc in gcc clang; do
 "$cc" -std=gnu99 -O1 -g -fno-pie -no-pie -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer host_actual.c ../sources/func_80004170_4D70.c ../sources/func_800041AC_4DAC.c ../sources/func_80013654_14254.c -o "$tmp/host-$cc"
 ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 "$tmp/host-$cc"
done
