#!/usr/bin/env bash
# Bundle missing host runtime pieces for an offline Japanese Goemon build.
# This is for a private chat upload. Never commit the resulting tarball.
set -euo pipefail

if [[ $# -gt 2 ]]; then
  echo "Usage: $0 [path/to/mnsg-japan/.venv] [destination.tar.gz]" >&2
  exit 2
fi
venv="$HOME/Desktop/mnsg-japan/.venv"
output="$HOME/Desktop/goemon-runtime-additions.tar.gz"
if [[ $# -ge 1 ]]; then venv="$1"; fi
if [[ $# -ge 2 ]]; then output="$2"; fi

if [[ ! -e "$venv/bin/python" ]]; then
  echo "Python venv is absent or has a broken interpreter link: $venv" >&2
  exit 1
fi
if [[ -e "$output" || -L "$output" ]]; then
  echo "Output already exists, refusing overwrite: $output" >&2
  exit 1
fi

py=$(readlink -f -- "$venv/bin/python")
if [[ "$("$py" --version 2>&1)" != Python\ 3.12.* ]]; then
  echo "Expected installed CPython 3.12, not another Python version." >&2
  exit 1
fi
prefix=$(dirname -- "$(dirname -- "$py")")
if [[ ! -f "$prefix/lib/python3.12/os.py" || ! -d "$prefix/bin" ]]; then
  echo "Unsupported Python base environment: $prefix" >&2
  exit 1
fi
if [[ "$prefix" == /usr || "$prefix" == /usr/local || "$prefix" == / ]]; then
  echo "Refusing to archive the system Python root; use uv-managed Python." >&2
  exit 1
fi

scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
bundle="$scratch/goemon-runtime-additions"
mkdir -p "$bundle/lib" "$bundle/python"

for name in \
  libopcodes-2.45.90-mips.20260125.so \
  libbfd-2.45.90-mips.20260125.so \
  libctf-mips.so.0 \
  libsframe.so.3
do
  path=$(ldconfig -p 2>/dev/null | awk -v lib="$name" '$1 == lib {print $NF; exit}')
  if [[ -z "$path" ]]; then
    path=$(find /usr/lib/x86_64-linux-gnu /lib/x86_64-linux-gnu /usr/lib /lib \
      -name "$name" -print -quit 2>/dev/null || true)
  fi
  if [[ -z "$path" || ! -r "$path" ]]; then
    echo "Cannot find missing binutils shared library: $name" >&2
    exit 1
  fi
  cp -L -- "$path" "$bundle/lib/$name"
done

# Package the complete uv-installed CPython 3.12 base interpreter/stdlib.
# The existing .venv site-packages were supplied in the first archive.
cp -a -- "$prefix/bin" "$bundle/python/bin"
cp -a -- "$prefix/lib" "$bundle/python/lib"
{
  printf 'Python runtime version: '
  "$py" --version
  printf 'Binutils version: '
  mips-linux-gnu-as --version | head -1
  printf 'Shared library checksums:\n'
  (cd "$bundle" && sha256sum lib/*)
} > "$bundle/manifest.txt"

mkdir -p -- "$(dirname -- "$output")"
tar -czf "$output" -C "$scratch" goemon-runtime-additions
echo "Created $output"
ls -lh -- "$output"
