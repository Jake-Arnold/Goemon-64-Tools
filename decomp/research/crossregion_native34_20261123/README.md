# Original USA / Japan cross-region matching-C native replay: 34 isolated exact (research-only)
**23 November 2026.** Original source `stable/decomp@838e9f87c3a860973e9d168b58fcf88bd456bfb4`. Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

34 distinct original-function native IDO 5.3 exact C sources: **33 Japan, 1 USA, 1,364 original instruction bytes**. Independent 34/34 source-mutated native negative controls rejected; replay recompiled in a clean output directory **34/34 PASS** with SGI original IDO 5.3 SHA-256 `76d796...`. Eight function cases also linked at the exact original guest VMA with symbolic globals and `.text : SUBALIGN(4)`. Original ROMs independently SHA-1 verified (USA `6ea0ed71032ce08fc2745f412d84936382197494`, Japan `6f8745fecc3a5e7d4918c7a73353eb0726116ded`).

**29 independently new exact native reconstructions**, plus five Japanese predicates already reported as isolated native matches in the open [research PR #183](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/183); do not double-count them. These original functions are absent from the accepted C partition at the pinned baseline. All C sources, 34 negative control sources, byte-fingerprinted manifest, original GNU linker-symbol maps, exact authenticated-ROM replay source, failed-variant logs and 12 passing manifest tests were delivered **as a source-only ZIP directly in this ChatGPT conversation**. ZIP SHA-256: `8c4adcd1311fe6e1387eeb326f4751a68d9f06120d923268d912aa3affa2373a`. The ZIP is **not in GitHub** and a filename or this pointer is not a substitute for the actual delivered attachment.

This is **ISOLATED_NATIVE / RESEARCH_ONLY**: no exact original regional translation-unit placement, complete 32 MiB original-ROM candidate identity, 7,376 full ELF identity audit, complete all-relocations audit, strict new inventory, new promotion-integrity validation, fresh full `decomp.local_ci` or gameplay was run. The GitHub checkout cannot be cloned from the local shell (GitHub DNS failure). Official counts **unchanged**: USA **2,164 C / 5,199 ASM**, Japan **2,398 C / 4,978 ASM**. The C sources remain unpromoted original ASM in canonical manifests. Do not merge as a matching-C promotion.

## Per-function native evidence index
| Region | Function | Original ROM offset | Bytes | Priority | Isolated proof | Relation to prior work |
|---|---|---:|---:|---|---|---|
| japan_0 | `func_8000A998_B598` | `0xB598` | 40 | A | original bytes | new exact |
| japan_0 | `func_80012180_12D80` | `0x12D80` | 56 | A | original bytes | new exact |
| japan_0 | `func_8001C568_1D168` | `0x1D168` | 52 | A | original bytes | new exact |
| japan_0 | `func_80033988_34588` | `0x34588` | 48 | A | original bytes | new exact |
| japan_0 | `osSyncPrintf` | `0x41130` | 28 | B | original bytes | new exact |
| japan_0 | `func_8004054C_4114C` | `0x4114C` | 28 | B | original bytes | new exact |
| japan_0 | `alLink` | `0x48830` | 36 | A | original bytes | new exact |
| japan_0 | `osAiGetLength` | `0x48A50` | 12 | A | original bytes | new exact |
| japan_0 | `__freeParam` | `0x48B58` | 24 | C | original-VMA single-function link | new exact |
| japan_0 | `alSeqFileNew` | `0x49388` | 64 | A | original bytes | new exact |
| japan_0 | `osGetThreadPri` | `0x4AA60` | 24 | C | original-VMA single-function link | new exact |
| japan_0 | `strlen` | `0x4B6CC` | 40 | A | original bytes | new exact |
| japan_0 | `__osGetActiveQueue` | `0x4C980` | 12 | C | original-VMA single-function link | new exact |
| japan_0 | `__osSpGetStatus` | `0x4CCF0` | 12 | A | original bytes | new exact |
| japan_0 | `__osSpSetStatus` | `0x4D010` | 12 | A | original bytes | new exact |
| japan_0 | `alSaveParam` | `0x51990` | 52 | A | original bytes | new exact |
| japan_0 | `alFxParam` | `0x53054` | 24 | A | original bytes | new exact |
| japan_0 | `func_801ECEC8_5A8E98` | `0x5A8E98` | 32 | A | original bytes | PR_183 |
| japan_0 | `func_801ECEE8_5A8EB8` | `0x5A8EB8` | 40 | A | original bytes | PR_183 |
| japan_0 | `func_801ECF10_5A8EE0` | `0x5A8EE0` | 48 | A | original bytes | PR_183 |
| japan_0 | `func_801ECF40_5A8F10` | `0x5A8F10` | 40 | A | original bytes | PR_183 |
| japan_0 | `func_801ED030_5A9000` | `0x5A9000` | 40 | A | original bytes | PR_183 |
| japan_0 | `func_801F3244_5AF214` | `0x5AF214` | 52 | A | original bytes | new exact |
| japan_0 | `func_801F3308_5AF2D8` | `0x5AF2D8` | 68 | A | original bytes | new exact |
| japan_0 | `func_801F334C_5AF31C` | `0x5AF31C` | 68 | A | original bytes | new exact |
| japan_0 | `func_801F8AAC_5B4A7C` | `0x5B4A7C` | 52 | A | original bytes | new exact |
| japan_0 | `func_802014A0_5BD470` | `0x5BD470` | 48 | C | original-VMA single-function link | new exact |
| japan_0 | `func_802014D0_5BD4A0` | `0x5BD4A0` | 48 | C | original-VMA single-function link | new exact |
| japan_0 | `func_801D9074_603AF4` | `0x603AF4` | 40 | C | original-VMA single-function link | new exact |
| japan_0 | `func_802125D8_67BCC8` | `0x67BCC8` | 48 | C | original-VMA single-function link | new exact |
| japan_0 | `func_80215900_69D000` | `0x69D000` | 76 | A | original bytes | new exact |
| japan_0 | `func_08000AAC_70AE1C` | `0x70AE1C` | 32 | A | original bytes | new exact |
| japan_0 | `func_08001454_734ED4` | `0x734ED4` | 20 | A | original bytes | new exact |
| usa | `func_80035314_35F14` | `0x35F14` | 48 | C | original-VMA single-function link | new exact |

## Next full acceptance gates
Restore complete clean current `stable/decomp` source, original ROMs and upstream/IDO. Stage a nonoverlapping batch **after** checking live manifests, source-unit layouts, relocations, symbol tables and all other open PRs. Before any further IDO native attempt re-read the live `decomp/COMPILER_QUIRKS.md`. Every failed variant remains original ASM. Complete the independent regional original 32 MiB/ELF/relocation/strict-inventory/promotion-integrity/full-local-CI gates, then publish a new reviewed `decomp/*` PR. The five overlapping PR #183 predicates require deduplication.
