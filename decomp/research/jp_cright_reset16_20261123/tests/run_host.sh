#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for cc in gcc clang; do
  if command -v "$cc" >/dev/null 2>&1;then
    "$cc" -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -Wall -Wextra -Werror host_reset16.c -o "/tmp/goemon-reset16-${cc}-$$"
    "/tmp/goemon-reset16-${cc}-$$"
    rm -f "/tmp/goemon-reset16-${cc}-$$"
  fi
done
