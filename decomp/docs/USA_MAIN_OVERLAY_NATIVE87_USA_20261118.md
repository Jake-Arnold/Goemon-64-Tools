# Original-USA main and overlays 13–20: 87 additional native-exact C candidates

**Date:** 18 November 2026. **Status:** `RESEARCH_ONLY`. Branch `chatgptweb/decomp`. This research extends the prior completed numbered-code resource-24–80 sweeps into the **main executable segment and the seven larger non-numbered overlays 13, 14, 15, 17, 18, 19 and 20**.

## Result

**87 new original-address native-exact C functions, totalling 912 original instruction bytes.** This total excludes four 8-byte no-op functions already accepted in production: `func_80035D84_36984`, `func_80037DB0_389B0`, `func_8003EA0C_3F60C`, and `func_8003EBA4_3F7A4`. Independent deduplication used the live **864-function** canonical `decomp/results/combined.json` list, not merely a search over the manifest text.

The exact-match breakdown is **62 no-op callbacks, 13 32-bit actor-field writes, four 32-bit field reads, and eight typed constant-field writes**. These are original distinct positive-sized function identities, not created aliases. All original names, ROM offsets and guest VMAs are present in the 87 committed C filenames, with complete original-code hashes and per-function metadata in the reproducibility ZIP.

The main-code additions comprise **12 functions / 120 bytes**, sourced from `E000.s`, `10D80.s`, `12760.s`, `204B0.s`, `35280.s` and `37440.s`. The other **75 functions / 792 bytes** cover the original ASM text source files `5F6840.s` (file13), `63A2B0.s` (file14), `65E310.s` (file15), `66C250.s` (**file17**, not 16), `676C80.s` (file18), `694CA0.s` (file19), and `69CBD0.s` (file20). Resource-to-overlay mappings were checked against the original linker script. No fixed RAM global or Japanese memory address was inferred or changed.

## Exact original-code proof

All 87 candidate C functions compiled with the original pinned **IDO 5.3** compiler and the actual `-O2 -mips2` flags, linked at the original USA guest addresses, and passed **87/87 exact MIPS code-byte comparisons**. Scratch source was introduced into a *separate disposable pinned upstream* checkout of `klorfmorf/mnsg`, commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Existing unaffected ASM remained original. Only verified-zero linker/assembler alignment padding was trimmed, with guards against relocations into trimmed padding; original instruction bytes were not patched.

The scratch build with all 87 new C functions simultaneously passed:

| Original-compatibility check | Fresh result |
| --- | --- |
| Complete decompressed USA ROM | **33,554,432/33,554,432 bytes identical** |
| SHA-1 of both originals and candidate | **`6ea0ed71032ce08fc2745f412d84936382197494`** |
| Original positive-sized ELF FUNC identities | **7,376/7,376 exact** |
| Original `.rel.main` semantic relocations | **15,058 exact** |
| Original file13/14/15/17/18/19/20 relocations | **9,589 / 3,041 / 1,625 / 1,739 / 3,365 / 1,078 / 68 exact** |
| Total changed-section relocations | **35,563 original entries preserved** |
| Host actual-source regression | **87/87 PASS under GCC AddressSanitizer + UndefinedBehaviorSanitizer** |

The committed `decomp/research/usa_main_overlay_87_20261118/test_actual87.c` is **byte-identical (Git blob `7309f9a016b13830674819627b75ef97e01d6609`)** to the actual host sanitizer test executed locally. It calls and verifies every compiled candidate, including 32-bit field offsets, return values, typed constants and no-op branches. Unlike earlier actor-pointer tests, this fixture requires **no alignment-sanitizer exception**.

## Files and verification boundary

Every matched C source is committed separately under `decomp/research/usa_main_overlay_87_20261118/sources/`. The report `decomp/results/usa_main_overlay_native87_upstream_scratch_20261118.json` records the numeric gates, precise original-ROM hash, source categories, deduplication and unexecuted production gates. A standalone source/archive bundle **`goemon_main_overlay_native87_20261118.zip`**, produced from the identical local matched C source files, includes full per-function source/original-code SHA-256 hashes, source index, original-address IDO replay, disposable upstream staging scripts, exact-ROM proof and the executed host regression. It contains **no ROMs, ASM extraction, proprietary compiler binary, game assets, save, or RAM dump**.

**Important acceptance boundary:** The successful whole-ROM test used a disposable **original upstream** source tree; it is **not** the live `chatgptweb/decomp` source tree with 864 accepted USA C functions. The current repository checkout cannot be fully and authentically materialized in the native compiler container because shell GitHub DNS access fails; GitHub connector access and the original upstream checkout are available, but are **not interchangeable**. Thus canonical 864+87 `python3 -m decomp.verify`, strict `decomp.inventory`, branch-original ELF/relocation proof and full `decomp.local_ci` are **NOT RUN** for this batch. No manifest/production source, inventory, accepted matching-C count or production verifier was modified. Do not report these 87 as production accepted.

At the time of this pass, accepted production remains **864 USA / 39 Japan**, with **37,904 accepted USA C instruction bytes** and **6,499 USA assembly entries remaining**. The 87 candidates would potentially bring the USA figure to **951** *only after* a full, separate canonical promotion. Preserve other research-only resources 24–80 without double-counting them.

**Next acceptance step:** materialize and authenticate a complete live decomp checkout, stage the 87 verified source files with all existing accepted C, then run the entire unchanged 32 MiB ROM, native linked symbol, relocation, strict inventory and full local CI gates. Retain original ASM for any failed candidate.
