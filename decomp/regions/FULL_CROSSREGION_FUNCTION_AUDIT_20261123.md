# Complete original-ROM USA ↔ Japan function audit (23 November 2026)

**RESEARCH_ONLY.** Canonical source baseline `838e9f87c3a860973e9d168b58fcf88bd456bfb4`. No matching-C promotion from this research.

This audit independently authenticated both USA and Japan-0 original expanded 32 MiB ROMs, recovered **all 7,376 positive-size original ELF function identities per region**, and computed original-ROM code hashes and opcode/register structure signatures for **all 14,752** original functions. The USA baseline rebuild was fully byte-exact. Japanese symbol identities were obtained from an original-ASM-only **relaxed-link research ELF**; it is **not** a native full-ROM G2 candidate and was never counted as such. Original Japanese instruction fingerprints came only from the independently SHA1-authenticated Japanese expanded retail ROM.

## Canonical ownership (live post-JP28)

- USA **2,164 accepted matching C / 5,199 remaining ASM**.
- Japan **2,398 accepted matching C / 4,978 remaining ASM**.
- The **13** historical USA unmarked positive original ELF functions stay separate from remaining ASM; two original-code donor hints for that category are excluded.

## Signature coverage

| Class | USA | Japan |
|---|---:|---:|
| Byte-identical unique | 677 | 677 |
| Byte-identical ambiguous | 442 | 441 |
| Same MIPS instruction/register skeleton unique | 4,447 | 4,447 |
| Same skeleton ambiguous | 1,541 | 1,546 |
| No such signature match | 269 | 265 |
| **All original functions** | **7,376** | **7,376** |

A separate bounded fuzzy opcode-sequence/neighboring-region analysis classified all 534 no-signature cases as *heuristic only*. No original-code semantic correspondence is claimed by an offset shift.

## Full available-C donor shortlist

**583 distinct currently ASM-owned destination functions have at least one existing, already accepted C donor in the other version:** **405 USA**, **178 Japan**. The priority tiers are code-change heuristics **not** proof that C translation will be easy:

| Priority | USA | Japan |
|---|---:|---:|
| A: exact code, uniquely paired | 1 | 27 |
| B: exact code, multiple donors | 4 | 4 |
| C: same skeleton, one differing MIPS immediate | 40 | 11 |
| D: same skeleton, 2–4 operand differences | 108 | 17 |
| E: same skeleton, 5–8 operand differences | 133 | 45 |
| F: more than 8 differences, unique | 31 | 16 |
| G: same skeleton, multiple possible donor identities | 88 | 58 |

Existing source-only PRs #183/#184 include prior isolated native exact C evidence; do not recount them. The 28 new Japanese canonical C from `838e9f87c3a860973e9d168b58fcf88bd456bfb4` were excluded as remaining ASM before generating this final shortlist.

### Source-only delivery

The comprehensive same-chat downloadable ZIP contains every original function's source/target identity and canonical accepted ownership, the 583 ranked exact/structural donor destinations, all 5,124 uniquely paired code signatures, raw ambiguity reports, 534 fuzzy no-match evaluations, eight passing metadata consistency tests, and replay scripts. No ROM, compiler, original assembly bytes, game assets or ELF binaries were uploaded.

Use `python3 -m decomp.region_crosswalk_lookup --audit /path/to/extracted/crossregion_audit --region usa --rom 0x35EAC` to query the source-only CSVs in both directions; lookups are explicit original ROM offsets, never the fixed-data-global `+0x57F0` heuristic. The previous 118-link PR #186 is a subset of documented native donor ports; the new audit distinguishes ambiguous and unaccepted counterparts.

**Native promotion gates NOT RUN for the 583 new destination attempts:** original SGI IDO 5.3 compile, original-translation-unit and ABI checks, complete region-specific 32 MiB ROM identity, 7,376 original ELF identities, original relocs, strict inventory, promotion integrity and full `decomp.local_ci`. Their official accepted-C contribution is **zero**.
