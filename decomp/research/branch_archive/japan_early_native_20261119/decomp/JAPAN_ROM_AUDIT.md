# Original Goemon 64 ROM identity: independent Japanese port inventory

**Date:** 2026-11-15  
**Purpose:** reproduction metadata only. No ROM bytes or extracts are tracked.

| Field | USA | Japan revision 0 |
| --- | --- | --- |
| User upload | `Mystical Ninja Starring Goemon (USA).z64` | `Ganbare Goemon - Neo Momoyama Bakufu no Odori (Japan).n64` |
| Uploaded file header | `80 37 12 40` | `37 80 40 12` |
| Canonical byte-order header | `80 37 12 40` | `80 37 12 40` |
| Canonical SHA-1 | `df8083a54296b8c151917c5333e1c85f014a2a66` | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Canonical SHA-256 | `1603be37427a33548857fc3d2e8867ede71121c353fb631b79b44f1d94845d80` | `a1d288fa352ef185e0499a63b64dfc937c460da15a10456f180ee71298277413` |
| Game code/revision | `NG5E/0` | `NG5J/0` |
| Header CRC1 / CRC2 | `FCBCCB21/72903C6B` | `832C168B/56A2CDAE` |
| Nisitenma signature | `0x57FC8` | `0x58248` |
| Nisitenma pointer table | `0x57FD8` | `0x58258` |
| ROM size | 16 MiB | 16 MiB |
| Expanded image SHA-1 from earlier branch research | `6ea0ed71032ce08fc2745f412d84936382197494` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

The Japanese upload is *16-bit byte-swapped* even though its filename is `.n64`. Project64 handles this transparently; native decomp extraction should use a converted `.z64` copy. SHA-1 checks always use canonical bytes.

Japanese upload's original as-is SHA-256: `881ea6adcb2c7a6fdb80bbc693f5f712e7f0c6a2973d5ace755939d5b1d21ffd`.

**Observed firsthand in this audit:** file sizes, byte-order headers, canonical SHA-1/SHA-256, game IDs/revisions, CRCs and file-table locations.

**Earlier existing-project proof, not independently rerun here:** 32 MiB expanded SHA-1s and any Japanese overlay mapping tests.

**Native full-ROM build status:** NOT RUN. **Japanese N64 emulator boot status:** NOT RUN. **Japanese PC static-recomp runtime:** NOT RUN.

Reference local verification entrypoints: `practice/game_versions.py`, `decomp/recomp_rom_input.py`, `decomp/japan_function_map.py`, `decomp/japan_overlay_map.py`. Rebuild instructions and stage gates: `docs/JAPANESE_DECOMP_PORT_PLAN.md`.

## 2026-11-15 independent expanded image reproduction

The uploaded `mnsg-japan.zip` was unpacked locally. Its Git HEAD was exactly `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, with all three source submodules and the native x86-64 IDO 5.3 toolchain present.

A standalone local Python implementation of the documented `Nisitenma-Ichigo`/LZKN64 expansion decoded the original Japanese retail cartridge. It used the original 1,312-entry file pointer table and CIC-6102 header CRC calculation. A separate file read and SHA-1 confirmed **33,554,432 bytes / `6f8745fecc3a5e7d4918c7a73353eb0726116ded` (PASS)**. The table contained 1,084 populated files, including 1,041 compressed. Local YAML parsing confirmed 72 Japanese executable code sections in the pinned Splat config. The generated ROM bytes and private file-boundary metadata remain local.

The IDO 5.3 `cc` compiler executed successfully on a small `-mips2 -O2` smoke test. `make setup VERSION=japan_0` did **not** reach Splat because `binutils-mips-linux-gnu` is absent. The environment has no DNS access to install it or the pinned Python packages. A full linked build and a verified 16 MiB recompression remain **NOT RUN**.

See `decomp/results/japan_0_reference_extraction_2026-11-15.json`. No asset or ROM bytes are stored in this repository.

## 2026-11-15 uploaded offline dependency archive

The supplied `goemon-dependencies.tar.gz` lacks four SONAME shared libraries required by its MIPS binutils executables, and its Python 3.12 venv symlink refers outside the archive. An independent upstream `tools/rommy.py decompress` run **did** succeed using the previously verified pure-Python LZKN64 decoder as a compatibility fallback. This produced the original `rommy.yaml` manifest and the exact 32 MiB Japanese reference SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. The native Splat and linker stages are not yet runnable. See `decomp/results/japan_0_offline_dependency_audit_2026-11-15.json`.
