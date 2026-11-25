# Semantic pass: Impact, player and event callbacks — 25 November 2026

Status: RESEARCH_ONLY (semantic annotations; no matching-C promotion, source renames, runtime changes or new native compiler attempt). Base stable/decomp@ad5c02dbba2a82ac37e94184c5aa82d53bb5561f, authenticated source archive 15020042724 (COMMIT.txt and SHA256SUMS passed). Both private original ROMs independently decompressed to the expected SHA-1: USA 6ea0ed71032ce08fc2745f412d84936382197494, Japan 6f8745fecc3a5e7d4918c7a73353eb0726116ded. All 863 distinct regional candidates in batch302, wave194 and promo367: candidate source SHA-256 and original ROM extent SHA-256 independently checked, zero mismatches. Original overlay ranges from decomp/data/rom_file_inventory.csv. Native verification NOT_RUN (no build inputs changed); canonical ownership unchanged.

## Overlay census

| File | USA | Japan |
|---|---:|---:|
| 11 (player/controller) | 50 | 38 |
| 12 (actor-management) | 21 | 16 |
| 13 (Impact) | 121 | 71 |
| 43 (includes key/lock code) | 31 | 8 |

These are counts by original owner, not counts of named gameplay functions. File 43 is not exclusively key logic.

## Impact (file 13)

Existing docs/IMPACT_BATTLE_MEMORY_TRACE.md identifies USA dynamic controller fields +0x64 (Ryo) and +0x6C (charge). Original MIPS independently examined in both ROMs, not translated by the fixed-save displacement:

* USA 801CEE80 / ROM 5FA260, JP 801D45B0 / ROM 5FF030 (56 B; 13/14 words identical). Both load their own controller slot, add signed argument to +0x6C and clamp to [0,100].
* USA 801D3A68 / ROM 5FEE48, JP 801D9188 / ROM 603C08 (60 B). Both add signed argument to +0x64 and return its value clamped to [0,999].
* USA controller slot 8020EED0, JP 80214600. JP original initializer calls allocator 80014480 at 801D0E78 (size 0x2D0), checks nonzero, stores returned pointer at 801D0EA0 and uses it for template copy. Cleanup reads slot at 801D0D14. This resolves the earlier unproven JP BSS-slot hypothesis (decomp/research/branch_archive/usa_japan_47_history_20261119/docs/JAPAN_IMPACT_RUNTIME_VALUE_SEARCH_20261116.md). Slot is overlay-scoped, not permanently valid; no JP runtime liveness claim. Never infer a dynamic heap address.

Newly accepted paired callbacks (all in today's native G2 manifests; compare corresponding original extents and actual recovered C):
| USA VMA / ROM | JP VMA / ROM | bytes each | confirmed conditional effect |
|---|---|---:|---|
| 801EA614 / 6159F4 | 801EFD44 / 61A7C4 | 284 | +4 charge; +5 Ryo if helper result >=60; position-based effect and scaled model |
| 801EA900 / 615CE0 | 801F0030 / 61AAB0 | 376 | +4 charge, conditional +5 Ryo, increments model halfword +0x16 by 3; interaction predicates and positive-height early return |
| 80203AE4 / 62EEC4 | 80209214 / 633C94 | 220 | +4 charge, conditional +10 Ryo, interaction-dependent effect |
| 80203DFC / 62F1DC | 8020952C / 633FAC | 352 | +4 charge, conditional +5 Ryo; similar conditional effect path |
| 80205C00 / 630FE0 | 8020B330 / 635DB0 | 356 | +10 charge, conditional +20 Ryo on second branch; counter decrement on two branches, one branch retires without reward |

Source files in decomp/research/{batch302,wave194}_20261125/sources/{usa,japan_0}/<original symbol>/candidate.c. The specific enemy/projectile and trigger meaning of the predicates (including the >=60 helper) remain unresolved; these are reward/effect callback hypotheses, not safe game controls.

## Player controller (file 11)

USA func_801E75D4_5A34E4 / JP func_801EC6FC_5A86CC (464 B, 93/116 original words identical), accepted in wave194. Four-way selector at actor +0x60. In case 0 it calls USA 801DCCF0 / JP 801E2130 with -10, clears flag bit 0 and nested state, resets floats and passes action ID 0x82. Cases 1/2/3 pass 0x8E/0x9B/0xAA. Case 2 writes 2.5f to +0xA4 and calls the previously accepted scale-related helper USA 801E3278. Original direct MIPS for 801DCCF0 (ROM 598C00) and 801E2130 (ROM 59E100) adds signed 16-bit argument to 32-bit Ryo word USA 8015C5E8 / JP 80161DD8, tests signed low halfword, floors negative to zero and caps >=10000 to 9999. Existing reviewed toolkit catalogue labels USA 8015C5E8 as Ryo and JP 80161DDA as its low halfword; full word location now independently instruction-traced. The selected state therefore deducts 10 normal-game Ryo. Exact gameplay event (damage, action cost, etc.) is unverified. No generalized clamp claim outside normal game input range.

## File 51 saved-event dependent actor

New USA func_08000174_70D8B4 (356 B) is a conditional actor update in resource 51. It tests bank-C event 0 (Super Pass-related prerequisite) via 800240DC, changes actor update path, and consumes actor +0x68 bit 0x4000 to set bank-A flag 0. When the bank-A test succeeds it clears actor +0x60 bit 0x10000000, selects action 0x43 or 0x44 from +0xD8, and registers callback at overlay +0x88. Existing decomp/docs/PHASE1_SAVED_EVENT_FLAG_TRACE_20261117.md identifies resource 51 gate-bit-1 readers and the independent Super Pass -> gate event chain. New actor function is a strong gate-related candidate, but tests event 0 rather than gate-open event 1; exact object identity unverified. Independently compared JP same resource offset +0x174 (ROM 711DE4): 73/89 original words equal; original bank-C test 80023D9C at overlay +0x190, bank-A set 80023AB0 at +0x1D0, bank-A test 80023B54 at +0x1FC, same literal flag 0. JP counterpart is original-MIPS identified, not promoted matching C by this work. VMA 08000174 is ambiguous without overlay ownership. Related new USA callbacks +0x0, +0x4AC, +0x598 modify actor flags and dispatch updates; +0x598 tests bank-A flag 1, not saved gate flag 1.

## Other reviewed functions

Main USA 8000D4E0 / JP 8000D230 (396 B, 91/99 words equal) and USA 8000D79C / JP 8000D4EC (380 B, 87/95 words equal): complementary three-mode rectangle/interpolation progression; signed halfwords +0x64..+0x6A advance by +/-20 and +/-10; float +0x44 advances to one or zero. Original USA 8000D918 computes geometric interpolation; completion 8000D66C sets +0x30 to 4, reverse completion invokes 8000C878. Likely window/visual transition; not established as scene loader.
USA 80212010 / ROM 670FC0 (492 B) is 39 calls to accepted menu resource record reset 800102E0 (56 B), which clears fields in a 16-byte indexed record when index != -1. Large but repetitive resource cleanup, not complex gameplay.

## Verification and limitations

Original expanded ROM SHA-1 and all 863 original code/source SHA-256 comparisons passed; original MIPS helpers and JP resource 51 counterpart disassembled with archived MIPS binutils. No new IDO compilation, full candidate ROM rebuild, emulator run, memory write, source rename or toolkit change. Existing canonical proof and counts USA 2939 / JP 2842 unchanged. Proposed names are descriptive research aliases, not source-symbol changes. Need original caller/actor-registration mapping and read-only event traces to resolve exact actor identities; verify JP pointer only during file 13 ownership. No universal overlay offset rule.
