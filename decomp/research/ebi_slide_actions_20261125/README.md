# Ebi Slide action 0x0D / 0x8E / 0x8F follow-up — 25 November 2026

Status: ISOLATED_EXACT / RESEARCH_ONLY for JP 801E905C (220 bytes); FAILED_NATIVE for four larger helper drafts. Live base 3669a15a807c77249e85cd177ef2704d5560e5d1, pinned tracked-clean upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. Both original expanded hashes authenticated: USA 6ea0ed71032ce08fc2745f412d84936382197494, JP 6f8745fecc3a5e7d4918c7a73353eb0726116ded. Native IDO 5.3 executable SHA256 76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0; current compiler ledger blob 5e524a9e7c0e0f0b3d8c859a415097838a7e2158 independently verified. Current full canonical archive unavailable, direct shell GitHub DNS failure. Independently generated original Splat references used only for isolated proof. No full original owner/ROM G2, promotion integrity, strict candidate inventory, hosted CI or gameplay replay. No accepted count change (USA2939 +13 upstream, JP2843). PR #268 research stays separate.

## Action table and entry

Original table ROM offsets USA 0x5BFAA0, JP 0x5C4A50. Already accepted C: 0x0D USA 801DDD7C/599C8C, JP 801E311C/59F0EC (32 B); 0x8E USA 801F56B8/5B15C8, JP 801FA6C8/5B6698 (52 B); 0x8F USA 801F56EC/5B15FC, JP 801FA6FC/5B66CC (72 B). Previous accepted atlas and live JP2843 inventory checked; no new count for these wrappers.

Already accepted 248-byte entry pair USA 801E77E4/5A36F4 and JP 801EC90C/5A88DC dispatch 0x8F when task+0x60 == 1. That branch sets context+0x30=0, clears task+0x30 bit 0, installs action 0x8F, calls several additional helpers, and clears context+0x48. No direct movement-vector or E4/E8 stores on this branch. Indirect helper effects and exact frame order remain unproved.

The 0x8E and 0x8F wrappers call shared helper USA 801F5734 / JP 801FA744. Parameters after task: 0x8E (0.001171875f,20.0f,0.025f), 0x8F (0.001171875f,12.0f,0.1f). Shared helper reads animation object at task+0x18, tests its +0x28 frame/progress against 12 and 20, advances context+0x30, and writes three animation floats +0x1C/+0x20/+0x24. At completion (progress >= duration - 1), writes final float, sets task flag bit 0, dispatches action 0 and resets context fields. The 0x8F wrapper clears context+0x86 only if helper returns success. USA alone has an additional conditional zeroing of context+0x50 and task+0xA4/+0x6C when context+0x59 is zero. Neither shared helper directly writes horizontal X/Z or E4/E8. Do not infer indirect callee semantics or that a new slide was reproduced. User clip showed the action 0x0D -> 0x8F transition with 2.8/0.7 retained while miniature.

Action 0x0D movement handler USA 801E3400/59F310 and JP 801E8610/5A45E0 calls regional movement selectors USA 801E1C90 and JP 801E6ED8. Accepted stopping helper USA 801E276C and JP 801E79B4 zeros three vector components and sets E4/E8 to 0.8 mini or 2.0 normal. New JP 801E905C/5A502C is the selector's input-dependent helper, donor USA 801E3DE0/59FCF0. It reads g_system+0x3B0FC with 24-byte profile stride. Below absolute input 0.00001 it returns zero without writing E4/E8; otherwise divisor 0.55/input capped above at 8, next=(target-initial)/divisor+initial, capped at target, E8=E4*factor. Original signed divisor retained. Thus neutral input can preserve previous parameters, but not proof of the complete slide sequence.

## Native results

| Target | Best original-position linked words | Candidate/original bytes | Named text relocations |
|---|---:|---:|---|
| JP 801E905C | 55/55 | 220/220 | 6/6 exact |
| JP 801FA744 | 84/89 | 356/356 | 8/8 exact |
| USA 801F5734 | 89/99 | 396/396 | 8/8 exact |
| JP 801E8610 | 164/239 | 972/956 | 42/42 count only |
| USA 801E3400 | 137/212 | 864/848 | 39/39 count only |

JP 801E905C: adapted from live USA donor decomp/research/pending_isolated233_20261120/sources/iso233_240.c blob ec0a9a7c871505c71e5bc44bc059db9c71696d32. Exact linked original extent, FUNC size/VMA, unrelocated object text including encoded addends, and all six ordered named relocation sites. Original code SHA256 3a088ff55b9749b35409042fbe130a199e01ac43343c1eef5ab4bde65b5a647b. Negative changes divisor test from 8 to 7 and matches 54/55; first +0x68, 3c014020 vs 3c01401c, same six relocs. NO_NEW_COMPILER_FINDING. Both animation helpers recover original sizes and all eight relocation sites via direct-return form; remaining register allocation, with two FP scheduling words recovered via known physical-line scheduling sensitivity. JP widening and same-line grouping gives 84/89; mask/direct-counter variants fail. 0x0D drafts recover original 0x28 frame using shared byte locals; both still 16 bytes too long and reloc sites nonexact.

24 native variants independently replayed from source-only kit. Initial replay had incorrect Japanese original ASM owner path; corrected by symbol lookup and replayed all 24 successfully. Original source and object relocation records unmodified. Positive and principal negative source blobs retained here; complete failed C candidates, all per-attempt digests/classifications, exact flags, first differences, and standard-library replay supplied in originating conversation ZIP goemon_ebi_slide_actions_20261125.zip SHA256 b9e0ad427c396548e5da83405c5d29590a4055ad5bf072371633834efe60f1ba. No original ROMs, generated ASM, assets, proprietary tools or binaries committed.

Next: complete shared helper allocation match, port JP selector from accepted USA with original jump-table proof, trace indirect calls and frame order during successful and partial slides. Read-only watches task+0x60, +0x30, +0x18 pointer and animation+0x28, context+0x30 and +0x86. All dynamic. Full canonical independent regional G2 and required CI before any promotion.
