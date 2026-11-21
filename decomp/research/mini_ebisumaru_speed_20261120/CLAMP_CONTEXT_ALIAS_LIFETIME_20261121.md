# USA movement clamp context-pointer aliasing and call-aware floating-point lifetime (21 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY.** No production promotion. Original USA `func_801CD310_589220`: ROM `0x589220`, VMA `0x801CD310`, original **4,320 bytes**, stack frame **232 bytes**, linker `file_11`. Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original SGI IDO 5.3 `-O2 -mips2 -G 0 -non_shared`.

## Source change derived from verified original MIPS

Following the original context-gate operations, the candidate reads context byte `+0x59` after four task movement-reset writes. Testing a separate task `+0x5C` context-pointer reload before that byte access, rather than a nested one-expression dereference, improves native original-offset matching. This change affects only that read in the independently reconstructed full function, not original ASM or toolchain. Source-only patch `clamp_context_reloaded_20261121.patch`. The full nonmatching C and reproducible compiler/test scripts are in the accompanying 14-file conversation ZIP `GOEMON_CLAMP_CONTEXT_LIFETIME_20261121.zip`.

| IDO native C trial | Function bytes | Stack frame | Same-position nonreloc words | Original-offset/type/symbol relocations |
| --- | ---: | ---: | ---: | ---: |
| Baseline magnitude lifetime (source `06e015d624c2c9be48d0c0e02bb43e882fc02c4e9aec084df39764d5bedd5be4`) | 4,320 | 232 | 19/895 | 4/101 |
| **Explicit context reload** (source `53f11a64313715e20c9c7e3faf2c2257d945833f9f9854700e6b5fd2b04d510b`) | **4,324** | **232** | **24/902** | **10/101** |
| Context reload plus reuse in status-bit gate | 4,324 | 232 | 23/902 | 10/101 |
| Reuse in status-bit gate only | 4,324 | 232 | 23/902 | 10/101 |

All four genuine original IDO compilations retain **33 authentic calls in order**, **9 inline `sqrt.s`**, **101 text relocations** and **99/101 literal ordered type+symbol records** (two compiler-owned `.rodata` references remain different from the named original jump table). The 18 jump destinations remain correctly grouped but their original relative positions differ by **4–20 bytes**. First same-position difference is still **`+0x04`**, extra `$f20` save; this candidate is 4 bytes too long. The earlier, historically stronger **157/925** original-position candidate remains unavailable as complete C in this session; it is not superseded by the 24-word source.

## Call-aware original-MIPS register audit

New source-only analyzer `context_lifetime.py` (SHA-256 `bba5f2edab68b22ab203eff9b1ec76c2d943285614cb1843d34ae87b37624e3f`) uses authenticated private original USA code and compiled native object, does not contain or publish any original MIPS words, and produces a sanitized def/use summary. It recognises that caller-saved COP1 registers can be overwritten **after** a `jal` delay slot; thus a later `$f0` return value must not be attributed to the initial zero. The analysis is conservative and linear, not full path-sensitive SSA.

- Original early `mtc1 zero,$f0` at `+0x04` has **three** stores at `+0x18,+0x1C,+0x20` before the first call, **zero** calls crossed as a zero value.
- Candidate uses `mtc1 zero,$f20` at `+0x08`; its conservative register live range has **66 reads**, surviving **29** intervening helper-call sites.
- Original function contains **58** explicit COP1 zero definitions; candidate **10**.
- Original `+0x1B4..+0x25F` context block contains **four separate zero definitions** (`$f14` once and `$f16` three times); candidate aligned window `+0x1C4..+0x26F` has **none**. These are real differences in generated registers/lifetime.
- The two aligned windows have **43 instructions each** and **34 ordered opcode/memory shapes** in common when register identity and branch distances are intentionally ignored. This is **not** 34 byte-identical words or a claim of equivalent branch semantics.
- Original context flag-byte load at `+0x1BC`; candidate at `+0x1CC`, offset shift **16 bytes**.

## Verification actually executed

- USA original 16 MiB ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, 32 MiB expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`: PASS.
- Clean original pinned-USA 33,554,432-byte rebuild, exact byte comparison and SHA-1: **PASS** (unmodified baseline, not an experimental replacement).
- Authentic native IDO compile, source hash checks, original offset instruction/relocation/ELF comparator and four bounded variants: **PASS measured, FAIL exact native equality**.
- **Seven** synthetic register-decoder/def-use unit tests: PASS.
- Original-MIPS context gate branch/write micro-execution: **3,000/3,000 PASS**. This tests original behaviour, not complete source C equivalence.
- Extracted fresh copy of 14-file conversation ZIP, compiled and replayed the four expected failures, checked all native reports and seven unit tests: PASS.
- Experimental C integration, current accepted-USA `decomp.verify`, strict inventory, full `decomp.local_ci`, emulator gameplay: **NOT RUN** because function remains nonmatching and complete live decomp local checkout unavailable (shell GitHub DNS fails).

Full source package SHA-256 `b13cd5719f454557927cc36e70e1d7161a78be5a15a87366a98d570af55eb532`. It contains complete C variants, comparator, read-only call-aware analyzer, synthetic unit tests, original-MIPS gate micro-executor and replay commands. No ROMs, extracted original ASM, native objects/ELFs or toolchains are in the package or this PR.

## Next concrete reconstruction action

Use the explicit context pointer reload as a source hypothesis, **not** as proof the original C had that declaration. With the stronger 157-word source when available, recover distinct source lifetimes matching the original context `$f14` zero, the three `$f16` zero definitions and reloads. Compare actual original-offset MIPS/relocations, preserving original branch-likely conditional memory accesses. Avoid further total-size/volatile chasing. Preserve original ASM and keep PR #144 draft.

Official USA production remains **1,965 matching C / 84,648 original instruction bytes / 5,398 ASM** (latest independent full-G2 proof); older `combined.json`/inventory snapshots are still at 1,956.
