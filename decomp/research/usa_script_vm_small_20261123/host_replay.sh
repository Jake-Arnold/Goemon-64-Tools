#!/bin/bash
set -euo pipefail
REPO=$(realpath "$1"); KIT=$(cd "$(dirname "$0")" && pwd); TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
cd "$REPO"
flags=(-no-pie -g -O1 -fsanitize=address,undefined -fno-sanitize-recover=all)
gcc "${flags[@]}" -DGOEMON_VM_RESOURCE_SOURCE=\"$KIT/sources/F038_reorder.c\" decomp/test_vm_resource_halfword_probe.c -o "$TMP/f038"
"$TMP/f038"
sed 's|#include "candidates/vm_digits_format_probe.c"|#include "F480_direct_call.c"|' decomp/test_vm_digits_format_probe.c > "$TMP/f480_harness.c"
gcc "${flags[@]}" -I"$KIT/sources" "$TMP/f480_harness.c" -o "$TMP/f480"
"$TMP/f480"
gcc "${flags[@]}" -DGOEMON_VM_WALKER_SOURCE=\"$KIT/sources/DE80_natural.c\" decomp/test_vm_command_walker_probe.c -o "$TMP/de80"
"$TMP/de80"
