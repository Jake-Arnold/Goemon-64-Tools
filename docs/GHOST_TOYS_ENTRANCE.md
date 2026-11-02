# Ghost Toys entrance: torches and unlocked door

Date: 2026-11-02. User gameplay observations plus read-only native-code trace.

## Reported observations

At `0x8015C63B`, the user reports values `2 -> 10 -> 30` when lighting the left
fire first, or `2 -> 6 -> 30` when lighting the right first. At completion the
entrance opens and its loading zone appears. Manually setting `16` opens the
door without flames. The state is reported permanent once lit.

The user confirms those values are decimal. Thus the hex sequences are
`02 -> 0A -> 1E`, `02 -> 06 -> 1E`, and manual `10`. Left is mask `08`, right
is mask `04`; the door latch is `10`. The initial `02` remains present during
normal lighting. Persistence is user-reported; no new save/reload experiment
was performed by the assistant.

## Original native code

Input: verified decompressed US ROM SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`, pinned mnsg baseline
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

The saved-event accessor maps these IDs into the same byte:

| ID | Address | Mask | Code-supported role |
| --- | --- | --- | --- |
| `0x19A` | `0x8015C63B` | `04` | One torch condition |
| `0x19B` | `0x8015C63B` | `08` | Other torch condition |
| `0x19C` | `0x8015C63B` | `10` | Entrance-unlocked latch |

In `func_08006490_6F9970` (file `0x02B`, `asm/usa/file_43.s`), the saved-bank
helper tests ID `0x19A` at ROM `0x6F998C`; a zero result returns without unlocking.
The same helper pointer tests `0x19B` at `0x6F999C`, with the same zero-result
exit. Only if both pass does the function set `0x19C` at `0x6F99B0`. It then
sets bit 0 in the task word at offset `0x60`, calls a helper with argument
`0x224`, and switches the callback to `func_0800651C_6F99FC`. The full animation,
sound and loading-zone helper semantics are not claimed by this short trace.

Separately, `func_08005D18_6F91F8` tests ID `0x19C` at ROM `0x6F92CC`, and
`func_080063C0_6F98A0` tests it at `0x6F9914`. This establishes a latch reader
separate from the two torch conditions, supporting the user's manual-open result.
It does not prove full door/collision/loading-zone equivalence from that bit alone.

Existing mn64rando annotations at pin
`9c580d03fe89354f79c3c83ba2e1bcf192f32577` identify Ghost Toys Torch actor
`0x195` in file `0x028` and Ghost Toys Entrance Barricade `0x3C8` in file
`0x02B`; the checked saved-flag dictionary does not name these IDs. Actor IDs and
saved flag IDs are separate namespaces, even if their numbers overlap.

The literal-call scanner catches the first torch test and latch setter but misses
the second torch test through the reused helper pointer. Manual assembly inspection
covers that gap. Other `0x19D` and `0x19E` references in nearby modules have not
been assigned to this mechanism merely because their IDs are adjacent.

## Toolkit and next steps

Story progress exposes the two torch masks and door latch independently. No
whole-byte presets or automatic writes were added. The initial mask `02` has no
assigned meaning; preserve it and all unrelated bits in any manual experiment.

Trace torch writers and
the remaining entrance callback/exit setup. Keep persistence observations separate
from inferred behavior. This is semantic reverse engineering, not a new verified
matching-C function. No assistant game writes were performed.
