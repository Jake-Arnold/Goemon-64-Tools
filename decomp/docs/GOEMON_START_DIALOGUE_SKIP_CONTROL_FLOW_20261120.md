# Gameplay Start input → pause transition → script VM reset (Japanese rev-0 and USA)

**Date:** 20 November 2026  
**Evidence status:** **STATIC_ROM_VERIFIED / RESEARCH_ONLY**. This is not an executed Bomb Text Skip, a matching-C promotion, or a proof that a real successful skip followed this path.  
**Region:** Original Japanese `Ganbare Goemon: Neo Momoyama Bakufu no Odori` revision 0 and original USA `Mystical Ninja Starring Goemon`.  
**Issue:** [#139 — Gourmet Sub savewarp](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/139).

## Evidence and ROM identity

- Japan original expanded, 32 MiB: SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- USA original expanded, 32 MiB: SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original original-MIPS data/code extracted from the pinned `klorfmorf/mnsg` source tree at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original main-segment code ROM offset = guest PC - `0x7FFFF400`.
- A separate read-only verifier authenticated both original ROMs, compared **18 exact instruction anchors in each region** (36 total), and checked the key JAL/branch destinations. **PASS**; Python syntax check **PASS**.
- The inspected functions remain original assembly unless independently promoted in a later G2 build. A static control-flow proof does **not** measure real frame scheduling or guarantee an exploit.

## Correction: former Start lead was not gameplay Start

Japanese `func_800020D8_2CD8` checks Start at `0x8000218C`, but the surrounding path is Controller Pak/menu management. Its related `func_801D1184` invokes `osPfsInit` and PFS state processing. **Retire `0x8000218C` as a presumed Bomb Text Skip breakpoint.** Its input mask alone never established relevance.

## Breakthrough A: the actual gameplay Start gate refuses active scripts

| Operation | Japanese original | USA original |
|---|---|---|
| Gameplay update | `func_8001F610_20210` (252 bytes) | `func_8001F940_20540` (252 bytes) |
| Sample Start input, halfword | `0x8001F63C` reads `0x800CD52C` | `0x8001F96C` reads `0x800C7D3C` |
| Test Start bit `0x1000` | `0x8001F644` | `0x8001F974` |
| Query script active | `0x8001F678` calls `func_8003EE44_3FA44` | `0x8001F9A8` calls `func_8003F1D8_3FDD8` |
| Refuse Start if active | `0x8001F684` branches on nonzero | `0x8001F9B4` branches on nonzero |
| Set transition latch to 1 | `0x8001F6DC`, `0x800CD2D6` halfword | `0x8001FA0C`, `0x800C7AE6` halfword |
| Clear phase byte to 0 | `0x8001F6E0`, `0x800CD290` | `0x8001FA10`, `0x800C7AA0` |
| Invoke phase handler on subsequent latched update | `0x8001F6F4`, `func_8001F750_20350` | `0x8001FA24`, `func_8001FA80_20680` |

The busy-query function is 36 bytes in either region. Japanese `0x8003EE48` loads the **script command cursor** `0x8007D288`; its next branch returns true if nonzero. The USA counterpart `0x8003F1DC` loads `0x80077858`. This check is **script active**, not “text window visibly open”. Other submode and state gates can also refuse Start.

**Implication:** A Start press can be accepted just before the script cursor becomes active, yet be refused once the script starts. This is a concrete code-level explanation for a narrow pre-dialogue input window; it does not by itself prove that a later reset overlaps the Gourmet Sub bomb script.

## Breakthrough B: a normally accepted Start can reach VM reset

| Operation | Japanese original | USA original |
|---|---|---|
| Pause transition function | `func_8001F750_20350` | `func_8001FA80_20680` |
| Phase-0 transition start | `0x8001F798` calls `func_80036660_37260` | `0x8001FAC8` calls `func_800369F0_375F0` |
| Phase-1 completion query | `0x8001F7D4` calls `func_80036578_37178` | `0x8001FB04` calls `func_80036908_37508` |
| Return early if transition pending | `0x8001F7DC` | `0x8001FB0C` |
| After completion, request VM reset | `0x8001F800` calls `func_8003D098_3DC98` | `0x8001FB30` calls `func_8003D428_3E028` |
| Reset wrapper calls resource/VM manager with `a1 = -1` | `0x8003D0A4` (delay slot `0x8003D0A8`) | `0x8003D434` (delay slot `0x8003D438`) |
| Reset dispatch tests `a1 = -1` | `0x8003D10C` | `0x8003D49C` |
| **Clear VM command cursor** | **`0x8003D1C8`** clears `0x8007D288` | **`0x8003D558`** clears `0x80077858` |

**Important guard:** the reset manager checks its global resource-system pointer (`JP 0x8007D290`; `USA 0x80077860`) and may return without clearing when that pointer is absent. The transition completion query must also return zero before the reset wrapper runs. These conditions are original-MIPS verified and must be captured in live testing.

AUDIO NOTE: the additional call `JP 0x8001F6E4` / `USA 0x8001FA14` to a queued system-event helper is not the VM reset. Do not confuse it with the pause-transition state change.

## Relationship to the bomb checkpoint writer

Previously verified original Japanese resource 95 script:
- `+0x263C`: `0x8010` text command, with next word text pointer.
- `+0x2644`: immediately following scripted assignment to `JP 0x80161FF8 = 13` (`USA resource95 +0x350C`, `USA 0x8015C808 = 13`).
- `+0x2654`: assign `JP 0x80162018 = 1`.
- `+0x2664`: assign `JP 0x801620D0 = 0` (Gourmet Sub visited marker).

The VM dispatcher advances the instruction cursor after loading text and can yield in text-wait states 3/4, **before the pending checkpoint assignment**.

### Leading hypothesis (not an observed complete glitch explanation)

1. On a particular update, a one-frame Start press is accepted because the **VM command cursor is still zero**.
2. The gameplay update latches the pause transition.
3. The bomb conversation starts before the pause transition reaches its reset phase; the script command cursor is pending at/near the checkpoint assignment.
4. The phase-1 reset reaches `JP 0x8003D1C8` and clears that command cursor before the index-13 store executes.
5. The previous checkpoint remains intact and survives saving/reloading.

**Static code supports each subsystem action and the allowed ordering, but it does not establish that the timing overlap in steps 3–4 occurs on a real successful Bomb Text Skip.** A different route through Start/input/scene state or a save-buffer discrepancy remains possible. If a successful skip writes index 13 anyway, this mechanism is false/incomplete.

## Falsifiable experiments (original Japanese and counterpart USA)

Record guest instruction PC, update/VI number, both Start-input halfword and transition latch, scene/submode, VM command cursor and state, script resource ID and relocated cursor, save fields, and the resource-system pointer. Do not assume one VM callback equals one video frame.

**Japanese key breakpoints:**
1. `0x8001F644`: gameplay Start recognized.
2. `0x8001F678` / `0x8001F684`: script-busy query and refusal condition.
3. `0x8001F6DC`: Start accepted; transition latch set.
4. `0x8001F7D4` / `0x8001F800`: phase-completion check and VM reset call.
5. `0x8003D1C8`: VM cursor cleared (observe `0x8007D288`).
6. `0x8003D7E0`: generic script immediate writer (observe saved index `0x80161FF8` and fields `0x80162018`, `0x801620D0`).

Compare: normal no-Start bomb dialogue; successful one-frame pre-text Start attempt; one-frame-too-early attempt; one-frame-too-late attempt (expected gate refusal when VM cursor already nonzero). Keep identical precondition save-state and ROM. A definitive result requires proving the index-13 writer is not reached **because of** the reset branch during the successful attempt, rather than merely noting a stale checkpoint afterward. No ROM modifications/saves are required for the read-only breakpoint experiment.

## Matching-C priorities

The program is now sufficiently understood in original assembly that matching C is **not a prerequisite** to testing the causal hypothesis. If doing original-address matching C for maintenance and future investigation, prioritize the 252-byte gameplay Start updater (`JP func_8001F610_20210`), the small script-active query (`JP func_8003EE44_3FA44`), and the script reset wrapper (`JP func_8003D098_3DC98`), then the larger pause-phase handler only if needed. Original-C verification gates, the full-ROM match and CI are independent and have **not** been performed in this research.

## Actual verification and limits

- **PASS:** Japanese and USA expanded ROM 32 MiB hash, 18 exact static instruction assertions per region, JAL targets for VM-busy query, pause-phase handler, reset wrapper and reset manager, and branch target checks; `python -m py_compile`.
- **NOT RUN:** successful gameplay skip, emulator event/watchpoint capture, Controller Pak reload, complete native codegen/matching-C integration, original full-ROM build, relocation/inventory gates, `decomp.local_ci`.
- **No conclusion** that all dialogue/item grant contexts are vulnerable, nor that VM cursor must always clear whenever Start is pressed. This report repairs an overstrong previous Start-handler assumption.


## Isolated original-address matching-C confirmation (20 November 2026)

[Complete original IDO research and deduplicated status](GOEMON_START_VM_NATIVE_MATCH_20261120.md): JP gameplay Start `func_8001F610_20210` 252/252 bytes and busy `func_8003EE44_3FA44` 36/36 bytes; USA gameplay Start `func_8001F940_20540` 252/252 bytes; USA VM-busy function already accepted, 36/36 bytes reverified. These native-exact C implementations confirm the source-level Start gating described above, with no real gameplay frame trace. Three new isolated sources are **not** promoted until the combined G2 gates pass.
