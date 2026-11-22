# USA file22 renderer — compiler source-shape and private stack reconstruction

22 November 2026. **RESEARCH_ONLY / FAILED_NATIVE**, no accepted-C promotion.

Target: USA `func_801CC0C4_69ECE4`, ROM `[0x69ECE4, 0x69F3F4)`, guest `[0x801CC0C4, 0x801CC7D4)`. Original size 1,808 bytes (452 MIPS instructions), stack frame 0x140, USA expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, function SHA-256 `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`.

## Direct native-IDO progress

In the previous corrected original-IDO 5.3 C, the function was 1,776 bytes, stack 0x50, and 39/40 `lui` constants (one extra `FD50` load missing). A bounded, reproducible C source-structure experiment with branch-local volatile one-element arrays produced **simultaneously**:

- **Exactly 1,808 native-compiled bytes and 0x140 original stack frame**.
- **Exactly the complete 40-entry original `lui` immediate multiset** (all counts; no missing or extraneous constants), including *two* `FD50` loads. Both original HI16/LO16 global symbolic relocations remain intact.
- **12 consecutive original entry instruction words**. Whole function still contains many nonmatching words and cannot be promoted.
- **113/113 complete observable-memory-event executions**: 90,910 matching external reads, 100,869 matching external writes and 33,623 identical Gfx commands. Four division guards trigger; ten memory-out-of-range cases are excluded. Tested actual IDO-produced MIPS against the original instructions, not merely a host C model.

Next, the *original* row-pixel state was shown by guest stack tracing to have 9 dynamic stores (once per row) and 80 dynamic loads (once per rendered tile). Our initial m2c model kept this state in a register, while a naïve volatile declaration loaded it **twice per tile** because two divisions use it. New `diagnostic_rowpixel_once_1808.c` declares the stack value volatile but snapshots it once before both divisions. This reproduces exactly **80 reads and 9 writes for that coordinate**, while retaining **1,808 compiled bytes, 0x140 frame, all 40 LUI loads, all 113 external memory events**, and improves positional original word matches **19 → 32 of 452**. The opcode-and-immediate-order alignment is 306/452 in this variant versus 307/452 in the first full-constants diagnostic; alignment deliberately ignores register operands and is not proof of native equality.

A third variant `diagnostic_functional_stack_1840.c` forces row counter, cached tile ID and row-pixel state to behave like original stack variables. In the default mode-2 trial, original private-stack accesses were **630 loads and 89 stores**. This candidate produces **635 loads and 94 stores**, of which **5 reads and 5 writes** belong exclusively to the *artificial* branch-local scratch array, leaving **630 / 89 functional stack events**. This **does not prove matching internal values or positions**. It generates 1,840 bytes, has one missing `FD50` LUI and is therefore *less* native-match-like in other dimensions. It passes all four default-mode external read/write/graphics tests.

### Why all candidates remain research-only

- The branch-local volatile one-element arrays are **artificial source diagnostics**; they are not established original Konami C declarations. Their stack loads/stores are invisible outside this function but differ from the original instruction stream.
- Although gross length, frame, constants and external-memory events now match **simultaneously** for one candidate, saved-register assignments and the actual 452 individual original machine instructions do not.
- The first `diagnostic_full_constants_1808.c` has **19** identical positional instruction words. The row-pixel revision has **32**, not 452. Original `$fp=0x07054150` and `$ra=0xE6000000` are still not reproduced.
- Source-only verifiers operate on synthetic big-endian guest memory with a hand-written interpreter. This is not a real hardware frame trace, compiler-source attribution, exhaustive test or whole-ROM G2 proof.
- Do **not** replace original assembly; no accepted-C manifest change, region-wide native ROM byte identity, ELF identity/semantic relocation inventory, or full local CI was run for these nonmatching candidates. Published USA accepted C remains 1,965 / 84,648 original bytes at the research baseline; re-read live counts before any eventual promotion.

## Reproduce

With the user's authenticated original expanded USA ROM in the pinned upstream `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` checkout, original IDO 5.3, `readelf`, and restored MIPS runtime, run from the extracted source-only kit:

```bash
python3 verify_native_diagnostics.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-unused-output-directory
```

This rejects wrong ROMs, source commits, compiler output sizes, stack frame sizes, `lui` multisets, relocation counts and unexpected instruction changes. It runs all four basic modes for every candidate and **113 full external-memory cases** for the best 1,808-byte row-pixel source. It reports the original and candidate private-stack read/write histogram and sanitised per-case metadata in the chosen local output directory. Generated objects, original MIPS, ROM bytes and test memory traces remain local and are **not included in this archive or GitHub**.
