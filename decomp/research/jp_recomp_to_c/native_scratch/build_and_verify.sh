#!/usr/bin/env bash
# Original-USA native scratch acceptance. Does not modify production checkout.
set -euo pipefail
: "${GOEMON_BASELINE:?Set to a pristine, Splat-split, exact-ROM-built original USA mnsg checkout}"
: "${GOEMON_C_SOURCE_ARCHIVE:?Set to the unpacked verified 52-function C source archive}"
: "${GOEMON_CANDIDATE:?Set to an unused, disposable candidate directory path}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -e "$GOEMON_CANDIDATE" ]]; then
  echo "Fail-closed: candidate directory already exists: $GOEMON_CANDIDATE" >&2
  exit 1
fi
if [[ ! -f "$GOEMON_BASELINE/build/usa/mnsg.elf" || ! -f "$GOEMON_BASELINE/build/usa/mnsg.z64" ]]; then
  echo 'Fail-closed: original USA baseline has not been fully rebuilt' >&2
  exit 1
fi
BASE_ORIGINAL="$GOEMON_BASELINE/config/usa/baserom.decompressed.z64"
if [[ "$(sha1sum "$BASE_ORIGINAL" | cut -d' ' -f1)" != '6ea0ed71032ce08fc2745f412d84936382197494' ]]; then
  echo 'Fail-closed: non-original expanded USA source ROM' >&2
  exit 1
fi
cmp -s "$GOEMON_BASELINE/build/usa/mnsg.z64" "$BASE_ORIGINAL" || {
  echo 'Fail-closed: original baseline build is not byte-exact' >&2;exit 1;
}

env -u PYTHONHOME -u PYTHONPATH /usr/bin/python3 "$HERE/stage_overlay_batch.py"
cd "$GOEMON_CANDIDATE"
mapfile -t c_objs < <(env -u PYTHONHOME -u PYTHONPATH /usr/bin/python3 - <<'PY'
import json
from pathlib import Path
p=Path('promotion_scratch_metadata.json')
for row in json.loads(p.read_text())['functions']:
    print('build/usa/src/promotion_scratch/'+row['name']+'.c.o')
PY
)
make -j4 VERSION=usa "${c_objs[@]}"
env -u PYTHONHOME -u PYTHONPATH /usr/bin/python3 "$HERE/pack_batch47.py"
mapfile -t asm_objs < <(find asm/usa -maxdepth 1 -name '*_scratch_part_*.s' -printf 'build/usa/%p.o\n' | sort)
make -j4 VERSION=usa "${asm_objs[@]}"
env -u PYTHONHOME -u PYTHONPATH /usr/bin/python3 "$HERE/trim_split_asm.py"
make -j4 VERSION=usa build/usa/mnsg.z64
env -u PYTHONHOME -u PYTHONPATH /usr/bin/python3 "$HERE/verify_batch47_link.py"
