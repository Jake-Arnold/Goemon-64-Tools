# Original USA/Japan file22 large renderer: dual-region native IDO and structural source study

**22 November 2026. Status: RESEARCH_ONLY / FAILED_NATIVE / NO_PROMOTION.** This targets the **1,808-byte** `func_801CC0C4_69ECE4` in USA (`0x69ECE4`, guest `0x801CC0C4`), not the 60-byte helper. All tests use original user-owned ROM images, the pinned `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, SGI IDO 5.3 `-O2 -mips2`, original relocations and isolated **synthetic** guest RAM. The C candidate contains artificial stack storage and is **not known Konami source**.

## New independent cross-region original-code identity

The original USA file22 code section is ROM `[0x69E080,0x69F400)`, with load address `0x801CB460`. Japan file22 code is `[0x6A2B70,0x6A3EF0)`, with load address `0x801D0B90`. Both original code sections have exactly `4,992` bytes; both large functions start at relative offset `+0xC64` and have exactly `1,808` bytes (452 original MIPS words).

The **authentic 32 MiB decompressed USA** SHA-1 is `6ea0ed71032ce08fc2745f412d84936382197494` (function SHA-256 `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`). The **authentic 32 MiB decompressed Japan** SHA-1 is `6f8745fecc3a5e7d4918c7a73353eb0726116ded` (function SHA-256 `51a7ff3b9863ee6bcdae6ca0796934ecf91218ace5d39e48b8b1c892cf1084ae`).

**450 / 452 original machine words are byte-for-byte identical** across the regions. The **only** differences are source-function-relative offsets `+0x40` and `+0x4C`, the original symbol-load `lui`/signed `addiu` pair which materializes the display-list cursor:

| | USA | Japan |
|---|---|---|
| Large function ROM | `0x69ECE4` | `0x6A37D4` |
| Guest VMA | `0x801CC0C4` | `0x801D17F4` |
| Cursor address | `0x801D701C` | **`0x801DC74C`** |
| Original stack | `0x140` | `0x140` |
| F300/E700 branch-local LUI counts | 3 / 3 | 3 / 3 |

**Signed-immediate caution:** Japan's `lui` upper immediate is `0x801E`, but the subsequent `addiu` low immediate is signed and negative. The resulting target is **0x801DC74C**, not `0x801EC74C`. Both function and global cursor VMAs differ by precisely **0x5730**, the overlay load-address delta. The remainder of the function (continuous suffix of **1,728 bytes**) is exactly identical in the two original binaries.

The dual-region verifier strictly authenticates both complete ROM hashes and original function slice hashes, insists on the two expected instruction differences only, checks that the two original address sequences resolve to their region-specific guest targets, and recompiles the diagnostic C using the authentic IDO compiler. It requires **precisely one original `R_MIPS_HI16`/`R_MIPS_LO16` pair**, relocates the candidate object separately to USA and Japan, then compares original instructions in **both** regions. It is an isolated candidate comparator, **not a full-ROM/ELF G2**.

The current source diagnostic is still **1,744 bytes** (original 1,808) with **13 consecutive matching entry words, 31/436 original positional words, one F300 and one E700 LUI**, in **each** region; neither region is native-exact. This confirms that compiler mismatch isn't caused by a USA-only ROM/address mapping. The artificial volatile stack pads must never be treated as recovered original source.

## More actual native compiled C tests

The dual-region test also executes authentic USA original MIPS and its separately **IDO-compiled** diagnostic C across **64 additional deterministic valid page layouts**, varying widths, heights, page grids, page IDs and formats `0..3`. **64/64 complete Gfx streams match, 18,181/18,181 64-bit command records identical, zero mismatches.** Inputs use positive, 32-pixel-aligned dimensions and page IDs bounded to the original 80-entry tilemap. These tests are not exhaustive and do not cover all possible negative or malformed descriptors. Combined with the prior 20 cases, **84 synthetic cases / 23,485 Gfx entries** have been checked against authentic MIPS. The original source still has unexecuted exceptional paths beyond the prior four division guards.

Three genuinely different C-shape diagnostics were also compiled with IDO 5.3 and checked against the original-USA MIPS for all original 20 scenarios:

| C hypothesis | Candidate text | Original-position words | Entry prefix | F300/E700 | Rendering |
|---|---:|---:|---:|---:|---|
| Commute page-map summands | 1,744 B | 31 / 436 | 13 | 1 / 1 | 20/20 |
| Break lookup into source-sequenced locals | 1,744 B | 19 / 436 | 0 | 1 / 1 | 20/20 |
| Three independent texture-mode `if` branches | 1,744 B | 23 / 436 | 0 | 1 / 1 | 20/20 |
| Prior unsigned-cache diagnostic baseline | 1,744 B | **31 / 436** | **13** | 1 / 1 | 20/20 |
| Original ROM | **1,808 B** | **452 / 452** | 452 | **3 / 3** | Reference |

None improves IDO codegen; all require exactly the original two global relocations. The independent-if diagnostic additionally emitted legitimate MIPS `bnel`; the research interpreter was extended to implement its branch-likely semantics correctly before treating **20/20** as valid. Earlier runs that failed with `NotImplementedError` were interpreter gaps, **not** behavioural failures. A separate volatile-row probe emitted code the old interpreter could not execute and was not counted as a passed semantic comparison.

The direct blockers remain IDO register allocation (`$fp` vs `$ra`, long-lived clipping coordinates), branch-local F300/E700 construction (three in original, one each in candidate), and original 0x140 register/stack liveness. The source-structured arithmetic and branch attempts tested here **do not** solve those issues. Repeating spelling-only changes is unlikely to advance the original register map. The dual-region original is now a strict independent anchor for future hypotheses.

## Reproduce without redistributing ROMs or original object code

Unpack this **source-only** ZIP in an empty directory. Required user-owned inputs: the authentic original USA and Japanese **decompressed** 32 MiB ROM images, a pinned already installed `mnsg` original checkout, restored `goemon-dependencies` and `goemon-runtime-additions`. You can use `GOEMON_BUILD_ENVIRONMENT.md` to decompress the supplied original JP retail image, which is distinct from the normalized 16 MiB `.z64`.

```bash
python3 dual_region_native_probe.py \
  --usa /private/usa/baserom.decompressed.z64 \
  --japan /private/japan/baserom.decompressed.z64 \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-dual-output

python3 structural_hypotheses.py \
  --usa /private/usa/baserom.decompressed.z64 \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-structural-output
```

Both scripts refuse pre-existing output paths, hash-check their inputs and create scratch ELF MIPS objects **only in the user-selected private scratch directories**. They report sanitized JSON metadata. The ZIP includes source scripts and synthetic-research C only, **no original ROM bytes, original assembly/instruction dump, proprietary compiler, compiled MIPS object, textures, game screenshot or raw gameplay memory**.

### Acceptance boundary

**NOT** original IDO matching C; no accepted implementation was touched, no current combined USA1965 source integration, complete 32 MiB G2, 7,376 original ELF identities, accepted-stage 82,103 semantic relocation comparisons, strict inventory, or full `python3 -m decomp.local_ci` was run. USA published baseline remains **1,965 accepted C functions / 84,648 bytes**. This is a reproducible research checkpoint under decomp draft PR #161 and must remain draft until every gate passes.

For the cross-region original-identity proof alone (does not invoke IDO):

```bash
python3 verify_original_dual_region.py \
  --usa /private/usa/baserom.decompressed.z64 \
  --japan /private/japan/baserom.decompressed.z64
```

This standalone verifier is also committed as plain source in the Goemon-64-Tools research PR. It checks the original-image SHA-1s, function SHA-256s, the exact two differing original instruction offsets, and the sign-extended cursor targets; it does **not** claim any matching C.
