# USA file22: branch-local constant lifetimes and original-order GBI graphics stores

22 November 2026. **RESEARCH_ONLY / FAILED_NATIVE**. Target original USA `func_801CC0C4_69ECE4`, decompressed ROM `[0x69ECE4,0x69F3F4)`, guest `[0x801CC0C4,0x801CC7D4)`; 1,808 bytes / 452 original MIPS instructions. User-owned, authenticated original USA 32 MiB ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`; target function SHA-256: `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`. Pinned upstream original `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original IDO 5.3 `-O2 -mips2`, precisely two expected HI16/LO16 global relocations.

## New falsifiable advances

**(1) Correct complete memory-write order without losing three texture-branch load sites.** Nintendo's original `gDPLoadTextureBlock` command expansion emits the right final graphics but writes the two words in the wrong order for 25 commands in the USA original mode-0 render. Explicit, source-level reverse-word writes fix three of the five command types; IDO still reschedules `F510` and `F300`. Qualifying **only those two Gfx stores** as `volatile` preserves their required order while retaining the original *three* `F300` LUI operations and *three* `E700` LUI operations. The resulting original IDO binary is 1,792 bytes and has **exact external read/write/graphics event sequences for all 113 completed tests** (90,910 reads, 100,869 writes, 33,623 Gfx entries). Includes 29 aliasing tests in which the generated display list overwrites future page/texture input data. Four original and compiled division error guards trigger. Ten cases exceed synthetic memory bounds in both runs and are excluded, never counted as passes. Removing **all artificial stack storage** retains this result (native frame 0x50).

**(2) Exact original load frequencies for five major graphics constants.** In the unpadded C renderer, introduce local `u32 e6_constant = 0xE6000000` and use it in all three texture branches. IDO moves `E600` to a single early load and instead loads `F550` separately in modes 1 and 2. Introduce `u32 tile_word = 0x07054150` and use it in all three texture branches: this removes the extra `0705` load. The resulting 1,776-byte native function has exactly the original per-constant LUI counts: `0705:1`, `E600:1`, `F550:2`, `F300:3`, `E700:3`. It retains **113/113 complete external event streams exact**.

**(3) The LUI immediate multiset is now 39/40 original occurrences, with no extras.** A single source-level named signed `0xFFFF` loop bound, shared by the outer and inner bounds tests, eliminates the compiler's four redundant `lui 0x0001` instructions (replaced by a single `ori` immediate pattern). The final 1,776-byte compiled MIPS source has **39 total LUI instructions; every one corresponds to an original LUI immediate**, with exactly one original `FD50` load still missing (one candidate load instead of the original two). The exact original frequency of *all other 21 distinct LUI immediate types* is matched. Opcode-and-immediate ordered alignment increases to **309/452**; raw positional matches remain **17/444**. This count-multiset proof is not an instruction-order or register-assignment proof; in particular, original `$fp` holds `0x07054150` and `$ra` holds `0xE6000000`, while the candidate uses other saved registers.

**(4) Unresolved original stack: only 18 distinct directly `$sp`-relative slots are referenced.** An authenticated original function scan enumerates the ten saved-register words (`sp+0x08..0x2C`) and eight observed functional slots (`sp+0x34,0xE0,0xE4,0xE8,0xF0,0xF8,0x100,0x138`). No other direct SP-relative memory operands occur in the original 452 instructions. This does not prove unreferenced frame bytes were unused: indirect register-based stack accesses or compiler-internal reservation remain possible. The original frame is **0x140**, versus **0x50** in the natural, unpadded candidate. The meaning of the large layout gaps cannot be inferred from raw offsets alone; artificial padding is not matching C.

## Bounded hypotheses rejected

- Unqualified reversed stores are rescheduled by IDO for `F510` and `F300` (20 out-of-order external word-store events per default mode-0 render).
- Volatile-qualifying **all five** command records changes a different command pair's ordering; only the specific `F510` and `F300` store qualification passes.
- Volatile locals for original row/cache alter observable execution; volatile clipped coords lose the correct branch-local `F300/E700` count.
- Direct `FD50` volatile stores, typed Gfx stores, bitfield expressions, or replacing first commands by the original `gDPSetTextureImage` macro all retain the candidate's hoisted single `FD50` load. Those variations do not solve remaining native register allocation.
- Named-local declaration order, `register` hints and `const` qualifiers for the two long-lived constants compile to identical code; a `volatile` tile constant introduces extra stack effects and fails the complete event-order oracle in two tested formats.

## Reproduction

On an x86_64 Linux host with the user's original authenticated USA ROM, pinned `mnsg` source and restored IDO/MIPS toolchains, extract this **source-only** kit and run:

```bash
python3 verify_constant_lifetimes.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-output-directory
```

This validates both ROM SHA identities, compiler commit and flags, ELF32 MIPS generated text, exactly two relocations, the LUI multisets and source candidate sizes, and runs the complete original-MIPS-versus-IDO-compiled-MIPS synthetic-memory-event oracle. The macro-only source is retained as a **negative control** and must fail mode-0 write-order equality in precisely 50 event positions (25 swapped pairs). The best dual-named-and-bound C source must pass all 113 event-order scenarios. The first two improved sources receive four-mode exact-event checks by default and passed independent 113-case runs in the originating experiments; run `--full-all` to rerun all three extended suites (longer). Local objects, raw memory traces, generated binaries and original assets remain outside this ZIP and the repo.

## Limitations and publication

The research interpreter is not an N64 emulator, and the 113 successful cases do not establish full C equivalence for every possible input. The best code is **1776 vs 1808 bytes**, **0x50 vs 0x140 stack**, uses different saved registers and is not original machine-code exact. No current accepted-USA1965 G2, complete ELF/relocation gate, strict inventory or full `decomp.local_ci` has been performed on this candidate. **Do not promote or remove the original assembly**. Published accepted USA remains **1,965 functions / 84,648 bytes** until independently verified in the current canonical branch.

The kit contains only user-independent authored source code and sanitized metadata; it deliberately excludes ROMs, extracted original assembly, original instruction dumps, copyrighted assets, proprietary tools, binary outputs, saves and raw guest memory captures.
