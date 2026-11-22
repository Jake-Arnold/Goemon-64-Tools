# Japan rev-0 actor pointer-table: eleven new native-exact C routines

**22 November 2026 — PASSED_ISOLATED_NATIVE / RESEARCH_ONLY, not accepted C.**

The original Japanese expanded ROM was SHA-1 verified as `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Using the pinned SGI IDO 5.3 compiler (`-O2 -mips2 -G 0`), 15 source routines linked at their exact original guest MIPS addresses and matched their original machine-code extents byte-for-byte. Every object preserved the two original symbolic `R_MIPS_HI16` and `R_MIPS_LO16` relocations to `D_8016D430_16E030`, for **30/30 original per-function relocation records**. A source-only replay script verifies these facts using the original ROM; none of the supplied files contains ROM bytes, original assembly, executable objects or proprietary tools.

**Deduplication is essential.** Four of these functions were already accepted in the published JP2268 short145 batch44 promotion and are included ONLY as donor/validation controls. There are **11 newly reconstructed, previously ASM-owned original functions, 588 original machine-code bytes and 22 original symbolic relocation records**. Their research-only sources are not staged into the canonical Japanese C manifest. The canonical published count remains **2,314 C / 123,236 instruction bytes / 5,062 ASM**.

## Eleven newly recovered ASM-owned functions

| Function | Original expanded offset | Bytes | Reconstructed operation |
|---|---:|---:|---|
| `func_8000C118_CD18` | `0xCD18` | 36 | nullable pointer-table entry, halfword store at `+0x70` |
| `func_8000C13C_CD3C` | `0xCD3C` | 52 | OR 64-bit field at `+0x18` with `2` |
| `func_8000C170_CD70` | `0xCD70` | 64 | AND 64-bit field with `~2` |
| `func_8000C1B0_CDB0` | `0xCDB0` | 52 | OR 64-bit field with `4` |
| `func_8000C1E4_CDE4` | `0xCDE4` | 64 | AND 64-bit field with `~4` |
| `func_8000C224_CE24` | `0xCE24` | 36 | 32-bit store at `+0x24` |
| `func_8000C298_CE98` | `0xCE98` | 52 | OR 64-bit field with `8` |
| `func_8000C2CC_CECC` | `0xCECC` | 64 | AND 64-bit field with `~8` |
| `func_8000C334_CF34` | `0xCF34` | 52 | OR 64-bit field with `16` |
| `func_8000C368_CF68` | `0xCF68` | 64 | AND 64-bit field with `~16` |
| `func_8000C600_D200` | `0xD200` | 52 | four ordered halfword stores `+0x64..+0x6A` |

All these functions share the same original main-segment translation-unit family and global pointer table at JP guest `0x8016D430`. Their separate original ASM functions remain in the project; no accepted C ownership has changed. The observed type at `+0x18` is 64-bit unsigned by original instruction scheduling and binary identity; its gameplay meaning remains unspecified.

## Already-accepted control functions (do not count again)

Four original float setters, each 40 bytes, in historical `decomp/research/jp_short145_20261121/batch44/manifest.json`:
`func_8000C248_CE48`, `func_8000C270_CE70`, `func_8000C30C_CF0C`, `func_8000C3A8_CFA8`.

Their independent reconstruction confirms the common typed pointer table and float ABI but contributes **zero** new accepted or newly recovered functions.

## Native replay

On a Linux host with the user-provided authentic Japan decompressed ROM and original pinned toolchain:

```bash
export LD_LIBRARY_PATH=/path/to/goemon-runtime-additions/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
python3 verify_isolated.py \
  --rom /path/to/japan_0/baserom.decompressed.z64 \
  --cc /path/to/ido-5.3/cc \
  --ld /path/to/mips-linux-gnu-ld \
  --objcopy /path/to/mips-linux-gnu-objcopy \
  --objdump /path/to/mips-linux-gnu-objdump \
  --report /tmp/jp_actor15_isolated.json
```

The verifier records all 15 source hashes, builds and links every source function at its original guest VMA using an explicit linker script, compares the linked code *fully* (including resolved global symbol immediates) with the original ROM and validates exact original relocation types, offsets, and symbols. It ignores only zero alignment bytes after each function, not the original function code. The proof JSON was produced by this script, with deduplication separately annotated.

## Actual host regression run

```bash
gcc -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined \
  -Isrc -o /tmp/jp_actor15_host tests/test_semantics.c src/*.c
ASAN_OPTIONS=detect_leaks=1 /tmp/jp_actor15_host
```

**PASS:** 15 real C implementations × 2,048 deterministic states, each tested with live and null pointer-table entries (61,440 calls); structural offsets verified using `offsetof`. This is host execution of the reconstructed C, **not** N64 gameplay emulation or linked original-ROM verification.

## Unrun acceptance gates

The complete current-branch 2,314-C Japanese workspace is not available in the local shell (GitHub DNS/cloning failed, and uploaded `mnsg-japan.zip` contains the pinned original upstream source rather than the latest decomp branch). Therefore complete 32 MiB and retail ROM re-link, all 7,376 ELF function identities, all 80,747 semantic relocations, strict original-C/ASM inventory and full `decomp.local_ci` are **NOT RUN**. No G2 promotion or official count increase is justified. To promote, merge only the **11 unpromoted** functions into the full latest adapter and run every gate; retain the four already accepted float setters as historical controls. No additional matching-C publication is claimed.