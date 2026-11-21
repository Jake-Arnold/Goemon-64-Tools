# Original-ROM native C promotion: gameplay Start + VM busy (21 November 2026)

**Status: PASSED_G2_LOCAL** until both the implementation commit and its remote branch SHA have been verified. No game runtime test of Bomb Text Skip is claimed.

## Newly accepted original-address C (deduplicated)

| Region | Original address / name | Size | Original ASM owner |
|---|---|---:|---|
| JP | `func_8001F580_20180` | 100 | `jp1686_263_000.s` |
| JP | `func_8001F610_20210` | 252 | `jp1686_263_002.s` |
| JP | `func_8003EE44_3FA44` | 36 | `jp1686_268_003.s` |
| USA | `func_8001F8B0_204B0` | 100 | mixed C/ASM `rotation_angles.c` |
| USA | `func_8001F940_20540` | 252 | mixed C/ASM `rotation_angles.c` |

**Five new, 740 original instruction bytes.** JP 2,118 -> 2,121 / USA 1,956 -> 1,958. All previous accepted C retained, and no original ASM was modified in the repository.

## Exact native G2 and source contract

The pinned source archive plus original retail ROM and downloaded compiler dependencies are private inputs, never committed. Source-only `decomp/glitch_g2_promotion.py` independently authenticates the decompressed original 32 MiB ROM, the previously verified per-region baseline, expected ASM ownership or mixed source owner, and source SHA-256.

Japan: the adapter partitions original assembly at exact function extent boundaries and links three IDO 5.3 C objects, retaining all other original MIPS assembly. A typed source expression for the Start input preserves original **`g_system + 0x3B07C`** relocation semantics; the dispatcher explicitly uses the original absolute **`D_3ADDE`** symbolic offset (not a hard-coded numeric-offset compiler shortcut). The adapter requires whole-ROM SHA-1 original, original 7,376 ELF function identities, and the complete **80,747 original `.rel.main` and overlay semantic relocations**.

USA: the adapter fail-closed SHA-256 checks the existing `rotation_angles.c` containing three previously accepted C functions and replaces only two original assembly pragmas with original-ID0 exact C. It preserves the unrelated pause-handler ASM pragma. Struct base references must use original symbol pair `D_800BCCC0_BD8C0` and `D_8014CCC0_14D8C0` to preserve every original `R_MIPS_HI16/LO16` relocation. Strict gate: exact original 32 MiB image, all original 7,376 ELF functions, **82,103 original relocations**, and exactly two newly unmarked accepted functions. The original USA ELF has thirteen separately accounted baseline unmarked functions; the accepted-C count remains 1,956 + 2 = 1,958, not 1,969 + 2.

**Source correctness is the original linked code and complete relocation graph**, not the C expression's superficial resemblance to original source. A previous test produced the original ROM bytes with *missing relocations*, and was rejected until source changes reproduced the original semantic records. The Japan teardown `func_8001F70C_2030C` (68 B) was explicitly excluded from this promotion because its isolated exact C lost original `D_3ADDF` relocation pairs or changed length/scheduling when symbols were corrected.

## Reproduce locally (never commit ROMs)

1. Establish independently validated JP 2,118 and USA 1,956 baseline workspaces using the pinned original upstream, original ROMs and compiler environment documented in root `GOEMON_BUILD_ENVIRONMENT.md`.
2. For each region, copy a verified local workspace, then run:

```bash
python3 -m decomp.glitch_g2_promotion stage --region japan_0 --checkout /path/to/fresh/japan
python3 -m decomp.glitch_g2_promotion build --region japan_0 --checkout /path/to/fresh/japan --deps /path/to/goemon-dependencies --runtime /path/to/goemon-runtime-additions
python3 -m decomp.glitch_g2_promotion verify --region japan_0 --checkout /path/to/fresh/japan --baseline /path/to/verified/jp2118

python3 -m decomp.glitch_g2_promotion stage --region usa --checkout /path/to/fresh/usa
python3 -m decomp.glitch_g2_promotion build --region usa --checkout /path/to/fresh/usa --deps /path/to/goemon-dependencies --runtime /path/to/goemon-runtime-additions
python3 -m decomp.glitch_g2_promotion verify --region usa --checkout /path/to/fresh/usa --baseline /path/to/verified/usa1956
```

All commands fail closed if the inputs or code differ. Correct MIPS toolchain path and runtime LD_LIBRARY_PATH are required for the `verify` command. Full Python/GCC `python3 -m decomp.local_ci` is an independent gate and does not substitute for original IDO/ROM identity. Production gameplay execution remains untested.

## Verification summary

- Japan: **33,554,432 / 33,554,432** identical bytes, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; **7,376 ELF identities**, **80,747 original semantic relocs** SHA-256 `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20`.
- USA: **33,554,432 / 33,554,432** identical bytes, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; **7,376 ELF identities**, **82,103 original semantic relocs** SHA-256 `f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97`.
- Source identity: see `manifest.json` and fail-closed source pins in the adapter. Exactly **3 new JP + 2 new USA functions**; existing C always deduplicated.
- No new actual gameplay execution or save modification. Do not treat any Start-skip timing hypothesis as verified by this matching-C promotion.
