# USA file_11 empty actor callbacks: original-IDO and complete-ROM proof

**Date:** 15 November 2026  
**Scope:** Research-only extension of the thirteen-function `file_11` character-switch stage in draft PR #20. These are genuine *no-op callbacks*, not new gameplay logic; their small original instruction bodies spill incoming parameters to stack and immediately return. Do not conflate this with the still-unmatched 180-byte character selector.

## New exact matching-C findings

The original pinned USA Splat source (`klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`) and authenticated 32 MiB USA ROM show **fifty 12-byte functions** with the same original MIPS instruction sequence (`sw $a0,0($sp)`; `jr $ra`; `sw $a1,4($sp)` delay slot). Each is semantically a no-op callback. Native original IDO 5.3 `-O2 -mips2` exactly reproduces this three-instruction pattern from:

```c
void func_ADDRESS_OFFSET(void *a0, void *a1) {}
```

**Thirty-seven of the fifty** occur in just two contiguous symbol sequences, making them low-risk matching-C experiments without overlapping assembly between the callbacks:

| Group | Original USA ROM range | Functions | MIPS bytes | Source |
| --- | --- | ---: | ---: | --- |
| A | `0x59D0C0..0x59D12C` | 9 | 108 | `decomp/research/callback_noops_a.c` |
| B | `0x59D38C..0x59D4DC` | 28 | 336 | `decomp/research/callback_noops_b.c` |
| **New** | — | **37** | **444** | — |

The other thirteen isolated or shorter-group 12-byte callbacks have **not** been integrated. The earlier thirteen *character-switch* C functions (620 bytes) are distinct from these thirty-seven. The combined scratch overlay therefore owns **50 C functions / 1,064 bytes**. No game logic was changed.

## Full-ROM demonstration

The research script `decomp/research/usa_file11_noop_groups.py` operated on a separate copy of the already-authenticated thirteen-function upstream USA workspace. It first verified all 37 original instruction patterns and the complete baseline ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, and required the 13-function Splat split to be present. It then inserted exactly two contiguous C chunks into the previously assembly-owned `0x599A38` tail, leaving all other functions/relocations, the 180-byte selector, and original game assets in their original form.

The native toolchain produced twelve total linker input sections in the expected order, with zero-only ELF `.text` tail padding trimmed to the original ROM sizes, and a pinned four-byte linker subalignment. The checker validates the exact C and MIPS linked function symbols, original per-function code bytes, exact twelve C/ASM map extents, original source and compiler-object hashes, **all 8,825 file_11 relocation records**, and the complete **33,554,432-byte** game image.

| Gate | Result |
| --- | --- |
| 37 new original-address native IDO C functions | 37/37 exact |
| Previous 13 original-address switch functions | 13/13 retained and exact |
| Linked C bytes in overlay | 1,064/1,064 original bytes |
| Ordered linker objects | 12/12 at original VMAs/sizes |
| Original vs rebuilt USA image | 33,554,432/33,554,432 identical |
| Original vs rebuilt SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Original vs rebuilt `file_11` ELF relocations | 8,825/8,825 identical **including order** |
| New combined research Python unit tests | 44 passed |

The original pristine linked ELF used for the relocation comparison has SHA-256 `1dc2309cce0fc5545a53d03301ebfbf7ab20fbdbd43afae51bea6e690613efa7`; candidate linked ELF SHA-256 is `2ef1b553b9d06f29c1eb0006b197199830f2379a29f94aa329fbfa19582212e6`.

## Technical limitations and remaining tasks

This is a **complete USA ROM and ELF provenance proof in a dedicated scratch checkout**, not a completed end-to-end central `decomp.verify` run with the 160 previously migrated matching-C functions. Therefore, **the official verified total is not increased**; do not report 210 formally promoted functions. The existing central `file_11` adapter initially supported thirteen character-switch functions; the follow-up adds a separate **opt-in v2** stage capable of staging all fifty from the same independently authenticated source. Neither v1 nor v2 is active in the canonical manifest, and neither has passed the full central 160+ function G2 in this session.

All 37 callbacks are meaningful only as **empty callback entry points**; their presence does not establish gameplay semantics or new character-switch knowledge. The additional thirteen isolated empty callbacks warrant separate source-layout review. The 180-byte cycling selector remains assembly, as do the Japanese build and overlay integration problems.

No ROM bytes, generated disassembly, linked objects or proprietary compiler binaries are committed. Only C reconstruction, bounded build script, tests and proof metadata are suitable for version control.

## Follow-up production-stage interface (research opt-in, not promoted)

The checked source adapter now exposes `STAGE_FORMAT = "goemon-file11-character-switch-50-v2"` and validates both new C source SHA-256 hashes before staging. It maintains the twelve pinned C/ASM chunks and the strict original-ROM, FUNC, source/object, map and relocation proofs. The canonical central verifier is extended separately to accept v1 (13 functions) or v2 (50 functions), refusing unknown formats. This API extension does not change the previously proven 32 MiB USA source build or official matching-C total.