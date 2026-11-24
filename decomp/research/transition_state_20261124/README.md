# Transition-state promotion staging — 24 November 2026

Base: 4efacadb87c1d3f14fc082959e280325ccec5185. This draft retains canonical manifests and ASM ownership unchanged until the complete promotion gates pass.

- USA 454C: fresh exact USA2323 predecessor, exact independent shadow and native full 32 MiB and retail 16 MiB ROM, whole mixed 2256-byte unit, 7376 FUNC identities, 26714 stable globals, all 82098 independent-reference relocations, strict predecessor-relative inventory (one new C). See `usa/full_native_summary.json`.
- Japan: 17 isolated exact native functions / 1432 bytes; see `japan/isolated_manifest.json`. The 4470 alias-free base expression preserves the original g_system symbol and all nine independent numeric-reference relocations. Full integrated proof and canonical acceptance are separate gates.
- Hold USA 3CF0 (exact instructions, unresolved no-argument caller vs research s32 argument) and Japan 3C90 (85/111 instructions, unresolved ABI) as ASM. Do not claim either.
- Both regional actual-source semantic suites passed GCC/Clang ASan/UBSan (USA 66051, JP 70400 per compiler); no emulator gameplay test. No ROMs, original generated assembly, binaries or toolchain are included.

Candidate status only. No canonical counts changed.

## Completed integrated native replay

Japan 2551-C candidate now independently reproduces the complete expanded and retail ROM, all 7376 FUNC identities, 26393 stable globals, and 80655 semantic relocations. The independent original ASM shadow drops exactly 90 synthetic ABS field-offset relocations. Original object padding was retained using the same reviewed zero-padding trim guard; no instruction bytes or relocations were edited. Strict predecessor-relative readelf inventory passes. See `japan/full_native_summary.json`. Full `decomp.local_ci` passed with unchanged canonical manifests (500+351 Python tests, 7 comparator tests and all configured sanitizers). This is not candidate canonical CI. Both promotion ownership stages and final canonical CI remain mandatory. Full private proof and replay scripts are preserved in the source-only handoff archive.

## 2026-11-24 — transition-state native promotion gates PASS (PR #218)

- Base `stable/decomp@4efacadb87c1d3f14fc082959e280325ccec5185`; USA `func_8000394C_454C` (+116 bytes), Japan 17 functions (+1,432 bytes). Candidate totals: USA 2,324 C / 5,039 ASM; Japan 2,551 C / 4,825 ASM. Both regional transition modules reach 21/22 matching C.
- Fresh pinned IDO 5.3 native builds reproduce expanded and retail original ROMs, all 7,376 function identities per region, USA 26,714 and JP 26,393 stable globals; independent original-reference semantic relocation counts 82,098 and 80,655. Independent numeric original shadows account for exactly 4 and 90 synthetic ABS-offset relocation differences respectively; native instructions and relocations were not edited. Strict inventory and both promotion integrity validators PASS. Frozen predecessor proofs retained. USA 3CF0 (142/142 isolated but unresolved caller ABI), Japan 3C90 (85/111) retain ASM. No gameplay testing or toolkit changes.
- Full `CC='gcc -no-pie' python3 -m decomp.local_ci` PASS (exit 0): 504 + 351 + 7 Python tests, three expected skips, configured sanitizer checks and both promotion integrity validators. Initial stale test projections corrected without weakening native gates. New host semantic tests: USA 66,051 and JP 70,400 cases each under GCC and Clang ASan/UBSan. See `decomp/results/transition_state_2324_2551_local_ci_20261124.json` and regional G2 reports. Publication subject to normal PR merge.

