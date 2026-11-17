# Graphics / actor-adjacent original-address C research — 2026-11-17

**Status: RESEARCH_ONLY. This is not a production promotion.** The independent scratch build contains **five** original-USA matching-C functions totalling **284 instruction bytes**. Four functions / 212 bytes are newly discovered in this research batch; the 72-byte matrix helper had been isolated earlier. The latest checked canonical `chatgptweb/decomp` production checkpoint was **782 matching C / 34,392 instruction bytes**. None of the five is in that accepted list.

## Candidate inventory

| Function | Guest VMA | Expanded-USA ROM offset | Bytes | Behaviour | Native result |
| --- | --- | --- | ---: | --- | --- |
| `func_8001965C_1A25C` | `0x8001965C` | `0x1A25C` | 72 | Initialise selected 4×4 matrix components to zero, the supplied diagonal and homogeneous 1.0 | Exact, previously found |
| `func_8001B918_1C518` | `0x8001B918` | `0x1C518` | 56 | Forward object fields +0x28, +0x2C, +0x70 and a sixth argument to `func_8001B950_1C550`; preserve its return value | Exact, newly found |
| `func_8001C970_1D570` | `0x8001C970` | `0x1D570` | 76 | Copy 3 floats, 3 u16 fields and 3 floats from the graphics pose struct | Exact, newly found |
| `func_8001C9BC_1D5BC` | `0x8001C9BC` | `0x1D5BC` | 28 | Copy pose vector of 3 float components | Exact, newly found |
| `func_8001C9D8_1D5D8` | `0x8001C9D8` | `0x1D5D8` | 52 | In-place addition of two 3-float pose vectors | Exact, newly found |

All five are **original USA main-code functions**, not runtime asset file offsets or Japanese code addresses. The last three were compiled **together in one source unit** (`gfx_vectors.c`) at relative offsets `0x00 / 0x4C / 0x68`, using pinned IDO 5.3 `-O2 -mips2`, without inter-function gaps. The candidate wrapper's pointer return type is essential to reflecting the original caller ABI; its value is used by callers, and pointer-returning C remains native-exact.

Sources: `anim_matrix.c`, `gfx_wrapper.c`, `gfx_vectors.c`. All four checked-in source/test files have Git blob SHA-1s identical to locally executed originals.

## Original-source full-ROM scratch verification (actually run)

- Used user-provided **original-USA retail 16 MiB ROM** (SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`), decompressed and split through pinned upstream `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- The **baseline original** rebuilt exactly; five C replacements were then staged only in an isolated scratch upstream checkout, leaving all other original assembly unchanged.
- For the earlier matrix helper and wrapper, the Splat boundaries were `0x1A25C`, `0x1A2A4`, `0x1C518`, `0x1C550`; the three contiguous vector helpers occupied `0x1D570..0x1D60C`.
- Invoked pinned IDO 5.3, GNU MIPS assembler/linker. Used `as -no-pad-sections` only for split-assembly section tails; removed **only** IDO-emitted zero padding after the last C instruction by changing the ELF32 `.text` section-size metadata (wrapper 0x40→0x38; vector unit 0xA0→0x9C). All C instruction bytes and original ELF relocation records remained intact. An earlier `objcopy --update-section` attempt **incorrectly removed the wrapper relocation**; it was rejected, replaced with a header-size-only edit, and retested. Avoid the destructive `objcopy` approach.
- Full rebuilt 33,554,432-byte ROM: **identical** to original decompressed ROM. SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Semantic ELF relocation multisets: **all 72 sections, all 82,216 entries identical**, including `.rel.main` 15,058 entries. Positive-size original ELF `FUNC` identities (name/VMA/size) **7,376 / 7,376 identical**.
- Host semantic test with GCC `-std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer -fsanitize=address,undefined`: **PASS**. It checks matrix initialized/untouched slots, 3-vector copy and addition, graphics struct offsets, forwarding of six arguments and the preserved return pointer.

Run the host test from the repository root (this requires no original ROM):

```sh
d=decomp/research/graphics_adjacent_20261117
gcc -std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer \
  -fsanitize=address,undefined \
  "$d/anim_matrix.c" "$d/gfx_wrapper.c" "$d/gfx_vectors.c" \
  "$d/test_graphics_host.c" -o /tmp/goemon-graphics-adjacent-test
/tmp/goemon-graphics-adjacent-test
```

## Adjacent nonmatching investigations — retain original ASM

- `func_800196A4_1A2A4` (76 bytes): conditionally emits F3DEX `G_POPMTX` after a matrix-storage rewind. Best bounded IDO variant has **two mismatching instructions at +0x3C / +0x40** (stores reordered). Other tried variants changed register allocation or scheduling; not promoted.
- `func_8001B6D4_1C2D4` (108 bytes): computes three floating differences, records an unsigned 16-bit field and calls `func_8001C7E4_1D3E4`. Best source yields **two instructions swapped at +0x48 / +0x4C** (LUI scheduling). Volatile and temporary-variable attempts regressed; retain ASM.
- `func_8001B6A4_1C2A4` (48 bytes): writes duplicate byte RGB values to graphics state; compiler deferred argument stack-home stores, unlike original. Best source differed in **nine instruction positions**. Retain ASM.
- The larger `func_800192D0_19ED0`, `func_800196F0_1A2F0`, `func_8001B950_1C550` and transform/actor systems remain ASM-owned. Do not infer a full skeletal animation implementation from these helper matches.

## Production acceptance gate NOT RUN

The original-ROM scratch reconstruction **does not include the current 782 accepted C implementations and staging adapters**, and is therefore insufficient for formal `chatgptweb/decomp` promotion. Shell `git ls-remote` failed DNS in this execution host; GitHub connector access provided publication but not a complete local canonical repository checkout. **Fresh 787-C canonical `decomp.verify`, inventory, and full `decomp.local_ci` were not run.**

Before promotion: transfer the exact live 782-C source checkout to Linux; add reviewed fail-closed main-code source-unit boundaries for all five functions; run native `decomp.verify` with all 782 accepted C, `decomp.inventory`, original ELF/relocation checks, and the full `decomp.local_ci` (not `--quick`). Only after all gates pass may the canonical manifests, matching-C counts, proof and inventory change. The scratch verification does not imply that a future 787-C build will necessarily pass.

No ROM, original ASM, object, executable, graphics asset or private memory dump is contained in these research files. Related model-resource work: issue #61 and PR #62.
