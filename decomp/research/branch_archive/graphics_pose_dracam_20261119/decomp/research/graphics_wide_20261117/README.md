# Wider original-USA actor / camera / graphics matching-C search — 18 November 2026

**State: RESEARCH_ONLY. Not a canonical C promotion.** The current mainline `chatgptweb/decomp` acceptance was **864 USA C / 37,904 original instruction bytes** and **39 Japan-0 C / 2,092 bytes**. A separate, user-owned USA-ROM original-upstream scratch build proves **nine further original-address C functions / 264 bytes** together, but the **full 873-C canonical verifier, inventory and local CI have not run**. Preserve their original ASM ownership.

The search widened from the previously studied `0x80018xxx–0x8001Fxxx` skeletal matrix and actor functions into `main` **Menu Graphics** (`0x10D80–0x12760` expanded-ROM source unit) and **dracam** (`0x12760–0x14540`). These are source-unit labels, **not proof of an NPC model or runtime actor registry**. The functions handle a conditional object pointer link and camera/graphics-state float fields.

## Nine separately deduplicated native-exact functions

| Original USA VMA | Expanded ROM | Size | Source / recovered observable behaviour |
| --- | --- | ---: | --- |
| `0x80011610` | `0x12210` | 36 B | `wide_objlink.c`: if owner exists, store `NULL` or `linked_object + 0x5C` at owner +0x5C |
| `0x800124A0` | `0x130A0` | 12 B | `wide_floatset.c`: write float argument to object +0x70 |
| `0x80012500` | `0x13100` | 24 B | `wide_intfloat.c`: reset float at +0x7C, convert signed integer argument to float at +0x74 |
| `0x800127B8` | `0x133B8` | 48 B | `wide_vectors.c`: initialise three floats +0x80/+0x84/+0x88 and clear +0x9C/+0xA4/+0xAC |
| `0x800127E8` | `0x133E8` | 20 B | Set +0x84 float and clear +0xAC |
| `0x800127FC` | `0x133FC` | 28 B | Copy three floats from +0x80/+0x84/+0x88 through three caller-supplied output pointers |
| `0x80012818` | `0x13418` | 48 B | Initialise three floats +0x8C/+0x90/+0x94 and clear +0xB4/+0xBC/+0xC4 |
| `0x80012848` | `0x13448` | 20 B | Set +0x90 float and clear +0xC4 |
| `0x8001285C` | `0x1345C` | 28 B | Copy three floats from +0x8C/+0x90/+0x94 through output pointers |
| **Total** | | **264 B** | **Nine functions in four native source units** |

The **last six functions compile together** from `wide_vectors.c` in one contiguous 192-byte MIPS text region `0x133B8..0x13478`, no inter-function padding or byte mismatches. The other three compile from separate original code slices because the remaining original neighbours between them are still ASM.

## Native original-USA scratch proof — actually run

Original USA retail SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`. Original **expanded** 32 MiB SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`. Used the bundled, authentic ROM, pinned upstream `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, native IDO 5.3 `-O2 -mips2`, original Splat source boundaries and GNU MIPS linker.

From a fresh independent pristine-upstream copy, Splat's `main` source units were split at:

```text
0x12210 [c, wide_objlink]    0x12234 [asm]
0x130A0 [c, wide_floatset]   0x130AC [asm]
0x13100 [c, wide_intfloat]   0x13118 [asm]
0x133B8 [c, wide_vectors]    0x13478 [asm]
```

`main` linker `SUBALIGN(4)` and assembler `-no-pad-sections` preserve original non-16-byte function boundaries. Three original IDO C ELF objects contained **generated zero-only .text tail alignment** beyond the true original functions: sizes `0x30→0x24`, `0x10→0x0C`, `0x20→0x18`. Only the ELF32 `.text` **section-size header metadata** was changed; no generated MIPS instructions, actual asset bytes or relocation records were patched or deleted. The six-function contiguous C source unit is exactly `0xC0` bytes without trimming.

After linking these nine functions in place of their original ASM (all other original code remained original ASM):

- **Complete USA image identical:** 33,554,432 / 33,554,432 bytes; SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- **All relocations identical:** 72 / 72 ELF relocation-section semantic multisets, **82,216 / 82,216 entries**, including all main-code relocations.
- **All original ELF function identities identical:** 7,376 / 7,376 positive-size symbols (name, actual guest VMA and size). Zero additional positive aliases.
- **All nine independently original-ROM SHA-256 anchored:** `verify_rom_anchors.py` PASS on original authentic USA 32 MiB input; two invalid ROM inputs rejected. This checker emits no original-ROM byte data.

These checks are a real pristine-upstream scratch proof, not a fresh combined build with all 864 already accepted C, so no accepted manifest, inventory, gate record, function count, or production ASM was modified.

## ROM-free host semantic regression

```bash
d=decomp/research/graphics_wide_20261117
gcc -std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer \
  -fsanitize=address,undefined \
  "$d/wide_objlink.c" "$d/wide_floatset.c" "$d/wide_intfloat.c" \
  "$d/wide_vectors.c" "$d/test_wider_actor_fields.c" -o /tmp/goemon-wide-actor-test
UBSAN_OPTIONS=halt_on_error=1 ASAN_OPTIONS=detect_leaks=1 /tmp/goemon-wide-actor-test
```

**PASS**. Tests cover null owner/linked object pointer cases, float writes and signed-int conversion, two three-component getters, both multi-field initialisers, individual float overrides, preserved unaffected fields, and repeat readback. On 64-bit Linux, the test offsets its synthetic base pointer by four bytes so the original `+0x5C` pointer field is aligned for **8-byte host pointers**; real N64 o32 pointers are 4 bytes. The initial host test emitted UBSan misalignment warnings before this **test-fixture-only** correction. The final host test is warning-free. Original matching-C source was not modified to hide the warning.

Original-ROM metadata checker (requires privately owned **expanded** USA image; not included in repository):

```bash
python3 decomp/research/graphics_wide_20261117/verify_rom_anchors.py \
  --usa-expanded /path/to/baserom.decompressed.z64
```

## Rejected or incomplete wider probes — retain ASM

- `func_800115B8` (40 B): at least five native differences, chiefly compiler collapse of a `+0x5C` intermediate pointer.
- `func_800115E0` and `func_800115F8` (24 B each): three differences each in intermediate-pointer schedule, no exact match.
- `func_80012470` (48 B): two remaining local halfword register allocation differences, not exact.
- `func_80020308` (92 B): nine differences in ring/slot selection and fixed-global register schedule.
- `func_800206D4` / `func_800206FC` (40 B each): eight differences each in large-offset resource/state address calculation.
- `func_8001E7C4`, `func_8001E868`, `func_8001E90C` (164 B each): matrix constructor family; bounded native variants failed due stack-frame and input register scheduling. Do not promote source that only reproduces the end of the function.
- `func_800127B8` and `func_80012818`: early variants had two zero-store ordering mismatches each; reversed zero-store **source order** yielded the exact 48-byte binaries now committed.

The wider scan also reviewed accepted and historically researched helpers first to avoid duplicating results. The canonical research queue already has **41 different scratch candidates / 4,108 bytes**, tracked independently; these nine have their own research evidence and must not silently be added to an accepted count.

## Missing production gate

A complete source checkout of the **live canonical 864-C** repository is unavailable to the local original-native build host because shell `git` cannot resolve `github.com` (the GitHub connector can publish/retrieve file-level metadata, but does not automatically materialise the entire source tree locally). Therefore `python3 -m decomp.verify` with **873 C**, `python3 -m decomp.inventory`, and complete `python3 -m decomp.local_ci` are all **NOT RUN**. Original-USA output from the untouched baseline and nine-C scratch **is** proven; this distinction is mandatory.

To promote: reconstruct exact live source checkout; add fail-closed main-code C/ASM split adapter with these four source units; verify every existing accepted C remains exact; run fresh **873-C** full 33,554,432-byte USA G2, original 7,376 ELF FUNC identities, 82,216 relocations, inventory and full local CI. Do not claim 873 accepted functions unless **every** gate passes. Treat Japan matching-C and original offsets independently: this batch changed no fixed-RAM globals and no Japan C verification was performed.

No original ROM, extracted ASM, proprietary compiler, original mesh/texture data or user memory dump is committed.
