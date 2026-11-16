#!/usr/bin/env bash
# Rebuild Japanese Goemon 64 with the first exact original-IDO C translation unit.
set -euo pipefail
if (( $# != 3 )); then
  echo 'Usage: build_japan_first_c.sh <pinned-mnsg-checkout> <dependencies-dir> <runtime-additions-dir>' >&2
  exit 2
fi
source_root=$(realpath -- "$1")
deps=$(realpath -- "$2")
additions=$(realpath -- "$3")
script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
host_python=$(command -v python3)
py312="$additions/python/bin/python3.12"
if [[ "$(git -C "$source_root" rev-parse HEAD)" != 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee ]]; then
  echo 'Unexpected pinned mnsg source commit' >&2; exit 1
fi
export PYTHONHOME="$additions/python"
export PYTHONPATH="$deps/.venv/lib/python3.12/site-packages"
export LD_LIBRARY_PATH="$additions/lib"
export PATH="$deps/bin:$PATH"
"$py312" -c 'import yaml, splat, lzkn64, spimdisasm'
cd "$source_root"
if [[ "$(sha1sum config/japan_0/baserom.z64 | cut -d' ' -f1)" != 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b ]]; then
  echo 'Missing or incorrect Japanese rev-0 canonical retail ROM' >&2; exit 1
fi
if [[ ! -e config/japan_0/baserom.decompressed.z64 || ! -e config/japan_0/rommy.yaml ]]; then
  "$py312" tools/rommy.py decompress --input config/japan_0/baserom.z64 \
    --output config/japan_0/baserom.decompressed.z64 --manifest config/japan_0/rommy.yaml --pad
fi
if [[ "$(sha1sum config/japan_0/baserom.decompressed.z64 | cut -d' ' -f1)" != 6f8745fecc3a5e7d4918c7a73353eb0726116ded ]]; then
  echo 'Japanese expanded reference hash mismatch' >&2; exit 1
fi
(cd "$script_dir/.." && env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_first_c stage-config "$source_root")
"$py312" -m splat split config/japan_0/splat_one_c.local.yaml
(cd "$script_dir/.." && env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_first_c install-source "$source_root")
(cd "$script_dir/.." && env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_asm_baseline patch-asm "$source_root")
make build/japan_0/mnsg.z64 VERSION=japan_0 C_FILES=src/jp_main_38620.c PYTHON="$py312" -j"$(printenv GOEMON_JOBS || echo 6)"
retail=build/japan_0/mnsg.first-c.retail.z64
rm -f -- "$retail"
"$py312" tools/rommy.py compress --input build/japan_0/mnsg.z64 --output "$retail" --manifest config/japan_0/rommy.yaml --pad --verify
(cd "$script_dir/.." && env -u PYTHONHOME -u PYTHONPATH "$host_python" -m decomp.japan_first_c verify "$source_root" --retail-output "$source_root/$retail" --report "$source_root/build/japan_0/first-c-proof.json")
