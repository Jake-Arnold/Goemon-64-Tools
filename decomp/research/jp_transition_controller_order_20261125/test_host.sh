#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
for cc in gcc clang; do
  for src in "$root"/src/func_*.c; do
    case "$src" in
      *34D8*) defs=(-DROOM_PAIR -DROOM=0x24C -DIS34=1 -DBUTTON_MASK=0xD000 -DDEST=5 -DTARGET=func_800028D8_34D8);;
      *381C*) defs=(-DROOM_PAIR -DROOM=0x231 -DIS34=0 -DBUTTON_MASK=0x1000 -DDEST=11 -DTARGET=func_80002C1C_381C);;
      *2F0C*) defs=(-DCOUNT_F0C -DTARGET=func_8000230C_2F0C);;
      *2FF4*) defs=(-DCOUNT_FF4 -DTARGET=func_800023F4_2FF4);;
      *3658*) defs=(-DCOUNT_658 -DTARGET=func_80002A58_3658);;
      *) exit 1;;
    esac
    case "$src" in *formal_half*) defs+=(-DFORMAL_HALF);; *formal_word*|*formal_selector*|*word_formal*) defs+=(-DFORMAL_WORD);; esac
    "$cc" -std=c99 -O1 -g -fno-strict-aliasing -fsanitize=address,undefined -fno-omit-frame-pointer -fno-pie -no-pie -I"$root/host" -I"$root/src" "${defs[@]}" "$root/host/test.c" "$src" -o "$work/test"
    printf '%s %s ' "$cc" "$(basename "$src")"
    "$work/test"
  done
done
