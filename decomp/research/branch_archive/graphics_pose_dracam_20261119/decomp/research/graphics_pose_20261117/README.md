# USA original graphics/actor adjacent C — second bounded batch (17 November 2026)

**State: RESEARCH_ONLY, NOT A CANONICAL C PROMOTION.** This investigation follows [the earlier five-C graphics scratch research](../graphics_adjacent_20261117/README.md). It adds **three unique USA candidates / 404 original instruction bytes**. The previously inspected `func_8001F878_20478` (56 bytes) was **already accepted** by the current decomp baseline and is not counted again.

The live `chatgptweb/decomp` proof at research start was **864 accepted USA matching C functions / 37,904 instruction bytes, 6,499 remaining assembly**. Japan's promotion process remains independent. Production manifest and results were not modified by this branch.

## Three decomp candidates verified against original USA ROM

| Function | Original guest VMA | Expanded ROM offset | Size | Reconstructed semantics | Source |
| --- | --- | --- | ---: | --- | --- |
| `func_80019160_19D60` | `0x80019160` | `0x19D60` | **108 bytes** | Follow hierarchy `next` at object +0x94; when a next object exists, examine `child` at +0x74 using `func_800191CC_19DCC(child, target)`; return 1 on successful child search, else walk cached next; 0 on exhaustion | `actor_graphics_traverse.c` |
| `func_8001E2BC_1EEBC` | `0x8001E2BC` | `0x1EEBC` | **196 bytes** | Convert halfword rotation sentinel `0x8000` to zero in three fixed graphics globals, otherwise write unmodified halfwords; forward packed pose components to `func_8001E9B0_1F5B0` | `pose_wrappers.c` |
| `func_8001E380_1EF80` | `0x8001E380` | `0x1EF80` | **100 bytes** | Forward pose position words, three rotation halfwords and three translation floats to `func_8001EC04_1F804` | `pose_wrappers.c` |

The latter two are **strictly contiguous**, `0x1EEBC..0x1EFE4`, and compile with original IDO 5.3 **together in one C source unit**, with exactly 296 unpadded instruction bytes and no instruction differences outside ordinary linker-resolved relocations. Their original MIPS frame sizes, branch targets, delay slots, register allocation, stack-passed arguments and object-field offsets match. The actor traversal matched on source variant 2 of 3: a cached `next` pointer, explicit loop and conditional callback, preserving the original traversal under callback mutation.

All three original instruction-region SHA-256 digests are independently checked by `verify_rom_anchors.py`; no original game instructions are checked in.

## Local original upstream native / full-ROM scratch verification — PASS

**Actually executed in this session:** unpacked the user's authentic USA ROM and bundled pinned upstream `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Reconstructed the separate Python/Splat/IDO 5.3/MIPS binutils runtime. Decompressed and Splat-split USA retail ROM, then built the original unmodified upstream, obtaining **33,554,432 exact bytes** and SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.

In a **separate original upstream scratch checkout**, replaced the three original assembly functions with the two reviewed C source units. This scratch also included the already-accepted `func_8001F878_20478` as an independent 56-byte C replacement; it is intentionally **excluded** from this new-function count. The exact Splat code boundaries were:

- Object unit: original `[0x17550, asm]`, then `[0x19D60, c, actor_graphics_traverse]`, then `[0x19DCC, asm]`.
- Pose unit: original `[0x1D570, asm]`, then `[0x1EEBC, c, pose_wrappers]`, then `[0x1EFE4, asm]`.
- Previously accepted rotation helper: `[0x20478, c, gfx_rotation_180]`, `[0x204B0, asm]`.
- Staged original `.main` output `SUBALIGN(4)` and trimmed only **tool-generated trailing section padding**, leaving actual original instruction payload, relocation records and source function boundaries unchanged. Specifically, `actor_graphics_traverse.c.o` `.text` 0x70→0x6C, pose wrapper C `0x130→0x128`, rotation C `0x40→0x38`; adjacent assembly tails `19DCC.s.o` `0x37B0→0x37A4`, `1D570.s.o` `0x1950→0x194C`, `1EFE4.s.o` `0x14A0→0x1494`. Adjusted **ELF32 section-header size metadata only**; never patched a MIPS instruction or deleted relocations. Input byte content and relocation entries remained original/native compiler output.

**Result:** Candidate original-upstream scratch image is **byte-for-byte identical across all 33,554,432 ROM bytes**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Independent `readelf -rW` semantic multiset audit: **72/72 relocation sections and 82,216/82,216 entries match**, including original source symbol targets. `readelf -Ws` original positive-size `FUNC` identity triples (name, address, size): **7,376/7,376 identical**, zero new aliases.

The passing scratch proves original-address C equivalence against **pristine original assembly**, not coexistence with all current 864 accepted production C functions.

## Host semantic tests — PASS

Using GCC with `-std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer -fsanitize=address,undefined`:

```bash
d=decomp/research/graphics_pose_20261117
gcc -std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer \
  -fsanitize=address,undefined "$d/pose_wrappers.c" "$d/test_pose_wrappers_host.c" -o /tmp/goemon-pose-host
/tmp/goemon-pose-host
gcc -std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer \
  -fsanitize=address,undefined "$d/actor_graphics_traverse.c" "$d/test_actor_traverse_host.c" -o /tmp/goemon-actor-traverse-host
/tmp/goemon-actor-traverse-host
```

The pose test checks each packed argument, three rotation sentinel cases, the original offsets and forwarding behaviour. The hierarchy test checks empty traversal, callback success on the first/second inspected child, skipping the terminal node, and a callback that **mutates the preceding node's next pointer** (the function must follow the cached pointer). Host 64-bit pointers change C struct layout; original o32 offset proof is provided by the actual MIPS IDO object, **not** an invalid host 64-bit `offsetof` assertion.

## Required independent Japan-0 counterpart investigation

The USA function `func_8001E2BC_1EEBC` writes three 16-bit fixed graphics globals at `0x801689F0`, `0x801689F2`, `0x801689F4`. The independent, authenticated Japan-0 **32 MiB** image (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`) contains the corresponding **196-byte** function at **ROM `0x1EB80` / guest `0x8001DF80`**. Direct original code comparison differs at only **seven 32-bit instruction words**: six halfword-store immediate words (+0x28, +0x2C, +0x48, +0x4C, +0x68, +0x6C) and the final callee JAL (+0xA8). The Japanese store targets are **`0x8016E1D0`, `0x8016E1D2`, `0x8016E1D4`**, matching original Japan BSS symbol widths and calls.

**Regional displacement is +0x57E0, NOT +0x57F0.** This is a code-supported exception to the common fixed-RAM offset heuristic and is recorded independently; no memory edit is permitted. USA values are original-code verified; Japan values are **original-code instruction-traced**. No Japan live gameplay probe, runtime write, native Japan IDO-unit match or full Japanese ROM G2 is claimed.

The script `verify_rom_anchors.py` verifies the authenticated original **expanded** USA/Japan images, all three USA byte hashes and the Japan source-writer comparison. It emits *metadata only*; no ROM bytes or code extracts.

## Deduplication and nonmatches

- **Already in accepted 864-C proof:** `func_8001F878_20478` (56-byte rotation adjustment), `func_8001F914_20514` (44 bytes), `func_8001FA3C_2063C` (68 bytes). No re-promotion.
- `func_8001E3E4_1EFE4` (96 bytes): IDO produces the correct length but reorders two independent FP instructions at +0x14/+0x18. Keep ASM.
- `func_8001E444_1F044` (96 bytes): register allocation / zero-store ordering differs; keep ASM.
- `func_80019160_19D60` actor search variants 1 and 3 did not match; variant 2 did and is preserved exactly.
- Previous draft graphics research PR #63 has five other full-ROM-scratch-exact sources but its canonical G2 is also pending; **do not assume these 404 bytes promote atop those 284 scratch bytes** without a combined verified build.

## Production gate — NOT RUN / exact blocking input

The complete live **864-C** canonical repository source tree was not transferable into this native execution filesystem: local GitHub DNS fails, while the GitHub connector permits file-level research publishing. The separately verified pinned original `mnsg` upstream checkout and toolchain are available and were used; **the canonical `decomp.verify` build with all 864 currently accepted C, `decomp.inventory`, full `decomp.local_ci` and a fresh combined 867-C source/staging adapter were NOT RUN**. No production manifest, result count or inventory is edited on this research branch.

**Next verified action:** materialize exact live canonical decomp source and stage the two 296-byte contiguous pose wrappers plus the 108-byte hierarchy search as separate reviewed main-code C units; perform native `decomp.verify` plus inventory/semantic ELF and full `decomp.local_ci`. Only promote to an **867-C** manifest if every gate passes. Separately investigate the nonmatching E3E4/E444 matrix constructors within a bounded compiler budget. Keep all failed and unverified source regions assembly-owned.
