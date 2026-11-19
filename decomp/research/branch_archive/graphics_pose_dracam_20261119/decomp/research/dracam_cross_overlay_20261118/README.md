# dracam cross-overlay dependency expansion — 18 November 2026

**RESEARCH_ONLY / no accepted-C promotion.** This is a new read-only examination of the authentic USA expanded ROM's Splat-generated original assembly, deliberately widened beyond the nine functions in draft PR #65. It does not alter the canonical 864-C manifest or assert a new native-exact C function.

> **Native follow-up (18 Nov 2026):** All three original targets below, plus five additional dracam neighbours (eight distinct USA C / 352 bytes), now pass pinned IDO original-address compilation, a combined full original-upstream 32 MiB ROM scratch build, all 82,216 semantic relocations and all 7,376 ELF FUNC identities. Host ASan/UBSan regression passes. **RESEARCH_ONLY:** canonical 864+8 production verification, inventory and full local CI remain NOT RUN; USA accepted 864 C unchanged. See [NATIVE_PROOF.md](NATIVE_PROOF.md) and [sanitized proof](../../results/dracam_eight_native_upstream_scratch_20261118.json). Previous unexecuted-gate/next-target language below describes the *initial* research-only scan and is superseded by this update.

## Reproducible source

Original retail USA ROM SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`. Pinned `mnsg` upstream: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Decompression and Splat extraction both completed successfully in a fresh isolated Linux workspace using the project-supplied runtime. Read-only source: `asm/usa/12760.s` and all `asm/usa/*.s` files from that extraction. Counts below are **static assembly references**, not measured runtime calls or unique caller functions. A `%hi(symbol)` count is one address-load high-half occurrence, not necessarily a unique pointer or dispatch table slot.

| USA function | ROM offset | Original size | Direct `jal/j` references | `%hi` address references | Distinct assembly source files with either |
|---|---:|---:|---:|---:|---:|
| `func_800127B8_133B8` | 0x133B8 | 48 B | 74 | 90 | 29 |
| `func_80012818_13418` | 0x13418 | 48 B | 72 | 104 | 29 |
| `func_80012878_13478` | 0x13478 | 136 B | 0 | 24 | 20 |
| `func_80012900_13500` | 0x13500 | 56 B | 2 | 67 | 31 |
| `func_80012938_13538` | 0x13538 | 8 B | 19 | 31 | 20 |

**New functional evidence beyond PR #65:** `func_80012878` reads a pointer at owner +0x6C, copies 0x60 bytes from the caller-supplied buffer into that pointed-to region in 0x0C-byte steps, then calls the three existing PR #65 candidates: `func_800127B8` with input floats at +0/+4/+8, `func_80012818` with input floats at +0x0C/+0x10/+0x14, and `func_80012500` with an unsigned 16-bit input from +0x1A. This is a **combined state loader** (functional description, not a recovered original symbol name). The copied 0x60-byte buffer and subsequent typed accesses overlap: exact layout/aliasing requires further investigation.

`func_80012900` performs the inverse 0x60-byte copy from the pointer at owner +0x6C to the caller-supplied destination. `func_80012938` is an 8-byte pointer getter, returning the word at owner +0x6C via `lw $v0, 0x6C($a0)` in the return delay slot. Together these form an identifiable load/copy-out/getter cluster immediately adjacent to the six native-exact float setters/getters.

## Widening hypothesis, not established semantics

The two three-float groups (+0x80/+0x84/+0x88 and +0x8C/+0x90/+0x94), paired reset fields (+0x9C/+0xA4/+0xAC and +0xB4/+0xBC/+0xC4), the owner +0x6C state pointer, and the 0x60-byte copy suggest a reusable graphics/camera-state record. Do **not** label these fields camera position/target or world coordinates without caller and runtime evidence. The very broad cross-overlay static reference fan-out indicates this unit is a higher-value semantic anchor than a local-only leaf.

## Next exact-C candidates and investigation

1. `func_80012938_13538` (8 B): minimal getter. Compile with original IDO at original address; validate ELF symbol extent, section placement, relocation identity and complete 864-plus-C gate.
2. `func_80012900_13500` (56 B): reverse 0x60-byte block-copy. Investigate whether compiler emits the original unrolled three-word copy loop; test bounded pointer typing and loop variants.
3. `func_80012878_13478` (136 B): full loader calling the three existing native-exact setters; preserve original 0x60-byte copy and unsigned halfword conversion. Try as a **single adjacent source unit** with PR #65's six-function 192-byte cluster only after determining original source boundaries.
4. Trace the 24 static address-load sites of `func_80012878` and 67 of `func_80012900` into their containing callback/registration structures, including `file_29`, `file_31`, `file_57`, and `file_73`.
5. Build a cross-overlay caller/dataflow graph for the two vector initializers: `676C80.s` contains 49 and 47 static references respectively, and `694CA0.s` contains 21 each. Prioritize understanding which state records these overlays create and restore.
6. Check overlap against the 41-function promotion queue and PRs #63–65 before counting anything new. Retain ASM for all unmatched candidates.

## Gates and limitations

**Actually performed:** USA retail SHA-1 check, pinned upstream commit check, original ROM decompression, Splat extraction, read-only original MIPS instruction inspection, cross-overlay static reference counting.

**At initial scan, not performed; subsequently completed for this batch:** fresh IDO compilation of all eight functions, original-upstream replacement ROM scratch proof and sanitizer host CI. **Still NOT RUN:** canonical 864-plus-C verification, canonical inventory, and full production local CI. No new C counts are claimed. The repo's canonical 864-C checkout was not materialized in the native workspace because direct shell GitHub DNS failed; the connected GitHub interface is used only for this research publication.

No ROM, generated ASM, binary or extracted asset is included.
