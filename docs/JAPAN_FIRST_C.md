# First exact Japanese matching-C promotion

**Date:** 2026-11-15. **Status: native function bytes PASS; full 32 MiB link PASS; exact 16 MiB recompression PASS.**

This is the first native IDO 5.3 Japanese matching-C function integrated into an otherwise assembly-only Japanese Goemon N64 build. It does **not** imply that Goemon64Recomp runs the Japanese game natively on PC.

## Target

| Item | Value |
| --- | --- |
| Function | func_80037A20_38620 |
| Japanese original VMA | 0x80037A20 |
| Original ROM offset | 0x38620 |
| Function | 8 bytes, jr ra followed by nop |
| C implementation | void func_80037A20_38620(void) {} |
| Compiled .text | 16 bytes, includes 8 trailing padding bytes |
| Native compiler | pinned mnsg/tools/ido-5.3/cc, -mips2 -O2 |
| Object text SHA-256 | 2415714719d85e4a789acee079f28e4e4c4c2b693ab00b843e8d8d91c8c3882c |
| Text relocations | 0, confirmed by MIPS objdump -r -j .text |

Original MIPS and compiled object .text are identical:

~~~text
03 e0 00 08 00 00 00 00 00 00 00 00 00 00 00 00
~~~

The C source is in decomp/japan_matching/jp_main_38620.c. This deliberately leaves all other functions as original assembly. A no-op function is a pipeline proof, not substantial game-code recovery.

## Reproduce from private input files

Requirements: the two offline dependency directories, the exact pinned upstream mnsg source checkout at 7e2029c5, and an exact canonical Japanese rev-0 baserom.z64. The previously documented assembly-only build is the control.

From Goemon-64-Tools:

~~~bash
python3 -m unittest decomp.test_japan_asm_baseline decomp.test_japan_first_c -v

bash decomp/build_japan_first_c.sh \
  /path/to/mnsg-japan \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
~~~

The dedicated runner builds a fresh Splat variant with **one** original segment restored as C, at ROM 0x38620, using the local source file. It does not modify the pinned upstream original Splat configuration. All other 188 formerly C-designated segments stay assembly. It fixes the same 22 cross-object generated labels and two BSS name collisions, then builds with:

~~~sh
make build/japan_0/mnsg.z64 VERSION=japan_0 C_FILES=src/jp_main_38620.c
~~~

The runner compresses the completed 32 MiB image using upstream Rommy with the original manifest, then validates the source C object .text and both full-image SHA-1 values.

Local-only outputs: build/japan_0/mnsg.z64 (32 MiB), build/japan_0/mnsg.first-c.retail.z64 (16 MiB), and build/japan_0/first-c-proof.json (hash-only report).

## Verified results

- Native IDO 5.3 compiled the C function to exact original 16-byte .text, with no text relocation entries.
- The actual Splat-generated linker script selected build/japan_0/src/jp_main_38620.c.o at the original function address in place of the assembly translation unit.
- Complete 32 MiB linked ROM SHA-1: **6f8745fecc3a5e7d4918c7a73353eb0726116ded**, zero differing bytes.
- Complete recompressed 16 MiB retail ROM SHA-1: **9843ee979b5f6c80f5eda85df0baed9ae7c4e73b**, zero differing bytes.
- ROM-free test suites: **6/6 passed** (3 assembly baseline + 3 first-C), shell syntax checked.
- Original USA full-ROM regression, Japanese emulator gameplay and Japanese PC native port: **NOT RUN**.
- The standalone first-C runner is provided and syntax-checked; its individual stages and native build were run locally, not the wrapper end-to-end as a single command.

Proof file: decomp/results/japan_0_first_c_2026-11-15.json.

## Next target

Move from the trivial no-op to a small functional Japanese helper, preserving the same original-address assembly/IDO, overlay relocation and complete image validation. Expand region-aware matching manifests and verification without altering USA baseline.
