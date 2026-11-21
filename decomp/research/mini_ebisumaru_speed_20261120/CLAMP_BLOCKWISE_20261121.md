# 21 November 2026 — USA main movement clamp: original instruction blocks recovered

**RESEARCH_ONLY / FAILED_NATIVE. Not production matching C.** Target original USA `func_801CD310_589220` at ROM `0x589220`, VMA `0x801CD310`, 4,320 original bytes. Research source SHA-256 `f9cb237b685b4177f1dcba787392bf74476ca6274092f145756bc77bfa65d2f1`, native compiler original IDO 5.3 (`-O2 -mips2 -G 0 -non_shared`), pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

## Substantive original-address instruction improvements

Starting with prior `clamp_frame232_switch_4332.c`, the research patch (stored alongside this report) changes only native C declaration order and reads the switch discriminator directly from the original task field, rather than storing it in a temporary later overwritten by every switch case. The compiled ELF still has a **232-byte stack frame**, **4,332-byte genuine FUNC** (12 B over original), **33 original calls in original order**, **nine native inline `sqrt.s`**, 101 text relocations with original types/counts and 18 original switch destinations. No MIPS patch, padded-symbol trick or compiler change.

Read-only original MIPS vs candidate *same original relative offsets* (never shift matches or count padding):

- `+0x000` to `+0x03B` — **15/15 complete instruction words equal**.
- `+0x050` to `+0x08F` — **13/13 non-relocation words equal**; all **3/3** relocation sites at original offset, with matching type and symbol.
- `+0x090` to `+0x1B3` — **55/55 non-relocation words equal** across a **292-byte** contiguous region; all **18/18 relocation sites** are at the original offsets. **16/18** site type-and-symbol pairs match; the two exceptional HI16/LO16 sites reference compiler-owned `.rodata` rather than original `jtbl_8020A85C_5C676C`. They are NOT linked-byte matches.
- Breakdown: switch dispatch `+0x090..+0x0BB` **9/9**, switch bodies `+0x0BC..+0x193` **40/40**, two trig calls at `+0x194..+0x1B3` **6/6** non-relocation words exactly.

The original compiler register and slot pattern is now reproduced for: initial `sh v0,sp+0xE6`; switch `lhu t3` and arithmetic `t4`; angle `sp+0x6E` and second angle `sp+0x6C`; case float `sp+0x5C`; trig float `sp+0x64`. Global same-offset non-relocation instruction matches **66/912 -> 93/912**, a **27-word** increase with 819 other comparable offsets still different. Of original function's complete 101 relocations, **99/101 types and target symbols match in order**, but only **20/101** type/symbol/offset triples match across the *entire* function, so this is NOT original ELF relocation equality.

## Next mismatching block and failed variants

The first substantive non-relocation difference after the recovered switch/trig region occurs at `+0x1B4`: original initializes FP zero in `$f14` and loads the task context via `$v1`; the candidate loads the context via `$a0`, retains it via `$a1`, and initializes a different FP register later. The first actual raw-code difference earlier at `+0x3C` is a normal JAL relocation; the `+0x44` branch to the function epilogue also differs because the entire function remains 12 B longer. Fifteen bounded native IDO C variants, including changing the zero-initializer location and flag variable scope, did not extend the next block's original-address match. Do not fabricate progress at this block.

## 3D and 2D clamp blocks as distinct research fixtures

Original function's nine `sqrt.s` occurrences preserved in both original and C candidate. The 5th is the three-component movement clamp at original relative `+0x9A8` (PC `0x801CDCB8`); current candidate 5th sqrt at `+0x9BC` (**+20 B drift**). The 7th is the horizontal x/z clamp at original `+0xDDC` (PC `0x801CE0EC`); candidate seventh sqrt at `+0xDF8` (**+28 B drift**). They are not matching native blocks. Original MIPS arithmetic shows the 3D norm uses `(x*x+y*y)+z*z` before scaling three components when the magnitude exceeds the movement cap, and 2D norm uses `x*x+z*z` before scaling x/z; the surrounding original 2D path separately zeroes y. Precise game-mode conditions, aliasing, and gameplay are not proved.

A portable **analytical-only** C fixture for these two formulas was host-compiled with GCC AddressSanitizer and UndefinedBehaviorSanitizer; 5,000 deterministic finite/nonnegative-cap paired property cases PASS. These fixtures are not original-address source and do not count toward matching C.

## Reproduction and formal gate state

The 13-file `GOEMON_CLAMP_BLOCKWISE_20261121.zip` conversation artifact includes full current and comparison C sources, a fail-closed original-ROM/IDA ELF structural comparator, native replay script, source/trial CSV, 3D/2D arithmetic fixtures and hashes. Replayed from freshly extracted ZIP with native IDO 5.3: PASS for reported structural facts. Pristine expanded original-USA 32 MiB ROM remains **33,554,432/33,554,432** byte identical, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. **No clamp C was linked into this original ROM**; no candidate full-ROM or complete ELF equality was claimed. Do not publish original ROM, disassembly, generated objects, compiler or original game assets.

Original-address full-function match **FAIL** (4,332 B vs 4,320 B and divergent later instructions). Current combined `python3 -m decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci` and gameplay/emulator tests **NOT RUN**. The container cannot resolve github.com for a full current local decomp checkout; GitHub connector read/write is separate and is not a local checkout. **No accepted C promotion**, current verified USA inventory **1,956 matching C / 83,940 instruction bytes / 5,407 ASM**. All research must remain draft until current combined gates actually pass.

**Next focused instruction task:** rebuild the context flag branch beginning at `+0x1B4`, with C alias and FPU register lifetimes derived from original block input/output, not arbitrary total-size matching. Keep the stable 232-frame switch region and independently track 3D/2D sqrt drift.
