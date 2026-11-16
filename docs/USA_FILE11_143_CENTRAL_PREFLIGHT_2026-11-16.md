# USA file_11 143-C central promotion preflight

Date: 16 November 2026. **Status: candidate preparation only; not a production promotion.**

The canonical `chatgptweb/decomp` verifier currently accepts 13-C and 50-C `file_11` stage formats. The native-matching research fixture at `decomp/research/file11_143_candidate/file11_143_source_fixture.json` instead contains **143 functions / 3,908 bytes** in **44 C plus 44 ASM slices**, including the existing **50 C / 1,064 bytes** and **93 additional research C / 2,844 bytes**. The fixture's separately exact clean-upstream ROM build does **not** establish a combined 303-function canonical G2.

## Opt-in preflight command

Run from a full local decomp checkout with Python 3.10+:

```bash
python3 -m decomp.file11_143_preflight \
  --manifest decomp/manifest.json \
  --fixture decomp/research/file11_143_candidate/file11_143_source_fixture.json \
  --original-expanded-usa-rom /path/to/authenticated/usa/baserom.decompressed.z64 \
  --output-dir /tmp/goemon-file11-143-preflight-new
```

The original-ROM argument is optional for ROM-free source/schema planning, but **required for ROM-authenticated preflight**. It must be the actual 32 MiB original expanded USA ROM with SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The stage checks exact original ROM chunk SHA-256s when that argument is supplied.

Outputs are written **only** to a previously nonexistent external directory: `src/*.c` (44 embedded reviewed C sources), `file11-subsegments.txt` (all 88 original-order Splat subsegment lines), and `preflight.json` (metadata-only). No build, ROM, compiled object or main repository file is modified. Existing output directories and staging inside `decomp/` are rejected.

## Guards

- Exact canonical 210-function manifest with 50-function file_11 v2 stage, authenticated region and upstream source pins.
- All 50 previously claimed file_11 functions preserved **by original function name, ROM offset and size**, not merely by count.
- Exactly 93 new and distinct original-address research functions. No overlap with other 210 canonical C names.
- 44 complete C groups plus 44 intervening ASM ownership spans; no holes or overlaps, original guest VMA mapping and pinned source/object/checksum identities.
- All embedded source content checked against per-C SHA-256; change, duplicate, move or unsafe source rejects the stage.
- Production claims remain **210**. `preflight.json` always records `central_g2_verified: false` and `eligible_for_manifest_promotion: false`.

ROM-free tests: `python3 -m unittest tests.test_decomp_file11_143_preflight -v`. This suite needs the full connected repository fixture; Python source syntax was checked in an isolated environment, and connected-repository structural assertions for the existing 50 and new 93 were performed. The complete Python suite and native 303-function build **have not yet been run**.

## Fresh original-ROM boundary audit

Using the authentic local original USA expanded 32 MiB ROM (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`), independently recomputed SHA-256 for **all 88 contiguous file_11 text chunks**, spanning ROM `0x587370–0x5B8500` (**201,104 bytes**). Every chunk digest matched the corresponding pinned source fixture's `original_sha256`; **88/88 PASS, zero discrepancies**. The aggregate FNV-1a 64-bit value `a60bac069e456e44` was used only to transport/check the individual SHA-256 comparison list between isolated runtimes, not as a replacement cryptographic hash.

The audit proves original-ROM chunk extents/data identity, **not** that the 44 emitted C sources reproduce original IDO object code when combined with the current 210-C production build. Metadata-only report: `decomp/results/file11_143_original_rom_chunks_20261116.json`.

## Central production acceptance still required

This preflight is only the staging input. Implement a separately reviewed, opt-in **143-C mixed-stage adapter** for `decomp.verify`, preserving all non-file_11 canonical C/ASM objects, followed by the full USA **210+93=303** whole-ROM comparison, original address/name/size validation, all 8,825 semantic file_11 relocations, `decomp.inventory`, and complete `decomp.local_ci`. Do not change `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json` or any official matching-C count until every gate passes. The later 118 distinct file_11 candidates and three Impact/dialogue candidates remain independently pending.

## Draft central 303-function native trial (not yet executed)

The opt-in adapter is now implemented in `decomp/file11_143_stage.py` and conditionally invoked by `decomp/verify.py`. It is activated only by a separate, newly generated manifest with `"overlay_file11_stage": {"format": "goemon-file11-143-central-v1"}`. The tracked canonical `manifest.json` remains **unchanged**, with 210 matching USA C functions.

On an Ubuntu checkout containing all private `Goemon-64-Tools` source files and the pinned toolchain, create the trial manifest *outside* the repository:

```bash
python3 - <<'PY'
from copy import deepcopy
import json
from pathlib import Path
from decomp.verify import load_manifest
manifest = deepcopy(load_manifest(Path("decomp/manifest.json")))
manifest["overlay_file11_stage"] = {"format": "goemon-file11-143-central-v1"}
Path("/tmp/goemon-usa-303-trial-manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
)
PY

python3 -m decomp.verify \
  --upstream /path/to/pinned/mnsg-japan \
  --retail-rom "/path/to/Mystical Ninja Starring Goemon (USA).z64" \
  --manifest /tmp/goemon-usa-303-trial-manifest.json \
  --workdir /tmp/goemon-303-g2-FRESH \
  --report /tmp/goemon-303-g2-report-FRESH.json \
  --source-dir decomp \
  --jobs 8

python3 -m decomp.inventory \
  --manifest /tmp/goemon-usa-303-trial-manifest.json \
  --baseline /tmp/goemon-303-g2-FRESH/baseline \
  --candidate /tmp/goemon-303-g2-FRESH/candidate \
  --report /tmp/goemon-303-g2-inventory-FRESH.json

python3 -m decomp.local_ci
```

Replace the pinned checkout and ROM paths with the actual available paths, and provide portable Python/binutils options if using the supplied offline environment. Both `--workdir` and report paths must be **new/nonexistent**, and all generated ROMs, objects and reports must remain outside Git.

**Required green gates:** the trial verifier must report **303 newly C-owned USA functions / 16,180 instruction bytes** and an identical original 33,554,432-byte ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, with 143 original-function symbols and **8,825** semantic file_11 relocations. The inventory must retain **7,376** positive-sized original ELF function entries, 13 original upstream C entries, 303 newly promoted C and **7,060** assembly-owned entries, with zero unexpected aliases. The unchanged `decomp.local_ci` regression suite must also pass.

**Status:** This native 303-C execution is **not run**. The original USA source/ROM baseline and 143 original ELF entry identities were independently verified in this session, but the container does not have the private canonical 210-C source tree. A draft code change is not proof of native matching and must not be merged or counted until all native and ROM-free gates pass.
