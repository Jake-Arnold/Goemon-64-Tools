# Cross-region JP N64Recomp leads → exact matching C: 2026-11-16

**Research only. This report does not constitute an integrated decomp promotion.**

## Inputs and verified original-code discovery

- Original USA decompressed 32 MiB SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original Japanese revision-0 decompressed 32 MiB SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- Original pinned `mnsg` source `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, Splat section definitions, generated original USA assembly, original IDO 5.3 `-O2 -mips2 -G 0 -non_shared`.
- Cross-region scanner inspected **69 corresponding executable sections**, parsed **4,810 original USA assembly annotations**, identified **4,372 eligible functions** of at least 32 bytes, of which **303** were uniquely byte-identical for the entire function across regions, **62** ambiguous and **4,007** non-identical. This is a discovery pool, not 303 decompiled C functions, and not exhaustive of the 7,376 original ELF function identities.
- Isolated original-ID0 verification re-run locally and passed for **36/36 original-address C source functions**, **1,744 original instruction bytes per region**; each generated source has pinned SHA-256, correct exact compiler function length, no external relocations and byte-exact code against both hash-verified original ROMs.
- Three of 36, `func_80016660_17260` and `func_80016684_17284`, are **already** USA canonical C; thus **33 newly identified research candidates / 1,616 bytes**. One nonmatching trial `func_801E7398_5A32A8` was explicitly rejected.
- The live canonical USA branch advanced from 307 to **315 verified C functions** during this research, with eight independent file_11 promotions; these new 33 were not part of those eight promoted slices. The upper bound is **348 USA C** *only if* all 33 prove distinct and pass a combined production gate. Japan's independently verified 24 C remain a separate count.

## Verified isolated C function map

Function names and ROM-derived Japanese VMAs are source-verified individual spans, **not** a fixed-offset translation. Every table row reproduced its entire original instruction byte sequence in both regions.

| USA symbol | Segment | Japanese VMA | Bytes | Existing USA C? |
| --- | --- | --- | ---: | --- |
| `func_800133E0_13FE0` | main | `0x80012F70` | 32 | NEW |
| `func_80016660_17260` | main | `0x800161F0` | 36 | EXISTING |
| `func_80016684_17284` | main | `0x80016214` | 40 | EXISTING |
| `func_801F3AD0_5AF9E0` | file_11 | `0x801F8AE0` | 32 | NEW |
| `func_801D600C_6013EC` | file_13 | `0x801DB72C` | 48 | NEW |
| `func_801D603C_60141C` | file_13 | `0x801DB75C` | 48 | NEW |
| `func_801D606C_60144C` | file_13 | `0x801DB78C` | 48 | NEW |
| `func_801D60E4_6014C4` | file_13 | `0x801DB804` | 64 | NEW |
| `func_801D6124_601504` | file_13 | `0x801DB844` | 40 | NEW |
| `func_801D614C_60152C` | file_13 | `0x801DB86C` | 80 | NEW |
| `func_801D61E8_6015C8` | file_13 | `0x801DB908` | 36 | NEW |
| `func_801D6CB0_602090` | file_13 | `0x801DC3D0` | 144 | NEW |
| `func_801D721C_6025FC` | file_13 | `0x801DC93C` | 64 | NEW |
| `func_801D725C_60263C` | file_13 | `0x801DC97C` | 100 | NEW |
| `func_80202A54_62DE34` | file_13 | `0x80208184` | 72 | NEW |
| `func_80202D34_62E114` | file_13 | `0x80208464` | 72 | NEW |
| `func_802138C0_67D2A0` | file_18 | `0x802186A0` | 40 | NEW |
| `func_8021BE14_6857F4` | file_18 | `0x80220BF4` | 36 | NEW |
| `func_8021C2B4_685C94` | file_18 | `0x80221094` | 40 | NEW |
| `func_80225B00_68F4E0` | file_18 | `0x8022A8E0` | 32 | NEW |
| `func_80225D84_68F764` | file_18 | `0x8022AB64` | 32 | NEW |
| `func_80229948_693328` | file_18 | `0x8022E728` | 32 | NEW |
| `func_80210520_697F20` | file_19 | `0x80215318` | 32 | NEW |
| `func_80210A94_698494` | file_19 | `0x8021588C` | 32 | NEW |
| `func_80210F80_698980` | file_19 | `0x80215D78` | 32 | NEW |
| `func_80210FA0_6989A0` | file_19 | `0x80215D98` | 32 | NEW |

| `func_801D619C_60157C` | file_13 | `0x801DB8BC` | 56 | NEW |
| `func_801D825C_60363C` | file_13 | `0x801DD97C` | 52 | NEW |
| `func_80203F5C_62F33C` | file_13 | `0x8020968C` | 44 | NEW |

| `func_8021EE90_688870` | file_18 | `0x80223C70` | 32 | NEW |
| `func_802143E4_69BDE4` | file_19 | `0x802191DC` | 36 | NEW |
| `func_8021B270_684C50` | file_18 | `0x80220050` | 44 | NEW |
| `func_800166AC_172AC` | main | `0x8001623C` | 52 | EXISTING |
| `func_802143A0_69BDA0` | file_19 | `0x80219198` | 48 | NEW |
| `func_80212C38_69A638` | file_19 | `0x80217A30` | 48 | NEW |
| `func_802291F8_692BD8` | file_18 | `0x8022DFD8` | 36 | NEW |

New candidates by segment: **main 1; file_11 1; Impact file_13 15; file_18 6; file_19 4**. The most reusable recovered shapes include linked-node X/Y/Z coordinate adjustments, vector field setters/accessors, floating-point clamping, float decay, and bit-array operations. Internal field names are provisional semantics, not newly established full actor struct layouts.

## Japanese Impact RAM addresses and corresponding code

The USA Impact battle trace on `codex/goemon-impact-research` (`docs/IMPACT_BATTLE_MEMORY_TRACE.md`) identifies a dynamically allocated **controller** and its fields: HP `B+0x60`, Ryo `B+0x64`, oil `B+0x68`, charge `B+0x6C`, where `B` must be read from a valid live controller pointer. It also describes the fixed USA file_13 BSS slot at `0x8020EED0`, *not* a permanent live controller address.

The original Splat layouts place the USA Impact overlay at `0x801CB460` and Japanese Impact overlay at `0x801D0B90`. The original JP file_13 data/BSS section boundary is `0x80214600`. **This boundary has not yet been proven to store the Japanese controller pointer.** Do not infer active JP HP, oil, charge or player fields from that boundary without original load/store cross-references and live RAM confirmation. Do not use a universal USA→JP constant: individual function shifts, overlay BSS positions, data locations and dynamic allocations can differ.

For example, original USA Impact `func_801D721C_6025FC` maps to JP `0x801DC93C`; the distinct `func_801D600C_6013EC` maps to JP `0x801DB72C`. These are executable function VMAs, **not memory watch addresses**. Actual Japanese gameplay watch addresses should be separately logged with observed value changes, sample scene, endianness, type, and source pointer chain; runtime claims require repeated independent evidence. The new 15 Impact C candidates can then be cross-referenced against confirmed controller offset consumers and MIPS references, without confusing model XYZ functions with cockpit resource fields.

## Fail-closed path to promotion and exhaustive coverage

1. Keep source, SHA-256 manifest, original-ROM-only `verify_candidates.py`, and full matching discovery script/report in a local research archive pending source review. No ROMs, original game assembly, generated objects, proprietary compiler or extracted assets go into Git.
2. Deduplicate original symbols against the **315-USA** canonical linked C *and all mixed-overlay stage sources*, plus PR #23/#24. A literal search of the small standalone manifest does not establish complete overlay deduplication.
3. Integrate independent main/file_11/file_13/file_18/file_19 C islands while retaining original assembly, VMA, ROM ranges, object order, linker symbols and semantic relocations. Start with low-risk C in existing file_13 adapter; stage additional overlay adapters separately.
4. Require fresh complete USA `decomp.verify` matching all 33,554,432 bytes, complete original-symbol `decomp.inventory` (7,376 names), linked-overlay and relocation proofs, and the **full** ROM-free `decomp.local_ci`. No function-count increment before every gate succeeds. Japanese matching remains independently gated by Japanese ROM and regional source paths.
5. Expand to all **7,376 original symbol entries**, including short functions and structurally matching but byte-different code. Use the existing `decomp.japan_symbol_reconciliation`/overlay mappings to generate per-function candidates, corroborate Japanese bounds, reject duplicate/common snippets, reconstruct simple C and optimize under finite original-ID0 compiler budgets. Do not claim that structural MIPS normalization proves source code or runtime behaviour.

## Execution provenance

This entry documents a real local original-ROM scan and 36 isolated IDO compiler checks, but **does not claim a new full-ROM build, a 24-C combined verification, a Japanese runtime test, or a compiler-source import into this Git branch**. All source and discovery data are preserved in the separate reproducible research bundle delivered with the findings. Canonical USA manifest, result proofs and inventory are untouched by this documentation commit.

## Additional Impact original-ID0 matches (29-function checkpoint)

Three further previously-unpromoted file_13 functions compiled with exact byte-for-byte original MIPS output under pinned IDO 5.3 against both USA and JP original ROMs: `func_801D619C_60157C` (56 bytes, JP `0x801DB8BC`), `func_801D825C_60363C` (52 bytes, JP `0x801DD97C`), and `func_80203F5C_62F33C` (44 bytes, JP `0x8020968C`). All three have exact individual symbol sizes, no external relocations and pinned source hashes. Full isolated checker now passes **36/36 functions (1,744 bytes)**. Of 23 originally byte-identical Impact discovery spans, **15** have matching C in isolation; eight remain. Two further bounded Impact probes, `func_801D620C_6015EC` and `func_801DF5C4_60A9A4`, were **nonmatching** and remain assembly-owned. No combined-ROM verification or promotion was performed.

## Continued 36-function original-ROM native verification (16 November)

A second original-ID0 bounded pass produced seven exact matching-C functions (296 bytes per region): six **new** isolated USA candidates, and one **already canonical** main-code bit-test `func_800166AC_172AC` (52 bytes). Thus the 36 individual exact matches comprise three already-promoted USA C functions and **33 new USA candidates**, 1,616 original instruction bytes. The original 315-C production proof is unchanged; 348 is a conditional arithmetic upper bound only.

New verified C source files, original ROM VMAs and original source hashes are recorded under `decomp/research/jp_recomp_to_c/` in this draft research branch. The full 36-source, manifest, verifier, 303-candidate discovery and tests bundle is also provided as a separately downloadable source archive; do not count the repo's seven new source files as a new linked promotion.

**New user-provided Japanese runtime data:** `Impact Values.zip` includes three independent read-only value-search exports at `0x802F7060` (1965, one sample), `0x802F7064` (400→396), and `0x802F7068` (140→440). All are guest u32. The latter export is labelled 'impact hp', but its offset is `B+0x68`, corresponding to oil in the established USA Impact controller layout, not the previously named enemy HP at `B+0x60`. This is corroboration of the dynamic field layout in a Japanese runtime, **not** verified JP BSS pointer identity. Detailed audit: `docs/JAPAN_IMPACT_RUNTIME_VALUE_SEARCH_20261116.md`.

**Fresh local checks:** original SHA-1s reproduced for both 32 MiB ROMs; strict original IDO 5.3 codegen and SHA-256 source/size/zero-relocation tests passed **36/36 original named C symbols**, **1,744/1,744 code bytes** per ROM. Seven synthetic exact-scanner tests passed. No production G2/ELF inventory/full local CI was run for this documentation/source-only branch.
