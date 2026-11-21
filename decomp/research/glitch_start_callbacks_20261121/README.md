# Glitch Start callback — original-address C research only

Three new complete IDO 5.3 original-address matches (JP 100 B dispatcher, USA 100 B dispatcher, JP 68 B teardown); no G2 promotion. See [the full technical report](../../docs/GOEMON_GLITCH_CALLBACK_NATIVE_MATCH_20261121.md) and root `PROGRESS.md`.

C implementation and verified host tests are in this directory. The complete user-visible source-only research archive `goemon_glitch_native_followup_2026-11-21.zip` includes a standalone original-address compiler/linker/ROM verification script and two explicitly **FAILED_NATIVE** C drafts. The package contains no original ROM, game asset, extracted ASM, ELF/object, proprietary compiler or save data.

The original Japanese dispatcher performs `Table cbs = D_80071210_71E10;` then indirect-calls `((Fn*)&cbs)[g_system_ptr[0x3ADDE]]()`; its USA equivalent uses `D_8006B730_6C330`. Japanese teardown executes two callbacks and sets `g_system_ptr[0x3ADDF] = 1`. All three original extents are 100% IDO-byte-identical at their original VMAs. External host tests exercise only synthetic callback state, not real gameplay.

**Status:** `ISOLATED_EXACT / RESEARCH_ONLY` until full native 32 MiB ROM, ELF identity, semantic relocations, inventory and full local CI complete.
