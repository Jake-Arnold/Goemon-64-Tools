# USA clamp — eight original F16 reset instructions now reproduced in complete native C

**22 November 2026 · FAILED_NATIVE / RESEARCH_ONLY. Do not promote.**

Original USA `func_801CD310_589220`: ROM `0x589220`, guest `0x801CD310`, original code `4,320` bytes, original frame `232` bytes, owner overlay `file_11`. Original USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, expanded 32MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, authentic SGI IDO 5.3 `-O2 -mips2 -G 0 -non_shared`.

## New result — exact original F16 word sequence within the **whole** C function

The full independently reconstructed C source `clamp_f16_exact_reset.c` (SHA-256 **`3f37cae5ab8d641f08d7818594c3b8a82b9767fa648b41cf66904c0509a485b3`**) generates **eight exact original instruction words at their original function-relative positions**:

| Relative original offset | Authenticated original / candidate |
| --- | --- |
| `+0x1F0` | Original FP branch-likely `bc1fl` |
| `+0x1F4` | `mtc1 zero,$f16` in conditional delay |
| `+0x1F8` | `mtc1 zero,$f16` for reset-only path |
| `+0x200`, `+0x204`, `+0x208`, `+0x20C` | Four native task-field `swc1 $f16` |
| `+0x214` | Third `mtc1 zero,$f16` |

This extends the earlier *isolated fixture* breakthrough to a **complete original-sized-function scope** compiled with the actual IDO 5.3 toolchain and original-address native comparator. The exact source difference against `clamp_gate_control_107.c` is **five type-correct positive-zero C expressions**: `0.0f` to `(f32)0` for reset stores at task +0x7C,+0x74,+0x70,+0x68 and the later default `pool_fp_2`. The reset destination fields retain C `f32*` lvalues and native `swc1`; no integer-store opcode substitution, original assembly, inline machine-code patch, or forged helper arguments.

| Source | Native function bytes | Frame | Matching original-offset comparable words | Exact offset/type/symbol text relocation triples | Original gate words | Eight F16 words |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Control from alternate branch | 4400 | 232 | 107/910 | 26/101 | 18/39 | 1/8 |
| First three reset cast expressions | 4408 | 232 | 84/906 | 20/101 | 15/39 | 7/8 |
| **All four reset casts + magnitude cast** | **4412** | **232** | **86/906** | **20/101** | **17/39** | **8/8** |
| Independent stronger F14 candidate | 4440 | 232 | 117/917 | 30/101 | 1/36 | 0/8 |

All four full-C candidates have **33** helper calls in original callee order, **9** native `sqrt.s`, **101** original-type text relocations (99/101 ordered type/symbol pairs), the five correct destination groups for **18** switch-table entries, and the original `mtc1 zero,$f0` at `+0x04`. All are **FAILED_NATIVE**; F16 candidate is 92 bytes too long, with many instructions and relocations different. The F16-exact candidate **does not** reproduce original `mtc1 zero,$f14` at `+0x1B4` and its `swc1 f14,sp+0x8C` at `+0x218`. The stronger F14 candidate reproduces `+0x1B4` and more overall words but not F16 reset sequence. Do not combine scores from different candidates.

## Experiments and verification actually run

- Hundreds of bounded C-source original-ID0 5.3 whole-function variants: magnitude declaration timing, stack lifetime, field-vs-local threshold, gate nesting, floating-point value aliases, integer/float register hints, typed-zero distributions and vector length. None yielded original F14 and F16 simultaneously. No invented outcome.
- Authenticated original 16MiB retail SHA-1, expanded 32MiB SHA-1 and **pristine original USA full-ROM rebuild 33,554,432/33,554,432 bytes identical**. This is an unmodified original, not a candidate-integrated ROM.
- **Four native IDO 5.3 complete-C builds** freshly replayed from source-only ZIP; original-offset MIPS/ELF/33-call/9-sqrt/101-relocation/f16-word/232-frame assertions pass for the measured **expected FAILED_NATIVE** outputs.
- Fail-closed exact-word read-only auditor verified all eight original F16 instruction words from the authenticated original-ROM bytes and native compiled object at original relative positions, with branch-likely semantics from previous original CFG 65-state audit.
- GCC and Clang ASan/UBSan **65,536 deterministic gate positive-zero cases each**, including NaN, infinity and signed zero, **PASS**. This is bounded predicate/reset semantics, not full movement function equivalence or emulator proof.
- Fresh ZIP extraction, **11 source-only files**, SHA256SUMS and full native/host replay **PASS**.
- Candidate full-ROM replacement, current combined `decomp.verify`, strict inventory, full `decomp.local_ci` and emulator gameplay: **NOT RUN**; complete native equality is false.

## Source and reproducible run

Conversation-delivered `GOEMON_CLAMP_F16_FULL_GATE_20261122.zip`, SHA-256 **`7232c90c24c57d7caf7cd29dfdfba0d0ed07d55f808226aaaa985984ac95462b`**, contains all four **complete** C sources, original-offset comparator `audit_scaffold.py`, standalone `replay.py`, host sanitizer fixture, exact source patch `gate_typed_zero.patch`, README, SHA256SUMS and sanitized JSON evidence. No ROM, extracted original ASM/opcodes, original game assets, ELF/object, proprietary IDO compiler or dependencies are included.

Reproduction with original private ROM, pinned upstream and compiler installed:

```sh
python3 replay.py --upstream /path/to/pinned/mnsg-japan --rom /path/to/private/baserom.decompressed.z64 --elf /path/to/original/mnsg.elf --built-rom /path/to/pristine/mnsg.z64 --retail-rom /path/to/retail/USA.z64 --host
```

The GitHub PR stores sanitized proof and the **five-expression source patch**, and the conversation ZIP stores all four complete C source files for independent replay.

**Next problem:** Find type-correct C representation that delays the original long-lived F14 magnitude zero spill until `+0x218`, while retaining F16 reset definitions `+0x1F4,+0x1F8,+0x214`. Original `sp+0x8C` is overwritten by 3D norm at `+0x4E4` and read again at `+0xFE8`. Exact F14 and F16 have been reproduced **separately** in whole-C, not together. Keep original ASM as production owner, preserve draft PR #144 and avoid changing canonical acceptance.

Current independently verified USA G2 unchanged **1,965 accepted C / 84,648 original MIPS instruction bytes / 5,398 ASM entries**.
