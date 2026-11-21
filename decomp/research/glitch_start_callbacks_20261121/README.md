# Glitch Start callback — original-address C research only

Three new complete IDO 5.3 original-address matches (JP 100 B dispatcher, USA 100 B dispatcher, JP 68 B teardown); no G2 promotion. See [the full technical report](../../docs/GOEMON_GLITCH_CALLBACK_NATIVE_MATCH_20261121.md) and root `PROGRESS.md`.

C implementation and verified host tests are in this directory. The complete user-visible source-only research archive `goemon_glitch_native_followup_2026-11-21.zip` includes a standalone original-address compiler/linker/ROM verification script and two explicitly **FAILED_NATIVE** C drafts. The package contains no original ROM, game asset, extracted ASM, ELF/object, proprietary compiler or save data.

The original Japanese dispatcher performs `Table cbs = D_80071210_71E10;` then indirect-calls `((Fn*)&cbs)[g_system_ptr[0x3ADDE]]()`; its USA equivalent uses `D_8006B730_6C330`. Japanese teardown executes two callbacks and sets `g_system_ptr[0x3ADDF] = 1`. All three original extents are 100% IDO-byte-identical at their original VMAs. External host tests exercise only synthetic callback state, not real gameplay.

**Status:** `ISOLATED_EXACT / RESEARCH_ONLY` until full native 32 MiB ROM, ELF identity, semantic relocations, inventory and full local CI complete.


## 21 November 2026 — complete contiguous Japanese gameplay callback unit

`jp_gameplay_callback_four_combined.c` combines **all four** original functions in ROM `0x20180..0x2034F` (exclusive end `0x20350`) as one source unit, and `verify_combined_japan.py` authenticates the original JP 32 MiB ROM, compiles with original IDO 5.3, links at the exact original VMA, and requires **464/464 bytes, 116/116 instructions**, original code SHA-256 `95030527ce8cf70a35cd44ebf1d7f7c85b8267b277765557ac02b62c671c0062`. The same exact source bytes were verified by Git blob SHA `cec3a40a22261488825972498e12d31bf9f69766`. This is **ISOLATED_EXACT / RESEARCH_ONLY**, not a full-ROM-G2 promotion. Two functions in the unit were already matched in previous research; net new is still JP +2/168 B, USA +1/100 B. Full source research archive `goemon_glitch_native_followup_v2_2026-11-21.zip` SHA-256 `9cb7b39c3a9980ba9e8c5399975fc8a771126fd969a0a205a6488b7575088131`.
