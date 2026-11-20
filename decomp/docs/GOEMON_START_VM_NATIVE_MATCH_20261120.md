# Native-exact C research: gameplay Start input and VM-busy function (20 November 2026)

**Status: ISOLATED_EXACT / RESEARCH_ONLY. Not canonically G2 promoted.**  
**Branch:** `chatgptweb/decomp` only. No `main` changes.  
**Original pin:** `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.  
**ROMs:** Japan expanded 32 MiB SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; USA expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.

## New original-address native-exact C

| Region | Original ELF function | Original ROM offset | Size | Exact native instructions | Status |
|---|---|---:|---:|---:|---|
| JP | `func_8001F610_20210` | `0x20210` | 252 | 63/63 | **New JP source; isolated exact** |
| JP | `func_8003EE44_3FA44` | `0x3FA44` | 36 | 9/9 | **New JP source; isolated exact** |
| USA | `func_8001F940_20540` | `0x20540` | 252 | 63/63 | **New USA source; isolated exact** |
| USA | `func_8003F1D8_3FDD8` | `0x3FDD8` | 36 | 9/9 | Already accepted in USA `decomp/script_vm.c`, **not new** |

**Net novel research:** 2 JP / 288 bytes plus 1 USA / 252 bytes. Compiled with pinned **IDO 5.3 `-G 0 -non_shared -O2 -mips2`** and original-compatible flags, linked at original function VMAs against independently checked guest symbol addresses. Every byte in the original extent compares equal; no padding or relaxed comparator was counted.

**Original function code SHA-256:**

- JP Start: `13bc993823cd242c3233f7a7c2294f1996f83bc629420cf3d9b7072da914c4ac`
- JP VM busy: `4cf777613f43631f9300d2b1d2c1d3137f2ddf1cbcff01473c7d2cdc0356281f`
- USA Start: `025dd045f4347ed791523672b3779a1d7e9e78d093ee2e33e846cfa78b12a497`
- USA VM busy: `6c5243a277aa2e1bf3d5d8f5e01bf97d82be6b5af0da7eb395a655165e057a45`

Original C types matter: the Start handler needs a sparse typed `g_system` aggregate with the original offsets `0x3ADE0/1`, `0x3ADE4`, `0x3AE16`, `0x3AE26`, `0x3AE29`, `0xCF88D`, `0xCF8A2`, plus an explicit sampled-input halfword at JP `0x800CD52C` / USA `0x800C7D3C`. A first-pass array-based reconstruction compiled to only **6/63** identical Start-handler instructions, while the typed struct compiled to **61/63** and the correctly symbolized sampled input raised it to **63/63**. Original linked code identity does not itself establish identical *full-ROM* semantic relocation ownership.

## Static control-flow finding, supported by the exact C

The gameplay update calls its per-update helper and checks the system pause latch. When latched, it invokes the pause-phase function. Otherwise it accepts **Start bit `0x1000`** only if several game-state gates pass: the local inhibit byte must be zero; submode must be <4 and not 3; the VM command cursor must be zero; two further external bytes and the halfword condition must be zero. The successful path sets the transition latch to 1, clears two phase bytes, and queues action 3. The 36-byte script-busy function is exactly `return cursor != 0`.

**New caller-path observation:** Japanese `func_8001F580_20180` uses a 3-function table at `0x80071210` with `func_8001F5E4` (initialise), `func_8001F610` (update) and `func_8001F70C` (teardown). It loads the dispatch index from `g_system_ptr` (global `0x80161DB8`) at object offset `+0x3ADDE` and calls the table entry through `jalr`. No table-index range check occurs in the bounded dispatcher. Reachability of an invalid index is **unknown**; do not call this a working exploit.

Subsequent pause transitions can call `func_8003D098_3DC98` and the script manager with ID -1, clearing the Japanese command cursor at `0x8003D1C8` if its guards permit. This establishes a plausible pre-text Start→deferred VM abort mechanism. **A successful Bomb Text Skip has not been executed in this investigation**, so the specific scheduling overlap remains unproven.

## Existing exact matches independently replayed; not counted as new

Four Japanese functions associated with the same path were recompiled and linked byte-identically, but **already belong to the JP2118 local G2 research promotion**: `func_8003D098_3DC98` (36 B, 9/9), `func_8003CC40_3D840` (76 B, 19/19), `func_8003CC8C_3D88C` (60 B, 15/15), and `func_8003E2F0_3EEF0` (64 B, 16/16). The JP2118 promotion's publication marker remains `PASSED_G2_LOCAL`; do not represent it as a newly published combined build.

## Negative probes, faithfully reported

- `func_8001F580_20180` (100-byte callback dispatcher): **23/25** matched words with two independent instructions scheduled in reverse order; `FAILED_NATIVE`.
- `func_8003D0D8_3DCD8` (548-byte reset manager): m2c first pass **29/137** matched words; `FAILED_NATIVE`.
- `func_8001F750_20350` (2,184-byte pause-state handler): original assembly reviewed, not compiled into a C candidate; `RESEARCH_ONLY`.

## Reproducibility and acceptance boundary

A sanitized stand-alone source package `goemon_start_vm_native_research_2026-11-20.zip` (11 KB) was generated in the research conversation. Its ZIP SHA-256 is `3f810a89bb7517c851c36327a3b47bd80c94e31763292c8563edac8e048aae82`. It contains four region-specific C translation units, a read-only isolated IDO compilation/link/byte-comparison verifier, a 15-case host semantic test, a full README and source hash ledger. It contains **no original-ROM bytes, extracted assembly, game assets, object/ELF files or proprietary toolchain**. Source versions are pinned with SHA-256 values in that package's manifest.

**Tests actually run:** expanded JP/USA original ROM SHA-1 checks PASS; four isolated original-address native code comparisons **4/4 PASS** (144/144 original MIPS instructions, 576/576 tested bytes including already accepted USA VM busy); GCC host-side **15/15** cases with ASan/UBSan PASS; Python verifier syntax PASS; research ZIP CRC/integrity test PASS. The **new**, deduplicated subset is 540 bytes.

**Not run:** actual emulator/gameplay skip; N64 frame scheduling; native code integration into a fresh *canonical* USA1723/JP2118 checkout; full 32 MiB rebuilt-ROM G2; original ELF relocation-multiset validation; strict inventory; full `decomp.local_ci` on the newly reconstructed C. The pinned original mnsg workspace and isolated tests are **not** substitutes for those gates. Consequently **zero functions are promoted**.

**Next exact task:** integrate the *three new* sources on `chatgptweb/decomp`, deduplicate against both live manifests, preserve all accepted original C, run full region-specific exact-ROM/ELF/relocation/inventory/CI acceptance, and only then increment accepted counters. The independent gameplay timing test requires instrumentation of a successful Start skip to establish whether script reset occurs before the checkpoint-13 store. See [Issue #139](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/139).
