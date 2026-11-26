#!/usr/bin/env bash
# Compile only our input bridge against an installed or user-selected SDK.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
if_needed=0
if [[ "${1:-}" == --if-needed ]]; then if_needed=1; shift; fi
sdk="${1:-${MUPEN_SDK:-}}"
case "$(uname -s)" in
    Darwin) flags=(-dynamiclib); libs=(); suffix=dylib ;;
    Linux) flags=(-shared -fPIC); libs=(-ldl); suffix=so ;;
    *) echo 'Build on macOS or Linux with a C11 compiler.' >&2; exit 2 ;;
esac
output="build/goemon_mupen_input.$suffix"
stamp="$output.stamp"
# Changes to the bridge or build recipe trigger an automatic rebuild after a Git update.
fingerprint="$(uname -sm)\n$(cksum native/goemon_mupen_input.c scripts/build_mupen_input.sh)"
if [[ "$if_needed" == 1 && -s "$output" && -f "$stamp" && "$(cat "$stamp")" == "$fingerprint" ]]; then
    echo "Current $output"
    exit 0
fi
if [[ -z "$sdk" ]] && command -v brew >/dev/null 2>&1; then
    prefix="$(brew --prefix mupen64plus 2>/dev/null || true)"
    if [[ -n "$prefix" ]]; then
        header="$(find "$prefix/include" -name m64p_plugin.h -type f -print -quit 2>/dev/null || true)"
        [[ -z "$header" ]] || sdk="$(dirname -- "$header")"
    fi
fi
if [[ -z "$sdk" ]]; then
    for candidate in /usr/include/mupen64plus /usr/local/include/mupen64plus .mupen-sdk/src/api; do
        if [[ -f "$candidate/m64p_plugin.h" ]]; then sdk="$candidate"; break; fi
    done
fi
if [[ ! -f "$sdk/m64p_plugin.h" ]]; then
    echo 'Usage: bash scripts/build_mupen_input.sh [--if-needed] /directory/containing/m64p_plugin.h' >&2
    echo 'Use the matching upstream Mupen64Plus SDK, not the synthetic test fixture.' >&2
    exit 2
fi
mkdir -p build
# A compiler failure must not truncate an already installed working plugin.
tmp="$(mktemp "build/goemon_mupen_input.$suffix.tmp.XXXXXX")"
tmp_stamp="${tmp}.stamp"
trap 'rm -f -- "$tmp" "$tmp_stamp"' EXIT
"${CC:-cc}" -std=c11 -O2 -Wall -Wextra -Werror "${flags[@]}" -I "$sdk" native/goemon_mupen_input.c -o "$tmp" ${libs[@]+"${libs[@]}"}
printf '%s\n' "$fingerprint" > "$tmp_stamp"
mv -f -- "$tmp" "$output"
mv -f -- "$tmp_stamp" "$stamp"
echo "Built $output"
