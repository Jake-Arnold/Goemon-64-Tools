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

## Central production acceptance still required

This preflight is only the staging input. Implement a separately reviewed, opt-in **143-C mixed-stage adapter** for `decomp.verify`, preserving all non-file_11 canonical C/ASM objects, followed by the full USA **210+93=303** whole-ROM comparison, original address/name/size validation, all 8,825 semantic file_11 relocations, `decomp.inventory`, and complete `decomp.local_ci`. Do not change `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json` or any official matching-C count until every gate passes. The later 118 distinct file_11 candidates and three Impact/dialogue candidates remain independently pending.
