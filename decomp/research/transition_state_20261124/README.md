# Transition-state promotion staging — 24 November 2026

Base: 4efacadb87c1d3f14fc082959e280325ccec5185. This draft retains canonical manifests and ASM ownership unchanged until the complete promotion gates pass.

- USA 454C: fresh exact USA2323 predecessor, exact independent shadow and native full 32 MiB and retail 16 MiB ROM, whole mixed 2256-byte unit, 7376 FUNC identities, 26714 stable globals, all 82098 independent-reference relocations, strict predecessor-relative inventory (one new C). See `usa/full_native_summary.json`.
- Japan: 17 isolated exact native functions / 1432 bytes; see `japan/isolated_manifest.json`. The 4470 alias-free base expression preserves the original g_system symbol and all nine independent numeric-reference relocations. Full integrated proof and canonical acceptance are separate gates.
- Hold USA 3CF0 (exact instructions, unresolved no-argument caller vs research s32 argument) and Japan 3C90 (85/111 instructions, unresolved ABI) as ASM. Do not claim either.
- Both regional actual-source semantic suites passed GCC/Clang ASan/UBSan (USA 66051, JP 70400 per compiler); no emulator gameplay test. No ROMs, original generated assembly, binaries or toolchain are included.

Candidate status only. No canonical counts changed.
