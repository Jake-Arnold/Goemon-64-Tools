# Adjacent `file_11`: 21 additional original-address C matches and exact 73-function USA scratch proof

**Date:** 16 November 2026. **Status:** research; **not** a central 233-function promotion.

## Relation to the existing work

The 50 `file_11` functions in PR #20 are already formally promoted on `chatgptweb/decomp` (210 central exact USA C functions). Draft PR #24 adds two standalone verified transition C functions, 56 bytes, and an independent 52-function scratch build. The present work finds **21 further unique USA functions (336 bytes)** and combines them with those 52.

## New exact USA/Japan native-C pairs

| USA VMA (ROM) | Japan VMA (ROM) | Bytes each | C semantics |
|---|---|---:|---|
| `801F7130 (5B3040)` | `801FC014 (5B7FE4)` | 8 | Clear actor's word at offset `0x48` |
| `801F7138 (5B3048)` | `801FC01C (5B7FEC)` | 8 | Empty function |
| `801F8EDC (5B4DEC)` | `801FDDE4 (5B9DB4)` | 48 | Call three helpers in order |
| `801FA5A8 (5B64B8)` | `801FF4B8 (5BB488)` | 44 | Call helper with a 16-bit value and zero |
| `801FA6C4 (5B65D4)` | `801FF5D4 (5BB5A4)` | 32 | Call helper with zero |
| `801FB230 (5B7140)` | `80200140 (5BC110)` | 16 | Write `0x80` to region-specific byte |

These six equal 156 bytes in each region. The last function writes USA `0x8015C54D`, Japan `0x80161D3D`. Fourteen other original-USA 12-byte empty two-argument callbacks plus a fifteenth were also proved (180 USA bytes) at:

`801CB5C4`, `801CB7F4`, `801D23C8`, `801E0810`, `801E08B0`, `801E5084`, `801EA0CC`, `801EA4D0`, `801EA4DC`, `801ED500`, `801ED50C`, `801F2CB4`, `801F2CC0`, `801FC578`, `801FC584`.

The final two USA callbacks also have exact Japan counterparts `0x80201488`, `0x80201494` (24 JP bytes). Consequently **21 USA new functions / 336 bytes** and **eight JP functions / 180 bytes** were authenticated at original VMA with original IDO 5.3. The 37 formerly promoted noops and PR #24's 12-byte noop were excluded, so the 21 do not double-count.

## Independent complete USA scratch proof

- **73** original-address `file_11` C functions (the earlier 52 plus 21), **1,456 matching instruction bytes**.
- **46** linked original-order C/ASM chunks, preserving assembly gaps.
- **33,554,432 / 33,554,432 bytes** of the USA ROM match exactly; SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- `file_11` VMA `0x801CB460`, overlay size `0x41400`, unchanged.
- **73/73 original-address FUNC symbols**, function lengths and instruction SHA-256 values validated.
- Complete pristine USA ELF versus candidate ELF: **8,825/8,825 semantic relocation tuples** identical. Their raw ordering is **not identical**: two 3-record rotations, at indices **2506–2508** and **6131–6133**; no other differences.
- Both baseline and 73-C scratch ELF have exactly **7,376** positive-size function entries. One Splat-generated extra FUNC label on the original NOP at USA VMA `0x801F2CCC` was removed without changing the NOP or ROM bytes.
- **19 ROM-free research/claim-guard tests passed**; not a full repository Local CI run.
- The full Japanese ROM is not rebuilt by this result; Japan claims are **isolated original-VMA function matches**.

The source-only reproducibility archive `goemon-file11-adjacent-73-research-20261116.zip` in the project conversation includes `probe_adjacent.py`, the 46-chunk `stage_file11_73_scratch.py`, the generated per-island C sources, independent native proof JSON, full pristine/candidate ELF audit JSON, regression tests, and supporting auditor/trimmer scripts. SHA-256 of the research archive: `deb96e14a4a6e13af6a6b7b9e6098f503990db7e9afcbddfc731145078456094`. ROMs, ELFs, generated assembly, objects, private compiler, and assets are **not** included or committed.

## Promotion gate (not completed)

Current formal central USA count remains **210 C functions / 13,336 bytes**. The two functions in PR #24 and these 21 new matches are research-only. A future central 210 + 23 = **233-function** build would need to prove 13,728 bytes, exactly 7,130 remaining assembly entries, all overlay symbol/relocation provenance and the entire USA 32 MiB ROM using a separate, opt-in v3 stage. Those are *targets*, not achieved promotions. Do not modify canonical `decomp/manifest.json`, `results/combined.json` or inventory based on this scratch build.
