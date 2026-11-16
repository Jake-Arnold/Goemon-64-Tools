# Japanese warp matching-C eligibility review — 16 November 2026

**Research-only result:** Eight newly recovered Japanese functions have exact isolated original-address IDO 5.3 machine-code matches, totaling **476 bytes**. This does **not** promote them into the formal Japanese matching-C manifest. The verified baseline remains **10 functions / 280 bytes**. Complete source-linked 32 MiB and recompressed 16 MiB ROMs were **not** rebuilt for these eight candidates in this investigation.

## Candidate summary

| Function | Original ROM | Bytes | IDO trailing zero padding | Relocations | Probe |
|---|---|---:|---:|---:|---|
| `func_80036C70_37870` | `0x37870` | 96 | 0 | 3 | Exact isolated link |
| `func_80036D20_37920` | `0x37920` | 56 | 8 | 3 | Exact isolated link |
| `func_80036F58_37B58` | `0x37B58` | 52 | 12 | 2 | Exact isolated link |
| `func_8003704C_37C4C` | `0x37C4C` | 56 | 8 | 3 | Exact isolated link |
| `func_80037084_37C84` | `0x37C84` | 52 | 12 | 2 | Exact isolated link |
| `func_800370B8_37CB8` | `0x37CB8` | 40 | 8 | 2 | Exact isolated link |
| `func_800370E0_37CE0` | `0x37CE0` | 60 | 4 | 2 | Exact isolated link |
| `func_8003711C_37D1C` | `0x37D1C` | 64 | 0 | 3 | Exact isolated link |

**All eight:** Identified in the pinned Japanese Splat main warp segment, independently compiled by native IDO 5.3 `-G 0 -non_shared -O2 -mips2`, and linked one function at a time with LLVM LLD for the original Japanese RAM address and the explicit original referenced-symbol addresses. The resulting function bytes were compared against the original decompressed Japanese ROM with SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Every function was exact and every relocation signature matched the reviewed original.

The two 52-byte functions initially appeared three words different, but those were **12 trailing zero-padding bytes**, not different instructions. Both match after a zero-only metadata layout adjustment. The 96-byte `func_80036C70_37870` needs an `int` intermediate to reproduce the original register allocation. The 64-byte `func_8003711C_37D1C` needs an `u8` argument for the exact stack spill. These are concrete native compiler findings rather than inferred game behaviours.

## Promotion eligibility

- **Immediate integration priority:** `func_80036C70_37870` (96 bytes) and `func_8003711C_37D1C` (64 bytes), because their original-sized compiled `.text` needs no size trim. The latter still needs four-byte section alignment at its original VMA.
- **Require reviewed section metadata packing:** the other six functions (56, 52, 56, 52, 40 and 60 bytes) have respectively 8, 12, 8, 12, 8 and 4 trailing zero bytes in IDO's standalone `.text`. A probe changed **only** the ELF `.text` header's size/alignment after verifying zeros and preserved every relocation; isolated LLD links then matched the originals. This is not proof that the original project's GNU MIPS full linker accepts the same layout.
- **Not yet eligible to count formally:** All eight await fresh Japanese Splat C/ASM split, original GNU MIPS compilation/linker-map ownership, complete 32 MiB ROM byte equality, Rommy 16 MiB retail byte equality, strict Japanese region verifier and ELF inventory tests. Do not edit `decomp/regions/japan_0.json` or increment matching totals before all gates pass.

## Verification performed

- Pinned `klorfmorf/mnsg` source commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` and original Japanese ROM SHA identities checked.
- Reproducible independent IDO+LLD checker: **8/8** exact original-address function probes, **476/476** code bytes.
- ROM-free guardrail tests **4/4 PASS**, including malformed ELF and nonzero-padding rejection.
- Changed the `0x260` constant in the 56-byte C source to `0x261` in a private test: checker correctly failed the original-ROM comparison.
- **NOT RUN:** new eight-C source-linked 32 MiB GNU MIPS build, recompression to 16 MiB retail, formal verifier, emulator, Japanese PC port, or fresh USA G2.

**Reusable private research archive:** `japan_warp_eligibility_probes.zip` generated in the user conversation, containing eight candidate C source files, a fail-closed Python IDO/LLD probe, four ROM-free tests and metadata-only proof. The archive is not attached to this GitHub commit; the checked-in JSON records its SHA-256 `3aa1a5aa3f322ce3165cec14342d0b903e8f7f3440e55cb7dce4f8fcaf7e0fa2`. No ROM or extracted proprietary game bytes are inside it.

## Additional warp leads

The same original Japanese assembly slice has larger non-promoted functions `func_80036D58_37958` (204 bytes), `func_80036E24_37A24` (208 bytes), `func_80036EF4_37AF4` (100 bytes), and `func_8003715C_37D5C` (92 bytes). These have been inspected, **not matched**. Their presence should not be included in candidate code-byte totals.

**Next step:** Stage the 96-byte and 64-byte clean candidates separately against the verified ten-C baseline, prove both ROM images, then create a dedicated fail-closed GNU MIPS object-layout adapter for the six padded C candidates.

Full metadata: `decomp/results/japan_0_warp_eligibility_2026-11-16.json`.
