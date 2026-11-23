# Japan-0 C-Right call graph — 60-byte system-state reset reconstructed

**Research status: PASSED_COMBINED_2371_RESEARCH_ONLY. Official Japan accepted count stays 2,370.**

## Exact new C function

- Original name: `func_80004170_4D70`
- ROM region: Japan-0, original *expanded* ROM offset `0x4D70`, linked guest VMA `0x80004170`
- Function length: 60 bytes / 15 original MIPS instructions
- Direct caller: original `func_80212C50_5CE1E0` at `0x5CE1E0` (already accepted C in `jp1686`; PR #178 closed as duplicate ownership)
- Data: `g_system_ptr` global at guest `0x80161DB8`; the routine writes zero to **16 single-byte entries**, spaced 16 bytes, beginning at pointer-relative `+0x3B168`. This offset is **not** a fixed RAM address or proof of the C-Right stage `+0xD1` flag's meaning. The other 15 bytes per record are untouched.
- Exact source: `source/func_80004170_4D70.c`; source SHA-256 `d59c3bfbd24ae69e442f47ee0bc95ac7571dd4b0e1e1e9dd93b93409435e2b5d`.
- Native SGI IDO5.3 source order matters. The failing `negative_schedule_v1.c` has the same loop semantics but its store and pointer increment appear in different instruction slots; first original-vs-candidate mismatch ROM `0x4D98`. The exact v2 advances pointer then stores via `p[-16]` to reproduce the original branch-delay-slot instruction. **Compiler finding: EXISTING_QUIRK_REPRODUCED** (source scheduling); negative source archived.

## Three levels of verification (do not conflate)

1. **Native original function:** SGI IDO5.3 (`-O2 -mips2 -G 0 -non_shared` original flags) 15/15 code instructions original. Both HI16/LO16 relocations against `g_system_ptr` exact after linking.
2. **Independent original-ASM baseline:** full Japan original all-ASM 33,554,432/33,554,432 ROM bytes exact (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`); 7,376/7,376 ELF function identities; 80,810/80,810 ELF semantic relocation tuples exact. One mixed original C/ASM translation unit must preserve four subsequent ASM functions. Its last ASM owner has original FUNC size 1488B; asm-processor incorrectly records 1492B by including four trailing zero padding bytes. The exact generated-object metadata workaround modifies only one byte of the final FUNC `.st_size`, from 1492 to 1488, after validating the 4 padding bytes, the original ASM `.NON_MATCHING` size, the precise native object SHA and all ELF section/symbol invariants. It **does not** patch code or relocations. See `stage_and_verify.py`.
3. **Full accepted Japanese CRight combined:** freshly rebuild the 2,369-C accepted Japanese baseline (all native CI gates PASS), then the 2,370-C historical CRight dual-reference build (32MiB ROM exact; all 7,376 ELF identities; 80,745 semantic relocations). Add **only the reset16 C** via the stage/metadata/relink script. Candidate is 2,371 C and **every one of the 80,745 complete ELF relocations equals the accepted 2,370-C predecessor**, exactly, fingerprint SHA-256 `43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0`. Complete original 32MiB ROM and 7,376 ELF functions remain identical. Clean independent private replay of the source-only stager also passed. New C-owned identity set = `{func_80004170_4D70}`, none removed. Candidate original C bytes 127,068, remaining ASM 5,005. The existing CRight Splat-original 80,747-to-dual-original-ASM 80,745 provenance finding is inherited, not newly waived.

**No production promotion yet:** current `stable/decomp` canonical manifest/combined/inventory were NOT updated; the full current-stable branch `decomp.local_ci` has NOT been run in the clean stable checkout. Full local CI in the *historical source checkout* passed exit 0, **not** substitute for the current-stable gate. All exact build evidence is local research until a fresh stable-based promotion transaction and PR are reviewed.

## Calls and other assembly-owned functions

```
[already accepted] func_80212C50_5CE1E0 60B stage handoff
  +-- [NEW EXACT C RESEARCH] func_80004170_4D70 60B: clear 16 x 16B-stride records
  +-- [ASM] func_8000339C_3F9C 88B: updates g_system_ptr+0x3ADDE/+0x3ADDF; invokes func_800032A4_3EA4

[already accepted] 374 overlay file_12 template wrappers, 36B each
  +-- [ASM] func_80013654_14254 80B: iterate 16-bit record IDs
         +-- [ASM] func_800136A4_142A4 248B: per-ID resource/registration call

[ASM] func_80212BD0_5CE160 128B: stage periodic callback
[ASM] func_800041AC_4DAC 48B: clear one indexed record's first byte
[ASM] func_800041DC_4DDC and func_80004224_4E24 72B each: set resource record fields
```

**Deduplication correction:** The 374 wrapper functions and original stage handoff are already accepted in the previous `jp1686` source set; replacing them in original assembly generates an independently matching ROM, but **zero new canonical ownership**. The previous research PR #178 incorrectly called the handoff new and has been closed transparently. Only `func_80004170_4D70` is novel in this research batch.

## Failed IDO controls (retain ASM)

- 48B `func_800041AC_4DAC`, 14 bounded native attempts (`source/negative_slot_v01.c` through `negative_slot_v14.c`): none produced exact original code; earliest nonrelocation differences are register allocation, expression offset encoding or instruction scheduling. **EXISTING_QUIRK_NOT_APPLICABLE**. No C ownership change.
- 88B `func_8000339C_3F9C`, two native attempts: wrong length/constant scheduling; **NO_NEW_COMPILER_FINDING**.
- 80B `func_80013654_14254` (resource registration loader), one native attempt: 84B vs original 80B / branch scheduling mismatch; **NO_NEW_COMPILER_FINDING**.
- 128B `func_80212BD0_5CE160` (stage periodic callback), one native attempt: 132B vs original 128B; **NO_NEW_COMPILER_FINDING**.
- Earlier failed 76B and 104B overlay stages are preserved in issue #174 and historical closed PR #178; no new exact native match asserted for those.

All compiler attempts, source hashes, first mismatches and negative source files appear in `evidence/native_variant_audit.json`. No new reusable compiler quirk is asserted. Pure host tests use synthetic buffers only. User Project64 normal versus held live trace indicates stage `+0xD1=0` versus `1` after loading, but no verified original code reader and no freeze cause; **this is not a game patch**.

## Reproduce (private original ROM/compiler required)

The downloaded archive carries **NO ROM, extracted original ASM, ELF, object, savestate, raw memory trace or compiler binary**. The script stages all four necessary ASM fragments from the user's authenticated *private* original JP2370 build; do not check these resulting private files into Git.

```bash
# Requires pinned original mnsg, actual SGI IDO5.3, MIPS GNU binutils,
# private Japan retail/expanded ROM and verified original JP2370 combined build.
python3 -m unittest discover -s tests -p 'test_*.py' -v
bash tests/run_host.sh

# Creates a NEW isolated candidate copy and verifies complete ROM/ELF/relocs.
# Arguments: accepted build, nonexistent scratch target, deps, runtime, repo source.
bash run_private_native.sh /PRIVATE/JP2370 /PRIVATE/JP2371-new \
  /PRIVATE/goemon-dependencies /PRIVATE/goemon-runtime-additions /PRIVATE/Goemon-64-Tools
```

Native compiler/flags and padded source-object SHA are pinned; stager rejects changed original code/symbols, altered original ROM, duplicate/stale stage, forged C ownership and relocation/ELF mismatch. This does not constitute a canonical `stable/decomp` promotion.

## Original USA/Japan fixed-global crosswalk (23 November 2026 review follow-up)

The original Japan reset routine reads its fixed 32-bit `g_system_ptr` slot at guest `0x80161DB8`. The different original USA initializer at the same named function address writes its 32-bit `D_8015C5C8_15D1C8` slot at guest `0x8015C5C8`. Their fixed **slot** addresses differ by exactly `+0x57F0`. Both retail ROM SHA-1 identities and original MIPS LUI/LW vs LUI/ADDIU/SW register/operand forms were independently checked, not inferred solely from the offset. See [CROSSWALK.md](CROSSWALK.md), [crosswalk.json](crosswalk.json), [sanitized opcode proof](original_rom_pointer_proof.json), and [ROM-gated verifier](verify_rom_pointer_slots.py). Run its eight host tests with `python3 -m unittest discover -s tests -p 'test_rom_pointer_slots.py' -v`. The dynamic `g_system_ptr+0x3B168` pointee field is **not** an independently fixed guest address or evidence of matching USA/Japan pointee structure layouts. No live gameplay pointer-value correlation, read/write automation, or freeze-cause claim is established.
