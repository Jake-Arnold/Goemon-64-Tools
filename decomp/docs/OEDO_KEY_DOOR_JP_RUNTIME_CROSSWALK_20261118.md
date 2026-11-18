# Oedo silver key / door: USA research crosswalk and Japanese Project64 runtime confirmation

**18 November 2026 — RESEARCH_ONLY.** This note records the incremental Japanese evidence **without re-counting the already documented USA discovery**. It does not change toolkit save writes, accepted C, production manifests, `main`, or any live game state.

## What was known before this session

- [USA key/lock code trace](../../docs/KEY_LOCK_CODE_TRACE.md) (3 November) already identified file-43 key respawn, pickup and door checks: key actor `+0xD4` = collected event; door actor `+0xD4` = opened event and `+0xD6` = required-key event.
- [USA Oedo room definitions](../../docs/OEDO_SILVER_KEYS.md) already identified the **second** silver key `0x114` and map-13 lock `0x113`, as well as the distinct first key `0x110` and lock `0x10F`. The displayed carried-key count remains unresolved.
- [Independent paired saved-bank research](USA_JAPAN_SAVE_EDITOR_EVENT_FLAG_CROSSWALK_20261117.md) established USA bank C `0x8015C608` and JP rev-0 bank C `0x80161DF8` with `+0x57F0`, and the independently read original regional set/clear/test routines. **This is not a universal address translation.** Banks A/B have a different displacement.
- [Paired actor-definition loader research](PHASE1_ROOM_ACTOR_DEFINITION_COPY_USA_JP_20261117.md) already described the shared definition-word transfer to live actor parameters in both ROMs. This session did not rediscover that loader.

## New evidence: Japanese gameplay reaches the original file-43 callers

The user ran a **read-only Project64 interpreter** event-hook script on the Japanese ROM. During pickup the script reported scene `0x012` and set saved ID `0x114`; during door interaction it reported scene `0x00D`, tested `0x113` and `0x114`, then set `0x113`. The native setter wrote the packed byte in two successive transitions:

| Event | Flag | JP byte/mask | USA corresponding byte/mask | JP observed byte |
| --- | --- | --- | --- | --- |
| Key pickup | `0x114` | `0x80161E1A / 0x10` | `0x8015C62A / 0x10` | `0x00 -> 0x10` |
| Door unlock | `0x113` | `0x80161E1A / 0x08` | `0x8015C62A / 0x08` | `0x10 -> 0x18` |

The earlier user report mentioned scene `0x018` for a key pickup; the **actual MIPS-hook capture is scene `0x012`**. Do not conflate these scene identifiers or claim to have resolved why they differed. One scene-`0x00D` test for ID `0x104`, and several clears of ID `0x082` in other bytes, were also observed and **are not assigned silver-key semantics**.

Crucially, Project64 returned caller addresses such as **`0x08000610`**, **`0x0800106C`**, **`0x080010B0`**, **`0x080010C0`** and **`0x080010D0`**. They are **actual original MIPS return PCs in overlay `file_43`**, not malformed main-code PCs and not script cursor addresses. The following original instruction sites corroborate them:

| Runtime action | Original JP caller / flag source | JP expanded-ROM site | Captured return PC |
| --- | --- | --- | --- |
| Set picked-up key `0x114` | `0x08000608` call; `lhu a0, +0xD4(s0)` in delay slot | `0x6F8198` | `0x08000610` |
| Test door-unlocked ID `0x113` | `0x08001064` call; argument loaded from door `+0xD4` | `0x6F8BF4` | `0x0800106C` |
| Test required-key ID `0x114` | `0x080010A8` call; argument loaded from door `+0xD6` | `0x6F8C38` | `0x080010B0` |
| Repeat required-key test | `0x080010B8` call; `+0xD6` in delay slot | `0x6F8C48` | `0x080010C0` |
| Set opened-door ID `0x113` | `0x080010C8` call; `+0xD4` in delay slot | `0x6F8C58` | `0x080010D0` |

The **bank-C store** in JP is at `0x80023D44` (inside `func_80023CF8`); the trace observed the store with old/new byte `0x00/0x10` and `0x10/0x18`. This confirms the **native computed-ID actor route**, previously a static lead for other actor types, for these two particular Japanese Oedo interactions. It does **not** prove the runtime dispatch of every actor that uses this overlay.

## Original overlay functions and the lock-visual observation

JP `file_43` has expanded-ROM base `0x6F7B90` and logical overlay guest VMA base `0x08000000`. The following **original machine-code spans**, not original Konami C, were rechecked against the authenticated JP 32 MiB ROM:

| Original JP function | Relative overlay VMA | Expanded ROM offset | Size | Role |
| --- | --- | --- | ---: | --- |
| `func_080001BC_6F7D4C` | `0x080001BC` | `0x6F7D4C` | 96 | Key no-respawn gate, tests actor `+0xD4` |
| `func_0800058C_6F811C` | `0x0800058C` | `0x6F811C` | 328 | Silver key pickup and flag set |
| `func_08000AA8_6F8638` | `0x08000AA8` | `0x6F8638` | 1400 | Door initialization, saved-lock test, object/callback setup |
| `func_08001020_6F8BB0` | `0x08001020` | `0x6F8BB0` | 536 | Door use, required-key check and lock set |

**All four original function SHA-256 checks passed** against the Japanese expanded-ROM input, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. The corresponding USA decomp already identified the key initialization at ROM `0x6F369C`, pickup at `0x6F3A6C` and door use at `0x6F4500`. Do not use the saved-RAM `+0x57F0` offset to translate these original code offsets or overlay VMAs.

The JP door initializer tests actor `+0xD4` and follows **different callback/visual setup branches** for set versus unset lock state. The interaction handler separately checks the **current persistent bit**. This is a stronger original-instruction explanation of the user observation that clearing the bit immediately blocks entry yet the visible lock reappears only after reloading the scene. Precise renderer lifetime and teardown remain untraced.

## Reusable cross-region read-only trace

The adjacent research scripts `oedo_key_door_usa.js` and `oedo_key_door_japan_0.js` are **region-pinned**, use the three native flag entry PCs and only the relevant event byte, and support both **legacy `gpr`** and **newer `cpu.gpr`** register APIs. They register **only targeted callbacks** (no `ADDR_ANY`/all-instruction hooks), never pause execution or mutate memory, and log IDs and caller return PCs. Use the interpreter core and stop other active debugger scripts first. These new scripts are based on the successful legacy-API approach, but **the published region-generalized versions were host-mock tested, not independently run in Project64**. The separate USA variant has **no new live USA capture**.

## Verification boundaries

- **Performed in this research:** local SHA-1 verification of the supplied Japanese normalized retail ROM and original 32 MiB JP expanded ROM; local SHA-256 checks of the four original JP function spans; inspection of original MIPS at the five JP overlay callsites; review of prior USA/JP decomp records; four synthetic API tests for the two new tracers (`node test_oedo_key_door_mock.js`).
- **User-provided runtime evidence:** JP Project64 v5 read-only execution trace, pickup `0x114` and lock `0x113` with exact caller return PCs and bank-C writes. Sanitized summaries only; full private trace, saves and raw ROM data are **not committed**.
- **Not performed:** new USA gameplay execution, independent JP gameplay replay by the assistant, native IDO compilation of the four actor functions, whole-ROM original-address build, relocation/ELF/inventory acceptance, or full `decomp.local_ci` from a complete GitHub checkout. No new matching-C acceptance or toolkit write authority is claimed.
- **Remaining:** locate the displayed carried-key counter/derivation; detail the door animation teardown/update path; determine whether an individual JP scene `0x018` pickup is a distinct context; identify the owner of unrelated flag `0x104` check at scene `0x00D` before assigning semantics.
