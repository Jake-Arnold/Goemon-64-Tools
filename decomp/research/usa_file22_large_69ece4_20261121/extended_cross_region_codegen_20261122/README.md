# Original file22 large renderer: cross-region machine-code identity and bounded IDO live-range tests

**22 November 2026 — RESEARCH_ONLY / FAILED_NATIVE.** This is the original USA `func_801CC0C4_69ECE4`, ROM `0x69ECE4`, guest `0x801CC0C4`, **1,808 bytes/452 instructions**. Original ASM ownership is preserved. This does not promote a function or add to accepted-C counts.

## Independently reproduced original binary identity

SHA-1-pinned original full USA decompressed 32 MiB: `6ea0ed71032ce08fc2745f412d84936382197494`. Original Japan decompressed 32 MiB: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Rechecked original USA expanded 32 MiB rebuild by byte-for-byte `cmp`: PASS.

The Japan analog is ROM `0x6A37D4`, guest `0x801D17F4`, also 1,808 bytes. Exact **450/452 original MIPS words are byte-for-byte identical across the two regions**, with differences restricted to function-relative `+0x40` and `+0x4C`. These form the original cursor-address `R_MIPS_HI16/LO16` materialisation:

| Original address | USA | Japan |
|---|---|---|
| Function ROM | `0x69ECE4` | `0x6A37D4` |
| Function guest | `0x801CC0C4` | `0x801D17F4` |
| Global DL cursor | `0x801D701C` | `0x801DC74C` |
| Machine code | 1,808 B | 1,808 B |
| Original stack | `0x140` | `0x140` |

The `0x5730` guest VMA shift agrees exactly between overlay and global. In Japan, low immediate of `addiu` is **negative** and must be sign-extended: the target is `0x801DC74C`, **not** `0x801EC74C`. Original function SHA-256: USA `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`, Japan `51a7ff3b9863ee6bcdae6ca0796934ecf91218ace5d39e48b8b1c892cf1084ae`.

Pinned original SGI IDO 5.3 compiled the artificial source diagnostic with exactly the original two HI16/LO16 relocations. Relocated separately to each region, it **fails native exactness in precisely the same way** in USA and Japan: **1,744 compiled bytes** versus 1,808 originals, first **13 consecutive** instructions exact, **31/436** raw positional words exact, frame 0x140. Original F300/E700 have 3/3 branch-local LUI; candidate has 1/1 hoisted LUI. This excludes a USA-specific address/overlay error as the explanation for the register discrepancy.

In separate synthetic guest-memory experiments, direct original MIPS and authentic IDO-compiled C were compared across **64 new valid page geometries**, varying positive 32-pixel-aligned widths/heights, page-grid dimensions, tile IDs and texture modes. **64/64 complete Gfx streams, 18,181/18,181 64-bit commands matched**. Together with the earlier independent 20-case suite, 84 controlled geometries and 23,485 Gfx commands have been compared. Not a running guest-frame capture or arbitrary-input equivalence proof.

## New register/stack pressure evidence

An additional portable, source-only IDO harness was independently executed, with **11 variants × 20 original-MIPS/IDO-MIPS scenarios = 220/220 passed graphics-stream comparisons**, zero mismatches and exactly the original two symbol relocations per build. Only the *diagnostic* source's register lifetimes were manipulated:

| Candidate shape | Code bytes | Stack | Raw positional words | F300/E700 LUI |
|---|---:|---:|---:|---:|
| Prior unsigned-cache diagnostic | 1744 | 320 | **31/436** | 1/1 |
| Hold clipped Y coordinates | 1744 | 328 | 23/436 | 1/1 |
| Hold masked Y coordinates | 1744 | 328 | 17/436 | 1/1 |
| Hold X coordinates | 1744 | 328 | 23/436 | 1/1 |
| Hold X and masked Y | 1744 | 344 | 17/436 | 1/1 |
| Precompute 1 rectangle command word | 1744 | 320 | 26/436 | 1/1 |
| Precompute 2 rectangle command words | 1744 | 328 | 23/436 | 1/1 |
| Precompute 3 rectangle command words | 1744 | 328 | 23/436 | 1/1 |
| Volatile branch-local F300 temporary | 1776 | 320 | 30/436 | 1/1 |
| Volatile branch-local E700 temporary | 1776 | 320 | 31/436 | 1/1 |
| Both volatile command temporaries | 1792 | 328 | 29/436 | 1/1 |

**Negative but discriminating conclusion:** keeping X/Y coordinates live, prepacking final rectangle fields, or inserting volatile command temporaries is insufficient to recover original `$fp=0x07054150`, saved/reused `$ra=0xE6000000`, and three branch-local F300/E700 constructions. IDO still hoists both constants once; some attempts perturb the frame to 0x148/0x158. These are *synthetic source diagnostics*, not plausible recovered original Konami declarations. None exceeds the previous 31 positional matches; every candidate remains `FAILED_NATIVE`.

## Exact source-only reproducibility kit

The complete ZIP is attached to the **same ChatGPT conversation** as `goemon-usa-file22-cross-region-codegen-study-20261122.zip`, SHA-256 `9b942b8dec6b3dac1c3d372077573cf56528be08d60fb568b2afceee44b45627`. It includes `register_pressure_study.py`, `dual_region_native_probe.py`, `verify_original_dual_region.py`, the original-MIPS interpreter, pinned 13,445-byte synthetic C diagnostic, IDO integration script, explanatory README and structured metadata. No user ROM, original ASM, native object, compiled game, proprietary compiler, raw trace or graphics assets are in the ZIP.

After **fresh extraction**, these tests were re-executed against the user's original authenticated USA/Japan 32 MiB decompressed images and pinned `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` IDO:

```bash
python3 verify_original_dual_region.py --usa /private/USA.decompressed.z64 --japan /private/JP.decompressed.z64

python3 dual_region_native_probe.py --usa /private/USA.decompressed.z64 --japan /private/JP.decompressed.z64 \
    --checkout /private/pinned/mnsg --deps /private/goemon-dependencies \
    --runtime /private/goemon-runtime-additions --output /private/NEW-dual-output

python3 register_pressure_study.py --usa /private/USA.decompressed.z64 \
    --checkout /private/pinned/mnsg --deps /private/goemon-dependencies \
    --runtime /private/goemon-runtime-additions --output /private/NEW-register-output
```

Each generated compiler object and executable trace stays in the user's private scratch directory, never in Git. These scripts fail closed on original hashes, pinned checkout and previously existing output directories. The accompanying GitHub research directory `../dual_region_20261122/` separately holds the core original-code cross-region verifier source.

## Acceptance boundary

**Not matching C.** No current USA1,965 accepted-source translation unit, whole original 33,554,432-byte G2 with *candidate*, 7,376 original ELF identities, 82,103 accepted-stage relocations, strict inventory or full `decomp.local_ci` was attempted, because all 11 native compiles remain mismatching. No canonical manifest/ASM ownership changed. USA stays **1,965 C / 84,648 bytes**. Continue with substantive texture-branch dataflow/aliasing and codegen source reconstruction, not repetitive type or volatile hints.