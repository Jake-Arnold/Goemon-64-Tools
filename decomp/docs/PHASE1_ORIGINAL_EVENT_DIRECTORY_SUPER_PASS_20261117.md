# Phase 1 follow-up: native event directory, Super Pass acquisition, guard flags (2026-11-17)

**Evidence tier:** Original USA NG5E and Japanese rev-0 NG5J *decompressed ROM* instruction/data anchors, with separately reported Japanese gameplay corroboration for gate flag `0x001`. **Not** a game-runtime instruction trace or matching-C promotion. Flag names from the third-party editor remain annotations unless corroborated by source/runtime evidence.

## Regional ROM evidence

| Region | Original 32 MiB ROM SHA-1 | Native event pointer table VMA / decompressed ROM offset | s16 resource-number table VMA / ROM offset |
| --- | --- | --- | --- |
| USA | `6ea0ed71032ce08fc2745f412d84936382197494` | `0x800779A0 / 0x785A0` | `0x80078608 / 0x79208` |
| Japan-0 | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` | `0x8007D3D0 / 0x7DFD0` | `0x8007E038 / 0x7EC38` |

The **original MIPS shared-event entrypoint** (`func_8003D310_3DF10` in USA) indexes the pointer array by `event_id * 4` and the resource array by `event_id * 2`, then calls the VM event loader (`func_8003D468_3E068` in USA). The corresponding Japanese instructions load the regional tables above. These are code/data addresses specific to each ROM, **not** a `+0x57F0` field crosswalk.

The pointer-to-resource-table span is `0xC68` bytes = **794 slots** in each region. The authenticated original tables yielded **508 paired registered events** and **286 empty events** per region, with **zero** mismatched event IDs, resource IDs, segment prefixes, pointer alignment or out-of-resource offsets. **505** registered pointers use segment `0x08`; **three** use `0x09` (events 791–793, resource 81). A registered slot is *not* proof an NPC/actor ever launches it during ordinary gameplay. Script offsets below are **relative to their own regional decompressed resource**, never global ROM or guest-RAM addresses.

## Registered progression entrypoints

| Event ID | Resource | USA resource-relative start | Japanese resource-relative start | Evidence |
| --- | --- | --- | --- | --- |
| **202** | 94 | `+0x4B70` | `+0x312C` | Acquisition script containing saved-flag `0x000` setter and subsequent inventory writes |
| **270** | 96 | `+0x8258` | `+0x50D0` | First gate-setting path, tests `0x000` then `0x001`, sets `0x001` |
| 271 | 96 | `+0x8318` | `+0x5198` | Distinct intervening dialogue; **not** the second gate-setting path |
| **272** | 96 | `+0x8420` | `+0x5290` | Second gate-setting path, tests `0x000` then `0x001`, sets `0x001` |
| 791 | 81, segment 9 | `+0xE4` | `+0x68` | JP resource includes unique set/clear/test commands, registration verified, launch unknown |
| 792 | 81, segment 9 | `+0x100` | `+0x7C` | Registered text/script entry |
| 793 | 81, segment 9 | `+0x11C` | `+0xA4` | Registered text/script entry |

The entire 508-row directory was exported as read-only CSV locally and validated against both original file tables. It is not a universal script CFG: callbacks and VM jumps can redirect program control outside the lexical range between entrypoints.

## Original event 202 sets both the receipt flag and Super Pass inventory

At **USA resource 94 `+0x4CA0` / JP `+0x325C`**, both original script streams have the identical semantic sequence:

| Offset from receipt-flag setter | Script command | USA target | JP target | What original VM implementation does |
| --- | --- | --- | --- | --- |
| `+0x00` | `0x8020, 0x000` | Saved bit `0x8015C608 & 0x01` | Saved bit `0x80161DF8 & 0x01` | Set bit ID 0 through the native bank-C setter |
| `+0x08` | `0x8004, address, 0x8009, 1` | `0x8015C700` | `0x80161EF0` | Assign **32-bit word** = 1; editor's Super Pass item byte is the low byte at `...703 / ...EF3` |
| `+0x18` | `0x8004, address, 0x8013, 1` | `0x8015C89C` | `0x8016208C` | Increment **32-bit saved word** by 1; precise meaning unknown |
| `+0x28` | `0x8004, address, 0x8009, 1` | `0x8015C81C` | `0x8016200C` | Assign **32-bit saved word** = 1; precise meaning unknown |

The assignment semantics come from accepted USA `decomp/script_vm.c` `func_8003DB0C_3E70C` and the original dispatch for `0x8004`. The flag-set semantics come from the original `0x8020` → native saved-event setter. Four exact script anchors were checked in each authenticated ROM; Japanese fields are verified by their **own original script operand**, not just an address delta.

Event 202 begins before the setter in both regional tables and ends after it. Prior commands include dialogue and a callback-driven wait, so this is a **script-defined acquisition path**, not proof that every invocation reaches the setter under all runtime conditions. The script itself establishes the immediate ordered flag/inventory updates once the VM continues to those commands.

## Original events 270 and 272 set gate flag 0x001

| Original command | USA event 270 | JP event 270 | USA event 272 | JP event 272 |
| --- | --- | --- | --- | --- |
| Test prerequisite `0x000` (`0x8022`) | `+0x8260` | `+0x50D8` | `+0x8428` | `+0x5298` |
| Test gate `0x001` (`0x8022`) | `+0x82C0` | `+0x5138` | `+0x8470` | `+0x52E0` |
| Set gate `0x001` (`0x8020`) | `+0x8304` | `+0x5184` | `+0x84BC` | `+0x532C` |

The `0x8022` branch targets to the next listed test were verified word-for-word. The test of gate bit `0x001` branches **past** the setter if it is already set, so the first-time sequence only sets a new gate bit when necessary. This is consistent with the user's **one-event JP capture** from 2026-11-17T19:34:40Z (recomp: `0x80161DF8 & 0x02` set after speaking to guards, door observed open); there were no idle or control trials in that report. USA and Japan file-51 native gate-object functions independently read flag `0x001`, as documented in [the prior Phase 1 report](PHASE1_SAVED_EVENT_FLAG_TRACE_20261117.md).

**Byte-level distinction:** both flags occupy `0x8015C608` (USA) / `0x80161DF8` (JP), with **mask 0x01** (Super Pass-related event ID 0) and **mask 0x02** (gate event ID 1). The bit-0 prerequisite is not an instruction to clear bit 0: if both are present the byte may be `0x03`.

## Computed flags and gaps

- **Generic actor-supplied saved-event IDs:** USA resource 43 `+0x1020` (JP also `+0x1020`) loads `u16 actor[+0xD4]` and `u16 actor[+0xD6]` as arguments to native saved-event testers. When the `+0xD6` condition succeeds and the `+0xD4` condition does not, the routine calls the **bank-C setter with the actor's `+0xD4` halfword** (USA `+0x10C8`, JP same). This is an **original native computed-ID writer**, not a literal `flag_id` constant, and explains why the earlier literal-only reference count underreports real native flag use. The actor's initial `+0xD4/+0xD6` values must be identified before assigning it to a specific torch or story flag. Other actor-side effects differ across USA and JP; do not claim full semantic equality from just this argument pattern.
- **Ghost Toys conditions:** Original file 43 `0x19A` and `0x19B` tester calls and conditional `0x19C` setter are already proven in both regions. USA file 60 has a clearing sequence for `0x199/0x19A/0x19B`, showing another original native **clearer** of the two prerequisites, not their acquisition writer. The actual original setter(s) of the two prerequisites remain unresolved.
- **Mr. Arrow ID `0x104`:** USA file 77 has `li a0, 0x104` followed by **`func_8003D310_3DF10` (launch event 260)**, **not** the saved-event setter. The event dispatch table resolves event 260 to resource 95, USA `+0x33D4`, JP `+0x250C`. Numerically equal *event ID 260* and *saved flag ID `0x104`* are **distinct namespaces**. No native/script setter of that particular packed bit is established yet.
- **Japanese resource 81:** JP event 791 text/script stream includes `+0x84: 0x8020,0x081`, `+0x8C: 0x8021,0x142`, and `+0x94: 0x8022,0x081,0x09000068`. The original event directory proves registration, but does not establish real gameplay invocation. USA event 791 instead starts at `+0xE4` in different script data.

## Verification and limits

**Actually executed:** authenticated both original decompressed 32 MiB ROM SHA-1s; checked all 794 directory slots in both regions (508 valid registered, 286 empty, no invalid entries); checked the event 202 flag/inventory operations and events 270/272 tests/branch targets/setters in both original resources; checked JP file-81 script anchors. A separate **six-test ROM-free unit suite passed**, covering regional pairings, segment 9, invalid targets, mismatched resource IDs, exact byte anchors and wrong-ROM rejection. The private-ROM runner produced the complete 508-row CSV. The two user-uploaded 36,928-byte `.n64` save files were also compared and are **byte-identical**, so they provide no differential event evidence; no saves were published.

**Not executed:** local full `decomp.local_ci`, native IDO C compilation, new full-ROM G2/ELF inventory, runtime VM instruction tracing or live control trials. **No new C promotions.** Canonical accepted baseline at this work's start: **USA 779 C / 34,288 bytes; JP 34 C / 1,912 bytes**.

**Remaining:** Establish native actor parameter `+0xD4/+0xD6` initialization and the setters of Ghost Toys flags `0x19A/0x19B`; establish an actual *packed flag* writer for Mr. Arrow `0x104`; prove which actor calls start events 202, 270 and 272; test JP event 791 reachability only with targeted read-only runtime capture.
