#!/bin/sh
set -eu
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
for r in usa japan_0; do
 flag=; [ "$r" = usa ] || flag=-DJP
 gcc -std=c11 -O1 -g -fno-pie -no-pie -Wno-pointer-to-int-cast -fsanitize=address,undefined $flag test_host.c -Wl,--defsym,D_3AE29=0x3ae29 -Wl,--defsym,D_CF894=0xcf894 -o "$work/$r"
 "$work/$r"
done
