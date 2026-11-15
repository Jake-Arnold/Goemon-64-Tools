# Japan-0 Project64: live read-only Value Search and A/B/C evidence

**Date:** 2026-11-15  
**Source:** Four user-provided Windows screenshot attachments in the ongoing Goemon project conversation. The repository contains this **transcription/analysis**, not the original binary PNG attachments; retain the screenshots in the conversation for visual verification.  
**Environment reported:** Windows, Project64, Goemon Practice Toolkit v0.11.17, selected `Japan - Ganbare Goemon`, branch `chatgptweb/japan-controlled-party-writes`. The exact PID, host RAM base, actual 4-vs-8-MiB mapping and ROM hash are **not shown** in these frames.
**Validation scope:** User confirms the expanded PowerShell test suite passes and explicitly reports that Value Search and A/B/C comparison work in live gameplay. The screenshots substantiate the GUI outputs below; no claim of an independently run emulator test by the assistant.

## Screenshot inventory and direct observations

| User-uploaded filename | Surface | Directly visible evidence |
| --- | --- | --- |
| `image(20261115-143753).png` | Japan Live read-only custom watch | `Value Search 0x80161DDA`: address `0x80161DDA`, `u16`, current value **95**, raw `0x005F`, status `CUSTOM: u16, unverified`. |
| `image(20261115-143809).png` | Value Search | Type `u16`; number field `97`; next filter `Decreased`; **5 snapshots**, **1 surviving candidate**; sole row `0x80161DDA`, displayed value **93**, raw big-endian `0x005D`. Status: `No game memory was modified.` |
| `image(20261115-143825).png` | Scene / boss investigation context | Scene and gameplay values listed below; the panel reads them without a valid player object. |
| `image(20261115-143906).png` | Event sessions → Advanced RAM comparison | Test selection **Scene transition**, range **focused**. Report: **2 regions**, **22 byte changes**, **2 displayed candidates**. Both candidates show `C matched A? yes`; values listed below. No Japanese event-bank semantics claimed by GUI. |

### Value Search — changing Ryo candidate

- `0x80161DDA` was found with a read-only `u16` numeric search and narrowed through five snapshots/Decreased filters to **one candidate**.
- A separate Japan Live custom watch at the same address displays `95` / `0x005F`; the Value Search screenshot displays `93` / `0x005D`. The UI's search input reads `97`. These observations are **different instants**, consistent with a changing counter; neither screenshot alone proves the complete `97 → 95 → 93` temporal ordering.
- The field matches the previously published Japanese Ryo lead and provides strong live evidence that `0x80161DDA` is the **current money/Ryo count candidate** on this Japan-0 session. The screenshots do not independently show the in-game currency HUD or exact transaction that caused the decrease.
- The promoted watch remains **`CUSTOM: u16, unverified`** in the UI. Promotion from a scan never turns a candidate into a safe writable field.

### Scene / boss investigation — read-only context

| Field | Observed raw/decoded value | GUI evidence classification |
| --- | --- | --- |
| `scene_map` | `353 / 0x161` — **Oedo Town (South) [0161]** | OBSERVED: two JP scene transitions |
| `scene_phase` | `1 [01]` | UNVERIFIED: regional-offset hypothesis |
| `scene_submode` | `2` — town (candidate) `[02]` | OBSERVED: one JP submode change |
| `scene_previous` | `465 / 0x1D1` — **South Oedo - Goemon's House [01D1]** | OBSERVED: two JP scene transitions |
| `scene_pending` | `353 / 0x161` — **Oedo Town (South) [0161]** | OBSERVED: two endpoint traces; timing unknown |
| `scene_transition` | `0 [00]` | UNVERIFIED: regional-offset hypothesis |
| `scene_exit` | `0 [00]` | UNVERIFIED: regional-offset hypothesis |
| `scene_pause` | `0 [00]` | UNVERIFIED: regional-offset hypothesis |
| `scene_character` | **Goemon (0)**, `00000000` | CONFIRMED: Goemon/Ebisumaru both directions from earlier traces |
| `scene_loading` | `0 [00000000]` | UNVERIFIED: regional-offset hypothesis |

This is evidence that the scene-context reader and its region-specific labels render on Windows. It does not establish the unverified fields' meaning or a functioning scene-warp control.

### Focused Advanced A/B/C comparison

In **Event sessions → Advanced RAM comparison**, the screenshot shows a three-capture comparison under `Scene transition`, `focused` range, with two candidate bytes among **22 raw byte changes across two regions**.

| Japan guest address | Reported region | A (before) | B (after) | XOR mask | C matched A? | Reported potential type |
| --- | --- | --- | --- | --- | --- | --- |
| `0x80161DCF` | `jp_inventory_candidates` | `00` | `01` | `01` | **yes** | Boolean candidate |
| `0x80161DBD` | `jp_inventory_candidates` | `0B` | `09` | `02` | **yes** | One-bit candidate |

The columns prove that the GUI can capture and compare **A→B changes with C returning to A** on the same Japanese read-only RDRAM session. The first candidate is a 0→1 bit change; the second clears bit `0x02`. Both are **hypotheses**. No event flag, storyline meaning, or safe write permission has been established from these screenshots.

## What is now validated versus still open

**User-confirmed live Windows functionality:**

- PowerShell synthetic/Tk regression suite passed (reported earlier; raw log not attached).
- Japan Live can add and read typed custom watch values for `0x80161DCC` (`u32=0`, Goemon) and `0x80161DDA` (`u16`, displayed as 95).
- Value Search reads Japanese live RAM, narrows decreasing `u16` values, yields one `0x80161DDA` candidate after five snapshots, and promotes a result into Japan Live.
- Scene / boss investigation reads and displays Japanese context fields.
- Focused read-only Advanced A/B/C comparison produces reversible candidates with raw A/B/XOR/C columns.

**Not established by this evidence:**

- 4 MiB vs 8 MiB detected mapping, exact host address, active process PID, or actual ROM revision digest (although the user reports a successful connection).
- Full **wide-range** A/B/C capture, exported comparison JSON, sustained performance or scan correctness during scene loading and emulator reset.
- Semantic identification of `0x80161DCF` or `0x80161DBD` as game flags, despite reversible changes.
- Project64 savestate save/load rollback, dynamic Sasuke/Yae switching, or Project64-specific party-write verification.
- Japanese player/task pointer, XYZ, scene warping, mapped event banks, and general-purpose Japanese writes.

**Safety:** This milestone uses no newly approved Japanese RAM writes. The existing Sasuke/Yae-only write opt-in remains unchanged. Keep the Project64 feature PR as draft pending savestate and dynamic character switch evidence.
