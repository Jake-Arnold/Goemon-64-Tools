# 21 November 2026 — movement-clamp contiguous-vector IDO reconstruction

**Status: FAILED_NATIVE / RESEARCH_ONLY.** No full original-address matching C, code/ROM patch or production acceptance claim.

Target: `func_801CD310_589220`; original USA ROM `0x589220`, VMA `0x801CD310`, 4,320 instruction bytes. Original private USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; original expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. The **pristine baseline** was byte-identical to the original 33,554,432 bytes. The new candidate was **not linked** into that original ROM.

## Root cause: missing data relocation pair

The previous draft declared stack floats `spA4`, `spA8`, `spAC` as three independent scalar C locals but passed `&spA4` to original native vector helpers. Independent C scalars are **not guaranteed contiguous or reachable** through `&spA4`. The draft consequently allowed IDO to eliminate the `spA8 = 3.1f` write. The original function **does** reference `D_8020A958_5C6868` (`3.1f`) with one HI16/LO16 relocation pair. This was the previously missing pair (the original function has 34 pairs; the earlier native draft had only 33).

Replacing the three scalar declarations/usages with a single `f32 vecA[3]` restores the `3.1f` load and produces **34/34** HI16/LO16 pairs, retaining original **33 call relocations**. The resulting native ELF function is **4,152 B**, compared to previous **4,124 B**.

## Independently compiled variants

| Vector groups reconstructed | ELF function bytes | Shortfall | HI16 pairs | Native frame |
|---|---:|---:|---:|---:|
| None (previous) | 4,124 | 196 | 33 | 440 |
| A = `spA4/spA8/spAC` | 4,152 | 168 | 34 | 448 |
| B = `spB0/spB4/spB8` only | 4,144 | 176 | 33 | 440 |
| C = `spC0/spC4/spC8` only | 4,140 | 180 | 33 | 448 |
| A+B+C | 4,188 | 132 | 34 | 448 |
| A+B+C+D (`spCC/spD0/spD4`) | **4,200** | **120** | **34** | **448** |

Additional A/B/C/D subsets and seven early-third-argument ABI variants were compiled using pinned original IDO 5.3 and unchanged original flags. The early ABI variants did not reduce the best 4,200-byte discrepancy and sometimes added stack spills. Groups B, C and D are source-layout reconstruction candidates; the original numeric stack offsets are grounded, but whether group D represents a true gameplay vector is not yet independently identified.

**Final current structural audit of 4,200-byte candidate:** 33/33 native calls match original callee identities and order; all nine `sqrt.s` instructions are present; 18-entry switch table case-group assignments match; original text has 33 `R_MIPS_26`, 34 `R_MIPS_HI16`, 34 `R_MIPS_LO16` and current C emits exactly those **counts** (101 total). The actual relocated targets/instructions **do not** yet match. Frame is **448 vs 232** original and saved `$f20` remains. Compiler emits 16 pointer-type warnings; semantics not host-tested. The candidate differs in full native text and is **not** formally accepted.

**Reproduction:** separate conversation artifact `GOEMON_CLAMP_VECTOR_LAYOUT_20261121.zip` contains latest complete C, preceding 4,124-byte C, original-ID0 replay shell, read-only ELF/ROM audit, 14-case source-layout variant matrix and sanitized JSON. No original ASM, original ROM bytes, extracted assets, proprietary tools or compiled ELF/object included. Fresh replay of bundled source and auditor **PASS** for reported structural facts; original 32 MiB unchanged baseline **PASS**. Complete canonical `decomp.verify`, strict inventory, full `decomp.local_ci`, and emulator gameplay **NOT RUN**.

**Next:** resolve 448-vs-232 stack allocation and the hoisted saved `$f20` register, reconstruct early `a2`/`f12` argument handling from original MIPS and restore correct branch scheduling. No re-promotion or change to accepted counts. Last checked production USA: **1,956 matching C / 83,940 instruction bytes / 5,407 ASM**.
