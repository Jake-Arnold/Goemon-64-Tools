#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
for cc in gcc clang; do
  for src in "$root"/src/func_*.c; do
    case "$src" in
      *2BE0*) defs=(-DDISPATCHER);;
      *3C90*) defs=(-DSTATE);;
      *4408*) defs=(-DDONOR);;
      *3984*formal_byte*) defs=(-DPAIR -DTARGET=func_80002D84_3984 -DCALL_ID=10 -DFORMAL_BYTE);;
      *3984*formal_int*) defs=(-DPAIR -DTARGET=func_80002D84_3984 -DCALL_ID=10 -DFORMAL_INT);;
      *3984*) defs=(-DPAIR -DTARGET=func_80002D84_3984 -DCALL_ID=10);;
      *3A10*) defs=(-DPAIR -DTARGET=func_80002E10_3A10 -DCALL_ID=11);;
      *) exit 1;;
    esac
    "$cc" -std=c99 -O1 -g -fno-strict-aliasing -fsanitize=address,undefined -fno-omit-frame-pointer -fno-pie -no-pie -I"$root/host" -I"$root/src" "${defs[@]}" "$root/host/test.c" "$src" -o "$work/test"
    printf '%s %s ' "$cc" "$(basename "$src")"
    "$work/test"
  done
done
