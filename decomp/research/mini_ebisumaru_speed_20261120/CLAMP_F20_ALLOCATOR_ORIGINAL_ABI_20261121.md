# Deep clamp ABI / compiler floating-zero investigation — 21 November 2026

**Research only / FAILED_NATIVE.** Original USA `func_801CD310_589220`, ROM offset `0x589220`, guest `0x801CD310`, 4,320 native bytes, 232-byte frame. Original instruction proof from SHA-1-authenticated expanded USA ROM `6ea0ed71032ce08fc2745f412d84936382197494` and original SGI IDO 5.3. No original ASM/ROM/ELF/objects or proprietary tools committed.

## Major new result: a reproducible *cause* of the extra f20 save

The whole recovered C has 33 direct `M2C_FIELD(arg0, f32*,off)=0.0f` writes. Original C uses scratch floating-point zeros repeatedly; the recovered scaffold reuses one $f20 constant across 29 intervening JALs and saves it at function-relative +0x04, unlike the original `mtc1 zero,$f0` at that position.

A **diagnostic only** source rewrite of later float-zero task-field stores into bitwise-equivalent integer-zero stores reveals a distinct IDO allocation threshold:

| Diagnostic change to original f32 stores | IDO at +0x04 | FUNC / frame | Original-position words / exact relocs |
| --- | --- | --- | --- |
| **10** field stores | still `sdc1 f20,sp+0x10` | 4,292/232 B | 9 / 1 |
| **11** field stores | **`mtc1 zero,f0`** | **4,456/224 B** | **62 / 20** |
| **30** field stores | **`mtc1 zero,f0`** | **4,400/224 B** | **62 / 21** |

Eleven single-removal tests from a passing 11-field subset all restore saved f20 when reduced to ten. Independent 11-field sets spanning early, middle, late and mixed fields also remove it, while a 10-field subset does not. This is a bounded compiler codegen finding, **not a valid C reconstruction**: it generates wrong integer store opcodes instead of original floating-point `swc1`, changes stack frame, and may alter pointer aliasing. Do not promote the 62-word score.

Source-level forwarding of later zeros from an adjacent earlier **float field**, with correct f32 store lvalues, lowers explicit `0.0f` literals from 60 to 39 but IDO CSE restores the unchanged 4,292-byte/232-byte/f20-save output. Marking the field read volatile removes the save yet introduces actual `lwc1` reloads, creates a 4,536-byte/224-frame nonmatch and does **not** reproduce the original prologue. A prior comparator's `-8192` frame estimate is incorrect for that volatile variant: its stack allocation moved from instruction +0x00 to +0x04; actual 224 B.

## Additional valid source-level improvement: switch merge load and store schedule

The five-first-angle/one-second-angle C previously had `sh v0,sp+0x6C` immediately before `lhu a0,sp+0x6E` at the merge. A semantically valid source-level read into an existing local **before** writing the second angle now compiles as `lhu a0,sp+0x6E` followed by `sh v0,sp+0x6C`. It retains **five case-local first-angle `sh`**, one merge second-angle `sh`, both original stack slots and a **232-byte frame**. The pair remains +4 bytes late, the original uses `a1` rather than `v0`, and native result remains **4,292/4,320 bytes, 9/888 same-offset nonrelocated instructions, 1/101 exact relocation triples**.

A stronger *shift-aware* comparison (omitting both sides' relocation-bearing words) shows why the early C is structurally close: original window +0x50..+0x8F matches **13/13 words at candidate +4** (0/10 same offset); original switch window +0x90..+0x1B3 matches **43/55 baseline**, **44/55 load-first** at +4 (0/46 same offset). **Shifted matches are diagnostics only, not native correctness or offset-based promotion.**

## Original cross-function / data references actually inspected

- Caller `func_801CC4C0_5883D0`: original clamp call at ROM `0x5886F4`, `a2` from its stack +0x90 and `a1` from stack +0x8C in the JAL delay slot. Preserve their raw ABI values.
- Actual cosine `func_80003EA0_4AA0` at ROM `0x4AA0`, size 144 bytes, masks its sole used argument `a0 & 0x3FF`, returns table-based f32 in `f0`, and stores `a0` in the call-home stack area. **No MIPS instruction reads `a1`**; 12 original ROM-indexed cosine checks differ by at most 4.9e-8 from the mathematical cosine. Its sibling table helper `func_80003E10_4A10` supplies other trig operations.
- `func_801CE3F0_58A300`: begins with **`mtc1 zero,$f14`** at original +0x04 and three original `swc1` task zero stores +0x74/+0x78/+0x7C; accesses global pointer `D_8020CA2C_5C893C` with f32 +0xC.
- Context gate reads **known** global `D_801FC60C_5B851C` and its referent +0x20; task+0x5C points to changing context. These are pre-existing address references, not new fixed-RAM discoveries.
- Original switch `jtbl_8020A85C_5C676C`: 18 entries/five destination groups. Original case-local first-angle halfword stack +0x6E, second-angle merged from a1 to +0x6C at +0x198, trig calls +0x19C/+0x1A4, return saved to sp+0x64 at +0x1B0.
- **Diagnostic ABI variant, invalid as original-C evidence:** declaring the cosine function with an unspecified argument list and passing a second dummy angle can persuade IDO to use `a1` in the merge, but this is **not supported by the actual callee**, and both JAL PCs remain late. Do not adopt a fake 2-argument API.

## Tests executed

- Exact pristine pinned USA 32MiB ROM rebuild: **33,554,432/33,554,432 bytes identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; not an integrated experimental C ROM.
- Original MIPS instruction/stack/caller/callee signatures verified, read-only against the private original ROM.
- Native IDO 5.3 builds of 8 representative complete-C sources freshly replayed: all compile, every one still **FAILED_NATIVE**. Earlier source variants and 11 threshold-subset checks recorded in the companion sanitized JSON.
- Source archive clean extraction + SHA256SUMS audit + native replay **PASS**; four original-ROM failure-mode unit tests **PASS**; GCC and Clang ASan+UBSan each **65,536** bounded switch/angle test cases **PASS**.
- Combined canonical `decomp.verify`, strict inventory, full `decomp.local_ci`, candidate-linked ROM integration, gameplay **NOT RUN**; no original-address native match.

**Complete reproducible C, scripts, source patches and comparative JSON:** attached conversation source-only `GOEMON_CLAMP_DEEP_FP20_ABI_20261121.zip` SHA-256 `afc7ec7c2e3bd3842beba2a10eb7f8b99bb841de970e39e86c27be6326b486ed`. Standalone native replay:

```sh
python3 replay.py --upstream PINNED_UPSTREAM --rom PRIVATE_EXPANDED_USA --elf ORIGINAL_USA_ELF --built-rom PRISTINE_BUILD --host
python3 test_original_abi.py --rom PRIVATE_EXPANDED_USA
```

Restore the documented pinned Python/IDO/MIPS env before calling; the ZIP contains no original ROM/ASM/ELF/binary/toolchain. Source patch below applies to previously committed original full C `case_store_first_scalar_second_20261121.c.gz`.

**Next:** restore original short-lived *typed* float-zero definitions across helper calls and regenerate early prologue naturally, preserving `swc1` types and 232-byte frame. Treat the threshold and fake ABI as diagnostic discriminants only. Earlier historical 157/925 original-position C is not recoverable from available materials. Keep ASM and PR #144 draft. USA published original-ROM G2 unchanged **1,965 C / 84,648 machine-code instruction bytes / 5,398 ASM**.
