#!/usr/bin/env bash
# Build exact Japanese N64 ROM with pinned mnsg and supplied offline dependencies.
set -euo pipefail
if (( $# != 3 )); then
  echo "Usage: $0 <pinned-mnsg-checkout> <goemon-dependencies-dir> <goemon-runtime-additions-dir>" >&2
  exit 2
fi
source_root=$(realpath -- "$1")
deps=$(realpath -- "$2")
additions=$(realpath -- "$3")
script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
tool="$script_dir/japan_asm_baseline.py"
host_python=$(command -v python3)
python312="$additions/python/bin/python3.12"
expected_source=7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee
if [[ "$(git -C "$source_root" rev-parse HEAD)" != "$expected_source" ]]; then
  echo "Wrong upstream mnsg checkout commit: $expected_source required" >&2
  exit 1
fi
if [[ ! -x "$python312" || ! -d "$deps/.venv/lib/python3.12/site-packages" ]]; then
  echo "Missing Python 3.12 executable or offline site-packages." >&2
  exit 1
fi
export PYTHONHOME="$additions/python"
export PYTHONPATH="$deps/.venv/lib/python3.12/site-packages"
export LD_LIBRARY_PATH="$additions/lib"
export PATH="$deps/bin:$PATH"
"$python312" -c 'import yaml, splat, lzkn64, spimdisasm'
mips-linux-gnu-ld --version >/dev/null
cd "$source_root"
if [[ ! -f config/japan_0/baserom.z64 ]]; then
  echo "Missing locally verified Japanese config/japan_0/baserom.z64" >&2
  exit 1
fi
expected_retail=9843ee979b5f6c80f5eda85df0baed9ae7c4e73b
actual_retail=$(sha1sum config/japan_0/baserom.z64 | cut -d' ' -f1)
if [[ "$actual_retail" != "$expected_retail" ]]; then
  echo "Wrong Japanese ROM: $actual_retail" >&2
  exit 1
fi
if [[ ! -f config/japan_0/baserom.decompressed.z64 || ! -f config/japan_0/rommy.yaml ]]; then
  "$python312" tools/rommy.py decompress \
    --input config/japan_0/baserom.z64 \
    --output config/japan_0/baserom.decompressed.z64 \
    --manifest config/japan_0/rommy.yaml --pad
fi
expected_expanded=6f8745fecc3a5e7d4918c7a73353eb0726116ded
actual_expanded=$(sha1sum config/japan_0/baserom.decompressed.z64 | cut -d' ' -f1)
if [[ "$actual_expanded" != "$expected_expanded" ]]; then
  echo "Wrong Japanese decompressed image: $actual_expanded" >&2
  exit 1
fi
env -u PYTHONHOME -u PYTHONPATH "$host_python" "$tool" stage-config "$source_root"
"$python312" -m splat split config/japan_0/splat_asm_only.local.yaml
env -u PYTHONHOME -u PYTHONPATH "$host_python" "$tool" patch-asm "$source_root"
make build/japan_0/mnsg.z64 VERSION=japan_0 C_FILES= PYTHON="$python312" -j"$(printenv GOEMON_JOBS || echo 6)"
retail_output=build/japan_0/mnsg.retail.z64
rm -f -- "$retail_output"
"$python312" tools/rommy.py compress --input build/japan_0/mnsg.z64 \
  --output "$retail_output" --manifest config/japan_0/rommy.yaml --pad --verify
env -u PYTHONHOME -u PYTHONPATH "$host_python" "$tool" verify "$source_root" \
  --retail-output "$source_root/$retail_output" \
  --report "$source_root/build/japan_0/asm-baseline-proof.json"
