# USA Mini clamp typed-zero and early original MIPS reconstruction — 21 November 2026

RESEARCH ONLY / FAILED_NATIVE. The production assembly stays in place; no acceptance count changes.

Original target: USA func_801CD310_589220, original ROM offset 0x589220, guest VMA 0x801CD310, original function size 4320 bytes, original stack frame 232 bytes; original expanded 32 MiB ROM SHA-1 6ea0ed71032ce08fc2745f412d84936382197494. Authentic SGI IDO 5.3, -O2 -mips2 -G 0 -non_shared, pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee.

## Recovered original prologue and stack/calls

Eleven existing task-field floating-zero assignments changed only their expression from 0.0f to (f32)0. The lvalue remains f32 and compiled zero stores retain the correct swc1 opcode, unlike the previous diagnostic integer-store transformation. In native IDO output this eliminates the whole-function saved f20, recovering the original mtc1 zero,f0 instruction at function relative +0x04. Ten changes do not. This is a genuine compiler-expression phenomenon, not proof of original literal spelling.

Restoring an authentic 232-byte frame requires changing a live stack-backed three-float vector declaration to four floats, without accessing its fourth component. Three original vector helper implementations were inspected and access only first three components. A declaration-order move of an already-live integer temporary moves the angle and trig-return stack group into its original locations. These are C codegen hypotheses; actual original C declarations remain unknown.

The best early-layout source compiles to a 4480-byte function (original 4320), frame 232/232, 85/910 same-offset comparable nonrelocated instruction words, and 20/101 exact offset/type/symbol relocations. Original first 15/15 comparable MIPS words, the first context 13/13 and the switch window 49/55 match. Original first-angle halfword stores in five cases exactly at +0xC8,+0xFC,+0x12C,+0x160,+0x180 use sp+0x6E. At merge original lhu a0,sp+0x6E at +0x194 is exact; candidate store sh v0,sp+0x6C at +0x198 differs in source register from original sh a1,sp+0x6C. Both trigonometric JALs are at their original +0x19C and +0x1A4 offsets; second delay-slot lhu at +0x1A8 and trig float-return swc1 f0,sp+0x64 at +0x1B0 are also exact. All 18 jump-table destination offsets have zero displacement drift. 33 calls / 9 inline sqrt.s / 101 text relocations preserved; ordered relocation type+symbol matches 99/101, but only 20 exact offset/type/symbol triples. First non-relocation mismatch +0x44 (branch target displacement). Downstream context +0x1B4..+0x260 0/38 comparable words match.

Alternative whole-C source is 4440/232 bytes with 109/910 same-original-offset words and 26/101 exact relocation triples, but its cosine calls are 4 bytes early and its angle-store topology differs. Both C sources remain nonmatching; do not combine metrics from distinct candidates or promote either. Historical 157-word source not recoverable as a complete source here.

## Native and host tests actually executed

- Private USA retail original SHA-1 df8083a54296b8c151917c5333e1c85f014a2a66; expanded USA SHA-1 6ea0ed71032ce08fc2745f412d84936382197494; pristine pinned ROM 33554432/33554432 bytes identical (unmodified original, not C replacement).
- Clean source archive extraction, file-hash verification and replay with original IDO 5.3: four entire C variants compiled and checked with real original-offset ELF/MIPS/relocation and specific call/stack/jump assertions. All four reproduce EXPECTED FAILED_NATIVE.
- GCC and Clang AddressSanitizer/UBSan: 65536 bounded cases each for typed-positive-zero / vec fourth element unused, and 65536 switch-angle cases each. They do not establish whole-function gameplay equivalence.
- Candidate full-ROM integration, current accepted-C combined decomp.verify, strict inventory, complete decomp.local_ci, and gameplay: NOT RUN. No production C changes or manifest edits.

## Permanent source recovery

Full C source files, original-address comparator, replay, host test, patch, source reconstructor and sanitized evidence delivered in this conversation as source-only GOEMON_CLAMP_TYPED_ZERO_EARLY_20261121.zip, SHA-256 33b3d0abf00f469a41d5151d891cb515f6ca64e0625155947bf0bf673a4fd92b. No ROM, original assembly, asset, ELF/object or proprietary toolchain included.

Previously committed full research C is on this branch as case_store_first_scalar_second_20261121.c.gz, uncompressed SHA256 612bc4baa9c81b0c2397fa1b9b0853da6f0d4738b2c65c7842a77a4d35546d90. The attached source-only Python file RECONSTRUCT_TYPED_ZERO_EARLY_20261121.py deterministically builds the best current complete C from that GitHub source and checks SHA256 b444006aa5bd9dddf64b3fd19d2d5a49d43a7ff962f2d65778e93f72c8ac6078. Example: python3 RECONSTRUCT_TYPED_ZERO_EARLY_20261121.py case_store_first_scalar_second_20261121.c.gz clamp_typed_zero_exact_early.c

Next original-MIPS mismatch: second-angle store uses candidate v0 versus original a1 at +0x198. Function also remains 160 bytes too large and lacks original independent f14/f16 zero definitions in downstream context. Preserve ASM and research draft PR #144.

Published USA G2 stays at 1965 matching C, 84648 original MIPS bytes, 5398 remaining ASM entries.
