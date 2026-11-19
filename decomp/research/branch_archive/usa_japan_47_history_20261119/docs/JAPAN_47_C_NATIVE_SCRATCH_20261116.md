# Native USA promotion scratch: 47 additional cross-region matching-C functions (16 November 2026)

## Outcome — original ASM baseline + 47 C: PASS

The source reconstructed from the Japanese/USA N64Recomp cross-region audit has passed a complete original-USA native **linker scratch** proof. This is a substantial step beyond isolated C codegen but **not yet formal canonical promotion**.

| Gate | Native scratch result |
| --- | --- |
| Original USA decompressed ROM input | 32 MiB, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` |
| Rebuilt original all-ASM baseline | Byte-for-byte exact |
| New C functions staged in same complete ROM | **47**, 2,220 original instruction bytes |
| Linked candidate full original ROM | **33,554,432/33,554,432 bytes exact**, same SHA-1 |
| Original/candidate ELF positive-sized FUNC identities | **7,376 / 7,376 identical name–VMA–size triples**, no new aliases |
| `file_12` semantic relocation multiset | 7,051 / 7,051 exact |
| `file_13` semantic relocation multiset | 9,589 / 9,589 exact |
| `file_14` semantic relocation multiset | 3,041 / 3,041 exact |
| `file_15` semantic relocation multiset | 1,625 / 1,625 exact |
| `file_17` semantic relocation multiset | 1,739 / 1,739 exact |
| `file_18` semantic relocation multiset | 3,365 / 3,365 exact |
| `file_19` semantic relocation multiset | 1,078 / 1,078 exact |
| New C object function sizes / original code bytes | **47/47 exact** under IDO 5.3 |
| External relocations inside the 47 C objects | **Zero** |
| Original ASM baseline ELF SHA-256 | `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038` |
| Linked candidate scratch ELF SHA-256 | `206d7ca0f79ad58bf37d42f5bb6130e53dc0a4405c4fa978ae9efd6c51c1a859` |

New source allocation: `file_12` 5 C, `file_13` 15 C, `file_14` 8 C, `file_15` 2 C, `file_17` 1 C, `file_18` 9 C, `file_19` 7 C.

## Original boundary and compiler treatment

Starting from the pinned original upstream `mnsg` Splat split, split original assembly **on its known full original function boundaries** and replace exactly the source-owned function spans with original-IDO objects. Leave every other original ASM instruction unchanged. Original IDO C generated 212 bytes of provably zero alignment beyond the 47 named function extents; the Splat ASM fragment assembler generated 316 zero alignment bytes beyond its **original** code extents. These were removed by editing only ELF32 section `sh_size` and `sh_addralign`, never instruction words or original game data. The seven affected overlay `.text` linker collections used MIPS-word alignment 4 to avoid inserting new gaps. The initial untrimmed scratch failed ROM equality; only the corrected trial is reported as PASS.

The script suite `goemon_47_native_promotion_scratch_20261116.zip` reproduces the transformation from a user-owned, exact, already-built original mnsg checkout and the 52-source SHA-256-pinned research archive, without modifying the original checkout. It compiles, trims, links, compares complete game ROM, all 7,376 positive ELF symbols and **full** seven relocation multisets. Individual source files and proof summary are retained in this draft branch. No ROMs, ELF/objects, original extracted assembly or proprietary compiler are committed.

## Deduplication and pending production acceptance

Live canonical production baseline at analysis: `chatgptweb/decomp` commit `7255b2fa59b376c0e03346f434f82d4d02e639e0` = **315 USA matching C / 16,660 bytes**. There are three duplicate already-promoted main helpers in the 52 isolated research results. Of the **49 genuinely new** original-USA isolates, 47 overlay helpers pass this fresh native full-ROM scratch; one additional main helper and one `file_11` helper remain outside this pass. Ongoing `file_11` native PR #41 contains a distinct eight-function candidate batch; this scratch does not reuse that batch.

The **315-C canonical verifier source, manifest and published G2/inventory results remain unchanged.** The authoritative promotion requirement is a fresh **combined** `315 + 47 = 362` original-address C run under `decomp.verify`, complete 33,554,432-byte original ROM, linked overlay relocation and original 7,376 positive function inventory gate, plus full `decomp.local_ci`. Do **not** label this independent 47-C all-ASM native scratch as that combined 362-C proof. The hypothetical **364 C** ceiling requires separately promoting main and `file_11` as well, and rechecking live-branch deduplication. Japanese full-ROM stage acceptance remains separate.

### Source and proof locations

- Git source: `decomp/research/jp_recomp_to_c/src/` — 47 new C files, plus one already-promoted main-code duplicate retained for provenance.
- Evidence JSON: `decomp/research/jp_recomp_to_c/native_scratch_47_evidence.json`.
- Existing cumulative research report: `docs/JP_RECOMP_TO_C_MATCHING_2026-11-16.md`.
- Reproducible local proof scripts and full proof JSON (ROM/assets excluded): `goemon_47_native_promotion_scratch_20261116.zip` delivered as a project research artifact.

This documentation is a **native scratch acceptance checkpoint**. It is not a claim that the user-facing canonical USA production count has increased.
