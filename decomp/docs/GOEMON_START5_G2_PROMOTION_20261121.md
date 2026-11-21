# Native G2 promotion: Goemon gameplay Start path (five functions, both regions)

**21 November 2026** — original-ROM exact C, full linked original ELF and **all-section** semantic relocations. Implementation branch: `chatgptweb/decomp`. Actual gameplay: **NOT RUN**. Native-code proof is not a claim that the one-frame Bomb Text Skip causation has been observed.

## Summary of acceptance

| Metric | Japanese rev-0 | USA |
|---|---:|---:|
| Previously accepted C | 2,118 | 1,956 |
| New original-address C | **3** | **2** |
| New original instruction bytes | **388** | **352** |
| Total accepted C | **2,121** | **1,958** |
| Total accepted original C bytes | **112,244** | **84,292** |
| Remaining original assembly functions | **5,255** | **5,405** |
| Full original ROM comparison | **33,554,432/33,554,432** | **33,554,432/33,554,432** |
| Original ELF positive-size FUNC identities | **7,376/7,376** | **7,376/7,376** |
| All original semantic relocations preserved | **80,747/80,747** | **82,103/82,103** |

The five new functions (name/region/original ROM offset/size) are:

- JP `func_8001F580_20180` / `0x20180` / 100 bytes — gameplay three-callback dispatcher.
- JP `func_8001F610_20210` / `0x20210` / 252 bytes — actual gameplay Start gate and pause latch.
- JP `func_8003EE44_3FA44` / `0x3FA44` / 36 bytes — VM command-cursor busy test.
- USA `func_8001F8B0_204B0` / `0x204B0` / 100 bytes — gameplay dispatcher.
- USA `func_8001F940_20540` / `0x20540` / 252 bytes — gameplay Start gate.

Original expanded ROM SHA-1s: Japan `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; USA `6ea0ed71032ce08fc2745f412d84936382197494`. Original ELF positive function identities and relocations were compared between **existing verified staged baselines** and newly integrated sources; no original ROM executable bytes changed. Japan's normalized retail original was independently proved during the baseline JP 2,118 full build.

Original all-section semantic-relocation SHA-256 (canonical `readelf -r -W` record multiset): Japan `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20`; USA `f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97`.

**USA inventory nuance:** a previous baseline accepted-code counter was 1,956, but original ELF contains **13 preexisting non-owned unmarked functions**. Full unmarked ELF count is 1,969 before and 1,971 after this two-function increment; official accepted-C count is **1,958** (do not miscount the 13).

## How original semantic relocations were recovered

A naïve C copy of the Japanese dispatcher and Start input produced the **exact original 32 MiB ROM** but failed a strict relocation check: four original main relocations were missing and two were renamed. The project-local overlay-only relocation helper did not detect these. The final adapter's `all_semantic_relocations` audit explicitly includes **`.rel.main`**, fails closed on every changed symbol/type/address, and requires the entire original relocation SHA-256.

- JP dispatcher code must refer to original absolute-offset symbol **`D_3ADDE`**. Writing the constant numeric index `0x3ADDE` can produce identical instructions but drops the two original HI16/LO16 records.
- JP Start input must reference a pointer derived from **`g_system + 0x3B07C`**, not a new independent global named `D_800CD52C` pointing to the same virtual address. Source expression choice matters for original relocation identity.
- USA Start C must reference the original separated region data symbols **`D_800BCCC0_BD8C0`** and **`D_8014CCC0_14D8C0`**, with appropriately sized struct layouts. A single global aggregate produces byte or relocation differences even when behaviour is equivalent.
- USA candidate functions replace two original `GLOBAL_ASM` pragmas within the already accepted mixed source unit `src/rotation_angles.c`; original neighbouring accepted C and the untouched pause controller ASM pragma remain.

## Excluded sixth function: still original assembly

Japanese `func_8001F70C_2030C` is **not** part of this promotion. Its 68-byte original-address isolated C is byte-identical, but the numeric-offset version drops original relocation pairs to `D_3ADDF`. The symbolic-pointer variants changed the IDO instruction schedule and/or compiled extent (64 instead of 68 bytes). The complete full-ROM and relocation test therefore rejects it. Keep the original ASM until exact **instructions + complete original relocation graph** both pass. No count for this function was included above.

## Reproducibility and tests

Authoritative staging/rebuild/verification tool: `decomp/glitch_g2_promotion.py`. Exact source and hash ledger: `decomp/research/glitch_g2_20261121/manifest.json`. Research/acceptance report: `decomp/results/glitch_start5_2121jp_1958usa_g2_20261121.json`. Source-only instructions: `decomp/research/glitch_g2_20261121/README.md`.

- Fresh pinned Japanese upstream and verified JP 2,118 full build: **PASS original expanded/retail 32 MiB/16 MiB, 7,376 original ELF functions, 80,747 original semantic relocations and full local CI**.
- Fresh USA 1,956 full original ROM baseline: **PASS**, original ELF and relocation verification.
- New JP 3 C stage: **PASS** exact expanded ROM, all ELF functions, *all* 80,747 relocs, strict C/ASM ownership (2,118→2,121); reproduced from an independent clean copy of JP 2,118 verified workspace.
- New USA 2 C stage: **PASS** exact expanded ROM, all ELF functions, *all* 82,103 relocs, strict C/ASM ownership (1,956→1,958); reproduced from an independent clean copy of USA 1,956 verified workspace.
- `python3 -m unittest decomp.test_glitch_g2_promotion` **PASS**; detects source/manifest drift, dedupe, original symbols and main-relocation inclusion.
- Full `python3 -m decomp.local_ci` **PASS** on final staged code and tests: 300 decomp Python test cases (one skipped), 349 verifier/ledger cases (four skipped), task/evidence validation and all configured native-C host ASan/UBSan fixtures.
- Emulator gameplay / successful Start-driven Bomb Text Skip: **NOT RUN**. Save files: not modified. The hypothesis that a correctly timed Start launches a deferred pause/reset before bomb checkpoint index 13 is written remains unproven.

## Publication boundary

These five functions have reached **PASSED_G2 — PUBLISHED_REMOTE_VERIFIED**. Implementation commit [`13a3a08a`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/13a3a08a124e3ba9883d0a30d46b33995e9137d8) is present on `chatgptweb/decomp`; original-ROM, ELF and full relocation checks were repeated from the published source, and full local CI passed. Do not claim a full-ROM result based only on isolated IDO function matches. No game ROMs, original assembly dumps, object/ELF files, saves, personal diagnostics or proprietary toolchain are committed.
