# USA `file_11` third adjacent matching-C sweep — 16 November 2026

## Verification result

No original-USA function was presumed to be matching C based only on adjacency. The 906 original `file_11` function boundaries were re-indexed from the pinned upstream Splat source and compared with the currently promoted 50 `file_11` functions and **189 previously verified, unpromoted research functions**. The remaining functions were screened for C-shaped state updates, float operations, predicates, wrappers and inter-function adjacency.

**Ten additional C functions match exactly at their original USA addresses under IDO 5.3, covering 488 original MIPS instruction bytes.** Every match was obtained through the authenticated original compiler/linker and a byte-for-byte instruction comparison. All ten belong to **nine complete contiguous C islands** that also match as combined native C translation units: **27 original functions / 984 instruction bytes, 9/9 exact**. Seventeen of those grouped functions were already identified in earlier research or formally promoted; only ten are new.

Original input authenticity:

- Original USA decompressed ROM: **33,554,432 bytes**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original generated USA `asm/usa/587370.s` containing 906 positive-size `file_11` functions: SHA-256 `e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b`.
- Pinned upstream revision: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Compiler: original IDO 5.3, `-O2 -mips2 -G0`, linked with original MIPS VMAs; final compilation section padding is excluded from original function extents.

## New matched C functions

| Original USA ROM offset | Size | Observed native C behaviour |
|---|---:|---|
| `0x59E860` | 48 | Clears an indirect actor byte and invokes the same resource/event helper with two constant IDs (`526`, `587`) |
| `0x59EB80` | 60 | Invokes an actor handler with event `19`, then resets two actor float fields to `1.0` and `0.0` |
| `0x59EEB4` | 60 | Clears a nested actor halfword and two actor floats, clears bit 0 of an actor flag, invokes a state helper |
| `0x59EF18` | 52 | Resets multiple actor floats and indirect fields, sets an actor mode byte to `20` |
| `0x59F068` | 32 | Sets actor action byte to `60` and updates two actor flag bits |
| `0x5A0FA0` | 48 | Resets four actor floats, sets an indirect halfword to `1`, clears a flag bit |
| `0x5A3CF8` | 48 | Predicate: actor character byte equals `1` and indirect state halfword equals `0xFFFF` |
| `0x5B0568` | 48 | Calls one actor handler, then another with a zero secondary argument |
| `0x5B436C` | 44 | Calls a first handler, then a second handler with a pointer to a global object |
| `0x5B7150` | 48 | Sets a bit in a global object's halfword and calls a follow-up handler |
| **Total** | **488** | **10/10 original-VMA native C matches** |

The field names describe byte offsets and instruction-level effects. They do not establish gameplay semantics beyond those operations. This batch adds meaningful character/actor state logic rather than merely returning empty callbacks.

## Nine matching adjacent C islands

| Contiguous USA ROM range | Function count | Newly found | Exact C bytes |
|---|---:|---:|---:|
| `0x59E860–0x59E8B0` | 2 | 1 | 80 |
| `0x59EB60–0x59EBFC` | 4 | 1 | 156 |
| `0x59EEB4–0x59EF8C` | 6 | 2 | 216 |
| `0x59F044–0x59F088` | 2 | 1 | 68 |
| `0x5A0F94–0x5A0FD0` | 2 | 1 | 60 |
| `0x5A3CB0–0x5A3D28` | 3 | 1 | 120 |
| `0x5B04F4–0x5B0598` | 4 | 1 | 164 |
| `0x5B436C–0x5B43A4` | 2 | 1 | 56 |
| `0x5B7140–0x5B7180` | 2 | 1 | 64 |
| **Total** | **27** | **10** | **984** |

The six-function `0x59EEB4–0x59EF8C` block is the strongest extension: it joins a newly matched 60-byte actor reset, two previously proven 20-byte float-reset functions, a newly matched 52-byte reset, and two previously proven 32-byte wrappers. The entire **216-byte block** matches the original machine instructions in one combined C object. No assembly is elided inside the group.

The three-function `0x5A3CB0–0x5A3D28` group likewise extends character/actor predicates; the four-function `0x5B04F4–0x5B0598` group extends fixed-event wrappers with a two-handler callback. Two helper functions at `0x5B436C–0x5B43A4` form a 56-byte group, reusing a previously identified empty callback. This is useful for mixed-C/ASM linker integration because fewer, larger original-contiguous chunks need size-locking.

## Reproduction

The following research artifacts contain source declarations and SHA-256s, but **no original game code bytes**:

- `decomp/research/file11_adjacent_wave3_sources.json` — ten new C source bodies, pinned original offsets, original byte hashes, and nine combined contiguous C source bodies.
- `decomp/research/file11_adjacent_wave3_probe.py` — strict ROM/upstream Splat authentication; verifies previous 77/68/44 candidate identity, prevents duplicate production/research claims, checks all original function boundaries/VMAs and exact original instruction bytes; compiles all ten functions and nine grouped source units with IDO.
- `decomp/results/file11_adjacent_wave3_native_proof_20261116.json` — generated original-VMAs, original/source/compiled SHA-256, and comparison results.
- `tests/test_decomp_file11_adjacent_wave3.py` — 18 ROM-free contract/regression tests, including duplicate candidate, broken adjacency, invalid compiler source and symbol-binding mutations.

Run the new original-address probe using its module docstring CLI and the user-supplied original ROM, pinned upstream Splat source and compiler archives. A repeat run produced the same result: **10/10 isolated exact, 9/9 contiguous-group exact**. All **18/18 focused ROM-free regression tests passed**.

## Rejected or incomplete targets

Additional neighbouring candidates were examined rather than assumed to match. The 64-byte state-changing function at `0x59EE74`, the 52-byte global/event wrapper at `0x5B4338`, the 40-byte float calculation at `0x5A3C88`, and the 48-byte float update at `0x5B3050` have **not** matched native IDO exactly. For `0x59EE74`, the closest candidate reproduced 14 of 16 instruction words but differs in instruction scheduling/register materialisation; it remains assembly. Similarly, no unverified candidate was included merely because it sits beside a verified island.

## Promotion restrictions

The previous research counts were **77 + 68 + 44 = 189** additional original-address native-matching C functions. This pass adds ten disjoint new functions, making **199 unpromoted candidates / 7,000 matching MIPS bytes** in total. Combined with the formal production **210 functions / 13,336 bytes**, a hypothetical fully promoted total is **409 functions / 20,336 bytes**. These are *not* production counts.

**No full 409-function central `decomp.verify` G2, complete 32 MiB mixed-ROM rebuild, 8,825-relocation provenance check or generated inventory has run.** The canonical manifest, `decomp/results/combined.json`, and `decomp/results/inventory.json` remain **210 matching-C functions and 7,153 assembly entries**. The older uploaded repository ZIP predates the merged 210-function promotion and its two known source-fingerprint failures must not be represented as a passing full local CI. The 180-byte original character selector and full Japanese ROM pipeline remain separate unresolved research.

Next: promote a reviewable subset starting with the 216-byte six-function block and adjacent 164-byte wrapper group in a separately versioned mixed C/ASM adapter, then run the complete central native G2 and inventory before changing published counts.
