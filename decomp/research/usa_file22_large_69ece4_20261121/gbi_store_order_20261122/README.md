# File22 original-MIPS vs IDO GBI macro: observed graphics-store ordering

**22 November 2026 — RESEARCH_ONLY / FAILED_NATIVE.** The original renderer is `func_801CC0C4_69ECE4`, USA ROM `[0x69ECE4,0x69F3F4)` / guest `0x801CC0C4`, 1808 bytes. This is a *follow-up combining two independent research lines*: true IDO `gDPLoadTextureBlock` macro tests and exact guest memory-event ordering.

## New falsifiable result

Replacing the renderer's original mode-0 seven-command texture emission with Nintendo GBI `gDPLoadTextureBlock` and compiling with genuine pinned IDO5.3 `-O2` yields an 1808-byte candidate with **three** `F300` and **three** `E700` LUI operations, the same as the original. However, its frame is **0x90**, not the original **0x140**; it is **not matching C**. Its default mode-0 display list still contains exactly **275 64-bit commands**, all bit-for-bit identical to the original.

**The new external-write event oracle finds 50 out-of-order guest-word stores** in original mode 0: exactly **25 adjacent 32-bit store-pair reversals**, five reversed command records in each of five texture loads. The original stores the second 32-bit word before the first for the five middle Gfx commands in each seven-command texture setup, while this compiled GBI macro writes the first before the second. The first and last texture commands retain the original write order. This is a true difference in event ordering despite identical final graphics bytes.

The source-only probe also executes original formats 1, 2, and unsupported 3 in the same original-MIPS interpreter: **all their external loads, stores and final graphics are identical**. For original mode 0, input reads and final graphics are identical; the only observed external-event difference is the 25 adjacent write-order swaps. This does **not** rule out original Konami source using a GBI macro: compiler scheduling, other historical GBI header variants, or distinct wrappers might alter store order. It does prove that **the particular pinned GBI-header macro expansion under the tested C structure** is not fully observationally equivalent to the actual original renderer.

This is a complementary constraint, not an accepted function or a proof of original source text. The separate selectively `volatile` descriptor-load C variant (from `goemon-usa-file22-event-order-proof-20261122.zip`) has **113/113 exact external read+write streams** but hoists F300/E700 and fails original code size. Macro structure resolves the constant-load pattern but introduces write-order differences. Future source shapes must satisfy both constraints simultaneously.

## Reproduction

Extract this source-only ZIP alongside a pinned local original USA decompilation source and toolchain:

```bash
python3 verify_gbi_store_order.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-output-directory
```

The script checks pinned git commit and original ROM SHA-1, native-IDO compiles one new C source against the **original checkout's libultra header** (not distributed), validates precisely two relocations, executes original and IDO-generated guest MIPS, and checks the expected word-store swaps. It emits only JSON summaries; local `.o` files and logs stay in your private output directory. No ROM, extracted MIPS, proprietary header, linker object or compiler is contained in the source ZIP. The MIPS interpreter is research code, not a hardware emulator.

No current-USA accepted-stage whole-ROM G2, strict inventory or full CI was run because the candidate is nonmatching; previous published USA accepted total **1,965 / 84,648 bytes** remains unchanged.
